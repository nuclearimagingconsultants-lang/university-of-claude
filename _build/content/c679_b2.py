# -*- coding: utf-8 -*-
"""CSCE 679 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "The Channel Ranking",
 "subtitle": "Measured accuracy, which decides most design questions.",
 "question": "Which visual channels are read accurately?",
 "outcomes": [
     "State the ranking for quantitative and categorical data.",
     "Explain why position dominates.",
     "Explain separability and the channels that interfere.",
     "Explain popout and its single-dimension limit.",
     "Use the ranking as a prediction.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The ranking",
   "blurb": "Empirical, and short enough to memorise."},

  {"t": "table", "kicker": "Quantitative", "title": "The ranking for quantitative data, most accurate first",
   "header": ["Rank", "Channel", "Note"],
   "widths": [1.7, 3.6, 5.7],
   "rows": [
     ["<b>1</b>", "<b>Position on a common scale</b>", "<b>By a wide margin. Use it for your most important variable</b>"],
     ["<b>2</b>", "<b>Position on unaligned scales</b>", "<b>Still good; the comparison is harder across panels</b>"],
     ["<b>3</b>", "<b>Length</b>", "<b>Which is why bars work, and why they must start at zero</b>"],
     ["<b>4</b>", "<b>Angle and slope</b>", "<b>Slope judgement depends on the aspect ratio (M05 §4)</b>"],
     ["<b>5</b>", "<b>Area</b>", "<b>Systematically underestimated; doubling looks like 1.5×</b>"],
     ["<b>6</b>", "<b>Luminance and colour saturation</b>", "<b>Ordered but imprecise; fine for a few levels</b>"],
     ["<b>7</b>", "<b>Colour hue</b>", "<b>Not ordered at all — do not use it for quantity (M04)</b>"],
   ],
   "footnote": "<b>This table decides most chart questions before they "
               "become arguments</b> — and it is the single most "
               "useful artefact in the course, which is why "
               "Module 01 §4 said to memorise it.",
   "note": "Have students reproduce this from memory; it is that "
           "load-bearing."},

  {"t": "callout", "title": "Position dominates because it is judged against a shared reference",
   "kind": "Why the ranking has this shape",
   "body": ["<b>A position on a common axis can be compared against "
            "a gridline, against the axis itself, and against every "
            "other mark</b> — so the judgement is relative and "
            "supported.",
            "<b>Length is next because it also has a zero "
            "reference</b> — <b>which is exactly why a truncated bar "
            "axis is a deception rather than a stylistic "
            "choice</b> (Module 10 §2): it removes the "
            "reference the channel depends on.",
            "<b>And area is poor because there is no reference and "
            "the perceptual exponent is below one</b> — <b>people "
            "systematically underestimate area ratios</b>, so a bubble "
            "twice the value looks about one and a half times as "
            "big.",
            "<b>Which means the ranking is not arbitrary:</b> "
            "<b>channels with a shared reference beat channels "
            "without one</b>, and that explains the order rather than "
            "merely stating it."]},

  {"t": "section", "label": "Part 2", "title": "Categorical channels",
   "blurb": "A different ranking, and a capacity limit."},

  {"t": "bullets", "kicker": "Categorical", "title": "The ranking for categories, and how many each holds",
   "items": [
     "<b>Spatial region first</b> — small multiples, or "
     "separate panels. <b>Effectively unlimited, and the most "
     "accurate.</b>",
     "",
     "<b>Then colour hue</b> — <b>which holds about five to "
     "seven categories before the reader has to consult the "
     "legend</b> (CSCE 671 §03 §2).",
     "",
     "<b>Then motion</b>, which is extremely salient and holds "
     "very few — and is intrusive.",
     "",
     "<b>Then shape</b>, which holds a moderate number and is "
     "poor at small sizes.",
     "",
     "<b>And note the inversion:</b> <b>hue is second for "
     "categories and last for quantity</b>, which is the clearest "
     "demonstration that the channel ranking depends on the data "
     "type (Module 03).",
   ],
   "footnote": "<b>Hue is second for categories and last for "
               "quantity</b> — which is why 'is colour good' is not a "
               "question with an answer until the data type is "
               "named."},

  {"t": "section", "label": "Part 3", "title": "Separability",
   "blurb": "Channels that interfere with each other."},

  {"t": "callout", "title": "Some channel pairs are read independently and some interfere",
   "kind": "The property that limits how many variables fit",
   "body": ["<b>Position and colour hue are fully separable</b> "
            "— a reader can judge one without the other affecting "
            "it, which is why a coloured scatter plot works.",
            "<b>But size and colour interfere:</b> <b>a small patch "
            "of colour is harder to identify, so encoding one variable "
            "on size and another on hue degrades both.</b>",
            "<b>And width and height are not separable at "
            "all</b> — <b>the reader perceives the resulting area and "
            "aspect ratio rather than two independent "
            "values</b>, which makes a two-variable rectangle "
            "encoding read as one.",
            "<b>So the number of variables you can encode is bounded "
            "by separability rather than by the number of "
            "channels</b> — which is the argument for small multiples "
            "and linked views (Module 06) over one dense figure."]},

  {"t": "bullets", "kicker": "Practice", "title": "What follows for multivariate figures",
   "items": [
     "<b>Three or four encoded variables is a practical "
     "limit</b> for one set of marks — and <b>beyond that, use "
     "faceting rather than more channels.</b>",
     "",
     "<b>Put the most important variable on position</b>, "
     "always — which is the single decision the ranking most "
     "clearly settles.",
     "",
     "<b>Avoid size-plus-hue</b> on the same marks, and "
     "<b>never encode two variables on the two dimensions of a "
     "rectangle.</b>",
     "",
     "<b>And check for unintended encoding</b> — <b>if marks "
     "differ in a channel for an incidental reason, readers will "
     "attribute meaning to it.</b>",
     "",
     "<b>Which is CSCE 671 §02 §1's spacing-wins "
     "result</b>: the visual system groups and orders whether you "
     "intended it or not.",
   ],
   "footnote": "<b>Readers attribute meaning to any channel that "
               "varies</b> — so an incidental difference in size or "
               "colour is a claim you did not mean to "
               "make."},

  {"t": "section", "label": "Part 4", "title": "Using it as a prediction",
   "blurb": "Which is what makes it worth knowing."},

  {"t": "callout", "title": "The ranking predicts which questions a figure will answer well",
   "kind": "The point of the module",
   "body": ["<b>Before showing anybody a figure, you can predict "
            "which comparisons will be read accurately</b> — the "
            "ones on position, then length — <b>and which will be "
            "guessed</b>, the ones on area or hue.",
            "<b>So a design review becomes:</b> <b>'the reader's main "
            "task is comparing these two values, and they are encoded on "
            "area, which is rank five'</b> — which is a statement "
            "about accuracy rather than taste.",
            "<b>And it is testable:</b> <b>ask five readers the "
            "comparison and measure their accuracy</b>, which is "
            "Project 1 and which reliably confirms the "
            "ranking.",
            "<b>Which is why this module is the one to "
            "internalise</b> — <b>it converts an aesthetic argument "
            "into a prediction that can be checked in an "
            "afternoon.</b>"]},

  {"t": "code", "kicker": "Review", "title": "A design review in four questions",
   "lang": "text", "code": """
  1. WHAT IS THE READER'S MAIN TASK?
     a lookup, a comparison, a trend, a total, or a
     search for an extreme (Module 01 section 2)

  2. WHICH VARIABLE DOES THAT TASK CONCERN?

  3. WHICH CHANNEL IS IT ENCODED ON, AND WHAT RANK IS
     THAT?

  4. IF IT IS NOT NEAR THE TOP, WHY NOT?
     there are legitimate reasons -- the position
     channels are already used, the figure serves
     several tasks, the data has more dimensions than
     channels -- and the answer should be one of them
     rather than "it looked better".

  THAT IS THE WHOLE REVIEW. It takes two minutes and
  it catches the large errors, which are nearly always
  a channel mismatch rather than a styling problem.
""",
   "caption": "<b>Two minutes, and it catches the large errors</b> "
              "— which are nearly always a channel mismatch rather "
              "than a styling problem.",
   "note": "This four-question review is the course's most portable "
           "tool."},
 ],
 "takeaways": [
   "Position on a common scale dominates by a wide margin, so the most "
   "important variable goes there.",
   "Channels with a shared reference beat channels without one, which "
   "explains the ranking's shape rather than merely stating it.",
   "Area is systematically underestimated, so doubling the value looks "
   "like about one and a half times.",
   "Hue is second for categories and last for quantity, so 'is colour "
   "good' has no answer until the data type is named.",
   "Width and height are not separable, so a two-variable rectangle reads "
   "as one.",
   "Readers attribute meaning to any channel that varies, so an incidental "
   "difference is a claim you did not mean to make.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The ranking for quantitative data"),
  ("table", ["Rank", "Channel", "Note"],
   [["<b>1</b>", "<b>Position on a common scale</b>",
     "<b>By a wide margin.</b> Put your most important quantitative "
     "variable here (&sect;4)."],
    ["<b>2</b>", "<b>Position on unaligned scales</b>",
     "<b>Still good</b>; the comparison across separate panels is harder "
     "than within one (Module 06 &sect;1)."],
    ["<b>3</b>", "<b>Length</b>",
     "<b>Which is why bars work</b>, and <b>why their axis must start at "
     "zero</b> — see the callout."],
    ["<b>4</b>", "<b>Angle and slope</b>",
     "<b>Slope judgement depends on the aspect ratio</b>, which is a "
     "design parameter (Module 05 &sect;4)."],
    ["<b>5</b>", "<b>Area</b>",
     "<b>Systematically underestimated</b> — doubling the value looks "
     "like roughly 1.5 times."],
    ["<b>6</b>", "<b>Luminance and colour saturation</b>",
     "<b>Ordered but imprecise</b>; acceptable for a few distinguishable "
     "levels (Module 04 &sect;3)."],
    ["<b>7</b>", "<b>Colour hue</b>",
     "<b>Not ordered at all</b> — do not use it for quantity "
     "(Module 04 &sect;2)."]],
   [0.10, 0.32, 0.58]),
  ("p", "<b>This table decides most chart questions before they become "
        "arguments</b> — and it is <b>the single most useful artefact "
        "in the course</b>, which is why Module 01 &sect;4 recommended "
        "memorising it. <b>Reproducing it from memory is worth doing</b>, "
        "because it is that load-bearing: &sect;4's review, "
        "Module 04's colour rules, and Module 05's chart choices all "
        "reduce to it."),
  ("callout", "Position dominates because it is judged against a shared "
              "reference",
   ["<b>A position on a common axis can be compared against a "
    "gridline, against the axis itself, and against every other mark in "
    "the figure</b> — so the judgement is relative and supported by "
    "multiple references rather than absolute.",
    "<b>Length comes next because it also has a zero "
    "reference</b> — the bar's base — and <b>that is exactly why "
    "a truncated bar axis is a deception rather than a stylistic "
    "choice</b> (Module 10 &sect;2): <b>it removes the reference the "
    "channel depends on</b>, so the length no longer means what the "
    "reader's visual system assumes.",
    "<b>And area is poor because there is no reference and the "
    "perceptual exponent is below one</b> — <b>people systematically "
    "underestimate area ratios</b>, so <b>a bubble representing twice "
    "the value looks about one and a half times as large</b>, and the "
    "error is consistent rather than random.",
    "<b>Which means the ranking is not arbitrary:</b> <b>channels "
    "with a shared reference beat channels without one</b>, and <b>that "
    "explains the order rather than merely stating it</b> — which "
    "makes it possible to reason about a channel the table does not "
    "list."]),

  ("h1", "2 &nbsp; Categorical channels"),
  ("ul", ["<b>Spatial region first</b> — small multiples, or "
          "separate panels, or distinct areas of one figure. "
          "<b>Effectively unlimited in the number of categories it "
          "holds, and the most accurately read</b>, which is why faceting "
          "is such a strong technique (Module 06 &sect;1).",
          "<b>Then colour hue</b> — <b>which holds about five to "
          "seven categories before the reader has to consult the legend "
          "for each mark</b> (CSCE 671 Module 03 &sect;2's working "
          "memory limit), after which it has stopped being a channel and "
          "become a lookup.",
          "<b>Then motion</b>, which is <b>extremely salient and holds "
          "very few categories</b> — and is intrusive enough that it "
          "should be reserved (CSCE 671 Module 02 &sect;3).",
          "<b>Then shape</b>, which holds a moderate number and is "
          "<b>poor at small mark sizes</b>, where the shapes become "
          "indistinguishable — so it interacts with size "
          "(&sect;3).",
          "<b>And note the inversion:</b> <b>hue is second for "
          "categories and last for quantity</b>, <b>which is the clearest "
          "demonstration that the channel ranking depends on the data "
          "type</b> (Module 03) — and is why <b>'is colour good' "
          "is not a question with an answer until the data type is "
          "named.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Separability"),
  ("callout", "Some channel pairs are read independently and some interfere",
   ["<b>Position and colour hue are fully separable</b> — a reader "
    "can judge a mark's position without its colour affecting the "
    "judgement, and vice versa — <b>which is why a colour-coded "
    "scatter plot works well</b> and is such a common and effective "
    "encoding.",
    "<b>But size and colour interfere:</b> <b>a small patch of colour "
    "is genuinely harder to identify than a large one</b>, so <b>encoding "
    "one variable on size and another on hue degrades the reading of "
    "both</b> — and the degradation is worst exactly for the small "
    "marks, which biases the reading.",
    "<b>And width and height are not separable at all</b> — "
    "<b>the reader perceives the resulting area and aspect ratio rather "
    "than two independent values</b>, <b>which makes a two-variable "
    "rectangle encoding read as one variable plus a distraction.</b>",
    "<b>So the number of variables you can usefully encode is bounded "
    "by separability rather than by the number of channels "
    "available</b> — which is <b>the argument for small multiples "
    "and linked views</b> (Module 06) <b>over one dense figure</b>, "
    "and it is a perceptual argument rather than an aesthetic one."]),
  ("ul", ["<b>Three or four encoded variables is a practical "
          "limit</b> for a single set of marks — and <b>beyond that, "
          "use faceting rather than adding more channels</b> (&sect;2's "
          "first row, which is both accurate and unlimited).",
          "<b>Put the most important variable on position, "
          "always</b> — <b>which is the single decision the ranking "
          "most clearly settles</b> and the one most often got wrong by "
          "putting a decorative variable there instead.",
          "<b>Avoid size-plus-hue on the same marks</b>, and "
          "<b>never encode two variables on the two dimensions of a "
          "rectangle</b> — both of which follow directly from the "
          "callout.",
          "<b>And check for unintended encoding</b> — <b>if your "
          "marks differ in a channel for an incidental reason (a default "
          "colour cycle, a size that varies with the label length), "
          "readers will attribute meaning to it.</b>",
          "<b>Which is CSCE 671 Module 02 &sect;1's spacing-wins "
          "result in another form</b>: <b>the visual system groups and "
          "orders whether you intended it to or not.</b> <b>Readers "
          "attribute meaning to any channel that varies</b>, <b>so an "
          "incidental difference in size or colour is a claim you did not "
          "mean to make</b> — and is worth auditing before a figure "
          "ships."]),

  ("h1", "4 &nbsp; Using the ranking as a prediction"),
  ("callout", "The ranking predicts which questions a figure will answer "
              "well",
   ["<b>Before showing a figure to anybody, you can predict which "
    "comparisons will be read accurately</b> — the ones encoded on "
    "position, then on length — <b>and which will be guessed at</b>, "
    "the ones on area, luminance, or hue.",
    "<b>So a design review becomes a specific claim:</b> <b>'the "
    "reader's main task is comparing these two values, and they are "
    "encoded on area, which is rank five'</b> — <b>which is a "
    "statement about reading accuracy rather than about taste</b>, and is "
    "therefore arguable on evidence.",
    "<b>And it is directly testable:</b> <b>ask five readers to make "
    "the comparison and measure their accuracy and their time</b>, which "
    "is <b>Project 1</b> and which <b>reliably confirms the "
    "ranking</b> — the effect sizes are large enough to see with "
    "five people.",
    "<b>Which is why this module is the one to internalise</b> — "
    "<b>it converts an aesthetic argument into a prediction that can be "
    "checked in an afternoon</b>, and that conversion is what makes the "
    "rest of the course empirical rather than stylistic."]),
  ("code", """1. WHAT IS THE READER'S MAIN TASK?
   a lookup, a comparison, a trend, a total, or a
   search for an extreme (Module 01 section 2)

2. WHICH VARIABLE DOES THAT TASK CONCERN?

3. WHICH CHANNEL IS IT ENCODED ON, AND WHAT RANK IS
   THAT?

4. IF IT IS NOT NEAR THE TOP, WHY NOT?
   there are legitimate reasons -- the position
   channels are already in use, the figure has to
   serve several tasks at once, the data has more
   dimensions than there are good channels -- and the
   answer should be one of them rather than "it
   looked better".

THAT IS THE WHOLE REVIEW. It takes two minutes and it
catches the large errors, which are nearly always a
channel mismatch rather than a styling problem."""),
  ("p", "<b>Two minutes, and it catches the large errors</b> — "
        "<b>which are nearly always a channel mismatch rather than a "
        "styling problem</b>, and which no amount of attention to "
        "typography or colour palette will fix. <b>This four-question "
        "review is the course's most portable tool</b>: it requires only "
        "&sect;1's table, it applies to any figure, and it produces a "
        "specific objection rather than a general dissatisfaction."),
 ],
 "resources": [
   ("Cleveland & McGill &mdash; Graphical Perception (free)",
    "https://www.jstor.org/stable/2288400",
    "<b>&sect;1's ranking in the original</b> — the experiments that "
    "established it, and still the reference."),
   ("Munzner, chapter 5 (slides free)",
    "https://www.cs.ubc.ca/~tmm/vadbook/",
    "<b>&sect;1 through &sect;3</b> — the ranking, separability, and "
    "the popout material, organised."),
   ("Heer & Bostock &mdash; Crowdsourcing Graphical Perception (free)",
    "http://vis.stanford.edu/papers/crowdsourcing-graphical-perception",
    "<b>&sect;1 replicated at scale</b> — which confirmed the original "
    "ranking and extended it."),
   ("Ware &mdash; Information Visualization, chapters 1 through 5",
    "https://www.elsevier.com/books/information-visualization/ware/978-0-12-812875-6",
    "<b>&sect;1 and &sect;3's perceptual basis</b> — why the ranking "
    "has the shape it does. Library copy."),
 ],
 "exercises": [
   "<b>Reproduce the quantitative ranking from memory</b>, and check "
   "it.",
   "<b>Encode the same variable on position, length, and area</b>, and "
   "ask five people to estimate ratios from each.",
   "<b>Measure the area underestimation</b> in your own readings.",
   "<b>Truncate a bar axis</b> and ask people to compare two bars, then "
   "untruncate and ask again.",
   "<b>Encode eight categories on hue</b> and time how long a lookup "
   "takes.",
   "<b>Do the same with eight small multiples</b> and compare.",
   "<b>Encode two variables on size and hue</b>, then separate them, and "
   "compare readings.",
   "<b>Encode two variables on a rectangle's width and height</b>, and "
   "ask what people read.",
   "<b>Find an incidental channel variation</b> in a figure you made.",
   "<b>Run the four-question review</b> on five published figures.",
 ],
 "selfcheck": [
   "Give the quantitative ranking in order.",
   "Why does position dominate, and why is length second?",
   "Why is a truncated bar axis a perceptual problem rather than a "
   "stylistic one?",
   "By how much is area misread, and in which direction?",
   "Give the categorical ranking and the capacity of hue.",
   "What is the inversion between the two rankings, and what does it "
   "show?",
   "Name a separable pair and two interfering pairs.",
   "What bounds the number of variables you can encode?",
   "Why do readers attribute meaning to incidental variation?",
   "Give the four-question design review.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Data Types and Marks",
 "subtitle": "What the data is determines what the channel can be.",
 "question": "Why can this variable not go on that channel?",
 "outcomes": [
     "Classify attributes by measurement type.",
     "Explain which channels each type permits.",
     "Explain keys against values and why it matters.",
     "Explain derived attributes and when to compute them.",
     "Diagnose a type-channel mismatch.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Measurement types",
   "blurb": "Four, and each permits different operations."},

  {"t": "table", "kicker": "Types", "title": "The types, and what each permits",
   "header": ["Type", "Permits", "Example"],
   "widths": [2.5, 4.4, 4.5],
   "rows": [
     ["<b>Nominal</b>", "<b>Equality only</b>", "<b>Country, product category</b>"],
     ["<b>Ordinal</b>", "<b>Equality and order, not distance</b>", "<b>Small/medium/large; survey agreement</b>"],
     ["<b>Interval</b>", "<b>Order and differences, no true zero</b>", "<b>Temperature in Celsius; dates</b>"],
     ["<b>Ratio</b>", "<b>All of the above, plus ratios</b>", "<b>Count, mass, revenue, duration</b>"],
   ],
   "footnote": "<b>The interval/ratio distinction decides whether a "
               "ratio statement is meaningful</b> — 20 degrees "
               "Celsius is not twice 10, and that is also why an area "
               "encoding of an interval variable is "
               "nonsense.",
   "note": "The Celsius example settles the interval/ratio question "
           "quickly."},

  {"t": "callout", "title": "The type determines which channels are even available",
   "kind": "Why this module precedes the chart types",
   "body": ["<b>A nominal attribute cannot go on a quantitative "
            "channel</b> — <b>putting country codes on a numeric "
            "axis implies an order and a spacing that do not "
            "exist</b>, and readers will read both.",
            "<b>An ordinal attribute can go on an ordered channel "
            "and must not go on a continuous one</b> — the spacing "
            "between 'small' and 'medium' is undefined, so a position "
            "encoding asserts something false.",
            "<b>And a ratio attribute is the only type for which "
            "length and area are meaningful</b>, because <b>both "
            "channels are read as ratios from a zero</b> "
            "(Module 02 §1).",
            "<b>Which gives a diagnostic:</b> <b>a bar chart of an "
            "interval variable is a type error</b> — a bar's length "
            "asserts a ratio from zero, and an interval scale has no "
            "meaningful zero."]},

  {"t": "section", "label": "Part 2", "title": "Keys and values",
   "blurb": "A distinction that organises every chart."},

  {"t": "callout", "title": "A key identifies an item; a value is measured about it",
   "kind": "The distinction that determines the chart's structure",
   "body": ["<b>A key is independent</b> — the thing you are "
            "looking at, and usually what you are indexing or grouping "
            "by. <b>A value is dependent</b> — the measurement.",
            "<b>And the chart's structure follows:</b> <b>keys "
            "typically go on spatial position or on faceting; values go "
            "on the quantitative channels</b>, which is why most charts "
            "look the way they do.",
            "<b>With the number of keys determining the chart "
            "family:</b> <b>one key gives a bar chart or a line; two "
            "give a heatmap or a grouped chart; three or more give a "
            "faceted arrangement.</b>",
            "<b>So counting the keys and the values is the first step "
            "in choosing an encoding</b> — and <b>it is more "
            "informative than knowing the chart types</b>, because it "
            "narrows the choice before any aesthetic question "
            "arises."]},

  {"t": "code", "kicker": "Counting", "title": "The count determines the family",
   "lang": "text", "code": """
  1 KEY, 1 VALUE
      bar chart (key on position, value on length)
      or a line if the key is ordered and continuous

  1 KEY, SEVERAL VALUES
      grouped or stacked bars; a parallel coordinates
      plot; a radar chart (and radar charts have the
      angle problem of Module 02)

  2 KEYS, 1 VALUE
      a heatmap (both keys on position, value on
      colour) or a grouped bar

  0 KEYS, 2 VALUES
      a scatter plot -- both values on position,
      which is why it is the most accurate chart
      there is (Module 02 section 1)

  0 KEYS, 3+ VALUES
      a scatter plot matrix, or dimensionality
      reduction first (CSCE 676 Module 05)

  SO: count first, then choose.
""",
   "caption": "<b>A scatter plot puts both values on position</b>, "
              "which is why it is the most accurate chart available and "
              "should be the default for two quantities.",
   "note": "The scatter-plot-is-rank-one-twice observation is worth "
           "making explicit."},

  {"t": "section", "label": "Part 3", "title": "Derived attributes",
   "blurb": "Computing the thing the reader actually wants."},

  {"t": "bullets", "kicker": "Derivation", "title": "When to compute rather than to encode",
   "items": [
     "<b>If the reader's task is a difference, plot the "
     "difference.</b> <b>Two lines and a mental subtraction is far "
     "worse than one line of the difference</b> — because "
     "subtraction is not a visual channel.",
     "",
     "<b>If the task is a ratio or a rate, compute "
     "it</b> — per capita, per unit time, as a proportion of a "
     "total.",
     "",
     "<b>If the task is a change, plot the change</b>, not two "
     "snapshots — which is the commonest missed derivation.",
     "",
     "<b>And if the task is a rank, plot the rank</b> rather than "
     "the value, if the ordering is what matters.",
     "",
     "<b>Which is a restatement of Module 01 §2:</b> "
     "<b>the task determines the data, not only the "
     "encoding.</b>",
   ],
   "footnote": "<b>Plot the difference rather than two lines</b> "
               "— because <b>subtraction is not a visual "
               "channel</b>, and a reader asked to perform one will "
               "estimate it badly."},

  {"t": "callout", "title": "And normalisation is a derivation with a large effect on the conclusion",
   "kind": "Which makes it a reportable decision",
   "body": ["<b>Raw counts, per capita, per unit area, and "
            "year-on-year change can each produce a different and "
            "defensible picture of the same data</b> — and a map of "
            "raw counts is largely a map of population.",
            "<b>So the normalisation is an analytical choice that has "
            "to be stated</b>, not a formatting step — and "
            "<b>the reader cannot infer it from the figure</b> unless "
            "the label says so.",
            "<b>And the wrong normalisation is a common honest "
            "error:</b> <b>dividing by the wrong denominator produces "
            "a confident and wrong conclusion</b>, which Module 08 "
            "§3 treats for maps specifically.",
            "<b>Which is why the axis label is load-bearing</b> "
            "— <b>'cases' and 'cases per 100,000' are different "
            "claims</b>, and a figure that does not say which is not "
            "interpretable."]},

  {"t": "section", "label": "Part 4", "title": "Diagnosing mismatches",
   "blurb": "The errors this module exists to catch."},

  {"t": "bullets", "kicker": "Mismatches", "title": "The type-channel errors, and what each implies",
   "items": [
     "<b>Nominal on a position axis without a stated "
     "order</b> — which <b>implies an order the data does not "
     "have</b>, and readers will read the order as "
     "meaningful.",
     "",
     "<b>Ordinal spaced as though it were continuous</b> — "
     "which asserts distances that are undefined.",
     "",
     "<b>Interval encoded on length or area</b> — which "
     "asserts a ratio from a zero that does not exist.",
     "",
     "<b>Quantitative on hue</b> — which is "
     "Module 02 §1's rank seven, and is "
     "Module 04's main subject.",
     "",
     "<b>And a continuous variable binned without saying "
     "so</b> — where <b>the bin boundaries then do work the data "
     "did not</b> (Module 05 §3).",
   ],
   "footnote": "<b>Sorting a nominal axis by value is the fix for the "
               "first row</b> — it gives the reader a meaningful "
               "order instead of an arbitrary one, and costs "
               "nothing."},

  {"t": "callout", "title": "And sorting is the cheapest improvement available",
   "kind": "Closing",
   "body": ["<b>A bar chart with categories in alphabetical or "
            "source order makes the reader search</b> — and <b>the "
            "same chart sorted by value makes the ranking, the extremes, "
            "and the distribution readable at a glance.</b>",
            "<b>Which costs one line of code and improves every task "
            "except looking up a named category</b> — and that task "
            "is better served by a table "
            "(Module 01 §3).",
            "<b>So: sort by value unless there is a meaningful "
            "order</b> — and <b>if there is a meaningful order, "
            "respect it</b>, which is the ordinal case above.",
            "<b>And it is a good illustration of the module's "
            "point:</b> <b>the data's type determined that sorting was "
            "available</b>, and the task determined that it was "
            "worth doing."]},
 ],
 "takeaways": [
   "The interval/ratio distinction decides whether a ratio statement is "
   "meaningful, which is why a bar chart of an interval variable is a type "
   "error.",
   "A nominal attribute on a numeric axis implies an order and a spacing "
   "that do not exist, and readers will read both.",
   "Counting the keys and the values narrows the chart choice before any "
   "aesthetic question arises.",
   "A scatter plot puts both values on position, which makes it the most "
   "accurate chart available.",
   "Plot the difference rather than two lines, because subtraction is not "
   "a visual channel.",
   "Normalisation is an analytical choice the reader cannot infer, which "
   "is why the axis label is load-bearing.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Measurement types"),
  ("table", ["Type", "What it permits", "Example"],
   [["<b>Nominal</b>", "<b>Equality comparison only.</b>",
     "<b>Country, product category, error code.</b>"],
    ["<b>Ordinal</b>",
     "<b>Equality and order, but not distance.</b>",
     "<b>Small / medium / large; survey agreement levels; "
     "severity.</b>"],
    ["<b>Interval</b>",
     "<b>Order and differences, with no meaningful zero.</b>",
     "<b>Temperature in Celsius; calendar dates.</b>"],
    ["<b>Ratio</b>", "<b>All of the above, plus meaningful ratios.</b>",
     "<b>Count, mass, revenue, duration, distance.</b>"]],
   [0.19, 0.38, 0.43]),
  ("p", "<b>The interval/ratio distinction decides whether a ratio "
        "statement is meaningful</b> — <b>20 degrees Celsius is not "
        "twice 10 degrees</b>, because the zero is arbitrary — "
        "<b>and that is also exactly why an area or length encoding of an "
        "interval variable is nonsense</b> (&sect;1's callout). <b>The "
        "Celsius example settles the question quickly</b> and is worth "
        "keeping to hand, because the distinction otherwise feels "
        "pedantic until it produces a wrong chart."),
  ("callout", "The type determines which channels are even available",
   ["<b>A nominal attribute cannot go on a quantitative channel</b> "
    "— <b>putting country codes on a numeric axis implies both an "
    "order and a spacing that do not exist</b>, and <b>readers will read "
    "both of them</b> as meaningful (Module 02 &sect;3's "
    "attributed-meaning point).",
    "<b>An ordinal attribute can go on an ordered channel and must not "
    "go on a continuous one</b> — the spacing between 'small' and "
    "'medium' is undefined, <b>so a position encoding on a continuous "
    "axis asserts something the data does not contain.</b>",
    "<b>And a ratio attribute is the only type for which length and "
    "area are meaningful</b>, because <b>both of those channels are read "
    "as ratios from a zero</b> (Module 02 &sect;1's shared-reference "
    "argument) — so the zero has to mean something.",
    "<b>Which gives a clean diagnostic:</b> <b>a bar chart of an "
    "interval variable is a type error</b> — a bar's length asserts "
    "a ratio from zero, and an interval scale has no meaningful zero, so "
    "the figure makes a claim the data cannot support. A line or a point "
    "is correct there instead."]),

  ("h1", "2 &nbsp; Keys and values"),
  ("callout", "A key identifies an item; a value is measured about it",
   ["<b>A key is independent</b> — it is the thing you are looking "
    "at, and usually what you are indexing, grouping, or faceting "
    "by. <b>A value is dependent</b> — it is the measurement made "
    "about the item the key identifies.",
    "<b>And the chart's structure follows directly:</b> <b>keys "
    "typically go on spatial position or on faceting, and values go on "
    "the quantitative channels</b> — <b>which is why most charts "
    "look the way they do</b>, and makes the convention intelligible "
    "rather than arbitrary.",
    "<b>With the number of keys determining the chart family:</b> "
    "<b>one key gives a bar chart or a line; two keys give a heatmap or "
    "a grouped chart; three or more require a faceted "
    "arrangement</b> (Module 06 &sect;1).",
    "<b>So counting the keys and the values is the first step in "
    "choosing an encoding</b> — and <b>it is considerably more "
    "informative than knowing the names of chart types</b>, because it "
    "narrows the available choices before any aesthetic question "
    "arises."]),
  ("code", """1 KEY, 1 VALUE
    bar chart (key on position, value on length)
    or a line if the key is ordered and continuous

1 KEY, SEVERAL VALUES
    grouped or stacked bars; a parallel coordinates
    plot; a radar chart (and radar charts inherit the
    angle problem of Module 02 section 1)

2 KEYS, 1 VALUE
    a heatmap (both keys on position, the value on
    colour) or a grouped bar chart

0 KEYS, 2 VALUES
    a scatter plot -- both values on position, which
    is why it is the most accurate chart there is
    (Module 02 section 1)

0 KEYS, 3+ VALUES
    a scatter plot matrix, or dimensionality
    reduction first (CSCE 676 Module 05)

SO: count first, then choose."""),
  ("p", "<b>A scatter plot puts both values on position</b> — rank "
        "one, twice — <b>which is why it is the most accurate chart "
        "available and should be the default for two quantities</b>. "
        "<b>The scatter-plot-is-rank-one-twice observation is worth making "
        "explicit</b>, because it explains why scatter plots are so "
        "effective and why replacing one with a bar chart of binned values "
        "throws away accuracy (Module 05 &sect;3's binning point)."),

  ("break",),
  ("h1", "3 &nbsp; Derived attributes"),
  ("ul", ["<b>If the reader's task is a difference, plot the "
          "difference.</b> <b>Two lines and a mental subtraction is far "
          "worse than one line showing the difference directly</b> "
          "— <b>because subtraction is not a visual channel</b> and "
          "the reader will estimate it badly, especially where the lines "
          "are far apart.",
          "<b>If the task is a ratio or a rate, compute it</b> — "
          "per capita, per unit time, per unit area, or as a proportion "
          "of a total — rather than showing the numerator and the "
          "denominator and expecting division.",
          "<b>If the task is a change, plot the change</b>, not two "
          "snapshots — <b>which is the commonest missed "
          "derivation</b>, and which turns a comparison task into a "
          "lookup task.",
          "<b>And if the task is a rank, plot the rank</b> rather than "
          "the value, where the ordering is what matters and the "
          "magnitudes do not.",
          "<b>Which is a restatement of Module 01 &sect;2:</b> "
          "<b>the reader's task determines the data you should be "
          "plotting, not only the encoding you put it on</b> — and "
          "that is the broader and more useful version of the "
          "principle. <b>Plot the difference rather than two lines</b> "
          "is the one-line summary."]),
  ("callout", "And normalisation is a derivation with a large effect on the "
              "conclusion",
   ["<b>Raw counts, per capita figures, per unit area, and "
    "year-on-year change can each produce a different and individually "
    "defensible picture of exactly the same data</b> — and <b>a map "
    "of raw counts is largely a map of population</b>, which is "
    "Module 08 &sect;3's central warning.",
    "<b>So the normalisation is an analytical choice that has to be "
    "stated</b>, not a formatting step — and <b>the reader cannot "
    "infer which one you used from the figure</b> unless the axis label "
    "says so explicitly.",
    "<b>And the wrong normalisation is a common honest error:</b> "
    "<b>dividing by the wrong denominator produces a confident and wrong "
    "conclusion</b> that nothing in the figure contradicts — which "
    "Module 08 &sect;3 treats for geographic data where it is most "
    "frequent.",
    "<b>Which is why the axis label is load-bearing rather than "
    "decorative</b> — <b>'cases' and 'cases per 100,000' are "
    "different claims</b>, and <b>a figure that does not say which it is "
    "showing is not interpretable</b> at all, however well encoded."]),

  ("h1", "4 &nbsp; Diagnosing mismatches"),
  ("ul", ["<b>Nominal on a position axis without a stated order</b> "
          "— which <b>implies an order the data does not have</b>, "
          "and <b>readers will read that order as meaningful</b> "
          "(Module 02 &sect;3). See the fix below.",
          "<b>Ordinal spaced as though it were continuous</b> — "
          "equal gaps between 'rarely', 'sometimes', and 'often' "
          "— which <b>asserts distances that are undefined</b> and "
          "invites arithmetic on them.",
          "<b>Interval encoded on length or area</b> — which "
          "<b>asserts a ratio from a zero that does not exist</b> "
          "(&sect;1's diagnostic), and is why temperature bar charts are "
          "wrong and temperature lines are right.",
          "<b>Quantitative on colour hue</b> — which is "
          "<b>Module 02 &sect;1's rank seven</b> and is <b>Module 04's "
          "main subject</b>, and is probably the single most common "
          "mismatch in published figures.",
          "<b>And a continuous variable binned without saying so</b> "
          "— where <b>the bin boundaries then do work the data did "
          "not</b>, and a different binning gives a different picture "
          "(Module 05 &sect;3). <b>Sorting a nominal axis by value is "
          "the fix for the first row</b>: <b>it gives the reader a "
          "meaningful order instead of an arbitrary one, and it costs "
          "nothing.</b>"]),
  ("callout", "And sorting is the cheapest improvement available",
   ["<b>A bar chart with its categories in alphabetical order, or in "
    "whatever order the source file had, makes the reader search for "
    "everything</b> — and <b>the same chart sorted by value makes "
    "the ranking, the extremes, and the shape of the distribution "
    "readable at a glance.</b>",
    "<b>Which costs one line of code and improves every reader task "
    "except looking up a specific named category</b> — and <b>that "
    "task is better served by a table in any case</b> "
    "(Module 01 &sect;3's division of labour).",
    "<b>So: sort by value unless there is a meaningful order</b> "
    "— and <b>if there is a meaningful order, respect it</b>, which "
    "is the ordinal case from &sect;1 and is why sorting a month axis by "
    "value would be wrong.",
    "<b>And it is a good illustration of this module's whole "
    "point:</b> <b>the data's type determined that sorting was even "
    "available</b> (nominal, so no inherent order to violate), <b>and "
    "the reader's task determined that it was worth doing</b> — "
    "which is &sect;1 and Module 01 &sect;2 working together."]),
 ],
 "resources": [
   ("Munzner, chapters 2 and 3 (slides free)",
    "https://www.cs.ubc.ca/~tmm/vadbook/",
    "<b>&sect;1 and &sect;2</b> — the attribute types, the key/value "
    "distinction, and the dataset taxonomy."),
   ("Stevens &mdash; On the theory of scales of measurement (free)",
    "https://www.science.org/doi/10.1126/science.103.2684.677",
    "<b>&sect;1's four types in the original</b> — short, and the "
    "permitted-operations framing comes from here."),
   ("Wilkinson &mdash; The Grammar of Graphics",
    "https://link.springer.com/book/10.1007/0-387-28695-0",
    "<b>&sect;2 and &sect;3 formalised</b> — the grammar that "
    "ggplot2 and Vega-Lite implement. Library copy."),
   ("Wilke, the chapters on directory of visualizations (free)",
    "https://clauswilke.com/dataviz/",
    "<b>&sect;2's counting rules applied</b> — organised by what the "
    "data looks like rather than by chart name."),
 ],
 "exercises": [
   "<b>Classify twenty attributes</b> from a real dataset by "
   "measurement type.",
   "<b>Find an interval variable</b> and explain why a bar chart of it "
   "is wrong.",
   "<b>Find a nominal variable on a numeric axis</b> in a published "
   "figure.",
   "<b>Count the keys and values</b> for five datasets, and predict the "
   "chart family.",
   "<b>Plot two series and then their difference</b>, and ask five "
   "people to estimate the gap from each.",
   "<b>Compute a rate from two raw counts</b> and compare the two "
   "figures.",
   "<b>Normalise the same data three ways</b> and write the three "
   "different conclusions.",
   "<b>Find a figure whose axis label does not say the "
   "normalisation.</b>",
   "<b>Sort an alphabetical bar chart by value</b> and compare the "
   "readability.",
   "<b>Find a case where sorting would be wrong</b>, and say why.",
 ],
 "selfcheck": [
   "Name the four measurement types and what each permits.",
   "Why is 20 degrees Celsius not twice 10, and what follows for "
   "encoding?",
   "Why can nominal data not go on a numeric axis?",
   "Why is a bar chart of an interval variable a type error?",
   "Distinguish a key from a value, and say where each goes.",
   "Give the chart family for four key/value counts.",
   "Why is a scatter plot the most accurate chart?",
   "Give four derivations and the commonest missed one.",
   "Why is normalisation a reportable decision?",
   "Give five type-channel mismatches, and the cheapest improvement.",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Colour",
 "subtitle": "Where most published figures go wrong.",
 "question": "Why is the rainbow scale a defect?",
 "outcomes": [
     "Explain the three scale types and when each applies.",
     "Explain why the rainbow scale misleads.",
     "Explain perceptual uniformity and luminance ordering.",
     "Explain the accessibility requirements.",
     "Choose and check a colour scale.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Three kinds of scale",
   "blurb": "Matched to the three kinds of data."},

  {"t": "table", "kicker": "Scales", "title": "The scale types and what each is for",
   "header": ["Scale", "For", "Built from"],
   "widths": [2.5, 4.1, 4.8],
   "rows": [
     ["<b>Categorical</b>", "<b>Nominal data; no order implied</b>", "<b>Distinguishable hues, similar luminance</b>"],
     ["<b>Sequential</b>", "<b>Ordered data from a low to a high</b>", "<b>Monotonic luminance, one or two hues</b>"],
     ["<b>Diverging</b>", "<b>Data with a meaningful midpoint</b>", "<b>Two sequential ramps meeting at a neutral</b>"],
   ],
   "footnote": "<b>A diverging scale asserts that the midpoint "
               "means something</b> — zero, a baseline, an "
               "average — <b>so using one on data with no natural "
               "midpoint invents a reference the reader will "
               "believe.</b>",
   "note": "The invented-midpoint error is common and easy to "
           "state."},

  {"t": "callout", "title": "Luminance carries the ordering, which is why sequential scales must be monotonic in it",
   "kind": "The principle behind every correct scale",
   "body": ["<b>Hue is not ordered</b> "
            "(Module 02 §1's rank seven) — there is "
            "no perceptual sense in which green is between blue and "
            "yellow, whatever the wavelengths do.",
            "<b>But luminance is ordered</b>, and reliably "
            "so — <b>which means a sequential scale must increase "
            "monotonically in luminance</b>, and the hue is then "
            "decoration.",
            "<b>And that is the test:</b> <b>convert the scale to "
            "greyscale, and it should run smoothly from dark to "
            "light</b> — which is a five-second check and is "
            "CSCE 671 §02 §2's greyscale rule applied "
            "to a scale.",
            "<b>Which immediately condemns the rainbow</b> "
            "(Part 2), because <b>its luminance goes up and "
            "down several times</b> and therefore encodes no consistent "
            "order at all."]},

  {"t": "section", "label": "Part 2", "title": "The rainbow problem",
   "blurb": "Specifically, and it is worth being precise about."},

  {"t": "code", "kicker": "Rainbow", "title": "Four specific defects",
   "lang": "text", "code": """
  1. NON-MONOTONIC LUMINANCE
     it is bright at yellow and dark at blue and red,
     so the apparent ordering reverses mid-scale.

  2. PERCEPTUALLY NON-UNIFORM
     equal steps in the data are unequal steps in
     perceived difference. The green region is a wide
     band of near-identical colour; the
     cyan-to-blue transition is a sharp edge.

  3. IT CREATES FALSE BOUNDARIES
     those sharp transitions read as contours in the
     data. Readers see structure that is in the
     colour map, not in the measurement.

  4. AND IT FAILS FOR COLOUR VISION DEFICIENCY
     the red-green axis carries much of the range.

  SO: the rainbow scale invents boundaries and hides
  real gradients, which is the worst possible
  combination for a quantitative encoding.
""",
   "caption": "<b>It invents boundaries and hides real "
              "gradients</b> — which is the worst possible "
              "combination, and is why this is a defect rather than a "
              "preference.",
   "note": "The false-boundary point is the one that persuades "
           "scientists."},

  {"t": "callout", "title": "And the replacements are designed to fix exactly those four things",
   "kind": "What perceptual uniformity buys",
   "body": ["<b>The viridis family and its relatives are constructed "
            "to be monotonic in luminance and approximately uniform in "
            "perceived difference</b> — so equal data steps look "
            "equally different.",
            "<b>Which means no false boundaries</b>, because there "
            "are no sharp transitions to be mistaken for "
            "contours.",
            "<b>And they are designed to remain ordered under the "
            "common colour vision deficiencies</b>, because the "
            "luminance ramp survives when the hue discrimination does "
            "not (CSCE 632 §03).",
            "<b>So the switch is free and strictly "
            "better</b> — <b>which makes continuing to use a rainbow "
            "scale a decision rather than a default</b>, and one worth "
            "flagging in review."]},

  {"t": "section", "label": "Part 3", "title": "Categorical colour",
   "blurb": "A different problem with a capacity limit."},

  {"t": "bullets", "kicker": "Categorical", "title": "Choosing a categorical palette",
   "items": [
     "<b>Keep the luminance similar across the "
     "categories</b>, because <b>a luminance difference implies an "
     "order</b> that nominal data does not have.",
     "",
     "<b>Use at most five to seven</b> "
     "(Module 02 §2) — <b>and if you have more "
     "categories, group them or facet</b> rather than adding "
     "colours.",
     "",
     "<b>Reserve grey for the unimportant</b> — which is the "
     "most effective single technique in categorical colour: colour the "
     "one series that matters and grey the rest.",
     "",
     "<b>Respect existing conventions</b> where they exist, and "
     "<b>beware the ones that are cultural</b> — red for loss and "
     "green for gain is not universal.",
     "",
     "<b>And label directly rather than using a legend</b> where "
     "you can, since a legend is a memory task "
     "(CSCE 671 §03 §2).",
   ],
   "footnote": "<b>Direct labelling beats a legend</b> because it "
               "removes the lookup — and it is almost always "
               "possible for a small number of series."},

  {"t": "section", "label": "Part 4", "title": "Checking",
   "blurb": "Three tests, all fast."},

  {"t": "bullets", "kicker": "Checks", "title": "What to run on every figure",
   "items": [
     "<b>The greyscale test.</b> <b>Convert to greyscale: a "
     "sequential scale must still be ordered, and a categorical one "
     "must still be distinguishable</b> or must have a second "
     "channel.",
     "",
     "<b>The colour-vision simulation</b>, for the common "
     "deficiencies — <b>which takes seconds and catches the "
     "red-green encoding</b> (CSCE 632 §03).",
     "",
     "<b>And the print test</b>, since figures are still printed "
     "and photocopied, which is the greyscale test with worse "
     "contrast.",
     "",
     "<b>Plus: never use colour as the only channel</b> — add "
     "shape, pattern, position, or a direct label.",
     "",
     "<b>Which together take under a minute</b> and catch most of "
     "the colour errors in published work.",
   ],
   "footnote": "<b>Under a minute, and it catches most published "
               "colour errors</b> — which makes omitting the checks "
               "hard to defend."},

  {"t": "callout", "title": "And the honest summary of this module",
   "kind": "Closing",
   "body": ["<b>Colour is the channel people reach for first and the "
            "one with the most rules</b> — because it is "
            "perceptually complicated and because it is the easiest "
            "thing to change.",
            "<b>The rules reduce to three:</b> <b>match the scale "
            "type to the data type, make the ordering carried by "
            "luminance, and never let colour be the only "
            "channel.</b>",
            "<b>And the checks reduce to one:</b> <b>convert to "
            "greyscale and see whether it still works</b>, which "
            "subsumes most of the others.",
            "<b>Which is a small enough set to apply every "
            "time</b> — and <b>the rainbow scale persists in "
            "published science precisely because nobody applied "
            "it.</b>"]},
 ],
 "takeaways": [
   "A diverging scale asserts that the midpoint means something, so using "
   "one without a natural midpoint invents a reference.",
   "Hue is not ordered and luminance is, so a sequential scale must be "
   "monotonic in luminance and the hue is decoration.",
   "The rainbow scale invents boundaries and hides real gradients, which "
   "is the worst possible combination.",
   "Keep luminance similar across categorical colours, because a "
   "luminance difference implies an order nominal data does not have.",
   "Reserve grey for the unimportant — colouring the one series that "
   "matters is the most effective single technique.",
   "Convert to greyscale and see whether it still works; that one check "
   "subsumes most of the others.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Three kinds of scale"),
  ("table", ["Scale", "What it is for", "How it is built"],
   [["<b>Categorical</b>",
     "<b>Nominal data, with no order implied.</b>",
     "<b>Distinguishable hues at similar luminance</b> — see "
     "&sect;3."],
    ["<b>Sequential</b>",
     "<b>Ordered data running from a low value to a high one.</b>",
     "<b>Monotonic luminance, with one or two hues</b> — see the "
     "callout."],
    ["<b>Diverging</b>",
     "<b>Data with a meaningful midpoint.</b>",
     "<b>Two sequential ramps meeting at a neutral colour</b> at the "
     "midpoint."]],
   [0.19, 0.38, 0.43]),
  ("p", "<b>A diverging scale asserts that the midpoint means "
        "something</b> — a zero, a baseline, a long-run average, a "
        "threshold — <b>so using one on data with no natural midpoint "
        "invents a reference that the reader will believe</b>, and the "
        "neutral colour will be read as 'normal'. <b>The invented-midpoint "
        "error is common and easy to state</b>, and it is one of the few "
        "colour errors that changes the conclusion rather than merely the "
        "legibility."),
  ("callout", "Luminance carries the ordering, which is why sequential "
              "scales must be monotonic in it",
   ["<b>Hue is not ordered</b> (Module 02 &sect;1's rank seven) "
    "— <b>there is no perceptual sense in which green is 'between' "
    "blue and yellow</b>, whatever the wavelengths do, and readers cannot "
    "reliably order hues even when told the intended order.",
    "<b>But luminance is ordered, and reliably so</b> — darker and "
    "lighter are unambiguous — <b>which means a sequential scale "
    "must increase monotonically in luminance</b>, and <b>the hue is then "
    "decoration</b> that helps with discrimination but carries no "
    "order.",
    "<b>And that gives the test:</b> <b>convert the scale to "
    "greyscale, and it should run smoothly from dark to light</b> "
    "— <b>which is a five-second check</b> and is <b>CSCE 671 "
    "Module 02 &sect;2's greyscale rule applied specifically to a "
    "colour scale.</b>",
    "<b>Which immediately condemns the rainbow</b> (&sect;2), because "
    "<b>its luminance goes up and down several times across the "
    "range</b> — bright at yellow, dark at both ends — <b>and "
    "therefore encodes no consistent order at all.</b>"]),

  ("h1", "2 &nbsp; The rainbow problem"),
  ("code", """1. NON-MONOTONIC LUMINANCE
   it is bright at yellow and dark at both blue and
   red, so the apparent ordering reverses mid-scale
   and the brightest region is in the middle.

2. PERCEPTUALLY NON-UNIFORM
   equal steps in the data are unequal steps in
   perceived difference. The green region is a wide
   band of near-identical colour; the cyan-to-blue
   transition is a sharp perceptual edge.

3. IT CREATES FALSE BOUNDARIES
   those sharp transitions read as contours in the
   data. Readers see structure that is in the colour
   map and not in the measurement.

4. AND IT FAILS FOR COLOUR VISION DEFICIENCY
   the red-green axis carries much of the range.

SO: the rainbow scale invents boundaries and hides
real gradients, which is the worst possible
combination for a quantitative encoding."""),
  ("p", "<b>It invents boundaries and hides real gradients</b> — "
        "<b>which is the worst possible combination for a quantitative "
        "encoding, and is why this is a defect rather than a "
        "preference</b>. <b>The false-boundary point is the one that "
        "persuades scientists</b>: a reader examining a rainbow-coloured "
        "field will identify features at the cyan-blue transition that "
        "have no counterpart in the data, and will fail to see a real "
        "gradient that falls inside the green band. That is a measurement "
        "being misreported by its presentation."),
  ("callout", "And the replacements are designed to fix exactly those four "
              "things",
   ["<b>The viridis family and its relatives are constructed to be "
    "monotonic in luminance and approximately uniform in perceived "
    "difference</b> — so <b>equal steps in the data look equally "
    "different to a reader</b>, which is the property the encoding "
    "requires.",
    "<b>Which means no false boundaries</b>, because <b>there are no "
    "sharp perceptual transitions to be mistaken for contours in the "
    "data</b> — the second and third defects are addressed by the "
    "same construction.",
    "<b>And they are designed to remain ordered under the common "
    "colour vision deficiencies</b>, <b>because the luminance ramp "
    "survives even when the hue discrimination does not</b> "
    "(CSCE 632 &sect;3) — which is a direct consequence of the "
    "monotonic luminance rather than a separate feature.",
    "<b>So the switch is free and strictly better</b> — the scales "
    "ship with every plotting library — <b>which makes continuing to "
    "use a rainbow scale a decision rather than a default</b>, and "
    "<b>one worth flagging in review</b> rather than tolerating."]),

  ("break",),
  ("h1", "3 &nbsp; Categorical colour"),
  ("ul", ["<b>Keep the luminance similar across the "
          "categories</b>, because <b>a luminance difference implies an "
          "order</b> (&sect;1's callout) <b>that nominal data does not "
          "have</b> — and readers will take the darkest category to "
          "be the most or the largest.",
          "<b>Use at most five to seven colours</b> (Module 02 "
          "&sect;2's capacity) — <b>and if you have more categories, "
          "group them or facet rather than adding more colours</b>, which "
          "turns the channel into a legend lookup.",
          "<b>Reserve grey for the unimportant</b> — which is "
          "<b>the most effective single technique in categorical "
          "colour</b>: colour the one or two series that matter and make "
          "all the others grey, which uses the preattentive pop-out of "
          "CSCE 671 Module 02 &sect;3 deliberately.",
          "<b>Respect existing conventions where they exist</b>, and "
          "<b>beware the ones that are cultural</b> — <b>red for "
          "loss and green for gain is not universal</b>, and neither is "
          "the political colour mapping, which inverts between "
          "countries.",
          "<b>And label the series directly rather than using a "
          "legend</b> wherever you can, since <b>a legend is a memory "
          "task</b> (CSCE 671 Module 03 &sect;2) that has to be "
          "performed for every mark. <b>Direct labelling beats a "
          "legend</b> because it removes the lookup, <b>and it is almost "
          "always possible for a small number of series.</b>"]),

  ("h1", "4 &nbsp; Checking"),
  ("ul", ["<b>The greyscale test.</b> <b>Convert the figure to "
          "greyscale: a sequential scale must still be ordered, and a "
          "categorical one must still be distinguishable</b> or <b>must "
          "carry a second channel</b> (shape, pattern, direct "
          "label).",
          "<b>The colour-vision simulation</b>, for the common "
          "deficiencies — <b>which takes seconds with any of several "
          "free tools and catches the red-green encoding</b> immediately "
          "(CSCE 632 &sect;3).",
          "<b>And the print test</b>, since figures are still "
          "printed, photocopied, and projected badly — <b>which is "
          "the greyscale test with worse contrast</b> and catches "
          "insufficient luminance separation.",
          "<b>Plus the standing rule: never use colour as the only "
          "channel</b> — add shape, pattern, position, or a direct "
          "label, so that the figure degrades gracefully rather than "
          "becoming unreadable.",
          "<b>Which together take under a minute</b> and <b>catch most "
          "of the colour errors in published work</b> — <b>which "
          "makes omitting them quite hard to defend</b>, and is why this "
          "module ends on them rather than on the theory."]),
  ("callout", "And the honest summary of this module",
   ["<b>Colour is the channel people reach for first and the one with "
    "the most rules</b> — <b>because it is perceptually complicated "
    "and because it is the easiest thing in a figure to change</b>, so it "
    "absorbs attention disproportionately.",
    "<b>The rules reduce to three:</b> <b>match the scale type to the "
    "data type (&sect;1), make the ordering carried by luminance "
    "(&sect;1's callout), and never let colour be the only channel "
    "(&sect;4).</b>",
    "<b>And the checks reduce to one:</b> <b>convert to greyscale and "
    "see whether it still works</b> — <b>which subsumes most of the "
    "others</b>, since it tests the luminance ordering, the "
    "colour-only encoding, and the print case simultaneously.",
    "<b>Which is a small enough set to apply every single "
    "time</b> — and <b>the rainbow scale persists in published "
    "science precisely because nobody applied it</b>, not because "
    "anybody defended it."]),
 ],
 "resources": [
   ("Wilke, the colour chapters (free)",
    "https://clauswilke.com/dataviz/",
    "<b>The whole module</b> — the scale types, the pitfalls, and the "
    "examples, free in full."),
   ("Borland & Taylor &mdash; Rainbow Color Map (Still) Considered "
    "Harmful (free)",
    "https://ieeexplore.ieee.org/document/4118486",
    "<b>&sect;2's four defects</b>, with the figures — short, and the "
    "false-boundary demonstration is the persuasive part."),
   ("Colorbrewer, and the viridis documentation (free)",
    "https://colorbrewer2.org/",
    "<b>&sect;1 and &sect;3 as working tools</b> — with the "
    "colour-blind-safe and print-safe filters, which do &sect;4's work "
    "for you."),
   ("Crameri, Shephard & Heron &mdash; The misuse of colour in science "
    "(free)",
    "https://www.nature.com/articles/s41467-020-19160-7",
    "<b>&sect;2 measured across a literature</b> — how prevalent the "
    "problem is, and what it has cost."),
 ],
 "exercises": [
   "<b>Classify five figures' colour scales</b> as categorical, "
   "sequential, or diverging, and say whether each matches its data.",
   "<b>Find a diverging scale on data with no midpoint</b>, and say "
   "what it implies.",
   "<b>Convert a rainbow scale to greyscale</b> and plot its luminance "
   "against position.",
   "<b>Render the same field in rainbow and in viridis</b>, and ask five "
   "people to describe the features.",
   "<b>Count the features they report that are not in the data.</b>",
   "<b>Build a categorical palette with varying luminance</b> and ask "
   "people which category is largest.",
   "<b>Grey out all but one series</b> in a multi-series chart, and "
   "compare.",
   "<b>Replace a legend with direct labels</b> and time a lookup from "
   "each.",
   "<b>Run all three checks</b> on five of your own figures.",
   "<b>Find a cultural colour convention</b> that inverts between two "
   "regions.",
 ],
 "selfcheck": [
   "Name the three scale types and what each is for.",
   "What does a diverging scale assert, and what is the error?",
   "Why does luminance carry the ordering and hue not?",
   "Give the five-second test for a sequential scale.",
   "Give the four defects of the rainbow scale.",
   "Which defect persuades scientists, and why?",
   "What do the perceptually uniform scales fix, and how does that help "
   "colour vision deficiency?",
   "Give five rules for categorical colour, and the most effective "
   "technique.",
   "Give the three checks and the standing rule.",
   "Reduce this module to three rules and one check.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Chart Types",
 "subtitle": "Which follow from the earlier modules rather than "
             "preceding them.",
 "question": "Which chart, and why that one?",
 "outcomes": [
     "Choose a chart from the data and the task.",
     "Explain distributions and why histograms mislead.",
     "Explain the specific chart controversies with evidence.",
     "Explain aspect ratio and axis conventions.",
     "Justify a chart choice from the ranking.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The choice",
   "blurb": "Which is now nearly determined."},

  {"t": "code", "kicker": "Choosing", "title": "The decision, from Modules 01 to 04",
   "lang": "text", "code": """
  1. COUNT keys and values (Module 03 section 2),
     which gives the chart family.

  2. NAME the reader's task (Module 01 section 2),
     which says which variable must be accurate.

  3. ASSIGN that variable to position
     (Module 02 section 1), and work down the ranking
     for the others.

  4. CHECK the types permit the channels
     (Module 03 section 1).

  5. CHECK the colour (Module 04 section 4).

  AND THE CHART TYPE IS WHATEVER THAT PRODUCED.

  WHICH IS THE POINT OF THE ORDERING: by this module
  the choice is nearly determined, and the remaining
  decisions are the ones in sections 2 to 4.
""",
   "caption": "<b>By this module the choice is nearly "
              "determined</b> — which is why the chart types come "
              "fifth rather than first.",
   "note": "Emphasise that this module is a consequence rather than a "
           "catalogue."},

  {"t": "callout", "title": "Which is why there is no chart-type decision tree worth memorising",
   "kind": "The methodological point",
   "body": ["<b>A decision tree from data shape to chart name "
            "encodes somebody's answers to Modules 01 to 04 without "
            "showing the reasoning</b> — so it works on the cases "
            "they considered and fails silently on yours.",
            "<b>And it cannot produce a chart nobody has "
            "named</b>, which real data frequently requires "
            "(Module 01 §1).",
            "<b>So the five steps above are the method, and the "
            "chart-type galleries are a source of ideas rather than of "
            "answers.</b>",
            "<b>Which is worth saying because the galleries are "
            "excellent and are used wrongly</b> — <b>as a menu to "
            "choose from rather than as examples of encodings to "
            "learn.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Distributions",
   "blurb": "Where the standard chart is the weakest."},

  {"t": "bullets", "kicker": "Distributions", "title": "Showing a distribution, in increasing honesty",
   "items": [
     "<b>A histogram</b> — and <b>the bin width changes the "
     "shape</b>, sometimes dramatically, which makes the bin choice an "
     "undisclosed analytical decision "
     "(Module 03 §4).",
     "",
     "<b>A density estimate</b> — which replaces the bin "
     "width with a bandwidth and has the same problem, more "
     "smoothly.",
     "",
     "<b>A box plot</b> — compact and comparable across "
     "groups, and <b>it hides multimodality entirely</b>: two "
     "very different distributions can give identical "
     "boxes.",
     "",
     "<b>A violin or a beeswarm</b> — which shows the shape, "
     "and is the right default for a moderate number of "
     "points.",
     "",
     "<b>And the points themselves</b>, jittered, which is the "
     "most honest and only works below a few hundred.",
   ],
   "footnote": "<b>Show the points where you can</b> — every "
               "summary above discards the thing you were looking for, "
               "which is the shape."},

  {"t": "callout", "title": "A box plot hides exactly the structure you were looking for",
   "kind": "The specific case worth knowing",
   "body": ["<b>A box plot shows five numbers</b> — and "
            "<b>bimodality, clustering, gaps, and unequal sample sizes "
            "are all invisible in it.</b>",
            "<b>So two groups with identical boxes can have "
            "completely different distributions</b> — one unimodal, "
            "one split into two separated clusters — and the figure "
            "says they are the same.",
            "<b>Which is CSCE 679 §01 §3's "
            "identical-statistics problem</b>, arriving in the chart "
            "most commonly used to compare groups.",
            "<b>So: overlay the points on the box</b> where the "
            "sample size permits, which costs nothing and restores "
            "what the summary removed — and <b>state the n per "
            "group</b>, which a box plot never shows."]},

  {"t": "section", "label": "Part 3", "title": "The controversies",
   "blurb": "With the evidence, which is more mixed than the arguments."},

  {"t": "table", "kicker": "Contested", "title": "The contested charts, assessed",
   "header": ["Chart", "The objection", "The honest position"],
   "widths": [2.3, 3.9, 5.2],
   "rows": [
     ["<b>Pie chart</b>", "<b>Angle is rank four (M02 §1)</b>", "<b>Poor for comparison; acceptable for part-of-whole with few slices</b>"],
     ["<b>Stacked bar</b>", "<b>Only the bottom series has a baseline</b>", "<b>Fine for the total, poor for the middle series</b>"],
     ["<b>Dual axis</b>", "<b>The crossing point is arbitrary</b>", "<b>Genuinely misleading; use two panels</b>"],
     ["<b>3D bar chart</b>", "<b>Occlusion and foreshortening</b>", "<b>No defence; it is strictly worse</b>"],
     ["<b>Radar chart</b>", "<b>Area scales as the square; axis order matters</b>", "<b>Hard to read; a parallel coordinates plot is better</b>"],
   ],
   "footnote": "<b>The dual axis is the one that actually "
               "deceives</b> — the apparent crossing or divergence is "
               "a function of the two scalings, which the author chose "
               "and the reader cannot see.",
   "note": "Distinguish the merely weak from the actively "
           "misleading."},

  {"t": "callout", "title": "And the data-ink argument did not survive measurement intact",
   "kind": "A case where the influential advice was partly wrong",
   "body": ["<b>The claim was that non-data elements should be "
            "minimised</b> — gridlines, frames, redundant labels, "
            "decoration — <b>and that chart junk harms "
            "reading.</b>",
            "<b>And the direction is right for genuine "
            "clutter:</b> <b>heavy gridlines, 3D effects, and "
            "background images do measurably interfere.</b>",
            "<b>But the stronger version did not replicate:</b> "
            "<b>some redundancy aids reading, gridlines aid value "
            "estimation, and memorable decoration improved recall in "
            "controlled studies</b> without harming "
            "accuracy.",
            "<b>So the honest position is: remove what interferes, "
            "and keep what helps a stated task</b> — <b>which is "
            "less quotable and more defensible</b>, and is a good "
            "illustration of why this course states mechanisms."]},

  {"t": "section", "label": "Part 4", "title": "Axes and aspect",
   "blurb": "Two decisions with large perceptual effects."},

  {"t": "bullets", "kicker": "Axes", "title": "The conventions, with their reasons",
   "items": [
     "<b>A bar chart's value axis must include "
     "zero</b>, because <b>length is read as a ratio from the "
     "baseline</b> (Module 02 §1) — so truncating it "
     "misstates every comparison.",
     "",
     "<b>A line chart's axis need not include zero</b>, because "
     "<b>position is read against the scale and not against a "
     "baseline</b> — which is why the two conventions "
     "differ.",
     "",
     "<b>And the aspect ratio changes the perceived "
     "trend</b> — the same data looks flat or steep depending on "
     "it, which makes it a reportable choice.",
     "",
     "<b>Banking to 45 degrees</b> is the classical answer: "
     "slopes are judged most accurately near that angle.",
     "",
     "<b>And a log axis must be labelled as such "
     "prominently</b>, because <b>readers extrapolate linearly from "
     "a log plot</b> if they do not notice.",
   ],
   "footnote": "<b>The bar-versus-line zero distinction is the one "
               "people get wrong in both directions</b> — and the "
               "reason is the channel, not a convention."},

  {"t": "callout", "title": "Which is the module's summary",
   "kind": "Closing",
   "body": ["<b>Every rule in this module is a consequence of the "
            "channel ranking or of the data types</b> — including the "
            "ones that are usually stated as conventions.",
            "<b>Which means you can derive them rather than "
            "remembering them</b>, and <b>can decide a case the "
            "conventions do not cover</b>.",
            "<b>And where the evidence is mixed, say so</b> "
            "— <b>the data-ink case shows that confident design "
            "advice can be partly wrong</b>, and the mechanism is what "
            "survives.",
            "<b>So: derive the choice, state the task it serves, and "
            "test it on readers</b> (Module 13) — which is this "
            "course's whole method in one line."]},
 ],
 "takeaways": [
   "By this module the chart choice is nearly determined, which is why the "
   "chart types come fifth rather than first.",
   "A chart-type decision tree encodes somebody else's reasoning without "
   "showing it, and cannot produce a chart nobody has named.",
   "A histogram's bin width changes the shape, which makes it an "
   "undisclosed analytical decision.",
   "A box plot hides bimodality, clustering, and gaps — exactly the "
   "structure you were looking for.",
   "The dual axis is the contested chart that actually deceives, because "
   "the crossing point is a function of two chosen scalings.",
   "A bar's axis must include zero and a line's need not, because length "
   "is read from a baseline and position is not.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The choice"),
  ("code", """1. COUNT keys and values (Module 03 section 2),
   which gives the chart family.

2. NAME the reader's task (Module 01 section 2),
   which says which variable must be read accurately.

3. ASSIGN that variable to position (Module 02
   section 1), and work down the ranking for the
   others.

4. CHECK that the data types permit the channels you
   assigned (Module 03 section 1).

5. CHECK the colour (Module 04 section 4).

AND THE CHART TYPE IS WHATEVER THAT PRODUCED.

WHICH IS THE POINT OF THE ORDERING: by this module the
choice is nearly determined, and the only remaining
decisions are the ones in sections 2 to 4."""),
  ("callout", "Which is why there is no chart-type decision tree worth "
              "memorising",
   ["<b>A decision tree running from data shape to chart name encodes "
    "somebody else's answers to Modules 01 through 04 without showing the "
    "reasoning</b> — <b>so it works on the cases they considered and "
    "fails silently on yours</b>, with no indication that it has done "
    "so.",
    "<b>And it cannot produce a chart nobody has named</b>, <b>which "
    "real data frequently requires</b> (Module 01 &sect;1's "
    "mark-and-channel framing exists precisely to make that "
    "possible).",
    "<b>So the five steps above are the method, and the chart-type "
    "galleries are a source of ideas rather than of answers.</b>",
    "<b>Which is worth saying because the galleries are genuinely "
    "excellent and are used wrongly</b> — <b>as a menu to choose "
    "from rather than as a collection of encodings to learn from</b>, and "
    "the difference determines whether you can handle a case they do not "
    "contain."]),

  ("h1", "2 &nbsp; Distributions"),
  ("ul", ["<b>A histogram</b> — and <b>the bin width changes the "
          "shape</b>, sometimes dramatically: the same data can appear "
          "unimodal or bimodal depending on it, <b>which makes the bin "
          "choice an undisclosed analytical decision</b> "
          "(Module 03 &sect;4's binning point).",
          "<b>A kernel density estimate</b> — which replaces the "
          "bin width with a bandwidth and <b>has exactly the same "
          "problem, more smoothly</b> and therefore less visibly, since "
          "the result always looks plausible.",
          "<b>A box plot</b> — compact, and genuinely good for "
          "comparing many groups — and <b>it hides multimodality "
          "entirely</b>: see the callout.",
          "<b>A violin plot or a beeswarm</b> — which shows the "
          "actual shape, and <b>is the right default for a moderate "
          "number of points</b> and a moderate number of groups.",
          "<b>And the points themselves, jittered</b>, which is <b>the "
          "most honest representation and only works below a few hundred "
          "points</b> per group. <b>Show the points where you "
          "can</b> — <b>every summary above discards the thing you "
          "were looking for</b>, which is the shape of the "
          "distribution."]),
  ("callout", "A box plot hides exactly the structure you were looking for",
   ["<b>A box plot shows five numbers</b> — the median, the "
    "quartiles, and the whisker extent — and <b>bimodality, "
    "clustering, gaps, and unequal sample sizes are all completely "
    "invisible in it.</b>",
    "<b>So two groups with identical box plots can have entirely "
    "different distributions</b> — one unimodal and one split into "
    "two well-separated clusters — <b>and the figure asserts that "
    "they are the same.</b>",
    "<b>Which is Module 01 &sect;3's identical-statistics problem "
    "arriving in the chart most commonly used to compare groups</b>, and "
    "is therefore worth knowing specifically rather than as a general "
    "caution.",
    "<b>So: overlay the individual points on the box</b> wherever the "
    "sample size permits — <b>which costs nothing and restores "
    "exactly what the summary removed</b> — and <b>state the n per "
    "group</b>, <b>which a box plot never shows</b> and which determines "
    "how much any of it means."]),

  ("break",),
  ("h1", "3 &nbsp; The controversies"),
  ("table", ["Chart", "The objection", "The honest position"],
   [["<b>Pie chart</b>",
     "<b>It encodes on angle and area, ranks four and five</b> "
     "(Module 02 &sect;1).",
     "<b>Poor for comparing slices; acceptable for a part-of-whole "
     "judgement with very few slices.</b>"],
    ["<b>Stacked bar</b>",
     "<b>Only the bottom series has a common baseline.</b>",
     "<b>Fine for reading the total and poor for comparing the middle "
     "series</b> — so it depends entirely on the task."],
    ["<b>Dual axis</b>",
     "<b>The apparent crossing point is arbitrary.</b>",
     "<b>Genuinely misleading; use two stacked panels sharing an x "
     "axis</b> — see the note."],
    ["<b>3D bar chart</b>",
     "<b>Occlusion, foreshortening, and a false depth channel.</b>",
     "<b>No defence; it is strictly worse than the 2D version</b> in "
     "every respect."],
    ["<b>Radar / spider chart</b>",
     "<b>Area scales as the square of the values, and the axis order "
     "changes the shape.</b>",
     "<b>Hard to read; a parallel coordinates plot or a small-multiple "
     "bar chart does the job better.</b>"]],
   [0.18, 0.31, 0.51]),
  ("p", "<b>The dual axis is the one that actually deceives</b> — "
        "<b>the apparent crossing or divergence of the two series is a "
        "function of the two independent scalings, which the author chose "
        "and the reader cannot see</b> — so any desired relationship "
        "can be manufactured by adjusting one axis. <b>Distinguishing the "
        "merely weak charts from the actively misleading ones is worth "
        "doing</b>: a pie chart is a poor encoding and an honest one, and "
        "a dual axis is a specific deception "
        "(Module 10 &sect;2)."),
  ("callout", "And the data-ink argument did not survive measurement intact",
   ["<b>The claim was that non-data elements should be "
    "minimised</b> — gridlines, frames, redundant labels, decorative "
    "imagery — <b>and that 'chart junk' actively harms reading</b>, "
    "stated forcefully and very influentially.",
    "<b>And the direction is right for genuine clutter:</b> <b>heavy "
    "gridlines, 3D effects, drop shadows, and background images do "
    "measurably interfere with reading</b>, which the studies "
    "confirm.",
    "<b>But the stronger version did not replicate:</b> <b>some "
    "redundancy aids reading, gridlines measurably aid value estimation, "
    "and memorable decoration improved recall in controlled studies "
    "without harming accuracy</b> — so the minimisation principle "
    "was overstated.",
    "<b>So the honest position is: remove what interferes, and keep "
    "what helps a stated task</b> — <b>which is considerably less "
    "quotable and considerably more defensible</b>, and <b>is a good "
    "illustration of why this course states mechanisms rather than "
    "rules</b> (CSCE 671 Module 05 &sect;1): a rule with no "
    "mechanism cannot be corrected by evidence."]),

  ("h1", "4 &nbsp; Axes and aspect ratio"),
  ("ul", ["<b>A bar chart's value axis must include zero</b>, because "
          "<b>length is read as a ratio from the baseline</b> "
          "(Module 02 &sect;1's shared-reference argument) — <b>so "
          "truncating it misstates every comparison in the figure</b>, by "
          "an amount the reader cannot recover.",
          "<b>A line chart's axis need not include zero</b>, because "
          "<b>position is read against the scale rather than against a "
          "baseline</b> — <b>which is precisely why the two "
          "conventions differ</b>, and is the reason rather than an "
          "arbitrary distinction.",
          "<b>And the aspect ratio changes the perceived "
          "trend</b> — the same series looks flat in a wide figure "
          "and steep in a tall one — <b>which makes it a reportable "
          "choice</b> rather than a layout detail.",
          "<b>Banking to 45 degrees is the classical answer:</b> "
          "<b>slopes are judged most accurately when they are near 45 "
          "degrees</b>, so choose the aspect ratio to put the trend of "
          "interest near that angle.",
          "<b>And a log axis must be labelled as such "
          "prominently</b>, because <b>readers extrapolate linearly from "
          "a log plot if they do not notice the scale</b> — which "
          "produces order-of-magnitude errors in the conclusion. <b>The "
          "bar-versus-line zero distinction is the one people get wrong "
          "in both directions</b>, and <b>the reason is the channel "
          "rather than a convention</b>, which is what makes it "
          "memorable."]),
  ("callout", "Which is the module's summary",
   ["<b>Every rule in this module is a consequence of the channel "
    "ranking or of the data types</b> — <b>including the ones that "
    "are usually stated as bare conventions</b>, like the zero-baseline "
    "rule and the pie chart objection.",
    "<b>Which means you can derive them rather than remembering "
    "them</b>, and more importantly <b>can decide a case the conventions "
    "do not cover</b> — which is what the five-step method in "
    "&sect;1 is for.",
    "<b>And where the evidence is mixed, say so</b> — <b>the "
    "data-ink case shows that confident design advice can be partly "
    "wrong</b>, <b>and the mechanism is what survives</b> when the rule "
    "does not.",
    "<b>So: derive the choice, state the task it serves, and test it "
    "on readers</b> (Module 13) — <b>which is this course's whole "
    "method in one line</b> and is what Project 1 asks you to "
    "demonstrate."]),
 ],
 "resources": [
   ("Wilke, the directory of visualisations and the pitfalls chapters "
    "(free)",
    "https://clauswilke.com/dataviz/",
    "<b>&sect;2 through &sect;4</b> — the distribution charts and the "
    "axis conventions, with examples of each failure."),
   ("Tufte &mdash; The Visual Display of Quantitative Information",
    "https://www.edwardtufte.com/tufte/books_vdqi",
    "<b>&sect;3's data-ink argument in the original</b> — read it "
    "alongside the replication work below. Library copy."),
   ("Bateman et al. &mdash; Useful Junk? (free)",
    "https://dl.acm.org/doi/10.1145/1753326.1753716",
    "<b>&sect;3's callout, measured</b> — the study that found "
    "decoration aided recall without harming accuracy."),
   ("Cleveland &mdash; The Elements of Graphing Data",
    "https://www.taylorfrancis.com/books/mono/10.1201/9781315402840/",
    "<b>&sect;4's banking argument and the aspect ratio "
    "material</b> — where it was developed. Library copy."),
 ],
 "exercises": [
   "<b>Run the five-step choice</b> on three datasets and record what "
   "chart it produced.",
   "<b>Find a case the galleries do not cover</b> and design for it from "
   "the steps.",
   "<b>Plot the same data at four bin widths</b> and report how the "
   "shape changes.",
   "<b>Construct two distributions with identical box plots</b> and "
   "different shapes.",
   "<b>Overlay the points</b> and confirm the difference becomes "
   "visible.",
   "<b>Find a dual-axis chart</b> and rescale one axis to reverse the "
   "apparent conclusion.",
   "<b>Replace it with two panels</b> and compare.",
   "<b>Truncate a bar axis and a line axis</b>, and explain why only one "
   "is a deception.",
   "<b>Vary the aspect ratio</b> of a time series and ask five people "
   "whether the trend is strong.",
   "<b>Find a log axis that is not prominently labelled.</b>",
 ],
 "selfcheck": [
   "Give the five-step chart choice.",
   "Why is there no decision tree worth memorising?",
   "Name five ways to show a distribution, in increasing honesty.",
   "What does a histogram's bin width do, and why is a density estimate "
   "no better?",
   "What does a box plot hide, and what is the fix?",
   "Name five contested charts and the honest position on each.",
   "Which one actually deceives, and why?",
   "What survived of the data-ink argument and what did not?",
   "Why must a bar axis include zero and a line axis need not?",
   "What does aspect ratio do, and what is banking to 45 degrees?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Multiple Views and Interaction",
 "subtitle": "More than fits in one figure.",
 "question": "What do you do when one chart is not enough?",
 "outcomes": [
     "Explain small multiples and when to use them.",
     "Explain coordinated views and linked selection.",
     "Explain the interaction vocabulary.",
     "Explain what interaction costs.",
     "Design a multi-view figure for a stated task.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Small multiples",
   "blurb": "The strongest technique in the course."},

  {"t": "callout", "title": "Small multiples put a categorical variable on spatial region, which is the most accurate channel for it",
   "kind": "Why this works so well",
   "body": ["<b>Repeat the same chart once per category, in a "
            "grid</b> — which puts the category on spatial region, "
            "<b>rank one for categorical data</b> "
            "(Module 02 §2), with no capacity "
            "limit.",
            "<b>And the comparison works because every panel shares "
            "the encoding</b>: <b>the same axes, the same scales, the "
            "same marks</b> — so a reader learns the chart once and "
            "reads it n times.",
            "<b>Which requires the scales to be shared.</b> <b>Panels "
            "with independent axes cannot be compared</b>, and are a "
            "common and self-defeating default in plotting "
            "libraries.",
            "<b>And the ordering of the panels is a free "
            "channel</b> — <b>sort them by something meaningful</b> "
            "and the grid itself carries information "
            "(Module 03 §4's sorting argument)."]},

  {"t": "bullets", "kicker": "Small multiples", "title": "And when they beat a single dense chart",
   "items": [
     "<b>When you have more than five to seven "
     "categories</b> — past colour's capacity "
     "(Module 02 §2).",
     "",
     "<b>When the series overlap</b> and would occlude one "
     "another in a single panel.",
     "",
     "<b>When the task is 'which of these is "
     "different'</b>, which the grid supports directly and a "
     "superimposed chart does not.",
     "",
     "<b>But not when the task is a precise pairwise "
     "comparison</b> — <b>position on unaligned scales is rank "
     "two rather than rank one</b>, so superimposing wins "
     "there.",
     "",
     "<b>Which is the trade:</b> <b>superimpose for precise "
     "comparison, facet for everything else.</b>",
   ],
   "footnote": "<b>Superimpose for precise comparison, facet for "
               "everything else</b> — which follows directly from "
               "ranks one and two of the quantitative "
               "ranking."},

  {"t": "section", "label": "Part 2", "title": "Coordinated views",
   "blurb": "Different encodings of the same data, linked."},

  {"t": "callout", "title": "Several views with linked selection show what no single encoding can",
   "kind": "The technique, and the reason for it",
   "body": ["<b>No single encoding supports every task</b> "
            "(Module 01 §2) — so <b>show several, each "
            "good at a different one, and link the selection between "
            "them.</b>",
            "<b>Which means selecting points in a scatter plot "
            "highlights the same records in a histogram, a map, and a "
            "table</b> — and the reader sees how the selection sits in "
            "every other distribution.",
            "<b>And brushing is the operation that makes it "
            "work:</b> <b>select a region in one view and see the "
            "corresponding marks everywhere else</b>, which answers "
            "'what are those outliers' directly.",
            "<b>With one design requirement:</b> <b>the views must "
            "be visible simultaneously</b> — <b>a linked view behind a "
            "tab is not linked</b>, because the comparison requires both "
            "to be seen at once."]},

  {"t": "code", "kicker": "Vocabulary", "title": "The interaction operations",
   "lang": "text", "code": """
  SELECT      mark a subset, persistently
  BRUSH       select by dragging a region, and see
              the selection reflected in other views
  FILTER      remove data from view, which changes
              the scales unless you fix them
  ZOOM / PAN  change the spatial extent shown
  AGGREGATE   change the level of detail
  REORDER     change the arrangement of a
              categorical axis (Module 03 section 4)
  ENCODE      change the channel assignment itself,
              which is the most powerful and the
              least used

  AND NAVIGATE: overview first, zoom and filter, then
  details on demand -- which is the classical sequence
  and is still the right default for an unfamiliar
  dataset.
""",
   "caption": "<b>Overview first, zoom and filter, details on "
              "demand</b> — the classical sequence, and still the "
              "right default for exploring something unfamiliar.",
   "note": "The vocabulary makes interaction designable rather than "
           "improvised."},

  {"t": "section", "label": "Part 3", "title": "What interaction costs",
   "blurb": "Which is more than it appears."},

  {"t": "bullets", "kicker": "Costs", "title": "The costs, which are usually unstated",
   "items": [
     "<b>Nothing is seen until somebody acts.</b> <b>An "
     "interaction is a question the reader has to think to ask</b>, and "
     "<b>most will not</b> — so the default view carries almost "
     "all of the communication.",
     "",
     "<b>It does not survive the medium.</b> <b>A printed, "
     "pasted, or screenshotted figure is its default state</b>, which "
     "is how most figures are actually seen.",
     "",
     "<b>And discoverability is a real problem</b> — "
     "<b>an unsignified interaction is not there</b> "
     "(CSCE 671 §01 §3).",
     "",
     "<b>Plus the implementation and maintenance cost</b>, which "
     "is large compared with a static figure.",
     "",
     "<b>So: make the default view answer the main "
     "question</b>, and let interaction answer the follow-ups.",
   ],
   "footnote": "<b>Make the default view answer the main question</b> "
               "— because the default is what most readers will ever "
               "see, which is CSCE 671 §05 §3's default "
               "argument."},

  {"t": "callout", "title": "And animation is a weak channel for comparison",
   "kind": "The specific caution",
   "body": ["<b>Animating between two states requires the reader to "
            "remember the first one</b> — which is "
            "CSCE 671 §03 §2's four-chunk limit, and "
            "<b>means an animated transition cannot support a precise "
            "comparison.</b>",
            "<b>So small multiples beat animation for comparing "
            "states</b>, reliably and in measured studies — because "
            "the states are simultaneously visible.",
            "<b>But animation is good for showing a "
            "<i>transition</i></b> — <b>object constancy, so the "
            "reader can follow which mark went where</b>, which no static "
            "figure conveys.",
            "<b>Which gives the rule:</b> <b>animate to show how "
            "something changed, and facet to compare what it "
            "was</b> — two different tasks, and the common mistake is "
            "animating for comparison."]},

  {"t": "section", "label": "Part 4", "title": "Designing it",
   "blurb": "From the task, as always."},

  {"t": "bullets", "kicker": "Design", "title": "How to design a multi-view figure",
   "items": [
     "<b>List the reader's tasks</b>, and <b>assign each to a "
     "view whose encoding suits it</b> — which is "
     "Module 01 §2 applied several times.",
     "",
     "<b>Share the scales where comparison across views is "
     "intended</b>, and say so where they are not shared.",
     "",
     "<b>Link the selection</b>, because an unlinked set of views "
     "is a dashboard rather than a tool.",
     "",
     "<b>Keep the number of views small</b> — four is "
     "already a lot, and each one costs attention "
     "(CSCE 671 §03 §1).",
     "",
     "<b>And test what readers extract</b> "
     "(Module 13), because <b>a multi-view figure is much "
     "easier to misread than a single chart.</b>",
   ],
   "footnote": "<b>An unlinked set of views is a dashboard rather "
               "than a tool</b> — and a dashboard answers whatever "
               "questions its designer anticipated, which is the "
               "limitation worth knowing."},

  {"t": "callout", "title": "And the honest position on dashboards",
   "kind": "Closing",
   "body": ["<b>A dashboard is a set of views chosen in advance for "
            "questions anticipated in advance</b> — which is useful "
            "for monitoring and poor for investigation.",
            "<b>So it answers 'is anything unusual' well and 'why is "
            "this unusual' badly</b>, because the follow-up question was "
            "not anticipated.",
            "<b>Which is why linked selection and the ability to "
            "re-encode matter so much</b> — <b>they are what turn a "
            "dashboard into something you can investigate "
            "with.</b>",
            "<b>And it is CSCE 701 §12's measurement "
            "problem in visual form:</b> <b>the dashboard makes the "
            "measured portion look like the whole</b>, and what was not "
            "charted is invisible rather than absent."]},
 ],
 "takeaways": [
   "Small multiples put the category on spatial region, which is rank one "
   "for categorical data and has no capacity limit.",
   "Panels with independent axes cannot be compared, and that is a common "
   "library default.",
   "Superimpose for precise comparison and facet for everything else, "
   "which follows from ranks one and two.",
   "A linked view behind a tab is not linked, because the comparison "
   "requires both to be visible.",
   "An interaction is a question the reader has to think to ask, and most "
   "will not — so the default view carries the communication.",
   "Animate to show how something changed and facet to compare what it "
   "was; animating for comparison is the common mistake.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Small multiples"),
  ("callout", "Small multiples put a categorical variable on spatial region, "
              "which is the most accurate channel for it",
   ["<b>Repeat the same chart once per category, arranged in a "
    "grid</b> — which puts the categorical variable on spatial "
    "region, <b>rank one for categorical data</b> (Module 02 "
    "&sect;2), <b>with no capacity limit</b> where colour had five to "
    "seven.",
    "<b>And the comparison works because every panel shares the "
    "encoding</b>: <b>the same axes, the same scales, the same mark "
    "type, the same colour</b> — so <b>a reader learns the chart "
    "once and then reads it n times</b>, which is why a grid of twenty "
    "panels is not twenty times the work.",
    "<b>Which requires the scales to be shared.</b> <b>Panels with "
    "independent axes cannot be compared at all</b> — the whole "
    "benefit disappears — and <b>independent scaling is a common and "
    "self-defeating default in plotting libraries</b>, which scale each "
    "facet to its own data.",
    "<b>And the ordering of the panels is a free channel</b> — "
    "<b>sort them by something meaningful</b> rather than "
    "alphabetically, <b>and the grid itself carries information</b> "
    "(Module 03 &sect;4's sorting argument, applied to layout "
    "rather than to an axis)."]),
  ("ul", ["<b>When you have more than five to seven categories</b> "
          "— past colour's capacity (Module 02 &sect;2) — "
          "which is the commonest trigger and the clearest.",
          "<b>When the series overlap substantially</b> and would "
          "occlude one another in a single superimposed panel, making the "
          "lower ones unreadable.",
          "<b>When the reader's task is 'which of these is "
          "different'</b>, <b>which the grid supports directly</b> "
          "— an odd panel is visible at a glance — <b>and a "
          "superimposed chart does not.</b>",
          "<b>But not when the task is a precise pairwise "
          "comparison</b> — <b>position on unaligned scales is rank "
          "two rather than rank one</b> (Module 02 &sect;1), <b>so "
          "superimposing in one panel wins there</b> and the faceting "
          "costs accuracy.",
          "<b>Which is the trade:</b> <b>superimpose for precise "
          "comparison, facet for everything else</b> — and it "
          "<b>follows directly from ranks one and two of the quantitative "
          "ranking</b> rather than from any separate principle, which is "
          "a satisfying consequence of having the ranking."]),

  ("h1", "2 &nbsp; Coordinated views"),
  ("callout", "Several views with linked selection show what no single "
              "encoding can",
   ["<b>No single encoding supports every task</b> (Module 01 "
    "&sect;2's callout) — so <b>show several views, each one good at "
    "a different task, and link the selection between them.</b>",
    "<b>Which means that selecting points in a scatter plot "
    "highlights the same records in a histogram, on a map, and in a "
    "table</b> — and <b>the reader sees how that selection sits "
    "within every other distribution</b>, which is information no single "
    "figure contains.",
    "<b>And brushing is the operation that makes it work:</b> "
    "<b>select a region by dragging in one view and see the corresponding "
    "marks highlighted everywhere else</b>, <b>which answers 'what are "
    "those outliers' directly</b> rather than requiring a separate "
    "query.",
    "<b>With one design requirement that is frequently "
    "violated:</b> <b>the views must be visible simultaneously</b> "
    "— <b>a linked view behind a tab is not linked</b>, because the "
    "comparison requires both to be in view at once and switching "
    "reintroduces the memory demand (CSCE 671 Module 03 "
    "&sect;2)."]),
  ("code", """SELECT      mark a subset, persistently
BRUSH       select by dragging a region, and see the
            selection reflected in the other views
FILTER      remove data from view, which changes the
            scales unless you deliberately fix them
ZOOM / PAN  change the spatial extent shown
AGGREGATE   change the level of detail shown
REORDER     change the arrangement of a categorical
            axis (Module 03 section 4)
ENCODE      change the channel assignment itself,
            which is the most powerful operation and
            the least often provided

AND NAVIGATE: overview first, zoom and filter, then
details on demand -- which is the classical sequence
and is still the right default for an unfamiliar
dataset."""),
  ("p", "<b>Overview first, zoom and filter, details on demand</b> "
        "— Shneiderman's sequence — <b>and it is still the right "
        "default for exploring something unfamiliar</b>, because it "
        "establishes the context before the detail and so prevents reading "
        "a subset as the whole. <b>The vocabulary makes interaction "
        "designable rather than improvised</b>: 'add brushing between "
        "these two views' is a specification, where 'make it interactive' "
        "is not. <b>And note that filter changes the scales unless you "
        "fix them</b>, which silently breaks comparison across filter "
        "states."),

  ("break",),
  ("h1", "3 &nbsp; What interaction costs"),
  ("ul", ["<b>Nothing is seen until somebody acts.</b> <b>An "
          "interaction is a question the reader has to think to ask</b>, "
          "and <b>most readers will not ask it</b> — <b>so the "
          "default view carries almost all of the communication</b>, "
          "whatever else is available.",
          "<b>It does not survive the medium.</b> <b>A printed, "
          "pasted, screenshotted, or embedded-in-a-slide figure is its "
          "default state</b> — <b>which is how most figures are "
          "actually seen</b>, regardless of where they were "
          "published.",
          "<b>And discoverability is a real problem</b> — <b>an "
          "unsignified interaction is not there</b> at all for anybody "
          "who does not try it (CSCE 671 Module 01 &sect;3's "
          "signifier argument).",
          "<b>Plus the implementation and maintenance cost</b>, which "
          "is substantial compared with a static figure — and which "
          "includes keeping the interaction working as the data and the "
          "platform change.",
          "<b>So: make the default view answer the main "
          "question</b>, and let the interaction answer the follow-up "
          "questions. <b>Make the default view answer the main "
          "question</b> — <b>because the default is what most "
          "readers will ever see</b>, which is <b>CSCE 671 Module 05 "
          "&sect;3's default-dominance argument</b> arriving in this "
          "subject."]),
  ("callout", "And animation is a weak channel for comparison",
   ["<b>Animating between two states requires the reader to hold the "
    "first state in memory while seeing the second</b> — which is "
    "<b>CSCE 671 Module 03 &sect;2's four-chunk limit</b>, and "
    "<b>means an animated transition cannot support a precise "
    "comparison</b> of more than a few marks.",
    "<b>So small multiples beat animation for comparing states</b>, "
    "reliably and in measured studies — <b>because the states are "
    "simultaneously visible</b> and the comparison becomes a spatial "
    "judgement rather than a memory one.",
    "<b>But animation is genuinely good for showing a "
    "<i>transition</i></b> — <b>object constancy, so that the reader "
    "can follow which particular mark moved where</b> — <b>which no "
    "static figure conveys</b> and which matters when the identity of the "
    "moving items is the point.",
    "<b>Which gives a clean rule:</b> <b>animate to show how "
    "something changed, and facet to compare what it was</b> — "
    "<b>two different tasks, and the common mistake is animating for "
    "comparison</b>, which looks impressive and communicates less than a "
    "grid."]),

  ("h1", "4 &nbsp; Designing it"),
  ("ul", ["<b>List the reader's tasks</b>, and <b>assign each one to "
          "a view whose encoding suits it</b> — which is "
          "<b>Module 01 &sect;2 applied several times over</b> rather "
          "than a new principle.",
          "<b>Share the scales wherever comparison across views is "
          "intended</b>, and <b>say so explicitly where they are not "
          "shared</b> — since a reader will assume they are and "
          "compare anyway.",
          "<b>Link the selection</b>, because <b>an unlinked set of "
          "views is a dashboard rather than a tool</b> (see the "
          "closing callout) and loses the main benefit of having several "
          "views at all.",
          "<b>Keep the number of views small</b> — <b>four is "
          "already a lot</b>, and <b>each one costs attention</b> that is "
          "then unavailable for the data (CSCE 671 Module 03 "
          "&sect;1).",
          "<b>And test what readers actually extract</b> "
          "(Module 13), because <b>a multi-view figure is very much "
          "easier to misread than a single chart</b> — readers "
          "misattribute selections, miss the linking, and compare across "
          "unshared scales. <b>An unlinked set of views is a dashboard "
          "rather than a tool</b>, and <b>a dashboard answers whatever "
          "questions its designer anticipated</b>, which is the "
          "limitation worth knowing before building one."]),
  ("callout", "And the honest position on dashboards",
   ["<b>A dashboard is a set of views chosen in advance for questions "
    "anticipated in advance</b> — <b>which is genuinely useful for "
    "monitoring and poor for investigation</b>, and those are different "
    "activities that get conflated.",
    "<b>So it answers 'is anything unusual' well and 'why is this "
    "unusual' badly</b>, <b>because the follow-up question was not "
    "anticipated</b> and the dashboard cannot be re-encoded to address "
    "it.",
    "<b>Which is exactly why linked selection and the ability to "
    "re-encode matter so much</b> — <b>they are what turn a "
    "dashboard into something you can actually investigate with</b>, and "
    "the ENCODE operation in &sect;2's vocabulary is the most powerful "
    "and least often provided for this reason.",
    "<b>And it is CSCE 701 Module 12's measurement problem in "
    "visual form:</b> <b>the dashboard makes the measured portion look "
    "like the whole</b>, and <b>what was not charted is invisible rather "
    "than absent</b> — which is why a dashboard needs a statement of "
    "what it does not show, exactly as a metrics programme does."]),
 ],
 "resources": [
   ("Munzner, chapters 12 through 14 (slides free)",
    "https://www.cs.ubc.ca/~tmm/vadbook/",
    "<b>&sect;1 and &sect;2</b> — faceting, superimposing, and the "
    "view coordination design space."),
   ("Shneiderman &mdash; The Eyes Have It (free)",
    "https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf",
    "<b>&sect;2's task taxonomy and the overview-first sequence</b>, in "
    "the original."),
   ("Robertson et al. &mdash; Effectiveness of Animation in Trend "
    "Visualization (free)",
    "https://ieeexplore.ieee.org/document/4658136",
    "<b>&sect;3's callout, measured</b> — small multiples against "
    "animation for comparison, with the numbers."),
   ("Heer & Shneiderman &mdash; Interactive Dynamics for Visual "
    "Analysis (free)",
    "https://queue.acm.org/detail.cfm?id=2146416",
    "<b>&sect;2's vocabulary</b>, organised as a taxonomy of interaction "
    "operations."),
 ],
 "exercises": [
   "<b>Facet a chart by a ten-category variable</b>, and compare "
   "against colouring by it.",
   "<b>Let the facets scale independently</b> and show that the "
   "comparison breaks.",
   "<b>Sort the facets meaningfully</b> and report what the ordering "
   "now conveys.",
   "<b>Find a task where superimposing beats faceting</b>, and "
   "justify it from the ranking.",
   "<b>Build two linked views with brushing</b>, and use them to "
   "identify an outlier's other properties.",
   "<b>Put one view behind a tab</b> and report what is lost.",
   "<b>Show the same comparison as an animation and as small "
   "multiples</b>, and test five readers on accuracy.",
   "<b>Make an interactive figure's default state answer the main "
   "question</b>, and screenshot it to check.",
   "<b>Count the views in a dashboard you use</b>, and list the "
   "questions it cannot answer.",
   "<b>Add a re-encode control</b> to one figure, and see whether anybody "
   "uses it.",
 ],
 "selfcheck": [
   "Why do small multiples work so well?",
   "What do they require, and what is the common library default that "
   "breaks it?",
   "When do small multiples beat a dense chart, and when not?",
   "State the superimpose-or-facet rule and its basis.",
   "What do coordinated views provide, and what is brushing?",
   "Why is a linked view behind a tab not linked?",
   "Name seven interaction operations and the classical sequence.",
   "Give four costs of interaction, and what follows for the default "
   "view.",
   "Why is animation weak for comparison and good for transition?",
   "What is a dashboard good and bad at, and what makes it "
   "investigable?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Networks and Hierarchies",
 "subtitle": "Structure the plane does not naturally hold.",
 "question": "How do you draw a graph nobody can read?",
 "outcomes": [
     "Explain node-link layout and its limits.",
     "Explain the matrix alternative and its trade.",
     "Explain hierarchy layouts and what each preserves.",
     "Explain when a network should not be drawn at all.",
     "Choose a representation from the task.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Node-link",
   "blurb": "The obvious representation, and it scales badly."},

  {"t": "callout", "title": "A force-directed layout has no principled reading, and it is the default everywhere",
   "kind": "The honest position on the familiar picture",
   "body": ["<b>The layout minimises an energy function with no "
            "relationship to the data's meaning</b> — so <b>position "
            "encodes nothing</b>, which wastes the highest-ranked channel "
            "entirely (Module 02 §1).",
            "<b>And it is non-deterministic:</b> <b>two runs give "
            "different pictures of the same graph</b>, which means any "
            "apparent cluster may be an artefact of the "
            "initialisation.",
            "<b>Beyond a few hundred nodes it becomes a hairball</b> "
            "— <b>a dense region conveying only that the graph is "
            "dense</b>, which is a fact better stated as a number.",
            "<b>But it is genuinely good for small graphs where the "
            "topology is the point</b> — up to perhaps a hundred "
            "nodes, where the reader can trace paths and see the "
            "structure."]},

  {"t": "bullets", "kicker": "Node-link", "title": "And what makes one readable",
   "items": [
     "<b>Few enough nodes to trace</b> — which is the "
     "binding constraint, and is roughly one to two "
     "hundred.",
     "",
     "<b>Position encoding something, where you can.</b> <b>A "
     "layered layout for a DAG, or geography, or a computed "
     "attribute</b> — all better than a force layout's "
     "nothing.",
     "",
     "<b>Minimal edge crossings</b>, which is what most layout "
     "algorithms actually optimise and is measurably "
     "helpful.",
     "",
     "<b>And a deterministic layout</b>, so the picture is stable "
     "across runs and comparable across versions.",
     "",
     "<b>Which together mean: use a force layout for "
     "exploration and something principled for publication.</b>",
   ],
   "footnote": "<b>A force layout for exploration and something "
               "principled for publication</b> — because a figure "
               "that changes between runs cannot support a claim about "
               "structure."},

  {"t": "section", "label": "Part 2", "title": "The matrix",
   "blurb": "Which trades path-following for density reading."},

  {"t": "callout", "title": "An adjacency matrix scales where node-link does not, and loses path-following",
   "kind": "The trade, stated directly",
   "body": ["<b>Rows and columns are nodes; a cell encodes an "
            "edge</b> — so <b>the layout is deterministic, there is "
            "no occlusion, and it scales to thousands of nodes "
            "legibly.</b>",
            "<b>And the row and column ordering is the "
            "design</b> — <b>a well-ordered matrix makes clusters "
            "appear as blocks on the diagonal</b>, which is a readable "
            "and quantitative view of community structure "
            "(CSCE 676 §07 §3).",
            "<b>While an alphabetically ordered matrix shows "
            "nothing</b>, which is Module 03 §4's sorting "
            "point with unusually high stakes.",
            "<b>But you cannot trace a path in a matrix</b> — "
            "<b>following a three-hop connection requires three separate "
            "lookups</b>, which is the task node-link does well and the "
            "matrix does not at all."]},

  {"t": "table", "kicker": "Choosing", "title": "Which representation, by task",
   "header": ["Task", "Use", "Why"],
   "widths": [2.9, 3.4, 5.1],
   "rows": [
     ["<b>Trace a path</b>", "<b>Node-link</b>", "<b>The matrix requires a lookup per hop</b>"],
     ["<b>Find clusters</b>", "<b>Ordered matrix</b>", "<b>Blocks on the diagonal, quantitatively</b>"],
     ["<b>Find a high-degree node</b>", "<b>Either, or a bar chart</b>", "<b>Degree is a value; a chart beats both</b>"],
     ["<b>Judge overall density</b>", "<b>Matrix, or a number</b>", "<b>A hairball conveys only density</b>"],
     ["<b>Compare two graphs</b>", "<b>Matrices, same ordering</b>", "<b>Node-link layouts are not comparable</b>"],
   ],
   "footnote": "<b>Several network questions are better answered by a "
               "non-network chart</b> — degree distribution, "
               "centrality ranking, and component sizes are all "
               "quantitative and belong on position "
               "(Module 02 §1).",
   "note": "The don't-draw-the-graph option is underused and belongs "
           "in the table."},

  {"t": "section", "label": "Part 3", "title": "Hierarchies",
   "blurb": "Which have more options and clearer trades."},

  {"t": "bullets", "kicker": "Hierarchies", "title": "The layouts, and what each preserves",
   "items": [
     "<b>A node-link tree</b> — depth on position, which "
     "<b>makes the structure clearest</b> and uses space "
     "poorly for wide trees.",
     "",
     "<b>An icicle or sunburst</b> — depth on position and "
     "size on length or angle, which <b>shows structure and "
     "quantity together.</b>",
     "",
     "<b>A treemap</b> — quantity on area, which "
     "<b>uses space efficiently and reads the quantity badly</b> "
     "(rank five) and the structure worse.",
     "",
     "<b>And an indented list</b>, which is a node-link tree with "
     "better space efficiency and no visual "
     "overview.",
     "",
     "<b>So: a tree for structure, an icicle for both, and a "
     "treemap only when the space constraint dominates.</b>",
   ],
   "footnote": "<b>A treemap puts quantity on area, which is rank "
               "five</b> — so it is chosen for space efficiency and "
               "pays for it in reading accuracy, which should be a "
               "deliberate trade."},

  {"t": "section", "label": "Part 4", "title": "When not to draw it",
   "blurb": "Which is more often than it is done."},

  {"t": "callout", "title": "Most network questions are about a derived quantity, which belongs on a quantitative chart",
   "kind": "The conclusion of the module",
   "body": ["<b>The degree distribution, the centrality ranking, the "
            "component sizes, the clustering coefficient, and the path "
            "length distribution are all numbers</b> "
            "(CSCE 676 §07) — and <b>numbers go on "
            "position, which is rank one.</b>",
            "<b>So a degree distribution on log-log axes answers "
            "'is this heavy-tailed' far better than any picture of the "
            "graph</b>, and a sorted bar chart answers 'who is central' "
            "better than a layout.",
            "<b>Which means the network diagram is for the questions "
            "that are genuinely topological</b> — 'how are these "
            "connected', 'is there a path', 'what does this "
            "neighbourhood look like'.",
            "<b>And a hairball is a strong signal that the question "
            "was not topological</b> — <b>it is a figure that "
            "survived the choice of representation without passing "
            "it.</b>"]},

  {"t": "bullets", "kicker": "Practice", "title": "So, in order",
   "items": [
     "<b>State the question</b>, and check whether it is about "
     "the topology or about a derived quantity.",
     "",
     "<b>If it is a quantity, plot the quantity</b> — which "
     "is Module 03 §3's derivation argument applied to "
     "graphs.",
     "",
     "<b>If it is topological and the graph is small, use "
     "node-link</b> with a principled layout.",
     "",
     "<b>If it is topological and the graph is large, use an "
     "ordered matrix</b>, or <b>extract and draw the relevant "
     "subgraph.</b>",
     "",
     "<b>And if none of those work, say that the graph is too "
     "large to show</b> — which is an honest finding rather than a "
     "failure.",
   ],
   "footnote": "<b>'Too large to show' is an honest finding</b> "
               "— and the alternative is a figure that implies a "
               "structure nobody can verify."},
 ],
 "takeaways": [
   "A force-directed layout has no principled reading, so position encodes "
   "nothing and the highest-ranked channel is wasted.",
   "It is non-deterministic, so any apparent cluster may be an artefact of "
   "the initialisation.",
   "An adjacency matrix is deterministic and scales, and the row ordering "
   "is the design — clusters appear as diagonal blocks.",
   "You cannot trace a path in a matrix, which is the task node-link does "
   "well.",
   "A treemap puts quantity on area, which is rank five, so it is a "
   "deliberate trade for space efficiency.",
   "A hairball is a strong signal that the question was not topological in "
   "the first place.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Node-link"),
  ("callout", "A force-directed layout has no principled reading, and it is "
              "the default everywhere",
   ["<b>The layout minimises a physical energy function that has no "
    "relationship to the data's meaning</b> — springs on edges, "
    "repulsion between nodes — so <b>position encodes nothing in "
    "particular</b>, <b>which wastes the highest-ranked channel "
    "entirely</b> (Module 02 &sect;1).",
    "<b>And it is non-deterministic:</b> <b>two runs produce different "
    "pictures of the same graph</b>, which means <b>any apparent cluster "
    "may be an artefact of the random initialisation</b> rather than a "
    "feature of the data — and the reader cannot tell which.",
    "<b>Beyond a few hundred nodes it becomes a hairball</b> — "
    "<b>a dense region conveying only the fact that the graph is "
    "dense</b>, <b>which is a fact better stated as a number</b> "
    "(&sect;4).",
    "<b>But it is genuinely good for small graphs where the topology "
    "is the point</b> — up to perhaps a hundred nodes, where <b>the "
    "reader can trace paths, see the neighbourhoods, and perceive the "
    "structure</b>, which is a real capability no other representation "
    "offers."]),
  ("ul", ["<b>Few enough nodes to trace</b> — <b>which is the "
          "binding constraint</b>, and is roughly one to two hundred "
          "depending on the edge density.",
          "<b>Position encoding something, wherever you can arrange "
          "it.</b> <b>A layered layout for a directed acyclic graph, "
          "geographic position for a spatial network, or a computed "
          "attribute on one axis</b> — all of which are better than "
          "a force layout's nothing.",
          "<b>Minimal edge crossings</b>, <b>which is what most layout "
          "algorithms actually optimise</b> and <b>is measurably "
          "helpful</b> for path tracing, which is the task node-link is "
          "for.",
          "<b>And a deterministic layout</b>, so that <b>the picture "
          "is stable across runs and comparable across versions of the "
          "data</b> — which matters for anything that will be "
          "regenerated.",
          "<b>Which together mean: use a force layout for exploration "
          "and something principled for publication.</b> <b>A figure "
          "that changes between runs cannot support a claim about "
          "structure</b>, which is <b>CSCE 676 Module 04 &sect;3's "
          "stability argument</b> arriving as a visualisation "
          "requirement."]),

  ("h1", "2 &nbsp; The matrix"),
  ("callout", "An adjacency matrix scales where node-link does not, and "
              "loses path-following",
   ["<b>Rows and columns are the nodes; each cell encodes the presence "
    "or weight of an edge</b> — so <b>the layout is entirely "
    "deterministic, there is no occlusion whatsoever, and it scales to "
    "thousands of nodes while remaining legible.</b>",
    "<b>And the row and column ordering is the design</b> — <b>a "
    "well-ordered matrix makes clusters appear as solid blocks along the "
    "diagonal</b>, <b>which is a readable and quantitative view of "
    "community structure</b> (CSCE 676 Module 07 &sect;3) and shows "
    "the between-cluster density too.",
    "<b>While an alphabetically ordered matrix shows nothing at "
    "all</b> — the same data, unreadable — <b>which is "
    "Module 03 &sect;4's sorting point with unusually high "
    "stakes</b>: the ordering is not a refinement here but the entire "
    "difference between a useful figure and noise.",
    "<b>But you cannot trace a path in a matrix</b> — "
    "<b>following a three-hop connection requires three separate lookups "
    "in different parts of the figure</b> — <b>which is exactly the "
    "task node-link does well and the matrix does not do at all.</b>"]),
  ("table", ["The task", "Use", "Why"],
   [["<b>Trace a path between two nodes</b>", "<b>Node-link</b>",
     "<b>The matrix requires a separate lookup per hop</b> "
     "(&sect;2)."],
    ["<b>Find clusters</b>", "<b>An ordered matrix</b>",
     "<b>Blocks on the diagonal, read quantitatively</b> rather than "
     "guessed from a layout."],
    ["<b>Find the high-degree nodes</b>",
     "<b>Either, or a bar chart</b>",
     "<b>Degree is a value, and a sorted bar chart beats both network "
     "views</b> (&sect;4)."],
    ["<b>Judge the overall density</b>", "<b>A matrix, or a number</b>",
     "<b>A hairball conveys only density</b>, so report the number."],
    ["<b>Compare two graphs</b>",
     "<b>Matrices with the same ordering</b>",
     "<b>Node-link layouts of two graphs are not comparable at "
     "all</b> (&sect;1's non-determinism)."]],
   [0.24, 0.28, 0.48]),
  ("p", "<b>Several network questions are better answered by a "
        "non-network chart</b> — the degree distribution, the "
        "centrality ranking, and the component sizes are all quantitative "
        "and <b>belong on position</b> (Module 02 &sect;1). <b>The "
        "don't-draw-the-graph option is underused and belongs in the "
        "table</b>, which is why &sect;4 develops it."),

  ("break",),
  ("h1", "3 &nbsp; Hierarchies"),
  ("ul", ["<b>A node-link tree</b> — depth encoded on position, "
          "which <b>makes the structure clearest of any option</b> and "
          "<b>uses space poorly for wide or deep trees</b>, since most of "
          "the canvas is empty.",
          "<b>An icicle plot or a sunburst</b> — depth on "
          "position and quantity on length (icicle) or angle "
          "(sunburst) — which <b>shows the structure and the "
          "quantity together</b>, and is the best general compromise. "
          "<b>Prefer the icicle, since length is rank three and angle is "
          "rank four.</b>",
          "<b>A treemap</b> — quantity on area, nesting on "
          "containment — which <b>uses space very efficiently and "
          "reads the quantity badly (rank five) and the structure worse "
          "still</b>, since deep nesting becomes invisible.",
          "<b>And an indented list</b>, which is a node-link tree with "
          "much better space efficiency and <b>no visual overview</b> "
          "— excellent for navigation and poor for seeing the "
          "shape.",
          "<b>So: a tree for structure, an icicle for structure and "
          "quantity together, and a treemap only when the space "
          "constraint genuinely dominates.</b> <b>A treemap puts "
          "quantity on area, which is rank five</b> — <b>so it is "
          "chosen for space efficiency and pays for it in reading "
          "accuracy</b>, and that should be a deliberate trade rather "
          "than a default."]),

  ("h1", "4 &nbsp; When not to draw it"),
  ("callout", "Most network questions are about a derived quantity, which "
              "belongs on a quantitative chart",
   ["<b>The degree distribution, the centrality ranking, the connected "
    "component sizes, the clustering coefficient, and the path length "
    "distribution are all numbers</b> (CSCE 676 Module 07's whole "
    "subject) — and <b>numbers go on position, which is rank "
    "one.</b>",
    "<b>So a degree distribution on log-log axes answers 'is this "
    "heavy-tailed' far better than any picture of the graph</b> "
    "(CSCE 676 Module 07 &sect;1), and <b>a sorted bar chart "
    "answers 'who is most central' better than any layout</b>, including "
    "one that sizes nodes by centrality.",
    "<b>Which means the network diagram is for the questions that are "
    "genuinely topological</b> — 'how are these two connected', 'is "
    "there a path', 'what does this particular neighbourhood look "
    "like' — and those are a minority of the questions people bring "
    "to a graph.",
    "<b>And a hairball is a strong signal that the question was not "
    "topological in the first place</b> — <b>it is a figure that "
    "survived the choice of representation without ever passing "
    "through it</b>, which is the diagnosis to make when you see "
    "one."]),
  ("ul", ["<b>State the question</b>, and <b>check whether it is about "
          "the topology or about a derived quantity</b> — which takes "
          "a sentence and decides the rest.",
          "<b>If it is a quantity, plot the quantity</b> — which "
          "is <b>Module 03 &sect;3's derivation argument applied to "
          "graphs</b>, and is the step most often skipped because the "
          "graph feels like the natural object.",
          "<b>If it is topological and the graph is small, use "
          "node-link</b> with a principled and deterministic layout "
          "(&sect;1).",
          "<b>If it is topological and the graph is large, use an "
          "ordered matrix</b> (&sect;2), or <b>extract the relevant "
          "subgraph and draw that</b> — a neighbourhood of fifty "
          "nodes is readable where the whole graph is not.",
          "<b>And if none of those work, say that the graph is too "
          "large to show</b> — <b>which is an honest finding rather "
          "than a failure</b>, and <b>the alternative is a figure that "
          "implies a structure nobody can verify</b>, which is "
          "Module 13's concern."]),
 ],
 "resources": [
   ("Munzner, chapter 9 (slides free)",
    "https://www.cs.ubc.ca/~tmm/vadbook/",
    "<b>&sect;1 through &sect;3</b> — node-link, matrix, and the "
    "hierarchy layouts, with the trades stated."),
   ("Ghoniem, Fekete & Castagliola &mdash; Node-link vs matrix (free)",
    "https://ieeexplore.ieee.org/document/1382882",
    "<b>&sect;2's trade, measured</b> — which tasks each "
    "representation wins, with the crossover point."),
   ("Behrisch et al. &mdash; Matrix reordering methods (free)",
    "https://onlinelibrary.wiley.com/doi/10.1111/cgf.12935",
    "<b>&sect;2's ordering, surveyed</b> — the methods, since the "
    "ordering is the whole design."),
   ("Shneiderman &mdash; Tree-maps (free)",
    "https://www.cs.umd.edu/hcil/treemap-history/",
    "<b>&sect;3's treemap in the original</b>, with the space-filling "
    "motivation that justifies the area encoding."),
 ],
 "exercises": [
   "<b>Run a force layout twice</b> on the same graph and compare the "
   "pictures.",
   "<b>Identify an apparent cluster</b> and check whether it survives a "
   "re-run.",
   "<b>Draw a 500-node graph</b> as node-link and report what you can "
   "read.",
   "<b>Draw the same graph as an alphabetically ordered matrix</b>, then "
   "reorder by a clustering.",
   "<b>Trace a three-hop path</b> in each, and time it.",
   "<b>Plot the degree distribution</b> and compare what it tells you "
   "against the node-link figure.",
   "<b>Draw a hierarchy as a tree, an icicle, and a treemap</b>, and ask "
   "five people to compare two sizes.",
   "<b>Find a published hairball</b> and state the question it was "
   "probably meant to answer.",
   "<b>Answer that question with a non-network chart.</b>",
   "<b>Extract a neighbourhood subgraph</b> and draw that instead.",
 ],
 "selfcheck": [
   "Why does a force layout have no principled reading?",
   "Why does non-determinism matter for a structural claim?",
   "Give four things that make a node-link diagram readable.",
   "State the matrix trade in both directions.",
   "Why is the matrix ordering the whole design?",
   "Give the representation for five network tasks.",
   "Name four hierarchy layouts and what each preserves.",
   "Why is a treemap a deliberate trade?",
   "Which network questions belong on a quantitative chart?",
   "What does a hairball signal?",
 ],
},

]
