# -*- coding: utf-8 -*-
"""CSCE 629 — Modules 11-13."""

MODULES = [

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Network Flow and Matching",
 "subtitle": "One algorithm, an implausible number of applications.",
 "question": "Why does so much reduce to pushing water through pipes?",
 "outcomes": [
     "State the max-flow min-cut theorem and explain why it holds.",
     "Implement Ford–Fulkerson and Edmonds–Karp.",
     "Explain residual graphs and why reverse edges are necessary.",
     "Model bipartite matching, project selection, and segmentation as flow.",
     "Recognise when a problem is secretly a flow problem.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "Pipes, capacities, and one source and sink."},

  {"t": "bullets", "kicker": "Setup", "title": "What a flow network is",
   "items": [
     "A directed graph with a capacity c(u,v) ≥ 0 on each edge.",
     "A <b>source</b> s and a <b>sink</b> t.",
     "",
     "A <b>flow</b> assigns f(u,v) to each edge subject to:",
     ("<b>Capacity:</b> 0 ≤ f(u,v) ≤ c(u,v)", 1),
     ("<b>Conservation:</b> at every vertex except s and t, flow in = flow "
      "out", 1),
     "",
     "The <b>value</b> of a flow is the net amount leaving s.",
     "",
     "Goal: maximise it.",
   ]},

  {"t": "callout", "title": "Max-flow min-cut", "kind": "The theorem",
   "body": ["An <b>s–t cut</b> partitions the vertices with s on one "
            "side and t on the other. Its capacity is the total capacity of "
            "edges crossing forward.",
            "<b>The maximum flow equals the minimum cut capacity.</b>",
            "One direction is easy: every flow must cross every cut, so "
            "flow ≤ any cut capacity. The hard direction is that "
            "equality is achieved — and the proof is constructive, which "
            "is what gives the algorithm.",
            "This is one of the great theorems in combinatorial optimisation, "
            "and a surprising number of other results are corollaries of it."]},

  {"t": "section", "label": "Part 2", "title": "Finding the max flow",
   "blurb": "Augmenting paths, and the trick that makes them sufficient."},

  {"t": "bullets", "kicker": "Ford–Fulkerson", "title": "The algorithm",
   "items": [
     "While an augmenting path from s to t exists in the <b>residual "
     "graph</b>:",
     ("Push as much flow along it as the bottleneck allows.", 1),
     ("Update the residual graph.", 1),
     "",
     "Terminates when no augmenting path remains — and at that moment "
     "the flow is maximum.",
     "",
     "The reachable set from s in the final residual graph <b>is</b> the "
     "minimum cut.",
     ("So you get the cut for free, which is often what you actually "
      "wanted.", 1),
   ],
   "note": "Emphasise that min-cut falls out of the algorithm. Many "
           "applications want the cut, not the flow."},

  {"t": "callout", "title": "Residual edges: why you must be able to undo",
   "kind": "The crucial idea",
   "body": ["The residual graph has, for every edge with flow f and capacity "
            "c: a forward edge of residual capacity c−f, <b>and a "
            "reverse edge of capacity f</b>.",
            "The reverse edge represents <i>cancelling</i> flow you already "
            "sent. Without it the algorithm is a greedy algorithm, and greedy "
            "fails here — an early bad routing decision becomes "
            "permanent.",
            "With reverse edges, a later augmenting path can reroute earlier "
            "flow as a side effect of pushing new flow. That is precisely "
            "what makes augmenting paths sufficient to reach the optimum.",
            "This is the single idea in the module. Everything else is "
            "bookkeeping."]},

  {"t": "table", "kicker": "Variants", "title": "Path choice decides the bound",
   "header": ["Algorithm", "Path choice", "Complexity"],
   "widths": [3.3, 4.4, 4.4],
   "rows": [
     ["Ford–Fulkerson", "Any augmenting path", "O(E · maxflow) — may not terminate on irrationals"],
     ["Edmonds–Karp", "Shortest path (BFS)", "O(VE²)"],
     ["Dinic", "Blocking flows on level graph", "O(V²E); O(E√V) for matching"],
     ["Push-relabel", "Local pushes, no paths", "O(V³) or better"],
   ],
   "footnote": "Edmonds–Karp is Ford–Fulkerson with BFS — a "
               "one-line change that makes the bound independent of capacities.",
   "note": "The irrational-capacity non-termination result is a good "
           "illustration that 'obviously it finishes' deserves scrutiny."},

  {"t": "section", "label": "Part 3", "title": "Why this matters",
   "blurb": "The reductions are the point. Flow itself is rarely the "
            "question."},

  {"t": "bullets", "kicker": "Reduction 1", "title": "Bipartite matching",
   "items": [
     "Given two sets and allowed pairings, find the largest set of disjoint "
     "pairs.",
     "",
     "<b>Reduction:</b> add a source into all of L, a sink out of all of R, "
     "capacity 1 on every edge.",
     "",
     "Max flow = maximum matching. Integrality guarantees the flow is 0/1, so "
     "it <i>is</i> a matching.",
     "",
     "Applications: job assignment, scheduling, resource allocation, stable "
     "pairing variants, könig's theorem.",
   ]},

  {"t": "table", "kicker": "Reductions", "title": "Problems that are secretly flow",
   "header": ["Problem", "Modelled as"],
   "widths": [4.6, 7.5],
   "rows": [
     ["Bipartite matching", "Unit capacities, source into L, sink out of R"],
     ["Edge-disjoint paths", "Unit capacity on every edge; max flow = path count"],
     ["Vertex-disjoint paths", "Split each vertex into in/out with a unit edge between"],
     ["Project selection", "Min cut separating profitable projects from their costs"],
     ["Image segmentation", "Min cut between foreground and background likelihoods"],
     ["Baseball elimination", "Can team X still win? — a flow feasibility question"],
     ["Airline scheduling", "Min flow covering all required flights"],
   ],
   "note": "The segmentation row is worth dwelling on for a graphics student "
           "— graph cuts are a standard tool in vision."},

  {"t": "callout", "title": "Vertex splitting: the trick to remember",
   "kind": "Technique",
   "body": ["Flow constrains <i>edges</i>, not vertices. To put a capacity on "
            "a vertex — 'this router handles at most 10 units', 'this "
            "person can take at most 3 jobs' — split it.",
            "Replace v with v_in and v_out, join them by an edge of the "
            "desired capacity, and redirect all incoming edges to v_in and "
            "all outgoing edges from v_out.",
            "Every path through v must now traverse that one edge, so the "
            "vertex constraint is enforced. This one trick converts a large "
            "family of apparently non-flow problems into flow problems."]},

  {"t": "bullets", "kicker": "Min cut", "title": "Often the cut is the answer",
   "items": [
     "Many applications want the <b>cut</b>, not the flow.",
     "",
     "<b>Image segmentation:</b> pixels are vertices; edges to a source "
     "(foreground) and sink (background) weighted by likelihood; edges "
     "between neighbours weighted by similarity.",
     ("The min cut is the segmentation that best balances per-pixel evidence "
      "against boundary smoothness.", 1),
     "",
     "<b>Project selection:</b> projects with profits, prerequisites with "
     "costs. The min cut selects the profitable closed subset.",
     "",
     "Max-flow min-cut means one algorithm answers both.",
   ]},

  {"t": "bullets", "kicker": "Recognition", "title": "Signs you are looking at a flow problem",
   "items": [
     "Something is being <b>assigned</b> or <b>routed</b> under capacity "
     "limits.",
     "A <b>bipartite</b> structure — two groups with allowed pairings.",
     "You are asked to <b>separate</b> two things as cheaply as possible.",
     "<b>Conservation</b> appears naturally — what goes in comes out.",
     "A greedy approach nearly works but gets stuck committed to an early "
     "choice.",
     "",
     "That last one is the strongest signal: flow is greedy plus the ability "
     "to undo.",
   ],
   "footnote": "The hard part is never the algorithm. It is seeing that the "
               "problem is flow."},
 ],
 "takeaways": [
   "Max flow equals min cut. One algorithm answers both, and the cut falls "
   "out of the final residual graph for free.",
   "Residual reverse edges let later augmentations undo earlier routing "
   "decisions. Without them augmenting paths would not suffice.",
   "Edmonds–Karp is Ford–Fulkerson with BFS — one line, and "
   "the bound stops depending on capacities.",
   "Bipartite matching is flow with unit capacities; integrality makes the "
   "flow a matching automatically.",
   "Vertex splitting converts vertex capacities into edge capacities, which "
   "extends flow to a large family of problems.",
   "The skill is recognition. Assignment under capacity, bipartite structure, "
   "or cheapest separation all signal flow.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Flow networks"),
  ("p", "A flow network is a directed graph with a non-negative capacity on "
        "each edge, a source s, and a sink t. A <b>flow</b> assigns a value "
        "to each edge subject to two constraints:"),
  ("ul", ["<b>Capacity:</b> 0 &le; f(u,v) &le; c(u,v) on every edge.",
          "<b>Conservation:</b> at every vertex other than s and t, total "
          "flow in equals total flow out."]),
  ("p", "The <b>value</b> of the flow is the net flow out of s, and the "
        "problem is to maximise it. The physical metaphor — water "
        "through pipes — is accurate and worth keeping, because the "
        "intuitions it supplies are correct."),
  ("h2", "1.1 &nbsp; Cuts"),
  ("p", "An <b>s&ndash;t cut</b> partitions the vertices into (S, T) with "
        "s &isin; S and t &isin; T. Its capacity is the sum of capacities of "
        "edges going from S to T (edges in the reverse direction do not "
        "count)."),
  ("p", "Every unit of flow from s to t must cross every such cut, so the "
        "value of any flow is at most the capacity of any cut. That direction "
        "is immediate. The content of the theorem is that the bound is "
        "tight."),
  ("callout", "Max-flow min-cut theorem",
   ["<b>The maximum value of an s&ndash;t flow equals the minimum capacity of "
    "an s&ndash;t cut.</b>",
    "The proof is constructive: when the augmenting-path algorithm "
    "terminates, the set of vertices still reachable from s in the residual "
    "graph forms one side of a minimum cut, and its capacity equals the flow "
    "value.",
    "This means you do not merely know the two numbers are equal — the "
    "algorithm hands you the actual cut. Many applications want the cut and "
    "treat the flow as a means to it."]),

  ("h1", "2 &nbsp; Ford&ndash;Fulkerson and the residual graph"),
  ("p", "The algorithm is almost trivially simple: while there is a path from "
        "s to t with spare capacity, push flow along it. The difficulty is "
        "that a naive version of this is greedy and greedy fails — an "
        "early routing choice can block the optimum, exactly as in Module 09. "
        "The residual graph is the repair."),
  ("h2", "2.1 &nbsp; Residual capacities"),
  ("p", "For each edge (u,v) carrying flow f out of capacity c, the residual "
        "graph contains:"),
  ("ul", ["a <b>forward</b> edge (u,v) with residual capacity c &minus; f "
          "— how much more you could send;",
          "a <b>reverse</b> edge (v,u) with residual capacity f — how "
          "much you could take back."]),
  ("callout", "The reverse edge is the whole idea",
   ["Sending flow along a reverse edge means <i>cancelling</i> flow you "
    "previously committed. It lets a later augmenting path reroute earlier "
    "decisions as a side effect of pushing new flow.",
    "Without reverse edges the algorithm is greedy and can stall below the "
    "optimum. With them, the theorem guarantees that if no augmenting path "
    "exists the flow is maximum — there is no longer any way to be "
    "stuck in a locally-committed state.",
    "If you remember one thing from this module, remember that flow is "
    "<i>greedy plus the ability to undo</i>, and that the undo is implemented "
    "as an edge in a derived graph."]),
  ("h2", "2.2 &nbsp; Choosing the augmenting path"),
  ("table", ["Algorithm", "Path selection", "Complexity", "Note"],
   [["Ford&ndash;Fulkerson", "Any augmenting path", "O(E &middot; |f*|)",
     "Depends on capacity <i>values</i>. With irrational capacities it may "
     "fail to terminate at all — a good reminder that termination needs "
     "proving."],
    ["Edmonds&ndash;Karp", "Shortest (fewest edges), via BFS", "O(VE&#178;)",
     "A one-line change from the above, and the bound becomes independent of "
     "capacities."],
    ["Dinic", "Blocking flows on a level graph", "O(V&#178;E)",
     "O(E&radic;V) on unit-capacity graphs, which makes it the practical "
     "choice for bipartite matching."],
    ["Push&ndash;relabel", "Local pushes, no path search", "O(V&#179;)",
     "Often fastest in practice on dense graphs."]],
   [0.21, 0.26, 0.17, 0.36]),

  ("break",),
  ("h1", "3 &nbsp; Reductions: the actual point"),
  ("p", "Flow is rarely the question anyone asks. Its importance is that an "
        "implausible range of problems reduce to it, and the reduction is "
        "usually the hard and interesting step."),
  ("h2", "3.1 &nbsp; Bipartite matching"),
  ("p", "Given sets L and R and a set of permitted pairs, find the largest "
        "collection of pairs using no element twice."),
  ("ol", ["Add a source s with a capacity-1 edge to each vertex of L.",
          "Keep each permitted pair as a capacity-1 edge from L to R.",
          "Add a sink t with a capacity-1 edge from each vertex of R.",
          "Compute the maximum flow. Its value is the size of the maximum "
          "matching, and the saturated L&ndash;R edges are the matching."]),
  ("callout", "Why the flow is automatically a matching",
   ["The <b>integrality theorem</b>: if all capacities are integers, there is "
    "a maximum flow in which every edge carries an integer amount, and "
    "augmenting-path algorithms find such a flow.",
    "With unit capacities, every edge therefore carries 0 or 1, so the "
    "solution is a genuine set of disjoint pairs rather than a fractional "
    "assignment. This is not an accident of the construction — it is a "
    "property of flow that makes a great many combinatorial reductions "
    "work."]),
  ("h2", "3.2 &nbsp; Vertex capacities"),
  ("p", "Flow constrains edges. To constrain a <i>vertex</i> — a router "
        "handling limited traffic, a worker taking at most three tasks, a "
        "path visiting each node once — split it:"),
  ("eq", "v &nbsp;&rarr;&nbsp; v<sub>in</sub> &rarr; v<sub>out</sub>, &nbsp; capacity on the connecting edge"),
  ("p", "Redirect every incoming edge to v<sub>in</sub> and every outgoing "
        "edge from v<sub>out</sub>. Any path through v must traverse the "
        "connecting edge, so its capacity bounds the traffic through the "
        "vertex. This single trick brings vertex-disjoint paths, node "
        "capacities, and several scheduling constraints into the flow "
        "framework."),
  ("h2", "3.3 &nbsp; Min cut as the answer"),
  ("p", "Several important applications want the cut rather than the flow."),
  ("table", ["Application", "Construction", "What the min cut gives"],
   [["<b>Image segmentation</b>",
     "Each pixel is a vertex. Edges to the source and sink weighted by how "
     "much the pixel looks like foreground or background. Edges between "
     "neighbouring pixels weighted by similarity.",
     "The labelling that best balances per-pixel evidence against boundary "
     "smoothness. This is the graph-cuts method, standard in computer "
     "vision."],
    ["<b>Project selection</b>",
     "Profitable projects joined to the source with their profit; costly "
     "prerequisites joined to the sink with their cost; infinite-capacity "
     "edges encoding dependencies.",
     "The maximum-profit set of projects that is closed under its "
     "prerequisites."],
    ["<b>Baseball elimination</b>",
     "Remaining games as flow that must be distributed among teams.",
     "Whether a given team can still finish first — a feasibility "
     "question, answered by whether the flow saturates."]],
   [0.20, 0.44, 0.36]),

  ("h1", "4 &nbsp; Recognising a flow problem"),
  ("p", "The algorithms here are in every library. The skill worth developing "
        "is noticing that a problem <i>is</i> a flow problem, which is "
        "frequently well disguised."),
  ("ul", ["Something is <b>assigned</b> or <b>routed</b> subject to capacity "
          "limits.",
          "There is a <b>bipartite</b> structure: two groups and a set of "
          "permitted pairings.",
          "You are asked to <b>separate</b> two things as cheaply as "
          "possible — that is a min cut.",
          "<b>Conservation</b> arises naturally: whatever enters a node "
          "leaves it.",
          "<b>A greedy approach almost works</b> but gets permanently stuck "
          "on an early commitment. This is the strongest signal of all, "
          "because flow is exactly greedy with the ability to undo."]),
  ("callout", "The honest summary",
   ["You will almost never implement a max-flow algorithm from scratch — "
    "good implementations exist everywhere.",
    "What you will do, if you have learned this module properly, is look at a "
    "scheduling, allocation, or separation problem that nobody described as a "
    "graph problem and realise it is one. That recognition is worth far more "
    "than the ability to code Dinic's algorithm from memory."]),
 ],
 "resources": [
   ("MIT 6.046J — Network Flow, Max-Flow Min-Cut",
    "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
    "Two lectures: the theorem with proof, then the reductions."),
   ("Jeff Erickson, Algorithms — Maximum Flow and Applications chapters",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "The best free treatment of the reductions, which is the part worth "
    "studying hardest."),
   ("Boykov & Kolmogorov — graph cuts in vision (free preprint)",
    "https://www.csd.uwo.ca/~yboykov/Papers/pami04.pdf",
    "How min cut became a standard tool in image segmentation. Directly "
    "relevant if you are heading toward CSCE 748."),
   ("CSES Problem Set — Graph section (flow problems)",
    "https://cses.fi/problemset/",
    "Auto-graded practice on matching, disjoint paths, and min cut."),
 ],
 "exercises": [
   "Implement Ford&ndash;Fulkerson with DFS path selection, then "
   "Edmonds&ndash;Karp with BFS. Construct a graph where the DFS version "
   "takes many more augmentations and measure the difference.",
   "Build the classic example where Ford&ndash;Fulkerson with a bad path "
   "choice takes a number of augmentations proportional to the capacity "
   "value, and confirm Edmonds&ndash;Karp avoids it.",
   "Remove reverse residual edges from your implementation and find a graph "
   "where it now returns a suboptimal flow. This is the clearest way to "
   "understand why they exist.",
   "Reduce bipartite matching to flow and solve a job-assignment instance. "
   "Verify the resulting flow is integral.",
   "Implement vertex splitting and solve a vertex-disjoint paths problem.",
   "Implement a two-label image segmentation by min cut on a small greyscale "
   "image. Use intensity difference for neighbour weights, and report how the "
   "smoothness weight changes the result.",
   "Extract the minimum cut from your final residual graph and verify its "
   "capacity equals the max flow value.",
 ],
 "selfcheck": [
   "State the max-flow min-cut theorem. Which direction is easy, and why?",
   "What are residual reverse edges and what would go wrong without them?",
   "What single change turns Ford&ndash;Fulkerson into Edmonds&ndash;Karp, "
   "and what does it buy?",
   "Describe the reduction from bipartite matching to flow, and explain why "
   "the resulting flow is a genuine matching.",
   "How do you impose a capacity on a vertex rather than an edge?",
   "Give three signals that a problem you are looking at might be a flow "
   "problem.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "NP-Completeness and Reductions",
 "subtitle": "Knowing when to stop looking for an exact efficient algorithm.",
 "question": "How do you show a problem is hard, and what do you do then?",
 "outcomes": [
     "Define P, NP, NP-hard, and NP-complete precisely.",
     "Explain what a polynomial-time reduction is and in which direction it "
     "runs.",
     "Prove a problem NP-complete by reduction from a known one.",
     "Name the standard starting problems and their typical uses.",
     "Explain what NP-completeness does and does not rule out.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The classes",
   "blurb": "Defined by verification, not by difficulty."},

  {"t": "table", "kicker": "Definitions", "title": "P, NP, and the rest",
   "header": ["Class", "Definition", "Example"],
   "widths": [2.6, 5.6, 3.9],
   "rows": [
     ["P", "Solvable in polynomial time", "Shortest path, matching, MST"],
     ["NP", "A proposed solution is <i>verifiable</i> in polynomial time", "SAT, clique, Hamiltonian cycle"],
     ["NP-hard", "At least as hard as everything in NP", "TSP optimisation, halting"],
     ["NP-complete", "In NP <b>and</b> NP-hard", "SAT, 3-SAT, vertex cover"],
   ],
   "note": "The key correction: NP is about verification, not about "
           "non-determinism being spooky and not about 'not polynomial'."},

  {"t": "callout", "title": "NP does not mean 'not polynomial'",
   "kind": "The common error",
   "body": ["NP stands for <b>nondeterministic polynomial</b>, and the "
            "practical definition is: a <i>claimed</i> solution can be "
            "checked in polynomial time.",
            "Given a proposed satisfying assignment, you can verify it by "
            "substitution in linear time. Given a proposed Hamiltonian cycle, "
            "you can check it is one. That is what puts these problems in NP.",
            "<b>P ⊆ NP</b> — everything you can solve quickly you "
            "can obviously verify quickly. Whether the containment is strict "
            "is the open question, and essentially everyone believes it is."]},

  {"t": "section", "label": "Part 2", "title": "Reductions",
   "blurb": "The direction is the thing everyone gets backwards."},

  {"t": "eq", "kicker": "Reduction", "title": "A reduces to B",
   "eqs": [
     ("A ≤ₚ B",
      "A polynomial-time transformation turning any instance of A into an "
      "equivalent instance of B."),
     ("if B is easy, then A is easy",
      "Solve A by transforming and calling B's algorithm."),
     ("if A is hard, then B is hard",
      "The contrapositive — and this is the direction you use for "
      "hardness proofs."),
   ],
   "caption": "To show B is hard, reduce a <b>known hard</b> problem to it. "
              "Reducing B to something hard proves nothing.",
   "note": "Have them say it aloud: 'known hard problem INTO my problem'. The "
           "direction error is the single most common mistake in this "
           "material."},

  {"t": "callout", "title": "The direction, stated as a recipe",
   "kind": "Get this right",
   "body": ["To prove <b>your</b> problem B is NP-hard:",
            "<b>1.</b> Pick a known NP-complete problem A.",
            "<b>2.</b> Show how to turn an arbitrary instance of A into an "
            "instance of B, in polynomial time.",
            "<b>3.</b> Prove the A-instance is a yes exactly when the "
            "B-instance is a yes — <i>both</i> directions.",
            "<b>4.</b> For NP-<i>completeness</i>, also show B is in NP by "
            "giving a polynomial verifier.",
            "The mnemonic: <b>known hard problem → your problem</b>. The "
            "arrow points into the thing you are proving hard."]},

  {"t": "bullets", "kicker": "Cook–Levin", "title": "Where the first one came from",
   "items": [
     "Reductions prove relative hardness. The chain has to start somewhere.",
     "",
     "<b>Cook–Levin theorem (1971):</b> SAT is NP-complete.",
     ("Proved directly: any polynomial-time verifier can be encoded as a "
      "Boolean formula that is satisfiable exactly when the verifier "
      "accepts.", 1),
     "",
     "Karp then reduced SAT to 21 other problems, and the field had a "
     "catalogue.",
     "",
     "Today thousands of problems are known NP-complete, all tracing back "
     "through reductions to this one theorem.",
   ]},

  {"t": "table", "kicker": "Toolkit", "title": "Standard problems to reduce from",
   "header": ["Problem", "Shape", "Good for reducing to"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["3-SAT", "Clauses of 3 literals", "Almost anything — the default"],
     ["Vertex cover", "Cover all edges with k vertices", "Graph covering/selection problems"],
     ["Clique", "k mutually adjacent vertices", "Dense-subgraph problems"],
     ["Independent set", "k mutually non-adjacent", "Conflict/compatibility problems"],
     ["Hamiltonian cycle", "Visit every vertex once", "Routing, sequencing, TSP"],
     ["Subset sum", "Subset with a target sum", "Numeric, packing, partition"],
     ["3-colouring", "Colour with 3 colours", "Scheduling, register allocation"],
   ],
   "note": "Advice: pick the one whose <i>structure</i> resembles your "
           "problem. The reduction is far easier when the shapes match."},

  {"t": "code", "kicker": "Worked", "title": "Independent set ≤ₚ vertex cover",
   "lang": "text", "code": """
CLAIM   S is an independent set of G  <=>  V - S is a vertex cover of G.

(=>) Let S be independent. Take any edge (u,v).
     Both endpoints cannot be in S (S is independent, so no edge
     inside it). So at least one is in V - S.
     Therefore V - S covers every edge.

(<=) Let C be a vertex cover. Take any two vertices u,v in V - C.
     If (u,v) were an edge, C would have to contain u or v --
     contradiction. So no edge lies inside V - C.
     Therefore V - C is independent.

REDUCTION  "Is there an independent set of size >= k?"
           becomes
           "Is there a vertex cover of size <= n - k?"

Linear time, and both directions proved. Done.
""",
   "caption": "Not every reduction is this clean, but the shape is always the "
              "same: a transformation, plus a proof in both directions.",
   "note": "Worth noting that both directions are genuinely required — "
           "half a proof is a common and fatal error here."},

  {"t": "section", "label": "Part 3", "title": "So what?",
   "blurb": "What NP-completeness actually licenses you to do."},

  {"t": "bullets", "kicker": "Consequences", "title": "What it does and does not mean",
   "items": [
     "<b>Does mean:</b> no polynomial exact algorithm is known, and finding "
     "one would solve P vs NP.",
     ("So you may stop looking, and say so in a design review with a straight "
      "face.", 1),
     "",
     "<b>Does <i>not</i> mean</b> your instances are hard.",
     ("SAT solvers routinely handle industrial instances with millions of "
      "variables.", 1),
     ("Hardness is worst-case. Your inputs are not adversarial.", 1),
     "",
     "<b>Does not mean</b> no good algorithm exists — only no exact "
     "polynomial one for all inputs.",
   ],
   "note": "The SAT solver point matters. Students over-learn 'NP-complete = "
           "impossible' and then avoid approaches that would have worked."},

  {"t": "table", "kicker": "Response", "title": "Five things to do instead",
   "header": ["Strategy", "Give up", "Keep"],
   "widths": [3.2, 4.2, 4.7],
   "rows": [
     ["Approximation", "Optimality", "A proven ratio. Module 13."],
     ["Heuristics", "Any guarantee", "Good results on real instances"],
     ["Exact, exponential", "Scalability", "Optimality on small inputs"],
     ["Parameterised", "General efficiency", "Fast when a parameter is small"],
     ["Restrict inputs", "Generality", "Polynomial on your actual structure"],
   ],
   "note": "The last row is underused: many NP-hard problems are polynomial "
           "on trees, planar graphs, or bounded treewidth — and real "
           "instances often have that structure."},

  {"t": "callout", "title": "Restricting the input is often the real answer",
   "kind": "Practical advice",
   "body": ["Many NP-hard problems become polynomial on restricted inputs: "
            "graph colouring on interval graphs, independent set on trees, "
            "many problems on bounded-treewidth or planar graphs.",
            "Real instances frequently have that structure without anyone "
            "having noticed. A dependency graph is usually nearly a tree; a "
            "map is planar; a schedule has bounded overlap.",
            "Before accepting an approximation, ask what is actually true of "
            "your inputs. The answer is sometimes that your special case was "
            "never hard."]},
 ],
 "takeaways": [
   "NP is defined by polynomial-time <i>verification</i>, not by being "
   "non-polynomial.",
   "A ≤ₚ B means A is no harder than B. To prove B hard, reduce a "
   "known hard problem <b>into</b> B.",
   "Every hardness proof needs the transformation plus equivalence in both "
   "directions — and, for completeness, membership in NP.",
   "Cook–Levin started the chain by proving SAT NP-complete directly; "
   "everything else descends from it by reduction.",
   "NP-complete means no exact polynomial algorithm for <i>all</i> inputs. It "
   "says nothing about your inputs, and SAT solvers handle enormous real "
   "instances.",
   "Five responses: approximate, heuristic, exact-exponential, parameterised, "
   "or restrict the input class. The last is underused.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The classes"),
  ("p", "A <b>decision problem</b> has a yes/no answer. The theory is stated "
        "for decision problems because it makes the definitions clean; "
        "optimisation versions are handled by asking 'is there a solution of "
        "value at least k?'"),
  ("table", ["Class", "Definition", "Examples"],
   [["<b>P</b>", "Decidable in polynomial time.",
     "Shortest path, bipartite matching, MST, linear programming."],
    ["<b>NP</b>", "A proposed solution (a <i>certificate</i>) can be verified "
     "in polynomial time.",
     "SAT, clique, Hamiltonian cycle, subset sum, graph colouring."],
    ["<b>NP-hard</b>", "At least as hard as every problem in NP, via "
     "polynomial reduction. Need not itself be in NP.",
     "TSP optimisation, the halting problem (which is not in NP at all)."],
    ["<b>NP-complete</b>", "In NP and NP-hard. The hardest problems that are "
     "still verifiable.", "SAT, 3-SAT, vertex cover, clique, subset sum."]],
   [0.15, 0.45, 0.40]),
  ("callout", "The definition people get wrong",
   ["NP does <b>not</b> stand for 'not polynomial'. It stands for "
    "<i>nondeterministic polynomial</i>, and the useful definition is about "
    "verification: given a candidate answer, can you check it quickly?",
    "Given a proposed satisfying assignment for a Boolean formula, you "
    "substitute and evaluate — linear time. Given a proposed Hamiltonian "
    "cycle, you check it visits each vertex once. That is what membership in "
    "NP means.",
    "<b>P &sube; NP</b> trivially: if you can find a solution quickly you can "
    "certainly check one. Whether the inclusion is strict is the P versus NP "
    "question, open since 1971 and believed by nearly everyone to be strict."]),

  ("h1", "2 &nbsp; Reductions"),
  ("p", "A <b>polynomial-time reduction</b> from A to B, written "
        "A &le;<sub>p</sub> B, is a polynomial-time transformation taking any "
        "instance of A to an instance of B with the same yes/no answer."),
  ("p", "The meaning is: <b>A is no harder than B</b>. If you had a fast "
        "algorithm for B, you would have one for A — transform, then "
        "call it."),
  ("callout", "The direction, and why everyone gets it backwards",
   ["To prove <b>your</b> problem B is hard, you must reduce a <i>known "
    "hard</i> problem A <b>into</b> B. The logic: A is hard; if B were easy, "
    "A would be easy; therefore B is not easy.",
    "Reducing B to a known hard problem proves nothing whatsoever — "
    "every problem in NP reduces to SAT, including trivial ones.",
    "<b>Mnemonic: known hard problem &rarr; your problem.</b> The arrow "
    "points at the thing you are proving hard. Say it out loud before writing "
    "any reduction; this error accounts for most wrong proofs in this "
    "material."]),
  ("h2", "2.1 &nbsp; The recipe"),
  ("ol", ["Show B &isin; NP by describing a certificate and a polynomial-time "
          "verifier. (Needed for <i>completeness</i>; skip it if you only "
          "want NP-hardness.)",
          "Choose a known NP-complete problem A, preferably one whose "
          "structure resembles B.",
          "Give a polynomial-time transformation from an arbitrary instance "
          "of A to an instance of B.",
          "Prove the equivalence <b>in both directions</b>: the A-instance is "
          "a yes if and only if the constructed B-instance is a yes. Omitting "
          "a direction is the second most common error after getting the "
          "direction of the reduction wrong."]),
  ("h2", "2.2 &nbsp; Where the chain starts"),
  ("p", "Reductions establish relative hardness, so something must be proved "
        "hard from first principles. <b>Cook and Levin</b> did this "
        "independently around 1971 for SAT: given any polynomial-time "
        "verifier, they showed how to construct a Boolean formula that is "
        "satisfiable exactly when the verifier accepts some certificate. Every "
        "problem in NP therefore reduces to SAT."),
  ("p", "Karp followed with reductions from SAT to 21 well-known "
        "combinatorial problems, which turned an abstract theorem into a "
        "practical catalogue. Today thousands of problems are known to be "
        "NP-complete, and essentially all of them trace back through chains "
        "of reductions to Cook&ndash;Levin."),

  ("break",),
  ("h1", "3 &nbsp; A worked reduction"),
  ("p", "<b>Independent set &le;<sub>p</sub> vertex cover.</b> An independent "
        "set is a set of vertices no two of which are adjacent. A vertex "
        "cover is a set touching every edge."),
  ("p", "<b>Claim.</b> S is an independent set of G if and only if V &minus; "
        "S is a vertex cover of G."),
  ("p", "<b>(&rArr;)</b> Let S be independent and let (u,v) be any edge. Both "
        "u and v cannot lie in S, since S contains no edge. So at least one "
        "lies in V &minus; S, meaning V &minus; S covers that edge. As the "
        "edge was arbitrary, V &minus; S is a vertex cover."),
  ("p", "<b>(&lArr;)</b> Let C be a vertex cover and take u, v &isin; "
        "V &minus; C. If (u,v) were an edge, C would need to contain u or v, "
        "contradicting their membership in V &minus; C. So no edge lies "
        "within V &minus; C, which is therefore independent. &#9633;"),
  ("p", "The reduction follows immediately: 'does G have an independent set "
        "of size at least k?' becomes 'does G have a vertex cover of size at "
        "most n &minus; k?'. The transformation is the identity on the graph "
        "and arithmetic on the parameter — linear time, and both "
        "directions are proved."),
  ("h2", "3.1 &nbsp; Choosing what to reduce from"),
  ("table", ["Start from", "When your problem involves"],
   [["<b>3-SAT</b>", "Anything. The default choice, and the structure "
     "(variables and clauses) is flexible enough to encode most things."],
    ["<b>Vertex cover</b>", "Selecting a small set of elements that must "
     "touch or cover everything."],
    ["<b>Clique</b> / <b>Independent set</b>",
     "Mutual compatibility or mutual conflict among items."],
    ["<b>Hamiltonian cycle / path</b>",
     "Sequencing, routing, visiting things exactly once. The natural source "
     "for TSP-like problems."],
    ["<b>Subset sum</b> / <b>Partition</b>",
     "Numbers, weights, capacities, packing, scheduling by duration."],
    ["<b>3-colouring</b>",
     "Assigning limited resources under conflict constraints: register "
     "allocation, frequency assignment, exam timetabling."]],
   [0.26, 0.74]),
  ("p", "The practical advice is to pick the source problem whose "
        "<i>structure</i> most resembles your target. Reductions between "
        "structurally similar problems are short; reductions across a "
        "structural gap require gadgets and get painful."),

  ("h1", "4 &nbsp; What NP-completeness licenses"),
  ("callout", "What it does mean",
   ["No polynomial-time exact algorithm is known, and finding one would prove "
    "P = NP and resolve the most famous open problem in the field.",
    "So you may stop looking, and you may say so in a design review without "
    "embarrassment. That is a genuinely useful professional outcome: it "
    "converts an open-ended search into a bounded engineering decision."]),
  ("callout", "What it does not mean",
   ["<b>It does not mean your instances are hard.</b> NP-completeness is a "
    "worst-case statement over all possible inputs. Modern SAT solvers "
    "routinely dispatch industrial instances with millions of variables, "
    "because those instances have structure that adversarial ones do not.",
    "<b>It does not mean no good algorithm exists.</b> It rules out an exact "
    "polynomial algorithm correct on <i>every</i> input. Approximation "
    "algorithms with proven ratios, heuristics that work well in practice, "
    "and exact algorithms that are fast on realistic sizes are all still "
    "available.",
    "Treating 'NP-complete' as 'impossible' is a real and costly error. It "
    "leads people to abandon approaches that would have worked."]),
  ("h2", "4.1 &nbsp; The five responses"),
  ("table", ["Strategy", "What you give up", "What you keep", "Example"],
   [["<b>Approximation</b>", "Optimality",
     "A <i>proven</i> bound on how far off you can be",
     "2-approximation for vertex cover (Module 13)"],
    ["<b>Heuristics</b>", "Any guarantee at all",
     "Often excellent results on real data",
     "Simulated annealing, local search, genetic algorithms"],
    ["<b>Exact exponential</b>", "Scalability",
     "Guaranteed optimality on small instances",
     "Held&ndash;Karp TSP at O(2&#8319;n&#178;), branch and bound"],
    ["<b>Parameterised</b>", "Efficiency in general",
     "Polynomial when some parameter k is small",
     "Vertex cover in O(2&#7503; &middot; n)"],
    ["<b>Restrict the input</b>", "Generality",
     "Genuine polynomial time on your actual inputs",
     "Many problems are easy on trees, planar, or bounded-treewidth graphs"]],
   [0.19, 0.17, 0.30, 0.34]),
  ("callout", "The last row deserves more attention than it gets",
   ["A great many NP-hard problems are polynomial on restricted graph "
    "classes: independent set on trees, colouring on interval graphs, almost "
    "everything on bounded treewidth.",
    "Real instances frequently have that structure without anyone having "
    "checked. Dependency graphs are usually close to trees; geographic "
    "networks are planar; scheduling conflicts often have bounded overlap.",
    "Before settling for an approximation, find out what is actually true of "
    "your inputs. Sometimes the answer is that your special case was never "
    "hard in the first place."]),
 ],
 "resources": [
   ("MIT 6.046J — Complexity, Reductions, NP-completeness",
    "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
    "Three lectures covering the definitions, the reduction technique, and "
    "several worked hardness proofs."),
   ("Jeff Erickson, Algorithms — NP-Hardness chapter",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "The clearest free treatment, with an unusually good discussion of how to "
    "pick which problem to reduce from and many worked gadgets."),
   ("Karp — Reducibility Among Combinatorial Problems (1972, free)",
    "https://cgi.di.uoa.gr/~sgk/teaching/grad/handouts/karp.pdf",
    "The original 21 reductions. Short, readable, and historically the paper "
    "that made the theory practical."),
   ("Complexity Zoo",
    "https://complexityzoo.net/",
    "A catalogue of complexity classes, for when you encounter one you do not "
    "recognise."),
 ],
 "exercises": [
   "Prove vertex cover is NP-complete by reduction from independent set, "
   "writing out membership in NP and both directions of the equivalence.",
   "Prove clique is NP-complete by reduction from independent set via the "
   "complement graph.",
   "Reduce 3-SAT to independent set. This one needs a gadget: a triangle per "
   "clause plus edges between contradictory literals. Prove both directions.",
   "Write a reduction in the <i>wrong</i> direction for some problem and "
   "explain in one paragraph exactly why it proves nothing.",
   "Implement a brute-force exact solver and a 2-approximation for vertex "
   "cover. Compare on random graphs, and find the instance size at which "
   "exact becomes infeasible.",
   "Take a problem from your own work that you suspect is hard. Either reduce "
   "a known NP-complete problem to it, or find a polynomial algorithm. Report "
   "which, with the argument.",
   "Find an NP-hard problem that becomes polynomial on trees, implement both, "
   "and measure the difference.",
 ],
 "selfcheck": [
   "Define P and NP. What does the N stand for, and what is the useful "
   "working definition of NP?",
   "What does A &le;<sub>p</sub> B mean? To prove B hard, which direction do "
   "you reduce, and why?",
   "List the four steps of an NP-completeness proof, and name the two most "
   "common mistakes.",
   "What did Cook and Levin prove, and why was a direct proof necessary?",
   "Give two things NP-completeness does <i>not</i> tell you about your "
   "specific problem instances.",
   "Name the five standard responses to an NP-hard problem, with what each "
   "sacrifices.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Approximation Algorithms",
 "subtitle": "Provably close, when exactly right is unavailable.",
 "question": "If you cannot have the optimum, what can you guarantee?",
 "outcomes": [
     "Define approximation ratio and distinguish it from heuristic "
     "performance.",
     "Analyse approximation ratios without knowing the optimum.",
     "Apply the standard techniques: greedy, LP rounding, local search.",
     "Explain PTAS and FPTAS and give an example of each.",
     "Explain hardness of approximation results.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Guarantees",
   "blurb": "The difference between an approximation and a heuristic."},

  {"t": "eq", "kicker": "Definition", "title": "Approximation ratio",
   "eqs": [
     ("minimisation:  ALG  ≤  ρ · OPT",
      "ρ ≥ 1. A 2-approximation never exceeds twice the optimum."),
     ("maximisation:  ALG  ≥  OPT / ρ",
      "Never worse than a 1/ρ fraction of the optimum."),
     ("the guarantee holds on <b>every</b> input",
      "This is what separates an approximation algorithm from a heuristic."),
   ],
   "caption": "A heuristic may be excellent on average and arbitrarily bad "
              "once. An approximation algorithm cannot.",
   "note": "The 'every input' clause is the whole value proposition. Make it "
           "explicit."},

  {"t": "callout", "title": "The trick: bound against something you can compute",
   "kind": "Key idea",
   "body": ["You cannot compare ALG against OPT directly — if you could "
            "compute OPT you would not need an approximation.",
            "So find a quantity you <i>can</i> compute that bounds OPT: a "
            "lower bound for minimisation, an upper bound for maximisation.",
            "Then show ALG is within ρ of <i>that</i>, and the guarantee "
            "follows by transitivity.",
            "Every analysis in this module is this manoeuvre. Spotting the "
            "right bound is the creative step."]},

  {"t": "section", "label": "Part 2", "title": "Techniques",
   "blurb": "Four ways to build an algorithm with a provable ratio."},

  {"t": "code", "kicker": "Technique 1", "title": "Vertex cover: a 2-approximation from matching",
   "lang": "text", "code": """
ALGORITHM
  C = {}
  while some edge (u,v) is uncovered:
      add BOTH u and v to C
      remove all edges touching u or v
  return C

ANALYSIS
  The edges we picked form a MATCHING M -- no two share a vertex,
  since we delete all incident edges after each pick.

  Any vertex cover must include at least one endpoint of each
  edge in M, and those endpoints are all distinct.
      =>  OPT >= |M|                  <-- the computable lower bound

  We added 2 vertices per picked edge:
      =>  |C| = 2|M| <= 2 * OPT

2-approximation. And note we never computed OPT.
""",
   "caption": "Note the shape: find a computable lower bound on OPT, then "
              "bound ALG against it. Taking <i>both</i> endpoints looks "
              "wasteful and is what makes the proof work.",
   "note": "Students always propose taking the higher-degree endpoint "
           "instead. It is a better heuristic and has no bound — worth "
           "showing."},

  {"t": "bullets", "kicker": "Technique 2", "title": "LP relaxation and rounding",
   "items": [
     "Write the problem as an integer program.",
     "Relax the integrality constraint: let variables be fractional.",
     ("The LP is solvable in polynomial time.", 1),
     "",
     "<b>LP optimum ≤ integer optimum</b> for minimisation — "
     "a computable lower bound, exactly what Part 1 needs.",
     "",
     "Round the fractional solution to an integral one, and bound the damage.",
     ("Vertex cover: round xᵥ ≥ 1/2 up to 1. Gives 2-approximation "
      "again, by a completely different route.", 1),
   ],
   "note": "LP relaxation is the single most general technique here and the "
           "bridge to CSCE 669."},

  {"t": "bullets", "kicker": "Technique 3", "title": "Greedy with an analysis",
   "items": [
     "<b>Set cover:</b> repeatedly take the set covering the most uncovered "
     "elements.",
     "",
     "Each step covers at least a 1/OPT fraction of what remains.",
     ("After k steps, uncovered ≤ n(1 − 1/OPT)^k.", 1),
     ("Reaches zero after about OPT · ln n steps.", 1),
     "",
     "<b>Hₙ ≈ ln n approximation.</b>",
     "",
     "And this is <b>optimal</b>: no polynomial algorithm does better unless "
     "P = NP.",
   ],
   "footnote": "A rare case where the obvious algorithm is provably the best "
               "possible."},

  {"t": "bullets", "kicker": "Technique 4", "title": "Metric TSP from a spanning tree",
   "items": [
     "Assume the triangle inequality — true for geometric distances.",
     "",
     "<b>2-approximation:</b> build an MST, walk it depth-first, shortcut "
     "repeats.",
     ("MST ≤ OPT, since deleting an edge from the optimal tour leaves a "
      "spanning tree.", 1),
     ("The walk costs 2·MST; shortcutting only helps, by the triangle "
      "inequality.", 1),
     "",
     "<b>Christofides: 1.5-approximation</b> — add a minimum matching on "
     "the odd-degree vertices to make an Eulerian graph.",
     ("Unbeaten from 1976 until a 2020 improvement by a tiny margin.", 1),
   ],
   "note": "The MST ≤ OPT argument is the computable-lower-bound move "
           "again. Point it out."},

  {"t": "section", "label": "Part 3", "title": "Schemes and limits",
   "blurb": "When you can get arbitrarily close, and when you provably "
            "cannot."},

  {"t": "table", "kicker": "Schemes", "title": "PTAS and FPTAS",
   "header": ["", "PTAS", "FPTAS"],
   "widths": [2.6, 4.8, 4.7],
   "rows": [
     ["Guarantee", "(1+ε) for any ε &gt; 0", "Same"],
     ["Time", "Polynomial in n for each fixed ε", "Polynomial in n <b>and</b> 1/ε"],
     ["Catch", "Could be n^(1/ε) — useless in practice", "Genuinely usable"],
     ["Example", "Euclidean TSP", "0/1 knapsack"],
   ],
   "note": "The PTAS catch is real: a running time of n^(1/eps) at eps = 0.1 "
           "is n^10, which is polynomial and unusable."},

  {"t": "callout", "title": "Some problems cannot be approximated well either",
   "kind": "Hardness of approximation",
   "body": ["Approximability varies enormously, and the boundaries are "
            "themselves theorems.",
            "<b>Knapsack:</b> FPTAS — arbitrarily close, efficiently.",
            "<b>Vertex cover:</b> 2 is easy; better than 1.36 is NP-hard. Even "
            "2 may be optimal under stronger assumptions.",
            "<b>Set cover:</b> ln n, and that is provably the best possible.",
            "<b>General TSP:</b> no constant-factor approximation at all "
            "unless P = NP. Dropping the triangle inequality destroys "
            "everything.",
            "<b>Max clique:</b> inapproximable within n^(1−ε). "
            "Essentially hopeless."]},

  {"t": "bullets", "kicker": "Practice", "title": "Approximation or heuristic?",
   "items": [
     "<b>Use an approximation algorithm</b> when you need a guarantee you can "
     "state to someone else.",
     ("Contracts, safety arguments, cost bounds, published claims.", 1),
     "",
     "<b>Use a heuristic</b> when average quality matters more than the "
     "worst case.",
     ("Local search and simulated annealing routinely beat "
      "provable-ratio algorithms on real instances.", 1),
     "",
     "<b>Use both.</b> The approximation gives a bound; the heuristic gives "
     "the answer you ship.",
     ("Running both also tells you how good the heuristic actually is.", 1),
   ],
   "footnote": "That last point is the practical one: an approximation "
               "algorithm doubles as a quality yardstick for your heuristic."},

  {"t": "bullets", "kicker": "End", "title": "Where this course leaves you",
   "items": [
     "You can analyse an algorithm, and say honestly where the analysis stops "
     "predicting the machine.",
     "You can choose a technique from a problem's structure, and prove the "
     "choice correct.",
     "You can recognise a problem as a graph, flow, or DP problem when nobody "
     "has told you it is one.",
     "You can tell when to stop looking for an exact algorithm, and what to "
     "do next.",
     "",
     "<b>CSCE 614</b> explains the machine the analysis abstracts away.",
     "<b>CSCE 735</b> does this again for parallel machines.",
     "<b>CSCE 641</b> is where you will use the spatial data structures.",
   ]},
 ],
 "takeaways": [
   "An approximation ratio is a guarantee on every input. A heuristic has no "
   "guarantee at all, and that is the whole difference.",
   "You cannot compare against OPT directly. Find a computable bound on OPT "
   "and compare against that — every proof here is that move.",
   "Vertex cover: take both endpoints of a maximal matching. |M| ≤ OPT "
   "gives the factor of 2.",
   "LP relaxation gives a lower bound for free; rounding the fractional "
   "solution gives the algorithm.",
   "Greedy set cover achieves ln n, and provably nothing does better unless "
   "P = NP.",
   "Approximability varies from FPTAS to inapproximable. Which side your "
   "problem falls on is itself a theorem worth looking up.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a guarantee is"),
  ("p", "Module 12 established that for NP-hard problems you will not get an "
        "exact polynomial algorithm. One response is to accept a solution "
        "that is provably close."),
  ("eq", "minimisation: ALG &le; &rho; &middot; OPT &nbsp;&nbsp;&nbsp; maximisation: ALG &ge; OPT / &rho;"),
  ("callout", "Approximation versus heuristic",
   ["An <b>approximation algorithm</b> comes with a ratio &rho; that holds on "
    "<i>every</i> input, proved.",
    "A <b>heuristic</b> has no such guarantee. It may be far better than the "
    "approximation algorithm on typical data — local search and "
    "simulated annealing usually are — and it may be arbitrarily bad on "
    "some input, with no way to know in advance which.",
    "Neither is strictly better. The question is whether you need a statement "
    "you can defend, or an answer that is usually good."]),
  ("h2", "1.1 &nbsp; The central difficulty, and the standard manoeuvre"),
  ("p", "To prove ALG &le; 2&middot;OPT you would seem to need OPT. But if "
        "you could compute OPT you would not be approximating."),
  ("callout", "Bound against something computable",
   ["Find a quantity L you can compute, satisfying L &le; OPT (for "
    "minimisation). Then show ALG &le; &rho;&middot;L, and transitivity gives "
    "ALG &le; &rho;&middot;OPT.",
    "Every analysis in this module is this manoeuvre, and identifying the "
    "right L is the creative step. For vertex cover it is the size of a "
    "matching; for metric TSP it is the weight of a minimum spanning tree; "
    "for LP-based methods it is the value of the relaxation."]),

  ("h1", "2 &nbsp; Vertex cover: a 2-approximation"),
  ("code", """C = set()
while there is an uncovered edge (u, v):
    C.add(u); C.add(v)          # take BOTH endpoints
    remove every edge incident to u or v
return C"""),
  ("p", "<b>Analysis.</b> The edges selected by the loop form a "
        "<b>matching</b> M: after selecting (u,v) we delete every edge "
        "touching u or v, so no later selected edge shares a vertex with it."),
  ("p", "Any vertex cover must contain at least one endpoint of every edge in "
        "M. Since the edges of M are vertex-disjoint, those endpoints are all "
        "distinct, so any cover has size at least |M|. In particular "
        "<b>OPT &ge; |M|</b> — the computable lower bound."),
  ("p", "The algorithm adds exactly two vertices per edge of M, so "
        "|C| = 2|M| &le; 2&middot;OPT. &#9633;"),
  ("callout", "Taking both endpoints looks wasteful, and is the point",
   ["The obvious improvement — take only the higher-degree endpoint "
    "— is a better <i>heuristic</i> and has no provable constant ratio. "
    "It can be made to perform arbitrarily badly relative to the optimum.",
    "This is a recurring pattern: the algorithm with the clean guarantee is "
    "often not the one with the best typical behaviour. Knowing which you "
    "need is the engineering judgement."]),

  ("h1", "3 &nbsp; LP relaxation and rounding"),
  ("p", "The most general technique in the module, and the bridge to "
        "CSCE 669."),
  ("ol", ["Write the problem as an <b>integer program</b>. For vertex cover: "
          "minimise &Sigma; x&#7525; subject to x&#7524; + x&#7525; &ge; 1 for "
          "every edge, with x&#7525; &isin; {0,1}.",
          "<b>Relax</b> the integrality constraint to 0 &le; x&#7525; &le; 1. "
          "The result is a linear program, solvable in polynomial time.",
          "The LP optimum is a lower bound on the integer optimum, since "
          "every integer solution is also a feasible fractional one. That is "
          "your computable bound, obtained for free.",
          "<b>Round</b> the fractional solution to an integral one and bound "
          "the loss."]),
  ("p", "For vertex cover, every edge constraint x&#7524; + x&#7525; &ge; 1 "
        "forces at least one endpoint to have value &ge; 1/2. Round every "
        "x&#7525; &ge; 1/2 up to 1 and the rest down to 0. The result is a "
        "valid cover, and rounding at most doubles each variable, so the cost "
        "is at most twice the LP optimum, hence at most twice OPT."),
  ("p", "A 2-approximation again, by a completely different route. The "
        "<b>integrality gap</b> — the worst-case ratio between the "
        "integer and fractional optima — limits what any LP-rounding "
        "method can achieve, which makes it a useful thing to know about a "
        "formulation before investing in it."),

  ("break",),
  ("h1", "4 &nbsp; Greedy set cover: ln n, and provably optimal"),
  ("p", "Given a universe of n elements and a collection of subsets, choose "
        "the fewest subsets whose union is everything. Greedy: repeatedly "
        "take the set covering the most currently uncovered elements."),
  ("p", "<b>Analysis.</b> Suppose the optimum uses OPT sets. Those OPT sets "
        "cover everything, so at any moment some set covers at least a 1/OPT "
        "fraction of the remaining uncovered elements — otherwise the "
        "optimal sets could not cover the remainder between them. Greedy "
        "takes a set at least that good, so after k steps:"),
  ("eq", "uncovered &le; n(1 &minus; 1/OPT)<super>k</super> &lt; n&middot;e<super>&minus;k/OPT</super>"),
  ("p", "This drops below 1 once k &gt; OPT&middot;ln n, so greedy uses at "
        "most OPT&middot;ln n sets: an H&#8345; &asymp; ln n approximation."),
  ("callout", "And nothing does better",
   ["Feige proved in 1998 that no polynomial-time algorithm achieves a ratio "
    "better than (1 &minus; o(1)) ln n for set cover, unless P = NP.",
    "So the obvious greedy algorithm is, up to lower-order terms, the best "
    "possible. This is unusual and worth noticing: normally the first "
    "algorithm you think of is not optimal, and here it provably is."]),

  ("h1", "5 &nbsp; Metric TSP"),
  ("p", "General TSP admits no constant-factor approximation unless P = NP. "
        "Assume the <b>triangle inequality</b> — automatic for "
        "geometric distances — and the picture changes completely."),
  ("h2", "5.1 &nbsp; A 2-approximation from the MST"),
  ("ol", ["Build a minimum spanning tree.",
          "Walk it depth-first, listing vertices as first encountered.",
          "Shortcut past repeated vertices."]),
  ("p", "<b>Analysis.</b> Deleting any one edge from an optimal tour leaves a "
        "spanning path, which is a spanning tree, so MST &le; OPT — the "
        "computable bound. A full depth-first traversal uses every tree edge "
        "twice, costing 2&middot;MST. Shortcutting replaces a detour by a "
        "direct edge, which the triangle inequality guarantees is no longer. "
        "So the tour costs at most 2&middot;MST &le; 2&middot;OPT. &#9633;"),
  ("h2", "5.2 &nbsp; Christofides"),
  ("p", "Instead of doubling every tree edge, add a minimum-weight perfect "
        "matching on the odd-degree vertices of the MST. The result has all "
        "even degrees, so it has an Eulerian circuit, which shortcuts to a "
        "tour. The matching costs at most OPT/2, giving a "
        "<b>1.5-approximation</b>."),
  ("p", "Published in 1976, it stood as the best known ratio for metric TSP "
        "until 2020, when it was improved by a margin of roughly "
        "10<super>&minus;36</super>. That forty-four-year gap is a reasonable "
        "indication of how hard progress here is."),

  ("h1", "6 &nbsp; Schemes"),
  ("table", ["", "PTAS", "FPTAS"],
   [["Guarantee", "(1 + &epsilon;) for any fixed &epsilon; &gt; 0",
     "(1 + &epsilon;) for any &epsilon; &gt; 0"],
    ["Running time", "Polynomial in n for each fixed &epsilon;; dependence on "
     "1/&epsilon; may be arbitrary",
     "Polynomial in both n and 1/&epsilon;"],
    ["The catch", "n<super>1/&epsilon;</super> is a legal PTAS. At "
     "&epsilon; = 0.1 that is n<super>10</super> — polynomial and "
     "entirely unusable.", "None. Genuinely practical."],
    ["Example", "Euclidean TSP (Arora, Mitchell)",
     "0/1 knapsack, by rounding the values and running the DP of Module 10"]],
   [0.16, 0.42, 0.42]),
  ("h2", "6.1 &nbsp; Hardness of approximation"),
  ("p", "How well a problem can be approximated is itself a question with "
        "theorems attached, and the answers vary enormously:"),
  ("table", ["Problem", "Best known", "Hardness"],
   [["Knapsack", "FPTAS", "None — arbitrarily close, efficiently."],
    ["Vertex cover", "2", "No better than 1.36 unless P = NP; 2 may be "
     "optimal under the Unique Games Conjecture."],
    ["Metric TSP", "1.5 (Christofides)", "No better than 123/122."],
    ["Set cover", "ln n", "ln n is optimal (Feige)."],
    ["General TSP", "None", "No constant factor unless P = NP."],
    ["Max clique", "None useful",
     "Inapproximable within n<super>1&minus;&epsilon;</super>."]],
   [0.24, 0.26, 0.50]),
  ("p", "Before designing an approximation algorithm, look up what is known. "
        "Discovering that your target ratio is provably unachievable saves a "
        "great deal of time, and discovering that an FPTAS exists saves even "
        "more."),

  ("h1", "7 &nbsp; Choosing in practice"),
  ("table", ["Need", "Choice"],
   [["A guarantee you can state to a third party — a contract, a safety "
     "case, a published bound", "Approximation algorithm."],
    ["Best typical quality, no guarantee required",
     "Heuristic: local search, simulated annealing, or a tuned greedy."],
    ["Optimality on small instances",
     "Exact exponential: branch and bound, or DP over subsets."],
    ["Both a bound and a good answer",
     "Run both. The approximation bounds the optimum, which tells you how "
     "much room the heuristic has left — often the most useful "
     "information available."]],
   [0.44, 0.56]),
  ("callout", "Where this course leaves you",
   ["You can analyse an algorithm and say honestly where the analysis stops "
    "describing the machine. You can pick a technique from a problem's "
    "structure and prove the choice correct. You can see that an unfamiliar "
    "problem is really graph search, flow, or dynamic programming. And you "
    "can tell when to stop looking for an exact algorithm and what to do "
    "instead.",
    "<b>CSCE 614</b>, running alongside, explains the machine this course "
    "abstracted away. <b>CSCE 735</b> repeats the exercise for parallel "
    "hardware. <b>CSCE 641</b> is where the spatial data structures and the "
    "cost model start earning their keep."]),
 ],
 "resources": [
   ("MIT 6.046J — Approximation Algorithms",
    "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
    "Vertex cover, set cover, and TSP with the ratio proofs done carefully."),
   ("Williamson & Shmoys, The Design of Approximation Algorithms (free PDF)",
    "https://www.designofapproxalgs.com/",
    "The standard graduate text, released free by the authors. Organised by "
    "technique, which is the right way round."),
   ("Jeff Erickson, Algorithms — Approximation Algorithms chapter",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "A shorter introduction with the key proofs, good as a first pass."),
   ("Vazirani, Approximation Algorithms (author's page)",
    "https://www.ics.uci.edu/~vazirani/book.pdf",
    "The other standard reference, strong on LP duality and primal-dual "
    "methods."),
 ],
 "exercises": [
   "Implement the matching-based 2-approximation for vertex cover. Compare "
   "against a brute-force exact solver on small random graphs and record the "
   "observed ratios — they will mostly be well under 2.",
   "Implement the 'pick the highest-degree vertex' heuristic for vertex "
   "cover. Find a family of graphs on which its ratio grows without bound.",
   "Implement greedy set cover and construct an instance where it genuinely "
   "needs about ln n times the optimum.",
   "Implement the MST-based 2-approximation for metric TSP on random "
   "Euclidean points. Compare against an exact Held&ndash;Karp solution for "
   "n &le; 15, and report the observed ratios.",
   "Implement the FPTAS for knapsack by scaling and rounding values, then "
   "running the Module 10 DP. Plot solution quality against running time as "
   "&epsilon; varies.",
   "Implement a local-search heuristic for TSP (2-opt). Compare it against "
   "the MST approximation on 1,000-city instances: which gives better tours, "
   "and which gives you a bound?",
   "<b>Project 2 is now due.</b> Assemble the three-way comparison described "
   "in the syllabus — exact, approximate with a proved ratio, and "
   "heuristic — on your chosen NP-hard problem.",
 ],
 "selfcheck": [
   "Define approximation ratio for minimisation and maximisation, and state "
   "what distinguishes an approximation algorithm from a heuristic.",
   "How do you prove ALG &le; 2&middot;OPT without being able to compute OPT?",
   "Give the computable lower bound used in the vertex cover proof, and "
   "explain why it is a lower bound.",
   "Why does taking both endpoints give a provable ratio while taking the "
   "higher-degree endpoint does not?",
   "How does LP relaxation supply a lower bound for free, and what is an "
   "integrality gap?",
   "What is the difference between a PTAS and an FPTAS, and why does it "
   "matter?",
   "Name a problem with an FPTAS and one with no constant-factor "
   "approximation at all.",
 ],
},

]
