# -*- coding: utf-8 -*-
"""CSCE 679 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Maps",
 "subtitle": "Where position is taken, and every projection lies.",
 "question": "Why is a map of counts a map of population?",
 "outcomes": [
     "Explain projection distortion and the choice it forces.",
     "Explain why area encodings on maps mislead.",
     "Explain normalisation for spatial data.",
     "Explain the alternatives to a choropleth.",
     "Choose a spatial representation for a task.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Projection",
   "blurb": "You cannot have everything, and must choose."},

  {"t": "callout", "title": "No projection preserves area, angle, and distance together — this is a theorem",
   "kind": "The constraint, which is mathematical",
   "body": ["<b>A sphere cannot be mapped to a plane without "
            "distortion</b> — <b>it has intrinsic curvature and the "
            "plane does not</b>, which is Gauss's result and is not an "
            "engineering limitation.",
            "<b>So every projection chooses what to "
            "preserve:</b> <b>conformal keeps angles and distorts "
            "areas; equal-area keeps areas and distorts shapes; and "
            "compromise projections do neither "
            "exactly.</b>",
            "<b>Which means the choice is determined by the "
            "task:</b> <b>navigation wants angles, and any figure "
            "encoding a quantity on area wants equal area</b> — and "
            "using a conformal projection for the latter is a measurable "
            "error.",
            "<b>And the familiar world projection is "
            "conformal</b> — <b>so it inflates high latitudes "
            "severely</b>, which matters whenever a reader compares "
            "the visual sizes of countries."]},

  {"t": "bullets", "kicker": "Choosing", "title": "Which projection, by purpose",
   "items": [
     "<b>Equal-area for anything quantitative</b> — because "
     "<b>a reader comparing two regions' shaded areas is making an "
     "area judgement</b>, and the projection must not already have "
     "distorted it.",
     "",
     "<b>Conformal for navigation and for local detail</b>, where "
     "angles and shapes matter and the extent is small enough that "
     "area distortion is negligible.",
     "",
     "<b>A compromise projection for general reference</b>, which "
     "is what most atlases use and is a reasonable default for "
     "a non-quantitative map.",
     "",
     "<b>And a local projection for local data</b> — <b>a "
     "country-scale map should use that country's standard "
     "projection</b>, not a world one.",
     "",
     "<b>With the projection named in the caption</b>, which "
     "almost never happens and should.",
   ],
   "footnote": "<b>Name the projection in the caption</b> — which "
               "almost never happens, and which is the only way a reader "
               "can know what the areas mean."},

  {"t": "section", "label": "Part 2", "title": "The choropleth problem",
   "blurb": "The default map, and its two defects."},

  {"t": "callout", "title": "A choropleth encodes a value on colour and a region's importance on its area",
   "kind": "Two problems at once",
   "body": ["<b>The value is on colour</b>, which is rank six or "
            "seven (Module 02 §1) — so <b>the "
            "quantity is read imprecisely</b>, which is tolerable and "
            "is the lesser problem.",
            "<b>And the region's visual prominence is its geographic "
            "area</b>, which has nothing to do with its importance "
            "— <b>so a large sparsely populated region dominates the "
            "figure and a dense city is invisible.</b>",
            "<b>Which means a choropleth of a per-capita quantity "
            "systematically overweights rural areas</b>, and this is a "
            "structural property rather than a styling "
            "problem.",
            "<b>So the two defects are:</b> <b>an imprecise "
            "quantitative channel, and an irrelevant weighting by "
            "area</b> — and the second is the one that changes "
            "conclusions."]},

  {"t": "code", "kicker": "Alternatives", "title": "What to use instead, and when",
   "lang": "text", "code": """
  CARTOGRAM
      distort the regions so area encodes the value.
      Fixes the weighting; destroys recognisability,
      and the distortion is itself hard to read.

  DOT DENSITY
      one dot per n units, placed within the region.
      Area then correctly reflects the total, and
      density reflects the rate. Good, and it needs
      care about placement.

  PROPORTIONAL SYMBOLS
      a circle per region, area encoding the value.
      Still rank five (Module 02), and at least the
      geography is undistorted.

  SMALL MULTIPLES OF NON-MAPS
      a sorted bar chart of the regions, which puts
      the value on position -- rank one.

  AND THAT LAST ONE IS USUALLY BEST, unless the
  spatial pattern IS the finding. Which is the
  question to ask: does the reader need the geography?
""",
   "caption": "<b>Does the reader need the geography?</b> — and if "
              "not, a sorted bar chart puts the value on position, which "
              "is rank one.",
   "note": "The does-the-reader-need-geography question is the "
           "module's practical core."},

  {"t": "section", "label": "Part 3", "title": "Normalisation",
   "blurb": "Which is where maps mislead most often and most honestly."},

  {"t": "callout", "title": "A map of raw counts is a map of population, almost without exception",
   "kind": "The commonest honest error in the subject",
   "body": ["<b>Any count of people-related events — cases, "
            "crimes, sales, votes — is roughly proportional to the "
            "number of people</b>, so <b>the map shows where people "
            "are</b> and nothing else.",
            "<b>Which looks like a finding</b>, because the pattern "
            "is strong and spatially coherent — and it is a finding "
            "about population.",
            "<b>So normalise</b>, by population, by area, by "
            "exposure, or by whatever the relevant denominator "
            "is — <b>which is Module 03 §3's "
            "derivation argument where it matters most.</b>",
            "<b>And then the small-denominator problem "
            "appears:</b> <b>a rate computed over a small population is "
            "extremely noisy</b>, so the extreme values are all small "
            "regions — which is Module 09's subject and requires "
            "showing the uncertainty."]},

  {"t": "bullets", "kicker": "Normalisation", "title": "And the specific traps",
   "items": [
     "<b>The small-denominator problem</b> — <b>the highest "
     "and lowest rates are both in the smallest regions</b>, by "
     "construction, and a naive map highlights "
     "noise.",
     "",
     "<b>The modifiable areal unit problem</b> — <b>the same "
     "data aggregated to different boundaries gives different "
     "patterns</b>, and the boundaries were chosen for administrative "
     "reasons.",
     "",
     "<b>Which means the units are an analytical choice</b>, and "
     "aggregating to a different level is a legitimate and reportable "
     "decision.",
     "",
     "<b>And the binning of the colour scale</b> — <b>quantiles, "
     "equal intervals, and natural breaks give visibly different "
     "maps</b> from identical data.",
     "",
     "<b>So state the denominator, the units, and the "
     "binning</b>, all three.",
   ],
   "footnote": "<b>Quantile, equal-interval, and natural-break "
               "binnings give visibly different maps from the same "
               "data</b> — which makes the binning choice as "
               "consequential as the normalisation."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "By whether the geography is the point."},

  {"t": "bullets", "kicker": "Decision", "title": "The questions, in order",
   "items": [
     "<b>Is the spatial pattern the finding?</b> <b>If not, do "
     "not use a map</b> — use a chart that puts the value on "
     "position.",
     "",
     "<b>Is the quantity a rate or a count?</b> <b>If a count, "
     "normalise or use dot density</b>, where area correctly "
     "reflects the total.",
     "",
     "<b>Does the reader need to recognise the places?</b> If "
     "yes, a cartogram is out.",
     "",
     "<b>Is the denominator small anywhere?</b> If so, the "
     "uncertainty has to be shown "
     "(Module 09).",
     "",
     "<b>And which projection does the task require?</b> "
     "(Part 1) — equal-area for anything "
     "quantitative.",
   ],
   "footnote": "<b>'Is the spatial pattern the finding' is the first "
               "question and the one that eliminates most maps</b> "
               "— a great many maps exist because the data had a "
               "location column."},

  {"t": "callout", "title": "And a map is unusually persuasive, which raises the standard",
   "kind": "Closing",
   "body": ["<b>A map is read as authoritative and concrete in a way "
            "a bar chart is not</b> — it looks like a photograph of "
            "the world rather than an encoding of a table.",
            "<b>Which means its errors are believed</b>, and "
            "<b>a badly normalised choropleth produces confident wrong "
            "conclusions about places and the people in "
            "them</b>.",
            "<b>So the normalisation, the units, the binning, and the "
            "projection all have to be stated</b> — four things, and "
            "a typical published map states none of them.",
            "<b>Which is this module's version of the program's "
            "rule</b> — <b>and the four statements are the difference "
            "between a figure a reader can assess and one they can "
            "only believe.</b>"]},
 ],
 "takeaways": [
   "No projection preserves area, angle, and distance together, which is a "
   "theorem rather than an engineering limitation.",
   "Use an equal-area projection for anything quantitative, and name the "
   "projection in the caption.",
   "A choropleth weights each region by its geographic area, which has "
   "nothing to do with its importance.",
   "A map of raw counts of people-related events is a map of population, "
   "almost without exception.",
   "Quantile, equal-interval, and natural-break binnings give visibly "
   "different maps from identical data.",
   "'Is the spatial pattern the finding' is the first question, and it "
   "eliminates a great many maps.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Projection"),
  ("callout", "No projection preserves area, angle, and distance together "
              "— this is a theorem",
   ["<b>A sphere cannot be mapped to a plane without distortion</b> "
    "— <b>it has intrinsic Gaussian curvature and the plane does "
    "not</b> — which is Gauss's theorema egregium and is <b>a "
    "mathematical fact rather than an engineering limitation</b> that "
    "better algorithms will overcome.",
    "<b>So every projection chooses what to preserve:</b> <b>a "
    "conformal projection keeps angles locally and distorts areas; an "
    "equal-area projection keeps areas and distorts shapes; and "
    "compromise projections do neither exactly but spread the error</b> "
    "more evenly.",
    "<b>Which means the choice is determined by the task</b> "
    "(Module 01 &sect;2 again): <b>navigation wants angles "
    "preserved, and any figure that encodes a quantity on area wants "
    "equal area</b> — and <b>using a conformal projection for the "
    "latter is a measurable error</b> rather than a stylistic "
    "preference.",
    "<b>And the familiar world projection is conformal</b> — "
    "Mercator, chosen for navigation — <b>so it inflates the high "
    "latitudes severely</b>, by a large factor near the poles, <b>which "
    "matters whenever a reader compares the visual sizes of countries</b> "
    "and is why so many people's sense of relative national areas is "
    "wrong."]),
  ("ul", ["<b>Equal-area for anything quantitative</b> — because "
          "<b>a reader comparing two regions' shaded areas is making an "
          "area judgement</b> (Module 02 &sect;1's rank five), <b>and "
          "the projection must not already have distorted the areas</b> "
          "before the encoding did.",
          "<b>Conformal for navigation and for local detail</b>, "
          "where angles and local shapes matter and <b>the extent is "
          "small enough that the area distortion is negligible</b> "
          "— which is most city and regional mapping.",
          "<b>A compromise projection for general reference</b>, "
          "which is what most atlases use and <b>is a reasonable default "
          "for a non-quantitative map</b> where no particular property is "
          "being read.",
          "<b>And a local projection for local data</b> — <b>a "
          "country-scale map should use that country's standard national "
          "projection</b>, not a world projection cropped, which "
          "distorts unnecessarily.",
          "<b>With the projection named in the caption</b>, <b>which "
          "almost never happens and should</b> — and <b>is the only "
          "way a reader can know what the areas in the figure mean</b> "
          "(&sect;4's closing argument)."]),

  ("h1", "2 &nbsp; The choropleth problem"),
  ("callout", "A choropleth encodes a value on colour and a region's "
              "importance on its area",
   ["<b>The value is encoded on colour</b>, which is rank six or seven "
    "(Module 02 &sect;1) — so <b>the quantity is read "
    "imprecisely</b>, <b>which is tolerable and is the lesser of the two "
    "problems</b>, since a choropleth is usually read for pattern rather "
    "than for value.",
    "<b>And the region's visual prominence is determined by its "
    "geographic area</b>, which <b>has nothing whatever to do with its "
    "importance, its population, or its contribution to the "
    "total</b> — so <b>a large sparsely populated region dominates "
    "the figure and a dense city is almost invisible.</b>",
    "<b>Which means a choropleth of a per-capita quantity "
    "systematically overweights rural areas</b> in the reader's "
    "impression, and <b>this is a structural property of the "
    "representation rather than a styling problem</b> that better colours "
    "would fix.",
    "<b>So the two defects are:</b> <b>an imprecise quantitative "
    "channel, and an irrelevant weighting by geographic area</b> — "
    "and <b>the second is the one that changes conclusions</b>, because "
    "it determines what the reader perceives as the dominant pattern."]),
  ("code", """CARTOGRAM
    distort the regions so that area encodes the
    value. Fixes the weighting; destroys
    recognisability, and the distortion is itself
    hard to read quantitatively.

DOT DENSITY
    one dot per n units, placed within each region.
    Area then correctly reflects the total, and
    visual density reflects the rate. Good, and it
    needs care about placement so the dots are not
    read as locations.

PROPORTIONAL SYMBOLS
    a circle per region, with area encoding the
    value. Still rank five (Module 02), and at least
    the geography is undistorted and recognisable.

SMALL MULTIPLES OF NON-MAPS
    a sorted bar chart of the regions, which puts the
    value on position -- rank one.

AND THAT LAST ONE IS USUALLY BEST, unless the spatial
pattern IS the finding. Which is the question to ask:
does the reader need the geography?"""),
  ("p", "<b>Does the reader need the geography?</b> — and <b>if "
        "not, a sorted bar chart puts the value on position, which is rank "
        "one</b> and is read an order of magnitude more accurately than "
        "any colour scale. <b>The does-the-reader-need-geography question "
        "is this module's practical core</b>, and it is &sect;4's first "
        "question because it eliminates the majority of maps before any "
        "other decision has to be made."),

  ("break",),
  ("h1", "3 &nbsp; Normalisation"),
  ("callout", "A map of raw counts is a map of population, almost without "
              "exception",
   ["<b>Any count of people-related events — disease cases, "
    "crimes, retail sales, votes, library loans — is roughly "
    "proportional to the number of people present</b>, so <b>the map "
    "shows where the people are</b> and essentially nothing else.",
    "<b>Which looks very much like a finding</b>, because the pattern "
    "is strong, spatially coherent, and reproducible — <b>and it is "
    "a finding about population</b>, which you already knew.",
    "<b>So normalise</b>, by population, by area, by exposure, by "
    "the number at risk, or by whatever the relevant denominator "
    "is — <b>which is Module 03 &sect;3's derivation argument "
    "arriving where it matters most</b> and where it is most often "
    "skipped.",
    "<b>And then the small-denominator problem appears:</b> <b>a rate "
    "computed over a small population is extremely noisy</b>, <b>so the "
    "extreme values are all in the smallest regions</b> — which is "
    "<b>Module 09's subject</b> and <b>requires showing the "
    "uncertainty</b> rather than only the estimate."]),
  ("ul", ["<b>The small-denominator problem</b> — <b>the highest "
          "and the lowest rates are both found in the smallest "
          "regions</b>, by construction rather than by coincidence, "
          "<b>and a naive map highlights noise</b> as though it were "
          "signal (Module 09 &sect;4).",
          "<b>The modifiable areal unit problem</b> — <b>the same "
          "underlying data aggregated to different boundaries gives "
          "visibly different patterns</b>, and <b>the boundaries were "
          "chosen for administrative reasons unrelated to your "
          "question.</b>",
          "<b>Which means the choice of spatial unit is an analytical "
          "decision</b>, and <b>aggregating to a different level is a "
          "legitimate and reportable choice</b> rather than a "
          "manipulation — provided it is stated.",
          "<b>And the binning of the colour scale</b> — "
          "<b>quantiles, equal intervals, and natural breaks give "
          "visibly different maps from identical data</b>, because they "
          "place the class boundaries differently and the boundaries are "
          "where the visual contrast is.",
          "<b>So state the denominator, the units, and the binning, "
          "all three</b> — plus the projection from &sect;1. "
          "<b>The binning choice is as consequential as the "
          "normalisation</b>, and it is even less often "
          "reported."]),

  ("h1", "4 &nbsp; Choosing"),
  ("ul", ["<b>Is the spatial pattern the finding?</b> <b>If not, do "
          "not use a map</b> — use a chart that puts the value on "
          "position (&sect;2's last alternative).",
          "<b>Is the quantity a rate or a count?</b> <b>If it is a "
          "count, either normalise it or use dot density</b>, where "
          "<b>area correctly reflects the total</b> rather than "
          "misrepresenting it.",
          "<b>Does the reader need to recognise the places?</b> <b>If "
          "yes, a cartogram is out</b> — and if no, the cartogram's "
          "main cost disappears.",
          "<b>Is the denominator small anywhere?</b> <b>If so, the "
          "uncertainty has to be shown</b> (Module 09) — or the "
          "small regions will dominate the reader's impression with "
          "noise.",
          "<b>And which projection does the task require?</b> "
          "(&sect;1) — <b>equal-area for anything quantitative</b>, "
          "and named in the caption. <b>'Is the spatial pattern the "
          "finding' is the first question and the one that eliminates "
          "most maps</b> — <b>a great many maps exist because the "
          "data happened to have a location column</b>, which is not a "
          "reason."]),
  ("callout", "And a map is unusually persuasive, which raises the standard",
   ["<b>A map is read as authoritative and concrete in a way that a "
    "bar chart is not</b> — <b>it looks like a photograph of the "
    "world rather than an encoding of a table</b>, and readers extend to "
    "it the credence they give to a geographic fact.",
    "<b>Which means its errors are believed</b>, and <b>a badly "
    "normalised choropleth produces confident wrong conclusions about "
    "places and about the people who live in them</b> — which is a "
    "consequence beyond the figure (CSCE 638 Module 12's framing, "
    "arriving visually).",
    "<b>So the normalisation, the spatial units, the colour binning, "
    "and the projection all have to be stated</b> — <b>four "
    "things</b>, and <b>a typical published map states none of "
    "them.</b>",
    "<b>Which is this module's version of the program's rule</b> "
    "— and <b>the four statements are the difference between a "
    "figure a reader can assess and one they can only believe</b>, which "
    "is Module 13's distinction exactly."]),
 ],
 "resources": [
   ("Munzner, chapter 8 (slides free)",
    "https://www.cs.ubc.ca/~tmm/vadbook/",
    "<b>&sect;2's alternatives</b> — the spatial representation design "
    "space, with the trades."),
   ("Brewer &mdash; Designing Better Maps",
    "https://esripress.esri.com/display/index.cfm?fuseaction=display&websiteID=331",
    "<b>&sect;1 and &sect;3</b> — projections, classification, and "
    "colour for maps, from a cartographer. Library copy."),
   ("Openshaw &mdash; The Modifiable Areal Unit Problem",
    "https://www.taylorfrancis.com/",
    "<b>&sect;3's second trap</b> — the original statement, and it is "
    "a more serious problem than its obscurity suggests. Library "
    "copy."),
   ("Wilke, the geospatial chapters (free)",
    "https://clauswilke.com/dataviz/geospatial-data.html",
    "<b>&sect;1 and &sect;2 practically</b>, with the projection "
    "comparisons drawn out."),
 ],
 "exercises": [
   "<b>Render the same world data in Mercator and in an equal-area "
   "projection</b>, and compare the apparent sizes.",
   "<b>Measure the area inflation</b> at 60 degrees latitude.",
   "<b>Find a published choropleth</b> and identify the largest region "
   "and its population.",
   "<b>Map raw counts of something population-driven</b>, then map the "
   "rate, and compare.",
   "<b>Build a dot density map</b> of the same data.",
   "<b>Build a sorted bar chart</b> of the same data and ask five people "
   "to rank three regions from each.",
   "<b>Find the extreme-rate regions</b> and check their "
   "denominators.",
   "<b>Re-bin one choropleth three ways</b> and compare the maps.",
   "<b>Aggregate the same data to two different unit levels</b> and "
   "compare the patterns.",
   "<b>Write the four required statements</b> for a map you made.",
 ],
 "selfcheck": [
   "Why can no projection preserve everything, and what kind of claim "
   "is that?",
   "Which projection for quantitative data, and why?",
   "Give the four projection choices by purpose.",
   "Name the two defects of a choropleth, and which changes "
   "conclusions.",
   "Give four alternatives and say which is usually best.",
   "Why is a map of counts a map of population?",
   "What is the small-denominator problem?",
   "What is the modifiable areal unit problem, and what follows?",
   "Give the five decision questions in order.",
   "Why does a map's persuasiveness raise the standard, and what four "
   "things must be stated?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Uncertainty",
 "subtitle": "The thing almost always omitted and almost always "
             "decisive.",
 "question": "How sure is the line you drew?",
 "outcomes": [
     "Explain the kinds of uncertainty and their sources.",
     "Explain the representations and what each "
     "communicates.",
     "Explain why error bars are misread.",
     "Explain the frequency framings that work better.",
     "Show uncertainty in a figure and test the reading.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why it is omitted",
   "blurb": "The reasons, which are worth naming."},

  {"t": "callout", "title": "Uncertainty is omitted because it is harder to draw and because it weakens the figure",
   "kind": "The honest account of a widespread practice",
   "body": ["<b>A point estimate is one mark and a distribution is "
            "several</b> — so <b>showing the uncertainty costs "
            "channels, space, and clarity</b>, and a cluttered figure is "
            "a real cost.",
            "<b>And it weakens the apparent finding</b>, which is "
            "the uncomfortable half: <b>a trend with its interval shown "
            "is visibly less convincing than the same trend "
            "alone</b>, and the author knows it.",
            "<b>Which means the omission is frequently an honest "
            "decision with a dishonest effect</b> — the author was "
            "simplifying and the reader concluded something "
            "unsupported.",
            "<b>So the position this module takes is:</b> <b>a point "
            "estimate drawn without its uncertainty invites a conclusion "
            "the data does not support</b>, and that makes showing it a "
            "requirement rather than a refinement."]},

  {"t": "table", "kicker": "Sources", "title": "The kinds, which need different treatment",
   "header": ["Kind", "Source", "Shown as"],
   "widths": [2.6, 4.2, 4.6],
   "rows": [
     ["<b>Sampling</b>", "<b>You measured a sample, not everybody</b>", "<b>A confidence or credible interval</b>"],
     ["<b>Measurement</b>", "<b>The instrument is imprecise</b>", "<b>An error bar, or a band</b>"],
     ["<b>Model</b>", "<b>The fit could have been different</b>", "<b>A band, or several fitted draws</b>"],
     ["<b>Missing data</b>", "<b>Some values are absent</b>", "<b>Explicitly — a gap, not an interpolation</b>"],
     ["<b>Forecast</b>", "<b>The future has not happened</b>", "<b>A widening fan, with the width honest</b>"],
   ],
   "footnote": "<b>Missing data shown as an interpolated line is the "
               "quietest of these failures</b> — the figure asserts "
               "values that were never measured, and nothing in it says "
               "so.",
   "note": "The interpolated-gap failure is specific and worth "
           "naming."},

  {"t": "section", "label": "Part 2", "title": "Error bars are misread",
   "blurb": "Measurably, and in several directions."},

  {"t": "callout", "title": "Readers do not know what an error bar means, and the convention does not say",
   "kind": "Why the standard representation fails",
   "body": ["<b>An error bar may show a standard deviation, a "
            "standard error, a 95% confidence interval, or a range</b> "
            "— <b>and these differ by factors of several</b> on the "
            "same data.",
            "<b>So a figure with unlabelled error bars is not "
            "interpretable</b>, and <b>a large fraction of published "
            "figures do not say</b> which they used.",
            "<b>And readers misread even labelled ones:</b> "
            "<b>they treat non-overlapping bars as significant and "
            "overlapping ones as not</b>, which is wrong in both "
            "directions and is a measured finding.",
            "<b>Plus within-the-bar bias</b> — <b>readers judge "
            "points inside the bar as more likely than points just "
            "outside</b>, as though the interval had a hard "
            "boundary, which it does not."]},

  {"t": "bullets", "kicker": "Better", "title": "The representations that read better",
   "items": [
     "<b>A gradient or a violin</b>, which <b>shows that the "
     "density falls off smoothly</b> rather than implying a "
     "boundary.",
     "",
     "<b>Several draws from the posterior or from the "
     "bootstrap</b> — <b>spaghetti plots</b> — which show "
     "what plausible alternatives actually look "
     "like.",
     "",
     "<b>Hypothetical outcome plots</b>: <b>animate through "
     "individual plausible datasets</b>, which readers interpret "
     "measurably better than static intervals.",
     "",
     "<b>Quantile dotplots</b> — <b>twenty dots, so the "
     "reader counts rather than estimates</b>, which is "
     "Part 3's frequency framing.",
     "",
     "<b>And explicit gaps for missing data</b>, which is the "
     "cheapest and most often skipped.",
   ],
   "footnote": "<b>Quantile dotplots let the reader count rather than "
               "estimate</b> — and counting is a far more reliable "
               "operation than reading a density."},

  {"t": "section", "label": "Part 3", "title": "Frequency framing",
   "blurb": "Which is read more accurately than probability."},

  {"t": "callout", "title": "People read frequencies better than probabilities, which is a design opportunity",
   "kind": "The finding, and what to do with it",
   "body": ["<b>'3 out of 20' is understood more accurately than "
            "'15%'</b>, consistently and across populations — and "
            "<b>a figure showing twenty dots with three highlighted is "
            "understood better still.</b>",
            "<b>Which is why quantile dotplots work:</b> <b>twenty "
            "dots positioned at the quantiles of the distribution</b>, "
            "so <b>the reader counts how many fall beyond a threshold</b> "
            "rather than integrating a density.",
            "<b>And it transfers to any threshold question:</b> "
            "<b>'will this exceed the limit' becomes 'how many of these "
            "twenty are above the line'</b>, which is a counting task "
            "rather than an estimation one.",
            "<b>So where the reader has a decision to make, frame the "
            "uncertainty as a frequency</b> — which is "
            "CSCE 671 §01's task-first framing applied to "
            "uncertainty."]},

  {"t": "section", "label": "Part 4", "title": "Practice",
   "blurb": "What to do, and what to say."},

  {"t": "bullets", "kicker": "Practice", "title": "Showing uncertainty usefully",
   "items": [
     "<b>Say which quantity the interval represents</b>, "
     "always — which costs a caption clause and is omitted "
     "constantly.",
     "",
     "<b>Prefer a representation without a hard "
     "boundary</b> (Part 2), since the boundary is the "
     "thing readers over-read.",
     "",
     "<b>Show the sample size</b>, per group — <b>which a box "
     "plot and an error bar both hide</b> and which determines how much "
     "the interval means.",
     "",
     "<b>Never interpolate across missing data silently</b>, "
     "which asserts measurements that do not exist.",
     "",
     "<b>And for small denominators, show the "
     "uncertainty rather than the point estimate</b> "
     "(Module 08 §3).",
   ],
   "footnote": "<b>Showing the sample size per group is the cheapest "
               "uncertainty information available</b> — and both the "
               "box plot and the error bar conceal "
               "it."},

  {"t": "callout", "title": "And the honest summary",
   "kind": "Closing",
   "body": ["<b>Showing uncertainty makes a figure less "
            "persuasive and more honest</b>, and those pull in opposite "
            "directions whenever somebody wants the figure to persuade.",
            "<b>Which is why it is omitted, and why omitting it is "
            "the subject's commonest honest failure</b> — as "
            "distinct from Module 10's dishonest ones.",
            "<b>And the representations have improved:</b> "
            "<b>gradients, draws, dotplots, and animated outcomes all "
            "read better than error bars</b>, which were a convention "
            "rather than a design.",
            "<b>So there is no longer a good excuse</b> — "
            "<b>the techniques exist, they are implemented in every "
            "library, and they read better</b>, which leaves only the "
            "persuasiveness argument."]},
 ],
 "takeaways": [
   "A point estimate drawn without its uncertainty invites a conclusion the "
   "data does not support.",
   "The omission is frequently an honest simplification with a dishonest "
   "effect.",
   "An error bar may be a standard deviation, a standard error, an "
   "interval, or a range, and these differ by factors of several.",
   "Readers treat non-overlapping bars as significant and overlapping ones "
   "as not, which is wrong in both directions.",
   "People read frequencies better than probabilities, which is why "
   "quantile dotplots let them count rather than estimate.",
   "Showing the sample size per group is the cheapest uncertainty "
   "information available, and both box plots and error bars hide it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why uncertainty is omitted"),
  ("callout", "Uncertainty is omitted because it is harder to draw and "
              "because it weakens the figure",
   ["<b>A point estimate is one mark and a distribution is "
    "several</b> — so <b>showing the uncertainty costs channels, "
    "space, and visual clarity</b>, and <b>a cluttered figure is a real "
    "cost</b> rather than an excuse (Module 02 &sect;3's emphasis "
    "budget).",
    "<b>And it weakens the apparent finding</b>, which is the "
    "uncomfortable half of the explanation: <b>a trend drawn with its "
    "confidence band is visibly less convincing than the same trend drawn "
    "alone</b>, <b>and the author knows it.</b>",
    "<b>Which means the omission is frequently an honest decision with "
    "a dishonest effect</b> — the author was simplifying for "
    "legibility, and the reader concluded something the data does not "
    "support, and nobody intended the outcome.",
    "<b>So the position this module takes is:</b> <b>a point estimate "
    "drawn without its uncertainty invites a conclusion the data does not "
    "support</b>, <b>and that makes showing it a requirement rather than "
    "a refinement</b> — which is why Project 2 fails a figure that "
    "omits it."]),
  ("table", ["Kind", "Where it comes from", "Shown as"],
   [["<b>Sampling uncertainty</b>",
     "<b>You measured a sample rather than the whole population.</b>",
     "<b>A confidence or credible interval.</b>"],
    ["<b>Measurement uncertainty</b>",
     "<b>The instrument or the method is imprecise.</b>",
     "<b>An error bar, or a band around the series.</b>"],
    ["<b>Model uncertainty</b>",
     "<b>The fit could have been different given the same data.</b>",
     "<b>A band, or several fitted draws overlaid</b> (&sect;2)."],
    ["<b>Missing data</b>",
     "<b>Some values are simply absent.</b>",
     "<b>Explicitly — a gap in the line, not an interpolation across "
     "it.</b> See the note."],
    ["<b>Forecast uncertainty</b>",
     "<b>The future has not happened yet.</b>",
     "<b>A widening fan, with the width honestly derived rather than "
     "chosen for appearance.</b>"]],
   [0.20, 0.38, 0.42]),
  ("p", "<b>Missing data shown as an interpolated line is the quietest "
        "of these failures</b> — <b>the figure asserts values that "
        "were never measured, and nothing in it says so</b>. A series "
        "with a six-month gap drawn as a continuous line has invented six "
        "months of data, and the reader has no way to know. <b>The "
        "interpolated-gap failure is specific and worth naming</b>, "
        "because the fix is a single argument in every plotting library "
        "and is simply not reached for."),

  ("h1", "2 &nbsp; Error bars are misread"),
  ("callout", "Readers do not know what an error bar means, and the "
              "convention does not say",
   ["<b>An error bar may show one standard deviation, one standard "
    "error, a 95% confidence interval, the interquartile range, or the "
    "full range</b> — and <b>these differ by factors of several on "
    "exactly the same data</b>, so the bar's length carries no "
    "interpretable meaning on its own.",
    "<b>So a figure with unlabelled error bars is not "
    "interpretable</b>, and <b>a large fraction of published figures do "
    "not say which quantity they used</b> — which is a one-clause "
    "omission that makes the figure's central visual element "
    "meaningless.",
    "<b>And readers misread even the labelled ones:</b> <b>they treat "
    "non-overlapping bars as indicating a significant difference and "
    "overlapping ones as indicating none</b>, <b>which is wrong in both "
    "directions</b> (the relationship depends on which quantity is "
    "plotted and on the test) <b>and is a well-measured finding.</b>",
    "<b>Plus within-the-bar bias</b> — <b>readers judge a point "
    "just inside the bar as substantially more likely than a point just "
    "outside it</b>, <b>as though the interval had a hard boundary</b>, "
    "which it does not: the density is continuous across the end of the "
    "bar."]),
  ("ul", ["<b>A gradient or a violin</b>, which <b>shows that the "
          "density falls off smoothly</b> rather than implying a boundary "
          "— and so directly addresses the within-the-bar bias.",
          "<b>Several draws from the posterior or from a "
          "bootstrap</b> — <b>spaghetti plots</b> — which "
          "<b>show what the plausible alternative fits actually look "
          "like</b>, and communicate the shape of the uncertainty rather "
          "than its width.",
          "<b>Hypothetical outcome plots</b>: <b>animate through "
          "individual plausible datasets</b>, one at a time, <b>which "
          "readers interpret measurably better than static intervals</b> "
          "— one of the few places animation wins "
          "(Module 06 &sect;3's exception).",
          "<b>Quantile dotplots</b> — <b>twenty dots placed at "
          "the distribution's quantiles, so that the reader counts rather "
          "than estimates</b>, which is &sect;3's frequency framing made "
          "visual.",
          "<b>And explicit gaps for missing data</b>, which is "
          "<b>the cheapest of these and the most often skipped</b>. "
          "<b>Quantile dotplots let the reader count rather than "
          "estimate</b> — and <b>counting is a far more reliable "
          "operation than reading a density</b>, which is why they "
          "outperform both bars and bands in testing."]),

  ("break",),
  ("h1", "3 &nbsp; Frequency framing"),
  ("callout", "People read frequencies better than probabilities, which is a "
              "design opportunity",
   ["<b>'3 out of 20' is understood more accurately than '15%'</b>, "
    "consistently, across populations and across levels of numeracy "
    "— and <b>a figure showing twenty dots with three of them "
    "highlighted is understood better still.</b>",
    "<b>Which is exactly why quantile dotplots work:</b> <b>twenty "
    "dots positioned at the quantiles of the predictive "
    "distribution</b>, so that <b>the reader counts how many fall beyond "
    "a threshold</b> <b>rather than integrating a density function by "
    "eye</b>, which nobody does well.",
    "<b>And it transfers to any threshold question:</b> <b>'will this "
    "exceed the limit' becomes 'how many of these twenty are above the "
    "line'</b> — <b>which is a counting task rather than an "
    "estimation task</b>, and counting is accurate.",
    "<b>So where the reader has an actual decision to make, frame the "
    "uncertainty as a frequency</b> — which is <b>CSCE 671 "
    "Module 01's task-first framing applied to uncertainty</b>, and is "
    "the single most useful finding in this module for anybody building "
    "something people will act on."]),

  ("h1", "4 &nbsp; Practice"),
  ("ul", ["<b>Say which quantity the interval represents</b>, "
          "always — standard error, standard deviation, 95% "
          "interval, range — <b>which costs one caption clause and is "
          "omitted constantly</b> (&sect;2).",
          "<b>Prefer a representation without a hard boundary</b> "
          "(&sect;2's list), <b>since the boundary is precisely the thing "
          "readers over-read</b> — a gradient or a dotplot in place "
          "of a capped bar.",
          "<b>Show the sample size, per group</b> — <b>which both "
          "a box plot and an error bar hide completely</b>, and <b>which "
          "determines how much the interval means</b>: an interval from "
          "n = 4 and one from n = 400 look identical and are not.",
          "<b>Never interpolate across missing data silently</b>, "
          "<b>which asserts measurements that do not exist</b> "
          "(&sect;1's note) — break the line, and say in the caption "
          "why.",
          "<b>And for small denominators, show the uncertainty rather "
          "than the point estimate</b> (Module 08 &sect;3's "
          "small-denominator problem) — or consider a shrinkage "
          "estimate, stated as such. <b>Showing the sample size per "
          "group is the cheapest uncertainty information "
          "available</b>, and <b>both the box plot and the error bar "
          "conceal it.</b>"]),
  ("callout", "And the honest summary",
   ["<b>Showing uncertainty makes a figure less persuasive and more "
    "honest</b>, <b>and those two pull in opposite directions whenever "
    "anybody wants the figure to persuade</b> — which is most of the "
    "time, and is the real explanation for &sect;1.",
    "<b>Which is why it is omitted, and why omitting it is this "
    "subject's commonest <i>honest</i> failure</b> — as distinct "
    "from Module 10's deliberate ones, which are rarer and easier to "
    "condemn.",
    "<b>And the representations have genuinely improved:</b> "
    "<b>gradients, posterior draws, quantile dotplots, and hypothetical "
    "outcome plots all read measurably better than error bars</b>, "
    "<b>which were a convention inherited from print rather than a "
    "design</b>.",
    "<b>So there is no longer a good excuse</b> — <b>the "
    "techniques exist, they are implemented in every major library, and "
    "they read better</b> — <b>which leaves only the "
    "persuasiveness argument</b>, and that one is worth naming out loud "
    "when it is what is actually operating."]),
 ],
 "resources": [
   ("Wilke, the uncertainty chapters (free)",
    "https://clauswilke.com/dataviz/visualizing-uncertainty.html",
    "<b>The whole module</b>, free — and the best available practical "
    "treatment, with every representation drawn."),
   ("Hullman et al. &mdash; Hypothetical Outcome Plots (free)",
    "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0142444",
    "<b>&sect;2's animated representation, measured</b> — and it reads "
    "better than static intervals, which is the finding."),
   ("Kay et al. &mdash; When (ish) is My Bus? (free)",
    "https://dl.acm.org/doi/10.1145/2858036.2858558",
    "<b>&sect;3's quantile dotplots in the original</b> — the "
    "frequency framing applied to a real decision."),
   ("Belia et al. &mdash; Researchers misunderstand confidence "
    "intervals (free)",
    "https://psycnet.apa.org/record/2005-03518-003",
    "<b>&sect;2's misreading, measured on researchers</b> — which is "
    "the relevant population and the sobering result."),
 ],
 "exercises": [
   "<b>Take a figure you made</b> and add the uncertainty, then compare "
   "how persuasive each looks.",
   "<b>Classify the uncertainty in one dataset</b> into the five "
   "kinds.",
   "<b>Find a figure with unlabelled error bars</b> and compute what "
   "three different interpretations would mean.",
   "<b>Ask five people whether two overlapping error bars indicate a "
   "significant difference.</b>",
   "<b>Draw the same uncertainty as a bar, a gradient, and a quantile "
   "dotplot</b>, and test the readings.",
   "<b>Build a spaghetti plot</b> from bootstrap draws.",
   "<b>Pose a threshold question</b> and compare a percentage against a "
   "twenty-dot framing.",
   "<b>Find a series with missing data drawn as continuous</b>, and fix "
   "it.",
   "<b>Add the per-group n</b> to a box plot.",
   "<b>Find a small-denominator extreme</b> on a map and show its "
   "interval.",
 ],
 "selfcheck": [
   "Give the two reasons uncertainty is omitted, and why the omission "
   "is usually honest.",
   "State the position this module takes.",
   "Name five kinds of uncertainty and how each is shown.",
   "Which failure is quietest, and why?",
   "Why is an unlabelled error bar uninterpretable?",
   "Give two ways readers misread error bars.",
   "Name five better representations.",
   "Why do quantile dotplots work?",
   "State the frequency finding and how to use it.",
   "Give five practice rules, and the cheapest one.",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Deception",
 "subtitle": "The deliberate failures, and the conventions that prevent "
             "them.",
 "question": "How is this chart lying?",
 "outcomes": [
     "Recognise the standard deceptive techniques.",
     "Explain the axis conventions and their reasons.",
     "Explain selective framing and aggregation.",
     "Distinguish deception from a design mistake.",
     "Review a figure for deception.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Axis manipulation",
   "blurb": "The commonest, and the easiest to check."},

  {"t": "table", "kicker": "Axes", "title": "The axis techniques and what each does",
   "header": ["Technique", "Effect", "The convention"],
   "widths": [2.7, 4.1, 5.0],
   "rows": [
     ["<b>Truncated bar axis</b>", "<b>Exaggerates every difference</b>", "<b>Bars start at zero (M05 §4)</b>"],
     ["<b>Inverted axis</b>", "<b>Reverses the apparent trend</b>", "<b>Up means more, unless labelled loudly</b>"],
     ["<b>Dual axis</b>", "<b>Any crossing can be manufactured</b>", "<b>Use two panels (M05 §3)</b>"],
     ["<b>Unlabelled log scale</b>", "<b>Linear extrapolation from a log plot</b>", "<b>Label it prominently</b>"],
     ["<b>Irregular tick spacing</b>", "<b>Distorts the apparent rate</b>", "<b>Uniform spacing, or a stated break</b>"],
     ["<b>Aspect ratio choice</b>", "<b>Makes a trend flat or steep</b>", "<b>Bank to 45°, or state the choice</b>"],
   ],
   "footnote": "<b>The axis techniques are checkable in seconds</b> "
               "— look at the baseline, the direction, the scale "
               "type, and the tick spacing, which is four glances and "
               "catches most of this.",
   "note": "The four-glance check is the practical artefact."},

  {"t": "callout", "title": "A truncated bar axis is a deception and a truncated line axis is not",
   "kind": "The distinction, from the channel",
   "body": ["<b>A bar's length is read as a ratio from the "
            "baseline</b> (Module 02 §1) — so "
            "<b>truncating the axis makes a 2% difference look like a "
            "50% one</b>, by an amount the reader cannot "
            "recover.",
            "<b>A line's position is read against the scale</b>, "
            "which is labelled — so <b>a line chart with a non-zero "
            "axis is showing the variation at the resolution it "
            "occurs</b>, which is frequently the correct "
            "choice.",
            "<b>Which means the rule has a reason rather than being a "
            "convention</b> — and the reason tells you the "
            "exception: <b>a line chart whose axis is truncated so far "
            "that the variation is noise is also deceptive.</b>",
            "<b>So the test is not 'does the axis start at zero' but "
            "'does the encoding depend on the baseline'</b> — which "
            "is a question about the channel and settles both cases."]},

  {"t": "section", "label": "Part 2", "title": "Selective framing",
   "blurb": "Where no axis is touched and the figure still lies."},

  {"t": "bullets", "kicker": "Framing", "title": "The techniques that need no chart manipulation at all",
   "items": [
     "<b>Choosing the time window</b> — <b>any trend can be "
     "found in a long enough series by choosing the endpoints</b>, and "
     "the figure is entirely accurate.",
     "",
     "<b>Choosing the comparison</b> — against last month, "
     "last year, the forecast, or a competitor, each of which gives a "
     "different story.",
     "",
     "<b>Choosing the aggregation level</b> — <b>which is "
     "CSCE 679 §08 §3's areal unit problem applied "
     "to time and to categories.</b>",
     "",
     "<b>Omitting a series</b>, which is invisible — <b>a "
     "reader cannot see what is not plotted</b>.",
     "",
     "<b>And choosing the denominator</b> "
     "(Module 03 §3), which can reverse a "
     "conclusion without any number being wrong.",
   ],
   "footnote": "<b>A reader cannot see what is not plotted</b> "
               "— which makes omission the most effective and least "
               "detectable technique in the module."},

  {"t": "callout", "title": "Which makes selective framing harder to detect than axis manipulation",
   "kind": "Why the conventions are not sufficient",
   "body": ["<b>Every number in a selectively framed figure is "
            "correct</b>, every axis is conventional, and <b>the "
            "deception is entirely in what was left out.</b>",
            "<b>So no inspection of the figure detects it</b> "
            "— <b>you have to know the data, or ask what the other "
            "windows and comparisons would show</b>, which a reader "
            "generally cannot.",
            "<b>Which means the defence is procedural rather than "
            "visual:</b> <b>ask for the longer series, the other "
            "comparison, and the missing category</b> — and <b>treat "
            "an unusual window as a question.</b>",
            "<b>And in your own work, the defence is to show the "
            "alternatives</b> — <b>if three windows tell the same "
            "story, show one and say so; if they do not, that is the "
            "finding.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Deception and mistake",
   "blurb": "A distinction worth being careful about."},

  {"t": "callout", "title": "Most bad charts are mistakes, and the techniques are identical either way",
   "kind": "The fair reading",
   "body": ["<b>A truncated axis produced by a library default is a "
            "mistake; the same axis chosen to exaggerate a difference is "
            "a deception</b> — and <b>the figure is "
            "identical.</b>",
            "<b>So you cannot infer intent from a figure</b>, and "
            "attempting to is both unfair and unnecessary: <b>the "
            "correction is the same either way.</b>",
            "<b>Which is the useful position:</b> <b>name the "
            "technique and its effect, not the motive</b> — 'this "
            "axis exaggerates the difference by a factor of ten' is "
            "checkable and 'this is misleading' is an "
            "accusation.",
            "<b>And it is CSCE 671 §12's "
            "dual-use point</b> — <b>the same techniques serve honest "
            "simplification and deliberate deception</b>, which is why "
            "the review looks for effects rather than for "
            "intentions."]},

  {"t": "section", "label": "Part 4", "title": "Reviewing",
   "blurb": "A checklist, since this is checkable."},

  {"t": "code", "kicker": "Review", "title": "The review, in order",
   "lang": "text", "code": """
  THE FOUR GLANCES (Part 1)
      does the bar axis start at zero?
      which direction is "more"?
      is the scale linear or log, and is it labelled?
      are the ticks evenly spaced?

  THEN THE FRAMING (Part 2)
      what time window, and why that one?
      compared against what, and why that?
      what aggregation level?
      what is not shown?
      what is the denominator?

  THEN THE UNCERTAINTY (Module 09)
      is there any, and is it shown?
      what is the sample size?

  AND THEN THE ENCODING (Module 02 section 4)
      is the main variable on a high-ranked channel?

  WHICH IS FOUR PASSES, AND TAKES A FEW MINUTES.
""",
   "caption": "<b>Four passes, a few minutes</b> — and it covers "
              "the deliberate deceptions, the honest omissions, and the "
              "encoding errors in one pass each.",
   "note": "This checklist is the module's deliverable."},

  {"t": "callout", "title": "And the asymmetry worth stating",
   "kind": "Closing",
   "body": ["<b>A figure is much easier to make misleading than to "
            "make honest</b>, because <b>the honest version requires "
            "stating the window, the denominator, the units, the "
            "uncertainty, and what is not shown</b> — five things, "
            "each of which weakens the impression.",
            "<b>So the incentive runs toward the misleading "
            "version</b> wherever a figure is meant to persuade — "
            "which is CSCE 671 §12 §4's measurement "
            "argument in this subject.",
            "<b>And the defence is the same:</b> <b>a figure that "
            "states its choices is checkable, and a reader who knows the "
            "checklist can ask.</b>",
            "<b>Which is why this module is a checklist rather than "
            "an ethics lecture</b> — <b>the technique names and the "
            "four passes are what actually transfer.</b>"]},
 ],
 "takeaways": [
   "The axis techniques are checkable in four glances: baseline, "
   "direction, scale type, and tick spacing.",
   "A truncated bar axis is a deception and a truncated line axis may not "
   "be, and the reason is the channel rather than a convention.",
   "Selective framing needs no chart manipulation at all: every number is "
   "correct and the deception is in what was omitted.",
   "A reader cannot see what is not plotted, which makes omission the most "
   "effective and least detectable technique.",
   "You cannot infer intent from a figure, and the correction is the same "
   "either way — so name the effect rather than the motive.",
   "A figure is much easier to make misleading than honest, because the "
   "honest version requires five statements that each weaken the "
   "impression.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Axis manipulation"),
  ("table", ["Technique", "Its effect", "The convention"],
   [["<b>Truncated bar axis</b>",
     "<b>Exaggerates every difference in the figure.</b>",
     "<b>Bars start at zero</b> (Module 05 &sect;4) — see the "
     "callout."],
    ["<b>Inverted axis</b>",
     "<b>Reverses the apparent direction of the trend.</b>",
     "<b>Up means more, unless the inversion is labelled very "
     "loudly</b> — and occasionally it is justified."],
    ["<b>Dual axis</b>",
     "<b>Any crossing or divergence can be manufactured by rescaling "
     "one side.</b>",
     "<b>Use two stacked panels sharing an x axis</b> (Module 05 "
     "&sect;3)."],
    ["<b>Unlabelled log scale</b>",
     "<b>Readers extrapolate linearly from a log plot.</b>",
     "<b>Label it prominently</b>, not only in the tick values."],
    ["<b>Irregular tick spacing</b>",
     "<b>Distorts the apparent rate of change.</b>",
     "<b>Uniform spacing, or a clearly marked axis break.</b>"],
    ["<b>Aspect ratio choice</b>",
     "<b>Makes the same trend look flat or steep.</b>",
     "<b>Bank to 45 degrees, or state the choice</b> (Module 05 "
     "&sect;4)."]],
   [0.22, 0.33, 0.45]),
  ("p", "<b>The axis techniques are checkable in seconds</b> — "
        "<b>look at the baseline, the direction, the scale type, and the "
        "tick spacing</b>, <b>which is four glances and catches most of "
        "this category</b>. <b>The four-glance check is the practical "
        "artefact</b> of this section, and it is worth running on every "
        "figure you read rather than only on the suspicious ones, since "
        "the suspicious ones are the ones designed not to look it."),
  ("callout", "A truncated bar axis is a deception and a truncated line axis "
              "is not",
   ["<b>A bar's length is read as a ratio from the baseline</b> "
    "(Module 02 &sect;1's shared-reference argument) — so "
    "<b>truncating the axis makes a 2% difference look like a 50% "
    "one</b>, <b>by an amount the reader cannot recover</b> even if they "
    "notice the axis label.",
    "<b>A line's position is read against the scale</b>, which is "
    "labelled and gridded — so <b>a line chart with a non-zero axis "
    "is showing the variation at the resolution at which it actually "
    "occurs</b>, <b>which is frequently the correct choice</b> and is "
    "sometimes the only legible one.",
    "<b>Which means the rule has a reason rather than being an "
    "arbitrary convention</b> — and <b>the reason tells you the "
    "exception</b>: <b>a line chart whose axis is truncated so far that "
    "the visible variation is measurement noise is also deceptive</b>, "
    "even though no bar was involved.",
    "<b>So the test is not 'does the axis start at zero' but 'does "
    "the encoding depend on the baseline'</b> — <b>which is a "
    "question about the channel and settles both cases</b> and any new "
    "one, which is what a mechanism buys over a rule (CSCE 671 "
    "Module 05 &sect;1)."]),

  ("h1", "2 &nbsp; Selective framing"),
  ("ul", ["<b>Choosing the time window</b> — <b>any trend at all "
          "can be found in a long enough series by choosing the "
          "endpoints</b>, <b>and the resulting figure is entirely "
          "accurate</b>, which is what makes it effective.",
          "<b>Choosing the comparison</b> — against last month, "
          "last year, the same quarter two years ago, the forecast, or a "
          "competitor — <b>each of which gives a different "
          "story</b> from the same underlying number.",
          "<b>Choosing the aggregation level</b> — daily, weekly, "
          "or monthly; by region or by country — <b>which is "
          "Module 08 &sect;3's modifiable areal unit problem applied "
          "to time and to categories</b>, and has the same "
          "consequence.",
          "<b>Omitting a series entirely</b>, which is <b>invisible: "
          "a reader cannot see what is not plotted</b>, and there is no "
          "trace in the figure that anything is missing.",
          "<b>And choosing the denominator</b> (Module 03 "
          "&sect;3), <b>which can reverse a conclusion without any "
          "individual number being wrong</b>. <b>A reader cannot see "
          "what is not plotted</b> — <b>which makes omission the "
          "most effective and the least detectable technique in this "
          "module</b>, and the one no checklist of axis conventions "
          "catches."]),
  ("callout", "Which makes selective framing harder to detect than axis "
              "manipulation",
   ["<b>Every number in a selectively framed figure is correct</b>, "
    "every axis is conventional, every scale is labelled, and <b>the "
    "deception is entirely in what was left out</b> of the frame.",
    "<b>So no amount of inspection of the figure itself detects "
    "it</b> — <b>you have to know the underlying data, or ask what "
    "the other windows and the other comparisons would show</b>, <b>which "
    "a reader generally cannot do</b> and which is the asymmetry the "
    "technique exploits.",
    "<b>Which means the defence is procedural rather than "
    "visual:</b> <b>ask for the longer series, the alternative "
    "comparison, and the missing category</b> — and <b>treat an "
    "unusual window as a question</b> rather than as a fact (why does "
    "this series begin in 2017?).",
    "<b>And in your own work, the defence is to show the "
    "alternatives</b> — <b>if three different windows tell the same "
    "story, show one and say that the others agree; and if they do not "
    "agree, that disagreement is the finding</b> and belongs in the "
    "figure."]),

  ("break",),
  ("h1", "3 &nbsp; Deception and mistake"),
  ("callout", "Most bad charts are mistakes, and the techniques are "
              "identical either way",
   ["<b>A truncated axis produced by a plotting library's default is a "
    "mistake; the same truncated axis chosen deliberately to exaggerate a "
    "difference is a deception</b> — and <b>the resulting figure is "
    "identical in every respect.</b>",
    "<b>So you cannot infer intent from a figure</b>, and attempting "
    "to is both unfair and unnecessary: <b>the correction is exactly the "
    "same either way</b>, and the correction is what you wanted.",
    "<b>Which gives the useful position:</b> <b>name the technique "
    "and its effect, not the motive</b> — <b>'this axis exaggerates "
    "the difference by a factor of ten' is checkable, and 'this chart is "
    "misleading' is an accusation</b> that invites a defence rather than "
    "a fix.",
    "<b>And it is CSCE 671 Module 12's dual-use point in this "
    "subject</b> — <b>the same techniques serve honest simplification "
    "and deliberate deception</b> — <b>which is why the review in "
    "&sect;4 looks for effects rather than for intentions</b> and is "
    "therefore usable in a meeting."]),

  ("h1", "4 &nbsp; Reviewing"),
  ("code", """THE FOUR GLANCES (section 1)
    does the bar axis start at zero?
    which direction is "more"?
    is the scale linear or logarithmic, and is it
        labelled?
    are the ticks evenly spaced?

THEN THE FRAMING (section 2)
    what time window, and why that one?
    compared against what, and why that?
    what aggregation level?
    what is not shown?
    what is the denominator?

THEN THE UNCERTAINTY (Module 09)
    is there any, and is it shown?
    what is the sample size?

AND THEN THE ENCODING (Module 02 section 4)
    is the main variable on a high-ranked channel?

WHICH IS FOUR PASSES, AND TAKES A FEW MINUTES."""),
  ("p", "<b>Four passes, a few minutes</b> — and <b>it covers the "
        "deliberate deceptions, the honest omissions, and the encoding "
        "errors in one pass each</b>, which is the full set of ways a "
        "figure can mislead. <b>This checklist is the module's "
        "deliverable</b>, and it composes the previous nine modules into "
        "something you can run on a figure you did not make, which is most "
        "of the figures you will encounter."),
  ("callout", "And the asymmetry worth stating",
   ["<b>A figure is much easier to make misleading than to make "
    "honest</b>, because <b>the honest version requires stating the time "
    "window, the denominator, the spatial or categorical units, the "
    "uncertainty, and what is not shown</b> — <b>five things, each "
    "of which weakens the impression the figure makes.</b>",
    "<b>So the incentive runs toward the misleading version</b> "
    "wherever a figure is meant to persuade rather than to inform "
    "— which is <b>CSCE 671 Module 12 &sect;4's measurement "
    "argument arriving in this subject</b>: the easy path moves the "
    "metric and the costs land elsewhere.",
    "<b>And the defence is the same as it was there:</b> <b>a figure "
    "that states its choices is checkable, and a reader who knows the "
    "checklist can ask the questions</b> — which shifts the cost "
    "back to whoever framed it.",
    "<b>Which is why this module is a checklist rather than an ethics "
    "lecture</b> — <b>the technique names and the four passes are "
    "what actually transfer</b>, and a general exhortation to be honest "
    "does not survive contact with a deadline."]),
 ],
 "resources": [
   ("Wilke, the pitfalls and the honesty chapters (free)",
    "https://clauswilke.com/dataviz/",
    "<b>&sect;1 and &sect;2</b>, with the examples drawn and the axis "
    "arguments made from the channels."),
   ("Pandey et al. &mdash; How Deceptive are Deceptive "
    "Visualizations? (free)",
    "https://dl.acm.org/doi/10.1145/2702123.2702608",
    "<b>&sect;1 measured</b> — how much a truncated axis actually "
    "changes a reader's judgement, which is a large amount."),
   ("Cairo &mdash; How Charts Lie",
    "https://wwnorton.com/books/9781324001560",
    "<b>&sect;2's selective framing in depth</b> — and the best "
    "available treatment of the omission techniques. Library copy."),
   ("Huff &mdash; How to Lie with Statistics",
    "https://wwnorton.com/books/9780393310726",
    "<b>&sect;2 from 1954</b>, and still accurate — which is itself "
    "informative about how little the techniques have changed."),
 ],
 "exercises": [
   "<b>Take one dataset and produce the most misleading honest figure "
   "you can</b>, using only framing.",
   "<b>Then produce the most honest one</b>, and list what you had to "
   "state.",
   "<b>Truncate a bar axis</b> and measure how much the apparent "
   "difference grows.",
   "<b>Ask five people to estimate the ratio</b> from each version.",
   "<b>Find a published dual-axis chart</b> and rescale it to reverse "
   "the story.",
   "<b>Find a trend by choosing endpoints</b> in a long series, three "
   "different ways.",
   "<b>Find a figure where a series is omitted</b>, and say how you "
   "knew.",
   "<b>Run the four glances</b> on ten published figures.",
   "<b>Run all four passes</b> on one figure in detail.",
   "<b>Rewrite one 'this chart is misleading' complaint</b> as a "
   "statement of effect.",
 ],
 "selfcheck": [
   "Name six axis techniques and the convention for each.",
   "Give the four glances.",
   "Why is a truncated bar axis deceptive and a truncated line axis "
   "sometimes not?",
   "State the test that settles both cases.",
   "Name five selective framing techniques.",
   "Why is omission the most effective, and what is the defence?",
   "Why can you not detect selective framing from the figure?",
   "Why can intent not be inferred, and what should you name instead?",
   "Give the four review passes.",
   "State the asymmetry and why the incentive runs the way it does.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Scale",
 "subtitle": "When there are more data points than pixels.",
 "question": "How do you draw a billion points?",
 "outcomes": [
     "Explain overplotting and its consequences.",
     "Explain binning and density as the general answer.",
     "Explain sampling and when it is acceptable.",
     "Explain the rendering and interaction constraints.",
     "Visualise a dataset larger than the display.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Overplotting",
   "blurb": "The failure, and it is worse than it looks."},

  {"t": "callout", "title": "Overplotting destroys the density information, which was usually the finding",
   "kind": "The problem, stated precisely",
   "body": ["<b>When marks overlap, the figure saturates</b> — "
            "<b>a region with a hundred points and a region with ten "
            "thousand look identical</b>, so the densest part of the "
            "data is where the figure conveys least.",
            "<b>And it is order-dependent:</b> <b>the last points "
            "drawn are visible and the first are hidden</b>, so the "
            "figure depends on the row order of the file, which is "
            "arbitrary.",
            "<b>Which means the apparent outliers are the only "
            "reliable feature</b> — they are the points with nothing "
            "on top of them — and <b>the main mass is "
            "uninterpretable.</b>",
            "<b>So partial transparency is the first fix and is not "
            "sufficient</b>: <b>it saturates too, at a higher "
            "threshold</b>, and the threshold depends on the alpha value "
            "you happened to choose."]},

  {"t": "section", "label": "Part 2", "title": "Binning",
   "blurb": "The general answer: draw the density, not the points."},

  {"t": "code", "kicker": "Binning", "title": "Aggregate before drawing",
   "lang": "text", "code": """
  THE IDEA
      there are more data points than pixels, so
      aggregate to the pixel grid and encode the
      count on colour. One mark per bin, not per
      point.

  WHICH GIVES
      2D histogram / heatmap    rectangular bins
      hexbin                    hexagonal bins, with
                                more uniform
                                neighbour distances
      datashader-style          one bin per pixel,
                                with the count scaled
                                carefully

  AND THE SCALING OF THE COUNT MATTERS
      linear colour hides the structure outside the
          densest region
      log or a rank-based scale reveals it
      which is Module 08 section 3's binning choice
          again, with the same consequence

  SO: the colour scale on a density plot is as
  consequential as the bin size, and both should be
  stated.
""",
   "caption": "<b>The colour scale on a density plot is as "
              "consequential as the bin size</b> — a linear scale "
              "hides everything outside the mode.",
   "note": "The count-scaling point is what distinguishes a good "
           "density plot from a dark smudge."},

  {"t": "callout", "title": "And binning is a derivation, so the bins are an analytical choice",
   "kind": "The same warning as everywhere else in this course",
   "body": ["<b>The bin size changes the apparent structure</b> "
            "— <b>too fine and it is noise; too coarse and the "
            "structure is averaged away</b> — which is "
            "Module 05 §2's histogram problem in two "
            "dimensions.",
            "<b>And the bin boundaries can create or destroy apparent "
            "features</b>, particularly where the data has a natural "
            "grid or a rounding artefact.",
            "<b>So report the bin size and the count "
            "scaling</b>, and <b>check the figure at two or three bin "
            "sizes</b> before trusting a feature.",
            "<b>Which is the discipline this whole course "
            "repeats:</b> <b>any choice that changes the picture is an "
            "analytical decision and belongs in the "
            "caption</b> (Module 13)."]},

  {"t": "section", "label": "Part 3", "title": "Sampling",
   "blurb": "Which works, with a caveat."},

  {"t": "bullets", "kicker": "Sampling", "title": "When a sample is enough, and when it is not",
   "items": [
     "<b>For the overall shape, a sample is "
     "sufficient</b> — <b>ten thousand points show the same "
     "distribution as ten million</b>, and far more legibly.",
     "",
     "<b>And it is much cheaper</b> — in rendering, in "
     "transfer, and in interaction latency "
     "(CSCE 671 §11 §3).",
     "",
     "<b>But it loses the rare cases</b>, and <b>the rare cases "
     "are frequently the point</b> — outliers, anomalies, and "
     "small subgroups all disappear from a uniform "
     "sample.",
     "",
     "<b>So: sample for the shape and keep the extremes</b> "
     "— a stratified sample that over-represents the tails, which "
     "is explicit and effective.",
     "",
     "<b>And state the sampling</b>, because <b>a reader will "
     "assume they are seeing everything.</b>",
   ],
   "footnote": "<b>A reader will assume they are seeing "
               "everything</b> — so an unstated sample is a figure "
               "about data the reader does not know was "
               "selected."},

  {"t": "section", "label": "Part 4", "title": "The system constraints",
   "blurb": "Which shape what is possible."},

  {"t": "bullets", "kicker": "Constraints", "title": "What limits a large-data visualisation",
   "items": [
     "<b>Pixels.</b> <b>A display has a few million</b>, so "
     "anything beyond that is aggregated whether you chose to or "
     "not — the question is only whether you chose the "
     "aggregation.",
     "",
     "<b>Transfer.</b> <b>Sending a billion points to a browser "
     "is not possible</b>, so the aggregation has to happen server-side "
     "— which is why the architecture is the design.",
     "",
     "<b>Interaction latency.</b> <b>Under 100 ms for a brush to "
     "feel direct</b> (CSCE 671 §11 §3), which bounds "
     "what can be recomputed on each "
     "interaction.",
     "",
     "<b>So: precompute the aggregations you will need</b>, which "
     "is a data cube, and is how interactive large-data "
     "visualisation actually works.",
     "",
     "<b>And degrade deliberately</b> — show a sample while "
     "dragging and the full aggregate on release.",
   ],
   "footnote": "<b>Precompute the aggregations you will need</b> "
               "— which turns an interactive query into a lookup, and "
               "is the only way the latency budget is "
               "met."},

  {"t": "callout", "title": "And the honest summary of this module",
   "kind": "Closing",
   "body": ["<b>At scale you are always showing a summary</b> "
            "— binned, sampled, or aggregated — <b>so the "
            "question is which summary and whether you said "
            "so.</b>",
            "<b>Which is CSCE 676 §01 §2's framing "
            "exactly:</b> <b>an approximation with a stated bound is a "
            "result, and an exact answer you cannot compute is "
            "not.</b>",
            "<b>So state the aggregation, the bin size, the count "
            "scaling, and any sampling</b> — four things, and the "
            "figure is then assessable.",
            "<b>And the risk is specific:</b> <b>a density plot looks "
            "authoritative and is a function of four choices the reader "
            "cannot see</b>, which is the same problem as "
            "Module 08's map and has the same fix."]},
 ],
 "takeaways": [
   "Overplotting destroys the density information, so a region with a "
   "hundred points and one with ten thousand look identical.",
   "It is order-dependent, so the figure depends on the arbitrary row order "
   "of the file.",
   "Transparency saturates too, at a higher threshold that depends on the "
   "alpha you chose.",
   "The colour scale on a density plot is as consequential as the bin "
   "size, and a linear scale hides everything outside the mode.",
   "A sample shows the shape and loses the rare cases, which are "
   "frequently the point — so stratify and keep the extremes.",
   "At scale you are always showing a summary, so the question is which "
   "one and whether you said so.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Overplotting"),
  ("callout", "Overplotting destroys the density information, which was "
              "usually the finding",
   ["<b>When marks overlap, the figure saturates</b> — <b>a region "
    "containing a hundred points and a region containing ten thousand "
    "look identical</b> — so <b>the densest part of the data is "
    "exactly where the figure conveys least</b>, which inverts what you "
    "wanted.",
    "<b>And it is order-dependent:</b> <b>the last points drawn are "
    "visible and the first are hidden beneath them</b>, so <b>the figure "
    "depends on the row order of the input file</b>, which is arbitrary "
    "and frequently sorted by something meaningful — making the "
    "visible points a biased subset.",
    "<b>Which means the apparent outliers are the only reliable "
    "feature of an overplotted figure</b> — they are precisely the "
    "points with nothing drawn on top of them — and <b>the main mass "
    "is uninterpretable</b>, which is the opposite of the usual "
    "intention.",
    "<b>So partial transparency is the first fix and it is not "
    "sufficient</b>: <b>it saturates too, at a higher threshold</b>, "
    "<b>and the threshold depends on whatever alpha value you happened "
    "to choose</b> — which makes it another undisclosed parameter "
    "(&sect;2's callout)."]),

  ("h1", "2 &nbsp; Binning"),
  ("code", """THE IDEA
    there are more data points than pixels, so
    aggregate to the pixel grid and encode the count
    on colour. One mark per bin, not one per point.

WHICH GIVES
    2D histogram / heatmap    rectangular bins
    hexbin                    hexagonal bins, with
                              more uniform neighbour
                              distances and less
                              visual aliasing
    datashader-style          one bin per pixel, with
                              the count scaled
                              carefully

AND THE SCALING OF THE COUNT MATTERS
    linear colour hides the structure outside the
        densest region entirely
    log or a rank-based scale reveals it
    which is Module 08 section 3's binning choice
        again, with the same consequence

SO: the colour scale on a density plot is as
consequential as the bin size, and both should be
stated."""),
  ("p", "<b>The colour scale on a density plot is as consequential as "
        "the bin size</b> — <b>a linear scale hides everything "
        "outside the mode</b>, because the mode's count may be several "
        "orders of magnitude above the rest and compresses all the "
        "remaining structure into the bottom of the scale. <b>The "
        "count-scaling point is what distinguishes a good density plot "
        "from a dark smudge with a bright spot</b>, and it is the single "
        "most common defect in large-data figures."),
  ("callout", "And binning is a derivation, so the bins are an analytical "
              "choice",
   ["<b>The bin size changes the apparent structure</b> — <b>too "
    "fine and the figure shows noise; too coarse and the structure is "
    "averaged away</b> — which is <b>Module 05 &sect;2's "
    "histogram problem in two dimensions</b> and with the same lack of a "
    "principled answer.",
    "<b>And the bin boundaries can create or destroy apparent "
    "features</b>, particularly <b>where the data has a natural grid or "
    "a rounding artefact</b> — values rounded to the nearest five "
    "will produce stripes at some bin sizes and not others, and the "
    "stripes are in the binning rather than in the world.",
    "<b>So report the bin size and the count scaling</b>, and "
    "<b>check the figure at two or three different bin sizes before "
    "trusting any feature you see in it</b> — which takes minutes and "
    "is the equivalent of CSCE 676 Module 04 &sect;3's stability "
    "check.",
    "<b>Which is the discipline this whole course repeats:</b> <b>any "
    "choice that changes the picture is an analytical decision and "
    "belongs in the caption</b> (Module 13 &sect;2), and this module "
    "adds four such choices to the list."]),

  ("break",),
  ("h1", "3 &nbsp; Sampling"),
  ("ul", ["<b>For the overall shape, a sample is entirely "
          "sufficient</b> — <b>ten thousand points show the same "
          "distribution as ten million</b>, and <b>show it considerably "
          "more legibly</b> since they do not overplot.",
          "<b>And it is very much cheaper</b> — in rendering time, "
          "in network transfer, and in interaction latency "
          "(CSCE 671 Module 11 &sect;3's thresholds, which this "
          "module has to meet).",
          "<b>But it loses the rare cases</b>, and <b>the rare cases "
          "are frequently the point</b> — <b>outliers, anomalies, and "
          "small subgroups all disappear from a uniform sample</b>, which "
          "is CSCE 676 Module 08's subject vanishing from the "
          "figure.",
          "<b>So: sample for the shape and keep the extremes</b> "
          "— <b>a stratified sample that deliberately "
          "over-represents the tails</b>, which is explicit, effective, "
          "and easy to implement.",
          "<b>And state the sampling</b>, because <b>a reader will "
          "assume they are seeing everything</b>. <b>An unstated sample "
          "is a figure about data the reader does not know was "
          "selected</b> — and if the sampling was non-uniform, the "
          "figure is about a distribution that does not exist."]),

  ("h1", "4 &nbsp; The system constraints"),
  ("ul", ["<b>Pixels.</b> <b>A display has a few million of "
          "them</b>, so <b>anything beyond that is aggregated whether "
          "you chose to aggregate or not</b> — <b>the only question "
          "is whether you chose the aggregation</b> or let the rendering "
          "order choose it for you (&sect;1).",
          "<b>Transfer.</b> <b>Sending a billion points to a browser "
          "is simply not possible</b>, so <b>the aggregation has to "
          "happen server-side</b> — <b>which is why the architecture "
          "is the design</b> rather than an implementation detail "
          "(CSCE 676 Module 10).",
          "<b>Interaction latency.</b> <b>Under 100 ms for a brush "
          "to feel direct</b> (CSCE 671 Module 11 &sect;3), <b>which "
          "bounds what can be recomputed on each interaction</b> and "
          "therefore bounds what interactions you can offer at all.",
          "<b>So: precompute the aggregations you will need</b>, "
          "<b>which is a data cube</b>, and <b>is how interactive "
          "large-data visualisation actually works</b> — the "
          "interaction becomes a lookup in a precomputed structure rather "
          "than a query over the raw data.",
          "<b>And degrade deliberately</b> — <b>show a sample "
          "while the user is dragging and the full aggregate on "
          "release</b>, which meets the latency budget where recomputation "
          "cannot. <b>Precomputing the aggregations turns an interactive "
          "query into a lookup</b>, and <b>is the only way the latency "
          "budget is met</b> at this scale."]),
  ("callout", "And the honest summary of this module",
   ["<b>At scale you are always showing a summary</b> — binned, "
    "sampled, or aggregated, and frequently all three — <b>so the "
    "question is which summary and whether you said so.</b>",
    "<b>Which is CSCE 676 Module 01 &sect;2's framing "
    "exactly:</b> <b>an approximation with a stated bound is a result, "
    "and an exact answer you cannot compute is not an answer</b> — "
    "and the visualisation case adds that the approximation is visible "
    "and looks exact.",
    "<b>So state the aggregation method, the bin size, the count "
    "scaling, and any sampling</b> — <b>four things</b>, and the "
    "figure is then assessable by somebody who did not make it.",
    "<b>And the risk is specific:</b> <b>a density plot looks "
    "authoritative and is a function of four choices the reader cannot "
    "see</b> — <b>which is the same problem as Module 08's map "
    "and has exactly the same fix</b>, which is to state them."]),
 ],
 "resources": [
   ("The datashader documentation and its principles (free)",
    "https://datashader.org/",
    "<b>&sect;2 as a working system</b> — and its discussion of count "
    "scaling is the best treatment of that specific problem."),
   ("Carr et al. &mdash; Scatterplot matrix techniques for large N "
    "(free)",
    "https://www.jstor.org/stable/2288906",
    "<b>&sect;1 and &sect;2 in the original</b> — where hexagonal "
    "binning was introduced, for exactly this reason."),
   ("Liu, Jiang & Heer &mdash; imMens: Real-time Visual Querying of "
    "Big Data (free)",
    "http://vis.stanford.edu/papers/immens",
    "<b>&sect;4's data cube approach</b> — precomputed aggregation for "
    "interactive latency."),
   ("Lins, Klosowski & Scheidegger &mdash; Nanocubes (free)",
    "https://www.nanocubes.net/",
    "<b>&sect;4's structure</b> — the aggregation index that makes "
    "the interaction a lookup."),
 ],
 "exercises": [
   "<b>Plot ten million points directly</b> and report what you can "
   "read.",
   "<b>Reverse the row order</b> and compare the two figures.",
   "<b>Add transparency</b> and find the alpha at which it saturates.",
   "<b>Hexbin the same data</b> and compare.",
   "<b>Render the density with linear and log count scaling</b>, and "
   "report what appears.",
   "<b>Vary the bin size three ways</b> and check whether a feature "
   "survives.",
   "<b>Find a rounding artefact</b> that appears at one bin size and not "
   "another.",
   "<b>Sample uniformly and check whether a known outlier survives.</b>",
   "<b>Build a stratified sample</b> that keeps the tails, and "
   "compare.",
   "<b>Measure your interaction latency</b> against the 100 ms "
   "threshold.",
 ],
 "selfcheck": [
   "Why does overplotting destroy exactly the information you wanted?",
   "Why is it order-dependent, and what follows?",
   "Why is transparency insufficient?",
   "Give three binning approaches and what each offers.",
   "Why does the count scaling matter so much?",
   "Why is binning an analytical choice, and what should you check?",
   "What does a sample preserve and what does it lose?",
   "What is the fix, and why must sampling be stated?",
   "Name four system constraints and the architectural consequence.",
   "State the module's summary and the four things to report.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Scientific Visualisation",
 "subtitle": "Fields, volumes, and the return to rendering.",
 "question": "How do you see inside a three-dimensional field?",
 "outcomes": [
     "Distinguish scientific from information visualisation.",
     "Explain scalar field techniques and the transfer "
     "function.",
     "Explain volume rendering and its connection to "
     "CSCE 647.",
     "Explain vector and tensor field visualisation.",
     "Choose a technique for a field and a question.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The difference",
   "blurb": "Which is about whether the spatial layout is given."},

  {"t": "callout", "title": "In scientific visualisation the positions are given by the data, so the design question is different",
   "kind": "The distinction that organises this module",
   "body": ["<b>In information visualisation you choose where the "
            "marks go</b> — which is the whole subject of "
            "Modules 01 to 07 — <b>and the position channel is "
            "yours to assign.</b>",
            "<b>In scientific visualisation the positions are given "
            "by the physics</b> — a temperature field, a flow, a "
            "scan — <b>so position is already used and the design "
            "question is what to do with the remaining "
            "channels.</b>",
            "<b>Which means colour, opacity, and geometry carry "
            "everything</b> — and <b>Module 04's colour rules become "
            "the central design decision</b> rather than one among "
            "several.",
            "<b>And the central problem is occlusion:</b> <b>a "
            "three-dimensional field has interior structure, and "
            "anything in front hides what is behind</b> — which is "
            "Part 3's subject and is what volume rendering "
            "exists to solve."]},

  {"t": "section", "label": "Part 2", "title": "Scalar fields",
   "blurb": "One value per point, in two or three dimensions."},

  {"t": "code", "kicker": "Scalar", "title": "The techniques, and what each shows",
   "lang": "text", "code": """
  2D FIELDS
      colour map            the whole field, with
                            Module 04's rules
      contour lines         specific level sets,
                            precisely
      both together         the standard and usually
                            the right answer

  3D FIELDS
      slices                a 2D field at a chosen
                            plane. Simple, exact, and
                            it shows only the plane.
      isosurfaces           the surface where the
                            field equals a chosen
                            value. Shows one level
                            crisply; hides
                            everything else.
      direct volume         accumulate colour and
      rendering             opacity along a ray
                            through the whole volume
                            (Part 3)

  AND THE ISOSURFACE'S THRESHOLD IS THE WHOLE
  PICTURE. Change it and the structure changes, which
  makes it the same kind of undisclosed choice as a
  bin size (Module 11 section 2).
""",
   "caption": "<b>An isosurface's threshold is the whole "
              "picture</b> — which makes it the same kind of "
              "undisclosed analytical choice as a bin size.",
   "note": "The threshold-is-a-choice point connects this module to "
           "the rest."},

  {"t": "callout", "title": "Contours and colour together, because they answer different questions",
   "kind": "Why the standard combination is standard",
   "body": ["<b>A colour map shows the whole field at once and reads "
            "the values imprecisely</b> — rank six "
            "(Module 02 §1) — which suits "
            "seeing the overall structure.",
            "<b>Contour lines show specific levels exactly</b>, "
            "because <b>a labelled contour is a position-encoded "
            "value</b> — and they show nothing between the "
            "levels.",
            "<b>So the combination gives the overall shape and the "
            "precise levels together</b>, which is why topographic maps "
            "have used both for two centuries.",
            "<b>And the contour spacing is a choice</b> — "
            "<b>evenly spaced contours convey the gradient through their "
            "density</b>, which is an elegant free channel and is lost "
            "if the spacing is irregular."]},

  {"t": "section", "label": "Part 3", "title": "Volume rendering",
   "blurb": "Which is CSCE 647's ray marching, applied to data."},

  {"t": "eq", "kicker": "Volume rendering", "title": "The integral, and where you have seen it",
   "eqs": [
     ("C = ∫ c(s) · α(s) · exp(−∫₀ˢ α(t) dt) ds",
      "Accumulate emitted colour along the ray, attenuated by the "
      "opacity in front of it."),
     ("discretised: C ≈ Σᵢ cᵢ αᵢ ∏ⱼ<ᵢ (1 − αⱼ)",
      "Which is front-to-back compositing — exactly the same "
      "recurrence as alpha blending."),
     ("and this is CSCE 647's participating-media integral",
      "The same equation, with a measured scalar field in place of a "
      "physical density."),
   ],
   "caption": "<b>This is CSCE 647's volume rendering equation</b> "
              "— the same ray marching, with measured data in place "
              "of a physical medium.",
   "note": "Making the 647 connection explicit is the point of the "
           "module in this track."},

  {"t": "callout", "title": "And the transfer function is the design, which makes it the hard part",
   "kind": "Why volume rendering is difficult to use well",
   "body": ["<b>The transfer function maps the scalar value to colour "
            "and opacity</b> — and <b>it determines what is visible, "
            "what is transparent, and therefore what the image "
            "shows.</b>",
            "<b>Which means the picture is a function of a choice "
            "nobody can see</b>: <b>two transfer functions on the same "
            "volume produce images with different apparent "
            "structures</b>, both of them renderings of the same "
            "data.",
            "<b>And designing one is genuinely hard</b> — "
            "<b>it is a mapping from a one-dimensional value to four "
            "output channels</b>, with the opacity's effect being "
            "non-local because of the accumulation.",
            "<b>So the honest requirement is to publish the transfer "
            "function alongside the image</b> — which is this "
            "module's version of Module 11 §4's four "
            "statements, and is equally rarely done."]},

  {"t": "section", "label": "Part 4", "title": "Vector and tensor fields",
   "blurb": "Where the data has direction."},

  {"t": "bullets", "kicker": "Vectors", "title": "The techniques, and what each loses",
   "items": [
     "<b>Arrow glyphs</b> — direction and magnitude per "
     "sample point. <b>Simple, and it clutters immediately</b> and "
     "has a sampling artefact: the glyph positions are a "
     "grid you chose.",
     "",
     "<b>Streamlines</b> — curves tangent to the field, "
     "which <b>show the structure far better</b> and <b>lose the "
     "magnitude</b> unless it is encoded on colour or "
     "width.",
     "",
     "<b>Line integral convolution</b> — a texture smeared "
     "along the field, which <b>shows the direction everywhere "
     "densely</b> and is beautiful and is hard to read "
     "quantitatively.",
     "",
     "<b>And seed placement is the design for streamlines</b> "
     "— <b>uniform seeds give uneven coverage</b>, because the "
     "field concentrates them.",
     "",
     "<b>With tensor fields harder still</b>, usually reduced to "
     "glyphs or to derived scalars.",
   ],
   "footnote": "<b>Seed placement is the streamline design</b> — "
               "uniform seeds produce dense bundles and empty regions, "
               "which is a picture of the seeding rather than of the "
               "field."},

  {"t": "callout", "title": "And the connection back to the graphics track",
   "kind": "Closing",
   "body": ["<b>Volume rendering is CSCE 647's ray marching</b>, "
            "isosurface extraction is a geometry problem "
            "CSCE 620's computational geometry addresses, and the "
            "whole pipeline is a rendering pipeline.",
            "<b>Which means this module's techniques are implemented "
            "with the tools of that track</b> — and <b>the "
            "performance work is the same work</b>: acceleration "
            "structures, early ray termination, and GPU "
            "parallelism.",
            "<b>And the difference is entirely in the "
            "objective:</b> <b>CSCE 647 wants the image to be "
            "physically correct, and this module wants it to be "
            "<i>readable</i></b> — which is a different and "
            "sometimes conflicting goal.",
            "<b>So a scientifically useful volume rendering may look "
            "physically wrong on purpose</b> — <b>exaggerated "
            "opacity, non-physical colour, clipped regions</b> — and "
            "that is correct, because the objective is "
            "communication."]},
 ],
 "takeaways": [
   "In scientific visualisation the positions are given by the physics, so "
   "position is already used and colour carries everything.",
   "The central problem is occlusion, which is what volume rendering "
   "exists to solve.",
   "An isosurface's threshold is the whole picture, which makes it the same "
   "kind of undisclosed choice as a bin size.",
   "Evenly spaced contours convey the gradient through their density, which "
   "is a free channel lost by irregular spacing.",
   "The volume rendering integral is CSCE 647's participating-media "
   "equation with measured data in place of a physical medium.",
   "The transfer function determines what the image shows, so it should be "
   "published alongside it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The difference"),
  ("callout", "In scientific visualisation the positions are given by the "
              "data, so the design question is different",
   ["<b>In information visualisation you choose where the marks go</b> "
    "— which is the entire subject of Modules 01 through 07 — "
    "<b>and the position channel, rank one, is yours to assign</b> to "
    "whichever variable most needs it.",
    "<b>In scientific visualisation the positions are given by the "
    "physics</b> — a temperature field on a grid, a flow through a "
    "domain, a medical scan — <b>so position is already used, and "
    "the design question becomes what to do with the remaining "
    "channels.</b>",
    "<b>Which means colour, opacity, and derived geometry carry "
    "everything</b> — and <b>Module 04's colour rules become the "
    "central design decision</b> rather than one consideration among "
    "several, which is why the rainbow scale has done so much damage "
    "specifically in the sciences (Module 04 &sect;2).",
    "<b>And the central problem is occlusion:</b> <b>a "
    "three-dimensional field has interior structure, and anything in "
    "front of it hides what is behind</b> — which is &sect;3's "
    "subject and <b>is exactly what volume rendering exists to "
    "solve</b>."]),

  ("h1", "2 &nbsp; Scalar fields"),
  ("code", """2D FIELDS
    colour map            the whole field at once,
                          with Module 04's rules
    contour lines         specific level sets,
                          precisely
    both together         the standard, and usually
                          the right answer

3D FIELDS
    slices                a 2D field at a chosen
                          plane. Simple, exact, and
                          it shows only that plane.
    isosurfaces           the surface where the field
                          equals a chosen value.
                          Shows one level crisply and
                          hides everything else.
    direct volume         accumulate colour and
    rendering             opacity along a ray through
                          the whole volume
                          (section 3)

AND THE ISOSURFACE'S THRESHOLD IS THE WHOLE PICTURE.
Change it and the apparent structure changes, which
makes it the same kind of undisclosed analytical
choice as a bin size (Module 11 section 2)."""),
  ("p", "<b>An isosurface's threshold is the whole picture</b> — "
        "<b>which makes it the same kind of undisclosed analytical choice "
        "as a bin size</b> (Module 11 &sect;2) or a colour binning "
        "(Module 08 &sect;3). <b>The threshold-is-a-choice point "
        "connects this module to the rest of the course</b>: the "
        "techniques are different and the honesty requirement is "
        "identical, which is to state the parameter and show the figure at "
        "two or three values of it before trusting a feature."),
  ("callout", "Contours and colour together, because they answer different "
              "questions",
   ["<b>A colour map shows the whole field at once and reads the "
    "individual values imprecisely</b> — rank six (Module 02 "
    "&sect;1) — <b>which suits seeing the overall structure</b> and "
    "does not suit reading a value.",
    "<b>Contour lines show specific levels exactly</b>, because <b>a "
    "labelled contour is a position-encoded value</b> — you read it "
    "by finding the line — <b>and they show nothing at all between "
    "the levels.</b>",
    "<b>So the combination gives the overall shape and the precise "
    "levels together</b>, which is <b>why topographic maps have used "
    "both for two centuries</b> and is a good example of a combination "
    "arrived at empirically long before the perceptual argument for it "
    "existed.",
    "<b>And the contour spacing is itself a choice</b> — "
    "<b>evenly spaced contours convey the gradient through their "
    "density</b>: closely spaced lines mean a steep gradient, which the "
    "reader perceives directly. <b>That is an elegant free channel, and "
    "it is lost entirely if the spacing is irregular</b>, so irregular "
    "contour intervals should be a deliberate and stated choice."]),

  ("break",),
  ("h1", "3 &nbsp; Volume rendering"),
  ("eq", "C = &int; c(s) &middot; &alpha;(s) &middot; "
         "exp(&minus;&int;<sub>0</sub><sup>s</sup> &alpha;(t) dt) ds"),
  ("ul", ["<b>Accumulate the emitted colour along the ray, attenuated "
          "by the total opacity in front of it</b> — which is the "
          "emission-absorption model, and is the standard formulation.",
          "<b>Discretised, it becomes front-to-back "
          "compositing:</b> C &approx; &Sigma;<sub>i</sub> "
          "c<sub>i</sub>&alpha;<sub>i</sub> &prod;<sub>j&lt;i</sub> "
          "(1 &minus; &alpha;<sub>j</sub>) — <b>which is exactly the "
          "same recurrence as alpha blending</b>, and is why the "
          "implementation is a familiar one.",
          "<b>And this is CSCE 647's participating-media "
          "integral</b> — <b>the same equation, with a measured "
          "scalar field in place of a physical density</b> and a chosen "
          "transfer function in place of a material's optical "
          "properties.",
          "<b>Making the CSCE 647 connection explicit is the point of "
          "this module within this track</b>: the ray marching, the step "
          "size and its aliasing, the early termination when the "
          "accumulated opacity saturates, and the acceleration structures "
          "are all the same material, applied to a different kind of "
          "input (&sect;4's closing callout)."]),
  ("callout", "And the transfer function is the design, which makes it the "
              "hard part",
   ["<b>The transfer function maps the scalar value at each sample to "
    "a colour and an opacity</b> — and <b>it determines what is "
    "visible, what is transparent, and therefore what the resulting image "
    "shows at all.</b>",
    "<b>Which means the picture is a function of a choice nobody "
    "looking at it can see</b>: <b>two different transfer functions on "
    "the same volume produce images with visibly different apparent "
    "structures</b>, <b>both of them faithful renderings of identical "
    "data.</b>",
    "<b>And designing one is genuinely hard</b> — <b>it is a "
    "mapping from a one-dimensional value to four output "
    "channels</b>, <b>with the opacity's effect being non-local because "
    "of the accumulation</b>: raising the opacity of one value range "
    "hides everything behind it, which is not obvious from the function "
    "itself.",
    "<b>So the honest requirement is to publish the transfer function "
    "alongside the image</b> — <b>which is this module's version of "
    "Module 11 &sect;4's four statements</b>, and <b>is equally "
    "rarely done</b> even in published scientific work where the image is "
    "the evidence."]),

  ("h1", "4 &nbsp; Vector and tensor fields"),
  ("ul", ["<b>Arrow glyphs</b> — direction and magnitude at each "
          "sample point. <b>Simple, immediately understood, and it "
          "clutters at once</b>, <b>and it has a sampling artefact</b>: "
          "<b>the glyph positions are a grid you chose</b>, and the "
          "reader sees the grid as well as the field.",
          "<b>Streamlines</b> — curves everywhere tangent to the "
          "field — which <b>show the structure far better than "
          "glyphs</b> and <b>lose the magnitude entirely</b> unless it is "
          "encoded on colour or on line width.",
          "<b>Line integral convolution</b> — a noise texture "
          "smeared along the field direction — which <b>shows the "
          "direction everywhere and densely</b>, <b>is genuinely "
          "beautiful, and is hard to read quantitatively</b> since there "
          "are no discrete marks to measure.",
          "<b>And seed placement is the design decision for "
          "streamlines</b> — <b>uniform seeds give uneven "
          "coverage</b>, <b>because the field itself concentrates "
          "them</b>: streamlines converge where the flow converges, "
          "leaving bundles and gaps.",
          "<b>With tensor fields harder still</b>, usually reduced "
          "either to glyphs (ellipsoids, superquadrics) or to derived "
          "scalar fields that are then visualised by &sect;2's "
          "methods. <b>Seed placement is the streamline design</b> "
          "— <b>uniform seeds produce dense bundles and empty "
          "regions, which is a picture of the seeding rather than of the "
          "field</b>, and the adaptive placement algorithms exist for "
          "exactly that reason."]),
  ("callout", "And the connection back to the graphics track",
   ["<b>Volume rendering is CSCE 647's ray marching</b>, <b>isosurface "
    "extraction is a geometry problem that CSCE 620's computational "
    "geometry addresses</b> (marching cubes and its successors), <b>and "
    "the whole pipeline is a rendering pipeline</b> with a measured field "
    "as its scene.",
    "<b>Which means this module's techniques are implemented with the "
    "tools of that track</b> — and <b>the performance work is "
    "literally the same work</b>: acceleration structures, empty-space "
    "skipping, early ray termination, and GPU parallelism, all from "
    "CSCE 647 and CSCE 645.",
    "<b>And the difference is entirely in the objective:</b> "
    "<b>CSCE 647 wants the image to be physically correct, and this "
    "module wants it to be <i>readable</i></b> — <b>which is a "
    "different and sometimes directly conflicting goal.</b>",
    "<b>So a scientifically useful volume rendering may look "
    "physically wrong on purpose</b> — <b>exaggerated opacity, "
    "non-physical colour, clipped regions, and discontinuous transfer "
    "functions</b> — <b>and that is correct, because the objective "
    "is communication</b> rather than simulation. Which is a satisfying "
    "place for this track's rendering material to arrive."]),
 ],
 "resources": [
   ("Engel et al. &mdash; Real-Time Volume Graphics",
    "https://www.taylorfrancis.com/books/mono/10.1201/b10629/",
    "<b>&sect;3 in full</b> — the integral, the discretisation, and the "
    "GPU implementation. Library copy."),
   ("Levoy &mdash; Display of Surfaces from Volume Data (free)",
    "https://graphics.stanford.edu/papers/volume-cga88/",
    "<b>&sect;3 in the original</b> — direct volume rendering as it was "
    "introduced, and the transfer function argument is already "
    "there."),
   ("Lorensen & Cline &mdash; Marching Cubes (free)",
    "https://dl.acm.org/doi/10.1145/37401.37422",
    "<b>&sect;2's isosurface extraction</b> — and the connection to "
    "CSCE 620's geometry."),
   ("Cabral & Leedom &mdash; Line Integral Convolution (free)",
    "https://dl.acm.org/doi/10.1145/166117.166151",
    "<b>&sect;4's third technique in the original</b>, with the "
    "construction explained."),
 ],
 "exercises": [
   "<b>State what is different</b> about the design problem when "
   "position is given.",
   "<b>Render a 2D scalar field</b> as colour, as contours, and as "
   "both.",
   "<b>Vary the contour spacing</b> and report what the density "
   "conveys.",
   "<b>Extract an isosurface at three thresholds</b> and compare the "
   "structures.",
   "<b>Implement direct volume rendering by ray marching</b>, reusing "
   "your CSCE 647 code.",
   "<b>Show that the discretised integral is alpha blending.</b>",
   "<b>Design two transfer functions</b> for the same volume that "
   "suggest different structures.",
   "<b>Publish the transfer function</b> alongside one of your "
   "images.",
   "<b>Render a vector field as glyphs, streamlines, and LIC</b>, and "
   "compare what each shows.",
   "<b>Seed streamlines uniformly, then adaptively</b>, and compare the "
   "coverage.",
 ],
 "selfcheck": [
   "What is different about the design problem here?",
   "Why does colour become the central decision?",
   "What is the central problem of 3D fields?",
   "Name three 2D and three 3D scalar techniques.",
   "Why is an isosurface's threshold like a bin size?",
   "Why are contours and colour used together, and what does contour "
   "density convey?",
   "Give the volume rendering integral and its discretisation.",
   "Which CSCE 647 equation is it?",
   "Why is the transfer function the hard part, and what follows?",
   "Name three vector field techniques and what each loses.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming a Visualisation Shows Something",
 "subtitle": "What a figure establishes.",
 "question": "The chart shows a clear trend. Does it?",
 "outcomes": [
     "State what a figure establishes.",
     "Identify the standard overclaims.",
     "Write a caption that makes a figure assessable.",
     "Place this course relative to CSCE 671 and CSCE 632.",
     "State a proportionate practice for making figures.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a figure establishes",
   "blurb": "A reading, by a reader, of an encoding of a derivation."},

  {"t": "callout", "title": "A figure establishes that this encoding of this derivation reads this way to this reader",
   "kind": "The honest reading, in four parts",
   "body": ["<b>The derivation:</b> <b>which data, normalised how, "
            "aggregated to what units, binned how</b> — four choices "
            "before any encoding happens "
            "(Modules 03, 08, 11).",
            "<b>The encoding:</b> <b>which channels, which scales, "
            "which axis conventions</b> — each of which changes what "
            "can be read (Modules 02, 10).",
            "<b>The reading:</b> <b>what somebody who is not you "
            "extracts from it</b> — which is "
            "CSCE 671 §01 §2's designer blindness, "
            "and is the part never tested.",
            "<b>So 'the chart shows a clear trend' is a claim about "
            "all four</b> — <b>and the fourth is the only one you "
            "cannot determine by looking at your own "
            "figure.</b>"]},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["Claim", "Correction"],
   "widths": [4.4, 6.6],
   "rows": [
     ["<b>'The chart shows a clear trend'</b>", "<b>Over which window, with what uncertainty? (M09, M10 §2)</b>"],
     ["<b>'The data speaks for itself'</b>", "<b>It was normalised, binned, and encoded by you (M03 §3)</b>"],
     ["<b>'The map shows a regional pattern'</b>", "<b>Normalised how? A count map is a population map (M08 §3)</b>"],
     ["<b>'The clusters are visible'</b>", "<b>In a t-SNE or force layout? Those are not readable that way (M07 §1)</b>"],
     ["<b>'This visualisation is intuitive'</b>", "<b>Tested with whom? (CSCE 671 §13 §2)</b>"],
     ["<b>'The correlation is obvious'</b>", "<b>From the figure, or from the fitted line you drew on it?</b>"],
   ],
   "footnote": "<b>'The data speaks for itself' is the one to "
               "refuse</b> — every figure is the result of a chain of "
               "choices, and the phrase asserts that none of them "
               "happened.",
   "note": "The data-speaks-for-itself claim is the most common and "
           "the emptiest."},

  {"t": "section", "label": "Part 2", "title": "The caption",
   "blurb": "Which is where a figure becomes assessable."},

  {"t": "code", "kicker": "Caption", "title": "What a caption has to carry",
   "lang": "text", "code": """
  WHAT IS PLOTTED
      the variable, with its units, and the
      normalisation (Module 03 section 3)

  OVER WHAT
      the population, the time window, and the
      spatial or categorical units
      (Modules 08, 10)

  HOW IT WAS DERIVED
      the aggregation, the bin size or bandwidth, any
      smoothing, and any sampling
      (Modules 05, 11)

  THE UNCERTAINTY
      what the intervals or bands represent, and the
      sample size (Module 09)

  AND THE ENCODING, where it is unusual
      the projection for a map, the transfer function
      for a volume, the layout algorithm for a graph

  WHICH IS FIVE CLAUSES, AND MOST CAPTIONS HAVE ONE.
""",
   "caption": "<b>Five clauses, and most captions have one</b> "
              "— which is the gap between a figure a reader can "
              "assess and one they can only believe.",
   "note": "This caption template is the course's most immediately "
           "usable artefact."},

  {"t": "callout", "title": "Because the figure cannot carry those choices and the caption can",
   "kind": "Why this is the right place for them",
   "body": ["<b>None of the five is visible in the figure</b> — a "
            "normalisation, a bin size, a projection, and a sampling all "
            "leave no trace, which is what makes them "
            "dangerous.",
            "<b>And they each change the picture</b>, "
            "demonstrably — this course has shown that for every one "
            "of them.",
            "<b>So the caption is not a label but the figure's "
            "method section</b> — and <b>a figure separated from its "
            "caption is uninterpretable</b>, which matters because "
            "figures circulate alone.",
            "<b>Which argues for putting the critical ones in the "
            "figure itself</b> — the axis label carrying the "
            "normalisation, an annotation naming the window — "
            "<b>because that survives being screenshotted.</b>"]},

  {"t": "section", "label": "Part 3", "title": "The semester",
   "blurb": "Three courses, one correction."},

  {"t": "table", "kicker": "Semester 11", "title": "Where this course sits",
   "header": ["Course", "Its subject", "Its correction"],
   "widths": [2.3, 3.6, 5.6],
   "rows": [
     ["<b>CSCE 671</b>", "<b>Interaction</b>", "<b>You cannot judge your own design; watch somebody</b>"],
     ["<b>CSCE 679</b>", "<b>Visual encoding</b>", "<b>The channel decides what can be read, and it is measured</b>"],
     ["<b>CSCE 632</b>", "<b>Access</b>", "<b>Designing for a constraint improves it for everyone</b>"],
   ],
   "footnote": "<b>All three replace an argument about taste with a "
               "measurement</b> — the channel ranking, the five "
               "participants, and the assistive-technology test are the "
               "same move three times.",
   "note": "The replace-taste-with-measurement framing is the "
           "semester's result."},

  {"t": "section", "label": "Part 4", "title": "A proportionate practice",
   "blurb": "What to actually do."},

  {"t": "bullets", "kicker": "Practice", "title": "In order of return",
   "items": [
     "<b>1 · Put the main variable on position</b> "
     "(Module 02 §1) — <b>which costs nothing and is "
     "the single largest improvement available.</b>",
     "",
     "<b>2 · Sort, and fix the colour scale</b> "
     "(Modules 03 §4, 04) — both cheap, both "
     "high-return.",
     "",
     "<b>3 · Show the uncertainty and the sample "
     "size</b> (Module 09) — which is the honest "
     "one.",
     "",
     "<b>4 · Write the five-clause caption</b> "
     "(Part 2).",
     "",
     "<b>5 · And show it to three people and ask what it "
     "says</b> — before telling them, which is the only test of "
     "the fourth part of Part 1.",
   ],
   "footnote": "<b>Step 5 is the one that is never done</b> — and "
               "it is the only step that addresses the part of the claim "
               "you cannot assess yourself."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can specify an encoding rather than choosing a "
            "chart</b>, and <b>justify it from a measured ranking</b> "
            "— which turns a design argument into a prediction.",
            "<b>You can handle the hard structures</b> — "
            "networks, hierarchies, geography, volumes — <b>and say "
            "what each representation discards.</b>",
            "<b>You can show uncertainty</b>, which <b>most "
            "published figures do not</b>, and you know why they do "
            "not.",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it means the "
            "five-clause caption</b> — because <b>a figure without "
            "its derivation is a picture, and the derivation is where the "
            "claim lives.</b>"]},
 ],
 "takeaways": [
   "A figure establishes that this encoding of this derivation reads this "
   "way to this reader — and the fourth part is the one you cannot "
   "assess yourself.",
   "'The data speaks for itself' is the claim to refuse, because every "
   "figure is the result of a chain of choices.",
   "The caption is the figure's method section, and a figure separated "
   "from its caption is uninterpretable.",
   "Put the critical statements in the figure itself, because that "
   "survives being screenshotted.",
   "All three Semester 11 courses replace an argument about taste with a "
   "measurement.",
   "Showing the figure to three people before telling them what it says is "
   "the step that is never done.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a figure establishes"),
  ("callout", "A figure establishes that this encoding of this derivation "
              "reads this way to this reader",
   ["<b>The derivation:</b> <b>which data was included, normalised "
    "how, aggregated to which units, and binned how</b> — <b>four "
    "choices made before any encoding happens</b> (Modules 03, 08, and "
    "11), each of which changes the picture.",
    "<b>The encoding:</b> <b>which channels carry which variables, "
    "which scales, and which axis conventions</b> — <b>each of which "
    "changes what can be read from the result</b> (Modules 02 and "
    "10).",
    "<b>The reading:</b> <b>what somebody who is not you actually "
    "extracts from the figure</b> — which is <b>CSCE 671 "
    "Module 01 &sect;2's designer blindness</b>, and <b>is the part "
    "that is never tested.</b>",
    "<b>So 'the chart shows a clear trend' is a claim about all "
    "four</b> — <b>and the fourth is the only one you cannot "
    "determine by looking at your own figure</b>, because you already "
    "know what it is supposed to show (&sect;4's step five)."]),
  ("table", ["The claim", "The correction"],
   [["<b>'The chart shows a clear trend.'</b>",
     "<b>Over which window, and with what uncertainty?</b> "
     "(Module 09, Module 10 &sect;2.)"],
    ["<b>'The data speaks for itself.'</b>",
     "<b>It was selected, normalised, binned, and encoded by you</b> "
     "(Module 03 &sect;3) — see the note."],
    ["<b>'The map shows a regional pattern.'</b>",
     "<b>Normalised how?</b> <b>A count map is a population map</b> "
     "(Module 08 &sect;3)."],
    ["<b>'The clusters are clearly visible.'</b>",
     "<b>In a t-SNE plot or a force-directed layout?</b> <b>Neither is "
     "readable that way</b> (Module 07 &sect;1, CSCE 676 "
     "Module 05 &sect;4)."],
    ["<b>'This visualisation is intuitive.'</b>",
     "<b>Tested with whom?</b> Intuition is prior exposure "
     "(CSCE 671 Module 13 &sect;2)."],
    ["<b>'The correlation is obvious from the figure.'</b>",
     "<b>From the figure, or from the fitted line you drew on it?</b> "
     "The line is a model, not data."]],
   [0.34, 0.66]),
  ("p", "<b>'The data speaks for itself' is the one to refuse</b> "
        "— <b>every figure is the result of a chain of choices</b> "
        "(selection, normalisation, aggregation, binning, encoding, "
        "scaling, framing) <b>and the phrase asserts that none of them "
        "happened</b>. <b>It is the most common and the emptiest claim "
        "in this subject</b>, and refusing it is the beginning of being "
        "able to assess a figure at all."),

  ("h1", "2 &nbsp; The caption"),
  ("code", """WHAT IS PLOTTED
    the variable, with its units, and the
    normalisation (Module 03 section 3)

OVER WHAT
    the population, the time window, and the spatial
    or categorical units (Modules 08, 10)

HOW IT WAS DERIVED
    the aggregation, the bin size or bandwidth, any
    smoothing, and any sampling (Modules 05, 11)

THE UNCERTAINTY
    what the intervals or bands represent, and the
    sample size (Module 09)

AND THE ENCODING, where it is unusual
    the projection for a map, the transfer function
    for a volume, the layout algorithm for a graph

WHICH IS FIVE CLAUSES, AND MOST CAPTIONS HAVE ONE."""),
  ("callout", "Because the figure cannot carry those choices and the caption "
              "can",
   ["<b>None of the five is visible in the figure itself</b> — a "
    "normalisation, a bin size, a projection, a smoothing, and a sampling "
    "all leave no visual trace whatsoever, <b>which is exactly what makes "
    "them dangerous</b> rather than merely unstated.",
    "<b>And they each change the picture</b>, demonstrably — "
    "<b>this course has shown that for every single one of them</b>: "
    "Module 03 &sect;3 for normalisation, Module 05 &sect;2 and "
    "Module 11 &sect;2 for binning, Module 08 &sect;1 for "
    "projection, Module 12 &sect;3 for the transfer function.",
    "<b>So the caption is not a label but the figure's method "
    "section</b> — and <b>a figure separated from its caption is "
    "uninterpretable</b>, <b>which matters because figures circulate "
    "alone</b>: screenshotted into a message, pasted into a slide, "
    "reposted without context.",
    "<b>Which argues for putting the critical statements into the "
    "figure itself</b> — <b>the axis label carrying the "
    "normalisation ('cases per 100,000'), an annotation naming the "
    "window, the n beside each group</b> — <b>because that survives "
    "being screenshotted</b> and the caption does not. <b>This caption "
    "template is the course's most immediately usable artefact.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; The semester"),
  ("table", ["Course", "Its subject", "Its central correction"],
   [["<b>CSCE 671</b>", "<b>Interaction.</b>",
     "<b>You cannot judge your own design, so watch somebody</b> (its "
     "Module 01 &sect;2)."],
    ["<b>CSCE 679 (this one)</b>", "<b>Visual encoding.</b>",
     "<b>The channel decides what can be read, and the ranking is "
     "measured</b> (Module 02)."],
    ["<b>CSCE 632</b>", "<b>Access.</b>",
     "<b>Designing for a constraint improves the design for "
     "everybody</b>, which is a quality argument."]],
   [0.22, 0.30, 0.48]),
  ("p", "<b>All three courses replace an argument about taste with a "
        "measurement</b> — <b>the channel ranking, the five "
        "participants, and the assistive-technology test are the same move "
        "three times</b>, applied to the encoding, the interaction, and "
        "the access respectively. <b>The replace-taste-with-measurement "
        "framing is the semester's result</b>, and it is what makes these "
        "three courses engineering rather than criticism."),

  ("h1", "4 &nbsp; A proportionate practice"),
  ("ul", ["<b>1 &middot; Put the main variable on position</b> "
          "(Module 02 &sect;1) — <b>which costs nothing and is "
          "the single largest improvement available to most figures</b>, "
          "and is the decision the ranking most clearly settles.",
          "<b>2 &middot; Sort the categories, and fix the colour "
          "scale</b> (Module 03 &sect;4 and Module 04) — "
          "<b>both cheap, both high-return</b>, and both one line of "
          "code.",
          "<b>3 &middot; Show the uncertainty and the sample size</b> "
          "(Module 09) — <b>which is the honest one</b>, and the "
          "one that makes the figure less persuasive and more "
          "defensible.",
          "<b>4 &middot; Write the five-clause caption</b> "
          "(&sect;2), and <b>put the critical clauses into the figure "
          "itself.</b>",
          "<b>5 &middot; And show it to three people and ask what it "
          "says</b> — <b>before telling them</b> — <b>which is "
          "the only test of the fourth part of &sect;1's claim.</b> "
          "<b>Step 5 is the one that is never done</b>, and <b>it is the "
          "only step that addresses the part of the claim you cannot "
          "assess yourself</b> (CSCE 671 Module 01 &sect;2)."]),
  ("callout", "Where this course leaves you",
   ["<b>You can specify an encoding rather than choosing a chart</b>, "
    "and <b>justify it from a measured ranking</b> — <b>which turns "
    "a design argument into a prediction</b> that can be checked in an "
    "afternoon (Module 02 &sect;4).",
    "<b>You can handle the hard structures</b> — networks, "
    "hierarchies, geography, high dimension, and volumes — <b>and "
    "say what each representation discards</b>, which is the part that "
    "makes the choice defensible.",
    "<b>You can show uncertainty</b>, <b>which most published figures "
    "do not</b>, and <b>you know why they do not</b> "
    "(Module 09 &sect;1) — which makes the omission a decision "
    "rather than a habit.",
    "<b>The closing rule is the program's, unchanged across "
    "thirty-two courses:</b> <b>state what you measured, state what you "
    "assumed, and never claim more than you established.</b> <b>In this "
    "subject it means the five-clause caption</b> — because <b>a "
    "figure without its derivation is a picture, and the derivation is "
    "where the claim actually lives.</b>"]),
 ],
 "resources": [
   ("Munzner, the validation chapter (slides free)",
    "https://www.cs.ubc.ca/~tmm/vadbook/",
    "<b>&sect;1's four levels</b> — and what kind of evidence each "
    "level requires, which is the rigorous version of this module."),
   ("Hullman & Gelman &mdash; Designing for Interactive Exploratory "
    "Data Analysis (free)",
    "https://hdsr.mitpress.mit.edu/pub/zkjz7078",
    "<b>&sect;1's reading problem</b> — and the argument that a figure "
    "encodes a model whether or not you said so."),
   ("Wilke, the telling-a-story chapters (free)",
    "https://clauswilke.com/dataviz/",
    "<b>&sect;2's captions and annotation</b> — with the "
    "put-it-in-the-figure argument made concretely."),
   ("The IEEE VIS evaluation literature (free preprints)",
    "https://ieeevis.org/",
    "<b>&sect;4's step five, done properly</b> — how the field "
    "evaluates figures, and the limitations sections are the model."),
 ],
 "exercises": [
   "<b>Take one of your figures</b> and list the four parts of what it "
   "establishes.",
   "<b>Find a 'the data speaks for itself' claim</b> and enumerate the "
   "choices behind the figure.",
   "<b>Assess five published figures</b> against §1's table.",
   "<b>Write the five-clause caption</b> for three of your own "
   "figures.",
   "<b>Count the clauses</b> in ten published captions.",
   "<b>Move the critical clauses into the figure</b>, and screenshot it "
   "to check they survived.",
   "<b>Name the correction</b> each Semester 11 course makes.",
   "<b>Run §4's five steps</b> on one figure, in order.",
   "<b>Show a figure to three people and ask what it says</b>, before "
   "telling them.",
   "<b>Project 2 is now due.</b> Submit the figure, the uncertainty "
   "representation with its justification, the baseline it beats, the five "
   "readers' open-ended descriptions, the misreadings traced to encoding "
   "decisions, and the not-shown list.",
 ],
 "selfcheck": [
   "Give the four parts of what a figure establishes.",
   "Which part can you not assess yourself, and why?",
   "Give six overclaims and the correction to each.",
   "Why is 'the data speaks for itself' the one to refuse?",
   "Give the five caption clauses.",
   "Why must those choices go in the caption rather than the figure?",
   "Why put the critical ones in the figure anyway?",
   "What correction does each Semester 11 course make?",
   "Give the five-step practice in order.",
   "Which step is never done, and what does it uniquely address?",
 ],
},

]
