# -*- coding: utf-8 -*-
"""CSCE 679 Data Visualization — original course content."""

COURSE = {
    "code": "CSCE 679",
    "title": "Data Visualization",
    "tagline": "The encoding decides what can be read, so the encoding "
               "is the design",
    "term": "Semester 11 (with CSCE 671 and CSCE 632)",
    "prereqs": "CSCE 671 Human-Computer Interaction, especially its "
               "Module 02 on perception; CSCE 676 Data Mining for the "
               "material being visualised; CSCE 647 Advanced Rendering "
               "for Module 12",
    "deliverable": "A visualisation of a dataset you did not choose "
                   "for its convenience — with the encoding "
                   "justified against the perceptual ranking, the "
                   "uncertainty shown, a baseline chart it has to beat, "
                   "and readers tested on what they can actually "
                   "extract from it",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "description": [
        "<b>A visualisation is a mapping from data to visual "
        "properties, and that mapping determines what a reader can "
        "extract.</b> <b>Module 01 establishes that properly</b>, "
        "because it reframes the whole subject: <b>the question is not "
        "'which chart looks good' but 'which channel carries this "
        "variable accurately enough for the judgement the reader has to "
        "make'</b> — which has measured answers.",
        "<b>So the first third is the measurements.</b> <b>Some "
        "visual channels are read accurately and some are not, and the "
        "ranking is empirical</b> (Modules 02 through 04) — "
        "<b>which means a chart choice can be right or wrong rather "
        "than merely tasteful</b>, and that is what makes this an "
        "engineering subject rather than a design one.",
        "<b>The second theme is that the hard cases are the ones "
        "with structure the plane does not have.</b> <b>Networks, "
        "hierarchies, high dimension, and geography all have to be "
        "projected into two dimensions</b> (Modules 07 and 08), and "
        "<b>every projection discards something</b> — so the "
        "question becomes which distortion you are choosing and whether "
        "you said so.",
        "<b>The third is that uncertainty is almost always omitted "
        "and almost always matters.</b> <b>Module 09 is about showing "
        "it</b> — because <b>a point estimate drawn without its "
        "interval invites a conclusion the data does not "
        "support</b>, and this is the commonest honest failure in the "
        "subject (the dishonest ones are Module 10).",
        "<b>And the closing position is about honest claims.</b> "
        "<b>Module 10 covers deliberate deception and the axis "
        "conventions</b>, and <b>Module 13 is about what a "
        "visualisation establishes</b> — because <b>'the chart shows "
        "a clear trend' is a statement about the reader's perception as "
        "much as about the data.</b>",
    ],
    "outcomes": [
        "Explain visualisation as an encoding and state what follows.",
        "Rank the visual channels by accuracy and apply the "
        "ranking.",
        "Match marks and channels to data types.",
        "Use colour correctly and explain why most scales are "
        "wrong.",
        "Choose a chart type from the judgement required.",
        "Design multiple coordinated views and interaction.",
        "Visualise networks and hierarchies, with their trade-offs.",
        "Visualise spatial data and explain projection distortion.",
        "Show uncertainty, and explain why it is usually omitted.",
        "Recognise deceptive charts and state the axis conventions.",
        "Visualise data too large to draw directly.",
        "Explain scientific and volumetric visualisation.",
        "State what a visualisation honestly establishes.",
    ],
    "materials": [
        ("Munzner — Visualization Analysis and Design",
         "https://www.cs.ubc.ca/~tmm/vadbook/",
         "<b>The primary text.</b> The what-why-how framework and the "
         "channel ranking this course uses come from here, and it is "
         "the most rigorous treatment available. Library copy; the "
         "slides are free from the author."),
        ("Ware — Information Visualization: Perception for Design, "
         "4th edition",
         "https://www.elsevier.com/books/information-visualization/ware/978-0-12-812875-6",
         "<b>Modules 02 through 04.</b> The perceptual research "
         "underlying every claim about which channels work, with the "
         "studies cited. Library copy."),
        ("Wilke — Fundamentals of Data Visualization (free online)",
         "https://clauswilke.com/dataviz/",
         "<b>Modules 05, 09, and 10, free in full.</b> Practical, "
         "opinionated, and unusually good on uncertainty and on the "
         "ways a chart misleads."),
        ("Tufte — The Visual Display of Quantitative Information",
         "https://www.edwardtufte.com/tufte/books_vdqi",
         "<b>Module 10's conventions, and the data-ink argument.</b> "
         "Influential, assertive, and worth reading critically — "
         "several of its claims did not survive measurement, which "
         "Module 05 §4 covers. Library copy."),
        ("Healey & Enns — Attention and Visual Memory in "
         "Visualization (free)",
         "https://www.csc2.ncsu.edu/faculty/healey/PP/",
         "<b>Module 02's preattentive material</b>, with interactive "
         "demonstrations that are worth running rather than reading."),
        ("The IEEE VIS proceedings (free preprints)",
         "https://ieeevis.org/",
         "<b>The field's primary literature.</b> Module 13's "
         "exercises use it; the evaluation sections are where the "
         "honest claims are."),
    ],
    "tooling": [
        "<b>D3 or Vega-Lite</b>, and <b>Vega-Lite first</b> — "
        "because <b>its grammar makes the encoding explicit</b>, which "
        "is exactly what Module 01 asks you to think about, and D3's "
        "flexibility hides it.",
        "<b>Python with <code>matplotlib</code> and "
        "<code>altair</code></b>, or R with <code>ggplot2</code> "
        "— <b>a grammar-of-graphics library, so the encoding is a "
        "stated mapping rather than a chart type.</b>",
        "<b>A colour tool that reports perceptual "
        "uniformity</b> — <b>Colorbrewer, or the viridis "
        "family</b> — and <b>Module 04 §2 explains why the default "
        "rainbow scale is a defect.</b>",
        "<b>A colour-vision simulator</b>, used on every figure "
        "before it ships (CSCE 632 §03).",
        "<b>A dataset you did not choose for its "
        "convenience.</b> <b>Project 2 requires one with missing "
        "values, uncertainty, and more dimensions than will "
        "fit</b> — which is what real data is like.",
        "<b>And three people who will tell you what they think your "
        "figure says.</b> <b>Module 13 §1's point is that you cannot "
        "read your own chart naively</b>, which is CSCE 671's argument "
        "in this subject.",
    ],
    "projects": [
        {"title": "One dataset, four encodings", "after": 6,
         "brief": "Encode the same data four ways and measure what each "
                  "lets a reader extract.",
         "reqs": [
             "<b>One dataset and four genuinely different "
             "encodings</b> of the same variables — not four "
             "styles of the same chart.",
             "<b>Each encoding justified against the channel "
             "ranking</b> (Module 02 §2), stating which "
             "variable got which channel and why.",
             "<b>Three specific questions a reader should be able to "
             "answer</b> from the data — a lookup, a comparison, and "
             "a trend.",
             "<b>Five readers tested</b> on those three questions, "
             "per encoding, with accuracy and time recorded.",
             "<b>A colour-vision check</b> and a greyscale check on "
             "all four.",
             "<b>And an account of which encoding won which question, "
             "and why that was predictable</b> from the ranking.",
         ],
         "done": [
             "<b>Four genuinely different encodings</b>, not four "
             "colour schemes — <b>which is graded first</b>, because "
             "the exercise is about channels.",
             "<b>The predictions made before the testing</b>, and the "
             "wrong ones reported (CSCE 671 Project 1's same "
             "requirement).",
             "<b>Accuracy <i>and</i> time</b>, because a slow correct "
             "reading is a different finding from a fast wrong "
             "one.",
             "<b>And the ranking used as a prediction rather than "
             "cited</b> — <b>the point is that it works</b>, and "
             "demonstrating that is the deliverable.",
         ]},
        {"title": "A real dataset, honestly shown", "after": 12,
         "brief": "Visualise something messy, including its "
                  "uncertainty, and test what readers take away.",
         "reqs": [
             "<b>A dataset with missing values, uncertainty, and more "
             "dimensions than fit</b> — and <b>all three handled "
             "explicitly rather than dropped.</b>",
             "<b>The uncertainty shown</b> "
             "(Module 09), not omitted — and the choice of "
             "representation justified.",
             "<b>A baseline:</b> the obvious chart somebody would "
             "have made, which yours has to beat on a stated "
             "question.",
             "<b>Five readers asked what the figure says</b>, in "
             "their own words, before being told.",
             "<b>Every misreading recorded</b>, with the encoding "
             "decision that caused it.",
             "<b>And an honest claim</b> in Module 13 "
             "§2's form, including what the figure does not "
             "show.",
         ],
         "done": [
             "<b>The uncertainty shown and the representation "
             "justified</b> — <b>a figure that omits it fails this "
             "project</b>, whatever else it does.",
             "<b>Readers asked open-endedly before being "
             "prompted</b>, because <b>'does this show X' gets a "
             "yes</b> (CSCE 671 Module 09 §2).",
             "<b>The misreadings traced to encoding decisions</b>, "
             "which is the analytical skill being assessed.",
             "<b>And the not-shown list specific and "
             "non-empty.</b> <b>Every visualisation discards "
             "something</b>, and saying what is the difference between a "
             "figure and an argument.",
         ]},
    ],
    "map": [
        ("Munzner — Visualization Analysis and Design (slides free)",
         "https://www.cs.ubc.ca/~tmm/vadbook/",
         "<b>Modules 01 through 08.</b> The framework, the channel "
         "ranking, and the chart taxonomy, rigorously."),
        ("Wilke — Fundamentals of Data Visualization (free)",
         "https://clauswilke.com/dataviz/",
         "<b>Modules 04, 05, 09, and 10</b>, free in full — and the "
         "uncertainty chapters are the best available."),
        ("Ware — Information Visualization",
         "https://www.elsevier.com/books/information-visualization/ware/978-0-12-812875-6",
         "<b>Modules 02 through 04's evidence.</b> Where the "
         "perceptual claims come from. Library copy."),
        ("The Vega-Lite documentation and gallery (free)",
         "https://vega.github.io/vega-lite/",
         "<b>The grammar made explicit</b> — read the encoding "
         "specifications against Module 01's framing."),
        ("Observable's visualisation notebooks (free)",
         "https://observablehq.com/",
         "<b>Modules 05 through 08 as working examples</b> you can "
         "modify, which is the fastest way to understand an "
         "encoding."),
        ("Scientific Visualization: the volume rendering literature "
         "(free)",
         "https://www.cs.utah.edu/~jmk/",
         "<b>Module 12</b>, and the direct connection back to "
         "CSCE 647's ray marching."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Visualisation as Encoding",
 "subtitle": "The mapping decides what can be read.",
 "question": "What is a chart, mechanically?",
 "outcomes": [
     "Define a visualisation as a data-to-channel mapping.",
     "State the what-why-how framing and use it.",
     "Explain why the encoding determines the readable "
     "questions.",
     "Explain what visualisation is and is not good for.",
     "Specify an encoding rather than choosing a chart type.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The mapping",
   "blurb": "Marks, and the channels that vary them."},

  {"t": "callout", "title": "A visualisation is a set of marks whose visual channels encode data attributes",
   "kind": "The definition, and everything follows from it",
   "body": ["<b>A <i>mark</i> is a geometric primitive</b> — a "
            "point, a line, an area — and <b>a <i>channel</i> is a "
            "visual property that can vary</b>: position, length, "
            "angle, area, colour, shape, texture.",
            "<b>So a scatter plot is: point marks, with x position "
            "encoding one variable and y position encoding "
            "another</b> — and a bar chart is line or area marks with "
            "length encoding the value and position encoding the "
            "category.",
            "<b>Which means 'bar chart' and 'scatter plot' are names "
            "for common mark-and-channel combinations</b>, not "
            "primitives — <b>and thinking in combinations rather than "
            "in named charts is what lets you design one nobody has "
            "named.</b>",
            "<b>And the channel choice is the design decision</b>, "
            "because <b>channels differ enormously in how accurately "
            "they are read</b> (Module 02) — which is measured, and "
            "is what makes this subject empirical."]},

  {"t": "code", "kicker": "Specification", "title": "What a specification looks like",
   "lang": "text", "code": """
  INSTEAD OF "a grouped bar chart", write:

      mark:     bar
      x:        month          (ordered key)
      y:        revenue        (quantitative value)
      colour:   product line   (categorical key)

  WHICH MAKES THE DECISIONS VISIBLE
      why is product line on colour rather than on a
          second axis?
      why is revenue on length rather than on area?
      is month ordered, and does the encoding respect
          the order?

  AND IT MAKES THE ALTERNATIVES ENUMERABLE
      put product line on a small-multiple facet
      put revenue on position rather than length
      put month on a continuous axis as a line

  SO: specify the encoding, then look at the chart it
  produces -- rather than choosing the chart and
  inheriting its encoding.
""",
   "caption": "<b>Specify the encoding and inherit the chart</b> "
              "— rather than choosing the chart and inheriting its "
              "encoding, which is the usual direction.",
   "note": "This inversion is the module's practical contribution."},

  {"t": "section", "label": "Part 2", "title": "What, why, how",
   "blurb": "Three questions, in that order."},

  {"t": "table", "kicker": "Framework", "title": "The framing that keeps the design honest",
   "header": ["Question", "What it asks", "Why it comes first"],
   "widths": [2.3, 4.2, 5.0],
   "rows": [
     ["<b>What</b>", "<b>What is the data? Types, scale, structure</b>", "<b>It constrains which channels are available (M03)</b>"],
     ["<b>Why</b>", "<b>What task is the reader performing?</b>", "<b>It determines which channel must be accurate</b>"],
     ["<b>How</b>", "<b>The marks, channels, and interaction</b>", "<b>It follows from the other two, and nothing else</b>"],
   ],
   "footnote": "<b>'How' is the only one most people start with</b> "
               "— and a chart chosen before the task is known is "
               "optimised for nothing in particular, which is why it "
               "looks fine and reads badly.",
   "note": "The ordering is the whole discipline."},

  {"t": "callout", "title": "The reader's task determines which channel has to be accurate",
   "kind": "Why 'why' is the question people skip",
   "body": ["<b>Looking up one value, comparing two, finding an "
            "extreme, judging a trend, and estimating a total are "
            "different tasks</b> — and <b>an encoding good for one "
            "is frequently poor for another.</b>",
            "<b>A pie chart supports 'is this roughly half' and "
            "fails at 'which of these two is larger'</b>; a bar chart "
            "is the reverse of a stacked area for judging a total "
            "against a component.",
            "<b>So naming the task is what makes an encoding "
            "arguable</b> — <b>'this chart is bad' is a preference "
            "and 'this chart does not support the comparison the reader "
            "needs' is a claim.</b>",
            "<b>And a figure supporting several tasks is a "
            "compromise</b>, which is frequently correct and should be "
            "a decision rather than an accident "
            "(Module 06)."]},

  {"t": "section", "label": "Part 3", "title": "What it is for",
   "blurb": "And where a table or a number is better."},

  {"t": "bullets", "kicker": "Strengths", "title": "What visualisation does that other representations do not",
   "items": [
     "<b>Reveals structure nobody specified</b> — clusters, "
     "outliers, gaps, and shapes that no summary statistic names, "
     "which is the strongest argument for it.",
     "",
     "<b>Supports comparison across many items at once</b>, where "
     "a table requires serial reading "
     "(CSCE 671 §03 §2's memory "
     "limit).",
     "",
     "<b>And uses the visual system's parallelism</b>, which "
     "finds a differing item in constant time "
     "(CSCE 671 §02 §3).",
     "",
     "<b>But a table is better for looking up exact "
     "values</b>, and <b>a single number is better when there is one "
     "number.</b>",
     "",
     "<b>So: a chart for pattern, a table for lookup, and a "
     "sentence for a conclusion</b> — and most reports need all "
     "three.",
   ],
   "footnote": "<b>'A chart for pattern, a table for lookup, a "
               "sentence for a conclusion'</b> — and a figure used "
               "for lookup is a table drawn badly."},

  {"t": "callout", "title": "And the strongest case for visualisation is the structure a statistic hides",
   "kind": "Why this is not merely presentation",
   "body": ["<b>Datasets with identical means, variances, and "
            "correlations can have completely different "
            "shapes</b> — one linear, one curved, one a single "
            "outlier dragging a line — and <b>the summary statistics "
            "cannot distinguish them.</b>",
            "<b>Which is a constructed demonstration and a real "
            "phenomenon</b>: <b>the same thing happens in real data "
            "whenever a relationship is non-linear or a subgroup "
            "behaves differently.</b>",
            "<b>So visualisation is part of the analysis rather than "
            "a presentation of it</b> — which is "
            "CSCE 676 §01's two-problem framing, with "
            "the picture as a tool for the second.",
            "<b>And it is why 'look at the data first' is "
            "methodological advice</b> rather than aesthetic — "
            "<b>a model fitted without looking is fitted to something "
            "you did not inspect.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Reading this course",
   "blurb": "The structure, and the one module to internalise."},

  {"t": "bullets", "kicker": "Orientation", "title": "How the course is organised",
   "items": [
     "<b>Modules 02 to 05 are the measurements</b> — the "
     "channel ranking, data types, colour, and the chart types that "
     "follow from them.",
     "",
     "<b>Modules 06 to 08 are the hard structures</b> — "
     "multiple views and interaction, networks and hierarchies, and "
     "geography.",
     "",
     "<b>Module 09 is uncertainty</b>, which is the most often "
     "omitted and most often decisive.",
     "",
     "<b>Modules 10 to 12 are deception, scale, and scientific "
     "visualisation</b> — including the direct link back to "
     "CSCE 647's rendering.",
     "",
     "<b>And Module 02 is the one to internalise</b>, because "
     "<b>the channel ranking turns chart choice from taste into "
     "prediction.</b>",
   ],
   "footnote": "<b>If you take one thing from this course, take the "
               "channel ranking</b> — it is short, it is empirical, "
               "and it decides most design questions before they are "
               "arguments."},
 ],
 "takeaways": [
   "A visualisation is marks whose visual channels encode data attributes, "
   "and 'bar chart' is a name for a common combination.",
   "Specify the encoding and inherit the chart, rather than choosing the "
   "chart and inheriting its encoding.",
   "'How' is the only question most people start with, and a chart chosen "
   "before the task is optimised for nothing.",
   "Naming the reader's task is what makes an encoding arguable rather "
   "than a preference.",
   "A chart for pattern, a table for lookup, and a sentence for a "
   "conclusion — and a figure used for lookup is a table drawn badly.",
   "Datasets with identical summary statistics can have completely "
   "different shapes, which makes visualisation part of the analysis.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The mapping"),
  ("callout", "A visualisation is a set of marks whose visual channels "
              "encode data attributes",
   ["<b>A <i>mark</i> is a geometric primitive</b> — a point, a "
    "line, an area, a volume — and <b>a <i>channel</i> is a visual "
    "property of that mark which can be varied</b>: position, length, "
    "angle, slope, area, colour hue, colour luminance, shape, texture, "
    "or motion.",
    "<b>So a scatter plot is: point marks, with horizontal position "
    "encoding one variable and vertical position encoding "
    "another</b> — and <b>a bar chart is line or area marks with "
    "length encoding the value and position encoding the "
    "category.</b> Both are mappings, described completely by their "
    "mark and their channel assignments.",
    "<b>Which means 'bar chart' and 'scatter plot' are names for "
    "common mark-and-channel combinations rather than primitives</b> "
    "— and <b>thinking in combinations rather than in named charts "
    "is what lets you design a figure nobody has named</b>, which is "
    "frequently what unusual data requires.",
    "<b>And the channel choice is the design decision</b>, because "
    "<b>channels differ enormously in how accurately they are read</b> "
    "(Module 02) — <b>which is measured rather than asserted, and "
    "is what makes this subject empirical</b> rather than a matter of "
    "style."]),
  ("code", """INSTEAD OF "a grouped bar chart", write:

    mark:     bar
    x:        month          (ordered key)
    y:        revenue        (quantitative value)
    colour:   product line   (categorical key)

WHICH MAKES THE DECISIONS VISIBLE
    why is product line on colour rather than on a
        second axis?
    why is revenue on length rather than on area?
    is month ordered, and does the encoding respect
        that order?

AND IT MAKES THE ALTERNATIVES ENUMERABLE
    put product line on a small-multiple facet
    put revenue on position rather than on length
    put month on a continuous axis as a line

SO: specify the encoding, then look at the chart it
produces -- rather than choosing the chart and
inheriting its encoding."""),
  ("p", "<b>Specify the encoding and inherit the chart</b> — "
        "<b>rather than choosing the chart and inheriting its encoding, "
        "which is the usual direction</b> and which hides every decision "
        "inside a chart-type name. <b>This inversion is the module's "
        "practical contribution</b>, and it is why the course recommends a "
        "grammar-of-graphics library: the grammar forces the "
        "specification, where a chart-type API supplies it silently."),

  ("h1", "2 &nbsp; What, why, how"),
  ("table", ["Question", "What it asks", "Why it comes first"],
   [["<b>What</b>",
     "<b>What is the data?</b> Attribute types, cardinality, and "
     "structure.",
     "<b>It constrains which channels are even available</b> "
     "(Module 03) — an unordered category cannot go on a "
     "quantitative channel."],
    ["<b>Why</b>", "<b>What task is the reader performing?</b>",
     "<b>It determines which channel has to be accurate</b> — see "
     "the callout."],
    ["<b>How</b>",
     "<b>The marks, the channels, and the interaction.</b>",
     "<b>It follows from the other two, and from nothing else.</b>"]],
   [0.18, 0.34, 0.48]),
  ("p", "<b>'How' is the only one most people start with</b> — the "
        "question 'what chart should I make' is a 'how' question asked "
        "first — and <b>a chart chosen before the reader's task is "
        "known is optimised for nothing in particular</b>, <b>which is "
        "exactly why it looks fine and reads badly</b>. <b>The ordering "
        "is the whole discipline</b> of this framework, and it costs "
        "nothing but the habit."),
  ("callout", "The reader's task determines which channel has to be accurate",
   ["<b>Looking up one value, comparing two values, finding the "
    "extreme, judging a trend, estimating a total, and judging a "
    "proportion are all different tasks</b> — and <b>an encoding "
    "that is good for one is frequently poor for another.</b>",
    "<b>A pie chart supports 'is this roughly half' and fails badly "
    "at 'which of these two similar slices is larger'</b>; <b>and a "
    "stacked area chart supports judging the total while making the "
    "individual components hard to compare</b>, where a grouped bar "
    "chart does the reverse. Neither is wrong; they answer different "
    "questions.",
    "<b>So naming the task is what makes an encoding arguable</b> "
    "— <b>'this chart is bad' is a preference, and 'this chart does "
    "not support the comparison the reader needs' is a claim</b> that can "
    "be tested (Module 13 &sect;1).",
    "<b>And a figure supporting several tasks at once is a "
    "compromise</b>, <b>which is frequently correct and should be a "
    "decision rather than an accident</b> — or should be resolved by "
    "showing several linked views (Module 06) rather than by "
    "overloading one."]),

  ("break",),
  ("h1", "3 &nbsp; What visualisation is for"),
  ("ul", ["<b>It reveals structure nobody specified</b> — "
          "clusters, outliers, gaps, discontinuities, and shapes that no "
          "summary statistic names — <b>which is the strongest "
          "argument for it</b> and is the callout below.",
          "<b>It supports comparison across many items "
          "simultaneously</b>, where a table requires serial reading and "
          "therefore holding values in working memory "
          "(CSCE 671 Module 03 &sect;2's four-chunk limit).",
          "<b>And it uses the visual system's parallelism</b>, which "
          "locates an item differing in one channel in approximately "
          "constant time regardless of how many others there are "
          "(CSCE 671 Module 02 &sect;3's preattentive features).",
          "<b>But a table is better for looking up exact "
          "values</b> — reading a number off an axis is slow and "
          "approximate — and <b>a single number is better when there "
          "is genuinely one number</b>, which is more often than the "
          "number of charts produced would suggest.",
          "<b>So: a chart for pattern, a table for lookup, and a "
          "sentence for a conclusion</b> — and <b>most reports need "
          "all three</b> rather than one of them repeated. <b>A figure "
          "used for lookup is a table drawn badly</b>, and is a common "
          "and avoidable mistake."]),
  ("callout", "And the strongest case for visualisation is the structure a "
              "statistic hides",
   ["<b>Datasets with identical means, variances, and correlation "
    "coefficients can have completely different shapes</b> — one "
    "linear, one strongly curved, one a tight cluster with a single "
    "outlier dragging the fitted line — and <b>the summary "
    "statistics cannot distinguish between them at all.</b>",
    "<b>Which is a constructed demonstration (Anscombe's quartet, and "
    "its modern elaborations) and also a real phenomenon</b>: <b>the same "
    "thing happens in real data whenever a relationship is non-linear or "
    "a subgroup behaves differently from the aggregate</b> "
    "(CSCE 638 Module 12 &sect;1's disaggregation argument, "
    "arriving visually).",
    "<b>So visualisation is part of the analysis rather than a "
    "presentation of it</b> — which is <b>CSCE 676 Module 01's "
    "two-problem framing with the picture serving as a tool for the "
    "second problem</b>: deciding whether what you found is real.",
    "<b>And it is why 'look at the data first' is methodological "
    "advice rather than aesthetic</b> — <b>a model fitted without "
    "looking is fitted to something you did not inspect</b>, and the "
    "inspection is cheap."]),

  ("h1", "4 &nbsp; Reading this course"),
  ("ul", ["<b>Modules 02 to 05 are the measurements</b> — the "
          "channel accuracy ranking, the data types and what channels "
          "suit them, colour, and the chart types that follow from all "
          "three.",
          "<b>Modules 06 to 08 are the hard structures</b> — "
          "multiple coordinated views and interaction, networks and "
          "hierarchies, and geographic data — all of which have "
          "structure the plane does not naturally hold.",
          "<b>Module 09 is uncertainty</b>, which is <b>the most "
          "often omitted and most often decisive</b> element of a figure, "
          "and which has its own module for that reason.",
          "<b>Modules 10 to 12 are deception, scale, and scientific "
          "visualisation</b> — the last of which <b>connects directly "
          "back to CSCE 647's volume rendering and ray marching</b>, "
          "which is a pleasant closing of a loop in this track.",
          "<b>And Module 02 is the one to internalise</b>, because "
          "<b>the channel ranking turns chart choice from taste into "
          "prediction.</b> <b>If you take one thing from this course, "
          "take the channel ranking</b> — it is short, it is "
          "empirical, and <b>it decides most design questions before they "
          "become arguments.</b>"]),
 ],
 "resources": [
   ("Munzner &mdash; Visualization Analysis and Design, chapters 1 "
    "through 3 (slides free)",
    "https://www.cs.ubc.ca/~tmm/vadbook/",
    "<b>&sect;1 and &sect;2</b> — the what-why-how framework and the "
    "mark-and-channel vocabulary, from the source."),
   ("Wilke &mdash; Fundamentals of Data Visualization, chapter 1 "
    "(free)",
    "https://clauswilke.com/dataviz/",
    "<b>&sect;1's mapping framing</b>, with the aesthetics-as-channels "
    "vocabulary used throughout the book."),
   ("Anscombe &mdash; Graphs in Statistical Analysis (free)",
    "https://www.jstor.org/stable/2682899",
    "<b>&sect;3's callout in the original</b> — two pages, and it "
    "makes the argument once and permanently."),
   ("Matejka & Fitzmaurice &mdash; Same Stats, Different Graphs "
    "(free)",
    "https://www.autodeskresearch.com/publications/samestats",
    "<b>&sect;3 extended</b> — arbitrary shapes with identical "
    "statistics, generated, which is more striking than the "
    "original."),
 ],
 "exercises": [
   "<b>Write the encoding specification</b> for five charts you did not "
   "make.",
   "<b>Enumerate three alternative encodings</b> for one of them.",
   "<b>Take a chart you made</b> and write down the reader's task it "
   "was for.",
   "<b>Find a chart</b> where the task and the encoding do not "
   "match.",
   "<b>Find a figure used for lookup</b> and replace it with a "
   "table.",
   "<b>Find a chart that should have been one number.</b>",
   "<b>Construct two datasets</b> with the same mean and correlation and "
   "different shapes.",
   "<b>Plot both</b> and confirm the statistics do not distinguish "
   "them.",
   "<b>Fit a linear model to each</b> and report what you would have "
   "concluded without looking.",
   "<b>Write the three-question list</b> (lookup, comparison, trend) for "
   "Project 1's dataset.",
 ],
 "selfcheck": [
   "Define a mark and a channel, and give the encoding of a scatter "
   "plot.",
   "Why is 'bar chart' not a primitive?",
   "What does specifying the encoding make visible?",
   "Give the three framework questions and why the order matters.",
   "Why does the reader's task determine the encoding?",
   "Contrast what a pie chart and a bar chart support.",
   "What does visualisation do that a table does not, and vice "
   "versa?",
   "State the one-sentence division of labour.",
   "Why can identical statistics have different shapes, and what "
   "follows?",
   "Which module is the one to internalise, and why?",
 ],
},

]

for _b in ("c679_b2", "c679_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
