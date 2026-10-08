# -*- coding: utf-8 -*-
"""UC MATH 600 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Trees and Connectivity",
 "subtitle": "The structure every data structure course assumes.",
 "question": "Why does a tree on n vertices always have n − 1 "
             "edges?",
 "outcomes": [
     "Give the equivalent characterisations of a tree.",
     "Prove the edge-count theorem.",
     "Explain spanning trees and why they exist.",
     "Explain rooted trees, height, and node counts.",
     "Connect this to the data structures ahead.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a tree is",
   "blurb": "Five definitions, all the same."},

  {"t": "callout", "title": "A tree is a connected graph with no cycles — and four other statements that are equivalent to it",
   "kind": "The characterisations, which are used interchangeably",
   "body": ["<b>Connected and acyclic</b> is the usual "
            "definition. <b>Connected with exactly n − 1 "
            "edges</b> is equivalent. <b>Acyclic with exactly n − 1 "
            "edges</b> is equivalent.",
            "<b>And: a unique path between every pair of "
            "vertices</b> — which is the characterisation that "
            "explains why trees are useful for "
            "routing.",
            "<b>And: minimally connected</b> — <b>removing any edge "
            "disconnects it</b>, and adding any edge creates exactly "
            "one cycle.",
            "<b>All five are the same property</b>, and <b>proving "
            "the equivalences is the standard exercise</b> — which is "
            "worth doing once, because later courses switch between them "
            "without comment."]},

  {"t": "section", "label": "Part 2", "title": "The edge count",
   "blurb": "Proved by induction, which is the model proof."},

  {"t": "code", "kicker": "Proof", "title": "Every tree on n vertices has n − 1 edges",
   "lang": "text", "code": """
  CLAIM: a tree with n >= 1 vertices has n - 1 edges.

  BASE CASE. n = 1: one vertex, no edges. 1 - 1 = 0.

  INDUCTIVE STEP. Suppose every tree on n vertices
  has n - 1 edges. Let T be a tree on n + 1.

    1  T has a leaf (a vertex of degree 1).
       WHY: follow a longest path; its endpoint
       cannot continue (no repeats) and cannot
       branch back (no cycles), so it has degree 1.
       <-- this is the step people skip, and it is
           the only interesting part of the proof

    2  Delete that leaf and its one edge. The result
       is still connected (the leaf was on no path
       between other vertices) and still acyclic.
       So it is a tree on n vertices.

    3  By the hypothesis it has n - 1 edges.
       Add back the one we removed: n edges.

  So T has (n + 1) - 1 edges.  By induction, done. []
""",
   "caption": "<b>Step 1 is the only interesting part</b>, and it is "
              "the step most people assert rather than prove — which "
              "is Module 03's five errors in "
              "miniature.",
   "note": "Write this proof out yourself; it is the model for every "
           "tree argument later."},

  {"t": "section", "label": "Part 3", "title": "Spanning trees",
   "blurb": "Which always exist, and that is useful."},

  {"t": "callout", "title": "Every connected graph contains a spanning tree, and the proof is an algorithm",
   "kind": "Existence by construction",
   "body": ["<b>A spanning tree is a subgraph that is a tree and "
            "includes every vertex</b> — <b>the minimal structure that "
            "keeps the graph connected.</b>",
            "<b>And it always exists:</b> <b>while a cycle remains, "
            "delete one of its edges</b> — <b>connectivity is "
            "preserved because the rest of the cycle still joins the "
            "endpoints</b> — <b>and terminate when acyclic.</b>",
            "<b>Which is a constructive existence proof</b> "
            "(Module 02 §4) — and <b>the construction is the "
            "algorithm</b>, which is a pattern worth "
            "noticing.",
            "<b>Plus: a connected graph on n vertices has at least "
            "n − 1 edges</b>, which follows immediately — <b>and that "
            "bound is used constantly in complexity "
            "arguments.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Rooted trees",
   "blurb": "Which is what a data structure actually is."},

  {"t": "bullets", "kicker": "Rooted", "title": "The counting facts the data structures courses assume",
   "items": [
     "<b>Pick a root, and every vertex has a unique "
     "parent</b> — because there is a unique path to the root "
     "(Part 1).",
     "",
     "<b>A binary tree of height h has at most 2^(h+1) − 1 "
     "nodes</b>, so <b>a tree with n nodes has height at least "
     "log₂(n+1) − 1</b> — which is the lower bound every "
     "balanced-tree argument rests on.",
     "",
     "<b>And at least h + 1 nodes</b>, achieved by a path — "
     "<b>which is why unbalanced trees degrade to linear "
     "time</b>.",
     "",
     "<b>A binary tree with n internal nodes has n + 1 external "
     "ones</b>, which is a double count and is used in parsing and in "
     "coding arguments.",
     "",
     "<b>And the depth sum determines the search cost</b>, which "
     "is what CSCE 629's balanced trees are optimising.",
   ],
   "footnote": "<b>Height at least log₂(n+1) − 1</b> is the "
               "bound every balanced-tree argument rests on — and it "
               "is a counting argument, not an algorithmic "
               "one."},

  {"t": "callout", "title": "And this is where the program's data structures start",
   "kind": "Closing",
   "body": ["<b>Binary search trees, heaps, tries, B-trees, and "
            "BVHs are all rooted trees</b> — <b>and every bound on "
            "them is one of Part 4's counting "
            "facts.</b>",
            "<b>Including the graphics ones:</b> <b>a bounding "
            "volume hierarchy is a binary tree, and its traversal cost "
            "is its depth</b> (CSCE 647 §04).",
            "<b>So the balanced-tree machinery of CSCE 629 is "
            "entirely about forcing the height toward the "
            "lower bound</b> — which this module "
            "establishes and that course achieves.",
            "<b>Which is the pattern of this whole "
            "prerequisite:</b> <b>the bound comes from counting, and "
            "the algorithm is the attempt to meet it.</b>"]},
 ],
 "takeaways": [
   "Five characterisations of a tree are equivalent, and later courses "
   "switch between them without comment.",
   "Every tree has a leaf, proved by taking a longest path — and this "
   "is the step people assert rather than prove.",
   "Every connected graph contains a spanning tree, and the proof is an "
   "algorithm.",
   "A connected graph on n vertices has at least n − 1 edges.",
   "Height at least log₂(n+1) − 1 is the bound every balanced-tree "
   "argument rests on.",
   "The bound comes from counting, and the algorithm is the attempt to meet "
   "it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a tree is"),
  ("callout", "A tree is a connected graph with no cycles — and four "
              "other statements that are equivalent to it",
   ["<b>Connected and acyclic</b> is the usual "
    "definition. <b>Connected with exactly n &minus; 1 edges</b> is "
    "equivalent to it. <b>Acyclic with exactly n &minus; 1 edges</b> is "
    "equivalent to it as well — note that each of those drops a "
    "condition and adds the edge count.",
    "<b>And: there is a unique path between every pair of "
    "vertices</b> — <b>which is the characterisation that explains "
    "why trees are useful for routing and addressing</b>, since there "
    "is never a choice to make.",
    "<b>And: minimally connected</b> — <b>removing any edge "
    "disconnects the graph</b>, and symmetrically <b>adding any edge "
    "creates exactly one cycle</b>, which is the characterisation "
    "&sect;3 uses.",
    "<b>All five describe the same property</b>, and <b>proving the "
    "equivalences is the standard exercise</b> — <b>which is worth "
    "doing once</b>, because <b>later courses switch between them "
    "without comment</b> and expect you to follow."]),

  ("h1", "2 &nbsp; The edge count"),
  ("code", """CLAIM: a tree with n >= 1 vertices has n - 1 edges.

BASE CASE. n = 1: one vertex, no edges. 1 - 1 = 0.

INDUCTIVE STEP. Suppose every tree on n vertices has
n - 1 edges. Let T be a tree on n + 1 vertices.

  1  T has a leaf (a vertex of degree 1).
     WHY: follow a longest path in T; its endpoint
     cannot continue (that would make a longer path)
     and cannot have another edge back into the path
     (that would make a cycle), so it has degree 1.
     <-- this is the step people skip, and it is the
         only interesting part of the whole proof

  2  Delete that leaf and its single edge. The
     result is still connected (the leaf lay on no
     path between other vertices) and still acyclic
     (deleting never creates a cycle). So it is a
     tree on n vertices.

  3  By the inductive hypothesis it has n - 1 edges.
     Add back the edge we removed: n edges.

So T has (n + 1) - 1 edges.  By induction, done. []"""),
  ("p", "<b>Step 1 is the only interesting part of this proof</b>, "
        "<b>and it is the step most people assert rather than "
        "prove</b> — 'obviously a tree has a leaf' — <b>which "
        "is Module 03's five errors and Module 01 &sect;1's "
        "'obviously' warning, both in miniature</b>. <b>Write this "
        "proof out yourself</b>; it is the model for essentially every "
        "tree argument in the rest of the program, and the "
        "delete-a-leaf-and-apply-the-hypothesis move recurs "
        "constantly."),

  ("break",),
  ("h1", "3 &nbsp; Spanning trees"),
  ("callout", "Every connected graph contains a spanning tree, and the proof "
              "is an algorithm",
   ["<b>A spanning tree is a subgraph that is a tree and includes "
    "every vertex of the original</b> — <b>the minimal structure "
    "that keeps the graph connected</b>, with no redundancy left in "
    "it.",
    "<b>And one always exists, which is proved by "
    "construction:</b> <b>while any cycle remains, delete one edge of "
    "it</b> — <b>connectivity is preserved because the rest of "
    "that cycle still joins the deleted edge's endpoints</b> — "
    "<b>and stop when the graph is acyclic</b>, which must happen since "
    "each step removes an edge.",
    "<b>Which is a constructive existence proof</b> (Module 02 "
    "&sect;4's first flavour) — and <b>the construction <i>is</i> "
    "the algorithm</b>, <b>which is a pattern worth noticing</b> and "
    "which CSCE 629 relies on repeatedly: a good existence proof "
    "usually hands you an implementation.",
    "<b>Plus an immediate corollary: a connected graph on n "
    "vertices has at least n &minus; 1 edges</b>, since it contains a "
    "spanning tree — <b>and that bound is used constantly in "
    "complexity arguments</b> to justify writing O(E) rather than "
    "O(V + E)."]),

  ("h1", "4 &nbsp; Rooted trees"),
  ("ul", ["<b>Pick any vertex as the root, and every other vertex "
          "has a unique parent</b> — <b>because there is a unique "
          "path to the root</b> (&sect;1's fourth characterisation), and "
          "the parent is the first step along it. <b>An unrooted tree "
          "becomes a data structure the moment you choose a "
          "root.</b>",
          "<b>A binary tree of height h has at most "
          "2<sup>h+1</sup> &minus; 1 nodes</b> (a geometric sum over "
          "the levels), <b>so a tree with n nodes has height at least "
          "log<sub>2</sub>(n+1) &minus; 1</b> — <b>which is the "
          "lower bound every balanced-tree argument rests on</b>, and "
          "it is a counting fact rather than an algorithmic one.",
          "<b>And at least h + 1 nodes</b>, achieved by a path "
          "— <b>which is precisely why unbalanced trees degrade to "
          "linear time</b>: a tree can be as tall as it has "
          "nodes.",
          "<b>A binary tree with n internal nodes has n + 1 external "
          "(leaf) nodes</b>, <b>which is a double count</b> "
          "(Module 06 &sect;3) and <b>is used in parsing arguments "
          "and in the analysis of prefix codes</b>.",
          "<b>And the sum of the node depths determines the total "
          "search cost</b>, <b>which is what CSCE 629's balanced trees "
          "are actually optimising</b> — not the height alone, "
          "though bounding the height bounds the sum."]),
  ("callout", "And this is where the program's data structures start",
   ["<b>Binary search trees, heaps, tries, B-trees, and bounding "
    "volume hierarchies are all rooted trees</b> — <b>and every "
    "performance bound on them is one of &sect;4's counting "
    "facts</b> dressed in the vocabulary of the particular "
    "structure.",
    "<b>Including the graphics ones:</b> <b>a bounding volume "
    "hierarchy is a binary tree, and its traversal cost is its "
    "depth</b> (CSCE 647 Module 04's acceleration structures, and "
    "CSCE 620's spatial partitioning) — which is why a badly "
    "built BVH costs you the same way a badly built search tree "
    "does.",
    "<b>So the whole balanced-tree machinery of CSCE 629 is about "
    "forcing the height down toward the lower bound</b> — "
    "<b>which this module establishes and that course achieves</b>, "
    "and seeing the division of labour makes both easier.",
    "<b>Which is the pattern of this entire prerequisite:</b> "
    "<b>the bound comes from counting, and the algorithm is the attempt "
    "to meet it</b> — Module 09 makes that division explicit "
    "and it holds for the rest of the program."]),
 ],
 "resources": [
   ("Lehman, Leighton & Meyer, chapter 12 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>&sect;&sect;1 to 3</b>, free — trees and the equivalence "
    "proofs, done carefully."),
   ("MIT 6.042J, the trees lecture (free video)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/video_galleries/video-lectures/",
    "<b>&sect;&sect;1 and 2</b> — with the leaf argument of "
    "&sect;2 made explicit."),
   ("CLRS, the tree and heap chapters (library copy)",
    "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/",
    "<b>&sect;4</b> — where these counting facts become data "
    "structure bounds, which is CSCE 629."),
   ("Sedgewick & Wayne, Algorithms (free site and lectures)",
    "https://algs4.cs.princeton.edu/home/",
    "<b>&sect;4 implemented</b> — free, with code, and a good way to "
    "see the bounds hold empirically."),
 ],
 "exercises": [
   "<b>Prove two of the five characterisations equivalent</b>, both "
   "directions.",
   "<b>Prove every tree has a leaf</b>, carefully.",
   "<b>Write the edge-count induction out in full</b>, with all three "
   "of Module 03's requirements visible.",
   "<b>Construct a spanning tree</b> by the deletion algorithm.",
   "<b>Count the spanning trees</b> of a small graph by hand.",
   "<b>Derive the maximum node count</b> of a binary tree of "
   "height h.",
   "<b>Derive the minimum height</b> for n nodes.",
   "<b>Prove the internal-external node identity</b> by double "
   "counting.",
   "<b>Build an unbalanced BST</b> and measure its search cost "
   "against the bound.",
   "<b>Find the tree bound</b> behind one data structure you already "
   "use.",
 ],
 "selfcheck": [
   "Give five equivalent definitions of a tree.",
   "Why does every tree have a leaf?",
   "Prove the edge-count theorem.",
   "Which step is the interesting one, and why is it skipped?",
   "What is a spanning tree, and why does one always exist?",
   "What is the corollary about edge counts?",
   "Give the node-count bounds for a binary tree of height h.",
   "What is the minimum height for n nodes, and where is it used?",
   "State the internal-external identity.",
   "State the module's closing pattern.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Asymptotics",
 "subtitle": "What CSCE 629 is actually about.",
 "question": "What does O(n log n) mean, precisely?",
 "outcomes": [
     "State the definitions of O, Ω, and Θ precisely.",
     "Prove an asymptotic bound from the definition.",
     "Compare growth rates reliably.",
     "Explain what asymptotic analysis hides.",
     "Use the notation without the standard abuses.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The definitions",
   "blurb": "Which are about eventual behaviour, with constants."},

  {"t": "eq", "kicker": "Definitions", "title": "The three, stated exactly",
   "eqs": [
     ("f(n) = O(g(n)): there exist c > 0 and n₀ with "
      "f(n) ≤ c·g(n) for all n ≥ n₀",
      "An upper bound, eventually, up to a constant. The c and the "
      "n₀ are what you must exhibit to prove it."),
     ("f(n) = Ω(g(n)): same with f(n) ≥ c·g(n)",
      "A lower bound. Used far less often than it should be, and it "
      "is what a hardness result actually proves."),
     ("f(n) = Θ(g(n)): both at once, with different constants",
      "A tight bound. This is usually what you mean when you say "
      "'the algorithm is O(n log n)' — and saying O is weaker."),
   ],
   "caption": "<b>Exhibit the constant and the threshold</b> — "
              "that is what proving an asymptotic bound means, and "
              "intuition about growth is not a "
              "proof.",
   "note": "Project 2 requires asymptotic proofs that exhibit c and "
           "n₀ explicitly."},

  {"t": "callout", "title": "And the notation is an abuse that everybody commits, which is worth understanding once",
   "kind": "Why 'f = O(g)' is not an equation",
   "body": ["<b>O(g) is a <i>set</i> of functions</b>, and "
            "<b>'f = O(g)' really means 'f ∈ O(g)'</b> — which is why "
            "the relation is not symmetric and why you cannot "
            "cancel.",
            "<b>So 'O(n) = O(n²)' is true read left to right and "
            "false read right to left</b>, which is the clearest sign "
            "that the equals sign is doing something "
            "unusual.",
            "<b>And n² + O(n) means 'n² plus some function in "
            "O(n)'</b> — which is useful shorthand and is the "
            "reason the abuse survives.",
            "<b>So read it as 'is' rather than 'equals'</b> — "
            "<b>and never manipulate an O-expression as though it were "
            "an equation</b>, which is where the standard errors come "
            "from."]},

  {"t": "section", "label": "Part 2", "title": "Proving a bound",
   "blurb": "Which is mechanical once you know the shape."},

  {"t": "code", "kicker": "Proof", "title": "The shape of an asymptotic proof",
   "lang": "text", "code": """
  CLAIM: 3n^2 + 7n + 2 = O(n^2).

  PROOF. Take c = 12 and n0 = 1.
  For n >= 1 we have n <= n^2 and 1 <= n^2, so
      3n^2 + 7n + 2 <= 3n^2 + 7n^2 + 2n^2 = 12n^2.
  Hence f(n) <= 12 n^2 for all n >= 1.  []

  THAT IS THE WHOLE TECHNIQUE
      bound every lower-order term by the leading one
      add up the coefficients
      and that sum is your c

  FOR A LOWER BOUND
      CLAIM: 3n^2 + 7n + 2 = Omega(n^2).
      Take c = 3 and n0 = 1: the other terms are
      positive, so f(n) >= 3n^2.  []

  AND THEREFORE Theta(n^2), by both together.
  Two short proofs, and the tight bound follows.
""",
   "caption": "<b>Bound every lower-order term by the leading "
              "one</b>, add the coefficients, and that sum is your "
              "constant — which is the whole "
              "technique.",
   "note": "Lower bounds are usually easier than upper bounds and "
           "are usually omitted."},

  {"t": "section", "label": "Part 3", "title": "Comparing growth",
   "blurb": "The ordering you should know cold."},

  {"t": "table", "kicker": "Growth", "title": "The hierarchy, slowest to fastest",
   "header": ["Growth", "Example", "At n = 1,000,000"],
   "widths": [3.0, 3.8, 4.2],
   "rows": [
     ["<b>O(1)</b>", "<b>Hash lookup</b>", "<b>1</b>"],
     ["<b>O(log n)</b>", "<b>Binary search</b>", "<b>~20</b>"],
     ["<b>O(n)</b>", "<b>Linear scan</b>", "<b>10⁶</b>"],
     ["<b>O(n log n)</b>", "<b>Sorting, FFT</b>", "<b>~2 × 10⁷</b>"],
     ["<b>O(n²)</b>", "<b>Naive pair comparison</b>", "<b>10¹² — already too slow</b>"],
     ["<b>O(2ⁿ)</b>", "<b>Subset enumeration</b>", "<b>Unimaginable</b>"],
   ],
   "footnote": "<b>The gap between n log n and n² is where most "
               "algorithmic work happens</b> — the others are "
               "usually decided by the problem rather than by "
               "cleverness.",
   "note": "Knowing these numbers by feel is what makes complexity "
           "claims meaningful."},

  {"t": "section", "label": "Part 4", "title": "What it hides",
   "blurb": "Which is a great deal, and matters."},

  {"t": "bullets", "kicker": "Limits", "title": "What an asymptotic bound does not tell you",
   "items": [
     "<b>The constant</b> — <b>an O(n) algorithm with a "
     "constant of 10,000 loses to an O(n log n) one with a constant of "
     "2 for every n you will ever run</b>.",
     "",
     "<b>The threshold</b> — <b>'eventually' may be past "
     "every input size that exists</b>, which is the galactic-algorithm "
     "problem.",
     "",
     "<b>The memory hierarchy</b> — <b>two O(n) algorithms "
     "can differ by a factor of fifty on cache behaviour alone</b>, "
     "which is CSCE 614's whole subject.",
     "",
     "<b>The average case</b> — <b>O is worst case unless "
     "stated</b>, and quicksort is the standard example of worst case "
     "being the wrong question.",
     "",
     "<b>So asymptotics tells you which algorithm to "
     "reach for first</b>, and <b>measurement tells you which one is "
     "faster</b> — and both are needed.",
   ],
   "footnote": "<b>Asymptotics tells you which to reach for first; "
               "measurement tells you which is faster</b> — and "
               "treating either as the whole answer is the common "
               "error."},

  {"t": "callout", "title": "And why the notation exists at all",
   "kind": "Closing",
   "body": ["<b>Because the exact step count depends on the machine, "
            "the compiler, and the day</b> — <b>and the growth rate "
            "does not.</b>",
            "<b>So asymptotics is an abstraction that discards "
            "exactly the machine-dependent part</b> — which is what "
            "makes an algorithmic claim portable and "
            "durable.",
            "<b>And the cost of the abstraction is "
            "Part 3</b>: <b>everything it discarded is "
            "sometimes the thing that matters</b>, and knowing when is "
            "experience.",
            "<b>Which is CSCE 629 and CSCE 614 in one "
            "sentence</b> — <b>one course gives you the growth rate "
            "and the other gives you the constant</b>, and the program "
            "puts them in the same semester for that "
            "reason."]},
 ],
 "takeaways": [
   "Exhibit the constant and the threshold — that is what proving an "
   "asymptotic bound means.",
   "'f = O(g)' really means 'f is in the set O(g)', which is why you cannot "
   "manipulate it as an equation.",
   "Bound every lower-order term by the leading one, add the coefficients, "
   "and that sum is your constant.",
   "Lower bounds are usually easier than upper bounds and are usually "
   "omitted.",
   "The gap between n log n and n² is where most algorithmic work "
   "happens.",
   "Asymptotics tells you which algorithm to reach for first; measurement "
   "tells you which is faster.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The definitions"),
  ("eq", "f(n) = O(g(n)):&nbsp; there exist c &gt; 0 and "
         "n<sub>0</sub> with f(n) &le; c&middot;g(n) for all "
         "n &ge; n<sub>0</sub>"),
  ("ul", ["<b>An upper bound, eventually, up to a constant "
          "factor</b> — and <b>the c and the n<sub>0</sub> are "
          "exactly what you must exhibit in order to prove the "
          "claim</b> (&sect;2).",
          "<b>f(n) = &Omega;(g(n)) is the same definition with the "
          "inequality reversed</b> — a lower bound — <b>used "
          "far less often than it should be</b>, and <b>it is what a "
          "hardness result actually proves</b> (CSCE 637's lower "
          "bounds are all &Omega; statements).",
          "<b>f(n) = &Theta;(g(n)) means both at once</b>, with "
          "possibly different constants — <b>a tight bound</b> "
          "— and <b>this is usually what you mean when you say 'the "
          "algorithm is O(n log n)'</b>, so <b>saying O is strictly "
          "weaker than what you intended</b>.",
          "<b>Exhibit the constant and the threshold</b>: <b>that "
          "is what proving an asymptotic bound means</b>, and "
          "<b>intuition about which function grows faster is not a "
          "proof</b>. <b>Project 2 requires asymptotic proofs that "
          "exhibit c and n<sub>0</sub> explicitly</b>, for exactly this "
          "reason."]),
  ("callout", "And the notation is an abuse that everybody commits, which is "
              "worth understanding once",
   ["<b>O(g) is properly a <i>set</i> of functions</b>, and "
    "<b>'f = O(g)' really means 'f &isin; O(g)'</b> — <b>which is "
    "why the relation is not symmetric and why you cannot cancel terms "
    "across it</b>.",
    "<b>So 'O(n) = O(n<super>2</super>)' is a true statement read "
    "left to right and a false one read right to left</b> — "
    "<b>which is the clearest available sign that the equals sign is "
    "doing something unusual here</b>, since equality is symmetric and "
    "this is not.",
    "<b>And an expression like n<super>2</super> + O(n) means "
    "'n<super>2</super> plus some function that is in O(n)'</b> — "
    "<b>which is genuinely useful shorthand</b>, and is the reason the "
    "abuse has survived a century of complaints about it.",
    "<b>So read the sign as 'is' rather than 'equals'</b> — "
    "<b>and never manipulate an O-expression as though it were an "
    "equation</b>, <b>which is where the standard errors come "
    "from</b> (subtracting O(n) from both sides, for instance, is "
    "meaningless)."]),

  ("h1", "2 &nbsp; Proving a bound"),
  ("code", """CLAIM: 3n^2 + 7n + 2 = O(n^2).

PROOF. Take c = 12 and n0 = 1.
For n >= 1 we have n <= n^2 and 1 <= n^2, so
    3n^2 + 7n + 2 <= 3n^2 + 7n^2 + 2n^2 = 12n^2.
Hence f(n) <= 12 n^2 for all n >= 1.  []

THAT IS THE WHOLE TECHNIQUE
    bound every lower-order term by the leading one
    add up the coefficients
    and that sum is your c

FOR A LOWER BOUND
    CLAIM: 3n^2 + 7n + 2 = Omega(n^2).
    Take c = 3 and n0 = 1: the remaining terms are
    positive, so f(n) >= 3n^2 immediately.  []

AND THEREFORE Theta(n^2), by both together.
Two short proofs, and the tight bound follows."""),
  ("p", "<b>Bound every lower-order term by the leading one, add the "
        "coefficients, and that sum is your constant</b> — <b>which "
        "is the whole technique</b> for polynomials, and it adapts "
        "directly to anything else you can bound termwise. <b>Lower "
        "bounds are usually easier than upper bounds and are usually "
        "omitted</b>, which is a shame: the &Omega; proof above is two "
        "lines, and quoting &Theta; instead of O is a strictly stronger "
        "and more useful claim."),

  ("break",),
  ("h1", "3 &nbsp; Comparing growth"),
  ("table", ["Growth", "Typical example", "At n = 1,000,000"],
   [["<b>O(1)</b>", "<b>Hash lookup, array index.</b>", "<b>1</b>"],
    ["<b>O(log n)</b>", "<b>Binary search, balanced tree lookup.</b>",
     "<b>About 20.</b>"],
    ["<b>O(n)</b>", "<b>Linear scan, counting.</b>",
     "<b>10<super>6</super></b>"],
    ["<b>O(n log n)</b>", "<b>Comparison sorting, FFT.</b>",
     "<b>About 2 &times; 10<super>7</super></b> — still entirely "
     "fine."],
    ["<b>O(n<super>2</super>)</b>",
     "<b>Naive all-pairs comparison.</b>",
     "<b>10<super>12</super></b> — already too slow, by a lot."],
    ["<b>O(2<super>n</super>)</b>",
     "<b>Enumerating all subsets.</b>",
     "<b>Unimaginable</b> — and this is why CSCE 637 "
     "exists."]],
   [0.22, 0.38, 0.40]),
  ("p", "<b>The gap between n log n and n<super>2</super> is where "
        "most algorithmic work happens</b> — <b>the others are "
        "usually decided by the problem rather than by cleverness</b> "
        "(you cannot sort in O(n) by comparisons, and you cannot search "
        "an unsorted array in less than O(n)). <b>Knowing these numbers "
        "by feel is what makes a complexity claim meaningful</b> rather "
        "than decorative: 'quadratic' should immediately read as 'not at "
        "a million'."),

  ("h1", "4 &nbsp; What it hides"),
  ("ul", ["<b>The constant factor</b> — <b>an O(n) algorithm "
          "with a constant of 10,000 loses to an O(n log n) one with a "
          "constant of 2 for every input size you will ever actually "
          "run</b>, and the asymptotic comparison says the opposite.",
          "<b>The threshold n<sub>0</sub></b> — "
          "<b>'eventually' may begin past every input size that will "
          "ever exist</b>, <b>which is the galactic-algorithm "
          "problem</b>: asymptotically superior methods that are never "
          "worth running.",
          "<b>The memory hierarchy</b> — <b>two O(n) "
          "algorithms can differ by a factor of fifty on cache behaviour "
          "alone</b>, <b>which is CSCE 614's entire subject</b> and is "
          "invisible to this notation.",
          "<b>The distinction between worst, average, and amortised "
          "case</b> — <b>O is worst case unless stated "
          "otherwise</b>, and <b>quicksort is the standard example of "
          "the worst case being the wrong question</b> (quadratic worst "
          "case, n log n expected, and it wins in practice).",
          "<b>So asymptotics tells you which algorithm to reach for "
          "first, and measurement tells you which one is actually "
          "faster</b> — <b>and both are needed</b>; <b>treating "
          "either as the whole answer is the common error</b>, in "
          "opposite directions."]),
  ("callout", "And why the notation exists at all",
   ["<b>Because the exact step count depends on the machine, the "
    "compiler, the libraries, and the day</b> — <b>and the growth "
    "rate does not.</b> A claim about growth survives a hardware "
    "generation; a claim about milliseconds does not.",
    "<b>So asymptotic analysis is an abstraction that discards "
    "precisely the machine-dependent part</b> — <b>which is what "
    "makes an algorithmic claim portable and durable</b>, and is why "
    "the field can have results rather than only benchmarks.",
    "<b>And the cost of that abstraction is &sect;4</b>: "
    "<b>everything it discarded is sometimes the thing that "
    "matters</b>, and <b>knowing when is experience</b> rather than "
    "theory.",
    "<b>Which is CSCE 629 and CSCE 614 in one sentence</b> — "
    "<b>one course gives you the growth rate and the other gives you "
    "the constant</b> — and <b>the program puts them in the same "
    "semester for exactly that reason.</b>"]),
 ],
 "resources": [
   ("CLRS, chapter 3 (library copy)",
    "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/",
    "<b>&sect;&sect;1 and 2</b> — the definitions in the form "
    "CSCE 629 uses, with the set-membership point made "
    "explicitly."),
   ("Lehman, Leighton & Meyer, chapter 14 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>&sect;&sect;1 to 3</b>, free — asymptotics with the common "
    "abuses catalogued."),
   ("Knuth &mdash; Big Omicron and big Omega and big Theta (free)",
    "https://dl.acm.org/doi/10.1145/1008328.1008329",
    "<b>&sect;1's callout</b> — two pages on the notation and why "
    "the equals sign is what it is, by the person who "
    "standardised it."),
   ("Sedgewick & Wayne, the analysis lectures (free)",
    "https://algs4.cs.princeton.edu/14analysis/",
    "<b>&sect;4</b> — measurement alongside analysis, which is the "
    "practice this module argues for."),
 ],
 "exercises": [
   "<b>State all three definitions</b> from memory.",
   "<b>Prove three polynomial bounds</b>, exhibiting c and "
   "n₀.",
   "<b>Prove the matching lower bounds</b>, and conclude "
   "Θ.",
   "<b>Explain why O(n) = O(n²)</b> is true one way only.",
   "<b>Find an invalid O-manipulation</b> in the wild, or construct "
   "one.",
   "<b>Order ten functions</b> by growth and prove three of the "
   "comparisons.",
   "<b>Compute the hierarchy table</b> for n = 10⁹.",
   "<b>Find two algorithms with the same O</b> and measure a 10x "
   "difference.",
   "<b>Find an asymptotically better algorithm</b> that loses in "
   "practice, and say why.",
   "<b>State what worst, average, and amortised each mean</b>, with "
   "an example.",
 ],
 "selfcheck": [
   "State the definitions of O, Ω, and Θ.",
   "What must you exhibit to prove an O bound?",
   "Why is 'f = O(g)' an abuse, and what does it really say?",
   "Why can you not manipulate O-expressions as equations?",
   "Give the technique for proving a polynomial bound.",
   "Why is the lower bound usually easier?",
   "Give the growth hierarchy and the values at a million.",
   "Where does most algorithmic work happen?",
   "Name four things asymptotics hides.",
   "Why does the notation exist, and what does it cost?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Recurrences",
 "subtitle": "How recursive algorithms get their running times.",
 "question": "T(n) = 2T(n/2) + n. Now what?",
 "outcomes": [
     "Set up a recurrence from a recursive algorithm.",
     "Solve by expansion and by recursion tree.",
     "State and apply the master theorem.",
     "Verify a guess by substitution and induction.",
     "Recognise when the master theorem does not apply.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Setting one up",
   "blurb": "Which is the step that is actually error-prone."},

  {"t": "callout", "title": "A recurrence is a direct transcription of what the algorithm does, and getting it wrong is the usual failure",
   "kind": "Where the errors are",
   "body": ["<b>Count the recursive calls, the size of each "
            "subproblem, and the non-recursive work</b> — <b>three "
            "quantities, and the recurrence writes "
            "itself.</b>",
            "<b>Merge sort: two calls, each on half, plus linear "
            "merging</b> — <b>T(n) = 2T(n/2) + "
            "Θ(n)</b>.",
            "<b>And the base case matters</b>: <b>T(1) = Θ(1)</b> is "
            "nearly always right, and omitting it is "
            "Module 03's first error in a new "
            "setting.",
            "<b>Plus the floors and ceilings are usually "
            "ignorable</b> — <b>T(⌈n/2⌉) behaves like T(n/2) for the "
            "asymptotics</b> — and saying so once is better than "
            "carrying them."]},

  {"t": "section", "label": "Part 2", "title": "Solving by expansion",
   "blurb": "The method that always works and always takes longer."},

  {"t": "code", "kicker": "Expansion", "title": "Unroll it, and count the levels",
   "lang": "text", "code": """
  T(n) = 2T(n/2) + n

  EXPAND
      = 2[2T(n/4) + n/2] + n = 4T(n/4) + 2n
      = 4[2T(n/8) + n/4] + 2n = 8T(n/8) + 3n
      ...
      = 2^k T(n/2^k) + kn

  STOP when n/2^k = 1, i.e. k = log2(n)
      = n T(1) + n log2(n)
      = Theta(n log n)

  THE RECURSION TREE VIEW, same thing
      level 0:  one problem of size n,   work n
      level 1:  two of size n/2,         work n
      level 2:  four of size n/4,        work n
      ...
      log n levels, each doing n work -> n log n

  AND THE TREE VIEW IS THE ONE TO KEEP: it shows
  WHERE the cost is. If the work per level grows,
  the leaves dominate; if it shrinks, the root does.
""",
   "caption": "<b>The recursion tree shows <i>where</i> the cost "
              "is</b> — and whether the root, the leaves, or every "
              "level equally dominates is what the master theorem's "
              "three cases encode."},

  {"t": "section", "label": "Part 3", "title": "The master theorem",
   "blurb": "Three cases, and they are the three tree shapes."},

  {"t": "eq", "kicker": "Master theorem", "title": "For T(n) = aT(n/b) + f(n)",
   "eqs": [
     ("compare f(n) against n^(log_b a)",
      "n^(log_b a) is the total work at the leaves. The comparison "
      "decides which level dominates — which is exactly §2's "
      "tree picture."),
     ("f smaller (polynomially): T(n) = Θ(n^(log_b a))",
      "The leaves dominate. Example: T(n) = 4T(n/2) + n gives "
      "Θ(n²)."),
     ("f equal: Θ(n^(log_b a) log n);  f larger: Θ(f(n))",
      "Every level equal, or the root dominates. Merge sort is the "
      "middle case; T(n) = 2T(n/2) + n² is the last."),
   ],
   "caption": "<b>The three cases are the three tree shapes</b> "
              "— leaves dominate, all levels equal, or root "
              "dominates — which is why §2 is worth doing before "
              "memorising this.",
   "note": "Derive the master theorem from the tree once; then you "
           "will never misapply it."},

  {"t": "callout", "title": "And it does not always apply, which the 'polynomially' is doing",
   "kind": "The condition people skip",
   "body": ["<b>The comparison must be polynomial</b> — <b>f must "
            "be smaller or larger by a factor of n to some positive "
            "power</b>, not merely smaller.",
            "<b>So T(n) = 2T(n/2) + n log n falls in the "
            "gap</b> — <b>n log n is bigger than n, and not "
            "polynomially bigger</b> — and the theorem says "
            "nothing.",
            "<b>Which is handled by expansion</b> "
            "(Part 2), giving Θ(n log² n) — <b>so the "
            "fallback is always available</b> and is why "
            "Part 2 comes first.",
            "<b>And the regularity condition in case "
            "three</b> is almost always satisfied and should be checked "
            "once rather than assumed forever."]},

  {"t": "section", "label": "Part 4", "title": "Substitution",
   "blurb": "Guess and verify, which is the rigorous method."},

  {"t": "bullets", "kicker": "Substitution", "title": "The method that proves what the others suggest",
   "items": [
     "<b>Guess the answer</b> — from expansion, from the "
     "master theorem, or from a similar recurrence — <b>and then "
     "prove it by induction</b> "
     "(Module 03).",
     "",
     "<b>Which is the only one of the three methods that is "
     "actually a proof</b>: expansion has an informal 'and so on', and "
     "the master theorem needs its conditions "
     "checked.",
     "",
     "<b>And the standard trap: proving T(n) ≤ cn fails "
     "even when it is true</b>, because the induction does not carry "
     "— <b>and strengthening the hypothesis to "
     "T(n) ≤ cn − d fixes it</b>.",
     "",
     "<b>Which is counterintuitive and correct</b>: <b>a stronger "
     "claim is sometimes easier to prove by induction</b>, because the "
     "hypothesis you get to assume is "
     "stronger too.",
     "",
     "<b>And Project 2 asks for three recurrences solved three "
     "ways</b>, with the answers agreeing.",
   ],
   "footnote": "<b>A stronger claim is sometimes easier to prove by "
               "induction</b>, because the hypothesis you may assume is "
               "stronger too — which is the one genuinely "
               "counterintuitive fact in this "
               "module."},

  {"t": "callout", "title": "And this is the direct bridge into CSCE 629",
   "kind": "Closing",
   "body": ["<b>Every divide-and-conquer algorithm in that course "
            "has its running time established by one of these three "
            "methods</b>, usually the master theorem, usually in one "
            "line.",
            "<b>So being fluent here means those lines are "
            "readable</b> — <b>and not being fluent means the "
            "course's central technique arrives as an "
            "assertion.</b>",
            "<b>Which is the clearest case in this prerequisite of a "
            "specific skill with a specific payoff</b>, and is worth "
            "the practice.",
            "<b>And the three methods have a division of "
            "labour:</b> <b>the tree shows you where the cost is, the "
            "master theorem gives the answer fast, and substitution "
            "proves it.</b>"]},
 ],
 "takeaways": [
   "Count the recursive calls, the subproblem size, and the non-recursive "
   "work — three quantities, and the recurrence writes itself.",
   "The recursion tree shows where the cost is: root, leaves, or every "
   "level equally.",
   "The master theorem's three cases are the three tree shapes.",
   "The comparison must be polynomial, which is why T(n) = 2T(n/2) + n log "
   "n falls in the gap.",
   "Substitution is the only one of the three methods that is actually a "
   "proof.",
   "A stronger claim is sometimes easier to prove by induction, because the "
   "hypothesis you may assume is stronger too.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Setting one up"),
  ("callout", "A recurrence is a direct transcription of what the algorithm "
              "does, and getting it wrong is the usual failure",
   ["<b>Count three things: how many recursive calls, the size of "
    "each subproblem, and the non-recursive work done at this "
    "level</b> — <b>and the recurrence writes itself</b> as "
    "T(n) = (calls) &middot; T(size) + (work).",
    "<b>Merge sort: two recursive calls, each on half the input, "
    "plus linear time to merge</b> — <b>T(n) = 2T(n/2) + "
    "&Theta;(n)</b>. Binary search: one call on half, constant "
    "work — T(n) = T(n/2) + &Theta;(1).",
    "<b>And the base case matters</b>: <b>T(1) = &Theta;(1)</b> is "
    "nearly always what you want, <b>and omitting it is Module 03's "
    "first error arriving in a new setting</b> — a recurrence "
    "without a base case determines nothing.",
    "<b>Plus the floors and ceilings are usually ignorable</b> for "
    "asymptotic purposes — <b>T(&lceil;n/2&rceil;) behaves like "
    "T(n/2)</b> — and <b>saying so once explicitly is better than "
    "carrying them through every line</b>, which CLRS does and then "
    "justifies."]),

  ("h1", "2 &nbsp; Solving by expansion"),
  ("code", """T(n) = 2T(n/2) + n

EXPAND
    = 2[2T(n/4) + n/2] + n  = 4T(n/4) + 2n
    = 4[2T(n/8) + n/4] + 2n = 8T(n/8) + 3n
    ...
    = 2^k T(n/2^k) + kn

STOP when n/2^k = 1, i.e. when k = log2(n)
    = n T(1) + n log2(n)
    = Theta(n log n)

THE RECURSION TREE VIEW, which is the same thing
    level 0:  one problem of size n,    work n
    level 1:  two of size n/2,          work n
    level 2:  four of size n/4,         work n
    ...
    log n levels, each doing n work  ->  n log n

AND THE TREE VIEW IS THE ONE TO KEEP: it shows WHERE
the cost is. If the work per level grows as you
descend, the leaves dominate; if it shrinks, the root
dominates; if it is constant, every level matters."""),
  ("p", "<b>The recursion tree shows <i>where</i> the cost is</b> "
        "— and <b>whether the root, the leaves, or every level "
        "equally dominates is exactly what the master theorem's three "
        "cases encode</b> (&sect;3). Drawing the tree for three or four "
        "recurrences before meeting the theorem makes the theorem "
        "obvious rather than arbitrary, which is why this section comes "
        "first."),

  ("break",),
  ("h1", "3 &nbsp; The master theorem"),
  ("eq", "for T(n) = a&middot;T(n/b) + f(n), compare f(n) against "
         "n<super>log<sub>b</sub> a</super>"),
  ("ul", ["<b>n<super>log<sub>b</sub> a</super> is the total work "
          "done at the leaves</b> of the recursion tree, and <b>the "
          "comparison decides which level dominates</b> — <b>which "
          "is precisely &sect;2's tree picture turned into a "
          "rule</b>.",
          "<b>If f is polynomially smaller: T(n) = "
          "&Theta;(n<super>log<sub>b</sub> a</super>)</b> — the "
          "leaves dominate. <b>Example: T(n) = 4T(n/2) + n gives "
          "&Theta;(n<super>2</super>)</b>, since the leaf work grows as "
          "you descend.",
          "<b>If f is the same order: &Theta;(n<super>log<sub>b</sub> "
          "a</super> log n)</b> — every level contributes equally, "
          "and there are log n levels. <b>Merge sort is this middle "
          "case.</b>",
          "<b>If f is polynomially larger: &Theta;(f(n))</b> "
          "— the root dominates and the recursion is "
          "cheap. <b>T(n) = 2T(n/2) + n<super>2</super> is this "
          "case.</b>",
          "<b>The three cases are the three tree shapes</b> "
          "— <b>leaves dominate, all levels equal, or root "
          "dominates</b> — <b>which is why &sect;2 is worth doing "
          "before memorising this</b>. <b>Derive the master theorem "
          "from the tree once, and you will never misapply it.</b>"]),
  ("callout", "And it does not always apply, which is what the word "
              "'polynomially' is doing",
   ["<b>The comparison has to be polynomial</b> — <b>f must be "
    "smaller or larger than n<super>log<sub>b</sub> a</super> by a "
    "factor of n to some positive power</b>, <b>not merely smaller or "
    "larger</b>, and that qualifier is routinely dropped when the "
    "theorem is quoted.",
    "<b>So T(n) = 2T(n/2) + n log n falls straight into the "
    "gap</b> — <b>n log n is larger than n, and is not "
    "<i>polynomially</i> larger</b> (no n<super>&epsilon;</super> fits "
    "between them) — <b>and the theorem simply says nothing about "
    "it.</b>",
    "<b>Which is handled by expansion</b> (&sect;2), giving "
    "&Theta;(n log<super>2</super> n) in a few lines — <b>so the "
    "fallback is always available</b>, <b>and that is why &sect;2 "
    "comes first</b> rather than being presented as the slow "
    "method.",
    "<b>And the regularity condition attached to case three</b> "
    "(that a&middot;f(n/b) &le; c&middot;f(n) for some c &lt; 1) <b>is "
    "almost always satisfied by the functions you meet, and should be "
    "checked once rather than assumed forever.</b>"]),

  ("h1", "4 &nbsp; Substitution"),
  ("ul", ["<b>Guess the answer</b> — from an expansion, from "
          "the master theorem, or from a recurrence you have seen before "
          "— <b>and then prove it by induction</b> "
          "(Module 03), which is where this method gets its "
          "rigour.",
          "<b>Which makes it the only one of the three methods that "
          "is actually a proof</b>: <b>expansion contains an informal "
          "'and so on'</b> that hides an induction, <b>and the master "
          "theorem is a proof only once its conditions have been "
          "checked</b> (&sect;3's callout).",
          "<b>And the standard trap: trying to prove "
          "T(n) &le; cn fails even when the bound is true</b>, because "
          "the induction does not carry — the constants do not work "
          "out — <b>and strengthening the hypothesis to "
          "T(n) &le; cn &minus; d fixes it</b>.",
          "<b>Which is counterintuitive and correct</b>: <b>a "
          "stronger claim is sometimes easier to prove by induction, "
          "because the hypothesis you get to assume is stronger "
          "too</b> — <b>which is the one genuinely counterintuitive "
          "fact in this module</b>, and is worth meeting here rather "
          "than in the middle of CSCE 629.",
          "<b>And Project 2 asks for three recurrences solved three "
          "ways</b>, <b>with the three answers agreeing</b> and any "
          "disagreement tracked down rather than averaged."]),
  ("callout", "And this is the direct bridge into CSCE 629",
   ["<b>Every divide-and-conquer algorithm in that course has its "
    "running time established by one of these three methods</b> — "
    "<b>usually the master theorem, usually in a single line, usually "
    "without comment.</b>",
    "<b>So being fluent here means those lines are readable</b> "
    "— <b>and not being fluent means the course's central analytic "
    "technique arrives as an assertion you have to take on "
    "trust</b>, which is exactly Module 01 &sect;4's attrition "
    "mechanism.",
    "<b>Which makes this the clearest case in the whole "
    "prerequisite of a specific skill with a specific, nameable "
    "payoff</b>, and worth the practice even if the rest of the course "
    "felt easy.",
    "<b>And the three methods have a clean division of "
    "labour:</b> <b>the recursion tree shows you where the cost is, the "
    "master theorem gives you the answer quickly, and substitution "
    "proves it</b> — use all three, in that order."]),
 ],
 "resources": [
   ("CLRS, chapter 4 (library copy)",
    "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/",
    "<b>The whole module</b> — the three methods, the master "
    "theorem's proof, and the substitution trap of &sect;4 "
    "worked."),
   ("MIT 6.006, the divide-and-conquer lectures (free)",
    "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
    "<b>&sect;&sect;2 and 3</b> — recursion trees drawn, which is "
    "the right way to meet them."),
   ("Lehman, Leighton & Meyer, chapter 21 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>&sect;&sect;2 and 4</b>, free — recurrences solved by "
    "expansion and by guess-and-verify."),
   ("Mitzenmacher & Upfal, the recurrence material",
    "https://www.cambridge.org/9781107154889",
    "<b>&sect;4 for randomised algorithms</b> — where the "
    "recurrences become expectations, which is CSCE 658. Library "
    "copy."),
 ],
 "exercises": [
   "<b>Write recurrences</b> for merge sort, binary search, and "
   "Strassen's multiplication.",
   "<b>Solve T(n) = 2T(n/2) + n by expansion</b>, showing every "
   "level.",
   "<b>Draw the recursion tree</b> for three recurrences and identify "
   "the dominant level.",
   "<b>Apply the master theorem</b> to ten recurrences.",
   "<b>Find two where it does not apply</b>, and say why.",
   "<b>Solve one of those by expansion.</b>",
   "<b>Prove a bound by substitution</b>, with the induction "
   "explicit.",
   "<b>Hit the T(n) ≤ cn trap</b> deliberately, then fix it by "
   "strengthening.",
   "<b>Explain why strengthening helped</b>, in three sentences.",
   "<b>Solve three recurrences three ways</b> and check the answers "
   "agree.",
 ],
 "selfcheck": [
   "What three quantities give you a recurrence?",
   "Why does the base case matter?",
   "Solve T(n) = 2T(n/2) + n by expansion.",
   "What does the recursion tree show that the algebra does not?",
   "State the master theorem's three cases.",
   "How do the cases correspond to tree shapes?",
   "What is 'polynomially' doing, and give a recurrence in the gap.",
   "Which method is actually a proof, and why are the others not?",
   "State the substitution trap and its fix.",
   "Why can a stronger claim be easier to prove?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Discrete Probability",
 "subtitle": "Counting with weights, and the errors everyone makes.",
 "question": "The test is 99% accurate and you tested positive. What "
             "is the probability you have it?",
 "outcomes": [
     "Set up a probability space correctly.",
     "Use conditional probability and independence.",
     "Apply Bayes' rule and explain base rates.",
     "Avoid the standard probability errors.",
     "Connect this to the randomised algorithms ahead.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The setup",
   "blurb": "Which is where most errors are actually made."},

  {"t": "callout", "title": "Name the sample space before computing anything, because almost every error is a sample space error",
   "kind": "The discipline this module is built on",
   "body": ["<b>A probability space is a set of outcomes and a "
            "weight on each, summing to one</b> — <b>and an event is "
            "a subset</b>, whose probability is the sum of its "
            "weights.",
            "<b>Which means a probability question is a counting "
            "question with weights</b> "
            "(Module 06) — and <b>the rules of "
            "counting carry over directly.</b>",
            "<b>And the classic paradoxes are almost all disputes "
            "about the sample space</b> — <b>'two children, one is a "
            "boy' has different answers depending on how you learned "
            "it</b>, because the space differs.",
            "<b>So write the outcomes down</b>, especially when the "
            "answer surprises you — <b>which resolves more confusion "
            "than any formula</b>, and is this module's one "
            "habit."]},

  {"t": "section", "label": "Part 2", "title": "Conditioning",
   "blurb": "And independence, which is a claim and not a default."},

  {"t": "eq", "kicker": "Conditioning", "title": "The definitions, and what they mean",
   "eqs": [
     ("P(A | B) = P(A and B) / P(B)",
      "Restrict the sample space to B and renormalise. That is "
      "literally all conditioning is."),
     ("A and B independent iff P(A and B) = P(A)·P(B)",
      "Equivalently P(A|B) = P(A): knowing B tells you nothing about "
      "A. This is a property to check, not an assumption to make."),
     ("union bound: P(A or B) ≤ P(A) + P(B), always",
      "No independence needed, and it is the most useful inequality "
      "in CSCE 658 — crude, free, and usually enough."),
   ],
   "caption": "<b>The union bound needs no assumptions and is "
              "usually enough</b> — which makes it the most useful "
              "inequality in randomised "
              "algorithms.",
   "note": "Independence is a claim that must be justified, and "
           "assuming it is the second commonest "
           "error."},

  {"t": "section", "label": "Part 3", "title": "Bayes and base rates",
   "blurb": "The calculation everyone gets wrong, including "
            "professionals."},

  {"t": "code", "kicker": "Bayes", "title": "The 99% accurate test",
   "lang": "text", "code": """
  SETUP
      1 person in 10,000 has the condition
      the test is 99% accurate both ways
      you test positive. P(condition | positive)?

  COUNT 1,000,000 PEOPLE
      100 have it.  99 of them test positive.
      999,900 do not. 1% of them -- 9,999 --
          test positive anyway.

      positives: 99 + 9,999 = 10,098
      of which真 positives: 99

      P(condition | positive) = 99 / 10,098
                             = about 1%

  SO A 99% ACCURATE TEST GIVES A 1% ANSWER.
  Not a trick: the false positives come from a pool
  10,000 times larger, so they swamp the true ones.

  AND THE LESSON: the base rate is not a detail.
  Module 06's frequency framing makes this obvious
  and the formula makes it opaque.
""",
   "caption": "<b>Count a million people instead of applying the "
              "formula</b> — the frequency framing makes this "
              "obvious where the algebra makes it "
              "opaque.",
   "note": "This is the single most practically important "
           "calculation in the module."},

  {"t": "callout", "title": "Which generalises: a rare thing detected by an imperfect test is mostly false positives",
   "kind": "Where this reappears in the program",
   "body": ["<b>Intrusion detection, spam filtering, disease "
            "screening, and fraud detection all have this "
            "shape</b> — <b>and all of them produce alert fatigue for "
            "exactly this reason</b> "
            "(CSCE 701 §09).",
            "<b>And it is why precision and recall are reported "
            "separately</b> rather than as a single "
            "accuracy (CSCE 633, CSCE 670 §03).",
            "<b>A classifier that is 99% accurate on a 1-in-10,000 "
            "problem can be worse than useless</b> — <b>and 'accuracy' "
            "is the metric that hides it</b> "
            "(CSCE 676 §13's proxy "
            "problem).",
            "<b>So the habit:</b> <b>when told an accuracy, ask for "
            "the base rate</b> — <b>which is one question and changes "
            "the interpretation entirely.</b>"]},

  {"t": "section", "label": "Part 4", "title": "The standard errors",
   "blurb": "Five of them, and they recur for a lifetime."},

  {"t": "bullets", "kicker": "Errors", "title": "What goes wrong, reliably",
   "items": [
     "<b>Ignoring the base rate</b> "
     "(Part 3) — the most consequential, and the "
     "one professionals make.",
     "",
     "<b>Assuming independence</b> — <b>which is a claim "
     "about the world and is usually false for the things you care "
     "about</b>; correlated failures are the reason redundancy "
     "disappoints.",
     "",
     "<b>Confusing P(A|B) with P(B|A)</b> — <b>'most "
     "accidents happen near home' and 'driving near home is dangerous' "
     "are different claims</b>, and the first is about where people "
     "drive.",
     "",
     "<b>The gambler's fallacy</b> — independent trials have "
     "no memory, and <b>a coin is not 'due'.</b>",
     "",
     "<b>And conditioning on the wrong thing</b> — "
     "<b>selection effects</b>, where the sample you can see was "
     "filtered (CSCE 676 §08).",
   ],
   "footnote": "<b>Correlated failures are the reason redundancy "
               "disappoints</b> — which is the independence "
               "assumption failing where it was least "
               "examined."},

  {"t": "callout", "title": "And where this goes next",
   "kind": "Closing",
   "body": ["<b>CSCE 658 is this module plus Module 12's "
            "concentration bounds</b> — <b>randomised algorithms are "
            "probability applied to a sample space you "
            "constructed</b>, which is the easy "
            "case.",
            "<b>And every machine learning course is this module "
            "with continuous distributions</b> — <b>the discrete "
            "version is where the intuitions are "
            "built</b>.",
            "<b>Plus the probabilistic method</b>: <b>prove "
            "something exists by showing a random object has it with "
            "positive probability</b> — which is a counting argument in "
            "disguise and is one of the most elegant techniques in the "
            "subject.",
            "<b>So: name the space, check independence, and ask for "
            "the base rate</b> — <b>three habits, and they cover most "
            "of what goes wrong.</b>"]},
 ],
 "takeaways": [
   "Name the sample space before computing, because almost every error is a "
   "sample space error.",
   "Conditioning is restricting the sample space and renormalising — "
   "that is all it is.",
   "Independence is a property to check, not an assumption to make.",
   "The union bound needs no assumptions and is usually enough.",
   "A 99% accurate test for a 1-in-10,000 condition gives a 1% answer, "
   "because the false positives come from a pool 10,000 times larger.",
   "Correlated failures are the reason redundancy disappoints.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The setup"),
  ("callout", "Name the sample space before computing anything, because "
              "almost every error is a sample space error",
   ["<b>A probability space is a set of outcomes together with a "
    "weight on each, summing to one</b> — <b>and an event is "
    "simply a subset of the outcomes</b>, whose probability is the sum "
    "of the weights in it. Nothing more elaborate is going on.",
    "<b>Which means a probability question is a counting question "
    "with weights</b> (Module 06) — and <b>the sum rule, product "
    "rule, bijection rule, and inclusion-exclusion all carry over "
    "directly</b>, which is why that module comes before this "
    "one.",
    "<b>And the classic paradoxes are almost all disputes about the "
    "sample space rather than about the arithmetic</b> — <b>'I "
    "have two children and one is a boy' has different answers depending "
    "on how you came to learn that</b>, because the set of outcomes "
    "consistent with your information differs.",
    "<b>So write the outcomes down</b>, explicitly, <b>especially "
    "when the answer surprises you</b> — <b>which resolves more "
    "confusion than any formula</b>, and <b>is this module's one "
    "habit</b> if you take nothing else from it."]),

  ("h1", "2 &nbsp; Conditioning"),
  ("eq", "P(A | B) = P(A &cap; B) / P(B)"),
  ("ul", ["<b>Restrict the sample space to B and renormalise so the "
          "weights sum to one again</b> — <b>that is literally all "
          "conditioning is</b>, and seeing it that way removes most of "
          "the mystery from Bayes' rule in &sect;3.",
          "<b>A and B are independent exactly when "
          "P(A &cap; B) = P(A)&middot;P(B)</b>, <b>equivalently when "
          "P(A|B) = P(A)</b>: knowing B happened tells you nothing about "
          "A. <b>This is a property to be checked, not an assumption to "
          "be made</b>, and <b>assuming it is the second commonest "
          "error</b> in the subject (&sect;4).",
          "<b>The union bound says P(A &cup; B) &le; P(A) + P(B), "
          "always</b> — <b>no independence required, no conditions "
          "at all</b> — and it extends to any number of events by "
          "induction.",
          "<b>The union bound needs no assumptions and is usually "
          "enough</b>, <b>which makes it the most useful inequality in "
          "CSCE 658</b>: it is crude, it is free, and the typical "
          "randomised-algorithm argument ('the probability that any of n "
          "bad things happens is at most n times the probability of one') "
          "is exactly this."]),

  ("break",),
  ("h1", "3 &nbsp; Bayes and base rates"),
  ("code", """SETUP
    1 person in 10,000 has the condition
    the test is 99% accurate in both directions
    you test positive. What is
    P(condition | positive)?

COUNT 1,000,000 PEOPLE
    100 have it.  99 of those test positive.
    999,900 do not have it. 1% of them -- that is
        9,999 people -- test positive anyway.

    total positives: 99 + 9,999 = 10,098
    true positives among them: 99

    P(condition | positive) = 99 / 10,098
                            = about 1%

SO A 99% ACCURATE TEST GIVES A 1% ANSWER.
Not a trick: the false positives are drawn from a
pool 10,000 times larger, so they swamp the true
positives completely.

AND THE LESSON: the base rate is not a detail."""),
  ("p", "<b>Count a million people instead of applying the "
        "formula</b> — <b>the frequency framing makes this obvious "
        "where the algebra makes it opaque</b>, which is a measured "
        "effect and not merely a preference (CSCE 679 Module 09 "
        "&sect;3 covers the evidence). <b>This is the single most "
        "practically important calculation in the module</b>, and it is "
        "worth being able to produce from scratch rather than recalling "
        "the conclusion."),
  ("callout", "Which generalises: a rare thing detected by an imperfect test "
              "is mostly false positives",
   ["<b>Intrusion detection, spam filtering, disease screening, and "
    "fraud detection all have exactly this shape</b> — <b>and all "
    "of them produce alert fatigue for precisely this reason</b> "
    "(CSCE 701 Module 09's detection material, where the base rate is "
    "the central design constraint).",
    "<b>And it is why precision and recall are reported separately "
    "rather than collapsed into a single accuracy figure</b> "
    "(CSCE 633's evaluation material, CSCE 670 Module 03) — "
    "accuracy on an imbalanced problem is dominated by the majority "
    "class and says almost nothing.",
    "<b>A classifier that is 99% accurate on a one-in-ten-thousand "
    "problem can be worse than useless</b> — it can be beaten by "
    "always answering 'no' — <b>and 'accuracy' is exactly the "
    "metric that hides this</b> (CSCE 676 Module 13's proxy "
    "problem).",
    "<b>So the habit to build:</b> <b>when somebody tells you an "
    "accuracy, ask for the base rate</b> — <b>which is one "
    "question and changes the interpretation entirely</b>, and is "
    "answerable in every honest case."]),

  ("h1", "4 &nbsp; The standard errors"),
  ("ul", ["<b>Ignoring the base rate</b> (&sect;3) — <b>the "
          "most consequential of the five, and the one trained "
          "professionals make</b> in medicine and in security "
          "alike.",
          "<b>Assuming independence</b> — <b>which is a claim "
          "about the world and is usually false for the things you "
          "actually care about</b>: <b>correlated failures are the "
          "reason redundancy disappoints</b>, since the two replicas "
          "share a power supply, a rack, a library version, or a "
          "deployment (CSCE 678's correlated-failure material).",
          "<b>Confusing P(A|B) with P(B|A)</b> — <b>'most "
          "accidents happen near home' and 'driving near home is "
          "dangerous' are different claims</b>, <b>and the first is "
          "mostly a statement about where people drive</b>. This is the "
          "prosecutor's fallacy, and it has sent people to prison.",
          "<b>The gambler's fallacy</b> — independent trials "
          "have no memory, and <b>a coin that has come up heads five "
          "times is not 'due'</b>. The related error in the other "
          "direction is assuming a streak means the coin is "
          "biased.",
          "<b>And conditioning on the wrong thing</b> — "
          "<b>selection effects, where the sample you can observe was "
          "filtered by something related to what you are "
          "measuring</b> (CSCE 676 Module 08's survivorship, and "
          "CSCE 632 Module 02 &sect;2's analytics argument)."]),
  ("callout", "And where this goes next",
   ["<b>CSCE 658 is this module plus Module 12's concentration "
    "bounds</b> — <b>randomised algorithms are probability applied "
    "to a sample space you constructed yourself</b>, <b>which is the "
    "easy case</b>: you know the distribution exactly because you chose "
    "it.",
    "<b>And every machine learning course is this module with "
    "continuous distributions</b> — <b>the discrete version is "
    "where the intuitions get built</b>, and continuous probability adds "
    "machinery rather than ideas.",
    "<b>Plus the probabilistic method</b>: <b>prove that an object "
    "with some property exists by showing a randomly chosen object has "
    "it with positive probability</b> — <b>which is a counting "
    "argument in disguise</b> (Module 06) and is one of the most "
    "elegant techniques in combinatorics.",
    "<b>So: name the space, check independence, and ask for the "
    "base rate</b> — <b>three habits, and they cover most of what "
    "goes wrong</b> in this subject for the rest of your "
    "career."]),
 ],
 "resources": [
   ("Lehman, Leighton & Meyer, chapters 17 to 19 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>The whole module</b>, free — and the sample-space discipline "
    "of &sect;1 is emphasised throughout, correctly."),
   ("Mitzenmacher & Upfal, chapters 1 to 3",
    "https://www.cambridge.org/9781107154889",
    "<b>&sect;&sect;1 to 3</b> — probability for computer "
    "scientists, and the direct prerequisite for CSCE 658. Library "
    "copy."),
   ("Gigerenzer &mdash; Reckoning with Risk",
    "https://www.penguin.co.uk/books/558051/reckoning-with-risk-by-gerd-gigerenzer/9780140297867",
    "<b>&sect;3</b> — the frequency framing and why it works, with "
    "the medical examples. Library copy."),
   ("Tijms &mdash; Understanding Probability",
    "https://www.cambridge.org/9781107658561",
    "<b>&sect;&sect;1 and 4</b> — the paradoxes resolved by naming "
    "the sample space, which is the right way to meet them. Library "
    "copy."),
 ],
 "exercises": [
   "<b>Write the sample space</b> for five problems before "
   "computing.",
   "<b>Resolve the two-children problem</b> both ways, with the "
   "spaces written out.",
   "<b>Compute five conditional probabilities</b> from the "
   "definition.",
   "<b>Check independence</b> for four event pairs, and find one that "
   "is not.",
   "<b>Apply the union bound</b> to a problem with n bad events.",
   "<b>Do the 99% test calculation</b> by counting a million "
   "people.",
   "<b>Redo it</b> with base rates of 1 in 100 and 1 in "
   "1,000,000.",
   "<b>Find a published accuracy claim</b> and ask for its base "
   "rate.",
   "<b>Find an example of each of the five errors</b> in the "
   "wild.",
   "<b>Prove something exists</b> by the probabilistic method.",
 ],
 "selfcheck": [
   "What is a probability space, and what is an event?",
   "Why is naming the sample space the key habit?",
   "Define conditional probability and say what it does.",
   "Define independence, and say why it is a claim.",
   "State the union bound and say what it assumes.",
   "Work the 99% test problem by counting.",
   "Why does a 99% accurate test give a 1% answer?",
   "Where does this shape reappear in the program?",
   "Name the five standard errors.",
   "What are the three habits this module asks for?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Expectation and Concentration",
 "subtitle": "Averages, and why they are usually close to the truth.",
 "question": "How far from its average can a random variable get?",
 "outcomes": [
     "Compute expectations, including with linearity.",
     "Explain why linearity needs no independence.",
     "Use indicator variables to count.",
     "Apply Markov, Chebyshev, and Chernoff bounds.",
     "Explain concentration and why it matters.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Linearity",
   "blurb": "The most useful fact in the subject."},

  {"t": "callout", "title": "E[X + Y] = E[X] + E[Y], always — with no independence assumption whatsoever",
   "kind": "The fact that does most of the work",
   "body": ["<b>It holds for dependent variables, for variables "
            "defined on top of each other, for anything</b> — <b>which "
            "is remarkable and is used constantly without "
            "comment.</b>",
            "<b>So a complicated random quantity gets broken into "
            "simple pieces</b>, each of whose expectation is easy, and "
            "the pieces add — <b>even though the pieces interact "
            "wildly.</b>",
            "<b>Which makes the indicator variable trick "
            "work</b> (Part 2): <b>write a count as a sum of "
            "zero-one variables</b> and add their "
            "probabilities.",
            "<b>And note E[XY] = E[X]E[Y] does <i>not</i> hold in "
            "general</b> — <b>that one needs independence</b>, and "
            "confusing the two is the standard error "
            "here."]},

  {"t": "section", "label": "Part 2", "title": "Indicator variables",
   "blurb": "The technique linearity enables."},

  {"t": "code", "kicker": "Indicators", "title": "Counting by adding probabilities",
   "lang": "text", "code": """
  THE TRICK
      to find the expected number of things with
      some property, define
          X_i = 1 if thing i has it, else 0
      then X = sum of X_i, and by linearity
          E[X] = sum of E[X_i] = sum of P(thing i
                 has the property)

  EXAMPLE: n letters into n random envelopes.
  Expected number in the right envelope?
      X_i = 1 if letter i is correct
      E[X_i] = P(letter i correct) = 1/n
      E[X] = n * (1/n) = 1.    Always 1.

  AND THE X_i ARE WILDLY DEPENDENT
      if n-1 letters are correct the last must be
      -- and linearity does not care.

  THAT INDIFFERENCE TO DEPENDENCE IS THE WHOLE
  POWER OF THE METHOD.
""",
   "caption": "<b>The indicators are wildly dependent and linearity "
              "does not care</b> — which is what makes this the most "
              "reusable technique in the "
              "subject.",
   "note": "Every hashing analysis in CSCE 629 and CSCE 658 is this "
           "trick."},

  {"t": "section", "label": "Part 3", "title": "Concentration",
   "blurb": "Three bounds, in increasing strength and assumption."},

  {"t": "table", "kicker": "Bounds", "title": "The three, and what each costs",
   "header": ["Bound", "Needs", "Gives"],
   "widths": [2.6, 4.0, 4.4],
   "rows": [
     ["<b>Markov</b>", "<b>Non-negative, and the mean</b>", "<b>P(X ≥ a) ≤ E[X]/a. Weak, free</b>"],
     ["<b>Chebyshev</b>", "<b>The variance too</b>", "<b>Deviation by kσ has prob ≤ 1/k²</b>"],
     ["<b>Chernoff</b>", "<b>Independent bounded variables</b>", "<b>Exponentially small tails</b>"],
   ],
   "footnote": "<b>Chernoff is exponentially stronger and needs "
               "independence</b> — which is the trade, and is why "
               "the independence check of Module 11 §2 "
               "matters.",
   "note": "Markov from nothing, Chebyshev from variance, Chernoff "
           "from independence."},

  {"t": "callout", "title": "And concentration is why averages are useful at all",
   "kind": "The idea behind all three",
   "body": ["<b>A sum of many independent small contributions is "
            "very close to its mean, with overwhelming "
            "probability</b> — <b>which is why sampling works and why "
            "randomised algorithms are reliable.</b>",
            "<b>And the probability of being far off falls "
            "exponentially in the number of trials</b> — <b>so a few "
            "hundred samples pin down a proportion "
            "well</b>.",
            "<b>Which is the formal content of 'the average is "
            "representative'</b> — <b>a statement that is false for a "
            "single trial and true for many</b>, and the bounds say "
            "how many.",
            "<b>And it is what CSCE 658 runs on:</b> <b>repeat a "
            "randomised algorithm k times and the failure probability "
            "falls like a constant to the k</b>, which converts "
            "unreliable into reliable."]},

  {"t": "section", "label": "Part 4", "title": "Variance",
   "blurb": "And the one place independence is genuinely needed."},

  {"t": "bullets", "kicker": "Variance", "title": "What you need, and the asymmetry with expectation",
   "items": [
     "<b>Var(X) = E[X²] − E[X]²</b>, which is the "
     "computational form and is how it is always actually "
     "calculated.",
     "",
     "<b>And Var(X + Y) = Var(X) + Var(Y) only when X and Y are "
     "independent</b> — <b>unlike expectation</b> "
     "(Part 1), which is the asymmetry to "
     "remember.",
     "",
     "<b>In general Var(X + Y) = Var(X) + Var(Y) + "
     "2Cov(X,Y)</b>, and <b>the covariance term is what correlated "
     "failures contribute</b> "
     "(Module 11 §4).",
     "",
     "<b>Which is why diversification works and why correlated "
     "risk defeats it</b> — the same fact, in finance and in "
     "system reliability.",
     "",
     "<b>And the standard deviation scales as √n for a sum of "
     "n</b>, so <b>the <i>average</i>'s deviation shrinks as "
     "1/√n</b> — which is the square-root law behind every "
     "sample size calculation.",
   ],
   "footnote": "<b>The average's deviation shrinks as "
               "1/√n</b> — which is why quadrupling your sample "
               "halves your error, and why precision is "
               "expensive."},

  {"t": "callout", "title": "And this is the end of the prerequisite",
   "kind": "Closing",
   "body": ["<b>Linearity, indicators, and the three bounds are the "
            "whole probabilistic toolkit CSCE 629 and CSCE 658 "
            "assume</b> — <b>and they assume it without "
            "comment.</b>",
            "<b>The expected running time of quicksort is an "
            "indicator argument</b>; <b>the load of a hash table is "
            "Chernoff</b>; <b>amplification by repetition is "
            "concentration</b>.",
            "<b>So if those three sentences make sense, this course "
            "has done its job</b> — and if they do not, "
            "Modules 11 and 12 are worth another "
            "week.",
            "<b>Which is Module 13's self-check, "
            "essentially</b> — <b>and taking it honestly is the last "
            "thing this prerequisite asks.</b>"]},
 ],
 "takeaways": [
   "E[X + Y] = E[X] + E[Y] always, with no independence assumption — "
   "and E[XY] = E[X]E[Y] needs it.",
   "The indicator trick: write a count as a sum of zero-one variables and "
   "add their probabilities.",
   "The indicators are wildly dependent and linearity does not care, which "
   "is the whole power of the method.",
   "Markov from nothing, Chebyshev from variance, Chernoff from "
   "independence — in increasing strength.",
   "Variance adds only under independence, and the covariance term is what "
   "correlated failures contribute.",
   "The average's deviation shrinks as 1/√n, which is why quadrupling "
   "the sample halves the error.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Linearity"),
  ("callout", "E[X + Y] = E[X] + E[Y], always — with no independence "
              "assumption whatsoever",
   ["<b>It holds for dependent variables, for variables defined in "
    "terms of one another, for anything at all</b> — <b>which is "
    "genuinely remarkable and is used constantly without comment</b> in "
    "every algorithms text you will read.",
    "<b>So a complicated random quantity can be broken into simple "
    "pieces</b>, each of whose expectation is easy to compute, <b>and "
    "the pieces simply add</b> — <b>even when the pieces interact "
    "wildly with one another.</b>",
    "<b>Which is exactly what makes the indicator variable trick "
    "work</b> (&sect;2): <b>write a count as a sum of zero-one "
    "variables and add up their probabilities</b>, and you are "
    "done.",
    "<b>And note that E[XY] = E[X]&middot;E[Y] does <i>not</i> hold "
    "in general</b> — <b>that one does require independence</b> "
    "— <b>and confusing the two is the standard error in this "
    "module</b>, with the same shape as &sect;4's variance "
    "asymmetry."]),

  ("h1", "2 &nbsp; Indicator variables"),
  ("code", """THE TRICK
    to find the expected NUMBER of things with some
    property, define
        X_i = 1 if thing i has the property, else 0
    then X = sum of the X_i, and by linearity
        E[X] = sum of E[X_i]
             = sum of P(thing i has the property)

EXAMPLE: n letters into n random envelopes.
Expected number that land in the right envelope?
    X_i = 1 if letter i is in its own envelope
    E[X_i] = P(letter i correct) = 1/n
    E[X] = n * (1/n) = 1.    Always exactly 1,
    for every n.

AND THE X_i ARE WILDLY DEPENDENT
    if n-1 letters are correct then the last one
    must be too -- these are not independent in any
    sense -- and linearity does not care.

THAT INDIFFERENCE TO DEPENDENCE IS THE WHOLE POWER
OF THE METHOD."""),
  ("p", "<b>The indicators are wildly dependent and linearity does "
        "not care</b> — <b>which is what makes this the most "
        "reusable technique in the subject</b>, since the dependence "
        "between parts of a problem is usually the hard part and this "
        "sidesteps it entirely. <b>Every hashing analysis in CSCE 629 "
        "and CSCE 658 is this trick</b>: expected collisions, expected "
        "bucket load, expected probe count — all of them are a sum "
        "of indicators."),

  ("break",),
  ("h1", "3 &nbsp; Concentration"),
  ("table", ["Bound", "What it needs", "What it gives"],
   [["<b>Markov</b>",
     "<b>X non-negative, and its mean. Nothing else.</b>",
     "<b>P(X &ge; a) &le; E[X]/a.</b> Weak, and free — and it is "
     "what the other two are proved from."],
    ["<b>Chebyshev</b>", "<b>The variance as well.</b>",
     "<b>Deviating by k standard deviations has probability at most "
     "1/k<super>2</super></b> — which is distribution-free and "
     "useful."],
    ["<b>Chernoff / Hoeffding</b>",
     "<b>Independent, bounded random variables.</b>",
     "<b>Exponentially small tails</b> — vastly stronger, at the "
     "cost of the independence assumption."]],
   [0.20, 0.38, 0.42]),
  ("p", "<b>Chernoff is exponentially stronger and needs "
        "independence</b> — <b>which is the trade</b>, <b>and is "
        "why the independence check of Module 11 &sect;2 "
        "matters</b> rather than being pedantry. <b>Markov from "
        "nothing, Chebyshev from the variance, Chernoff from "
        "independence</b>: three bounds, three price points, and knowing "
        "which you can afford is the practical skill."),
  ("callout", "And concentration is why averages are useful at all",
   ["<b>A sum of many independent small contributions lies very "
    "close to its mean with overwhelming probability</b> — <b>which "
    "is why sampling works, why polling works, and why randomised "
    "algorithms are reliable</b> despite being random.",
    "<b>And the probability of being far from the mean falls "
    "exponentially in the number of trials</b> — <b>so a few "
    "hundred samples pin down a proportion remarkably well</b>, which "
    "is why survey sample sizes are smaller than intuition "
    "suggests.",
    "<b>Which is the formal content of the vague claim that 'the "
    "average is representative'</b> — <b>a statement that is simply "
    "false for a single trial and true for many</b>, <b>and the bounds "
    "say precisely how many</b> you need for a given confidence.",
    "<b>And it is what CSCE 658 runs on:</b> <b>repeat a "
    "randomised algorithm k times and take the majority, and the failure "
    "probability falls like a constant raised to the k</b> — which "
    "converts an unreliable procedure into a reliable one at "
    "logarithmic cost, and is the central move of that whole "
    "course."]),

  ("h1", "4 &nbsp; Variance"),
  ("ul", ["<b>Var(X) = E[X<super>2</super>] &minus; "
          "E[X]<super>2</super></b>, <b>which is the computational form "
          "and is how it is always actually calculated</b>, the "
          "definition as E[(X &minus; &mu;)<super>2</super>] being "
          "harder to work with.",
          "<b>And Var(X + Y) = Var(X) + Var(Y) only when X and Y are "
          "independent</b> — <b>unlike expectation</b> "
          "(&sect;1) — <b>which is the asymmetry to "
          "remember</b> and the one people get backwards.",
          "<b>In general Var(X + Y) = Var(X) + Var(Y) + "
          "2Cov(X,Y)</b>, and <b>the covariance term is exactly what "
          "correlated failures contribute</b> (Module 11 &sect;4's "
          "independence error) — positive covariance means the "
          "deviations reinforce.",
          "<b>Which is why diversification works and why correlated "
          "risk defeats it</b> — <b>the same mathematical fact, "
          "appearing in finance and in system reliability</b>, and in "
          "both places the covariance is the term nobody "
          "measured.",
          "<b>And the standard deviation of a sum of n independent "
          "terms scales as &radic;n</b>, so <b>the <i>average</i>'s "
          "standard deviation shrinks as 1/&radic;n</b> — <b>which "
          "is the square-root law behind every sample size "
          "calculation</b>: <b>quadrupling your sample halves your "
          "error</b>, which is why precision is expensive."]),
  ("callout", "And this is the end of the prerequisite",
   ["<b>Linearity of expectation, the indicator trick, and the three "
    "concentration bounds are the whole probabilistic toolkit that "
    "CSCE 629 and CSCE 658 assume</b> — <b>and they assume it "
    "without comment</b>, which is the attrition mechanism "
    "Module 01 &sect;4 described.",
    "<b>The expected running time of quicksort is an indicator "
    "argument</b>; <b>the maximum load of a hash table is a Chernoff "
    "bound</b>; <b>amplification by repetition is concentration</b> "
    "— three sentences from the first half of Semester 1.",
    "<b>So if those three sentences make sense to you, this course "
    "has done its job</b> — and <b>if they do not, Modules 11 "
    "and 12 are worth another week</b> before starting, which is a "
    "cheap insurance premium.",
    "<b>Which is Module 13's self-check, essentially</b> — "
    "<b>and taking it honestly is the last thing this prerequisite asks "
    "of you.</b>"]),
 ],
 "resources": [
   ("Lehman, Leighton & Meyer, chapters 19 and 20 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>The whole module</b>, free — and the indicator variable "
    "examples are the best collection available."),
   ("Mitzenmacher & Upfal, chapters 2 to 4",
    "https://www.cambridge.org/9781107154889",
    "<b>&sect;&sect;1 to 4</b> — expectation, variance, and the "
    "Chernoff bounds proved. The direct bridge to CSCE 658. Library "
    "copy."),
   ("MIT 6.042J, the expectation and deviation lectures (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/video_galleries/video-lectures/",
    "<b>&sect;&sect;1 to 3</b>, with linearity's independence-freedom "
    "emphasised properly."),
   ("Motwani & Raghavan &mdash; Randomized Algorithms",
    "https://www.cambridge.org/9780521474658",
    "<b>&sect;3 applied</b> — the bounds used in anger, which is "
    "CSCE 658's content. Library copy."),
 ],
 "exercises": [
   "<b>Compute five expectations</b> directly from the definition.",
   "<b>Prove linearity</b> for two dependent variables.",
   "<b>Find a case where E[XY] ≠ E[X]E[Y]</b>.",
   "<b>Solve the envelope problem</b> by indicators.",
   "<b>Count expected collisions</b> in a hash table by indicators.",
   "<b>Apply Markov, Chebyshev, and Chernoff</b> to the same problem "
   "and compare.",
   "<b>Find how many samples</b> you need for 1% precision at 95% "
   "confidence.",
   "<b>Compute a variance</b> both ways and confirm they agree.",
   "<b>Find two correlated variables</b> and compute the covariance "
   "term.",
   "<b>Verify the 1/√n law</b> empirically by simulation.",
 ],
 "selfcheck": [
   "State linearity of expectation and what it does not assume.",
   "Which product rule does need independence?",
   "Describe the indicator trick and why linearity enables it.",
   "Solve the envelope problem and say why dependence is irrelevant.",
   "Name the three bounds and what each requires.",
   "Why is Chernoff worth its assumption?",
   "What is concentration, and why does it make averages useful?",
   "Give the variance computational form.",
   "When does variance add, and what is the extra term otherwise?",
   "State the square-root law and its practical consequence.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming You Proved Something",
 "subtitle": "Finding your own gaps, and knowing you are ready.",
 "question": "Is that a proof, or is it a sketch you believe?",
 "outcomes": [
     "State what your proof actually establishes.",
     "Find gaps in your own arguments.",
     "Write a proof somebody else can check.",
     "Assess honestly whether you are ready for Semester 1.",
     "State the program's closing rule in this subject.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a proof establishes",
   "blurb": "Which is narrower than what you wanted to show."},

  {"t": "callout", "title": "A proof establishes the stated claim under the stated hypotheses, and nothing broader",
   "kind": "The honest reading",
   "body": ["<b>Which hypotheses</b> — <b>including the ones you "
            "used without noticing</b>: that n is positive, that the "
            "graph is simple, that the list is non-empty "
            "(Module 04 §1).",
            "<b>What exactly was proved</b> — <b>'for all n' or "
            "'for all sufficiently large n'</b>, which are different and "
            "are both common.",
            "<b>And what was assumed from elsewhere</b> — <b>a "
            "theorem you cited is a hypothesis you did not "
            "check</b>.",
            "<b>So the honest form is: 'under these assumptions, "
            "this claim, by this argument'</b> — <b>three things, and "
            "the first is the one people omit.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Finding your own gaps",
   "blurb": "Which is the hard skill, and is mechanical."},

  {"t": "code", "kicker": "Audit", "title": "The checklist, run on your own proof",
   "lang": "text", "code": """
  1  EVERY "OBVIOUSLY", "CLEARLY", "IT FOLLOWS"
         is a step you did not write down. Write it.
         (Module 01 section 1)

  2  EVERY HYPOTHESIS: where was it used?
         if nowhere, either the claim is stronger
         than you stated or the proof is wrong.

  3  EVERY INDUCTION: point at the line where the
         hypothesis was used, and say which
         predecessors it needed.
         (Module 03 section 1)

  4  EVERY EDGE CASE: n = 0, n = 1, the empty set,
         the single-element list, the disconnected
         graph. Does the argument still run?

  5  EVERY QUANTIFIER: is it "for all x there is a
         y" or "there is a y for all x"?
         (Module 02 section 1)

  6  AND: would somebody who wants to disbelieve
         this accept every line?

  RUN THIS ON A PROOF A WEEK OLD, NOT A FRESH ONE.
""",
   "caption": "<b>Run the audit on a proof a week old, not a fresh "
              "one</b> — you cannot see the gaps in an argument you "
              "just finished "
              "constructing.",
   "note": "Project 2's self-audit is exactly this checklist, and it "
           "reliably finds something."},

  {"t": "callout", "title": "Because you cannot see the gap in an argument you just built",
   "kind": "Why the delay is part of the method",
   "body": ["<b>While writing, you are holding the whole structure "
            "in mind</b> — <b>so the missing step is present in your "
            "head and absent from the page</b>, and you read it as "
            "though it were there.",
            "<b>A week later you are the sceptical reader</b> "
            "(Module 01 §1) — which is the reader the "
            "proof was supposed to be written "
            "for.",
            "<b>And reading it aloud catches a surprising "
            "amount</b>, because speech will not let you skim the "
            "connectives.",
            "<b>Which is CSCE 671 §01's designer blindness, "
            "arriving in mathematics</b> — <b>you cannot experience "
            "your own work as unfamiliar</b>, and every remedy is some "
            "way of manufacturing distance."]},

  {"t": "section", "label": "Part 3", "title": "Are you ready?",
   "blurb": "Honestly, which is the point of this module."},

  {"t": "bullets", "kicker": "Readiness", "title": "The test, which you should take before Semester 1",
   "items": [
     "<b>Can you prove something by induction with all three of "
     "Module 03's requirements visible</b>, without looking "
     "anything up?",
     "",
     "<b>Can you prove 3n² + 7n = O(n²) by exhibiting c "
     "and n₀?</b> "
     "(Module 09 §2).",
     "",
     "<b>Can you solve T(n) = 2T(n/2) + n and say which case of "
     "the master theorem it is?</b> "
     "(Module 10).",
     "",
     "<b>Can you do the 99% test calculation</b> by counting a "
     "million people? (Module 11 §3).",
     "",
     "<b>And can you compute an expected count by indicator "
     "variables?</b> (Module 12 §2).",
   ],
   "footnote": "<b>Five questions.</b> If you can answer all five "
               "without reference, start Semester 1; if not, the gaps "
               "name the modules to "
               "revisit."},

  {"t": "section", "label": "Part 4", "title": "The rule",
   "blurb": "Which is the program's, and starts here."},

  {"t": "callout", "title": "State what you proved, state what you assumed, and never claim more than you established",
   "kind": "Closing",
   "body": ["<b>This is the rule every course in the program closes "
            "on</b>, and <b>it begins here, in its original "
            "form</b> — <b>because a proof is where the distinction "
            "between established and believed is "
            "sharpest.</b>",
            "<b>In CSCE 629 it becomes a stated complexity with its "
            "model named</b>; <b>in CSCE 628 a methods section</b>; "
            "<b>in CSCE 640 a problem, a baseline, and a "
            "machine</b>.",
            "<b>And they are all this:</b> <b>a claim is a claim "
            "about an argument, and the argument is the part somebody "
            "else can check.</b>",
            "<b>Which is also why the proof portfolio keeps the "
            "wrong versions</b> — <b>a record of what you believed and "
            "why it failed is worth more than a record of what turned "
            "out to be true.</b>"]},
 ],
 "takeaways": [
   "A proof establishes the stated claim under the stated hypotheses, and "
   "nothing broader.",
   "A theorem you cited is a hypothesis you did not check.",
   "Run the audit on a proof a week old, not a fresh one.",
   "You cannot see the gap in an argument you just built, because the "
   "missing step is in your head and not on the page.",
   "Five questions decide readiness, and the ones you fail name the modules "
   "to revisit.",
   "A record of what you believed and why it failed is worth more than a "
   "record of what turned out to be true.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a proof establishes"),
  ("callout", "A proof establishes the stated claim under the stated "
              "hypotheses, and nothing broader",
   ["<b>Which hypotheses</b> — <b>including the ones you used "
    "without noticing</b>: that n is positive, that the graph is simple "
    "(Module 07 &sect;1), that the list is non-empty, that the set is "
    "finite (Module 04 &sect;1's empty-case trap).",
    "<b>What exactly was proved</b> — <b>'for all n' and 'for "
    "all sufficiently large n' are different claims</b>, and both are "
    "common; so are 'there exists' and 'we can construct'.",
    "<b>And what was assumed from elsewhere</b> — <b>a theorem "
    "you cited is a hypothesis you did not check</b>, and if its "
    "conditions do not hold in your setting then your proof does not "
    "either.",
    "<b>So the honest form is: 'under these assumptions, this "
    "claim, by this argument'</b> — <b>three things, and the first "
    "is the one people omit</b>, usually because the assumptions felt "
    "too obvious to mention, which is exactly when they are worth "
    "mentioning."]),

  ("h1", "2 &nbsp; Finding your own gaps"),
  ("code", """1  EVERY "OBVIOUSLY", "CLEARLY", "IT FOLLOWS THAT"
       is a step you did not write down. Write it.
       (Module 01 section 1)

2  EVERY HYPOTHESIS: where was it used?
       if nowhere, then either the claim is stronger
       than you stated it or the proof is wrong.

3  EVERY INDUCTION: point at the exact line where
       the inductive hypothesis was used, and say
       which predecessors it needed.
       (Module 03 section 1)

4  EVERY EDGE CASE: n = 0, n = 1, the empty set, the
       single-element list, the disconnected graph.
       Does the argument still run?

5  EVERY QUANTIFIER: is it "for all x there is a y"
       or "there is a y for all x"?
       (Module 02 section 1)

6  AND: would somebody who actively wants to
       disbelieve this accept every single line?

RUN THIS ON A PROOF A WEEK OLD, NOT A FRESH ONE."""),
  ("callout", "Because you cannot see the gap in an argument you just built",
   ["<b>While you are writing, you are holding the entire structure "
    "in your head</b> — <b>so the missing step is present in your "
    "mind and absent from the page</b>, <b>and you read it as though it "
    "were there</b>, every time, no matter how carefully you "
    "look.",
    "<b>A week later you are the sceptical reader</b> "
    "(Module 01 &sect;1) — <b>which is the reader the proof was "
    "supposed to be written for in the first place</b>, and the only "
    "one whose acceptance means anything.",
    "<b>And reading it aloud catches a surprising amount</b>, "
    "because <b>speech will not let you skim the connectives</b>: "
    "'therefore' and 'it follows that' have to be said, and saying them "
    "makes you notice whether they are earned.",
    "<b>Which is CSCE 671 Module 01's designer blindness arriving "
    "in mathematics</b> — <b>you cannot experience your own work "
    "as unfamiliar</b> — and <b>every remedy is some way of "
    "manufacturing distance</b>: time, reading aloud, or another "
    "person. <b>Project 2's self-audit is exactly this checklist, and "
    "it reliably finds something.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Are you ready?"),
  ("ul", ["<b>Can you prove something by induction with all three of "
          "Module 03's requirements visible</b> — base case "
          "computed, hypothesis named, use pointed at — <b>without "
          "looking anything up?</b>",
          "<b>Can you prove 3n<super>2</super> + 7n = "
          "O(n<super>2</super>) by exhibiting a c and an "
          "n<sub>0</sub>?</b> (Module 09 &sect;2.)",
          "<b>Can you solve T(n) = 2T(n/2) + n and say which case of "
          "the master theorem it is, and why?</b> (Module 10.)",
          "<b>Can you do the 99% test calculation by counting a "
          "million people, and explain why the answer is 1%?</b> "
          "(Module 11 &sect;3.)",
          "<b>And can you compute an expected count by indicator "
          "variables, and say why dependence does not matter?</b> "
          "(Module 12 &sect;2.) <b>Five questions.</b> <b>If you can "
          "answer all five without reference, start Semester 1</b>; "
          "<b>if not, the ones you failed name exactly the modules to "
          "revisit</b>, which is a far more useful outcome than a "
          "score."]),

  ("h1", "4 &nbsp; The rule"),
  ("callout", "State what you proved, state what you assumed, and never claim "
              "more than you established",
   ["<b>This is the rule that every one of the thirty-six courses in "
    "this program closes on</b>, and <b>it begins here, in its original "
    "form</b> — <b>because a proof is where the distinction between "
    "what is established and what is merely believed is sharpest and "
    "most checkable.</b>",
    "<b>In CSCE 629 it becomes a stated complexity with its "
    "machine model named</b>; <b>in CSCE 628 a five-part methods "
    "section</b>; <b>in CSCE 640 a problem, a baseline, and a "
    "machine</b>; <b>in CSCE 717 a solution concept, an agent model, "
    "and an impossibility.</b>",
    "<b>And they are all this one instruction:</b> <b>a claim is a "
    "claim about an argument, and the argument is the part somebody "
    "else can check</b> — which is why the argument is what gets "
    "written down.",
    "<b>Which is also why the proof portfolio keeps the wrong "
    "versions</b> (Project 1's requirement) — <b>a record of what "
    "you believed and why it failed is worth more than a record of what "
    "turned out to be true</b>, because the second teaches nothing about "
    "how you go wrong."]),
 ],
 "resources": [
   ("Velleman &mdash; How to Prove It, the final chapters",
    "https://www.cambridge.org/9781108424189",
    "<b>&sect;&sect;1 and 2</b> — writing proofs for a reader, which "
    "is the skill this module is about. Library copy."),
   ("Lamport &mdash; How to Write a 21st Century Proof (free)",
    "https://lamport.azurewebsites.net/pubs/proof.pdf",
    "<b>&sect;2</b> — a structured proof format designed so that gaps "
    "are visible, by somebody who found errors in published "
    "work."),
   ("Lehman, Leighton & Meyer, the false proofs (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>&sect;2</b> — worked examples of arguments that look right "
    "and are not, which is the best practice material there "
    "is."),
   ("Pólya &mdash; How to Solve It, the looking-back chapter",
    "https://press.princeton.edu/books/paperback/9780691164076/how-to-solve-it",
    "<b>&sect;2</b> — the step after finding a proof, which is where "
    "the learning is. Library copy."),
 ],
 "exercises": [
   "<b>State the three parts</b> of an honest claim for one of your "
   "proofs.",
   "<b>List the hypotheses you used without noticing</b> in three "
   "proofs.",
   "<b>Find a cited theorem</b> whose conditions you did not "
   "check.",
   "<b>Run the six-point audit</b> on a proof you wrote last "
   "month.",
   "<b>Read one of your proofs aloud</b> and note what you "
   "stumble on.",
   "<b>Swap proofs with somebody</b> and audit each other's.",
   "<b>Find three published false proofs</b> and locate the gap in "
   "each.",
   "<b>Take the five readiness questions</b> without reference "
   "material.",
   "<b>Name the modules</b> your failures point at, and spend a week "
   "there.",
   "<b>Project 2 is now due.</b> Submit the full thirty-proof "
   "portfolio, the wrong versions with their errors named, the three "
   "recurrences solved three ways, and the self-audit with at least two "
   "gaps found in your own earlier work.",
 ],
 "selfcheck": [
   "What does a proof establish, in three parts?",
   "Why is a cited theorem a hypothesis?",
   "Give the six-point audit.",
   "Why run it on an old proof rather than a fresh one?",
   "Why can you not see your own gaps?",
   "What two remedies manufacture distance?",
   "Give the five readiness questions.",
   "What should you do with the ones you fail?",
   "State the program's closing rule.",
   "Why does the portfolio keep the wrong versions?",
 ],
},

]
