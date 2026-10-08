# -*- coding: utf-8 -*-
"""CSCE 629 — Modules 07-10."""

MODULES = [

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Shortest Paths",
 "subtitle": "Weights change everything, and negative weights change it "
             "again.",
 "question": "Why does one algorithm not cover every shortest-path problem?",
 "outcomes": [
     "Explain why BFS fails on weighted graphs.",
     "Implement Dijkstra and justify its correctness by the greedy argument.",
     "Explain why Dijkstra fails on negative edges and what Bellman–Ford "
     "does instead.",
     "Use Bellman–Ford to detect negative cycles.",
     "Choose the right algorithm from the graph's properties.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why weights break BFS",
   "blurb": "Fewest edges and shortest distance are different questions."},

  {"t": "callout", "title": "BFS optimises edge count, not distance",
   "kind": "The problem",
   "body": ["BFS finds the path with the fewest edges, because it explores "
            "strictly in order of edge count.",
            "With weights, a two-edge path of total weight 3 beats a "
            "one-edge path of weight 100. BFS will commit to the one-edge "
            "path and never reconsider.",
            "The fix is to explore in order of <i>accumulated distance</i> "
            "rather than edge count. Replace the queue with a priority queue "
            "and you have Dijkstra's algorithm — which is, once again, "
            "the same traversal with a different container."]},

  {"t": "eq", "kicker": "The core operation", "title": "Relaxation",
   "eqs": [
     ("if d[u] + w(u,v) < d[v]:  d[v] = d[u] + w(u,v)",
      "Found a better route to v through u. Every algorithm here is a "
      "schedule of relaxations."),
     ("d[v]  always an upper bound on the true distance",
      "Starts at ∞, only ever decreases, never below the truth."),
     ("the question is only: in what order?",
      "Dijkstra, Bellman–Ford, and DAG relaxation differ in the order "
      "and nothing else."),
   ],
   "caption": "Seeing all three as relaxation schedules makes them one idea "
              "rather than three algorithms to memorise.",
   "note": "This framing is worth labouring. It makes Bellman-Ford's V-1 "
           "rounds obvious rather than arbitrary."},

  {"t": "section", "label": "Part 2", "title": "Dijkstra",
   "blurb": "Greedy, and correct exactly when weights are non-negative."},

  {"t": "code", "kicker": "Dijkstra", "title": "BFS with a priority queue",
   "lang": "python", "code": """
import heapq

def dijkstra(G, s):
    d = {v: float('inf') for v in G}
    d[s] = 0
    pq = [(0, s)]
    done = set()

    while pq:
        du, u = heapq.heappop(pq)
        if u in done:                 # lazy deletion: stale entry
            continue
        done.add(u)                   # d[u] is now FINAL

        for v, w in G[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(pq, (d[v], v))   # push, don't decrease-key
    return d
""",
   "caption": "Lazy deletion — pushing duplicates and skipping stale "
              "pops — is simpler than decrease-key and faster in "
              "practice. The heap holds O(E) entries instead of O(V).",
   "note": "Most textbooks present decrease-key. Almost no real "
           "implementation uses it. Worth saying."},

  {"t": "bullets", "kicker": "Dijkstra", "title": "Why it is correct, and the assumption it needs",
   "items": [
     "<b>Claim:</b> when u is popped, d[u] is the true shortest distance.",
     "",
     "Suppose not. Then a shorter path to u exists, passing through some "
     "unfinished vertex x.",
     ("That path reaches x before u, so its length up to x is ≤ its "
      "total length ≤ d[u].", 1),
     ("So d[x] ≤ d[u], and x would have been popped first. "
      "Contradiction.", 1),
     "",
     "<b>The assumption:</b> 'the prefix is no longer than the whole path'.",
     ("True only if weights are non-negative.", 1),
     ("A negative edge later on can make the whole path shorter than its own "
      "prefix — and the proof collapses.", 1),
   ],
   "note": "Making the proof depend visibly on non-negativity means the "
           "failure case is understood rather than memorised."},

  {"t": "table", "kicker": "Complexity", "title": "The heap decides the bound",
   "header": ["Priority queue", "Complexity", "Notes"],
   "widths": [3.3, 4.0, 4.8],
   "rows": [
     ["Binary heap", "O((V + E) log V)", "The practical default"],
     ["Fibonacci heap", "O(E + V log V)", "Better in theory; large constants"],
     ["Array (dense)", "O(V²)", "Best when E ≈ V²"],
     ["Bucket (small ints)", "O(E + VC)", "Dial's algorithm; integer weights"],
   ],
   "note": "Fibonacci heaps are the standard example of an asymptotic "
           "improvement that practice ignores."},

  {"t": "section", "label": "Part 3", "title": "Negative weights",
   "blurb": "Bellman–Ford, and what a negative cycle means."},

  {"t": "bullets", "kicker": "Bellman–Ford", "title": "Relax everything, V−1 times",
   "items": [
     "Relax <b>every edge</b>, and repeat V−1 times.",
     "",
     "Why V−1: a shortest path has at most V−1 edges (more would "
     "repeat a vertex).",
     ("After round k, all shortest paths using ≤ k edges are correct.", 1),
     ("So V−1 rounds suffice.", 1),
     "",
     "O(VE) — much slower than Dijkstra, and it handles negative edges.",
     "",
     "<b>Round V:</b> if anything still improves, a negative cycle is "
     "reachable.",
   ]},

  {"t": "callout", "title": "A negative cycle means there is no answer",
   "kind": "Not a bug",
   "body": ["If a cycle has negative total weight and lies on a path from s "
            "to t, you can go round it again and get a shorter walk. And "
            "again. The shortest distance is −∞.",
            "So 'shortest path' is undefined, not merely hard. Reporting the "
            "cycle is the correct output.",
            "This is useful rather than pathological: arbitrage detection in "
            "currency exchange is exactly negative-cycle detection, after "
            "taking −log of the exchange rates."]},

  {"t": "table", "kicker": "Choosing", "title": "Which algorithm, and when",
   "header": ["Situation", "Algorithm", "Cost"],
   "widths": [4.6, 3.6, 3.9],
   "rows": [
     ["Unweighted", "BFS", "O(V + E)"],
     ["Non-negative weights", "Dijkstra", "O((V+E) log V)"],
     ["Negative edges possible", "Bellman–Ford", "O(VE)"],
     ["DAG, any weights", "Relax in topological order", "O(V + E)"],
     ["All pairs, dense", "Floyd–Warshall", "O(V³)"],
     ["All pairs, sparse + negative", "Johnson", "O(VE + V² log V)"],
     ["Known goal, good heuristic", "A*", "Often far better"],
   ],
   "note": "The DAG row is worth flagging: topological order makes negative "
           "weights free, because no vertex is ever revisited."},

  {"t": "bullets", "kicker": "A*", "title": "Dijkstra plus a hint",
   "items": [
     "Dijkstra explores in all directions equally — it has no idea where "
     "the goal is.",
     "",
     "A* orders the queue by <b>d[v] + h(v)</b>, where h estimates the "
     "remaining distance.",
     "",
     "Correct if h is <b>admissible</b> — never overestimates.",
     ("Euclidean distance is admissible for road networks.", 1),
     ("h = 0 recovers Dijkstra exactly.", 1),
     "",
     "The better h, the fewer vertices expanded. On a game map this is "
     "routinely an order of magnitude.",
   ],
   "footnote": "The standard pathfinder in games and robotics for exactly "
               "this reason."},

  {"t": "callout", "title": "Floyd–Warshall: three lines, and a DP",
   "kind": "Worth seeing early",
   "body": ["<code>for k: for i: for j: d[i][j] = min(d[i][j], d[i][k] + "
            "d[k][j])</code>",
            "The invariant: after iteration k, d[i][j] is the shortest path "
            "using only vertices from {1..k} as intermediates.",
            "This is a dynamic program — the subproblem is 'shortest "
            "path restricted to the first k intermediates' — and it is "
            "the gentlest possible introduction to Module 10. The loop order "
            "<b>must</b> have k outermost, and that is exactly a DP "
            "dependency-order requirement."]},
 ],
 "takeaways": [
   "Every shortest-path algorithm is a schedule of relaxations. They differ "
   "only in the order.",
   "BFS minimises edge count, not distance. Replacing the queue with a "
   "priority queue gives Dijkstra.",
   "Dijkstra's correctness proof assumes a path prefix is no longer than the "
   "whole path — true only for non-negative weights.",
   "Bellman–Ford relaxes all edges V−1 times because a shortest "
   "path has at most V−1 edges. A V-th improving round means a negative "
   "cycle.",
   "A negative cycle means the shortest distance is −∞, so the "
   "answer is the cycle, not a path.",
   "On a DAG, relaxing in topological order handles any weights in O(V + E).",
 ],
 "notes": [
  ("h1", "1 &nbsp; Relaxation: the one operation"),
  ("p", "Every algorithm in this module maintains an array d[] of distance "
        "<i>estimates</i>, each an upper bound on the true shortest distance, "
        "and improves them with a single operation:"),
  ("eq", "if d[u] + w(u,v) &lt; d[v] then d[v] &larr; d[u] + w(u,v)"),
  ("p", "Estimates start at &infin; (except d[s] = 0), decrease "
        "monotonically, and never drop below the truth. Once every edge "
        "satisfies d[v] &le; d[u] + w(u,v), no further improvement is "
        "possible and the estimates are exact."),
  ("callout", "The only difference between these algorithms is the order",
   ["<b>Dijkstra</b> relaxes edges out of the closest unfinished vertex, "
    "which guarantees each vertex is finalised once.",
    "<b>Bellman&ndash;Ford</b> relaxes every edge repeatedly, V&minus;1 "
    "times, making no assumption about order at all.",
    "<b>DAG relaxation</b> relaxes edges in topological order, which "
    "guarantees a vertex is finalised before any of its successors are "
    "touched.",
    "Seeing them as three relaxation schedules rather than three algorithms "
    "makes their complexities and their limitations follow naturally."]),

  ("h1", "2 &nbsp; Why BFS is not enough"),
  ("p", "BFS explores strictly in order of edge count, so it finds the path "
        "with the fewest <i>edges</i>. Once weights exist, that is a "
        "different problem: a two-edge path of total weight 3 is shorter than "
        "a one-edge path of weight 100, and BFS commits to the latter."),
  ("p", "The repair is to explore in order of accumulated <i>distance</i> "
        "rather than edge count — that is, to replace the FIFO queue "
        "with a priority queue keyed by d[v]. The result is Dijkstra's "
        "algorithm, and the structural similarity to BFS is not a "
        "coincidence; it is the same traversal with a different container, "
        "exactly as in Module 06."),

  ("h1", "3 &nbsp; Dijkstra"),
  ("code", """import heapq

def dijkstra(G, s):
    d = {v: float('inf') for v in G}
    d[s] = 0
    pq = [(0, s)]
    done = set()

    while pq:
        du, u = heapq.heappop(pq)
        if u in done:          # stale entry from an earlier, worse estimate
            continue
        done.add(u)            # d[u] is final from here on

        for v, w in G[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(pq, (d[v], v))
    return d"""),
  ("callout", "Lazy deletion instead of decrease-key",
   ["Textbook Dijkstra calls <code>decrease-key</code> to update a vertex's "
    "priority in place, keeping the heap at O(V) entries.",
    "Real implementations push a duplicate entry and discard stale pops, as "
    "above. The heap grows to O(E) entries, which costs a constant factor in "
    "the log, and in exchange you avoid maintaining handles into the heap "
    "— simpler code that is usually faster.",
    "This is worth knowing because the gap between the textbook presentation "
    "and the deployed one is wide here, and the textbook version is the one "
    "people waste time implementing."]),
  ("h2", "3.1 &nbsp; Correctness, and where the assumption enters"),
  ("p", "<b>Claim.</b> When a vertex u is popped from the priority queue, "
        "d[u] equals the true shortest distance from s to u."),
  ("p", "<b>Proof sketch.</b> Suppose not, and let u be the first vertex "
        "popped with d[u] greater than the true distance. Then there is a "
        "genuinely shorter path P from s to u. Since u is being popped now, P "
        "must leave the finished set at some point; let x be the first "
        "unfinished vertex on P. The portion of P up to x has length at most "
        "the length of all of P, which is less than d[u]. But then d[x] &lt; "
        "d[u], so x would have been popped before u. Contradiction."),
  ("callout", "Find the assumption",
   ["The step 'the portion of P up to x has length at most the length of all "
    "of P' is where non-negativity is used, and it is the only place.",
    "With a negative edge later in P, the full path can be <i>shorter</i> "
    "than its own prefix. The inequality reverses and the proof fails.",
    "This is why Dijkstra is wrong on negative edges — not as an "
    "arbitrary restriction but as a direct consequence of its greedy "
    "argument. A greedy algorithm is only as good as its exchange argument, "
    "which is Module 09's theme."]),
  ("table", ["Priority queue", "Complexity", "When"],
   [["Binary heap", "O((V + E) log V)", "The default. Nearly always right."],
    ["Fibonacci heap", "O(E + V log V)",
     "Asymptotically better, constants large enough that it rarely wins. The "
     "canonical example of theory outrunning practice."],
    ["Simple array", "O(V&#178;)",
     "Better on dense graphs where E &asymp; V&#178;, since the log "
     "disappears."],
    ["Bucket queue", "O(E + VC)",
     "Dial's algorithm, for small integer weights bounded by C."]],
   [0.20, 0.23, 0.57]),

  ("break",),
  ("h1", "4 &nbsp; Bellman&ndash;Ford"),
  ("p", "Make no assumption about order: simply relax every edge in the "
        "graph, and repeat."),
  ("code", """def bellman_ford(V, edges, s):
    d = {v: float('inf') for v in V}
    d[s] = 0

    for _ in range(len(V) - 1):           # V-1 rounds
        for (u, v, w) in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w

    for (u, v, w) in edges:               # one more round
        if d[u] + w < d[v]:
            raise NegativeCycle(v)        # still improving -> neg. cycle
    return d"""),
  ("h2", "4.1 &nbsp; Why V&minus;1 rounds"),
  ("p", "A shortest path visits no vertex twice — revisiting a vertex "
        "means traversing a cycle, and with no negative cycles that cycle has "
        "weight &ge; 0, so removing it does not lengthen the path. A simple "
        "path therefore has at most V&minus;1 edges."),
  ("p", "By induction, after round k every shortest path using at most k "
        "edges has been found: round k relaxes the k-th edge of such a path "
        "after rounds 1..k&minus;1 established the prefix. So V&minus;1 "
        "rounds suffice, giving O(VE)."),
  ("h2", "4.2 &nbsp; Negative cycles"),
  ("callout", "The answer is &minus;&infin;, which is why detection matters",
   ["If a negative-weight cycle lies on some path from s to t, you can "
    "traverse the cycle repeatedly and reduce the total without limit. The "
    "shortest distance is &minus;&infin;, and 'shortest path' is not merely "
    "hard to compute — it is undefined.",
    "After V&minus;1 rounds everything should be settled. If a V-th round "
    "still improves some estimate, a negative cycle is reachable, and "
    "reporting it is the correct output.",
    "<b>Arbitrage detection</b> is exactly this: take &minus;log of each "
    "exchange rate, and a sequence of trades that multiplies to more than 1 "
    "becomes a cycle whose weights sum to less than 0. Bellman&ndash;Ford "
    "finds it."]),

  ("h1", "5 &nbsp; The other cases"),
  ("h2", "5.1 &nbsp; DAGs"),
  ("p", "On a directed acyclic graph, relax edges in topological order. Each "
        "vertex is finalised before any vertex it points to is examined, so "
        "one pass suffices: O(V + E), and negative weights are no obstacle "
        "because nothing is ever revisited. Worth remembering — "
        "scheduling and dependency problems are frequently DAGs, and this is "
        "both faster and simpler than Bellman&ndash;Ford."),
  ("h2", "5.2 &nbsp; A*"),
  ("p", "Dijkstra expands outward in every direction because it has no "
        "information about where the target is. A* adds a heuristic h(v) "
        "estimating the remaining distance and orders the queue by "
        "d[v] + h(v) — preferring vertices that look like progress "
        "toward the goal."),
  ("ul", ["Correct if h is <b>admissible</b>: it never overestimates the true "
          "remaining distance.",
          "If additionally h is <b>consistent</b> (h(u) &le; w(u,v) + h(v)), "
          "no vertex is expanded twice and the implementation is as simple as "
          "Dijkstra's.",
          "h = 0 is admissible and recovers Dijkstra exactly. Euclidean "
          "distance is admissible on a road network or a game map.",
          "The better the heuristic, the fewer vertices expanded — "
          "routinely an order of magnitude on a grid map, which is why A* is "
          "the standard pathfinder in games and robotics."]),
  ("h2", "5.3 &nbsp; All pairs"),
  ("p", "Floyd&ndash;Warshall computes shortest paths between every pair in "
        "O(V&#179;) and three lines:"),
  ("code", """for k in V:
    for i in V:
        for j in V:
            d[i][j] = min(d[i][j], d[i][k] + d[k][j])"""),
  ("callout", "This is a dynamic program, and a useful preview of Module 10",
   ["The invariant: after the iteration for k, d[i][j] is the shortest path "
    "from i to j using only vertices {1..k} as intermediates.",
    "The subproblem is therefore 'shortest i&ndash;j path restricted to the "
    "first k intermediates', and each is solved from smaller ones — "
    "exactly the shape of a dynamic program.",
    "This also explains why k <b>must</b> be the outermost loop. Putting it "
    "inside gives a subtly wrong answer, and the reason is a dependency-order "
    "violation: the DP table would be read before the entries it depends on "
    "were written. Module 10 makes this general."]),

  ("h1", "6 &nbsp; Choosing"),
  ("table", ["Graph", "Algorithm", "Complexity", "Note"],
   [["Unweighted", "BFS", "O(V + E)", "Do not reach for Dijkstra here."],
    ["Non-negative weights", "Dijkstra", "O((V + E) log V)", "The default."],
    ["Any weights, no negative cycles", "Bellman&ndash;Ford", "O(VE)",
     "Also detects negative cycles."],
    ["DAG, any weights", "Topological relaxation", "O(V + E)",
     "Faster and simpler than Bellman&ndash;Ford. Check for acyclicity "
     "first."],
    ["Known target, good heuristic", "A*", "Varies",
     "Often an order of magnitude better than Dijkstra."],
    ["All pairs, dense", "Floyd&ndash;Warshall", "O(V&#179;)",
     "Three lines; handles negative edges."],
    ["All pairs, sparse, negative edges", "Johnson",
     "O(VE + V&#178; log V)",
     "Reweight with Bellman&ndash;Ford, then run Dijkstra from each vertex."]],
   [0.26, 0.21, 0.22, 0.31]),
 ],
 "resources": [
   ("MIT 6.006 — Dijkstra, Bellman-Ford, DAG shortest paths",
    "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
    "Three lectures covering this module, with the relaxation framing made "
    "explicit."),
   ("Jeff Erickson, Algorithms — Shortest Paths chapter",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "Presents all of them as one generic relaxation algorithm with different "
    "orderings. The best treatment of this framing anywhere."),
   ("Amit Patel — Introduction to A* (Red Blob Games)",
    "https://www.redblobgames.com/pathfinding/a-star/introduction.html",
    "Interactive, and the clearest explanation of admissibility and heuristic "
    "quality available. Directly useful for game work."),
   ("CSES Problem Set — Shortest Path section",
    "https://cses.fi/problemset/",
    "Auto-graded problems covering every algorithm here."),
 ],
 "exercises": [
   "Implement Dijkstra with lazy deletion. Verify on a graph where the "
   "fewest-edges path differs from the shortest-weight path, and confirm BFS "
   "gets it wrong.",
   "Construct a small graph with one negative edge where Dijkstra returns an "
   "incorrect distance. Trace the execution and identify the exact step where "
   "the correctness proof fails.",
   "Implement Bellman&ndash;Ford with negative-cycle detection. Build a "
   "currency-exchange graph with &minus;log rates and detect an arbitrage "
   "opportunity.",
   "Implement DAG shortest paths by topological relaxation. Verify it handles "
   "negative weights correctly and measure it against Bellman&ndash;Ford on "
   "the same DAG.",
   "Implement A* on a grid with obstacles. Compare the number of expanded "
   "vertices against Dijkstra for the same start and goal, with Euclidean and "
   "Manhattan heuristics.",
   "Make your A* heuristic inadmissible by scaling it up by 1.5&times;. Show "
   "it expands fewer nodes and sometimes returns a suboptimal path. Quantify "
   "the trade.",
   "Implement Floyd&ndash;Warshall. Then move the k loop innermost and find "
   "an input where the answer becomes wrong. Explain it as a dependency-order "
   "violation.",
 ],
 "selfcheck": [
   "What single operation underlies every algorithm in this module, and what "
   "distinguishes the algorithms?",
   "Why does BFS fail on weighted graphs, and what minimal change fixes it?",
   "Reproduce the step in Dijkstra's correctness proof that requires "
   "non-negative weights.",
   "Why exactly V&minus;1 rounds in Bellman&ndash;Ford? What does a V-th "
   "improving round mean?",
   "Why is the shortest path undefined in the presence of a reachable "
   "negative cycle?",
   "What makes an A* heuristic admissible, and what happens to the result if "
   "it is not?",
   "Why must k be the outermost loop in Floyd&ndash;Warshall?",
 ],
},

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Minimum Spanning Trees and Union-Find",
 "subtitle": "Two greedy algorithms that are both correct, and the structure "
             "that makes one of them fast.",
 "question": "Why do two different greedy strategies both find the optimum?",
 "outcomes": [
     "State and apply the cut property.",
     "Implement Kruskal and Prim and explain why both are correct.",
     "Implement union-find with path compression and union by rank.",
     "Explain the inverse Ackermann bound informally.",
     "Recognise the matroid structure that makes greedy work here.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The cut property",
   "blurb": "One lemma, and both algorithms follow."},

  {"t": "callout", "title": "The cut property", "kind": "The whole module",
   "body": ["Take any partition of the vertices into two non-empty sets "
            "— a <b>cut</b>.",
            "The <b>minimum-weight edge crossing that cut</b> is in some "
            "minimum spanning tree. (If weights are distinct, it is in "
            "<i>every</i> MST.)",
            "Proof: suppose an MST T omits that edge e. Adding e creates a "
            "cycle, which must cross the cut again at some edge f with "
            "w(f) ≥ w(e). Swap e for f: still spanning, still a tree, no "
            "heavier. So an MST containing e exists.",
            "Both Kruskal and Prim are just different ways of choosing which "
            "cut to apply this to."]},

  {"t": "two", "kicker": "Two strategies", "title": "Kruskal and Prim",
   "lh": "Kruskal — global",
   "l": ["Sort all edges by weight.",
         "Add each edge if it joins two different components.",
         "Grows a <b>forest</b> that merges into a tree.",
         "Needs union-find to test connectivity.",
         ("O(E log E) — dominated by the sort.", 1)],
   "rh": "Prim — local",
   "r": ["Start from one vertex.",
         "Repeatedly add the cheapest edge leaving the current tree.",
         "Grows a single <b>connected tree</b>.",
         "Needs a priority queue — it is Dijkstra's shape.",
         ("O(E log V) with a binary heap.", 1)],
   "note": "Prim is Dijkstra with the key being edge weight rather than path "
           "distance. Saying so makes it one less thing to learn."},

  {"t": "bullets", "kicker": "Correctness", "title": "Both are the cut property",
   "items": [
     "<b>Prim:</b> the cut is (tree so far) versus (everything else).",
     ("The cheapest crossing edge is exactly what Prim picks. Cut property "
      "applies directly.", 1),
     "",
     "<b>Kruskal:</b> when edge e is added, the cut is (e's component) versus "
     "(the rest).",
     ("Every cheaper edge was already examined and rejected, so e is the "
      "cheapest crossing edge.", 1),
     "",
     "Different cuts, same lemma. That is why two quite different greedy "
     "strategies land on the same answer.",
   ],
   "note": "This is the satisfying bit of the module. Make sure it lands."},

  {"t": "section", "label": "Part 2", "title": "Union-find",
   "blurb": "The data structure that makes Kruskal practical."},

  {"t": "code", "kicker": "Union-find", "title": "Two optimisations, enormous effect",
   "lang": "python", "code": """
class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])   # PATH COMPRESSION:
        return self.p[x]                       # flatten on the way back

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.rank[a] < self.rank[b]:        # UNION BY RANK:
            a, b = b, a                        # hang the shorter tree
        self.p[b] = a                          # off the taller one
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1
        return True
""",
   "caption": "Neither optimisation alone is enough. Together they give "
              "O(α(n)) amortised, where α is the inverse Ackermann "
              "function — at most 4 for any n you will ever see.",
   "note": "Worth noting the bound is amortised, which ties back to Module "
           "05. The analysis is genuinely hard; the informal version is "
           "enough here."},

  {"t": "bullets", "kicker": "Union-find", "title": "Why both optimisations are needed",
   "items": [
     "<b>Neither alone:</b> O(log n) per operation.",
     "<b>Union by rank alone:</b> O(log n) — trees stay shallow but "
     "never improve.",
     "<b>Path compression alone:</b> O(log n) amortised — good, but "
     "unions can still build tall trees.",
     "<b>Both:</b> O(α(n)) amortised.",
     "",
     "α is the inverse Ackermann function. α(n) ≤ 4 for "
     "n &lt; 2^65536.",
     ("Effectively constant, though provably not constant — a rare and "
      "pleasing distinction.", 1),
   ],
   "footnote": "Tarjan proved this bound is tight: no union-find structure "
               "can do better."},

  {"t": "section", "label": "Part 3", "title": "Why greedy works here",
   "blurb": "Matroids: the structure that licenses greed."},

  {"t": "callout", "title": "Greedy usually fails. Why not here?",
   "kind": "The deeper reason",
   "body": ["Greedy fails on most problems — it is wrong for shortest "
            "paths with negative edges, for knapsack, for set cover.",
            "It is correct for MST because the forests of a graph form a "
            "<b>matroid</b>: a system of 'independent' sets closed under "
            "subsets, with an exchange property.",
            "<b>Theorem (Rado–Edmonds):</b> the greedy algorithm finds "
            "the optimum for <i>every</i> weight function precisely when the "
            "structure is a matroid.",
            "So this is not luck. There is a structural property that "
            "licenses greed, and when it is absent — as in knapsack "
            "— greed fails."]},

  {"t": "table", "kicker": "Practice", "title": "Choosing, and what MSTs are for",
   "header": ["Situation", "Use", "Why"],
   "widths": [3.8, 3.2, 5.1],
   "rows": [
     ["Sparse graph", "Kruskal", "Sort dominates; E is small"],
     ["Dense graph", "Prim with array", "O(V²) beats O(E log E)"],
     ["Edges arrive sorted", "Kruskal", "Skip the sort entirely"],
     ["Need incremental growth", "Prim", "Tree is connected throughout"],
   ],
   "note": "Also worth stating what MSTs are used for: clustering, network "
           "design, mesh simplification, image segmentation, approximation "
           "algorithms (Module 13)."},

  {"t": "bullets", "kicker": "Uses", "title": "Where MSTs actually show up",
   "items": [
     "<b>Network design</b> — the original motivation: cheapest wiring "
     "connecting all nodes.",
     "<b>Clustering</b> — build the MST, delete the k−1 heaviest "
     "edges, and you have k clusters (single-linkage clustering).",
     "<b>Image segmentation</b> — pixels as vertices, colour difference "
     "as weight.",
     "<b>Approximation</b> — a metric TSP tour within 2× optimal "
     "comes straight from an MST (Module 13).",
     "<b>Maze generation</b> — a random-weight MST of a grid is a "
     "perfect maze.",
     "<b>Mesh processing</b> — feature detection and simplification "
     "orderings.",
   ]},
 ],
 "takeaways": [
   "The cut property: the lightest edge across any cut belongs to some MST. "
   "Both algorithms are this lemma applied to different cuts.",
   "Kruskal sorts globally and uses union-find; Prim grows locally and is "
   "Dijkstra with a different key.",
   "Union-find needs both path compression and union by rank; either alone "
   "leaves you at O(log n).",
   "α(n) ≤ 4 for any n you will ever encounter — effectively "
   "constant, provably not constant.",
   "Greedy is correct here because graph forests form a matroid, and the "
   "Rado–Edmonds theorem says matroids are exactly where greedy always "
   "works.",
   "MSTs are the basis of single-linkage clustering, maze generation, and the "
   "2-approximation for metric TSP.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The problem"),
  ("p", "Given a connected, undirected, weighted graph, find a spanning tree "
        "— a subset of edges connecting all vertices with no cycles "
        "— of minimum total weight. A spanning tree always has exactly "
        "V&minus;1 edges."),
  ("p", "There may be exponentially many spanning trees, so enumeration is "
        "hopeless. Two different greedy algorithms both find the optimum, "
        "which is unusual enough to deserve an explanation."),

  ("h1", "2 &nbsp; The cut property"),
  ("callout", "Statement",
   ["Let (S, V&minus;S) be any partition of the vertices into two non-empty "
    "sets — a <b>cut</b>. Let e be a minimum-weight edge with one "
    "endpoint in each part.",
    "Then e belongs to some minimum spanning tree. If all edge weights are "
    "distinct, e belongs to <i>every</i> minimum spanning tree."]),
  ("p", "<b>Proof.</b> Let T be an MST not containing e. Adding e to T "
        "creates exactly one cycle. That cycle starts in S and ends in S "
        "while passing through V&minus;S, so it crosses the cut an even "
        "number of times — in particular, at least once besides e. Call "
        "such another crossing edge f."),
  ("p", "Since e is a minimum-weight edge across the cut, w(e) &le; w(f). "
        "Form T&prime; = T &minus; {f} + {e}. Removing f breaks the cycle, so "
        "T&prime; is acyclic; it still has V&minus;1 edges and still connects "
        "everything, so it is a spanning tree. Its weight is w(T) &minus; "
        "w(f) + w(e) &le; w(T). Since T was minimum, T&prime; is minimum too, "
        "and it contains e. &#9633;"),
  ("p", "This exchange argument — take a hypothetical optimum, swap one "
        "element for your greedy choice, show it does not get worse — is "
        "the standard proof technique for greedy correctness, and Module 09 "
        "generalises it."),

  ("h1", "3 &nbsp; Two algorithms, one lemma"),
  ("h2", "3.1 &nbsp; Kruskal"),
  ("code", """def kruskal(V, edges):
    edges.sort(key=lambda e: e[2])        # by weight
    dsu = DSU(len(V))
    mst = []
    for (u, v, w) in edges:
        if dsu.union(u, v):               # different components?
            mst.append((u, v, w))
    return mst"""),
  ("p", "Sort all edges and add each one that connects two currently separate "
        "components. The structure grows as a forest that gradually merges "
        "into a single tree. O(E log E) for the sort, plus near-linear work "
        "for the union-find operations — so the sort dominates."),
  ("p", "<b>Why the cut property applies:</b> when Kruskal adds edge e, "
        "consider the cut separating the component containing one endpoint of "
        "e from everything else. Every edge cheaper than e has already been "
        "examined, and any that crossed this cut would have merged the two "
        "sides. So e is a minimum-weight edge across that cut."),
  ("h2", "3.2 &nbsp; Prim"),
  ("p", "Start from an arbitrary vertex and repeatedly add the cheapest edge "
        "connecting the tree built so far to a vertex outside it. The "
        "structure is connected at every step."),
  ("p", "The implementation is Dijkstra's with one change: the priority queue "
        "key is the weight of the connecting edge rather than the accumulated "
        "path distance. Noticing this saves learning a second algorithm."),
  ("p", "<b>Why the cut property applies:</b> the cut is (vertices in the "
        "tree) versus (vertices outside), and Prim picks precisely the "
        "minimum-weight edge crossing it."),
  ("callout", "Different cuts, the same lemma",
   ["Prim always applies the cut property to the cut between its growing tree "
    "and the rest of the graph. Kruskal applies it to whichever cut separates "
    "the component it is currently merging.",
    "Two quite different-looking strategies turn out to be the same argument "
    "deployed differently, which is why both reach the optimum."]),

  ("break",),
  ("h1", "4 &nbsp; Union-find"),
  ("p", "Kruskal needs to answer 'are u and v already connected?' and 'merge "
        "these two components' many times. A <b>disjoint set union</b> "
        "structure does both in effectively constant amortised time."),
  ("code", """class DSU:
    def __init__(self, n):
        self.p = list(range(n))       # parent pointers
        self.rank = [0] * n           # upper bound on tree height

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])   # path compression
        return self.p[x]

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.rank[a] < self.rank[b]:        # union by rank
            a, b = b, a
        self.p[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1
        return True"""),
  ("h2", "4.1 &nbsp; The two optimisations"),
  ("ul", ["<b>Union by rank.</b> When merging, hang the shallower tree under "
          "the deeper one. This keeps heights at O(log n) rather than letting "
          "a bad sequence of unions build a path.",
          "<b>Path compression.</b> During <code>find</code>, repoint every "
          "node on the path directly at the root. Each traversal flattens the "
          "structure it walked, so future queries are cheaper."]),
  ("table", ["Optimisations", "Per operation"],
   [["Neither", "O(log n), and O(n) in the worst case without rank"],
    ["Union by rank only", "O(log n)"],
    ["Path compression only", "O(log n) amortised"],
    ["Both", "O(&alpha;(n)) amortised"]],
   [0.45, 0.55]),
  ("callout", "The inverse Ackermann function",
   ["&alpha;(n) is the inverse of a function that grows so fast it is hard to "
    "describe. In the other direction, &alpha; grows so slowly that "
    "&alpha;(n) &le; 4 for every n less than 2<super>65536</super> — "
    "vastly more than the number of atoms in the observable universe.",
    "So union-find is constant time for every input that will ever exist, "
    "while being provably not constant time. That distinction is a small "
    "delight and a good reminder that asymptotic statements are about limits, "
    "not about your data.",
    "Tarjan also proved the bound is <i>tight</i>: no union-find "
    "implementation can achieve O(1) worst-case amortised. This is one of the "
    "few data structures with a matching lower bound."]),

  ("h1", "5 &nbsp; Why greedy works here"),
  ("p", "Greedy algorithms usually fail. They are wrong for shortest paths "
        "with negative edges, wrong for 0/1 knapsack, wrong for set cover. "
        "Their success on MST is not luck, and there is a precise "
        "characterisation of when greed is safe."),
  ("p", "A <b>matroid</b> is a ground set E with a family of 'independent' "
        "subsets satisfying two conditions: every subset of an independent "
        "set is independent, and if A and B are independent with |A| &lt; "
        "|B|, then some element of B can be added to A keeping it independent "
        "(the <i>exchange property</i>)."),
  ("p", "The acyclic edge subsets of a graph — its forests — form a "
        "matroid, the graphic matroid."),
  ("callout", "Rado&ndash;Edmonds",
   ["The greedy algorithm finds an optimal solution for <b>every</b> weight "
    "function precisely when the underlying structure is a matroid.",
    "This is a genuine characterisation, not merely a sufficient condition. "
    "So 'is this a matroid?' is the right question to ask when wondering "
    "whether a greedy approach can be made correct — and when the answer "
    "is no, as for knapsack, no amount of cleverness in the greedy rule will "
    "fix it.",
    "That is the moment to reach for dynamic programming (Module 10) or "
    "approximation (Module 13)."]),

  ("h1", "6 &nbsp; In practice"),
  ("table", ["Situation", "Choice", "Reason"],
   [["Sparse graph (E = O(V))", "Kruskal",
     "The sort dominates and E is small."],
    ["Dense graph (E &asymp; V&#178;)", "Prim with an array",
     "O(V&#178;) without heap overhead beats O(E log E)."],
    ["Edges already sorted, or integer weights", "Kruskal",
     "Skip or linearise the sort; the rest is near-linear."],
    ["Need a connected structure at every step", "Prim",
     "Kruskal's intermediate state is a forest, not a tree."]],
   [0.30, 0.22, 0.48]),
  ("h2", "6.1 &nbsp; What MSTs are actually used for"),
  ("ul", ["<b>Single-linkage clustering.</b> Build the MST and delete the "
          "k&minus;1 heaviest edges: the remaining components are exactly the "
          "k clusters. This equivalence is why MST algorithms appear in "
          "clustering libraries.",
          "<b>Image segmentation.</b> Pixels as vertices, colour difference "
          "as edge weight; the MST structure reveals region boundaries.",
          "<b>Metric TSP approximation.</b> A depth-first walk of the MST "
          "visits every vertex and costs at most twice the optimal tour, "
          "giving a 2-approximation immediately (Module 13).",
          "<b>Maze generation.</b> Assign random weights to a grid's edges "
          "and take the MST: the result is a perfect maze with exactly one "
          "path between any two cells.",
          "<b>Network design.</b> The original motivation — the cheapest "
          "set of links connecting all sites."]),
 ],
 "resources": [
   ("MIT 6.046J — Greedy Algorithms, Minimum Spanning Trees",
    "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
    "The cut property proved carefully, with both algorithms derived from "
    "it."),
   ("Jeff Erickson, Algorithms — Minimum Spanning Trees chapter",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "Presents Kruskal, Prim, and Borůvka as one generic algorithm. "
    "Worth reading for that unification alone."),
   ("MIT 6.006 — Union-Find / Disjoint Sets",
    "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
    "The data structure with the amortised analysis at an accessible level."),
   ("CSES Problem Set — Graph section (Road Reparation, Road "
    "Construction)",
    "https://cses.fi/problemset/",
    "Direct practice on MST and union-find."),
 ],
 "exercises": [
   "Implement union-find four ways: neither optimisation, rank only, "
   "compression only, and both. Measure all four on 10&#8310; union and find "
   "operations and plot the results.",
   "Implement Kruskal and Prim. Verify they produce the same total weight on "
   "100 random graphs, and find a graph with equal weights where the two "
   "trees differ structurally.",
   "Prove the cut property in your own words, then construct a graph with "
   "duplicate edge weights where the MST is genuinely not unique.",
   "Implement single-linkage clustering by building an MST and removing the "
   "k&minus;1 heaviest edges. Test it on 2D point data and plot the clusters.",
   "Generate a maze by assigning random weights to a grid graph and taking "
   "the MST. Verify there is exactly one path between any two cells.",
   "Measure Kruskal against Prim on a sparse graph (E = 2V) and a dense one "
   "(E = V&#178;/2). Confirm the predicted crossover.",
 ],
 "selfcheck": [
   "State the cut property and prove it with an exchange argument.",
   "Show how the cut property applies to Prim and to Kruskal, naming the cut "
   "in each case.",
   "Why is Prim essentially Dijkstra? What exactly differs?",
   "Why does union-find need both path compression and union by rank?",
   "What is &alpha;(n) and in what sense is union-find constant time but not "
   "constant time?",
   "What is a matroid, and what does the Rado&ndash;Edmonds theorem tell you "
   "about when greedy algorithms work?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Greedy Algorithms and Exchange Arguments",
 "subtitle": "When taking the best option now is provably right, and how to "
             "tell.",
 "question": "How do you know a greedy algorithm is correct rather than "
             "merely plausible?",
 "outcomes": [
     "Identify the greedy choice property and optimal substructure.",
     "Prove greedy correctness by exchange argument.",
     "Prove greedy correctness by 'greedy stays ahead'.",
     "Recognise standard problems where greed fails, and why.",
     "Construct counterexamples to refute a proposed greedy rule.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The two requirements",
   "blurb": "Greedy works when, and only when, both hold."},

  {"t": "bullets", "kicker": "Requirements", "title": "What a greedy algorithm needs",
   "items": [
     "<b>1. Greedy choice property.</b> A locally optimal choice is part of "
     "<i>some</i> global optimum.",
     ("This is the hard one, and it is what the proofs establish.", 1),
     "",
     "<b>2. Optimal substructure.</b> After making that choice, the "
     "remaining problem is the same problem, smaller.",
     ("Shared with dynamic programming — Module 10.", 1),
     "",
     "The difference from DP: greedy commits immediately and never "
     "reconsiders. DP explores all choices.",
     ("Greedy is faster when it is correct, and silently wrong when it is "
      "not.", 1),
   ],
   "note": "Frame greedy and DP as a spectrum from the start: greedy is DP "
           "where you can prove you only need one branch."},

  {"t": "callout", "title": "A greedy algorithm that passes your tests is worth nothing",
   "kind": "The discipline",
   "body": ["Greedy rules are easy to invent and plausible-sounding greedy "
            "rules are usually wrong.",
            "The failure mode is specific and nasty: it works on every small "
            "case you try, then fails on a structured input in production.",
            "So a greedy algorithm without a proof is a conjecture. Either "
            "produce an exchange argument, or produce a counterexample. There "
            "is no third state in which 'it seems to work' is acceptable."]},

  {"t": "section", "label": "Part 2", "title": "Two proof techniques",
   "blurb": "Exchange, and staying ahead."},

  {"t": "bullets", "kicker": "Technique 1", "title": "Exchange argument",
   "items": [
     "Take an arbitrary optimal solution OPT.",
     "Show you can transform OPT into one agreeing with the first greedy "
     "choice, <b>without making it worse</b>.",
     "Repeat, or induct, to show the greedy solution is itself optimal.",
     "",
     "The move is always the same: find where OPT and greedy first disagree, "
     "swap OPT's choice for greedy's, argue the swap does not hurt.",
     "",
     "The cut property of Module 08 was exactly this.",
   ],
   "note": "Students find exchange arguments mysterious until they see that "
           "it is always the same three steps."},

  {"t": "code", "kicker": "Worked", "title": "Interval scheduling: earliest finish first",
   "lang": "text", "code": """
PROBLEM  Choose the most non-overlapping intervals from a set.

RULE     Repeatedly take the interval that FINISHES EARLIEST
         among those compatible with what you have chosen.

PROOF (exchange)
  Let OPT be any optimal solution, greedy = g1, g2, ...
  Let OPT = o1, o2, ... sorted by finish time.

  Suppose they first differ at position k.
  By the greedy rule, g_k finishes no later than o_k
    (greedy picked the earliest-finishing compatible interval,
     and o_k was available to it).

  So replace o_k with g_k in OPT.
    - g_k is compatible with o_1..o_{k-1}: greedy chose it after
      the same prefix.
    - g_k finishes <= o_k, so it cannot conflict with o_{k+1}...

  The result is still optimal and agrees with greedy one step further.
  Induct: greedy is optimal.
""",
   "caption": "Note what carries the argument: finishing earliest leaves the "
              "most room for everything after. Any other rule — shortest "
              "first, fewest conflicts first — fails.",
   "note": "Have them try to break 'shortest first' before showing the "
           "correct rule. The counterexample is small and memorable."},

  {"t": "bullets", "kicker": "Technique 2", "title": "Greedy stays ahead",
   "items": [
     "Define a measure of partial progress.",
     "Show that after each step, greedy's measure is at least as good as any "
     "other solution's at the same step.",
     "Conclude greedy's final result is at least as good.",
     "",
     "Often more natural than exchange when there is an obvious running "
     "quantity — time elapsed, intervals covered, distance remaining.",
     "",
     "For interval scheduling: greedy's k-th interval finishes no later than "
     "any solution's k-th. Same conclusion, different route.",
   ]},

  {"t": "section", "label": "Part 3", "title": "Where greed fails",
   "blurb": "And how to show it quickly."},

  {"t": "table", "kicker": "Failures", "title": "Classic greedy failures",
   "header": ["Problem", "Tempting rule", "Why it fails"],
   "widths": [3.0, 3.8, 5.3],
   "rows": [
     ["0/1 knapsack", "Best value-to-weight ratio first",
      "Taking the best ratio can block two items that together beat it"],
     ["Shortest path, neg. edges", "Nearest unvisited first",
      "A negative edge later makes a longer prefix better"],
     ["Set cover", "Largest uncovered set first",
      "Works, but only to within ln n — not optimal"],
     ["Coin change", "Largest coin first",
      "Correct for some coin systems, wrong for {1, 3, 4}: 6 = 3+3, not 4+1+1"],
     ["Graph colouring", "Colour greedily by degree",
      "Order-dependent; can use arbitrarily many more colours than needed"],
   ],
   "note": "The coin change row is especially good: greedy IS correct for US "
           "and Euro coins, which is why the failure is so easy to miss."},

  {"t": "callout", "title": "Fractional knapsack is greedy; 0/1 is not",
   "kind": "The instructive pair",
   "body": ["<b>Fractional</b> — you may take part of an item. Sort by "
            "value/weight and fill greedily. <b>Provably optimal</b>, by a "
            "clean exchange argument.",
            "<b>0/1</b> — each item is all or nothing. The same rule "
            "fails, and the problem is NP-hard.",
            "The difference is that fractional knapsack has a matroid-like "
            "exchange structure and 0/1 does not: you cannot always swap a "
            "little of one item for a little of another.",
            "A one-word change to the problem statement moves it from "
            "polynomial-greedy to NP-hard. This is worth remembering when "
            "someone says a problem is 'basically the same'."]},

  {"t": "bullets", "kicker": "Method", "title": "How to attack a candidate greedy rule",
   "items": [
     "<b>1. Try to break it first.</b> Spend ten minutes hunting a "
     "counterexample before trying to prove it.",
     ("Small cases, extreme values, ties, items that are nearly equal.", 1),
     "",
     "<b>2. If you cannot break it,</b> attempt an exchange argument.",
     ("Where would greedy and OPT first disagree? Can you swap?", 1),
     "",
     "<b>3. If the exchange fails,</b> the failure usually shows you the "
     "counterexample.",
     "",
     "<b>4. If greed genuinely fails,</b> go to dynamic programming "
     "(Module 10) or approximation (Module 13).",
   ],
   "footnote": "Trying to break it first is the efficient order — "
               "counterexamples are quick, proofs are slow."},

  {"t": "table", "kicker": "Summary", "title": "Greedy algorithms worth knowing",
   "header": ["Problem", "Greedy rule", "Proof"],
   "widths": [4.2, 4.3, 3.6],
   "rows": [
     ["Interval scheduling", "Earliest finish time", "Exchange"],
     ["Interval partitioning", "Sort by start; reuse a free room", "Stays ahead"],
     ["Fractional knapsack", "Best value/weight ratio", "Exchange"],
     ["Huffman coding", "Merge two least frequent", "Exchange"],
     ["MST (Kruskal, Prim)", "Lightest safe edge", "Cut property"],
     ["Dijkstra", "Closest unfinished vertex", "Exchange"],
   ],
   "note": "Note that Dijkstra and MST are on this list: they were greedy "
           "algorithms all along, and now the students have the vocabulary."},
 ],
 "takeaways": [
   "Greedy needs two properties: the greedy choice property and optimal "
   "substructure. The first is what you must prove.",
   "A greedy algorithm without a proof is a conjecture. It will pass your "
   "tests and fail in production.",
   "Exchange argument: take an optimum, swap its first disagreement for "
   "greedy's choice, show it does not get worse, induct.",
   "Greedy stays ahead: define a progress measure and show greedy leads at "
   "every step.",
   "Try to break a greedy rule before trying to prove it. Counterexamples are "
   "fast; proofs are slow.",
   "Fractional knapsack is greedy and 0/1 knapsack is NP-hard. A one-word "
   "change in the statement can move a problem across that line.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What greedy means"),
  ("p", "A greedy algorithm builds a solution incrementally, at each step "
        "taking whatever looks best right now and never reconsidering. It is "
        "the simplest possible strategy, it is usually fast, and it is "
        "usually wrong — which is exactly why the proof matters more "
        "here than almost anywhere else in the course."),
  ("h2", "1.1 &nbsp; The two requirements"),
  ("ul", ["<b>Greedy choice property.</b> There is an optimal solution "
          "containing the greedy first choice. This is the non-trivial "
          "condition and the one the proof techniques of &sect;2 establish.",
          "<b>Optimal substructure.</b> After committing to the greedy "
          "choice, what remains is an instance of the same problem, and an "
          "optimal solution to the whole contains an optimal solution to the "
          "remainder."]),
  ("p", "Optimal substructure is shared with dynamic programming. The "
        "difference is what you do with it: dynamic programming considers "
        "every choice at each step and keeps the best; greedy commits to one "
        "and never looks back. Greedy is therefore dramatically faster when "
        "the greedy choice property holds, and silently incorrect when it "
        "does not."),
  ("callout", "The discipline this module is really about",
   ["Plausible greedy rules are easy to invent and usually wrong, and their "
    "failure mode is unkind: they work on every small example you try by "
    "hand, then fail on a structured input months later.",
    "So treat an unproved greedy algorithm as a <b>conjecture</b>. Either "
    "produce an exchange argument or produce a counterexample. 'It seems to "
    "work on my tests' is not one of the available states."]),

  ("h1", "2 &nbsp; Proof technique 1: exchange arguments"),
  ("p", "The structure is always the same three steps:"),
  ("ol", ["Let OPT be an arbitrary optimal solution.",
          "Find the first place where OPT disagrees with the greedy solution, "
          "and exchange OPT's choice there for greedy's. Argue the result is "
          "still feasible and no worse.",
          "Conclude by induction that the greedy solution is itself "
          "optimal."]),
  ("p", "The cut property of Module 08 was an exchange argument: given an MST "
        "omitting the lightest edge across a cut, we swapped that edge in and "
        "a heavier one out, and showed the result was still a spanning tree "
        "of no greater weight."),
  ("h2", "2.1 &nbsp; Worked example: interval scheduling"),
  ("p", "Given intervals with start and finish times, select as many "
        "mutually non-overlapping intervals as possible."),
  ("p", "<b>Rule:</b> repeatedly take the compatible interval that finishes "
        "earliest."),
  ("p", "<b>Proof.</b> Let greedy produce g&#8321;, g&#8322;, &hellip; and let "
        "OPT be an optimal solution o&#8321;, o&#8322;, &hellip;, both sorted "
        "by finish time. Suppose they first differ at index k. Greedy chose "
        "g&#8342; as the earliest-finishing interval compatible with "
        "g&#8321;&hellip;g&#8342;&#8331;&#8321;, which equal "
        "o&#8321;&hellip;o&#8342;&#8331;&#8321;. Since o&#8342; was also "
        "compatible with that prefix, greedy had it available, so "
        "finish(g&#8342;) &le; finish(o&#8342;)."),
  ("p", "Replace o&#8342; with g&#8342; in OPT. It is compatible with the "
        "prefix by construction, and since it finishes no later than "
        "o&#8342;, it cannot conflict with o&#8342;&#8330;&#8321; or anything "
        "after. The modified solution has the same size, so it is still "
        "optimal, and it agrees with greedy one step further. Induction "
        "completes the argument. &#9633;"),
  ("callout", "Why <i>earliest finish</i> and not something else",
   ["Finishing earliest leaves the maximum possible room for everything that "
    "follows. That is the entire intuition, and it is what the exchange step "
    "formalises.",
    "Other plausible rules fail, and quickly: <b>shortest interval first</b> "
    "fails on one short interval that overlaps two long non-overlapping ones. "
    "<b>Earliest start first</b> fails on a single long interval that starts "
    "first and blocks everything. <b>Fewest conflicts first</b> fails too, "
    "though the counterexample is larger.",
    "Three plausible rules, all wrong. This is the normal situation."]),

  ("h1", "3 &nbsp; Proof technique 2: greedy stays ahead"),
  ("p", "Define a measure of partial progress, then show that after each step "
        "greedy's measure is at least as good as that of any other solution "
        "after the same number of steps. If greedy leads throughout, its "
        "final answer cannot be worse."),
  ("p", "For interval scheduling the measure is the finish time of the k-th "
        "selected interval: greedy's k-th always finishes no later than any "
        "other solution's k-th, so greedy can never run out of room first. "
        "Same conclusion as the exchange argument by a different route."),
  ("p", "Which technique to use is largely taste. Exchange arguments are more "
        "general; stays-ahead is often more natural when the problem has an "
        "obvious running quantity — elapsed time, remaining capacity, "
        "coverage so far."),

  ("break",),
  ("h1", "4 &nbsp; Where greed fails"),
  ("table", ["Problem", "Plausible rule", "Why it fails"],
   [["<b>0/1 knapsack</b>", "Highest value-to-weight ratio first",
     "The best-ratio item can occupy space that two slightly worse items "
     "would have used to greater total value. NP-hard."],
    ["<b>Shortest path with negative edges</b>",
     "Closest unfinished vertex first",
     "Dijkstra's exchange argument needs prefix &le; whole path, which "
     "negative edges break (Module 07)."],
    ["<b>Set cover</b>", "Set covering the most uncovered elements",
     "Greedy is not optimal, but it is an H&#8345; &asymp; ln n "
     "approximation — and that is provably the best possible unless "
     "P = NP (Module 13)."],
    ["<b>Coin change</b>", "Largest coin that fits",
     "Correct for US and Euro denominations, wrong in general. With coins "
     "{1, 3, 4}, greedy makes 6 as 4+1+1 (three coins) instead of 3+3 (two)."],
    ["<b>Graph colouring</b>", "Colour vertices greedily in some order",
     "Highly order-dependent. For some graphs and orderings greedy uses "
     "arbitrarily more colours than necessary."]],
   [0.22, 0.26, 0.52]),
  ("callout", "The coin change case is the cautionary one",
   ["Greedy coin change <i>is</i> optimal for the US and Euro systems, which "
    "are the ones everyone tests with. The algorithm therefore looks correct "
    "to anyone who does not try a pathological denomination set.",
    "This is precisely the failure mode described in &sect;1: works on every "
    "case you naturally try, wrong in general. The general problem needs "
    "dynamic programming (Module 10)."]),
  ("h2", "4.1 &nbsp; Fractional versus 0/1 knapsack"),
  ("p", "<b>Fractional knapsack</b>: items may be divided. Sort by "
        "value/weight ratio and fill the sack greedily, taking a fraction of "
        "the last item. This is optimal, by a straightforward exchange "
        "argument — if an optimal solution contains any of a lower-ratio "
        "item while a higher-ratio item remains available, swap a small "
        "amount and the value strictly increases."),
  ("p", "<b>0/1 knapsack</b>: items are indivisible. The same rule fails, and "
        "the problem is NP-hard (Module 12)."),
  ("p", "The structural difference is that the exchange step requires being "
        "able to swap an arbitrarily small amount. With indivisible items "
        "that move is unavailable, and the exchange argument — and with "
        "it the greedy choice property — collapses. One word in the "
        "problem statement moves it from polynomial to NP-hard, which is "
        "worth remembering the next time someone describes two problems as "
        "'basically the same'."),

  ("h1", "5 &nbsp; A method for attacking greedy rules"),
  ("ol", ["<b>Try to break it first.</b> Spend ten minutes looking for a "
          "counterexample before spending an hour on a proof. Probe small "
          "cases, extreme values, ties, and items that are nearly "
          "indistinguishable. Counterexamples are cheap and proofs are "
          "expensive, so search in that order.",
          "<b>If it survives, attempt an exchange argument.</b> Ask where "
          "greedy and a hypothetical optimum could first disagree, and "
          "whether you can swap without loss.",
          "<b>If the exchange fails, look at why.</b> The step that will not "
          "go through almost always points directly at the counterexample.",
          "<b>If greed genuinely fails, change technique.</b> Dynamic "
          "programming if the problem has overlapping subproblems (Module 10); "
          "approximation if it is NP-hard (Module 13)."]),

  ("h1", "6 &nbsp; The greedy algorithms worth knowing"),
  ("table", ["Problem", "Rule", "Proof technique"],
   [["Interval scheduling", "Earliest finish time", "Exchange"],
    ["Interval partitioning", "Sort by start; assign to any free resource",
     "Stays ahead (the answer equals the maximum overlap depth)"],
    ["Fractional knapsack", "Highest value/weight ratio", "Exchange"],
    ["Huffman coding", "Repeatedly merge the two least frequent symbols",
     "Exchange"],
    ["Minimum spanning tree", "Lightest edge that is safe",
     "Cut property (Module 08)"],
    ["Dijkstra", "Closest unfinished vertex",
     "Exchange (Module 07)"],
    ["Job sequencing with deadlines", "Highest profit first, scheduled as "
     "late as possible", "Exchange / matroid"]],
   [0.28, 0.40, 0.32]),
  ("p", "Note that Dijkstra and the MST algorithms appear here. They were "
        "greedy algorithms when you met them; this module supplies the "
        "vocabulary and the proof technique that were implicit at the time."),
 ],
 "resources": [
   ("MIT 6.046J — Greedy Algorithms",
    "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
    "Interval scheduling and the exchange argument, done carefully."),
   ("Jeff Erickson, Algorithms — Greedy Algorithms chapter",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "Unusually good on how to <i>find</i> the right greedy rule and on the "
    "discipline of trying to break it first. Includes several instructive "
    "wrong rules."),
   ("Tim Roughgarden — Greedy Algorithms (Part 3)",
    "https://www.algorithmsilluminated.org/",
    "Huffman coding and scheduling, with the proofs spelled out at length."),
   ("CSES Problem Set — Sorting and Searching section",
    "https://cses.fi/problemset/",
    "Many of these are greedy problems in disguise. Good practice at "
    "recognition."),
 ],
 "exercises": [
   "Implement interval scheduling with four rules: earliest finish, earliest "
   "start, shortest duration, fewest conflicts. Find a counterexample for each "
   "of the three incorrect ones.",
   "Write out the exchange argument for fractional knapsack in full, then "
   "construct a 0/1 instance where the same rule is suboptimal and explain "
   "which step of the proof fails.",
   "Implement greedy coin change. Verify it is optimal for US denominations, "
   "then find three coin systems where it is not. Write a brute-force checker "
   "to search for such systems automatically.",
   "Implement Huffman coding and prove the greedy choice property: the two "
   "least frequent symbols are siblings at maximum depth in some optimal "
   "tree.",
   "Implement interval partitioning (assign lectures to the fewest rooms). "
   "Prove by a stays-ahead argument that the number of rooms used equals the "
   "maximum number of overlapping intervals.",
   "Take a greedy rule you believe is correct for some problem of your own, "
   "and spend ten minutes trying to break it before attempting a proof. "
   "Report which you found.",
 ],
 "selfcheck": [
   "What two properties must hold for a greedy algorithm to be correct, and "
   "which one is the hard one?",
   "What distinguishes greedy from dynamic programming, given that both need "
   "optimal substructure?",
   "Describe the three steps of an exchange argument.",
   "Why is 'earliest finish time' the correct rule for interval scheduling, "
   "and why does 'shortest interval' fail?",
   "Give the structural reason fractional knapsack is greedy-solvable while "
   "0/1 knapsack is NP-hard.",
   "Why should you try to break a greedy rule before trying to prove it?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Dynamic Programming",
 "subtitle": "What to do when the subproblems overlap.",
 "question": "How do you avoid recomputing the same subproblem exponentially "
             "often?",
 "outcomes": [
     "Recognise overlapping subproblems and optimal substructure.",
     "Design a DP by defining the subproblem, recurrence, and base cases.",
     "Convert between memoised recursion and bottom-up tabulation.",
     "Analyse DP complexity as states × transitions.",
     "Reduce space when only recent rows are needed.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The signal",
   "blurb": "Overlapping subproblems — the thing divide and conquer "
            "cannot handle."},

  {"t": "code", "kicker": "The problem", "title": "Why naive recursion explodes",
   "lang": "text", "code": """
fib(5)
+- fib(4)
|  +- fib(3)
|  |  +- fib(2)  <-- computed here
|  |  +- fib(1)
|  +- fib(2)     <-- and again
+- fib(3)        <-- and the whole subtree again
   +- fib(2)     <-- and again
   +- fib(1)

fib(n) makes ~phi^n calls to compute n+1 distinct values.

The subproblems OVERLAP. Divide and conquer assumes they do not.
""",
   "caption": "Only n+1 distinct subproblems exist. Computing each once turns "
              "exponential into linear. That is the entire idea of dynamic "
              "programming.",
   "note": "Fibonacci is a toy, but it shows the mechanism with nothing else "
           "in the way. Spend the time."},

  {"t": "two", "kicker": "When", "title": "Divide and conquer, or dynamic programming",
   "lh": "Divide and conquer",
   "l": ["Subproblems are <b>independent</b>.",
         "Each arises once.",
         "Mergesort: the two halves never overlap.",
         ("Recursion is efficient as written.", 1)],
   "rh": "Dynamic programming",
   "r": ["Subproblems <b>overlap</b>.",
         "The same subproblem recurs many times.",
         "Fibonacci, edit distance, knapsack.",
         ("Store each answer; compute each once.", 1)],
   "note": "This slide answers the question students actually have: how do I "
           "know which technique to use?"},

  {"t": "callout", "title": "The two requirements", "kind": "Key idea",
   "body": ["<b>Optimal substructure</b> — an optimal solution contains "
            "optimal solutions to subproblems. (Shared with greedy.)",
            "<b>Overlapping subproblems</b> — the same subproblem is "
            "needed many times. (This is what distinguishes DP from divide "
            "and conquer.)",
            "Given both, dynamic programming is 'recursion plus a table'. "
            "That is genuinely all it is, and the mystique around it is "
            "unearned."]},

  {"t": "section", "label": "Part 2", "title": "The design method",
   "blurb": "Four questions, in order. Answer them and the code writes "
            "itself."},

  {"t": "bullets", "kicker": "Method", "title": "Four questions",
   "items": [
     "<b>1. What is the subproblem?</b> Define it in words first, precisely.",
     ("'dp[i][w] = the best value using the first i items with capacity w'", 1),
     ("Getting this wrong is the cause of nearly every stuck DP.", 1),
     "",
     "<b>2. What is the recurrence?</b> How does a subproblem use smaller "
     "ones?",
     "",
     "<b>3. What are the base cases?</b> The smallest subproblems, answered "
     "directly.",
     "",
     "<b>4. In what order?</b> Dependencies must be computed first.",
   ],
   "footnote": "Nearly every DP difficulty is a question-1 difficulty.",
   "note": "Insist they write the subproblem definition in English before "
           "touching code. It is the single highest-leverage habit here."},

  {"t": "eq", "kicker": "Complexity", "title": "States times transitions",
   "eqs": [
     ("time  =  (number of states) × (work per state)",
      "The whole complexity analysis of a DP, in one line."),
     ("knapsack:  O(nW) states × O(1)  =  O(nW)",
      "Pseudo-polynomial — W is a <i>value</i>, not an input length."),
     ("edit distance:  O(mn) states × O(1)  =  O(mn)",
      "Genuinely polynomial in the input size."),
   ],
   "caption": "Count the table entries, multiply by the work to fill one. "
              "Nothing more is required.",
   "note": "The pseudo-polynomial distinction matters for Module 12 and is "
           "worth planting now."},

  {"t": "section", "label": "Part 3", "title": "Top-down and bottom-up",
   "blurb": "The same computation, two implementations."},

  {"t": "code", "kicker": "Both forms", "title": "Memoisation and tabulation",
   "lang": "python", "code": """
# TOP-DOWN (memoised recursion) -- write the recurrence, add a cache
from functools import lru_cache

@lru_cache(maxsize=None)
def lcs(i, j):
    if i == 0 or j == 0:              return 0
    if a[i-1] == b[j-1]:              return 1 + lcs(i-1, j-1)
    return max(lcs(i-1, j), lcs(i, j-1))

# BOTTOM-UP (tabulation) -- fill the table in dependency order
def lcs_table(a, b):
    dp = [[0] * (len(b)+1) for _ in range(len(a)+1)]
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            dp[i][j] = (dp[i-1][j-1] + 1 if a[i-1] == b[j-1]
                        else max(dp[i-1][j], dp[i][j-1]))
    return dp[-1][-1]
""",
   "caption": "Top-down is easier to write and only computes reachable "
              "states. Bottom-up has no recursion overhead and allows space "
              "optimisation.",
   "note": "Recommend writing top-down first, always. Convert only if you "
           "need the space saving or the constant factor."},

  {"t": "table", "kicker": "Compare", "title": "Which form to write",
   "header": ["", "Top-down (memo)", "Bottom-up (table)"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Ease of writing", "<b>Easier</b> — it is the recurrence", "Must work out the order"],
     ["States computed", "<b>Only reachable ones</b>", "All of them"],
     ["Overhead", "Call stack, hashing", "<b>None</b>"],
     ["Space reduction", "Awkward", "<b>Natural</b> — keep few rows"],
     ["Deep recursion", "May overflow", "<b>No risk</b>"],
   ]},

  {"t": "code", "kicker": "Optimisation", "title": "Space reduction when only recent rows matter",
   "lang": "python", "code": """
# 0/1 knapsack: dp[i][w] depends only on row i-1.
# So keep ONE row -- and iterate w DOWNWARD.

def knapsack(items, W):
    dp = [0] * (W + 1)
    for value, weight in items:
        for w in range(W, weight - 1, -1):     # DOWNWARD is essential
            dp[w] = max(dp[w], dp[w - weight] + value)
    return dp[W]

# Going upward would read dp[w - weight] AFTER it was updated for this
# same item -- allowing the item to be used twice. That silently solves
# the UNBOUNDED knapsack problem instead. (Which is how you solve that
# one: use the same loop, upward.)
""",
   "caption": "O(nW) time, O(W) space. The loop direction is the difference "
              "between 0/1 and unbounded knapsack — one of the neatest "
              "facts in the subject.",
   "note": "This is a favourite exam question and a genuinely elegant point. "
           "Make sure they try it both ways."},

  {"t": "table", "kicker": "Canon", "title": "The DPs worth knowing by heart",
   "header": ["Problem", "State", "Complexity"],
   "widths": [4.4, 4.3, 3.4],
   "rows": [
     ["Fibonacci", "dp[i]", "O(n)"],
     ["0/1 knapsack", "dp[i][w]", "O(nW)"],
     ["Longest common subsequence", "dp[i][j]", "O(mn)"],
     ["Edit distance", "dp[i][j]", "O(mn)"],
     ["Longest increasing subsequence", "dp[i] (or patience)", "O(n²) / O(n log n)"],
     ["Matrix chain order", "dp[i][j]", "O(n³)"],
     ["Coin change", "dp[amount]", "O(n·amount)"],
     ["Floyd–Warshall", "dp[k][i][j]", "O(V³)"],
     ["Held–Karp TSP", "dp[subset][last]", "O(2ⁿ n²)"],
   ],
   "note": "The last row is a preview of Module 12: DP over subsets is how "
           "you get exponential algorithms that are nonetheless far better "
           "than brute force."},

  {"t": "callout", "title": "Pseudo-polynomial is not polynomial",
   "kind": "Important for Module 12",
   "body": ["Knapsack's O(nW) looks polynomial. It is not polynomial in the "
            "<i>input size</i>.",
            "W is a <b>value</b> written in binary, so encoding it takes "
            "log W bits. An algorithm running in O(nW) is therefore "
            "exponential in the length of its input.",
            "This is why knapsack can be NP-hard despite having an O(nW) "
            "algorithm — and why the distinction between a number's "
            "value and its encoding length matters in Module 12."]},
 ],
 "takeaways": [
   "Overlapping subproblems are the signal for dynamic programming; "
   "independent ones mean divide and conquer.",
   "DP is recursion plus a table. The mystique is unearned.",
   "Four questions: what is the subproblem, what is the recurrence, what are "
   "the base cases, in what order. Question 1 is where people get stuck.",
   "Complexity is states × work per state. That is the entire analysis.",
   "Write top-down first — it is just the recurrence with a cache. "
   "Convert to bottom-up only for space or constant factors.",
   "In 1-D knapsack the loop direction decides whether you solve 0/1 or "
   "unbounded. Downward is 0/1.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The signal: overlapping subproblems"),
  ("p", "Module 02 established that divide and conquer works when subproblems "
        "are independent. When they are not — when the same subproblem "
        "arises repeatedly — naive recursion recomputes it exponentially "
        "often."),
  ("p", "The canonical demonstration is Fibonacci. Computing fib(n) "
        "recursively makes approximately &phi;&#8319; calls, yet there are "
        "only n+1 distinct values to compute. Everything beyond those n+1 is "
        "pure recomputation."),
  ("callout", "Dynamic programming in one sentence",
   ["Compute each distinct subproblem once, store the answer, and look it up "
    "thereafter.",
    "That is the whole idea. The name is historical and actively misleading "
    "— Bellman chose it partly because it sounded impressive to a "
    "sceptical funder — and the technique is better described as "
    "'recursion with a table'."]),
  ("h2", "1.1 &nbsp; The two requirements"),
  ("ul", ["<b>Optimal substructure.</b> An optimal solution to the problem "
          "contains optimal solutions to its subproblems. Shared with greedy "
          "algorithms (Module 09).",
          "<b>Overlapping subproblems.</b> The same subproblem is required "
          "many times. This is what separates DP from divide and conquer, and "
          "what makes the table worth keeping."]),
  ("p", "Both are needed. Without optimal substructure the recurrence is "
        "invalid; without overlap the table is pointless overhead and plain "
        "recursion is better."),

  ("h1", "2 &nbsp; The design method"),
  ("p", "Four questions, answered in order. The code is mechanical once they "
        "are answered, and essentially every difficulty people have with "
        "dynamic programming is a difficulty with question 1."),
  ("h2", "2.1 &nbsp; What is the subproblem?"),
  ("p", "Write the definition in English, precisely, before touching code. "
        "Good definitions look like:"),
  ("ul", ["<code>dp[i][w]</code> = the maximum value obtainable using only "
          "the first i items with total weight at most w.",
          "<code>dp[i][j]</code> = the length of the longest common "
          "subsequence of a[0..i) and b[0..j).",
          "<code>dp[mask][v]</code> = the shortest route visiting exactly the "
          "cities in <code>mask</code> and ending at v."]),
  ("p", "Note what these have in common: each fixes a prefix, a subset, or a "
        "range, and each is a complete specification you could hand to "
        "someone else. If you cannot state your subproblem in one sentence, "
        "you do not yet have one, and no amount of coding will rescue that."),
  ("h2", "2.2 &nbsp; What is the recurrence?"),
  ("p", "How does a subproblem's answer follow from smaller ones? This is "
        "normally a case analysis over the <i>last decision</i>: take the "
        "item or do not; match the characters or delete from one side; place "
        "the parenthesis here or there."),
  ("h2", "2.3 &nbsp; What are the base cases?"),
  ("p", "The smallest subproblems, answerable directly. Empty prefix, empty "
        "set, zero capacity. Getting these wrong produces answers that are "
        "subtly off by a constant, which is harder to debug than a crash."),
  ("h2", "2.4 &nbsp; In what order?"),
  ("p", "Every entry must be computed after everything it depends on. "
        "Top-down memoisation handles this automatically — the recursion "
        "enforces it — which is one reason to write that form first. "
        "Bottom-up requires you to work the order out, and getting it wrong "
        "gives silently wrong answers rather than errors. Floyd&ndash;Warshall "
        "requiring k outermost (Module 07) is exactly this constraint."),

  ("h1", "3 &nbsp; Complexity"),
  ("eq", "time = (number of states) &times; (work per state)"),
  ("table", ["Problem", "States", "Per state", "Total"],
   [["Fibonacci", "O(n)", "O(1)", "O(n)"],
    ["0/1 knapsack", "O(nW)", "O(1)", "O(nW)"],
    ["Edit distance", "O(mn)", "O(1)", "O(mn)"],
    ["Matrix chain", "O(n&#178;)", "O(n) — try every split", "O(n&#179;)"],
    ["Held&ndash;Karp TSP", "O(2&#8319; n)", "O(n)", "O(2&#8319; n&#178;)"]],
   [0.26, 0.20, 0.30, 0.24]),
  ("p", "Count the table entries, multiply by the cost of filling one. There "
        "is nothing more to the analysis, which makes DP unusually easy to "
        "cost before you implement it — a real advantage when deciding "
        "whether an approach is affordable."),
  ("callout", "Pseudo-polynomial",
   ["Knapsack's O(nW) looks polynomial, and in a sense it is — but not "
    "in the length of the input.",
    "W is a <i>numeric value</i>. Writing it down takes about log&#8322; W "
    "bits, so an input containing W has size proportional to log W, and "
    "O(nW) is <b>exponential in the input length</b>. Doubling the number of "
    "bits used to write W squares the running time.",
    "Algorithms of this shape are called <b>pseudo-polynomial</b>. The "
    "distinction is why knapsack can be NP-hard (Module 12) while admitting "
    "an O(nW) algorithm, and it is a genuine trap when estimating "
    "feasibility."]),

  ("break",),
  ("h1", "4 &nbsp; Two implementations"),
  ("h2", "4.1 &nbsp; Top-down: memoised recursion"),
  ("code", """from functools import lru_cache

@lru_cache(maxsize=None)
def lcs(i, j):
    if i == 0 or j == 0:
        return 0
    if a[i-1] == b[j-1]:
        return 1 + lcs(i-1, j-1)
    return max(lcs(i-1, j), lcs(i, j-1))"""),
  ("p", "This is literally the recurrence, with a cache decorator. The "
        "recursion enforces dependency order for free, and only subproblems "
        "actually reachable from the top are computed — which can be a "
        "large saving when the state space is sparse."),
  ("h2", "4.2 &nbsp; Bottom-up: tabulation"),
  ("code", """def lcs_table(a, b):
    dp = [[0] * (len(b)+1) for _ in range(len(a)+1)]
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[len(a)][len(b)]"""),
  ("table", ["", "Top-down", "Bottom-up"],
   [["Ease of writing", "Easier — it <i>is</i> the recurrence",
     "You must determine the fill order yourself"],
    ["States computed", "Only those reachable from the top",
     "All of them, whether needed or not"],
    ["Overhead", "Call stack and cache lookups",
     "None — plain array indexing"],
    ["Space optimisation", "Awkward",
     "Natural — keep only the rows still needed"],
    ["Deep state chains", "Risk of stack overflow", "No risk"]],
   [0.20, 0.40, 0.40]),
  ("p", "<b>Recommendation:</b> write top-down first, always. It is closer to "
        "the recurrence you reasoned about, so there is less to get wrong. "
        "Convert to bottom-up only when you need the space reduction or the "
        "constant factor."),

  ("h1", "5 &nbsp; Space reduction"),
  ("p", "When a DP row depends only on the previous row, you need not keep "
        "the whole table."),
  ("code", """def knapsack(items, W):
    dp = [0] * (W + 1)
    for value, weight in items:
        for w in range(W, weight - 1, -1):   # DOWNWARD
            dp[w] = max(dp[w], dp[w - weight] + value)
    return dp[W]"""),
  ("callout", "The loop direction is the algorithm",
   ["Iterating w <b>downward</b> means <code>dp[w - weight]</code> still "
    "holds the value from the <i>previous</i> item's row, so each item is "
    "used at most once. This is 0/1 knapsack.",
    "Iterating w <b>upward</b> means <code>dp[w - weight]</code> may already "
    "have been updated for the <i>current</i> item, so the item can be used "
    "again. This is <b>unbounded</b> knapsack.",
    "Two problems, one loop, opposite directions. It is among the neatest "
    "facts in the subject, and it is also a trap: get the direction wrong and "
    "you solve the other problem silently, with no error and a plausible "
    "answer."]),
  ("p", "The same technique applies to edit distance and LCS (keep two rows, "
        "or one row plus a diagonal), reducing O(mn) space to O(min(m, n)). "
        "The cost is that you can no longer reconstruct the actual solution "
        "by backtracking through the table — only its value. "
        "Hirschberg's algorithm recovers the alignment in linear space by "
        "combining this with divide and conquer, which is a pleasing "
        "collision of Modules 02 and 10."),

  ("h1", "6 &nbsp; The canon"),
  ("table", ["Problem", "Subproblem", "Complexity", "Note"],
   [["0/1 knapsack", "dp[i][w]: first i items, capacity w", "O(nW)",
     "Pseudo-polynomial."],
    ["Longest common subsequence", "dp[i][j]: prefixes of length i and j",
     "O(mn)", "The basis of diff."],
    ["Edit distance", "dp[i][j]: prefixes", "O(mn)",
     "Spell checking, DNA alignment, fuzzy search."],
    ["Longest increasing subsequence", "dp[i]: LIS ending at i",
     "O(n&#178;) or O(n log n)",
     "The faster version uses patience sorting and binary search."],
    ["Matrix chain multiplication", "dp[i][j]: best cost for the range",
     "O(n&#179;)", "Range DP — the pattern for many parsing problems."],
    ["Coin change", "dp[amount]", "O(n &middot; amount)",
     "Solves what greedy could not (Module 09)."],
    ["Floyd&ndash;Warshall", "dp[k][i][j]", "O(V&#179;)",
     "You already wrote this in Module 07."],
    ["Held&ndash;Karp TSP", "dp[mask][last]", "O(2&#8319; n&#178;)",
     "Exponential, but vastly better than O(n!). Module 12."]],
   [0.23, 0.31, 0.19, 0.27]),
 ],
 "resources": [
   ("MIT 6.006 — Dynamic Programming I–IV",
    "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
    "Four lectures built around the 'five easy steps' framework, which is "
    "close to the four questions used here. The best structured introduction "
    "available."),
   ("Jeff Erickson, Algorithms — Dynamic Programming chapter",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "Outstanding on how to <i>find</i> the subproblem, with many worked "
    "examples and an honest account of the false starts."),
   ("Tim Roughgarden — Dynamic Programming (Part 3)",
    "https://www.algorithmsilluminated.org/",
    "Knapsack, sequence alignment, and optimal BSTs at an unhurried pace."),
   ("CSES Problem Set — Dynamic Programming section",
    "https://cses.fi/problemset/",
    "19 problems ordered by difficulty, auto-graded. The single best free "
    "source of DP practice."),
 ],
 "exercises": [
   "Implement Fibonacci three ways: naive recursion, memoised, and bottom-up "
   "with O(1) space. Measure all three and find the n at which naive "
   "recursion becomes unusable.",
   "Implement 0/1 knapsack with the 1-D array. Then flip the loop direction "
   "and verify you have solved unbounded knapsack. Explain the mechanism in "
   "writing.",
   "Implement edit distance and extend it to reconstruct the actual sequence "
   "of operations by backtracking through the table.",
   "Implement LIS in O(n&#178;), then in O(n log n) with patience sorting. "
   "Measure both at n = 10&#8309;.",
   "Implement matrix chain multiplication. Verify on a chain where the "
   "optimal order is dramatically better than left-to-right, and report the "
   "ratio.",
   "Implement Held&ndash;Karp TSP over subsets. Find the largest n you can "
   "solve in one minute, and compare with the n! brute force.",
   "Take a problem you solved greedily in Module 09 and where greed failed "
   "(coin change with {1,3,4} is a good choice). Solve it with DP and confirm "
   "the optimal answer.",
 ],
 "selfcheck": [
   "What property distinguishes a dynamic programming problem from a divide "
   "and conquer one?",
   "State the four design questions in order, and say which one causes most "
   "difficulty.",
   "How do you compute the complexity of a DP?",
   "What is pseudo-polynomial time, and why is O(nW) knapsack not polynomial "
   "in the input size?",
   "Give two reasons to prefer top-down, and two to prefer bottom-up.",
   "In 1-D knapsack, what does the loop direction determine, and why?",
 ],
},

]
