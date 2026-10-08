# -*- coding: utf-8 -*-
"""CSCE 748 — Modules 03-07."""

MODULES = [

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "High Dynamic Range",
 "subtitle": "Measuring more range than one exposure can hold.",
 "question": "How do you photograph a scene brighter than your sensor?",
 "outcomes": [
     "Explain dynamic range and where a single exposure fails.",
     "Recover a camera response curve from bracketed exposures.",
     "Merge exposures into a radiance map with justified weights.",
     "Handle ghosting from moving subjects.",
     "Explain how modern cameras avoid bracketing entirely.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The range problem",
   "blurb": "Scenes are wider than sensors."},

  {"t": "table", "kicker": "Range", "title": "Dynamic range, in stops",
   "header": ["", "Range", "Note"],
   "widths": [4.0, 3.2, 4.9],
   "rows": [
     ["<b>A real scene (sunlit room)</b>", "<b>~20+ stops</b>", "Window to shadow"],
     ["Human eye, fixed adaptation", "~10–14 stops", "More over time, by adapting"],
     ["<b>Camera sensor, one exposure</b>", "<b>~10–14 stops</b>", "<b>Good sensors; less at high ISO</b>"],
     ["8-bit display image", "~8 stops", "What you can actually show"],
     ["Print", "~6–7 stops", "Less still"],
   ],
   "footnote": "<b>A stop is a factor of two.</b> 20 stops is a ratio of a "
               "million to one.",
   "note": "The display row is the one that matters for Module 04 — even "
           "a perfect capture must be compressed to show it."},

  {"t": "callout", "title": "One exposure forces a choice",
   "kind": "Why bracketing exists",
   "body": ["<b>Expose for the highlights and the shadows go black.</b> "
            "Expose for the shadows and the highlights clip to white.",
            "<b>Clipped highlights are unrecoverable</b> — every pixel "
            "reads the same saturation value and the information is gone.",
            "<b>Crushed shadows are nearly as bad</b>, because what little "
            "signal there is sits below the read noise.",
            "<b>So: take several exposures and combine them.</b> Each one "
            "measures a different part of the range well, and together they "
            "cover the scene."]},

  {"t": "section", "label": "Part 2", "title": "The response curve",
   "blurb": "Undoing the camera's interpretation."},

  {"t": "callout", "title": "If you have raw, you may not need this",
   "kind": "An important caveat",
   "body": ["<b>Raw values are already linear</b> (Module 01), so merging "
            "is straightforward scaling and averaging.",
            "<b>The response curve problem exists because of JPEGs</b>, "
            "where an unknown non-linear tone curve has been applied.",
            "<b>Debevec and Malik's method recovers that curve</b> from the "
            "exposures themselves, which was essential in 1997 and is "
            "optional now.",
            "<b>It is still worth understanding</b>, because the same "
            "structure — recover an unknown transform from redundant "
            "measurements — recurs throughout computational photography."]},

  {"t": "eq", "kicker": "Debevec-Malik", "title": "Recovering the response",
   "eqs": [
     ("Z_ij = f( E_i · Δt_j )",
      "Pixel value Z at location i in exposure j is the response f applied "
      "to radiance times exposure time."),
     ("g(Z) = ln f⁻¹(Z) = ln E_i + ln Δt_j",
      "Take logs and define g. Now it is linear in the unknowns: g at each "
      "of 256 levels, and ln E at each sample location."),
     ("minimise  Σ w(Z)[g(Z_ij) − ln E_i − ln Δt_j]²  +  λ Σ w(z) g″(z)²",
      "Least squares, with a smoothness term on g and weights that "
      "down-weight unreliable extreme values."),
   ],
   "caption": "An overdetermined linear system: many pixels, many "
              "exposures, 256 unknowns in g. Solved with SVD.",
   "note": "The trick of taking logs to linearise is the whole idea. Make "
           "sure that step is clear."},

  {"t": "callout", "title": "Weight by reliability",
   "kind": "The detail that makes merging work",
   "body": ["<b>Pixels near 0 are dominated by read noise.</b> Pixels near "
            "saturation may be clipped. Neither is trustworthy.",
            "<b>Mid-range values are the reliable ones</b> — enough "
            "signal, no clipping.",
            "<b>So weight each contribution by a hat function</b> peaking "
            "in the middle and falling to zero at both ends.",
            "<b>Better weights use the noise model</b> (Module 01): weight "
            "by inverse variance, which for shot noise means weighting "
            "brighter measurements more. This is the principled version."]},

  {"t": "section", "label": "Part 3", "title": "Ghosting",
   "blurb": "What happens when the scene moves."},

  {"t": "callout", "title": "Anything that moves appears several times",
   "kind": "The practical problem",
   "body": ["<b>Merging assumes the exposures are of the same scene.</b> A "
            "person who walks between frames appears as a semi-transparent "
            "repetition.",
            "<b>Leaves, water, traffic, and people are the usual "
            "culprits</b> — and almost every real scene has one.",
            "<b>Detection:</b> compare each exposure against a reference "
            "after scaling for exposure time; large disagreement means "
            "motion.",
            "<b>Resolution:</b> in moving regions, take all the data from "
            "one exposure rather than blending — accepting more noise "
            "there in exchange for consistency."]},

  {"t": "bullets", "kicker": "Approaches", "title": "Deghosting strategies",
   "items": [
     "<b>Reference-based selection.</b> Pick a reference exposure; in "
     "disagreeing regions, use only data consistent with it. Simple and "
     "effective.",
     "",
     "<b>Median-based.</b> With enough exposures, the median is robust to "
     "objects that appear in a minority of frames.",
     "",
     "<b>Optical flow alignment.</b> Warp the exposures into "
     "correspondence. Powerful and it fails on occlusion boundaries.",
     "",
     "<b>Patch-based synthesis.</b> Fill moving regions with consistent "
     "content from elsewhere.",
     "",
     "<b>Or shoot a single raw</b> and avoid the problem, which is "
     "increasingly the answer.",
   ],
   "note": "The last bullet is the honest one — modern sensors often have "
           "enough range that bracketing is unnecessary."},

  {"t": "section", "label": "Part 4", "title": "What cameras actually do now",
   "blurb": "Bracketing has largely been replaced."},

  {"t": "callout", "title": "Modern HDR does not bracket exposures",
   "kind": "How the field moved",
   "body": ["<b>HDR+ and its successors capture a burst of "
            "<i>identically</i> underexposed raw frames</b> — all short, "
            "all dark.",
            "<b>Underexposing protects the highlights</b>, which is the "
            "unrecoverable failure. Nothing clips.",
            "<b>Averaging the burst recovers the shadows</b>, because SNR "
            "improves as √n (Module 01). The noise that made "
            "underexposure unusable is averaged away.",
            "<b>And identical exposures align far better than bracketed "
            "ones</b>, so ghosting is much easier to handle. <b>This is why "
            "phone HDR works so well</b>, and Module 10 covers it in "
            "full."]},

  {"t": "table", "kicker": "Comparison", "title": "Bracketing and burst",
   "header": ["", "Exposure bracketing", "Underexposed burst"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Frames", "3–9, very different", "<b>10–15, identical</b>"],
     ["Highlights", "Need the short frame", "<b>Never clipped</b>"],
     ["Shadows", "From the long frame", "<b>From averaging</b>"],
     ["Alignment", "<b>Hard — frames look different</b>", "<b>Easy — frames match</b>"],
     ["Motion", "Long frame has blur", "<b>All frames short; no blur</b>"],
     ["Total time", "Long — the long exposure dominates", "<b>Short</b>"],
   ],
   "footnote": "The burst approach wins on every row, which is why it "
               "replaced bracketing in consumer cameras.",
   "note": "Worth being direct: bracketing is now mostly a teaching "
           "exercise and a landscape-photography technique."},
 ],
 "takeaways": [
   "A sunlit scene spans 20+ stops; a sensor captures 10–14 and a "
   "display shows about 8. Something must be compressed.",
   "Clipped highlights are unrecoverable because every pixel reads the same "
   "saturation value; crushed shadows sit below the read noise.",
   "Debevec–Malik recovers an unknown response curve by taking logs to "
   "linearise, then solving an overdetermined least-squares system.",
   "With raw you may not need it — raw is already linear, and the "
   "response curve problem is an artefact of merging JPEGs.",
   "Weight contributions by reliability: mid-range values are trustworthy, "
   "and inverse-variance weighting from the noise model is the principled "
   "version.",
   "Modern cameras capture a burst of identically underexposed raws instead "
   "of bracketing — highlights never clip and averaging recovers the "
   "shadows.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The dynamic range problem"),
  ("table", ["", "Dynamic range", "Note"],
   [["<b>A real scene</b> — a sunlit room with a window",
     "<b>20 stops or more</b>",
     "A ratio of a million to one between the brightest and darkest parts "
     "you care about. Outdoors with the sun in frame is far more."],
    ["<b>Human eye, at a fixed adaptation level</b>", "10–14 stops",
     "<b>Much more over time</b>, because the eye adapts — which is "
     "part of why a scene looks fine to you and wrong in a photograph."],
    ["<b>Camera sensor, single exposure</b>", "10–14 stops",
     "For a good modern sensor at base ISO. Considerably less at high ISO, "
     "because the noise floor rises."],
    ["<b>8-bit display image</b>", "~8 stops",
     "<b>What you can actually show.</b> This is the constraint Module 04 "
     "exists to address."],
    ["<b>Print</b>", "6–7 stops", "Less still, and it depends on the "
     "paper and the viewing light."]],
   [0.28, 0.20, 0.52]),
  ("p", "<b>A stop is a factor of two in light.</b> Twenty stops is a "
        "ratio of about a million to one, and the display can show perhaps "
        "two hundred and fifty. <b>Compression is therefore not optional</b>, "
        "and the only question is how it is done — which is "
        "Module 04."),
  ("callout", "A single exposure forces a choice",
   ["<b>Expose for the highlights and the shadows fall below the noise "
    "floor.</b> Expose for the shadows and the highlights clip.",
    "<b>Clipped highlights are unrecoverable.</b> Every pixel in a clipped "
    "region reads the same saturation value, so the relative brightness "
    "information within it has been destroyed rather than merely "
    "compressed. No processing recovers it, and attempts to do so invent "
    "detail.",
    "<b>Crushed shadows are nearly as bad</b> — the signal is present "
    "but buried in read noise, and lifting it amplifies the noise with it "
    "(Module 01).",
    "<b>So: capture several exposures and combine them.</b> Each exposure "
    "measures a different portion of the scene's range well, and together "
    "they cover it."]),

  ("h1", "2 &nbsp; Recovering the response curve"),
  ("callout", "With raw files you may not need this at all",
   ["<b>Raw values are already linear in scene radiance</b> (Module 01), so "
    "merging exposures is a matter of dividing each by its exposure time and "
    "taking a weighted average. No curve recovery is required.",
    "<b>The response curve problem exists because of JPEGs</b>, to which the "
    "camera has applied an unknown, proprietary, non-linear tone curve. "
    "Merging those requires inverting it first, and nobody publishes it.",
    "<b>Debevec and Malik's 1997 method recovers the curve from the "
    "exposures themselves</b>, which was essential when raw capture was rare "
    "and is largely optional now.",
    "<b>It remains worth understanding</b>, because the structure of the "
    "problem — recover an unknown transform from redundant, "
    "overlapping measurements — recurs constantly in computational "
    "photography, and this is its cleanest instance."]),
  ("eq", "Z<sub>ij</sub> = f( E<sub>i</sub> &middot; "
         "&Delta;t<sub>j</sub> )"),
  ("p", "The value Z at pixel location i in exposure j is the camera's "
        "response f applied to the product of the scene irradiance "
        "E<sub>i</sub> at that location and the exposure time "
        "&Delta;t<sub>j</sub>. Both f and E are unknown; only Z and "
        "&Delta;t are known."),
  ("eq", "g(Z) &equiv; ln f<super>&minus;1</super>(Z) = ln E<sub>i</sub> + "
         "ln &Delta;t<sub>j</sub>"),
  ("p", "<b>Taking logarithms is the whole trick.</b> It converts a product "
        "into a sum and makes the problem <i>linear in the unknowns</i> "
        "— the 256 values of g (one per possible pixel level) and the "
        "log-irradiance at each sampled location. With many pixels across "
        "many exposures this is massively overdetermined."),
  ("eq", "min &Sigma; w(Z)[ g(Z<sub>ij</sub>) &minus; ln E<sub>i</sub> "
         "&minus; ln &Delta;t<sub>j</sub> ]&#178; + &lambda; "
         "&Sigma; w(z) g&Prime;(z)&#178;"),
  ("p", "A weighted least-squares problem, solved by SVD. The second term "
        "penalises curvature in g, enforcing the reasonable prior that a "
        "camera response is smooth — without it the solution is "
        "underdetermined at levels that appear rarely."),
  ("callout", "Weight by reliability",
   ["<b>Pixel values near zero are dominated by read noise</b> and carry "
    "little information. <b>Values near saturation may be clipped</b>, in "
    "which case they are actively misleading rather than merely noisy.",
    "<b>Mid-range values are the reliable ones</b> — enough signal to "
    "be well above the noise floor, and far enough from saturation to be "
    "unclipped.",
    "<b>So weight each measurement by a hat function</b> that peaks in the "
    "middle of the range and falls to zero at both ends. This is Debevec and "
    "Malik's choice and it works well.",
    "<b>The principled version uses the noise model from Module 01:</b> "
    "weight by inverse variance. Since shot noise is &radic;N, a brighter "
    "measurement has a better signal-to-noise ratio and deserves more "
    "weight — so the optimal weighting is asymmetric, favouring the "
    "brighter unclipped measurements rather than the middle. <b>This matters "
    "more than it sounds</b> and is what modern merging implementations "
    "do."]),

  ("break",),
  ("h1", "3 &nbsp; Ghosting"),
  ("callout", "Anything that moves appears several times",
   ["<b>Merging assumes every exposure is of the same scene.</b> A person "
    "who walks through the frame between the first and last exposure appears "
    "in the merged result as a semi-transparent repetition — a ghost, "
    "hence the name.",
    "<b>Leaves moving in wind, water, traffic, pedestrians, and clouds are "
    "the usual culprits</b>, and almost every real outdoor scene contains at "
    "least one of them. Ghosting is the normal case, not the exception.",
    "<b>Detection is straightforward in principle:</b> scale each exposure "
    "by its exposure time to bring it into a common radiance space, compare "
    "against a chosen reference, and flag regions of large disagreement that "
    "cannot be explained by noise or clipping.",
    "<b>Resolution involves accepting a loss.</b> In a region flagged as "
    "moving, take all the data from a single exposure rather than blending "
    "— which means more noise there, or clipped highlights there, in "
    "exchange for a consistent image. <b>There is no way to have both</b>, "
    "because the different exposures genuinely recorded different scenes."]),
  ("ul", ["<b>Reference-based selection.</b> Choose one exposure as the "
          "reference for structure; in regions that disagree with it, use "
          "only data consistent with that reference. Simple, robust, and the "
          "usual approach.",
          "<b>Median-based merging.</b> With enough exposures, taking a "
          "median rather than a mean is robust to objects appearing in a "
          "minority of frames — a person who crosses the frame once in "
          "nine exposures simply vanishes.",
          "<b>Optical flow alignment.</b> Estimate dense motion between "
          "exposures and warp them into correspondence, so that moving "
          "objects are merged correctly rather than excluded. <b>Powerful, "
          "and it fails at occlusion boundaries</b> where there is no "
          "correspondence to find.",
          "<b>Patch-based synthesis.</b> Fill the moving regions with "
          "plausible content assembled from elsewhere in the exposure stack. "
          "Effective and it is synthesis rather than measurement, which "
          "Module 13 takes up.",
          "<b>Or capture a single raw frame and avoid the problem.</b> With "
          "14 stops of sensor range this is increasingly viable for ordinary "
          "scenes, and it is the honest answer for a great many cases where "
          "people still bracket out of habit."]),

  ("h1", "4 &nbsp; What cameras actually do now"),
  ("callout", "Modern HDR does not bracket exposures",
   ["<b>HDR+ and its successors capture a burst of <i>identically</i> "
    "underexposed raw frames</b> — ten to fifteen of them, all short, "
    "all deliberately dark.",
    "<b>Underexposing protects the highlights</b>, which is the "
    "unrecoverable failure mode from &sect;1. Nothing clips, so nothing is "
    "lost.",
    "<b>Averaging the burst recovers the shadows.</b> Signal-to-noise "
    "improves as &radic;n (Module 01), so fifteen frames gives roughly a "
    "fourfold improvement — enough to make the deliberately dark "
    "exposure usable. <b>The noise that made underexposure unacceptable is "
    "averaged away</b>, and the highlights were never in danger.",
    "<b>And identical exposures align far better than bracketed ones.</b> "
    "Alignment between a bright frame and a dark one is genuinely hard "
    "because the images look different; alignment between fifteen nominally "
    "identical frames is comparatively easy. So ghosting becomes tractable "
    "rather than fundamental. <b>This is why phone HDR works as well as it "
    "does</b>, and Module 10 covers the pipeline in full."]),
  ("table", ["", "Exposure bracketing", "Underexposed burst"],
   [["Frames", "3 to 9, spanning several stops.",
     "<b>10 to 15, nominally identical.</b>"],
    ["Highlights", "Preserved only by the shortest exposure.",
     "<b>Never clipped at all.</b>"],
    ["Shadows", "From the longest exposure, which is noisy or blurred.",
     "<b>Recovered by averaging.</b>"],
    ["Alignment", "<b>Hard</b> — the frames genuinely look different, "
     "so feature matching is unreliable.",
     "<b>Easy</b> — the frames match, so simple block alignment "
     "works."],
    ["Motion", "The long exposure carries motion blur.",
     "<b>Every frame is short, so no blur in any of them.</b>"],
    ["Total capture time", "Dominated by the longest exposure — "
     "potentially a second or more.",
     "<b>Short</b>, because every frame is short."]],
   [0.15, 0.42, 0.43]),
  ("p", "<b>The burst approach wins on every row</b>, which is why it "
        "replaced bracketing in consumer cameras within a few years. "
        "Bracketing survives in landscape photography, where the scene is "
        "static and the camera is on a tripod, and as a teaching exercise "
        "— which is what Project 1 uses it for."),
 ],
 "resources": [
   ("Debevec & Malik &mdash; Recovering High Dynamic Range Radiance Maps "
    "from Photographs (1997, free)",
    "https://www.pauldebevec.com/Research/HDR/",
    "The paper. The log-linearisation of &sect;2 and the weighting scheme, "
    "in the original, and still clearly written."),
   ("Hasinoff et al. &mdash; Burst photography for HDR and low-light "
    "imaging (free, with dataset)",
    "https://hdrplusdata.org/",
    "The &sect;4 approach, documented by the team that shipped it, with a "
    "dataset of raw bursts to work on."),
   ("CMU 15-463 &mdash; HDR imaging lecture and assignment (free)",
    "http://graphics.cs.cmu.edu/courses/15-463/",
    "The merging assignment, which is essentially Project 1's HDR "
    "requirement."),
   ("Tursun et al. &mdash; The State of the Art in HDR Deghosting (free)",
    "https://diglib.eg.org/handle/10.1111/cgf12668",
    "A survey of &sect;3's techniques, with comparisons."),
 ],
 "exercises": [
   "Photograph a high-contrast scene at a single exposure and demonstrate "
   "that neither highlights nor shadows can be recovered afterwards.",
   "Capture a bracketed sequence on a tripod and recover the response curve "
   "by the Debevec–Malik method. Plot it.",
   "Merge the same sequence from raw, where no curve recovery is needed, and "
   "compare against the JPEG-derived result.",
   "Implement both the hat weighting and inverse-variance weighting, and "
   "compare the noise in the merged result.",
   "Capture a bracketed sequence with a person walking through it. "
   "Demonstrate the ghosting, then implement reference-based deghosting.",
   "Capture ten identically underexposed raw frames of a high-contrast "
   "scene. Average them and compare against a single correctly exposed "
   "frame.",
   "Measure the noise reduction from averaging n frames for n = 2, 4, 8, 16 "
   "and confirm the &radic;n relationship.",
   "Compare alignment difficulty between a bracketed set and an identical "
   "burst by running the same feature matcher on both.",
   "Compute the dynamic range of a scene you photograph, in stops, from the "
   "merged radiance map.",
 ],
 "selfcheck": [
   "Give the dynamic range of a scene, a sensor, and a display, and say "
   "which constraint Module 04 addresses.",
   "Why are clipped highlights unrecoverable?",
   "What does taking logarithms achieve in the Debevec–Malik "
   "formulation?",
   "Why might you not need response curve recovery, and why learn it "
   "anyway?",
   "Why weight by reliability, and what is the principled weighting?",
   "What causes ghosting, and why can it not be fully resolved?",
   "Name four deghosting approaches.",
   "Why does an underexposed burst beat exposure bracketing on every "
   "measure?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Tone Mapping",
 "subtitle": "Showing a million to one on a display that does two hundred.",
 "question": "How do you compress dynamic range without destroying the "
             "image?",
 "outcomes": [
     "Explain why tone mapping is underdetermined.",
     "Implement a global tone mapping operator.",
     "Implement a local operator and explain halos.",
     "Explain gradient-domain tone mapping.",
     "Evaluate tone mapping honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "There is no correct answer."},

  {"t": "callout", "title": "Tone mapping is underdetermined and therefore a choice",
   "kind": "The framing",
   "body": ["<b>You must map 20 stops onto 8.</b> Information will be "
            "lost; the only question is which.",
            "<b>There is no objectively correct mapping</b>, because the "
            "goal is not fidelity to the radiance — the display cannot "
            "produce it — but fidelity to the <i>impression</i>.",
            "<b>Which is a perceptual and aesthetic criterion</b>, not a "
            "numerical one.",
            "<b>So tone mapping operators are proposals</b>, evaluated by "
            "how images look, and the literature is correspondingly "
            "unsettled. This is the same honest position as CSCE 647's tone "
            "mapping section, reached from the capture side."]},

  {"t": "two", "kicker": "Two families", "title": "Global and local operators",
   "lh": "Global (tone curve)",
   "l": ["One function applied to every pixel.",
         "<b>Same input value &rarr; same output value</b>, everywhere.",
         "<b>No halos, no artefacts</b>, and fast.",
         ("Cannot preserve local contrast in both highlights and "
          "shadows.", 1),
         "Reinhard global, gamma, filmic curves."],
   "rh": "Local (spatially varying)",
   "r": ["The mapping depends on the neighbourhood.",
         "<b>Dark regions brightened, bright regions compressed</b>, "
         "independently.",
         "<b>Preserves local contrast everywhere.</b>",
         ("<b>Halos</b> at strong edges, and it can look unnatural.", 1),
         "Durand–Dorsey, Fattal, exposure fusion."],
   "note": "The halo problem is the defining difficulty of local operators "
           "and the reason edge-aware filters matter here."},

  {"t": "section", "label": "Part 2", "title": "Global operators",
   "blurb": "Simple, safe, and limited."},

  {"t": "eq", "kicker": "Reinhard", "title": "A global operator",
   "eqs": [
     ("L_scaled = (a / L̄) · L",
      "Scale by a key value a divided by the log-average luminance, which "
      "sets the overall exposure."),
     ("L_display = L_scaled / (1 + L_scaled)",
      "The compressive curve. Maps [0,∞) to [0,1), so nothing ever "
      "clips."),
     ("with white point:  L(1 + L/L_white²) / (1 + L)",
      "Allows very bright values to burn out deliberately, which often "
      "looks better than compressing everything."),
   ],
   "caption": "Three lines, no parameters to speak of, and it never fails. "
              "Which is why it remains a reasonable default.",
   "note": "The log-average luminance is the standard way to set exposure "
           "automatically and is worth knowing."},

  {"t": "callout", "title": "Operate on luminance, not on colour channels",
   "kind": "The mistake that desaturates everything",
   "body": ["<b>Applying a compressive curve to R, G, and B "
            "independently</b> compresses the differences between them.",
            "<b>So saturated colours desaturate</b> as they brighten, and "
            "bright regions drift toward white.",
            "<b>Instead: compute luminance, tone map it, and scale the "
            "colour channels by the ratio</b> of output to input "
            "luminance.",
            "<b>Then apply a saturation correction</b> — a power on the "
            "chroma — because compressing luminance reduces perceived "
            "colourfulness even when the ratios are preserved."]},

  {"t": "section", "label": "Part 3", "title": "Local operators",
   "blurb": "More contrast, and the halo problem."},

  {"t": "callout", "title": "Halos are what happens when the base layer crosses an edge",
   "kind": "The characteristic artefact",
   "body": ["<b>Local operators split the image into a base layer "
            "(large-scale) and a detail layer</b>, compress the base, and "
            "recombine.",
            "<b>If the base layer is a Gaussian blur, it smears across "
            "strong edges</b> — so near a bright/dark boundary the base is "
            "wrong on both sides.",
            "<b>The result is a bright halo on the dark side and a dark "
            "halo on the bright side.</b>",
            "<b>The fix is an edge-aware base layer</b> (Module 02) "
            "— bilateral or guided filtering. <b>This is the main reason "
            "the bilateral filter was invented for graphics.</b>"]},

  {"t": "code", "kicker": "Durand-Dorsey", "title": "Bilateral tone mapping",
   "lang": "text", "code": """
  1. L = luminance of the HDR image
  2. log_L = log(L)

  3. base   = bilateral_filter(log_L)      <-- EDGE-AWARE, not Gaussian
     detail = log_L - base                     so no halos

  4. base_compressed = (base - max(base)) * compression_factor
                           ^ compress ONLY the base; detail is untouched

  5. log_out = base_compressed + detail
     L_out   = exp(log_out)

  6. restore colour:  RGB_out = (RGB_in / L) * L_out
                      then a saturation power

  Local contrast (the detail layer) is fully preserved.
  Only the large-scale range is compressed. That is the whole idea.
""",
   "caption": "Compress the base, keep the detail. The bilateral filter is "
              "what makes the decomposition respect edges.",
   "note": "The 'compress base, keep detail' structure recurs in nearly "
           "every local operator."},

  {"t": "callout", "title": "Gradient domain: compress the gradients instead",
   "kind": "A different formulation",
   "body": ["<b>Fattal's insight:</b> the problem is large gradients, "
            "because those are what exceed the display's range.",
            "<b>So attenuate large gradients and leave small ones "
            "alone</b> — compressing the big transitions while preserving "
            "texture.",
            "<b>Then integrate the modified gradient field</b> back into an "
            "image, by solving a Poisson equation (Module 08).",
            "<b>It handles enormous ranges gracefully</b> and is the same "
            "machinery as seamless cloning — which is why Module 08 "
            "follows this one."]},

  {"t": "section", "label": "Part 4", "title": "Evaluation",
   "blurb": "Judging something with no ground truth."},

  {"t": "bullets", "kicker": "Honesty", "title": "How to evaluate tone mapping",
   "items": [
     "<b>There is no ground truth image</b> — the display cannot show "
     "the radiance map, so there is nothing to compare against.",
     "",
     "<b>So comparisons are perceptual</b>, which means showing images "
     "side by side under controlled conditions and asking people.",
     "",
     "<b>Report the operator and its parameters.</b> A comparison between "
     "two renderers with different tone mapping is a comparison of tone "
     "mapping.",
     "",
     "<b>Show what was lost</b> — the clipped regions, the compressed "
     "ranges — rather than only the pleasing result.",
     "",
     "<b>And distinguish 'accurate' from 'preferred'.</b> They are "
     "measurably different and people usually prefer the less accurate one.",
   ],
   "note": "The accurate-versus-preferred distinction is well established "
           "and worth stating plainly."},

  {"t": "callout", "title": "HDR displays change the question",
   "kind": "Where this is going",
   "body": ["<b>A display capable of 1000+ nits and deep blacks needs far "
            "less compression</b> — perhaps 12 stops rather than 8.",
            "<b>So tone mapping becomes a smaller intervention</b>, and "
            "the content can be closer to the measurement.",
            "<b>But it does not disappear.</b> Scenes still exceed any "
            "display, and the mapping must now target a <i>range</i> of "
            "display capabilities.",
            "<b>Which is why HDR standards carry metadata</b> describing "
            "the content's range, letting each display decide — moving "
            "the decision to the last possible moment, exactly as "
            "CSCE 647 Module 13 recommended."]},
 ],
 "takeaways": [
   "Tone mapping is underdetermined: 20 stops must become 8, information is "
   "lost, and which to lose is a perceptual choice rather than a "
   "computation.",
   "Global operators apply one curve everywhere — no artefacts, and "
   "they cannot preserve local contrast in both highlights and shadows.",
   "Apply the curve to luminance and scale the colour channels by the "
   "ratio; per-channel compression desaturates as it brightens.",
   "Local operators split base from detail and compress only the base; a "
   "Gaussian base layer smears across edges and produces halos.",
   "An edge-aware base layer fixes halos, which is largely why the bilateral "
   "filter entered graphics.",
   "Gradient-domain tone mapping attenuates large gradients and integrates "
   "by solving a Poisson equation — the same machinery as seamless "
   "cloning.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why there is no correct answer"),
  ("callout", "Tone mapping is underdetermined, and therefore a choice",
   ["<b>Twenty stops of scene range must be mapped onto roughly eight stops "
    "of display range.</b> Information will be lost. The only question is "
    "which information, and that question has no answer derivable from the "
    "data.",
    "<b>There is no objectively correct mapping</b>, because the goal is not "
    "fidelity to the measured radiance — the display is physically "
    "incapable of reproducing it — but fidelity to the <i>impression</i> "
    "a viewer would have had of the original scene.",
    "<b>Which is a perceptual and ultimately aesthetic criterion</b>, not a "
    "numerical one. Two operators can both be defensible and produce "
    "visibly different images.",
    "<b>So tone mapping operators are proposals rather than solutions</b>, "
    "evaluated by how their output looks to people, and the literature is "
    "correspondingly unsettled after thirty years. <b>This is the same "
    "honest position CSCE 647's Module 13 reached from the rendering "
    "side</b>, and the two courses agree because it is a property of the "
    "problem rather than of either field."]),
  ("table", ["", "Global operators", "Local operators"],
   [["Mapping", "One function applied identically to every pixel.",
     "The mapping depends on the pixel's neighbourhood."],
    ["Consequence", "<b>The same input value always produces the same "
     "output value.</b> Order is preserved everywhere.",
     "<b>A dark region is brightened and a bright region compressed, "
     "independently</b> — so two pixels of equal radiance can map to "
     "different outputs."],
    ["Local contrast", "Necessarily reduced where the curve is flat "
     "— which is wherever it is doing the most compression.",
     "<b>Preserved throughout</b>, because only the large-scale component "
     "is compressed."],
    ["Artefacts", "<b>None.</b> Cannot produce halos or reversals.",
     "<b>Halos</b> at strong edges (&sect;3), and results can look "
     "unnatural or 'HDR' in the pejorative sense."],
    ["Examples", "Gamma, Reinhard global, filmic curves, ACES.",
     "Durand&ndash;Dorsey bilateral, Fattal gradient-domain, exposure "
     "fusion."]],
   [0.15, 0.42, 0.43]),

  ("h1", "2 &nbsp; Global operators"),
  ("eq", "L<sub>scaled</sub> = (a / L&#772;) &middot; L "
         "&nbsp;&nbsp;&nbsp;&nbsp; L<sub>display</sub> = "
         "L<sub>scaled</sub> / (1 + L<sub>scaled</sub>)"),
  ("p", "Reinhard's operator. The first step scales by a chosen <i>key</i> "
        "value a divided by the <b>log-average luminance</b> of the image, "
        "which sets the overall exposure automatically — the log "
        "average is used because perception of brightness is roughly "
        "logarithmic, so it corresponds to the subjective mid-tone. The "
        "second step applies a compressive curve mapping [0, &infin;) to "
        "[0, 1), so <b>nothing ever clips</b>."),
  ("eq", "with a white point: L<sub>d</sub> = L(1 + L/L<sub>white</sub>"
         "&#178;) / (1 + L)"),
  ("p", "The extension allows values above a chosen white point to burn out "
        "deliberately rather than being compressed asymptotically. <b>This "
        "frequently looks better</b> — a photograph in which the sun is "
        "white is more natural than one in which it has been compressed into "
        "a grey disc, and viewers expect some highlights to clip."),
  ("callout", "Operate on luminance, not on the colour channels",
   ["<b>Applying a compressive curve independently to R, G, and B "
    "compresses the differences between them</b>, because the curve's slope "
    "falls as values rise.",
    "<b>So saturated colours desaturate as they brighten</b>, and bright "
    "regions drift toward white. A saturated red highlight becomes pink and "
    "then white, which is not what the measurement said.",
    "<b>Instead: compute luminance, apply the tone curve to the luminance "
    "alone, and scale all three colour channels by the ratio</b> of output "
    "luminance to input luminance. The ratios between channels — which "
    "is to say the hue and saturation — are then preserved exactly.",
    "<b>Then apply a saturation correction</b>, typically a power on the "
    "chroma. This is necessary because the Hunt effect means perceived "
    "colourfulness falls with luminance — so an image whose luminance "
    "has been compressed looks less colourful even when the ratios are "
    "mathematically preserved, and a modest saturation boost restores the "
    "intended appearance."]),

  ("break",),
  ("h1", "3 &nbsp; Local operators and halos"),
  ("callout", "Halos come from a base layer that crosses edges",
   ["<b>Local operators decompose the image into a 'base' layer carrying "
    "the large-scale brightness variation and a 'detail' layer carrying "
    "local contrast</b>, compress only the base, and recombine. The "
    "intuition is sound: the large-scale range is what exceeds the display, "
    "and local texture does not need compressing.",
    "<b>If the base layer is produced by a Gaussian blur, it smears across "
    "strong edges.</b> Near a boundary between a bright window and a dark "
    "wall, the blurred base is a mixture of both — too dark on the "
    "window side and too bright on the wall side.",
    "<b>So the compression applied is wrong on both sides of the edge, and "
    "in opposite directions.</b> The result is a bright halo along the dark "
    "side of the boundary and a dark halo along the bright side — the "
    "characteristic and immediately recognisable artefact of bad local tone "
    "mapping.",
    "<b>The fix is an edge-aware base layer</b> (Module 02): a bilateral or "
    "guided filter, which does not average across strong edges and therefore "
    "produces a base that is correct on both sides. <b>This application is "
    "a large part of why the bilateral filter entered graphics at all.</b>"]),
  ("code", """1. L      = luminance of the HDR image
2. log_L  = log(L)
3. base   = bilateral_filter(log_L)     # EDGE-AWARE, not Gaussian
   detail = log_L - base
4. base_c = (base - max(base)) * compression_factor
5. log_out = base_c + detail            # detail untouched
   L_out   = exp(log_out)
6. RGB_out = (RGB_in / L) * L_out ; then a saturation power"""),
  ("p", "<b>Compress the base, keep the detail.</b> That structure recurs "
        "in nearly every local operator, and the differences between them "
        "are largely differences in how the decomposition is computed."),
  ("callout", "Gradient-domain tone mapping",
   ["<b>Fattal's reformulation:</b> the thing that exceeds the display's "
    "range is not the absolute values but the large <i>gradients</i> "
    "— the big transitions between bright and dark regions. Texture "
    "consists of small gradients and is perfectly displayable.",
    "<b>So attenuate large gradients and leave small ones alone.</b> A "
    "spatially varying attenuation function, larger where the gradient "
    "magnitude is larger, compresses the big transitions while preserving "
    "fine detail exactly.",
    "<b>Then integrate the modified gradient field back into an image.</b> "
    "The modified field is not generally a valid gradient field of any "
    "image, so the integration is a least-squares problem — <b>which "
    "is a Poisson equation</b>, and is solved exactly as in Module 08.",
    "<b>It handles very large ranges gracefully</b> and produces results "
    "without the halos of naive base/detail methods. <b>And it is the same "
    "machinery as seamless cloning</b>, which is why Module 08 follows "
    "immediately and treats the gradient domain as a topic in its own "
    "right."]),

  ("h1", "4 &nbsp; Evaluating tone mapping honestly"),
  ("ul", ["<b>There is no ground truth image to compare against.</b> The "
          "display cannot show the radiance map, so there is no reference "
          "rendering of it that would be correct. This rules out the "
          "RMSE-style evaluation that CSCE 647 relied on throughout.",
          "<b>So comparisons are necessarily perceptual</b> — images "
          "shown side by side, under controlled viewing conditions, to "
          "people who are asked to judge. The methodology of CSCE 650 "
          "Module 13 applies here.",
          "<b>Report the operator and its parameters.</b> A great deal of "
          "published comparison between imaging systems is, on inspection, "
          "a comparison between their default tone curves. <b>If two images "
          "are tone mapped differently, nothing else about them is being "
          "compared.</b>",
          "<b>Show what was lost.</b> Mark the clipped regions, show the "
          "ranges that were compressed, and present the pleasing result "
          "alongside the honest accounting rather than instead of it.",
          "<b>And distinguish 'accurate' from 'preferred'.</b> These are "
          "measurably different and have been studied: in forced-choice "
          "experiments people frequently prefer operators that are "
          "demonstrably less faithful to the original scene. Both are "
          "legitimate goals and they are not the same goal, and a paper "
          "claiming one while measuring the other is a common failure."]),
  ("callout", "HDR displays change the question without removing it",
   ["<b>A display capable of a thousand nits or more with genuinely deep "
    "blacks requires far less compression</b> — perhaps twelve stops "
    "rather than eight, which is a substantial fraction of what the sensor "
    "captured.",
    "<b>So tone mapping becomes a smaller intervention</b>, and the "
    "displayed image can sit much closer to the measurement. The operator's "
    "choices matter less because it is choosing among fewer losses.",
    "<b>But it does not disappear.</b> Real scenes still exceed any "
    "display by orders of magnitude, and the mapping now has to target a "
    "<i>range</i> of display capabilities rather than one assumed standard "
    "— the same content may be shown on a phone in sunlight and a "
    "reference monitor in a dark room.",
    "<b>Which is why HDR delivery standards carry metadata</b> describing "
    "the content's actual range and intended appearance, letting each "
    "display perform the final mapping for its own capabilities. <b>This "
    "defers the decision to the last possible moment</b>, which is exactly "
    "what CSCE 647's Module 13 recommended for the same reason."]),
 ],
 "resources": [
   ("Reinhard et al. &mdash; Photographic Tone Reproduction for Digital "
    "Images (free)",
    "https://www-old.cs.utah.edu/docs/techreports/2002/pdf/UUCS-02-001.pdf",
    "The global operator of &sect;2, including the photographic analogy "
    "that motivates it."),
   ("Durand & Dorsey &mdash; Fast Bilateral Filtering for the Display of "
    "HDR Images (free)",
    "https://people.csail.mit.edu/fredo/PUBLI/Siggraph2002/",
    "The bilateral tone mapping of &sect;3, and one of the papers that "
    "brought the bilateral filter into graphics."),
   ("Fattal, Lischinski & Werman &mdash; Gradient Domain High Dynamic Range "
    "Compression (free)",
    "https://www.cs.huji.ac.il/~danix/hdr/",
    "The gradient-domain method, and a natural lead-in to Module 08."),
   ("Mantiuk et al. &mdash; tone mapping evaluation work (free)",
    "https://www.cl.cam.ac.uk/~rkm38/",
    "Perceptual evaluation of tone mapping, including the "
    "accurate-versus-preferred distinction in &sect;4."),
 ],
 "exercises": [
   "Implement Reinhard's global operator with and without a white point. "
   "Compare on a scene with a visible light source.",
   "Apply a tone curve per channel and to luminance only. Photograph "
   "something saturated and compare the desaturation.",
   "Implement a saturation correction and find the exponent you prefer. "
   "Report it and note that it is a preference.",
   "Implement base/detail tone mapping with a Gaussian base layer and "
   "<b>produce halos deliberately</b> on a high-contrast edge.",
   "Replace the Gaussian with a bilateral filter and show the halos "
   "disappear.",
   "Implement gradient-domain tone mapping, including the Poisson solve. "
   "Compare against the bilateral method on the same radiance map.",
   "Tone map one radiance map with four operators and present them without "
   "labels to six people. Ask which is most accurate and which they prefer, "
   "separately.",
   "Produce a figure showing, for one tone mapped image, which regions were "
   "clipped and how much each range was compressed.",
   "If you have access to an HDR display, show the same radiance map on it "
   "and on an SDR display and describe the difference in what the operator "
   "had to do.",
 ],
 "selfcheck": [
   "Why is tone mapping underdetermined, and what kind of criterion does "
   "that make it?",
   "Compare global and local operators on five axes.",
   "Write Reinhard's operator and say what the log-average luminance is "
   "for.",
   "Why apply the curve to luminance rather than per channel, and why "
   "correct saturation afterwards?",
   "Explain halos precisely, and give the fix.",
   "Describe base/detail tone mapping in five steps.",
   "What does gradient-domain tone mapping attenuate, and how is the result "
   "integrated?",
   "Give five rules for evaluating tone mapping honestly.",
   "What do HDR displays change, and what do they not?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Demosaicing and the Raw Pipeline",
 "subtitle": "Two-thirds of the colour data was never measured.",
 "question": "How do you get a colour image from a sensor that measures one "
             "channel per pixel?",
 "outcomes": [
     "Explain the colour filter array and why it exists.",
     "Implement demosaicing and explain its failure modes.",
     "Explain white balance and the illuminant estimation problem.",
     "Trace the full raw-to-display pipeline and justify the ordering.",
     "Explain colour spaces and the camera colour matrix.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The colour filter array",
   "blurb": "One colour per pixel, interpolated into three."},

  {"t": "callout", "title": "A sensor measures intensity, not colour",
   "kind": "Why the mosaic exists",
   "body": ["<b>A photosite counts photons.</b> It has no way to "
            "distinguish their wavelengths.",
            "<b>So each pixel gets a colour filter</b> — the Bayer "
            "pattern is 50% green, 25% red, 25% blue, arranged in 2×2 "
            "tiles.",
            "<b>Twice as many green because luminance sensitivity peaks "
            "there</b> and the eye resolves detail largely from the green "
            "channel.",
            "<b>So two-thirds of the colour data at every pixel is "
            "interpolated, not measured.</b> Demosaicing is the "
            "reconstruction, and its errors are visible as colour "
            "artefacts."]},

  {"t": "table", "kicker": "Demosaic", "title": "Demosaicing methods",
   "header": ["Method", "Idea", "Quality"],
   "widths": [3.0, 4.8, 4.3],
   "rows": [
     ["Nearest neighbour", "Copy the nearest same-colour pixel", "<b>Bad; blocky</b>"],
     ["Bilinear", "Average the neighbours of each colour", "<b>Soft; colour fringes at edges</b>"],
     ["<b>Edge-directed</b>", "Interpolate <i>along</i> edges, not across", "<b>Much better</b>"],
     ["<b>Gradient-corrected</b>", "Use the green channel's detail to guide R and B", "<b>The classic good method</b>"],
     ["Learned", "A network trained on raw/RGB pairs", "<b>Best, and it invents</b>"],
   ],
   "footnote": "<b>Green is the detail channel</b> — it is sampled "
               "twice as densely, so the good methods use it to guide the "
               "others.",
   "note": "The green-as-guide insight is what separates good demosaicing "
           "from bilinear."},

  {"t": "callout", "title": "Demosaicing errors are structural, not random",
   "kind": "The characteristic artefacts",
   "body": ["<b>Zippering:</b> alternating colour along a horizontal or "
            "vertical edge, from interpolating across it.",
            "<b>Colour moiré:</b> fine repeating detail near the sampling "
            "limit aliases differently in each channel, producing coloured "
            "bands where the scene is grey.",
            "<b>False colour</b> at sharp edges and on fine texture.",
            "<b>These are aliasing artefacts</b> (Module 02), which is why "
            "optical low-pass filters exist — and why removing them "
            "trades sharpness for exactly these."]},

  {"t": "section", "label": "Part 2", "title": "White balance",
   "blurb": "Deciding what colour the light was."},

  {"t": "callout", "title": "Colour constancy is an inference, and it is underdetermined",
   "kind": "The problem",
   "body": ["<b>The sensor measures reflected light</b> — the product of "
            "illumination and surface reflectance.",
            "<b>Separating them is underdetermined.</b> A white surface "
            "under orange light and an orange surface under white light "
            "produce identical measurements.",
            "<b>Humans do it anyway</b>, remarkably well, using scene "
            "context, memory of object colours, and the range of colours "
            "present.",
            "<b>Cameras estimate it with heuristics</b>, and get it wrong "
            "in exactly the cases where the assumptions fail."]},

  {"t": "table", "kicker": "Estimation", "title": "Illuminant estimation heuristics",
   "header": ["Method", "Assumption", "Fails when"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["<b>Grey world</b>", "The scene averages to grey", "<b>A large uniform colour dominates</b>"],
     ["<b>White patch</b>", "The brightest pixel is white", "No white object; a clipped highlight"],
     ["Grey edge", "Average of edges is achromatic", "More robust than grey world"],
     ["Gamut mapping", "Observed gamut constrains the illuminant", "Few colours present"],
     ["<b>Learned</b>", "Trained on labelled images", "<b>Scenes unlike the training set</b>"],
   ],
   "footnote": "A photograph of a forest defeats grey world; a photograph "
               "of snow defeats white patch.",
   "note": "Having a counterexample for each heuristic makes the "
           "underdetermination concrete."},

  {"t": "section", "label": "Part 3", "title": "The pipeline",
   "blurb": "Order matters, and the reasons are specific."},

  {"t": "code", "kicker": "Pipeline", "title": "Raw to display, in order",
   "lang": "text", "code": """
  1. SUBTRACT BLACK LEVEL      sensor's zero is not 0
  2. SCALE to [0,1]            using the saturation value
  3. WHITE BALANCE             per-channel multipliers
                               (BEFORE demosaic: channels become comparable)
  4. DEMOSAIC                  one channel -> three
  5. COLOUR MATRIX             camera RGB -> XYZ -> working space
  6. DENOISE / SHARPEN         IN LINEAR SPACE (Module 01)
  7. TONE MAP                  HDR -> display range (Module 04)
  8. GAMUT MAP                 handle out-of-gamut colours
  9. ENCODE                    apply the display transfer function
                               <-- LAST. ONCE.

  Steps 1-6 are LINEAR. Step 9 is where linearity ends.
""",
   "caption": "White balance before demosaicing because the interpolation "
              "assumes the channels are comparable — which they are "
              "not until it is applied.",
   "note": "The white-balance-before-demosaic ordering is the "
           "non-obvious one and students get it wrong."},

  {"t": "callout", "title": "Why white balance comes before demosaicing",
   "kind": "The ordering that surprises people",
   "body": ["<b>Demosaicing interpolates between channels</b> — the good "
            "methods use the green channel to guide red and blue.",
            "<b>That assumes the channels are on comparable scales.</b> "
            "Before white balance they are not: under tungsten light the "
            "blue channel may be a quarter of the red.",
            "<b>So interpolation guided by an uncorrected green channel "
            "introduces colour errors</b> at exactly the edges where "
            "demosaicing is already hardest.",
            "<b>Apply the per-channel multipliers first</b>, and the "
            "channels become comparable before the interpolation needs them "
            "to be."]},

  {"t": "bullets", "kicker": "Colour", "title": "Colour spaces, briefly",
   "items": [
     "<b>Camera RGB is device-specific</b> — it depends on the filters' "
     "spectral responses and means nothing outside that camera.",
     "",
     "<b>The colour matrix maps it to XYZ</b>, a device-independent space "
     "defined by the CIE standard observer.",
     "",
     "<b>Then XYZ to a working space</b> — sRGB, Adobe RGB, ProPhoto, "
     "ACEScg. Wider spaces preserve saturated colours and need more bits.",
     "",
     "<b>The mapping is approximate</b>, because camera filters do not "
     "match the human cone responses — no 3×3 matrix is exact.",
     "",
     "<b>This is why two cameras render the same scene differently</b>, "
     "even with identical white balance.",
   ],
   "note": "The 'no 3x3 matrix is exact' point explains camera colour "
           "differences better than any amount of brand folklore."},
 ],
 "takeaways": [
   "A photosite counts photons and cannot distinguish wavelength, so a "
   "colour filter array samples one channel per pixel — two-thirds of "
   "the colour data is interpolated.",
   "The Bayer pattern is half green because luminance detail is carried "
   "largely by green, and good demosaicing uses green to guide red and blue.",
   "Zippering, colour moir&eacute;, and false colour are aliasing artefacts, "
   "which is why optical low-pass filters exist.",
   "White balance is an underdetermined inference — a white surface "
   "under orange light is indistinguishable from an orange surface under "
   "white light.",
   "Every illuminant heuristic has a scene that defeats it: grey world fails "
   "on a forest, white patch fails on snow.",
   "White balance comes before demosaicing because interpolation assumes the "
   "channels are on comparable scales, and before correction they are not.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The colour filter array"),
  ("callout", "A sensor measures intensity, not colour",
   ["<b>A photosite counts photons.</b> It has no mechanism for "
    "distinguishing a red photon from a blue one — both liberate an "
    "electron, and the well counts electrons.",
    "<b>So each photosite is covered by a colour filter</b>, passing one "
    "band and blocking the others. The <b>Bayer pattern</b> — a "
    "2&times;2 tile of one red, one blue, and two greens — is near "
    "universal.",
    "<b>Twice as many green sites because human luminance sensitivity peaks "
    "in green</b>, and spatial detail is perceived largely through the "
    "luminance channel. Sampling green more densely therefore buys more "
    "perceived resolution than sampling red or blue would.",
    "<b>The consequence is that two-thirds of the colour information at "
    "every pixel is interpolated rather than measured.</b> Demosaicing is "
    "that reconstruction, and its errors appear as colour artefacts that no "
    "amount of later processing removes."]),
  ("table", ["Method", "Approach", "Assessment"],
   [["<b>Nearest neighbour</b>",
     "Copy the value from the nearest photosite of the required colour.",
     "<b>Poor.</b> Blocky, with obvious colour artefacts. Fast, and used "
     "only for previews."],
    ["<b>Bilinear</b>",
     "Average the surrounding photosites of each colour independently.",
     "Soft, with <b>coloured fringes at edges</b> — because averaging "
     "across an edge mixes two different surfaces, and does so differently "
     "in each channel."],
    ["<b>Edge-directed</b>",
     "Estimate the local edge direction and interpolate <i>along</i> it "
     "rather than across it.",
     "<b>Substantially better.</b> Removes most fringing on straight "
     "edges."],
    ["<b>Gradient-corrected / Malvar</b>",
     "<b>Use the densely sampled green channel's detail to guide the "
     "interpolation of red and blue</b>, on the assumption that the channels "
     "share structure.",
     "<b>The classic good method.</b> A fixed linear filter, cheap, and "
     "close to the quality of much more expensive approaches."],
    ["<b>Learned</b>",
     "A network trained on pairs of raw mosaics and ground-truth full-colour "
     "images.",
     "<b>Best measured quality, and it invents plausible detail</b> where "
     "the measurement is ambiguous — Module 13's question."]],
   [0.20, 0.38, 0.42]),
  ("p", "<b>The guiding insight is that green is the detail channel.</b> It "
        "is sampled at twice the density of the others, so it has the "
        "highest-quality structural information, and the chromatic channels "
        "can be reconstructed by assuming that colour varies more slowly "
        "than luminance — which is true for most real surfaces."),
  ("callout", "Demosaicing errors are structural",
   ["<b>Zippering:</b> alternating light and dark or coloured pixels along a "
    "horizontal or vertical edge, produced by interpolating across the edge "
    "rather than along it. The name describes the appearance exactly.",
    "<b>Colour moir&eacute;:</b> fine repeating detail near the sampling "
    "limit aliases <i>differently in each channel</i>, because the channels "
    "are sampled on different lattices. The result is coloured banding where "
    "the scene is grey — fabric and distant architecture are the "
    "classic subjects.",
    "<b>False colour</b> at sharp edges and on fine texture, where the "
    "assumption that chrominance varies slowly fails.",
    "<b>All of these are aliasing artefacts</b> in the sense of Module 02 "
    "— scene detail above the sampling rate folding down. <b>This is "
    "why cameras have historically included an optical low-pass filter</b> "
    "in front of the sensor, and why removing it is a deliberate trade of "
    "sharpness against exactly these artefacts."]),

  ("h1", "2 &nbsp; White balance"),
  ("callout", "Colour constancy is an underdetermined inference",
   ["<b>The sensor measures reflected light, which is the product of the "
    "illumination spectrum and the surface reflectance spectrum.</b> "
    "Recovering both from the product is underdetermined by construction.",
    "<b>A white surface under orange light and an orange surface under white "
    "light produce identical measurements.</b> There is no information in "
    "the pixel that distinguishes them — the ambiguity is "
    "fundamental, not a limitation of the sensor.",
    "<b>Humans perform this separation remarkably well</b>, using scene "
    "context, memory of what objects are usually coloured, the range of "
    "colours present, specular highlights (which carry the illuminant's "
    "colour directly), and probably several mechanisms not yet understood. "
    "A white shirt looks white indoors and outdoors.",
    "<b>Cameras estimate it with heuristics</b>, each of which encodes an "
    "assumption about scenes — and each therefore fails on the scenes "
    "where its assumption does not hold."]),
  ("table", ["Heuristic", "Assumption", "Fails when"],
   [["<b>Grey world</b>",
     "The average reflectance of a scene is achromatic, so the average of "
     "the image reveals the illuminant.",
     "<b>A large uniform colour dominates the frame.</b> A photograph of a "
     "forest is estimated as having green light, and the correction turns "
     "the foliage grey."],
    ["<b>White patch / max-RGB</b>",
     "The brightest pixel in each channel corresponds to a white surface.",
     "There is no white object in the scene, or the brightest pixel is a "
     "clipped highlight carrying no colour information. A snow scene has the "
     "opposite problem — everything is bright."],
    ["<b>Grey edge</b>",
     "The average of the <i>derivative</i> of the image is achromatic.",
     "More robust than grey world in practice, and it shares the same "
     "failure in principle."],
    ["<b>Gamut mapping</b>",
     "The set of colours observable under a given illuminant is constrained, "
     "so the observed gamut narrows the possibilities.",
     "Scenes containing few distinct colours, which constrain little."],
    ["<b>Learned</b>",
     "Statistics of illuminants and scenes, from labelled training data.",
     "<b>Scenes unlike the training distribution</b> — which is the "
     "standard failure mode of learned components and is covered in "
     "Module 12."]],
   [0.17, 0.41, 0.42]),

  ("break",),
  ("h1", "3 &nbsp; The pipeline"),
  ("code", """1. SUBTRACT BLACK LEVEL    the sensor's zero is not 0
2. SCALE to [0,1]          using the saturation value
3. WHITE BALANCE           per-channel multipliers   <-- before demosaic
4. DEMOSAIC                one channel -> three
5. COLOUR MATRIX           camera RGB -> XYZ -> working space
6. DENOISE / SHARPEN       in LINEAR space (Module 01)
7. TONE MAP                HDR -> display range (Module 04)
8. GAMUT MAP               handle out-of-gamut colours
9. ENCODE                  display transfer function  <-- LAST, ONCE"""),
  ("p", "<b>Steps 1 through 6 operate on linear data</b>, which is what "
        "makes them physically meaningful (Module 01). <b>Step 9 is where "
        "linearity ends</b>, and it happens exactly once, at the end."),
  ("callout", "Why white balance precedes demosaicing",
   ["This ordering surprises people and the reason is specific.",
    "<b>Good demosaicing interpolates <i>between</i> channels.</b> The "
    "gradient-corrected methods of &sect;1 use the densely sampled green "
    "channel's structure to guide the reconstruction of red and blue, on the "
    "assumption that the channels share edges.",
    "<b>That assumption requires the channels to be on comparable "
    "scales.</b> Before white balance they are not — under tungsten "
    "illumination the raw blue channel may be a quarter of the raw red, so "
    "a green-guided correction applied to blue is scaled wrongly.",
    "<b>So interpolation guided by uncorrected channels introduces colour "
    "errors</b>, and it does so at exactly the edges where demosaicing is "
    "already most difficult. <b>Applying the per-channel multipliers "
    "first</b> brings the channels into comparable ranges before the "
    "interpolation depends on it, and the artefacts largely disappear."]),
  ("ul", ["<b>Camera RGB is device-specific.</b> It depends on the spectral "
          "transmission of that camera's particular filters, and a value in "
          "it means nothing outside that camera model.",
          "<b>The colour matrix maps camera RGB to CIE XYZ</b>, a "
          "device-independent space defined by the standard observer's cone "
          "responses. This matrix is measured per camera model and is stored "
          "in the raw file's metadata.",
          "<b>Then XYZ to a working space</b> — sRGB for display, "
          "Adobe RGB or ProPhoto for editing, ACEScg for film pipelines. "
          "<b>Wider spaces preserve saturated colours that sRGB clips</b>, "
          "and they need more bits to avoid banding, which is why wide-gamut "
          "work is done in 16-bit or floating point.",
          "<b>The mapping is approximate.</b> A camera's filter responses "
          "are not a linear transformation of the human cone responses "
          "— the Luther&ndash;Ives condition is not satisfied by any "
          "real camera — so <b>no 3&times;3 matrix is exact</b>. The "
          "fit is optimised over a set of representative colours and is "
          "wrong elsewhere.",
          "<b>This is why two cameras render the same scene differently</b> "
          "even with identical white balance and identical processing. It is "
          "a measurable physical difference in the filters, not a matter of "
          "manufacturer preference — though the tone curves are that "
          "as well."]),
 ],
 "resources": [
   ("CMU 15-463 &mdash; the image processing pipeline lecture and "
    "assignment (free)",
    "http://graphics.cs.cmu.edu/courses/15-463/",
    "The complete raw pipeline, implemented. This assignment is Project 1's "
    "first requirement."),
   ("Malvar, He & Cutler &mdash; High-quality linear interpolation for "
    "demosaicing (free)",
    "https://www.microsoft.com/en-us/research/publication/"
    "high-quality-linear-interpolation-for-demosaicing-of-bayer-patterned-color-images/",
    "The gradient-corrected method of &sect;1. A fixed linear filter, a few "
    "lines, and close to state of the art for a long time."),
   ("Gijsenij, Gevers & van de Weijer &mdash; Computational Color Constancy "
    "survey (free)",
    "https://ivi.fnwi.uva.nl/cv/colorconstancy/",
    "The illuminant estimation methods of &sect;2, compared on standard "
    "datasets."),
   ("Adobe DNG specification (free)",
    "https://helpx.adobe.com/camera-raw/digital-negative.html",
    "What is actually in a raw file, including the colour matrices and how "
    "they are intended to be applied."),
 ],
 "exercises": [
   "Extract the raw Bayer array from a file and visualise it directly. "
   "Confirm the pattern and the channel ratios.",
   "Implement bilinear demosaicing and photograph a sharp high-contrast edge "
   "to produce visible fringing.",
   "Implement the Malvar gradient-corrected method and compare on the same "
   "image.",
   "Photograph fine repeating detail — fabric, a distant fence — "
   "and reproduce colour moir&eacute;.",
   "<b>Demosaic before and after white balance</b> on a tungsten-lit scene "
   "and compare the colour errors at edges.",
   "Implement grey world and white patch illuminant estimation. Find a "
   "photograph that defeats each.",
   "Implement the full nine-step pipeline and compare your output against "
   "the camera's JPEG. Identify the differences and attribute each to a "
   "stage.",
   "Apply the camera's colour matrix and compare against ignoring it. Report "
   "the colour error on a chart if you have one.",
   "Process the same raw file into sRGB and into ProPhoto. Find a colour "
   "that one clips and the other does not.",
 ],
 "selfcheck": [
   "Why does a sensor need a colour filter array, and why is half of the "
   "Bayer pattern green?",
   "What fraction of colour data is interpolated, and what is demosaicing?",
   "Name five demosaicing methods and the insight the good ones use.",
   "Name three demosaicing artefacts and say what they are instances of.",
   "Why is white balance underdetermined? Give the ambiguity precisely.",
   "Give five illuminant heuristics and a scene that defeats each.",
   "List the nine pipeline stages in order, and say where linearity ends.",
   "Why must white balance precede demosaicing?",
   "Why is the camera colour matrix only approximate, and what does that "
   "explain?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Deconvolution and Deblurring",
 "subtitle": "Undoing a blur, and why it is mostly impossible.",
 "question": "Can you recover a sharp image from a blurred one?",
 "outcomes": [
     "Model blur as convolution with a point spread function.",
     "Explain why naive inverse filtering fails.",
     "Implement Wiener and Richardson–Lucy deconvolution.",
     "Explain blind deconvolution and why it is ill-posed.",
     "Explain coded apertures and flutter shutters.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Blur as convolution",
   "blurb": "The forward model."},

  {"t": "eq", "kicker": "Model", "title": "The blur model",
   "eqs": [
     ("b = k * s + n",
      "Blurred image = kernel convolved with sharp image, plus noise. "
      "The kernel is the point spread function."),
     ("B = K · S + N",
      "In the frequency domain, convolution becomes multiplication — "
      "which is why deconvolution is attempted there."),
     ("S = (B − N) / K     ← the naive inverse",
      "Divide by the kernel's spectrum. And this is catastrophic, for the "
      "reason on the next slide."),
   ],
   "caption": "The forward model is simple and exact. The inverse is where "
              "the difficulty is.",
   "note": "Setting up the forward model cleanly makes the inverse "
           "problem's difficulty obvious."},

  {"t": "callout", "title": "Naive inverse filtering amplifies noise without bound",
   "kind": "Why you cannot just divide",
   "body": ["<b>A blur is a low-pass filter, so K is near zero at high "
            "frequencies.</b>",
            "<b>Dividing by a near-zero number amplifies whatever is "
            "there</b> — and what is there, at those frequencies, is "
            "almost entirely noise.",
            "<b>So the 'recovered' image is dominated by amplified "
            "noise</b>, usually by a wide margin, and looks far worse than "
            "the blurred input.",
            "<b>And where K is exactly zero, the information is genuinely "
            "gone.</b> No algorithm recovers it, because nothing was "
            "recorded. This is the fundamental limit."]},

  {"t": "section", "label": "Part 2", "title": "Regularised deconvolution",
   "blurb": "Trading sharpness against noise."},

  {"t": "eq", "kicker": "Wiener", "title": "Wiener deconvolution",
   "eqs": [
     ("S = B · K* / ( |K|² + 1/SNR )",
      "Divide by K, but add a term that prevents the division blowing up "
      "where K is small."),
     ("where SNR is large:  →  1/K    (full inversion)",
      "Where the signal is strong, invert normally."),
     ("where SNR is small:  →  K* · SNR  (suppress)",
      "Where the noise dominates, suppress rather than amplify."),
   ],
   "caption": "An optimal linear filter under a Gaussian noise assumption. "
              "One parameter, and it is the noise level.",
   "note": "The frequency-by-frequency behaviour is the intuition: trust "
           "the measurement where it is reliable."},

  {"t": "callout", "title": "Richardson–Lucy: iterate toward the answer",
   "kind": "The non-linear alternative",
   "body": ["<b>An iterative maximum-likelihood method</b> assuming "
            "Poisson noise — which is the correct model for photon "
            "counting (Module 01).",
            "<b>Each iteration compares the current estimate's blur against "
            "the observation</b> and corrects multiplicatively.",
            "<b>It preserves non-negativity automatically</b>, which is "
            "physically correct and which Wiener does not.",
            "<b>And it amplifies noise as iterations increase</b>, so you "
            "must stop early. <b>The stopping point is a tuning parameter "
            "disguised as a convergence criterion</b>, which is worth being "
            "honest about."]},

  {"t": "table", "kicker": "Priors", "title": "Regularisation by image priors",
   "header": ["Prior", "Assumes", "Effect"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Tikhonov (L2)", "The image is smooth", "<b>Blurs edges — wrong prior</b>"],
     ["<b>Total variation</b>", "Piecewise constant", "<b>Preserves edges; flattens texture</b>"],
     ["<b>Sparse gradients</b>", "Natural images have few strong edges", "<b>Matches real statistics well</b>"],
     ["Learned", "Whatever the training data showed", "Best results; invents detail"],
   ],
   "footnote": "<b>The heavy-tailed gradient distribution of natural "
               "images</b> is the empirical fact these priors encode.",
   "note": "The sparse-gradient prior is the one with genuine empirical "
           "support and it transformed the field around 2006."},

  {"t": "section", "label": "Part 3", "title": "Blind deconvolution",
   "blurb": "When you do not know the blur either."},

  {"t": "callout", "title": "Blind deconvolution is severely ill-posed",
   "kind": "Why it is hard",
   "body": ["<b>You observe b and must recover both k and s.</b> There are "
            "far more unknowns than measurements.",
            "<b>And there is a trivial wrong answer:</b> k = delta "
            "function, s = b. Sharp kernel, blurred image, perfect "
            "agreement with the observation.",
            "<b>So the problem is entirely driven by the priors.</b> What "
            "makes a plausible image, and what makes a plausible blur "
            "kernel?",
            "<b>Fergus et al. 2006 was the breakthrough</b> — use the "
            "heavy-tailed gradient statistics of natural images as the "
            "prior, and the delta solution becomes unlikely."]},

  {"t": "bullets", "kicker": "Practice", "title": "What makes blind deblurring work",
   "items": [
     "<b>Natural image priors</b> — sparse gradients, as above. The "
     "core idea.",
     "",
     "<b>Kernel priors:</b> motion blur kernels are sparse, connected, and "
     "non-negative. A camera shake path is a curve, not a cloud.",
     "",
     "<b>Coarse-to-fine</b> (Module 02): estimate a small kernel at low "
     "resolution, refine.",
     "",
     "<b>Edge prediction:</b> guess where the strong edges should be, and "
     "use them to constrain the kernel.",
     "",
     "<b>Or measure the blur</b> — an IMU records the camera shake "
     "directly, which is far easier than inferring it.",
   ],
   "note": "The IMU point is the practical one: measurement beats inference "
           "when it is available."},

  {"t": "section", "label": "Part 4", "title": "Coded imaging",
   "blurb": "Change the capture so the inverse is easier."},

  {"t": "two", "kicker": "Coded capture", "title": "Two ways to make deconvolution tractable",
   "lh": "Coded aperture",
   "l": ["Put a patterned mask in the aperture.",
         "<b>The defocus PSF becomes broadband</b> — no zeros in its "
         "spectrum.",
         "So deconvolution is well-conditioned.",
         ("And the PSF's scale reveals depth.", 1),
         "Cost: light is blocked by the mask."],
   "rh": "Flutter shutter",
   "r": ["Open and close the shutter in a coded sequence during exposure.",
         "<b>The motion blur PSF becomes broadband</b> instead of a box.",
         "A box kernel has zeros; a coded one does not.",
         ("Motion blur becomes invertible.", 1),
         "Cost: half the light, and you must know the motion."],
   "note": "Both are the same idea: engineer the PSF so its spectrum has no "
           "zeros, because zeros are unrecoverable."},

  {"t": "callout", "title": "The deep idea: design the measurement, not just the algorithm",
   "kind": "What computational photography means",
   "body": ["<b>A conventional camera is designed to form an image "
            "directly.</b> If the image is blurred, you are stuck with an "
            "ill-posed inverse.",
            "<b>A coded camera is designed so that the inverse is "
            "easy</b> — accepting a worse raw image in exchange for a "
            "better recoverable one.",
            "<b>This is the central move of the whole field</b>: "
            "co-design the optics and the computation rather than treating "
            "the camera as fixed.",
            "<b>Light field cameras (Module 09) are the same move</b>, as "
            "is burst photography (Module 10) — capture something that is "
            "not a photograph, and compute the photograph from it."]},
 ],
 "takeaways": [
   "Blur is convolution with a point spread function, so deconvolution is "
   "division in the frequency domain — and that division is "
   "catastrophic.",
   "A blur is low-pass, so its spectrum is near zero at high frequencies; "
   "dividing amplifies the noise that lives there.",
   "Where the spectrum is exactly zero the information is genuinely gone, "
   "and no algorithm recovers it.",
   "Wiener deconvolution adds a noise term so the division suppresses rather "
   "than amplifies where the signal is weak.",
   "Richardson–Lucy assumes Poisson noise and preserves non-negativity, "
   "and must be stopped early — which is a tuning parameter disguised "
   "as convergence.",
   "Coded apertures and flutter shutters engineer the PSF to have no "
   "spectral zeros: design the measurement so the inverse is easy.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The forward model"),
  ("eq", "b = k * s + n &nbsp;&nbsp;&nbsp;&nbsp; B = K &middot; S + N"),
  ("p", "The blurred observation b is the sharp image s convolved with a "
        "<b>point spread function</b> k, plus noise. The PSF is the image a "
        "single point of light would produce — a disc for defocus, a "
        "curve for camera shake, a line for linear motion. In the frequency "
        "domain the convolution becomes a multiplication, which is why "
        "deconvolution is attempted there."),
  ("callout", "Naive inverse filtering amplifies noise without bound",
   ["The obvious inverse is S = B/K. It fails comprehensively, for a reason "
    "worth understanding precisely.",
    "<b>A blur is a low-pass filter, so K is small at high frequencies and "
    "may be exactly zero at some.</b> That is what blurring means.",
    "<b>Dividing by a near-zero number amplifies whatever is in the "
    "numerator</b> — and at those frequencies the numerator is almost "
    "entirely noise, because the signal was attenuated and the noise was "
    "not.",
    "<b>So the 'recovered' image is dominated by enormously amplified "
    "noise</b>, typically unrecognisable and far worse than the blurred "
    "input. This is not a numerical issue to be worked around; it is the "
    "structure of the problem.",
    "<b>And where K is exactly zero, the information is genuinely "
    "gone.</b> Those frequencies contributed nothing to the measurement, so "
    "nothing in the measurement constrains them. <b>No algorithm recovers "
    "them</b> — anything that appears to is inventing, which is "
    "Module 12's subject."]),

  ("h1", "2 &nbsp; Regularised deconvolution"),
  ("eq", "S = B &middot; K* / ( |K|&#178; + 1/SNR )"),
  ("p", "<b>Wiener deconvolution</b> is the optimal linear filter under a "
        "Gaussian noise assumption. The added term in the denominator "
        "prevents the division from blowing up where K is small. Its "
        "behaviour is best understood frequency by frequency:"),
  ("table", ["Regime", "Behaviour", "Interpretation"],
   [["<b>High SNR</b> (K large, noise small)",
     "The 1/SNR term is negligible, so the filter approaches 1/K.",
     "<b>Invert fully</b> — the measurement is reliable here."],
    ["<b>Low SNR</b> (K small, noise dominant)",
     "The |K|&#178; term is negligible, so the filter approaches "
     "K* &middot; SNR, which is small.",
     "<b>Suppress rather than amplify</b> — the measurement says "
     "nothing reliable here, so do not trust it."]],
   [0.26, 0.37, 0.37]),
  ("p", "<b>The single parameter is the noise level</b>, which can be "
        "measured (Module 01) rather than guessed — which is unusually "
        "comfortable for a regularisation parameter."),
  ("callout", "Richardson–Lucy",
   ["<b>An iterative maximum-likelihood method assuming Poisson noise</b> "
    "— which, per Module 01, is the physically correct model for "
    "photon counting, where Wiener's Gaussian assumption is an "
    "approximation.",
    "<b>Each iteration blurs the current estimate, compares it against the "
    "observation, and applies a multiplicative correction.</b> The "
    "multiplicative form is what keeps it non-negative.",
    "<b>Non-negativity is preserved automatically</b>, which is physically "
    "correct — radiance cannot be negative — and which Wiener "
    "deconvolution does not guarantee. Negative values in a Wiener result "
    "are a visible artefact around strong edges.",
    "<b>And it amplifies noise as the iteration count rises.</b> It "
    "converges to the maximum-likelihood solution, which for noisy data is "
    "itself noisy — so the iteration must be stopped early. <b>The "
    "stopping point is a tuning parameter disguised as a convergence "
    "criterion</b>, and being clear about that is more honest than treating "
    "it as a property of the algorithm."]),
  ("table", ["Prior", "Assumption", "Effect on the result"],
   [["<b>Tikhonov (L2 on gradients)</b>", "The image is smooth.",
     "<b>Blurs edges</b> — which is the wrong prior for photographs, "
     "whose defining feature is that they have edges."],
    ["<b>Total variation (L1 on gradients)</b>",
     "The image is piecewise constant.",
     "<b>Preserves edges well</b> and flattens texture into cartoon-like "
     "regions, which is the characteristic TV artefact."],
    ["<b>Sparse gradients (hyper-Laplacian)</b>",
     "<b>Natural images have mostly small gradients and a few large "
     "ones</b> — a heavy-tailed distribution, which is an empirically "
     "measured property rather than an assumption of convenience.",
     "<b>Matches real image statistics closely</b>, and this is the prior "
     "that made blind deblurring work."],
    ["<b>Learned</b>", "Whatever the training distribution contained.",
     "Best measured results, and it synthesises detail consistent with the "
     "training data rather than with this image (Module 12)."]],
   [0.22, 0.42, 0.36]),

  ("break",),
  ("h1", "3 &nbsp; Blind deconvolution"),
  ("callout", "Blind deconvolution is severely ill-posed",
   ["<b>You observe only b, and must recover both the kernel k and the sharp "
    "image s.</b> The unknowns vastly outnumber the measurements.",
    "<b>And there is a trivial, wrong, perfectly consistent solution:</b> "
    "k = a delta function and s = b. The 'sharp' image is the blurred one "
    "and the 'kernel' does nothing, and this explains the observation "
    "exactly.",
    "<b>So the problem is driven entirely by the priors.</b> Without a "
    "reason to prefer a genuinely sharp image and a plausible blur kernel, "
    "the trivial solution is as good as any other — and in fact it "
    "maximises the likelihood, because it fits the data perfectly.",
    "<b>Fergus et al.'s 2006 paper was the breakthrough:</b> use the "
    "heavy-tailed gradient statistics of natural images as a prior. A truly "
    "sharp image has a few very large gradients and many near-zero ones; a "
    "blurred image has many medium ones. <b>Under that prior the delta "
    "solution becomes highly improbable</b>, and the optimisation moves "
    "toward a real answer. This single observation turned blind deblurring "
    "from impossible into merely difficult."]),
  ("ul", ["<b>Natural image priors</b> — sparse, heavy-tailed "
          "gradients. The core idea above.",
          "<b>Kernel priors.</b> A camera-shake kernel is sparse, "
          "connected, non-negative, and sums to one — it is the trace "
          "of a continuous path, not an arbitrary cloud of values. "
          "Constraining to that family removes a great deal of the search "
          "space.",
          "<b>Coarse-to-fine estimation</b> (Module 02): estimate a small "
          "kernel at low resolution where the problem is better conditioned, "
          "then refine at each finer scale. The same strategy as alignment "
          "and flow.",
          "<b>Edge prediction.</b> Predict where strong edges ought to be "
          "— by shock filtering, or from a learned estimate — and "
          "use the discrepancy between predicted and observed edges to "
          "constrain the kernel.",
          "<b>Or measure the blur directly.</b> An inertial sensor records "
          "the camera's motion during the exposure, which gives the kernel "
          "without any inference at all. <b>Measurement beats inference "
          "whenever it is available</b>, and this is the practical answer in "
          "any device that has an IMU — which is every phone."]),

  ("h1", "4 &nbsp; Coded imaging"),
  ("table", ["", "Coded aperture", "Flutter shutter"],
   [["Modification", "A patterned mask placed in the lens aperture.",
     "The shutter is opened and closed in a coded binary sequence during "
     "the exposure."],
    ["Effect on the PSF",
     "<b>The defocus PSF becomes broadband</b> — its spectrum has no "
     "zeros, where a plain disc aperture's spectrum has many.",
     "<b>The motion blur PSF becomes broadband</b> — a plain box "
     "kernel (continuous exposure) has regularly spaced spectral zeros; a "
     "coded one does not."],
    ["Consequence", "<b>Defocus deconvolution becomes well-conditioned</b>, "
     "and the scale of the PSF reveals depth — so a single image "
     "yields both a deblurred result and a depth map.",
     "<b>Motion blur becomes invertible</b>, so a long exposure of a moving "
     "subject can be deblurred."],
    ["Cost", "The mask blocks light — typically around half.",
     "Half the light, and the motion must still be known or estimated."]],
   [0.17, 0.41, 0.42]),
  ("callout", "Design the measurement, not just the algorithm",
   ["<b>A conventional camera is designed to form a good image "
    "directly.</b> When that image is degraded, you are left with an "
    "ill-posed inverse problem and whatever priors you can muster.",
    "<b>A coded camera is designed so that the inverse problem is "
    "easy</b> — deliberately capturing a <i>worse</i> raw image in "
    "exchange for one from which more can be recovered. The coded aperture "
    "image looks bad; the deconvolved result is better than anything the "
    "plain aperture could have given.",
    "<b>This is the central move of computational photography as a "
    "field:</b> co-design the optics and the computation, rather than "
    "treating the camera as a fixed device whose output must be repaired "
    "afterwards.",
    "<b>Light field cameras (Module 09) are the same move</b> — "
    "capture angular information instead of a focused image, and compute "
    "focus afterwards. <b>So is burst photography (Module 10)</b> "
    "— capture fifteen bad frames instead of one good one. <b>In each "
    "case what the sensor records is not a photograph</b>, and the "
    "photograph is computed from it."]),
 ],
 "resources": [
   ("CMU 15-463 &mdash; deconvolution and coded photography lectures (free)",
    "http://graphics.cs.cmu.edu/courses/15-463/",
    "Wiener, Richardson–Lucy, and the coded aperture material, with "
    "the assignment."),
   ("Fergus et al. &mdash; Removing Camera Shake from a Single Photograph "
    "(free)",
    "https://cs.nyu.edu/~fergus/research/deblur.html",
    "The &sect;3 breakthrough. The natural image prior argument is the part "
    "to read closely."),
   ("Levin et al. &mdash; Image and Depth from a Conventional Camera with a "
    "Coded Aperture (free)",
    "https://groups.csail.mit.edu/graphics/CodedAperture/",
    "The coded aperture of &sect;4, including the depth recovery."),
   ("Raskar, Agrawal & Tumblin &mdash; Coded Exposure Photography: Motion "
    "Deblurring using Fluttered Shutter (free)",
    "https://web.media.mit.edu/~raskar/deblur/",
    "The flutter shutter. The spectral argument is clearly made."),
 ],
 "exercises": [
   "Blur an image with a known kernel, add noise, and attempt naive inverse "
   "filtering. Report how bad the result is and explain it from the "
   "spectrum.",
   "Plot the frequency spectrum of a disc PSF and a box motion PSF and "
   "identify the zeros.",
   "Implement Wiener deconvolution and sweep the noise parameter. Find the "
   "value that works and note that it matches your measured noise.",
   "Implement Richardson–Lucy and plot image quality against iteration "
   "count. Identify where it starts getting worse.",
   "Implement total variation regularised deconvolution and compare against "
   "Wiener on an image with strong edges.",
   "Measure the gradient distribution of a natural photograph and confirm it "
   "is heavy-tailed. This is the empirical fact behind &sect;2's prior.",
   "Attempt blind deconvolution with no prior and demonstrate that it "
   "converges to the delta-function solution.",
   "Simulate a coded aperture: convolve with a coded PSF and with a disc of "
   "the same area, then deconvolve both. Compare.",
   "Simulate a flutter shutter on a moving object and deconvolve. Compare "
   "against a conventional exposure.",
 ],
 "selfcheck": [
   "Write the blur model and say what the PSF is.",
   "Why does naive inverse filtering fail, and what happens where the "
   "spectrum is exactly zero?",
   "Write the Wiener filter and describe its behaviour at high and low SNR.",
   "What noise model does Richardson–Lucy assume, what does it "
   "preserve, and why must it be stopped early?",
   "Name four priors and say which matches natural images and why.",
   "Why is blind deconvolution ill-posed, and what is the trivial wrong "
   "solution?",
   "What made blind deblurring work, and what is the practical alternative "
   "to inference?",
   "What do coded apertures and flutter shutters have in common?",
   "State the central move of computational photography as a field.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Alignment and Stitching",
 "subtitle": "Putting several photographs into one coordinate system.",
 "question": "How do you combine images taken from different positions?",
 "outcomes": [
     "Explain when a homography is the correct motion model.",
     "Implement feature detection, description, and matching.",
     "Implement RANSAC and explain why robust estimation is necessary.",
     "Explain bundle adjustment.",
     "Implement seamless blending.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Motion models",
   "blurb": "What transform relates two images?"},

  {"t": "table", "kicker": "Models", "title": "Transforms, from simple to general",
   "header": ["Model", "DOF", "Preserves", "Correct when"],
   "widths": [2.5, 1.3, 3.4, 5.0],
   "rows": [
     ["Translation", "2", "Everything", "Small shifts; burst alignment"],
     ["Euclidean", "3", "Lengths, angles", "Rotation about the optical axis"],
     ["Similarity", "4", "Angles, ratios", "Plus scale"],
     ["Affine", "6", "Parallelism", "Weak perspective; distant planes"],
     ["<b>Homography</b>", "<b>8</b>", "<b>Straight lines</b>", "<b>Pure rotation, OR a planar scene</b>"],
   ],
   "footnote": "<b>A homography is exact only for a camera rotating about "
               "its optical centre, or for a planar subject.</b> Nothing "
               "else.",
   "note": "The two-conditions rule for homographies is the thing people "
           "forget, and it explains most stitching failures."},

  {"t": "callout", "title": "Panoramas require rotation about the optical centre",
   "kind": "Why your panorama has seams",
   "body": ["<b>A homography can relate two views only if there is no "
            "parallax</b> — which means either the camera rotated about "
            "its optical centre, or the scene is planar.",
            "<b>Translate the camera and nearby objects shift relative to "
            "distant ones</b>, and no single transform aligns both.",
            "<b>Which is why handheld panoramas fail on close "
            "subjects</b> — the foreground and background cannot both be "
            "aligned.",
            "<b>And why panoramic tripod heads rotate about the nodal "
            "point</b> rather than the tripod screw. The distinction is a "
            "few centimetres and it is the difference between working and "
            "not."]},

  {"t": "section", "label": "Part 2", "title": "Correspondence",
   "blurb": "Finding the same point in two images."},

  {"t": "bullets", "kicker": "Features", "title": "Detect, describe, match",
   "items": [
     "<b>Detect:</b> find repeatable, distinctive points. Corners, not "
     "edges — an edge is ambiguous along its length (the aperture "
     "problem).",
     "",
     "<b>Describe:</b> summarise the neighbourhood in a way that is "
     "invariant to what you expect to change — rotation, scale, "
     "illumination.",
     "",
     "<b>Match:</b> compare descriptors between images and keep the "
     "plausible pairs.",
     "",
     "<b>The ratio test:</b> accept a match only if the best is "
     "substantially better than the second best. <b>Lowe's single most "
     "useful practical contribution.</b>",
   ],
   "note": "The ratio test is one line and removes most bad matches. Worth "
           "emphasising."},

  {"t": "table", "kicker": "Detectors", "title": "Feature detectors and descriptors",
   "header": ["Name", "Property", "Note"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["Harris", "Corner response from the structure tensor", "Not scale invariant"],
     ["<b>SIFT</b>", "Scale and rotation invariant", "<b>The standard; patent expired 2020</b>"],
     ["SURF", "Faster SIFT approximation", "Box filters and integral images"],
     ["<b>ORB</b>", "FAST + BRIEF, binary descriptor", "<b>Very fast; free; good enough</b>"],
     ["Learned", "Trained detectors and descriptors", "Better on hard cases"],
   ],
   "footnote": "<b>SIFT's descriptor is a histogram of gradient "
               "orientations</b>, normalised — which is where its "
               "invariance comes from.",
   "note": "ORB is the practical default now: fast, free, and adequate for "
           "most alignment."},

  {"t": "callout", "title": "Most matches are wrong, which is why RANSAC exists",
   "kind": "The robust estimation problem",
   "body": ["<b>Even after the ratio test, a substantial fraction of "
            "matches are incorrect</b> — repeated texture, moving "
            "objects, and plain ambiguity.",
            "<b>Least squares cannot tolerate this.</b> A single gross "
            "outlier pulls the fit arbitrarily far, because the squared "
            "error grows without bound.",
            "<b>RANSAC: sample a minimal set, fit, count inliers, "
            "repeat.</b> Keep the hypothesis with the most support, then "
            "refit using all its inliers.",
            "<b>Four point correspondences determine a homography</b>, so "
            "the minimal sample is small and the probability of an all-inlier "
            "sample is workable."]},

  {"t": "section", "label": "Part 3", "title": "Global consistency",
   "blurb": "Many images, one solution."},

  {"t": "callout", "title": "Pairwise alignment drifts; bundle adjustment fixes it",
   "kind": "Why a global solve is needed",
   "body": ["<b>Chaining pairwise homographies accumulates error.</b> Align "
            "1 to 2, 2 to 3, and so on, and by image ten the error is "
            "visible.",
            "<b>And a 360&deg; panorama does not close</b> — the last "
            "image does not meet the first.",
            "<b>Bundle adjustment solves for all camera parameters "
            "simultaneously</b>, minimising reprojection error over every "
            "correspondence at once.",
            "<b>It is a large sparse non-linear least squares problem</b>, "
            "and it is the same machinery that underlies structure from "
            "motion and SLAM (CSCE 650 Module 05)."]},

  {"t": "bullets", "kicker": "Blending", "title": "Making the seam invisible",
   "items": [
     "<b>Exposure differs between frames</b> — vignetting, auto "
     "exposure, changing light. A hard seam is always visible.",
     "",
     "<b>Feathering:</b> linearly blend across the overlap. Simple, and "
     "it ghosts if alignment is imperfect.",
     "",
     "<b>Multi-band (Laplacian pyramid) blending:</b> blend low "
     "frequencies over a wide band and high frequencies over a narrow one. "
     "<b>The standard answer</b> (Module 02).",
     "",
     "<b>Graph cut seam finding:</b> put the seam where the images already "
     "agree, rather than blending across a disagreement.",
     "",
     "<b>Gradient-domain blending</b> (Module 08) — the most powerful.",
   ],
   "note": "Multi-band blending is why the Laplacian pyramid's "
           "invertibility matters, and it is the practical default."},

  {"t": "callout", "title": "Choose the seam, then blend across it",
   "kind": "The combination that works",
   "body": ["<b>Blending hides small differences; it cannot hide a "
            "person who moved.</b>",
            "<b>Graph cut finds a seam through regions where the images "
            "already agree</b> — routing around the moving object rather "
            "than averaging it.",
            "<b>Then multi-band blending across that seam</b> removes the "
            "residual exposure difference.",
            "<b>Seam selection plus blending is what production stitchers "
            "do</b>, and either alone is noticeably worse."]},
 ],
 "takeaways": [
   "A homography is exact only for a camera rotating about its optical "
   "centre or for a planar scene — anything else has parallax.",
   "Handheld panoramas fail on close subjects because foreground and "
   "background cannot both be aligned by one transform.",
   "Detect corners rather than edges, describe invariantly to what will "
   "change, and apply Lowe's ratio test — one line that removes most "
   "bad matches.",
   "Most matches are still wrong, and least squares cannot tolerate "
   "outliers, so RANSAC samples minimal sets and counts inliers.",
   "Chained pairwise alignment drifts and 360&deg; panoramas do not close; "
   "bundle adjustment solves all cameras simultaneously.",
   "Choose the seam with a graph cut where the images already agree, then "
   "multi-band blend across it. Either alone is worse.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Motion models"),
  ("table", ["Model", "DOF", "Preserves", "Correct when"],
   [["<b>Translation</b>", "2", "Everything but position.",
     "Small shifts — burst alignment (Module 10), where frames differ "
     "by hand tremor."],
    ["<b>Euclidean</b>", "3", "Lengths and angles.",
     "Rotation about the optical axis plus translation."],
    ["<b>Similarity</b>", "4", "Angles and length ratios.",
     "The above plus uniform scale."],
    ["<b>Affine</b>", "6", "Parallelism.",
     "Weak perspective — a distant planar surface, or a long lens."],
    ["<b>Homography (projective)</b>", "<b>8</b>",
     "<b>Straight lines, and nothing else.</b>",
     "<b>A camera rotating about its optical centre, or a planar "
     "scene.</b> Those two cases and no others."]],
   [0.17, 0.08, 0.28, 0.47]),
  ("callout", "Panoramas require rotation about the optical centre",
   ["<b>A homography can relate two views only when there is no "
    "parallax.</b> That holds in exactly two circumstances: the camera "
    "rotated about its optical centre without translating, or everything "
    "photographed lies in a single plane.",
    "<b>Translate the camera and nearby objects shift relative to distant "
    "ones.</b> That relative shift is parallax, it carries depth "
    "information, and <b>no single 2D transform can account for it</b> "
    "— aligning the background necessarily misaligns the foreground.",
    "<b>Which is why handheld panoramas fail on close subjects.</b> "
    "Rotating your body moves the camera by tens of centimetres, so a "
    "foreground object at two metres and a background at fifty cannot both "
    "be aligned. Distant landscapes stitch beautifully; a room does not.",
    "<b>And it is why panoramic tripod heads rotate about the lens's nodal "
    "point</b> rather than about the tripod screw. The difference is a few "
    "centimetres of offset, and it is the difference between a panorama "
    "that works and one that cannot be made to."]),

  ("h1", "2 &nbsp; Finding correspondences"),
  ("ol", ["<b>Detect.</b> Find points that can be located repeatably in "
          "both images and that are distinctive enough to match. <b>Corners, "
          "not edges</b> — a point on an edge cannot be localised along "
          "the edge's direction, which is the <b>aperture problem</b>, and "
          "it makes edge points useless as correspondences.",
          "<b>Describe.</b> Summarise each point's neighbourhood as a "
          "vector that is invariant to whatever you expect to change between "
          "the images — rotation, scale, and illumination, typically.",
          "<b>Match.</b> For each descriptor in one image, find the nearest "
          "in the other, and keep the plausible pairs.",
          "<b>Apply the ratio test.</b> Accept a match only if the nearest "
          "neighbour is substantially closer than the second nearest "
          "— Lowe suggested a ratio of 0.8. <b>A point with two equally "
          "good matches has no reliable match at all</b>, which is exactly "
          "the situation produced by repeated texture. <b>This is one line "
          "of code and it removes the large majority of bad matches</b>, and "
          "it is Lowe's most useful practical contribution."]),
  ("table", ["Detector / descriptor", "Mechanism", "Assessment"],
   [["<b>Harris corner</b>",
     "Eigenvalues of the local structure tensor — both large means a "
     "corner.",
     "Classic, cheap, and <b>not scale invariant</b>, so it fails when the "
     "images differ in zoom."],
    ["<b>SIFT</b>",
     "Scale-space extrema of a difference-of-Gaussian pyramid, with a "
     "descriptor built from histograms of gradient orientation in a "
     "4&times;4 grid.",
     "<b>The standard for two decades.</b> Scale and rotation invariant, "
     "robust to illumination because the descriptor is normalised. <b>Patent "
     "expired in 2020</b>, so it is now freely usable."],
    ["<b>SURF</b>",
     "An approximation of SIFT using box filters and integral images.",
     "Faster, slightly less accurate. Largely superseded."],
    ["<b>ORB</b>",
     "FAST corner detection with a BRIEF binary descriptor, plus rotation "
     "handling.",
     "<b>Very fast, free, and adequate for most alignment tasks.</b> Binary "
     "descriptors compare with Hamming distance, which is extremely cheap. "
     "The practical default."],
    ["<b>Learned detectors and descriptors</b>",
     "Trained end to end on correspondence tasks.",
     "Better on hard cases — large viewpoint change, repeated "
     "structure — at greater cost."]],
   [0.19, 0.39, 0.42]),
  ("callout", "Most matches are wrong, which is why RANSAC exists",
   ["<b>Even after the ratio test, a substantial fraction of the surviving "
    "matches are incorrect.</b> Repeated texture, moving objects, and "
    "genuine ambiguity all produce confident wrong answers.",
    "<b>Least-squares fitting cannot tolerate this.</b> The squared error of "
    "an outlier grows without bound, so a single gross mismatch can pull the "
    "estimated transform arbitrarily far from the truth. <b>One bad match "
    "out of a hundred can ruin the fit.</b>",
    "<b>RANSAC</b> — random sample consensus — inverts the "
    "approach: repeatedly draw a <i>minimal</i> set of correspondences, fit "
    "a transform to just those, and count how many of the remaining matches "
    "agree with it. Keep the hypothesis with the most support, then refit "
    "using all of its inliers.",
    "<b>Four point correspondences determine a homography</b>, so the "
    "minimal sample is small — and the probability that four randomly "
    "chosen matches are all correct is workable even when half the matches "
    "are wrong, which is what makes the method practical. The required "
    "iteration count follows from the inlier ratio and can be computed "
    "rather than guessed."]),

  ("break",),
  ("h1", "3 &nbsp; Global consistency and blending"),
  ("callout", "Pairwise alignment drifts; bundle adjustment fixes it",
   ["<b>Chaining pairwise estimates accumulates error.</b> Align image 1 to "
    "2, then 2 to 3, then 3 to 4, and each small error compounds into the "
    "next. By the tenth image the misalignment is visible.",
    "<b>And a full 360-degree panorama does not close.</b> Coming all the "
    "way round, the last image does not meet the first — the "
    "accumulated error appears as a visible discontinuity, and simply "
    "forcing the ends together distributes the error badly.",
    "<b>Bundle adjustment solves for all camera parameters "
    "simultaneously</b>, minimising the total reprojection error across "
    "every correspondence in every image pair at once. The constraint that "
    "the panorama closes is then satisfied naturally rather than imposed.",
    "<b>It is a large sparse non-linear least-squares problem</b>, solved by "
    "Levenberg&ndash;Marquardt exploiting the sparsity structure. <b>And it "
    "is the same machinery underlying structure from motion and SLAM</b> "
    "— including the inside-out tracking of CSCE 650 Module 05, which "
    "is bundle adjustment running continuously."]),
  ("ul", ["<b>Exposure differs between frames.</b> Vignetting darkens each "
          "image's corners, automatic exposure changes between shots, and "
          "the light itself may change. <b>A hard seam is therefore always "
          "visible</b>, even with perfect geometric alignment.",
          "<b>Feathering</b> linearly blends across the overlap region. "
          "Simple, and <b>it ghosts whenever alignment is imperfect</b>, "
          "because it averages two slightly different images.",
          "<b>Multi-band blending</b> decomposes both images into Laplacian "
          "pyramids (Module 02) and blends each frequency band over a "
          "different width — low frequencies over a wide region to hide "
          "exposure differences, high frequencies over a narrow one to avoid "
          "ghosting detail. <b>This is the standard answer</b>, and it is "
          "why the Laplacian pyramid's invertibility matters.",
          "<b>Graph cut seam finding</b> chooses <i>where</i> to put the "
          "seam, by finding a path through the overlap along which the two "
          "images already agree — routing around a moving object rather "
          "than averaging it.",
          "<b>Gradient-domain blending</b> (Module 08) is the most powerful "
          "approach and the subject of the next module."]),
  ("callout", "Choose the seam, then blend across it",
   ["<b>Blending can hide a small exposure difference. It cannot hide a "
    "person who moved between frames</b> — averaging two images in "
    "which someone is in different places produces a ghost, and no amount of "
    "feathering removes it.",
    "<b>Graph cut seam selection finds a cut through the overlap region "
    "where the two images already agree</b>, treating disagreement as cost. "
    "The seam routes around the moving person, taking them entirely from one "
    "image or the other.",
    "<b>Then multi-band blending across that chosen seam</b> removes the "
    "residual exposure and vignetting difference, which the seam selection "
    "does not address.",
    "<b>Seam selection plus blending is what production stitchers do</b>, "
    "and either technique alone is noticeably worse: blending alone ghosts "
    "moving objects, and seam selection alone leaves a visible exposure step."]),
 ],
 "resources": [
   ("Szeliski &mdash; Computer Vision, Chapters 8 and 9 (free)",
    "https://szeliski.org/Book/",
    "Alignment, motion models, RANSAC, bundle adjustment, and stitching. "
    "<b>The reference for this module</b>, and Szeliski wrote the standard "
    "panorama survey as well."),
   ("Lowe &mdash; Distinctive Image Features from Scale-Invariant Keypoints "
    "(free)",
    "https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf",
    "SIFT, including the ratio test of &sect;2. One of the most cited "
    "papers in computer vision, and readable."),
   ("Brown & Lowe &mdash; Automatic Panoramic Image Stitching (free)",
    "https://www.cs.ubc.ca/~lowe/papers/07brown.pdf",
    "The complete pipeline of this module, end to end, including bundle "
    "adjustment and multi-band blending."),
   ("Burt & Adelson &mdash; A Multiresolution Spline with Application to "
    "Image Mosaics (free)",
    "https://persci.mit.edu/pub_pdfs/spline83.pdf",
    "Multi-band blending, from 1983 and still the method in use."),
 ],
 "exercises": [
   "Photograph a scene with a close foreground and a distant background, "
   "rotating your body between shots. Attempt to stitch and demonstrate the "
   "parallax failure.",
   "Repeat, rotating about the lens's approximate nodal point, and show the "
   "improvement.",
   "Implement Harris corner detection and show it fails under scale change.",
   "Implement or apply SIFT or ORB matching. Visualise the matches before "
   "and after the ratio test and count how many it removed.",
   "Implement RANSAC for homography estimation. Plot the estimated transform "
   "error against the fraction of outliers, for least squares and for "
   "RANSAC.",
   "Compute the number of RANSAC iterations needed for a given inlier ratio "
   "and confidence, and verify it empirically.",
   "Stitch five images by chaining pairwise homographies and measure the "
   "drift at the far end.",
   "Implement feathering and multi-band blending on the same overlap. "
   "Photograph something with fine texture to make the ghosting visible.",
   "Stitch a panorama containing a person who moved. Implement graph cut "
   "seam selection and show the ghost removed.",
 ],
 "selfcheck": [
   "Name five motion models with their degrees of freedom, and say when "
   "each is correct.",
   "Under exactly what two conditions is a homography exact?",
   "Why do handheld panoramas fail on close subjects?",
   "Why detect corners rather than edges?",
   "What is the ratio test and why does it work?",
   "Why can least squares not be used on raw feature matches?",
   "Describe RANSAC and say why four points matter for a homography.",
   "Why does pairwise alignment drift, and what does bundle adjustment do?",
   "Name four blending approaches and say which two should be combined.",
 ],
},

]
