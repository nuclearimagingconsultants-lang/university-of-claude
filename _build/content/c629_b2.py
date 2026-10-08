# -*- coding: utf-8 -*-
"""CSCE 629 — Modules 03-06."""

MODULES = [

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Randomization and Expectation",
 "subtitle": "Buying worst-case robustness with coin flips.",
 "question": "Why does adding randomness make an algorithm more reliable?",
 "outcomes": [
     "Explain why expected-case beats average-case as a guarantee.",
     "Use linearity of expectation, including on dependent variables.",
     "Analyse randomised quicksort and randomised selection.",
     "Distinguish Las Vegas from Monte Carlo algorithms.",
     "Apply concentration bounds to argue that deviation is unlikely.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why randomise at all",
   "blurb": "Not to be faster on average — to remove the adversary."},

  {"t": "callout", "title": "The real argument for randomisation",
   "kind": "Key idea",
   "body": ["Every deterministic algorithm has a worst case, and the worst "
            "case is a <i>fixed input</i>. Anyone who knows your code can "
            "construct it.",
            "Deterministic quicksort using the first element as pivot is "
            "Θ(n²) on sorted input — which is not an exotic "
            "case, it is the single most common shape of real data.",
            "Randomise the pivot and the bad case still exists, but it now "
            "depends on <i>your coins</i>, which the adversary cannot see. "
            "The guarantee moves from 'fast unless the input is bad' to "
            "'fast with overwhelming probability, on every input'.",
            "You have not removed the worst case. You have made it "
            "unreachable on purpose."]},

  {"t": "two", "kicker": "Two guarantees", "title": "Average case and expected case",
   "lh": "Average case",
   "l": ["Averages over a distribution of <b>inputs</b>.",
         "Requires an assumption about your data.",
         "Real data is rarely uniform — sorted, nearly sorted, and "
         "heavily duplicated inputs are everywhere.",
         ("An adversary just supplies an input outside the distribution.", 1)],
   "rh": "Expected case",
   "r": ["Averages over the algorithm's own <b>coin flips</b>.",
         "Holds for <b>every</b> input, with no assumption.",
         "The adversary cannot see your randomness, so cannot target it.",
         ("Strictly stronger. This is what randomisation buys.", 1)],
   "note": "This distinction is the single most important idea in the module "
           "and is routinely blurred in textbooks."},

  {"t": "table", "kicker": "Taxonomy", "title": "Las Vegas and Monte Carlo",
   "header": ["Type", "Correctness", "Running time", "Example"],
   "widths": [2.6, 3.2, 3.2, 3.1],
   "rows": [
     ["Las Vegas", "Always correct", "Random", "Randomised quicksort"],
     ["Monte Carlo", "Probably correct", "Bounded", "Primality testing"],
   ],
   "note": "Mnemonic: in Las Vegas you always get the right answer but you "
           "do not know when; with Monte Carlo you finish on time but might "
           "be wrong."},

  {"t": "section", "label": "Part 2", "title": "Linearity of expectation",
   "blurb": "The most useful tool in the module, and the one people "
            "distrust."},

  {"t": "eq", "kicker": "The tool", "title": "Linearity, stated",
   "eqs": [
     ("E[X + Y]  =  E[X] + E[Y]",
      "<b>Always.</b> No independence required. This is the surprising part."),
     ("E[cX]  =  c·E[X]",
      "Scaling passes through."),
     ("X = Σ Xᵢ with Xᵢ indicator  ⇒  E[X] = Σ Pr[eventᵢ]",
      "The standard move: decompose a count into indicators."),
   ],
   "caption": "Decompose the quantity you want into a sum of indicator "
              "variables, compute each probability separately, and add. "
              "Dependence between them does not matter.",
   "note": "Students expect independence to be required and it genuinely is "
           "not. Worth stating twice."},

  {"t": "code", "kicker": "Worked", "title": "Expected comparisons in quicksort",
   "lang": "text", "code": """
Let X_ij = 1 if elements of rank i and j are ever compared, else 0.
Total comparisons X = sum over i<j of X_ij.

By linearity:   E[X] = sum over i<j of Pr[i and j are compared]

When ARE ranks i and j compared?
  Consider the set S = {i, i+1, ..., j}, of size j-i+1.
  The first pivot chosen from S decides everything:
    - if it is i or j  -> they are compared (once)
    - otherwise        -> they are split apart, never compared

  Each element of S is equally likely to be the first pivot chosen.
    Pr[compared] = 2 / (j - i + 1)

E[X] = sum_{i<j} 2/(j-i+1)  =  2n * H_n  ~  1.39 n log2 n
""",
   "caption": "No independence was assumed anywhere — the Xᵢⱼ "
              "are heavily dependent. Linearity does not care.",
   "note": "Walk the 'first pivot from S' argument slowly. It is the elegant "
           "step and it generalises to several later proofs."},

  {"t": "section", "label": "Part 3", "title": "Two algorithms",
   "blurb": "Quicksort and selection, analysed properly."},

  {"t": "table", "kicker": "Quicksort", "title": "Why it wins despite a worse bound",
   "header": ["", "Mergesort", "Randomised quicksort"],
   "widths": [3.3, 4.4, 4.4],
   "rows": [
     ["Worst case", "Θ(n log n)", "Θ(n²), probability ~0"],
     ["Expected", "Θ(n log n)", "Θ(n log n)"],
     ["Extra memory", "Θ(n)", "Θ(log n) stack"],
     ["Memory access", "Two arrays, strided", "In place, sequential"],
     ["In practice", "Predictable", "<b>Usually faster</b>"],
   ],
   "note": "The decisive row is memory access, not the complexity rows. "
           "Module 01's point, made concrete."},

  {"t": "bullets", "kicker": "Selection", "title": "Finding the k-th smallest in Θ(n)",
   "items": [
     "Quickselect: partition as in quicksort, but recurse into <b>one</b> "
     "side only.",
     "",
     "T(n) = T(n/2) + Θ(n) in expectation → <b>Θ(n)</b>.",
     ("The geometric series sums to a constant times n.", 1),
     ("Compare mergesort's T(n) = 2T(n/2) + Θ(n) → n log n. One "
      "recursive call instead of two removes the log.", 1),
     "",
     "Deterministic Θ(n) selection exists — median of medians.",
     ("Beautiful, and slower than quickselect on every real input. The "
      "constant is enormous.", 1),
   ],
   "footnote": "A good example of a result worth knowing and not worth using.",
   "note": "Tie back to Module 02: one subproblem versus two is exactly the "
           "binary-search-versus-mergesort contrast."},

  {"t": "section", "label": "Part 4", "title": "Concentration",
   "blurb": "Expectation alone is a weak statement. These make it strong."},

  {"t": "eq", "kicker": "Bounds", "title": "Three bounds, increasing in strength",
   "eqs": [
     ("Markov:  Pr[X ≥ a] ≤ E[X]/a",
      "Needs only non-negativity. Very weak, but assumes almost nothing."),
     ("Chebyshev:  Pr[|X − μ| ≥ kσ] ≤ 1/k²",
      "Needs the variance. Polynomial decay."),
     ("Chernoff:  Pr[X ≥ (1+δ)μ] ≤ e^(−δ²μ/3)",
      "Needs independent bounded variables. <b>Exponential</b> decay."),
   ],
   "caption": "Chernoff is why randomised algorithms are trustworthy: the "
              "probability of being far from the mean falls off "
              "exponentially, not polynomially.",
   "note": "The practical upshot: 'expected O(n log n)' plus a Chernoff bound "
           "means the bad case effectively never happens, not merely rarely."},

  {"t": "callout", "title": "What 'with high probability' actually buys",
   "kind": "Perspective",
   "body": ["Randomised quicksort exceeds c·n log n comparisons with "
            "probability smaller than 1/n² for a modest c.",
            "At n = 10⁶ that is a probability below 10⁻¹² "
            "— comfortably less likely than the machine suffering an "
            "undetected memory error during the sort.",
            "At that point the worst case has stopped being an engineering "
            "concern. That is the practical content of a concentration bound."]},

  {"t": "bullets", "kicker": "Elsewhere", "title": "Where randomisation shows up again",
   "items": [
     "<b>Hashing</b> — a random hash function defeats adversarial keys "
     "(Module 05).",
     "<b>Treaps and skip lists</b> — balance by randomness instead of "
     "rotation logic.",
     "<b>Min-cut</b> — Karger's contraction algorithm, which is almost "
     "absurdly simple.",
     "<b>Primality</b> — Miller–Rabin, the basis of practical "
     "cryptography.",
     "<b>Sketching and streaming</b> — approximate answers in sublinear "
     "space (CSCE 727).",
     "<b>Monte Carlo rendering</b> — the whole of CSCE 647 is estimating "
     "an integral by sampling.",
   ],
   "note": "The rendering connection matters for this student: path tracing "
           "is importance-sampled Monte Carlo integration, and the variance "
           "reasoning here is the same reasoning."},
 ],
 "takeaways": [
   "Randomisation does not remove the worst case; it makes the worst case "
   "depend on your coins rather than on the input, so no adversary can reach "
   "it.",
   "Expected case holds for every input. Average case holds only if your "
   "distributional assumption does. The first is strictly stronger.",
   "Linearity of expectation needs no independence. Decompose into "
   "indicators, sum the probabilities.",
   "Quicksort's expected 1.39 n log₂ n comparisons come from a one-line "
   "observation about which pivot in a range is chosen first.",
   "Recursing into one side instead of two turns n log n into n — that "
   "is quickselect.",
   "Chernoff bounds give exponential decay, which is what turns 'expected' "
   "into 'effectively guaranteed'.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The case for randomisation"),
  ("p", "The usual explanation — that randomised algorithms are faster "
        "on average — is not the real argument, and it understates what "
        "is going on."),
  ("p", "Every deterministic algorithm has a worst case, and that worst case "
        "is a specific input. If the algorithm is public, the input is "
        "constructible. Deterministic quicksort taking the first element as "
        "pivot degrades to &Theta;(n&#178;) on already-sorted data, which is "
        "not an obscure adversarial construction — it is the most common "
        "shape real data takes."),
  ("callout", "What randomisation actually changes",
   ["After randomising the pivot, the &Theta;(n&#178;) behaviour still "
    "exists. But it is no longer a property of the <i>input</i>; it is a "
    "property of an unlucky sequence of <i>your own coin flips</i>.",
    "An adversary who knows your source code, your compiler, and your entire "
    "input history still cannot construct a slow case, because they cannot "
    "predict your randomness.",
    "The guarantee changes from <i>fast unless the input is adversarial</i> "
    "to <i>fast with overwhelming probability, on every input</i>. That is a "
    "qualitative difference, and it is why randomisation is used in practice "
    "far beyond its speed benefits."]),
  ("h2", "1.1 &nbsp; Las Vegas and Monte Carlo"),
  ("table", ["", "Las Vegas", "Monte Carlo"],
   [["Answer", "Always correct", "Correct with probability &ge; p"],
    ["Running time", "A random variable", "Bounded deterministically"],
    ["Example", "Randomised quicksort, quickselect",
     "Miller&ndash;Rabin primality, Karger min-cut"],
    ["Error handling", "Wait longer",
     "Repeat and take a majority / any success — error falls "
     "exponentially in the number of repeats"]],
   [0.17, 0.35, 0.48]),

  ("h1", "2 &nbsp; Linearity of expectation"),
  ("eq", "E[X + Y] = E[X] + E[Y] &nbsp;&nbsp; for <i>any</i> X, Y"),
  ("p", "No independence is required. This is worth stating emphatically, "
        "because it is the single fact that makes most expectation "
        "calculations in this course tractable, and almost everyone's "
        "instinct is that independence must be needed somewhere."),
  ("p", "The standard technique: express the quantity you care about as a sum "
        "of <b>indicator</b> random variables, each 0 or 1. The expectation "
        "of an indicator is just the probability of its event, so:"),
  ("eq", "X = &Sigma;&#7522; X&#7522; &nbsp;&rArr;&nbsp; E[X] = &Sigma;&#7522; Pr[event i occurs]"),
  ("p", "You have replaced a hard question about a complicated random "
        "variable with many easy questions about single events, and you are "
        "allowed to do this even when the events are tangled together."),

  ("h1", "3 &nbsp; Randomised quicksort, analysed"),
  ("p", "Quicksort picks a pivot, partitions around it, and recurses on both "
        "sides. With a random pivot, how many comparisons does it make in "
        "expectation?"),
  ("h2", "3.1 &nbsp; Setting it up"),
  ("p", "Label elements by their rank in sorted order: z&#8321; &lt; z&#8322; "
        "&lt; &hellip; &lt; z&#8345;. Define the indicator X&#7522;&#11388; = 1 "
        "if z&#7522; and z&#11388; are ever compared, 0 otherwise. Any two "
        "elements are compared at most once — a comparison only happens "
        "against a pivot, and a pivot is removed from all later subproblems. "
        "So the total comparison count is exactly &Sigma; X&#7522;&#11388;, and "
        "by linearity:"),
  ("eq", "E[comparisons] = &Sigma;<sub>i&lt;j</sub> Pr[z&#7522; and z&#11388; are compared]"),
  ("h2", "3.2 &nbsp; The key observation"),
  ("callout", "Which pivot is chosen first from the range?",
   ["Consider S = {z&#7522;, z&#7522;&#8330;&#8321;, &hellip;, z&#11388;}, the "
    "elements whose ranks lie between i and j inclusive. These stay together "
    "in the same subproblem until some element of S is chosen as a pivot.",
    "Whichever element of S is chosen as a pivot <b>first</b> determines "
    "everything: if it is z&#7522; or z&#11388;, the two are compared against "
    "it and hence to each other. If it is anything strictly between them, "
    "they are separated into different subproblems and will never be "
    "compared.",
    "Every element of S is equally likely to be the first of S chosen, and "
    "|S| = j &minus; i + 1. Two of them are favourable. So:"]),
  ("eq", "Pr[z&#7522; and z&#11388; compared] = 2 / (j &minus; i + 1)"),
  ("p", "Summing gives &Sigma;<sub>i&lt;j</sub> 2/(j&minus;i+1) &asymp; "
        "2n&middot;H&#8345; &asymp; 2n ln n &asymp; 1.39 n log&#8322; n. The "
        "constant 1.39 is worth remembering: quicksort makes about 39% more "
        "comparisons than the information-theoretic minimum, and is still "
        "usually the fastest sort."),
  ("callout", "Why quicksort beats mergesort anyway",
   ["Both are &Theta;(n log n) in expectation, and quicksort has a worse "
    "worst case and makes more comparisons. It is still generally faster.",
    "The reason is not in the comparison count. Quicksort partitions in "
    "place with two sequential scans, which is close to ideal for the "
    "prefetcher and uses &Theta;(log n) extra space. Mergesort needs "
    "&Theta;(n) auxiliary space and writes to a different array than it "
    "reads.",
    "This is Module 01's point made concrete: the model cannot see the "
    "difference, and the difference decides the benchmark."]),

  ("break",),
  ("h1", "4 &nbsp; Selection in linear time"),
  ("p", "Finding the k-th smallest element looks like it should require "
        "sorting, but it does not. <b>Quickselect</b> partitions exactly as "
        "quicksort does, then recurses into only the side containing rank k."),
  ("eq", "T(n) = T(n/2) + &Theta;(n) &nbsp;&rArr;&nbsp; T(n) = &Theta;(n)"),
  ("p", "The work forms a geometric series n + n/2 + n/4 + &hellip; &lt; 2n. "
        "Compare mergesort's T(n) = 2T(n/2) + &Theta;(n) = &Theta;(n log n): "
        "the only difference is one recursive call instead of two, and it "
        "removes the logarithmic factor entirely. This is exactly the "
        "binary-search-versus-mergesort contrast from Module 02."),
  ("p", "A deterministic linear-time algorithm also exists: <b>median of "
        "medians</b>, which chooses a provably decent pivot by recursively "
        "finding the median of groups of five. It is genuinely linear in the "
        "worst case and it is slower than quickselect on essentially every "
        "real input, because the constant factor is large. It is worth "
        "knowing as a proof that the worst case can be eliminated, and it is "
        "not worth using."),

  ("h1", "5 &nbsp; Concentration"),
  ("p", "An expectation on its own is a weak statement: a random variable "
        "with mean 10 could be 10 every time, or 0 half the time and 20 the "
        "other half. <b>Concentration bounds</b> say how unlikely it is to "
        "land far from the mean, and they are what make randomised algorithms "
        "trustworthy rather than merely good on average."),
  ("table", ["Bound", "Requires", "Gives", "Decay"],
   [["Markov", "X &ge; 0 only",
     "Pr[X &ge; a] &le; E[X]/a", "1/a — very weak"],
    ["Chebyshev", "Known variance &sigma;&#178;",
     "Pr[|X &minus; &mu;| &ge; k&sigma;] &le; 1/k&#178;", "Polynomial"],
    ["Chernoff / Hoeffding", "Independent bounded variables",
     "Pr[X &ge; (1+&delta;)&mu;] &le; e<super>&minus;&delta;&#178;&mu;/3</super>",
     "<b>Exponential</b>"]],
   [0.22, 0.28, 0.32, 0.18]),
  ("callout", "What this means in practice",
   ["For randomised quicksort, a Chernoff-style argument shows the "
    "probability of exceeding c&middot;n log n comparisons is below "
    "1/n&#178; for modest c.",
    "At n = 10&#8310;, that is under 10<super>&minus;12</super>. The machine "
    "is more likely to suffer an undetected memory error during the sort than "
    "the sort is to be slow.",
    "At that point the worst case has stopped being an engineering concern. "
    "This is the difference between 'expected to be fast' and 'you may stop "
    "worrying', and it is why concentration bounds matter more than the "
    "expectation calculation they accompany."]),

  ("h1", "6 &nbsp; Where randomisation recurs"),
  ("table", ["Setting", "What randomness buys", "Where"],
   [["Hashing", "Defeats adversarial key choice; makes the uniformity "
     "assumption true by construction rather than by hope.", "Module 05"],
    ["Treaps, skip lists", "Balance without rotation logic — far simpler "
     "code for the same expected bounds.", "Module 05"],
    ["Karger min-cut", "A trivially simple algorithm that succeeds with "
     "probability &ge; 2/n&#178;, repeated to amplify.", "Module 11"],
    ["Miller&ndash;Rabin", "Practical primality testing, hence practical "
     "public-key cryptography.", "CSCE 711"],
    ["Sketching, streaming", "Approximate answers in sublinear space.",
     "CSCE 727"],
    ["Monte Carlo rendering", "Estimating the reflectance integral by "
     "sampling light paths. Variance reduction there is the same mathematics "
     "as here.", "CSCE 647"]],
   [0.22, 0.60, 0.18]),
 ],
 "resources": [
   ("MIT 6.046J — Randomized Algorithms, Quicksort analysis",
    "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
    "The indicator-variable analysis of quicksort done carefully, plus "
    "Karger's min-cut."),
   ("Jeff Erickson, Algorithms — Randomized Algorithms chapter",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "Excellent on the Las Vegas / Monte Carlo distinction and on treaps."),
   ("Tim Roughgarden — Randomized Selection and QuickSort",
    "https://www.algorithmsilluminated.org/",
    "Part 1. Unhurried derivation of the 2/(j&minus;i+1) probability."),
   ("Mitzenmacher & Upfal, lecture slides (free)",
    "https://www.cs.cmu.edu/~avrim/Randalgs97/",
    "Concentration bounds with worked applications, if you want the "
    "probability theory tightened."),
 ],
 "exercises": [
   "Implement deterministic quicksort (first element as pivot) and randomised "
   "quicksort. Run both on sorted, reverse-sorted, and random input of size "
   "10&#8309;. Report the times and explain the pattern.",
   "Verify the comparison count empirically: instrument randomised quicksort "
   "to count comparisons, average over 100 runs at several n, and check the "
   "result against 1.39 n log&#8322; n.",
   "Implement quickselect and verify experimentally that it is linear by "
   "fitting a log-log slope.",
   "Implement median-of-medians selection. Confirm it is linear, then measure "
   "it against quickselect and report the constant-factor ratio.",
   "Use linearity of expectation to compute the expected number of fixed "
   "points in a random permutation of n elements. The answer is 1 regardless "
   "of n; explain why, and verify by simulation.",
   "Simulate 10,000 runs of randomised quicksort at n = 10&#8308; and plot the "
   "distribution of comparison counts. Observe how tightly it concentrates, "
   "and relate this to &sect;5.",
 ],
 "selfcheck": [
   "What does randomisation actually remove, given that the worst case still "
   "exists?",
   "State the difference between average-case and expected-case analysis and "
   "say which is stronger, with a reason.",
   "Does linearity of expectation require independence? Give an example from "
   "this module where the summands are clearly dependent.",
   "Derive Pr[z&#7522; and z&#11388; are compared] = 2/(j&minus;i+1).",
   "Why is quickselect linear while quicksort is n log n, given that they "
   "partition identically?",
   "What does a Chernoff bound add to an expectation result, and why does "
   "exponential rather than polynomial decay matter?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Sorting and Selection: Limits and Workarounds",
 "subtitle": "A proven lower bound, and the legitimate ways around it.",
 "question": "Why can't comparison sorting beat n log n, and when can you?",
 "outcomes": [
     "Prove the Ω(n log n) comparison-sorting lower bound.",
     "Explain exactly which assumption the bound depends on.",
     "Apply counting, radix, and bucket sort, and state their requirements.",
     "Explain stability and when it matters.",
     "Describe what production sorts actually do and why.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "A real lower bound",
   "blurb": "One of the few places you can prove that nothing will ever do "
            "better."},

  {"t": "bullets", "kicker": "The argument", "title": "The decision tree",
   "items": [
     "Model any comparison sort as a binary tree.",
     ("Each internal node is a comparison; each branch is an outcome.", 1),
     ("Each leaf is a permutation the algorithm can output.", 1),
     "",
     "There are <b>n!</b> possible orderings, so the tree needs n! leaves.",
     "A binary tree with n! leaves has height ≥ log₂(n!).",
     "",
     "By Stirling: log₂(n!) = Θ(n log n).",
     "",
     "Height = worst-case comparisons. So <b>every</b> comparison sort is "
     "Ω(n log n).",
   ],
   "note": "Stress that this is a statement about all possible algorithms, "
           "including ones nobody has invented. That is rare and worth "
           "savouring."},

  {"t": "callout", "title": "What the bound actually depends on",
   "kind": "The escape hatch",
   "body": ["The proof assumes the <i>only</i> operation available is "
            "comparing two elements. That is the entire content of the "
            "assumption.",
            "If you can do something else with a key — use it as an "
            "array index, extract its digits, hash it — the decision "
            "tree is no longer a model of your algorithm and the bound does "
            "not apply.",
            "This is not a loophole. It is the standard way lower bounds "
            "work: they constrain a model, and changing the model is a "
            "legitimate response. Part 2 is three algorithms that do exactly "
            "that."]},

  {"t": "section", "label": "Part 2", "title": "Sorting without comparing",
   "blurb": "Three algorithms that look at the keys instead."},

  {"t": "table", "kicker": "Linear sorts", "title": "What each one needs",
   "header": ["Sort", "Time", "Requires", "Breaks when"],
   "widths": [2.3, 2.6, 3.6, 3.6],
   "rows": [
     ["Counting", "Θ(n + k)", "Integer keys in [0, k)",
      "k ≫ n — memory explodes"],
     ["Radix", "Θ(d(n + k))", "Fixed-width keys, d digits",
      "Variable-length or unbounded keys"],
     ["Bucket", "Θ(n) expected", "Keys roughly uniform over a range",
      "Skewed distribution — degrades to Θ(n²)"],
   ],
   "note": "Each row's 'requires' column is the price. These are not free "
           "wins; they are trades of generality for speed."},

  {"t": "code", "kicker": "Counting sort", "title": "Linear, stable, and the basis of radix",
   "lang": "python", "code": """
def counting_sort(a, k):            # keys in [0, k)
    count = [0] * k
    for x in a:
        count[x] += 1               # histogram

    total = 0                       # prefix sums -> output positions
    for i in range(k):
        count[i], total = total, total + count[i]

    out = [None] * len(a)
    for x in a:                     # forward pass keeps equal keys
        out[count[x]] = x           #   in their original order
        count[x] += 1               #   -> STABLE
    return out
""",
   "caption": "Stability is not incidental here. Radix sort depends on it "
              "entirely: sorting digit by digit only works if earlier passes "
              "survive later ones.",
   "note": "Have them break stability deliberately and watch radix sort "
           "produce garbage. It is the clearest demonstration of why "
           "stability is a real property and not a nicety."},

  {"t": "bullets", "kicker": "Radix sort", "title": "Least significant digit first",
   "items": [
     "Sort by the least significant digit, then the next, up to the most "
     "significant.",
     "Each pass uses a <b>stable</b> counting sort.",
     "",
     "Why it works: after sorting by digit <i>i</i>, elements agreeing on "
     "digit <i>i</i> remain in the relative order established by digits "
     "<i>i−1</i> and below.",
     ("Stability is load-bearing. Remove it and the algorithm is wrong, not "
      "merely slower.", 1),
     "",
     "Θ(d(n + k)) — linear when d and k are constants.",
     ("32-bit integers as four 8-bit digits: 4 passes, k = 256.", 1),
   ]},

  {"t": "section", "label": "Part 3", "title": "Stability and practice",
   "blurb": "What production sorts actually do."},

  {"t": "two", "kicker": "Stability", "title": "When it matters",
   "lh": "Stable — equal keys keep input order",
   "l": ["Mergesort, counting sort, insertion sort, Timsort.",
         "Required for radix sort to be correct.",
         "Lets you sort by multiple keys in passes:",
         ("sort by name, then stably by department → sorted by "
          "department, alphabetical within each.", 1)],
   "rh": "Unstable — equal keys may be reordered",
   "r": ["Quicksort, heapsort, introsort.",
         "Usually faster and uses less memory.",
         "Fine when keys are unique or ties are genuinely irrelevant.",
         ("C++ <code>std::sort</code> is unstable; "
          "<code>std::stable_sort</code> exists and costs more.", 1)]},

  {"t": "table", "kicker": "Reality", "title": "What real sorts do",
   "header": ["Implementation", "Strategy"],
   "widths": [3.3, 8.8],
   "rows": [
     ["C++ std::sort", "Introsort: quicksort, heapsort if recursion too deep, insertion sort below ~16"],
     ["Python sorted()", "Timsort: find existing runs, merge them — Θ(n) on nearly-sorted data"],
     ["Java Arrays.sort", "Dual-pivot quicksort for primitives; Timsort for objects (stability required)"],
     ["Rust sort_unstable", "Pattern-defeating quicksort — detects adversarial patterns and adapts"],
   ],
   "footnote": "Not one of them is a textbook algorithm. All are hybrids.",
   "note": "The lesson: textbook algorithms are components, not products. "
           "Every production sort switches strategy based on input."},

  {"t": "callout", "title": "Timsort and the lesson it carries",
   "kind": "Worth noting",
   "body": ["Timsort scans for runs that are already sorted, then merges "
            "them. On already-sorted input it is Θ(n); on random input "
            "it matches mergesort.",
            "It exists because real data is very often partly ordered "
            "— appended logs, re-sorted tables, concatenated sorted "
            "files — and worst-case analysis is blind to that.",
            "The general lesson: asymptotic analysis of the worst case tells "
            "you what cannot go wrong. It does not tell you what usually "
            "happens, and exploiting what usually happens is where a great "
            "deal of practical speed lives."]},

  {"t": "bullets", "kicker": "Lower bounds", "title": "Other bounds worth knowing",
   "items": [
     "<b>Searching a sorted array:</b> Ω(log n) comparisons. Binary "
     "search is optimal.",
     "<b>Finding the maximum:</b> exactly n − 1 comparisons. Every "
     "element but one must lose.",
     "<b>Max and min together:</b> ⌈3n/2⌉ − 2, beating the "
     "obvious 2n − 3 by pairing first.",
     "<b>Element uniqueness:</b> Ω(n log n) in the comparison model.",
     "",
     "Each follows the same shape: count the possible outputs, bound how much "
     "information one operation yields, divide.",
   ],
   "footnote": "Knowing a bound exists is what stops you optimising "
               "something that is already optimal."},
 ],
 "takeaways": [
   "Any comparison sort is a binary decision tree with n! leaves, so its "
   "height is Ω(n log n). This constrains every algorithm, including "
   "undiscovered ones.",
   "The bound depends entirely on comparison being the only operation. Use "
   "the key as an index or a digit sequence and it does not apply.",
   "Counting, radix, and bucket sort each buy linearity by assuming something "
   "about the keys. The assumption is the price.",
   "Stability is load-bearing for radix sort — without it the algorithm "
   "is wrong, not slow.",
   "Every production sort is a hybrid that switches strategy by input size "
   "and shape. Textbook algorithms are components.",
   "Timsort is fast because real data is often partly sorted, which "
   "worst-case analysis cannot see.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The comparison lower bound"),
  ("p", "Most of this course is about finding better algorithms. This section "
        "is about proving that no better algorithm exists, which is a rarer "
        "and in some ways more satisfying kind of result."),
  ("h2", "1.1 &nbsp; The decision tree model"),
  ("p", "Model any comparison-based sorting algorithm as a binary tree. Each "
        "internal node is a comparison 'is a&#7522; &le; a&#11388;?'; the two "
        "children correspond to the two answers. Execution is a root-to-leaf "
        "path, and each leaf must be labelled with the permutation the "
        "algorithm outputs when it arrives there."),
  ("ol", ["To sort correctly, the algorithm must be able to output any of the "
          "n! possible permutations. So the tree has at least n! leaves.",
          "A binary tree of height h has at most 2&#7506; leaves. Hence "
          "2&#7506; &ge; n!, so h &ge; log&#8322;(n!).",
          "By Stirling's approximation, log&#8322;(n!) = n log&#8322; n "
          "&minus; n log&#8322; e + O(log n) = &Theta;(n log n).",
          "The height is the worst-case number of comparisons. Therefore "
          "every comparison sort makes &Omega;(n log n) comparisons in the "
          "worst case."]),
  ("callout", "Why this is a strong result",
   ["This is not a statement about mergesort or quicksort. It is a statement "
    "about <i>every comparison-based sorting algorithm that will ever be "
    "written</i>, including ones nobody has thought of.",
    "Results of this kind are uncommon. Most of the time we can only say that "
    "nobody currently knows how to do better — the P versus NP question "
    "(Module 12) is exactly that situation. Here we genuinely know."]),
  ("h2", "1.2 &nbsp; The assumption, stated plainly"),
  ("p", "The proof assumes the algorithm learns about the input <i>only</i> "
        "through comparisons. Each comparison yields one bit, there are "
        "log&#8322;(n!) bits of information to acquire, so you need that many "
        "comparisons. Stated that way the result is almost obvious, which is "
        "a good sign."),
  ("p", "And it immediately tells you how to beat it: extract more than one "
        "bit per operation. If a key can be used as an array index, that one "
        "operation distinguishes among k possibilities rather than two. The "
        "decision tree is then not a model of your algorithm and the bound "
        "simply does not apply to it."),

  ("h1", "2 &nbsp; Sorting in linear time"),
  ("h2", "2.1 &nbsp; Counting sort"),
  ("p", "For integer keys in [0, k): count occurrences of each value, convert "
        "the counts to prefix sums to get output positions, then place "
        "elements. &Theta;(n + k) time and &Theta;(n + k) space."),
  ("code", """def counting_sort(a, k):
    count = [0] * k
    for x in a:
        count[x] += 1                 # histogram

    total = 0                         # prefix sums -> start positions
    for i in range(k):
        count[i], total = total, total + count[i]

    out = [None] * len(a)
    for x in a:                       # forward pass over the input keeps
        out[count[x]] = x             #   equal keys in original order
        count[x] += 1                 #   -> stable
    return out"""),
  ("p", "Usable only when k is comparable to n. Sorting 32-bit integers "
        "directly would need an array of four billion counters, so counting "
        "sort is not used alone for wide keys — it is used as the inner "
        "loop of radix sort."),
  ("h2", "2.2 &nbsp; Radix sort"),
  ("p", "Treat each key as d digits in base k. Sort by the least significant "
        "digit, then the next, and so on to the most significant, using a "
        "stable sort at each pass."),
  ("callout", "Stability is load-bearing",
   ["After the pass on digit i, two elements agreeing on digit i must remain "
    "in the relative order that the earlier passes gave them — that is "
    "precisely what encodes the information from the lower-order digits.",
    "Use an unstable sort for the inner pass and radix sort does not merely "
    "slow down; it produces wrong output. This is the clearest example in the "
    "course of stability being a correctness property rather than a "
    "convenience."]),
  ("p", "&Theta;(d(n + k)). For 32-bit integers split into four 8-bit digits, "
        "that is four passes with k = 256 — linear in n with a small "
        "constant, and genuinely faster than comparison sorting for large "
        "arrays of fixed-width integers."),
  ("h2", "2.3 &nbsp; Bucket sort"),
  ("p", "Distribute elements into buckets by value range, sort each bucket, "
        "concatenate. Linear in expectation <i>if</i> the keys are roughly "
        "uniform over the range. Under a skewed distribution everything lands "
        "in one bucket and the cost degrades to that of the inner sort, which "
        "is the honest reason bucket sort is rarely used outside settings "
        "where the distribution is known."),

  ("break",),
  ("h1", "3 &nbsp; Stability"),
  ("p", "A sort is <b>stable</b> if elements comparing equal keep their "
        "original relative order."),
  ("table", ["Stable", "Unstable"],
   [["Mergesort, Timsort, counting sort, insertion sort, bubble sort",
     "Quicksort, heapsort, introsort, selection sort"]],
   [0.5, 0.5]),
  ("p", "Three reasons it matters:"),
  ("ol", ["<b>Radix sort requires it</b> for correctness, as above.",
          "<b>Multi-key sorting by repeated passes.</b> Sort by surname, then "
          "stably by department, and you get a listing grouped by department "
          "and alphabetical within each. Without stability the second pass "
          "destroys the first.",
          "<b>User-visible ordering.</b> Re-sorting a displayed table by a "
          "new column should not scramble rows that tie. Java's "
          "<code>Arrays.sort</code> uses Timsort for objects specifically "
          "because API users expect this."]),
  ("p", "Stability is not free — it typically costs auxiliary memory "
        "— which is why C++ offers both <code>std::sort</code> and "
        "<code>std::stable_sort</code> and makes you choose."),

  ("h1", "4 &nbsp; What production sorts actually do"),
  ("table", ["Implementation", "Algorithm", "Why"],
   [["C++ <code>std::sort</code>", "Introsort",
     "Quicksort for speed; switches to heapsort when recursion depth exceeds "
     "~2 log n, guaranteeing O(n log n) worst case; insertion sort below ~16 "
     "elements where its constant wins."],
    ["Python <code>sorted()</code>", "Timsort",
     "Detects existing ascending or descending runs and merges them. "
     "&Theta;(n) on already-sorted input, stable, and tuned for the partly "
     "ordered data that occurs constantly in practice."],
    ["Java <code>Arrays.sort</code>", "Dual-pivot quicksort / Timsort",
     "Dual-pivot quicksort for primitives, where stability is meaningless; "
     "Timsort for objects, where callers expect stability."],
    ["Rust <code>sort_unstable</code>", "Pattern-defeating quicksort",
     "Detects patterns that would trigger quicksort's bad cases and adapts, "
     "retaining quicksort's speed without the vulnerability."]],
   [0.21, 0.19, 0.60]),
  ("callout", "The lesson",
   ["Not one production sort is a textbook algorithm. Every one is a hybrid "
    "that switches strategy based on input size, detected structure, and "
    "recursion depth.",
    "Textbook algorithms are <i>components</i>. The engineering is in knowing "
    "which component applies when — and that judgement comes from "
    "exactly the analysis this course teaches.",
    "Timsort in particular is fast because real data is frequently partly "
    "sorted, a fact worst-case analysis is structurally unable to see. Worst-"
    "case bounds tell you what cannot go wrong; they do not tell you what "
    "usually happens."]),

  ("h1", "5 &nbsp; Other lower bounds"),
  ("table", ["Problem", "Bound", "Argument"],
   [["Search a sorted array", "&Omega;(log n)",
     "n possible answers, one bit per comparison."],
    ["Find the maximum", "Exactly n &minus; 1",
     "Every element except the maximum must lose at least one comparison, and "
     "each comparison produces one loser."],
    ["Find max and min together", "&lceil;3n/2&rceil; &minus; 2",
     "Pair elements first, then compare winners and losers separately. Beats "
     "the naive 2n &minus; 3."],
    ["Element uniqueness", "&Omega;(n log n)",
     "In the comparison model. Hashing beats it, by changing the model."],
    ["Sorting", "&Omega;(n log n)", "The decision tree argument of &sect;1."]],
   [0.26, 0.19, 0.55]),
  ("p", "All share a shape: count how many distinct outputs are possible, "
        "bound how much information one permitted operation can yield, and "
        "divide. Recognising that shape lets you derive bounds for new "
        "problems rather than memorising them."),
  ("p", "The practical value is knowing when to stop. If you have a "
        "comparison sort running at n log n, no amount of cleverness within "
        "that model will improve the asymptotics, and your remaining options "
        "are constant factors or a different model. That is a genuinely "
        "useful thing to know on a deadline."),
 ],
 "resources": [
   ("MIT 6.006 — Sorting lower bound, Counting and Radix Sort",
    "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
    "The decision tree argument presented carefully, with the linear-time "
    "sorts as the follow-on."),
   ("Jeff Erickson, Algorithms — Sorting chapter",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "Good on what the lower bound does and does not constrain."),
   ("Tim Peters — Timsort description (CPython source)",
    "https://github.com/python/cpython/blob/main/Objects/listsort.txt",
    "The design document for Timsort, written by its author. An unusually "
    "clear piece of engineering writing — read it."),
   ("Orson Peters — Pattern-defeating quicksort",
    "https://github.com/orlp/pdqsort",
    "How Rust's unstable sort resists adversarial patterns. Short and "
    "readable."),
 ],
 "exercises": [
   "Write out the decision tree for sorting three elements. Confirm it has 6 "
   "leaves and height 3, and check this against the log&#8322;(3!) bound.",
   "Implement counting sort and radix sort. Measure radix sort against "
   "<code>std::sort</code> (or <code>sorted()</code>) on 10&#8311; 32-bit "
   "integers and report the ratio.",
   "Break stability in your counting sort by iterating the final pass "
   "backwards without adjusting the indices, then run radix sort with it. "
   "Capture the wrong output and explain exactly which information was lost.",
   "Implement bucket sort and measure it on uniform input and on "
   "exponentially distributed input. Show the degradation and explain it.",
   "Implement the pairing algorithm that finds max and min in "
   "&lceil;3n/2&rceil; &minus; 2 comparisons. Verify the count empirically "
   "against the naive 2n &minus; 3.",
   "Generate a nearly-sorted array (sorted, then 1% of elements swapped at "
   "random). Measure Timsort or <code>sorted()</code> against "
   "<code>std::sort</code> on it. Explain the difference.",
 ],
 "selfcheck": [
   "Reproduce the decision-tree lower bound argument, including why the tree "
   "must have n! leaves.",
   "What single assumption does the &Omega;(n log n) bound rest on, and how "
   "do linear-time sorts evade it?",
   "State the requirement and the failure mode of counting, radix, and bucket "
   "sort.",
   "Why is stability a correctness requirement for radix sort rather than a "
   "convenience?",
   "Give two reasons a production sort would switch algorithms partway "
   "through.",
   "Why is Timsort fast on real data in a way that worst-case analysis cannot "
   "predict?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Hashing and Amortized Analysis",
 "subtitle": "Constant time on average, and what 'average' is doing there.",
 "question": "How can a lookup be O(1), and what is the catch?",
 "outcomes": [
     "Explain collision resolution strategies and their trade-offs.",
     "Explain why universal hashing is needed and what it guarantees.",
     "Perform amortised analysis by aggregate, accounting, and potential "
     "methods.",
     "Prove dynamic array doubling is O(1) amortised.",
     "Explain why hash tables degrade in practice and how to detect it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Hash tables",
   "blurb": "Trading a worst-case guarantee for an expected one."},

  {"t": "bullets", "kicker": "The idea", "title": "Index by content",
   "items": [
     "A direct-address table is O(1): use the key as an array index.",
     ("Needs a slot per possible key. Fine for k = 256, impossible for "
      "strings.", 1),
     "",
     "A <b>hash function</b> compresses a large key space into m slots.",
     ("h: U → {0, 1, …, m−1}", 1),
     "",
     "Compression forces <b>collisions</b> — by pigeonhole, if "
     "|U| &gt; m.",
     "",
     "So a hash table is: a direct-address table, plus a strategy for "
     "collisions.",
   ]},

  {"t": "two", "kicker": "Collisions", "title": "Two strategies",
   "lh": "Chaining",
   "l": ["Each slot holds a list of colliding entries.",
         "Expected search Θ(1 + α), α = n/m.",
         "Tolerates α &gt; 1 gracefully.",
         "Deletion is trivial.",
         ("Pointer chasing — poor cache behaviour.", 1)],
   "rh": "Open addressing",
   "r": ["Collisions probe elsewhere in the same array.",
         "Requires α &lt; 1; degrades sharply as α → 1.",
         "No pointers — <b>excellent</b> cache behaviour.",
         "Deletion needs tombstones, which accumulate.",
         ("What most modern high-performance tables use.", 1)],
   "note": "The cache argument has flipped the default over the last twenty "
           "years. Chaining is textbook; open addressing is what fast "
           "libraries do."},

  {"t": "eq", "kicker": "Load factor", "title": "Why α decides everything",
   "eqs": [
     ("α  =  n / m",
      "Elements over slots. The single number that characterises a table."),
     ("chaining:  E[probes]  =  1 + α",
      "Graceful. Doubling α roughly doubles chain length."),
     ("linear probing:  E[probes]  ≈  (1 + 1/(1−α)²)/2",
      "At α = 0.9 this is ~50 probes. The cliff is steep and sudden."),
   ],
   "caption": "Open-addressed tables resize at α ≈ 0.7 for exactly "
              "this reason — past that, performance falls off a cliff "
              "rather than degrading.",
   "note": "Have them plot the linear probing curve. The shape explains every "
           "'our service fell over at 70% capacity' story."},

  {"t": "section", "label": "Part 2", "title": "Universal hashing",
   "blurb": "Making the uniformity assumption true instead of hoping."},

  {"t": "callout", "title": "Every fixed hash function has a bad input set",
   "kind": "The problem",
   "body": ["For any fixed h mapping |U| keys into m slots, some slot "
            "receives at least |U|/m keys. An adversary who knows h can "
            "supply exactly those.",
            "Every operation then collides and the table degrades to a linked "
            "list: Θ(n) per lookup.",
            "This is not hypothetical. Hash-collision denial of service "
            "attacks against web frameworks — where form parameters go "
            "straight into a hash table — were a widespread real "
            "vulnerability, and the fix deployed everywhere was randomised "
            "hashing."]},

  {"t": "bullets", "kicker": "The fix", "title": "Choose the hash function at random",
   "items": [
     "A family H is <b>universal</b> if for any two distinct keys x ≠ y:",
     ("Pr[h(x) = h(y)] ≤ 1/m, over a random h drawn from H.", 1),
     "",
     "Pick h from H at run time, per table instance.",
     "",
     "Now the expected chain length is O(1 + α) <b>for every input</b>.",
     ("Exactly Module 03's move: the guarantee stops depending on the input "
      "and starts depending on your coins.", 1),
     "",
     "Standard in every modern language runtime, usually seeded per process.",
   ],
   "note": "Making the explicit link to Module 03 is the point of placing "
           "this module here."},

  {"t": "section", "label": "Part 3", "title": "Amortised analysis",
   "blurb": "A worst-case statement about a sequence, with no probability "
            "involved."},

  {"t": "callout", "title": "Amortised is not average", "kind": "Distinction",
   "body": ["<b>Average case</b> is probabilistic: it averages over a "
            "distribution of inputs, and could be wrong on your data.",
            "<b>Amortised</b> involves no probability at all. It is a "
            "worst-case bound on a <i>sequence</i>: any n operations cost at "
            "most X in total, guaranteed, always.",
            "An individual operation may be expensive. The claim is that it "
            "cannot be expensive often, and the proof is a counting argument, "
            "not a probabilistic one."]},

  {"t": "table", "kicker": "Methods", "title": "Three ways to do it",
   "header": ["Method", "How", "Best for"],
   "widths": [2.7, 5.4, 4.0],
   "rows": [
     ["Aggregate", "Bound total cost of n ops, divide by n",
      "Simple cases; a first pass"],
     ["Accounting", "Overcharge cheap ops; bank credit for expensive ones",
      "When you can see what pays for what"],
     ["Potential", "Define Φ on the structure; amortised = actual + ΔΦ",
      "The general method; use when the others get awkward"],
   ]},

  {"t": "code", "kicker": "Worked", "title": "Dynamic array doubling, three ways",
   "lang": "text", "code": """
Append is O(1), except when full: allocate 2x, copy everything, O(n).

AGGREGATE
  n appends trigger resizes at sizes 1, 2, 4, ..., n.
  Total copying = 1 + 2 + 4 + ... + n < 2n.
  Total cost < n + 2n = 3n  ->  O(1) amortised.

ACCOUNTING
  Charge 3 credits per append: 1 to insert, 2 banked.
  When the array of size n doubles, the n/2 elements added since the
  last resize have 2 credits each = n credits banked -- exactly enough
  to pay for copying all n elements.  Credit never goes negative.

POTENTIAL
  Phi = 2n - m   (n elements, capacity m).  Phi >= 0 always.
  Normal append:  actual 1, dPhi = 2    ->  amortised 3.
  Resizing one:   actual n, dPhi = -n+2 ->  amortised 3.
  Constant either way.
""",
   "caption": "All three give O(1). The potential method generalises best "
              "— it is what you reach for on splay trees and Fibonacci "
              "heaps.",
   "note": "Worth emphasising: growth must be <b>multiplicative</b>. Adding "
           "a constant gives Θ(n) amortised, which is the next slide."},

  {"t": "callout", "title": "Why growth must be multiplicative",
   "kind": "The thing to remember",
   "body": ["Doubling: resizes at 1, 2, 4, 8, … n. Total copying is a "
            "geometric series summing to under 2n. <b>O(1) amortised.</b>",
            "Growing by a constant c: resizes at c, 2c, 3c, … n. Total "
            "copying is an arithmetic series summing to "
            "Θ(n²/c). <b>Θ(n) amortised.</b>",
            "A geometric series converges and an arithmetic one does not. "
            "That single fact is why every growable buffer in every standard "
            "library multiplies rather than adds — and why "
            "<code>realloc</code> by +1 in a loop is a classic performance "
            "bug."]},

  {"t": "bullets", "kicker": "Practice", "title": "Why real hash tables disappoint",
   "items": [
     "<b>Bad hash function.</b> Clustering in the low bits is common; many "
     "tables mix before masking.",
     "<b>Load factor too high.</b> Open addressing collapses past ~0.7.",
     "<b>Tombstones.</b> Deletions in open addressing leave markers that make "
     "probes longer until a rehash.",
     "<b>Cache misses.</b> Every chained lookup is a pointer dereference to "
     "an unpredictable address.",
     "<b>Resize pauses.</b> O(1) amortised still means one O(n) operation, "
     "which matters under a latency budget.",
     "",
     "Measure <b>probe-length distribution</b>, not average lookup time. The "
     "tail is where the problem shows first.",
   ],
   "footnote": "Amortised O(1) is a statement about throughput, not about "
               "latency."},
 ],
 "takeaways": [
   "A hash table is a direct-address table plus a collision strategy. The "
   "load factor α = n/m characterises it.",
   "Chaining degrades gracefully; open addressing is cache-friendly but falls "
   "off a cliff near α = 0.7.",
   "Every fixed hash function has an adversarial input set. Universal hashing "
   "picks h at random, moving the guarantee off the input — the same "
   "move as Module 03.",
   "Amortised analysis involves no probability. It is a worst-case bound on a "
   "sequence.",
   "Growth must be multiplicative. Geometric series converge; arithmetic ones "
   "do not. That is the whole reason doubling works.",
   "Amortised O(1) bounds throughput, not latency — one operation in the "
   "sequence is still O(n).",
 ],
 "notes": [
  ("h1", "1 &nbsp; From direct addressing to hashing"),
  ("p", "If keys are integers in a small range, a lookup is trivially O(1): "
        "index an array. The difficulty is that real key spaces are enormous "
        "— all strings, all 64-bit integers — while the number of "
        "keys actually stored is small."),
  ("p", "A <b>hash function</b> h: U &rarr; {0, &hellip;, m&minus;1} "
        "compresses the key space to a table of m slots. Because |U| &gt; m, "
        "the pigeonhole principle guarantees <b>collisions</b>: distinct keys "
        "mapping to the same slot. A hash table is therefore a direct-address "
        "table plus a policy for what to do when two keys want the same "
        "slot."),
  ("h2", "1.1 &nbsp; Chaining versus open addressing"),
  ("table", ["", "Chaining", "Open addressing"],
   [["Structure", "Each slot points to a list of entries",
     "All entries live in the array; collisions probe elsewhere"],
    ["Load factor", "&alpha; may exceed 1; degrades linearly",
     "Requires &alpha; &lt; 1; degrades sharply as &alpha; &rarr; 1"],
    ["Expected probes", "1 + &alpha;",
     "~(1 + 1/(1&minus;&alpha;)&#178;)/2 for linear probing"],
    ["Cache behaviour", "Poor — each lookup chases a pointer to an "
     "unpredictable address",
     "Excellent — probes are contiguous and prefetch well"],
    ["Deletion", "Trivial: unlink from the list",
     "Needs tombstones, which accumulate and lengthen probes until a rehash"],
    ["Used by", "Textbooks; older standard libraries",
     "Most modern high-performance implementations"]],
   [0.15, 0.40, 0.45]),
  ("callout", "The cache argument has changed the default",
   ["Classical analysis favours chaining: the bounds are cleaner and it "
    "handles &alpha; &gt; 1. On modern hardware, open addressing usually "
    "wins, because a linear probe sequence is contiguous memory the "
    "prefetcher handles perfectly, whereas every chained lookup is a "
    "dependent load to an unpredictable address.",
    "This is Module 01's theme again: two structures with the same asymptotic "
    "behaviour, separated by a large constant factor the model cannot see. "
    "CSCE 614 Module 05 explains the mechanism."]),
  ("h2", "1.2 &nbsp; The load factor"),
  ("eq", "&alpha; = n / m"),
  ("p", "For chaining, the expected number of elements examined is 1 + "
        "&alpha; — well-behaved, and doubling &alpha; roughly doubles "
        "the work. For linear probing the expected probe count is "
        "approximately (1 + 1/(1&minus;&alpha;)&#178;)/2, which is about 2.5 "
        "at &alpha; = 0.5, about 8.5 at &alpha; = 0.75, and about 50 at "
        "&alpha; = 0.9."),
  ("p", "That is not a gradual degradation, it is a cliff, and it is why "
        "open-addressed tables resize at a load factor around 0.7 rather than "
        "waiting until full. A system sized to run at 90% capacity will "
        "appear fine in testing and collapse in production."),

  ("h1", "2 &nbsp; Universal hashing"),
  ("p", "The O(1 + &alpha;) analysis assumes keys distribute uniformly across "
        "slots. For any <i>fixed</i> hash function that assumption is false "
        "for some input: with |U| keys and m slots, some slot must receive at "
        "least |U|/m of them."),
  ("callout", "This became a real vulnerability",
   ["Web frameworks place form parameters, query strings, and JSON keys "
    "directly into hash tables. An attacker who knows the hash function can "
    "submit a request whose parameters all collide, turning every table "
    "operation into a linear scan.",
    "The resulting denial-of-service attacks affected most major web "
    "frameworks simultaneously around 2011. The deployed fix, essentially "
    "everywhere, was randomised hashing seeded per process.",
    "A theoretical worst case became an operational emergency, which is worth "
    "remembering when a worst case looks too unlikely to care about."]),
  ("h2", "2.1 &nbsp; The definition and what it buys"),
  ("eq", "H is universal &nbsp;&hArr;&nbsp; for all x &ne; y: &nbsp; Pr<sub>h&isin;H</sub>[h(x) = h(y)] &le; 1/m"),
  ("p", "Choose h uniformly at random from H when the table is created. The "
        "expected chain length is then O(1 + &alpha;) for <b>every</b> input, "
        "with no distributional assumption — because the randomness is "
        "in the choice of h, not in the data."),
  ("p", "This is precisely the move from Module 03. The bad case still "
        "exists, but it now depends on which hash function you happened to "
        "draw, which the adversary cannot observe. Average-case becomes "
        "expected-case, and the guarantee becomes unconditional."),

  ("break",),
  ("h1", "3 &nbsp; Amortised analysis"),
  ("p", "Some operations are usually cheap and occasionally expensive. "
        "Amortised analysis bounds the cost of a <i>sequence</i>, showing "
        "that the expensive cases cannot occur often enough to matter."),
  ("callout", "Not average case",
   ["Average-case analysis is probabilistic and depends on an assumption "
    "about the input distribution.",
    "Amortised analysis involves no probability whatsoever. It is a "
    "worst-case claim about a sequence of operations: <i>any</i> n operations "
    "cost at most X in total, always, including under adversarial ordering. "
    "The proof is a counting argument.",
    "Conflating the two is one of the most common misunderstandings in this "
    "subject."]),
  ("h2", "3.1 &nbsp; Three methods"),
  ("table", ["Method", "Technique", "When to use"],
   [["Aggregate", "Bound the total cost of n operations directly, then "
     "divide by n.", "Simple structures; always try this first."],
    ["Accounting", "Assign each operation an amortised charge; overcharged "
     "cheap operations bank credit that pays for later expensive ones. "
     "Credit must never go negative.",
     "When you can identify concretely which cheap operations pay for which "
     "expensive one."],
    ["Potential", "Define &Phi; mapping the structure's state to a "
     "non-negative number. Amortised cost = actual cost + &Delta;&Phi;.",
     "The general method. Use it for splay trees, Fibonacci heaps, and "
     "anything where the other two become awkward."]],
   [0.16, 0.50, 0.34]),
  ("h2", "3.2 &nbsp; Dynamic arrays, done three ways"),
  ("p", "A growable array appends in O(1) until full, then allocates double "
        "the capacity and copies everything: O(n) for that one operation."),
  ("code", """AGGREGATE
  Over n appends, resizes happen at capacities 1, 2, 4, ..., n.
  Total elements copied = 1 + 2 + 4 + ... + n < 2n.
  Total cost < n (appends) + 2n (copies) = 3n.
  Amortised cost per append = 3 = O(1).

ACCOUNTING
  Charge 3 credits per append: 1 pays the insert, 2 go in the bank.
  When a table of size n doubles, the n/2 elements inserted since the
  previous resize hold 2 credits each -> n credits available, exactly
  covering the n copies. The balance never goes negative.

POTENTIAL
  Phi = 2n - m   (n = elements, m = capacity); Phi >= 0 since m <= 2n.
  Ordinary append: actual = 1,  dPhi = +2       -> amortised 3
  Resizing append: actual = n,  dPhi = -(n-2)   -> amortised 3"""),
  ("callout", "Growth must be multiplicative",
   ["<b>Doubling:</b> copies total 1 + 2 + 4 + &hellip; + n &lt; 2n. A "
    "geometric series converges, so the amortised cost is O(1).",
    "<b>Growing by a fixed c:</b> resizes at c, 2c, 3c, &hellip;, n, so "
    "copies total c + 2c + &hellip; + n = &Theta;(n&#178;/c). An arithmetic "
    "series does not converge, and the amortised cost per append is "
    "&Theta;(n).",
    "This is why every growable buffer in every standard library grows by a "
    "factor (2, or 1.5 to allow memory reuse) rather than by an increment, "
    "and why calling <code>realloc</code> with size+1 in a loop is a classic "
    "quadratic-blowup bug."]),

  ("h1", "4 &nbsp; Why real hash tables disappoint"),
  ("table", ["Cause", "Symptom", "Detection and fix"],
   [["Poor hash function", "Clustering; some probe sequences very long",
     "Plot the probe-length distribution. Mix bits before masking; avoid "
     "using raw low bits of pointers or sequential IDs."],
    ["Load factor too high", "Sudden collapse rather than gradual slowdown",
     "Resize at &alpha; &asymp; 0.7 for open addressing. Monitor &alpha;."],
    ["Tombstone accumulation", "Degradation under delete-heavy workloads even "
     "at low &alpha;",
     "Count tombstones; rehash when they exceed a threshold."],
    ["Cache misses", "Throughput far below the O(1) expectation",
     "Prefer open addressing; store small values inline rather than behind a "
     "pointer."],
    ["Resize pauses", "Occasional multi-millisecond latency spikes",
     "Amortised O(1) is a throughput claim. Under a latency budget, use "
     "incremental resizing that moves a few entries per operation."]],
   [0.21, 0.33, 0.46]),
  ("callout", "Measure the tail, not the mean",
   ["Average lookup time hides exactly the behaviour that causes incidents. "
    "A table with a 2.1 average probe count and a 95th percentile of 60 is "
    "about to become someone's outage.",
    "Instrument the probe-length distribution. It tells you about hash "
    "quality, load factor, and tombstones all at once, and it degrades "
    "visibly well before the average does."]),
 ],
 "resources": [
   ("MIT 6.006 — Hashing with Chaining, Table Doubling, Amortization",
    "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
    "Both halves of this module, carefully done, including the potential "
    "method."),
   ("MIT 6.046J — Amortized Analysis",
    "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
    "The graduate treatment, with the potential method applied to more "
    "demanding structures."),
   ("Jeff Erickson, Algorithms — Hash Tables chapter",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "Universal hashing done properly, with the construction and the proof."),
   ("Google — Swiss Tables design notes (Abseil)",
    "https://abseil.io/about/design/swisstables",
    "How a state-of-the-art open-addressed hash table is actually built, and "
    "why it is laid out the way it is. Short and worth reading."),
 ],
 "exercises": [
   "Implement hash tables with chaining and with linear probing. Measure "
   "average and 99th-percentile probe count as &alpha; goes from 0.1 to 0.95, "
   "and plot both. Identify the cliff.",
   "Implement a deliberately poor hash function (for example, the low 8 bits "
   "of the key) and measure the probe-length distribution against a good one.",
   "Construct an adversarial key set for a fixed hash function in your "
   "language of choice, insert it, and measure the degradation. Then enable "
   "or simulate randomised seeding and repeat.",
   "Implement a dynamic array with doubling and one that grows by +1. Measure "
   "total time for 10&#8310; appends and confirm the second is quadratic.",
   "Prove by the potential method that a counter supporting increment has "
   "O(1) amortised bit-flips. Choose &Phi; = number of 1 bits.",
   "Instrument a delete-heavy workload on your open-addressed table and show "
   "tombstone accumulation degrading lookups. Implement rehash-on-threshold "
   "and show the recovery.",
 ],
 "selfcheck": [
   "Why are collisions unavoidable, and what are the two main strategies for "
   "handling them?",
   "Why does open addressing degrade sharply near &alpha; = 0.7 while "
   "chaining does not?",
   "Why does a fixed hash function always have a bad input set, and what does "
   "universal hashing change?",
   "State precisely how amortised analysis differs from average-case "
   "analysis.",
   "Give the aggregate argument for dynamic array doubling, and explain why "
   "growing by a constant increment fails.",
   "Amortised O(1) is a claim about what, exactly? Give a situation where it "
   "is not the guarantee you need.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Graph Search and Decomposition",
 "subtitle": "Two traversals, and a surprising amount of structure.",
 "question": "What can you learn about a graph by walking it once?",
 "outcomes": [
     "Choose between adjacency list and matrix on the basis of density.",
     "Implement BFS and DFS and state what each computes.",
     "Classify DFS edges and use them to detect cycles.",
     "Compute topological order and strongly connected components.",
     "Recognise when a problem is a graph problem in disguise.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Representation",
   "blurb": "The first decision, and it is about density."},

  {"t": "table", "kicker": "Representation", "title": "List or matrix",
   "header": ["", "Adjacency list", "Adjacency matrix"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Space", "Θ(V + E)", "Θ(V²)"],
     ["Is (u,v) an edge?", "Θ(deg u)", "Θ(1)"],
     ["Iterate neighbours", "Θ(deg u) — optimal", "Θ(V)"],
     ["Good when", "Sparse: E = O(V)", "Dense: E ≈ V²"],
     ["In practice", "<b>Almost always this</b>", "Small or dense graphs"],
   ],
   "note": "Most real graphs are sparse: road networks, social graphs, "
           "dependency graphs, meshes. Adjacency list is the default."},

  {"t": "callout", "title": "Why E matters more than V", "kind": "Framing",
   "body": ["Graph algorithm complexities are written in terms of both V and "
            "E, and E is usually what dominates.",
            "<b>Sparse</b> (E = Θ(V)): a road network, a 3D mesh, a "
            "package dependency graph. O(V + E) is effectively linear.",
            "<b>Dense</b> (E = Θ(V²)): a distance matrix, a "
            "complete graph. Here O(V + E) is quadratic.",
            "Always ask which regime you are in before quoting a complexity. "
            "'O(V + E)' sounds linear and may not be."]},

  {"t": "section", "label": "Part 2", "title": "Two traversals",
   "blurb": "The same algorithm with a different container."},

  {"t": "code", "kicker": "The pattern", "title": "BFS and DFS are one algorithm",
   "lang": "python", "code": """
def traverse(G, s, container):
    seen = {s}
    container.add(s)
    while container:
        u = container.remove()       # <-- the ONLY difference
        for v in G[u]:
            if v not in seen:
                seen.add(v)
                container.add(v)

# container = QUEUE (FIFO) -> breadth-first: explores by distance
# container = STACK (LIFO) -> depth-first:  follows one path to the end
""",
   "caption": "Swap a queue for a stack and the traversal order, the tree "
              "shape, and the properties you can extract all change "
              "completely.",
   "note": "Showing them as one algorithm first makes the difference in "
           "properties feel earned rather than arbitrary."},

  {"t": "two", "kicker": "Properties", "title": "What each one gives you",
   "lh": "BFS — queue",
   "l": ["Visits in order of distance from the source.",
         "<b>Shortest paths in unweighted graphs.</b>",
         "Finds connected components, bipartiteness.",
         "Memory ∝ width of the frontier.",
         ("Can be huge on wide graphs.", 1)],
   "rh": "DFS — stack",
   "r": ["Follows one path as deep as possible, then backtracks.",
         "<b>Topological order, SCCs, cycle detection.</b>",
         "Finds articulation points and bridges.",
         "Memory ∝ depth of recursion.",
         ("Stack overflow on deep graphs — use an explicit stack.", 1)]},

  {"t": "bullets", "kicker": "DFS", "title": "Edge classification: where the structure is",
   "items": [
     "Record discovery and finish times. Every edge then falls into one of "
     "four classes.",
     "",
     "<b>Tree edge</b> — to an undiscovered vertex. Forms the DFS "
     "forest.",
     "<b>Back edge</b> — to an ancestor still on the stack.",
     ("<b>A back edge exists ⟺ the graph has a cycle.</b> This is the "
      "whole of cycle detection.", 1),
     "<b>Forward edge</b> — to an already-finished descendant.",
     "<b>Cross edge</b> — to a finished vertex in another subtree.",
     "",
     "In an <i>undirected</i> graph only tree and back edges can occur.",
   ],
   "note": "The cycle-detection equivalence is the single most useful fact "
           "from DFS. Worth making them prove both directions."},

  {"t": "section", "label": "Part 3", "title": "Decomposition",
   "blurb": "Two algorithms that extract global structure from one or two "
            "walks."},

  {"t": "bullets", "kicker": "Topological sort", "title": "Ordering a DAG",
   "items": [
     "An order where every edge points forward. Exists <b>iff</b> the graph "
     "is acyclic.",
     "",
     "<b>Method 1 (DFS):</b> output vertices in reverse order of finishing "
     "time.",
     ("A vertex finishes only after everything it points to has finished.", 1),
     "",
     "<b>Method 2 (Kahn):</b> repeatedly remove a vertex with in-degree 0.",
     ("Detects cycles naturally — if vertices remain but none has "
      "in-degree 0, there is a cycle.", 1),
     "",
     "Build systems, task schedulers, spreadsheet recalculation, course "
     "prerequisites, shader compilation order.",
   ]},

  {"t": "bullets", "kicker": "SCCs", "title": "Strongly connected components",
   "items": [
     "An SCC is a maximal set where every vertex reaches every other.",
     "Contracting each SCC to a node yields the <b>condensation</b> — "
     "always a DAG.",
     "",
     "<b>Kosaraju:</b> DFS to get finish times, reverse all edges, DFS again "
     "in decreasing finish order.",
     ("Two passes, O(V + E), and remarkably short to implement.", 1),
     "",
     "<b>Tarjan:</b> one pass using low-link values. Faster in practice.",
     "",
     "Uses: deadlock detection, 2-SAT, module cycles, dataflow analysis.",
   ],
   "footnote": "That a DAG always falls out of contraction is the useful part "
               "— it means you can topologically sort any graph's "
               "components."},

  {"t": "table", "kicker": "Summary", "title": "One or two walks, this much structure",
   "header": ["Want", "Use", "Cost"],
   "widths": [4.6, 4.0, 3.5],
   "rows": [
     ["Shortest path, unweighted", "BFS", "O(V + E)"],
     ["Connected components", "BFS or DFS", "O(V + E)"],
     ["Is it bipartite?", "BFS, 2-colour by level", "O(V + E)"],
     ["Does it have a cycle?", "DFS, look for a back edge", "O(V + E)"],
     ["Topological order", "DFS reverse finish, or Kahn", "O(V + E)"],
     ["Strongly connected components", "Kosaraju or Tarjan", "O(V + E)"],
     ["Articulation points, bridges", "DFS with low-link", "O(V + E)"],
   ],
   "note": "Everything here is linear. Graph search is unusually generous "
           "that way, which is why modelling a problem as a graph is so "
           "often worth the effort."},

  {"t": "callout", "title": "The real skill is recognition",
   "kind": "What to take away",
   "body": ["These algorithms are short and you will not write most of them "
            "from scratch. The skill worth building is noticing that a "
            "problem <i>is</i> a graph problem.",
            "Build order, deadlock, type inference, dependency resolution, "
            "mesh connectivity, render-graph scheduling, state machines, "
            "word ladders, puzzle solving — all of these are graph "
            "search wearing other clothes.",
            "Once you see the graph, the algorithm is usually a lookup in the "
            "table above."]},
 ],
 "takeaways": [
   "Adjacency list for sparse graphs, matrix for dense. Most real graphs are "
   "sparse.",
   "BFS and DFS are the same algorithm with a different container: queue "
   "versus stack.",
   "BFS gives shortest paths in unweighted graphs and explores by distance; "
   "DFS gives ordering and connectivity structure.",
   "A back edge exists if and only if the graph has a cycle. That is cycle "
   "detection in full.",
   "Topological order exists iff the graph is a DAG, and reverse DFS finish "
   "order produces one.",
   "Contracting strongly connected components always yields a DAG. "
   "Everything in this module is O(V + E).",
 ],
 "notes": [
  ("h1", "1 &nbsp; Representation"),
  ("p", "A graph is vertices and edges, and the first engineering decision is "
        "how to store them. The answer depends almost entirely on density."),
  ("table", ["Operation", "Adjacency list", "Adjacency matrix"],
   [["Space", "&Theta;(V + E)", "&Theta;(V&#178;)"],
    ["Test whether (u,v) is an edge", "&Theta;(deg u)", "&Theta;(1)"],
    ["Enumerate u's neighbours", "&Theta;(deg u) — optimal",
     "&Theta;(V) — you scan a whole row"],
    ["Add an edge", "&Theta;(1)", "&Theta;(1)"],
    ["Remove an edge", "&Theta;(deg u)", "&Theta;(1)"]],
   [0.28, 0.36, 0.36]),
  ("callout", "Ask which regime you are in",
   ["<b>Sparse</b>: E = &Theta;(V). Road networks, 3D meshes, package "
    "dependency graphs, social graphs, the web. Here O(V + E) really is "
    "linear, and the adjacency matrix would waste enormous space.",
    "<b>Dense</b>: E = &Theta;(V&#178;). Distance matrices, complete graphs, "
    "all-pairs problems. Here O(V + E) is quadratic, and a matrix may be both "
    "simpler and faster.",
    "Quoting 'O(V + E)' without saying which regime applies is how people "
    "convince themselves a quadratic algorithm is linear."]),
  ("p", "Almost all real graphs are sparse, and the adjacency list is the "
        "default. A practical refinement for performance-critical code is "
        "<b>compressed sparse row</b>: two flat arrays, one of neighbour "
        "lists concatenated and one of start offsets. It has the same "
        "asymptotics and far better cache behaviour than a list of lists."),

  ("h1", "2 &nbsp; One algorithm, two containers"),
  ("code", """def traverse(G, s, container):
    seen = {s}
    container.add(s)
    while container:
        u = container.remove()        # the only difference
        for v in G[u]:
            if v not in seen:
                seen.add(v)
                container.add(v)

# queue (FIFO) -> BFS;  stack (LIFO) -> DFS"""),
  ("p", "Both visit every reachable vertex once and examine every incident "
        "edge once, so both are O(V + E). Swapping the container changes the "
        "order of exploration, the shape of the resulting tree, and the "
        "properties you can extract — which is a surprising amount of "
        "consequence for a one-line change."),
  ("h2", "2.1 &nbsp; BFS"),
  ("p", "A queue explores all vertices at distance 1, then all at distance 2, "
        "and so on. This gives the defining property: <b>BFS computes "
        "shortest paths in unweighted graphs</b>, because a vertex is first "
        "reached along a path of minimum edge count."),
  ("ul", ["Shortest paths (unweighted), and the distance to every reachable "
          "vertex.",
          "Connected components, by restarting from each unvisited vertex.",
          "Bipartiteness: two-colour by BFS level; an edge within a level "
          "means an odd cycle, so not bipartite.",
          "Memory is proportional to the <i>frontier width</i>, which on a "
          "wide shallow graph can approach V."]),
  ("h2", "2.2 &nbsp; DFS"),
  ("p", "A stack follows one path as far as it goes before backtracking. The "
        "interesting structure comes from recording <b>discovery</b> and "
        "<b>finish</b> times for each vertex, which lets every edge be "
        "classified."),
  ("table", ["Edge type", "Points to", "Meaning"],
   [["Tree", "An undiscovered vertex", "Part of the DFS forest."],
    ["Back", "An ancestor still on the stack",
     "<b>A cycle.</b> A directed graph has a cycle if and only if DFS finds a "
     "back edge."],
    ["Forward", "An already-finished descendant",
     "A shortcut down the tree. Cannot occur in undirected graphs."],
    ["Cross", "A finished vertex in another subtree",
     "Between branches. Cannot occur in undirected graphs."]],
   [0.13, 0.30, 0.57]),
  ("callout", "Cycle detection in full",
   ["A directed graph contains a cycle <b>if and only if</b> a DFS from any "
    "starting set discovers a back edge.",
    "(&rArr;) A back edge u &rarr; v means v is an ancestor of u, so the tree "
    "path from v to u plus that edge forms a cycle.",
    "(&lArr;) If a cycle exists, consider the first of its vertices to be "
    "discovered; every other vertex on the cycle is reachable from it along "
    "undiscovered vertices, so all become its descendants, and the cycle edge "
    "returning to it is a back edge.",
    "Memorise the equivalence. It is the basis of deadlock detection, build "
    "cycle errors, and recursive type checking."]),

  ("break",),
  ("h1", "3 &nbsp; Topological sort"),
  ("p", "A linear ordering of vertices in which every edge points forward. It "
        "exists precisely when the graph is acyclic — a cycle has no "
        "consistent ordering."),
  ("h2", "3.1 &nbsp; Two methods"),
  ("ul", ["<b>DFS.</b> Output vertices in decreasing order of finish time. A "
          "vertex finishes only after every vertex it points to has finished, "
          "so a later finish time means an earlier position in the order.",
          "<b>Kahn's algorithm.</b> Repeatedly output any vertex with "
          "in-degree 0 and remove it. If vertices remain but none has "
          "in-degree 0, the remainder contains a cycle — which makes "
          "cycle reporting natural, and is why build systems tend to use "
          "this form."]),
  ("p", "Applications are everywhere: build systems, task schedulers, "
        "spreadsheet recalculation order, course prerequisite chains, "
        "instruction scheduling, shader and render-pass ordering. Any time "
        "something must happen before something else, you have a DAG and this "
        "is the algorithm."),

  ("h1", "4 &nbsp; Strongly connected components"),
  ("p", "In a directed graph, u and v are <b>strongly connected</b> if each "
        "reaches the other. This is an equivalence relation, so it partitions "
        "the vertices into <b>strongly connected components</b>."),
  ("callout", "The condensation is always a DAG",
   ["Contract each SCC to a single node. The resulting graph is guaranteed "
    "acyclic — if it had a cycle, all the components on that cycle would "
    "be mutually reachable and would therefore have been one component.",
    "This is genuinely useful: it means <i>any</i> directed graph can be "
    "decomposed into a DAG of strongly connected pieces, and then "
    "topologically sorted at the component level. Dataflow analysis and "
    "module dependency resolution both rely on exactly this."]),
  ("h2", "4.1 &nbsp; Kosaraju"),
  ("ol", ["Run DFS on G, pushing each vertex onto a stack as it finishes.",
          "Reverse every edge to form G&#7488;.",
          "Pop vertices from the stack; each DFS in G&#7488; from an unvisited "
          "popped vertex yields exactly one SCC."]),
  ("p", "Two passes, O(V + E), and about twenty lines of code. Tarjan's "
        "algorithm achieves the same in a single pass using low-link values "
        "and is faster in practice, at the cost of being harder to remember. "
        "Learn Kosaraju for understanding; use Tarjan when it matters."),
  ("p", "Applications: deadlock detection, 2-SAT (satisfiable iff no variable "
        "shares an SCC with its negation), finding circular module "
        "dependencies, and loop identification in compiler dataflow "
        "analysis."),

  ("h1", "5 &nbsp; The table to remember"),
  ("table", ["Question", "Algorithm", "Cost"],
   [["Shortest path in an unweighted graph", "BFS", "O(V + E)"],
    ["Connected components", "BFS or DFS from each unvisited vertex", "O(V + E)"],
    ["Is the graph bipartite?", "BFS, two-colour by level", "O(V + E)"],
    ["Does a directed graph have a cycle?", "DFS, detect a back edge", "O(V + E)"],
    ["Valid execution order", "Topological sort (DFS or Kahn)", "O(V + E)"],
    ["Mutually reachable groups", "Kosaraju or Tarjan", "O(V + E)"],
    ["Single points of failure", "DFS with low-link (articulation points, "
     "bridges)", "O(V + E)"]],
   [0.42, 0.37, 0.21]),
  ("callout", "What is actually worth learning here",
   ["Every algorithm in this module is linear and short. You will rarely "
    "implement them from scratch — they are in every standard library "
    "and every graph package.",
    "The durable skill is <b>recognition</b>: noticing that build ordering, "
    "deadlock, type inference, dependency resolution, mesh connectivity, "
    "render-graph scheduling, state machines, and puzzle solving are all "
    "graph search in disguise.",
    "Once you see the graph, the algorithm is a table lookup. Getting to the "
    "graph is the work."]),
 ],
 "resources": [
   ("MIT 6.006 — Graphs, BFS, DFS, Topological Sort",
    "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
    "Careful development of both traversals and the properties each yields."),
   ("Jeff Erickson, Algorithms — Depth-First Search chapter",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "The best free treatment of edge classification and SCCs, with proofs "
    "that are actually readable."),
   ("Competitive Programmer's Handbook — Graph chapters",
    "https://cses.fi/book/book.pdf",
    "Implementation-focused, with the practical details (CSR layout, "
    "iterative DFS) that theory courses omit."),
   ("CSES Problem Set — Graph Algorithms section",
    "https://cses.fi/problemset/",
    "Around 35 auto-graded problems covering exactly this module. The best "
    "free practice available."),
 ],
 "exercises": [
   "Implement a graph with both adjacency list and adjacency matrix. Measure "
   "neighbour iteration and edge-existence queries on a sparse and a dense "
   "graph, and confirm the predicted crossover.",
   "Implement BFS and DFS from the single <code>traverse</code> skeleton, "
   "differing only in the container. Verify both visit the same vertex set.",
   "Use BFS to test bipartiteness. Construct a graph with an odd cycle and "
   "confirm detection.",
   "Implement DFS with discovery and finish times and classify every edge. "
   "Verify on a directed graph that back edges appear exactly when a cycle "
   "exists.",
   "Implement topological sort both ways — reverse DFS finish order and "
   "Kahn's algorithm. Make the Kahn version report the cycle when one exists.",
   "Implement Kosaraju's algorithm. Verify that contracting the components "
   "yields a DAG by running your cycle detector on the condensation.",
   "Convert a recursive DFS to an explicit-stack iterative version and "
   "demonstrate that it survives a path graph of 10&#8310; vertices where the "
   "recursive one overflows.",
 ],
 "selfcheck": [
   "When would you choose an adjacency matrix, and what does E = &Theta;(V) "
   "versus &Theta;(V&#178;) change about the complexity O(V + E)?",
   "BFS and DFS differ in one line. What is it, and what consequences follow?",
   "What exactly does BFS compute that DFS does not, and why?",
   "State and prove both directions of the back-edge / cycle equivalence.",
   "Why does reverse DFS finish order produce a valid topological order?",
   "Why is the condensation of a directed graph always a DAG, and why is that "
   "useful?",
 ],
},

]
