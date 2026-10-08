# -*- coding: utf-8 -*-
"""CSCE 627 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Finite Memory",
 "subtitle": "What a machine with no memory of how it got here cannot "
             "do.",
 "question": "What can be recognised with a fixed, finite amount of "
             "state?",
 "outcomes": [
     "Define a DFA and an NFA and convert between them.",
     "Explain why non-determinism adds no power here.",
     "Prove a language non-regular with the pumping lemma.",
     "State the closure properties and use them in proofs.",
     "Recognise regular languages in practical settings.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "States, transitions, and nothing else."},

  {"t": "callout", "title": "A finite automaton's only memory is which state it is in",
   "kind": "The whole constraint",
   "body": ["<b>A finite set of states, a transition on each input "
            "symbol, a start state, and a set of accepting "
            "states.</b> Read the input once, left to right.",
            "<b>So the machine's entire memory of the input so far is "
            "one state out of finitely many</b> — which means <b>two "
            "inputs leading to the same state are indistinguishable "
            "forever after</b>.",
            "<b>That observation is the whole theory.</b> <b>A language "
            "is regular exactly when it has finitely many "
            "distinguishable prefix classes</b> "
            "(Myhill–Nerode), and every non-regularity proof is "
            "that fact in disguise.",
            "<b>And it gives the minimal DFA for free:</b> the states "
            "<i>are</i> the equivalence classes, so <b>the minimal "
            "automaton is unique up to renaming</b> — which is "
            "unusual and useful."]},

  {"t": "code", "kicker": "Equivalence", "title": "Non-determinism adds nothing, and the proof is a construction",
   "lang": "text", "code": """
  AN NFA may have several transitions on one symbol, or
  none, or epsilon-transitions. It accepts if SOME path
  accepts.

  CLAIM: every NFA has an equivalent DFA.

  THE SUBSET CONSTRUCTION:
      the DFA's states are SETS of NFA states
      the DFA's state after reading w is exactly the set of
          NFA states reachable on w
      accept if that set contains any NFA accepting state

  Determinism is recovered by tracking ALL the places the
  NFA could be, at once.

  THE COST: 2^n states in the worst case, and that bound is
  TIGHT -- there are languages where every equivalent DFA
  really does need exponentially many states.
""",
   "caption": "<b>Determinism is recovered by tracking all the places "
              "the NFA could be at once</b>, which costs states and "
              "buys predictability.",
   "note": "Hold the construction before drawing the conclusions."},

  {"t": "code", "kicker": "Consequences", "title": "What that equivalence means",
   "lang": "text", "code": """
  SO NON-DETERMINISM BUYS CONCISENESS, NOT POWER.

  That distinction recurs. In CSCE 637, whether
  non-determinism buys POWER for polynomial time is the
  P vs NP question, and it is OPEN. Here the same question
  is settled, and the answer is no.

  AND IT IS WHY REGEX ENGINES COME IN TWO KINDS:
      Thompson NFA simulation -- linear time, because it
          tracks a SET of states rather than searching
          paths
      backtracking -- exponential worst case, but it
          supports backreferences, which are not regular
          at all

  So the engine choice is a choice about which language
  class you support, and the performance follows from the
  theory rather than from implementation quality.
""",
   "caption": "<b>Catastrophic backtracking is a direct consequence of "
              "leaving the regular languages</b> — a theorem "
              "showing up as a production incident.",
   "note": "The P vs NP parallel is the connection worth making early."},

  {"t": "section", "label": "Part 2", "title": "Proving a limit",
   "blurb": "The pumping lemma, and how to use it."},

  {"t": "callout", "title": "The pumping lemma is the pigeonhole principle on states",
   "kind": "Where it comes from",
   "body": ["<b>If a DFA with p states accepts a string of length at "
            "least p, some state repeats</b> — there are more steps "
            "than states.",
            "<b>The segment between the two visits to that state is a "
            "loop</b>, so it can be traversed any number of times and "
            "the machine still accepts.",
            "<b>So every sufficiently long accepted string splits as "
            "xyz with |y| > 0 and |xy| ≤ p, and "
            "xyⁱz is accepted for every i ≥ 0.</b>",
            "<b>To prove a language non-regular, assume p exists, "
            "choose a string cleverly, and show no valid split "
            "survives pumping.</b> <b>The art is entirely in the "
            "choice of string.</b>"]},

  {"t": "code", "kicker": "Worked", "title": "A proof, in full",
   "lang": "text", "code": """
  CLAIM: L = { a^n b^n : n >= 0 } is not regular.

  Suppose it is, with pumping length p.
  Choose s = a^p b^p, which is in L and has length >= p.

  The lemma gives s = xyz with |y| > 0 and |xy| <= p.
  Since |xy| <= p, the prefix xy lies entirely within the
  a's -- so y consists only of a's, and y is non-empty.

  Then xyyz has MORE a's than b's, so it is not in L.
  But the lemma says xyyz must be in L. Contradiction.
  Therefore L is not regular.

  WHY THE CHOICE OF s MATTERED: with s = (ab)^p the split
  could straddle, and the argument is harder. With
  s = a^p b^p the |xy| <= p condition pins y inside the
  a's, which is what makes the contradiction immediate.

  THE GENERAL TACTIC: choose s so that the |xy| <= p
  condition FORCES y into a region where pumping visibly
  breaks a counting or matching requirement.

  AND THE INTUITION FIRST: a^n b^n needs UNBOUNDED counting,
  and finite state cannot count without a bound. The lemma
  is the formal version of that; have the intuition before
  writing the proof.
""",
   "caption": "<b>Have the intuition before the proof</b> — 'this "
              "needs unbounded memory' comes first, and the lemma makes "
              "it rigorous.",
   "note": "Students apply the lemma mechanically and fail; the "
           "string-choice tactic is the teachable part."},

  {"t": "section", "label": "Part 3", "title": "Closure",
   "blurb": "Building proofs out of other proofs."},

  {"t": "table", "kicker": "Closure", "title": "Regular languages are closed under",
   "header": ["Operation", "Construction", "Note"],
   "widths": [2.6, 4.2, 5.2],
   "rows": [
     ["<b>Union, intersection</b>", "<b>Product automaton</b>", "<b>States are pairs; accept per the operation</b>"],
     ["<b>Complement</b>", "<b>Swap accepting states — of a DFA</b>", "<b>Does NOT work on an NFA. A classic error</b>"],
     ["<b>Concatenation, star</b>", "<b>Easy with an NFA</b>", "<b>Which is what NFAs are for</b>"],
     ["<b>Reversal, homomorphism</b>", "Reverse the arrows; relabel", "Both straightforward"],
     ["<b>Intersection with regular</b>", "<b>Product</b>", "<b>The most useful proof tool — see below</b>"],
   ],
   "footnote": "<b>Closure under intersection is the best proof "
               "technique here:</b> to show L is not regular, intersect "
               "it with a regular language and get something already "
               "known not to be.",
   "note": "The intersection trick saves many painful pumping "
           "arguments."},

  {"t": "callout", "title": "Why closure proofs beat pumping proofs when they apply",
   "kind": "The practical advice",
   "body": ["<b>Pumping arguments require inventing a string and "
            "checking every split.</b> They are error-prone and the "
            "cases multiply.",
            "<b>Closure arguments reuse a result you already have.</b> "
            "<b>To show L non-regular, intersect it with a regular "
            "language and obtain a known non-regular "
            "language</b> — if L were regular, so would that be.",
            "<b>Example:</b> the language of balanced strings over "
            "{a,b} intersected with a*b* is "
            "{aⁿbⁿ}, which Part 2 settled.",
            "<b>So try closure first.</b> <b>And note that the pumping "
            "lemma is necessary but not sufficient</b> — a language "
            "can satisfy it and still not be regular, so a failed "
            "pumping argument proves nothing."]},

  {"t": "section", "label": "Part 4", "title": "In practice",
   "blurb": "Where regular languages actually appear."},

  {"t": "bullets", "kicker": "Practice", "title": "Regular languages in real systems",
   "items": [
     "<b>Lexical analysis.</b> <b>Tokens are regular by design</b>, "
     "which is why a lexer is a DFA and runs in linear time "
     "(CSCE 605 §02).",
     "",
     "<b>Protocol and input validation</b>, where finite state is "
     "exactly the right amount of power and an unbounded parser would "
     "be a liability.",
     "",
     "<b>Model checking of finite-state systems</b>, where the state "
     "space is finite by construction and everything is decidable.",
     "",
     "<b>Text search.</b> <b>Thompson NFA simulation is linear and "
     "immune to catastrophic backtracking</b>, which is why "
     "<code>grep</code> does not hang and some regex libraries do.",
     "",
     "<b>And not: matching nested brackets, HTML, or anything "
     "balanced.</b> <b>That is Module 03, and the famous refusal to "
     "parse HTML with a regex is this theorem.</b>",
   ],
   "footnote": "<b>'Regex' in most libraries is not regular</b> "
               "— backreferences and lookahead exceed the regular "
               "languages, which is exactly where the exponential "
               "behaviour comes from."},
 ],
 "takeaways": [
   "A finite automaton's entire memory is its current state, so two inputs "
   "reaching the same state are indistinguishable forever after.",
   "A language is regular exactly when it has finitely many "
   "distinguishable prefix classes, and the minimal DFA's states are those "
   "classes.",
   "Non-determinism buys conciseness and not power here — whereas the "
   "same question for polynomial time is P versus NP and is open.",
   "The pumping lemma is the pigeonhole principle on states, and the art "
   "is entirely in choosing the string.",
   "Closure under intersection is the better proof technique when it "
   "applies, and a failed pumping argument proves nothing.",
   "Most libraries' 'regex' is not regular — backreferences exceed "
   "the class, which is where catastrophic backtracking comes from.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The model, and non-determinism"),
  ("callout", "A finite automaton's only memory is which state it is in",
   ["<b>A finite set of states, a transition function on each input "
    "symbol, a start state, and a set of accepting states.</b> The input "
    "is read once, left to right, with no ability to go back.",
    "<b>So the machine's entire memory of everything it has read is one "
    "state out of finitely many</b> — which means <b>two different "
    "inputs that lead to the same state are indistinguishable from that "
    "point onward, for every possible continuation.</b>",
    "<b>That single observation is the whole theory.</b> <b>A language "
    "is regular exactly when it has finitely many distinguishable prefix "
    "classes</b> — the Myhill–Nerode theorem — where two "
    "prefixes are distinguishable if some suffix puts one in the language "
    "and the other out. <b>Every non-regularity proof in this module is "
    "that fact in disguise.</b>",
    "<b>And it gives the minimal DFA for free:</b> the states "
    "<i>are</i> the equivalence classes, so <b>the minimal automaton for "
    "a regular language is unique up to renaming of states</b> — "
    "which is an unusual property (nothing like it holds for context-free "
    "grammars or for Turing machines) and is what makes DFA minimisation "
    "a well-defined operation with a canonical answer."]),
  ("code", """AN NFA may have several transitions on one symbol, or none,
or epsilon-transitions. It accepts if SOME path accepts.

CLAIM: every NFA has an equivalent DFA.

THE SUBSET CONSTRUCTION:
    the DFA's states are SETS of NFA states
    the DFA's state after reading w is exactly the set of
        NFA states reachable from the start on w
    accept if that set contains any NFA accepting state

Determinism is recovered by tracking ALL the places the NFA
could simultaneously be.

THE COST: 2^n states in the worst case, and the bound is
TIGHT -- there are languages for which every equivalent DFA
genuinely needs exponentially many states.

SO NON-DETERMINISM BUYS CONCISENESS, NOT POWER. And that
distinction recurs: in CSCE 637, whether non-determinism
buys POWER for polynomial time is the P vs NP question, and
it is open. Here the same question is settled, and the
answer is no.

AND THIS IS WHY REGEX ENGINES COME IN TWO KINDS: Thompson
NFA simulation (linear time, because it tracks a SET of
states) and backtracking (exponential worst case, but it
supports backreferences, which are not regular at all)."""),
  ("p", "<b>The regex-engine connection is the practical payoff of this "
        "section.</b> <b>Catastrophic backtracking is a direct "
        "consequence of leaving the regular languages</b>: a pattern with "
        "a backreference is not describable by any finite automaton, so no "
        "linear-time simulation exists for it, so the engine must search "
        "— and the search is exponential. <b>Which means the choice "
        "between the two engine designs is a choice about which language "
        "class you are willing to support</b>, and the performance "
        "follows from the theory rather than from implementation "
        "quality."),

  ("h1", "2 &nbsp; Proving a language non-regular"),
  ("callout", "The pumping lemma is the pigeonhole principle on states",
   ["<b>If a DFA with p states accepts a string of length at least p, "
    "then some state must repeat during the computation</b> — there "
    "are more steps than there are states, so by the pigeonhole principle "
    "two of them coincide.",
    "<b>The segment of input consumed between the two visits to that "
    "state forms a loop</b>, so it can be traversed zero times, once, or "
    "any number of times, and the machine ends in the same state and "
    "still accepts.",
    "<b>So every sufficiently long accepted string splits as xyz with "
    "|y| &gt; 0 and |xy| &le; p, and xy<super>i</super>z is accepted for "
    "every i &ge; 0.</b> The |xy| &le; p condition records that the "
    "repeat happens within the first p symbols.",
    "<b>To prove a language non-regular: assume a pumping length p "
    "exists, choose a string in the language cleverly, and show that no "
    "valid split of it survives pumping.</b> <b>The art is entirely in "
    "the choice of string</b>, and &sect;2's worked example shows what a "
    "good choice does."]),
  ("code", """CLAIM: L = { a^n b^n : n >= 0 } is not regular.

Suppose it is, with pumping length p.
Choose s = a^p b^p, which is in L and has length >= p.

The lemma gives s = xyz with |y| > 0 and |xy| <= p.
Since |xy| <= p, the prefix xy lies entirely within the
a's -- so y consists only of a's, and y is non-empty.

Then xyyz has strictly MORE a's than b's, so it is not in L.
But the lemma says xyyz must be in L. Contradiction.
Therefore L is not regular.

WHY THE CHOICE OF s MATTERED: with s = (ab)^p the split
could straddle an a and a b, and the case analysis is
harder. With s = a^p b^p the |xy| <= p condition PINS y
inside the a's, which makes the contradiction immediate.

THE GENERAL TACTIC: choose s so that the |xy| <= p
condition FORCES y into a region where pumping visibly
breaks a counting or matching requirement.

AND HAVE THE INTUITION FIRST: a^n b^n requires UNBOUNDED
counting, and a machine with finite state cannot count
without a bound. The lemma is the formal version of that
observation -- so form the intuition, then write the
proof."""),

  ("break",),
  ("h1", "3 &nbsp; Closure properties"),
  ("table", ["Operation", "Construction", "Note"],
   [["<b>Union and intersection</b>", "<b>The product automaton.</b>",
     "<b>States are pairs (p, q), one from each machine; accept "
     "according to the operation.</b> Simulates both at once."],
    ["<b>Complement</b>",
     "<b>Swap accepting and non-accepting states — of a DFA.</b>",
     "<b>This does NOT work on an NFA</b>, because an NFA accepts if "
     "<i>some</i> path accepts and swapping does not negate that. <b>A "
     "classic and costly error</b>: convert to a DFA first."],
    ["<b>Concatenation and star</b>",
     "<b>Easy with an NFA</b> — add &epsilon;-transitions.",
     "<b>Which is precisely what NFAs are for</b>: these constructions "
     "are awkward on a DFA and trivial on an NFA."],
    ["<b>Reversal, homomorphism, inverse homomorphism</b>",
     "Reverse all arrows and swap start and accepting; relabel symbols.",
     "All straightforward, and all occasionally useful in proofs."],
    ["<b>Intersection with a regular language</b>",
     "<b>The product construction again.</b>",
     "<b>The most useful proof tool in the module</b> — see the "
     "callout."]],
   [0.22, 0.34, 0.44]),
  ("callout", "Why closure proofs beat pumping proofs when they apply",
   ["<b>Pumping arguments require inventing a suitable string and then "
    "checking every valid split of it.</b> They are error-prone, the "
    "cases multiply when the string is not well chosen, and a student's "
    "first attempt usually picks a string that admits an awkward "
    "split.",
    "<b>Closure arguments reuse a result you already have.</b> <b>To "
    "show L is not regular, intersect it with a regular language and "
    "obtain a language already known not to be regular</b> — if L "
    "were regular, the intersection would be too, by the table above, "
    "and it is not.",
    "<b>Example:</b> the language of strings over {a, b} with equally "
    "many a's and b's, intersected with the regular language "
    "a*b*, is exactly {a<super>n</super>b<super>n</super>}, which "
    "&sect;2 settled. <b>Two lines, no case analysis.</b>",
    "<b>So try a closure argument first.</b> <b>And note that the "
    "pumping lemma is a necessary condition and not a sufficient one</b> "
    "— there exist non-regular languages that satisfy it — "
    "<b>so a failed pumping argument proves nothing at all</b>, which is "
    "a distinction worth being careful about since the lemma is usually "
    "taught as if it were a characterisation. <b>Myhill–Nerode "
    "(&sect;1) is the actual characterisation</b>, and it is sometimes "
    "the easier route."]),

  ("h1", "4 &nbsp; Regular languages in real systems"),
  ("ul", ["<b>Lexical analysis.</b> <b>Programming language tokens are "
          "regular by deliberate design</b> — identifiers, numbers, "
          "operators, comments — <b>which is why a lexer is a DFA "
          "and runs in time linear in the input</b> (CSCE 605 "
          "Module 02). <b>The design decision came first and the "
          "efficiency followed.</b>",
          "<b>Protocol and input validation</b>, where finite state is "
          "exactly the right amount of power — and where an "
          "unbounded parser would be a liability rather than a feature, "
          "since it could accept inputs nobody intended.",
          "<b>Model checking of finite-state systems</b>, where the "
          "state space is finite by construction, so everything about it "
          "is decidable and the techniques of this module apply "
          "directly.",
          "<b>Text search.</b> <b>Thompson NFA simulation is linear in "
          "the input and immune to catastrophic backtracking</b>, because "
          "it tracks the set of reachable states rather than searching "
          "paths — <b>which is why <code>grep</code> does not hang "
          "on adversarial patterns and several widely-used regex "
          "libraries do.</b>",
          "<b>And not: matching nested brackets, parsing HTML, or "
          "anything requiring balance.</b> <b>That is Module 03, and "
          "the well-known refusal to parse HTML with a regular expression "
          "is this theorem rather than an aesthetic preference.</b> "
          "<b>Note also that 'regex' in most libraries is not "
          "regular</b> — backreferences and lookahead strictly "
          "exceed the regular languages, which is exactly where the "
          "exponential behaviour comes from."]),
 ],
 "resources": [
   ("Sipser &mdash; chapter 1",
    "https://math.mit.edu/~sipser/book.html",
    "<b>Finite automata, the subset construction, and the pumping "
    "lemma</b> — the reference for this module."),
   ("MIT 18.404J &mdash; lectures 1–3 (free)",
    "https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/",
    "<b>The same material lectured</b>, with problem sets and "
    "solutions."),
   ("Cox &mdash; Regular Expression Matching Can Be Simple And Fast "
    "(free)",
    "https://swtch.com/~rsc/regexp/regexp1.html",
    "<b>&sect;1's engine distinction, in practice</b> — Thompson "
    "simulation against backtracking, with measurements. Required "
    "reading for anyone who uses regular expressions."),
   ("Hopcroft, Motwani & Ullman &mdash; chapters 2–4",
    "https://www.pearson.com/en-us/subject-catalog/p/introduction-to-automata-theory-languages-and-computation/P200000003517",
    "<b>Myhill–Nerode and DFA minimisation</b>, treated more "
    "thoroughly than Sipser does."),
 ],
 "exercises": [
   "<b>Implement a DFA simulator</b> and a DFA for a language of your "
   "choosing.",
   "<b>Implement the subset construction</b> and convert an NFA with 8 "
   "states. Report the DFA's size.",
   "<b>Construct a language where the blow-up is exponential</b> and "
   "confirm it.",
   "<b>Prove three languages non-regular</b> by the pumping lemma, "
   "choosing the strings yourself.",
   "<b>Deliberately choose a bad string</b> for one of them and report "
   "how much harder the case analysis becomes.",
   "<b>Prove one of the same languages non-regular by a closure "
   "argument</b> and compare the two proofs' lengths.",
   "<b>Complement an NFA by swapping accepting states</b> and exhibit a "
   "string showing the result is wrong.",
   "<b>Minimise a DFA</b> and relate its states to Myhill–Nerode "
   "classes.",
   "<b>Write a catastrophically backtracking regex</b> and time it "
   "against input length.",
   "<b>Run the same pattern against a Thompson-based engine</b> (RE2, or "
   "Go's regexp) and compare.",
 ],
 "selfcheck": [
   "What is a finite automaton's entire memory, and what follows?",
   "State Myhill–Nerode and explain why the minimal DFA is "
   "unique.",
   "Describe the subset construction and its cost.",
   "What does non-determinism buy here, and what is the open analogue?",
   "Derive the pumping lemma from the pigeonhole principle.",
   "Prove a^n b^n non-regular, and say why the string choice "
   "mattered.",
   "Why is the pumping lemma not a characterisation?",
   "Name five closure properties and the one that fails on NFAs.",
   "Why is the intersection trick the better proof technique?",
   "Why do some regex engines backtrack catastrophically?",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Memory as a Stack",
 "subtitle": "Context-free languages, and why parsing works.",
 "question": "What does adding a stack buy you?",
 "outcomes": [
     "Write a context-free grammar and derive strings from it.",
     "Explain the equivalence of grammars and pushdown automata.",
     "Explain ambiguity and why it matters for parsing.",
     "Prove a language not context-free.",
     "Place the practical grammar classes in the hierarchy.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Grammars",
   "blurb": "Rules that rewrite, and the trees they produce."},

  {"t": "callout", "title": "A context-free grammar generates; a pushdown automaton recognises",
   "kind": "Two views of one class",
   "body": ["<b>A grammar is a set of rules rewriting a non-terminal "
            "into a string of terminals and non-terminals.</b> A string "
            "is in the language if some derivation produces it.",
            "<b>A pushdown automaton is a finite automaton with a "
            "stack</b> — push, pop, and branch on the top symbol. "
            "<b>The stack is unbounded, and it is the only unbounded "
            "memory.</b>",
            "<b>The two are equivalent</b>, and the proof is a "
            "construction in each direction — <b>which is why "
            "'context-free' can mean either a generating or a "
            "recognising device.</b>",
            "<b>And the stack is exactly what counting needs:</b> "
            "<b>push on each a, pop on each b, accept if empty</b> "
            "— so {aⁿbⁿ} is context-free, which "
            "Module 02 showed is not regular."]},

  {"t": "table", "kicker": "The hierarchy", "title": "What each memory discipline buys",
   "header": ["Class", "Memory", "Can express"],
   "widths": [2.7, 3.9, 5.4],
   "rows": [
     ["<b>Regular</b>", "<b>Finite state only</b>", "<b>Tokens. Not nesting</b>"],
     ["<b>Context-free</b>", "<b>A stack</b>", "<b>Nesting. Not cross-dependency</b>"],
     ["<b>Context-sensitive</b>", "<b>Linear tape</b>", "<b>aⁿbⁿcⁿ; declare-before-use</b>"],
     ["<b>Recognisable</b>", "<b>Unbounded tape</b>", "<b>Anything a program can verify (M04)</b>"],
     ["<b>Decidable</b>", "<b>Tape, with a halting guarantee</b>", "<b>Anything a program can decide (M05)</b>"],
   ],
   "footnote": "<b>The hierarchy is strict at every level</b>, and each "
               "separation is proved by the same two techniques — "
               "which is why Module 02's pumping argument is worth having "
               "done properly.",
   "note": "Showing the whole hierarchy here orients the rest of the "
           "course."},

  {"t": "section", "label": "Part 2", "title": "Ambiguity",
   "blurb": "When a string has two trees."},

  {"t": "code", "kicker": "Ambiguity", "title": "Why parsing cares, and what cannot be fixed",
   "lang": "text", "code": """
  A grammar is AMBIGUOUS if some string has two distinct
  parse trees. The classic:

      E -> E + E | E * E | id

  Then "a + b * c" has two trees, and THEY MEAN DIFFERENT
  THINGS. Parsing is not just recognition; the TREE is the
  output, and an ambiguous grammar does not determine it.

  THE USUAL FIXES
      stratify the grammar by precedence level
          E -> E + T | T ;  T -> T * F | F ;  F -> id
      or declare precedence and associativity and let the
          parser generator resolve conflicts
      -- which is what yacc-family tools do, and the
         conflict report is telling you the grammar is
         ambiguous (CSCE 605 Module 03).

  AND SOME LANGUAGES ARE INHERENTLY AMBIGUOUS: no
  unambiguous grammar exists for them at all. Rare, and it
  establishes that ambiguity is not always a grammar-writing
  mistake.

  WORSE: WHETHER A GRAMMAR IS AMBIGUOUS IS UNDECIDABLE
  (Module 08). So a parser generator cannot tell you
  "your grammar is unambiguous" -- it can only report the
  conflicts IT found with ITS method. That is why the
  conflict count is a diagnostic rather than a verdict.
""",
   "caption": "<b>The undecidability of ambiguity is why parser "
              "generators report conflicts rather than verdicts</b> "
              "— a practical consequence of a theorem.",
   "note": "This is the first concrete undecidability payoff in the "
           "course."},

  {"t": "section", "label": "Part 3", "title": "The limit",
   "blurb": "What a stack cannot do."},

  {"t": "callout", "title": "A stack counts one thing at a time",
   "kind": "Where context-free stops",
   "body": ["<b>{aⁿbⁿcⁿ} is not "
            "context-free.</b> The stack can match the a's against the "
            "b's, and it is then empty and cannot also match the "
            "c's.",
            "<b>Nor is {ww : w ∈ {a,b}*}</b> — "
            "<b>a stack reverses what it stores</b>, so it can "
            "recognise wwᴿ and not ww.",
            "<b>The pumping lemma for context-free languages</b> "
            "pumps <i>two</i> segments at once (from a repeated "
            "non-terminal in the parse tree), which is the formal "
            "tool.",
            "<b>And these are exactly the real cases:</b> "
            "<b>declare-before-use, type agreement, and matching "
            "argument counts are all beyond context-free</b> — which "
            "is precisely why a compiler has a separate semantic "
            "analysis phase (CSCE 605 §06)."]},

  {"t": "bullets", "kicker": "Closure", "title": "Context-free closure, and the surprise",
   "items": [
     "<b>Closed under union, concatenation, and star</b> — "
     "combine the grammars.",
     "",
     "<b>NOT closed under intersection.</b> <b>aⁿbⁿc* and "
     "a*bⁿcⁿ are each context-free and their intersection is "
     "aⁿbⁿcⁿ, which is not.</b>",
     "",
     "<b>NOT closed under complement</b>, which follows.",
     "",
     "<b>Closed under intersection with a <i>regular</i> "
     "language</b> — which preserves Module 02's best proof "
     "technique.",
     "",
     "<b>And the deterministic context-free languages are a strict "
     "subclass</b> — unlike the regular case, <b>here "
     "non-determinism does buy power.</b>",
   ],
   "footnote": "<b>That non-determinism matters here and not for regular "
               "languages is worth noting</b> — the question's "
               "answer depends on the model, which is why P versus NP is "
               "hard."},

  {"t": "section", "label": "Part 4", "title": "The practical classes",
   "blurb": "What parsers actually accept."},

  {"t": "table", "kicker": "Parsing", "title": "The grammar classes tools use",
   "header": ["Class", "Parsed by", "Property"],
   "widths": [2.5, 4.0, 5.4],
   "rows": [
     ["<b>LL(k)</b>", "<b>Recursive descent, predictive</b>", "<b>Top-down; no left recursion allowed</b>"],
     ["<b>LR(k), LALR</b>", "<b>Shift-reduce tables</b>", "<b>Strictly more powerful than LL; yacc</b>"],
     ["<b>Deterministic CF</b>", "<b>Deterministic PDA</b>", "<b>Exactly the LR(1) languages</b>"],
     ["<b>General CF</b>", "<b>Earley, CYK, GLR</b>", "<b>O(n³), or O(n²·⁸) by matrix tricks</b>"],
     ["<b>PEG</b>", "<b>Packrat, ordered choice</b>", "<b>NOT a CF subclass — incomparable</b>"],
   ],
   "footnote": "<b>LR(1) exactly characterises the deterministic "
               "context-free languages</b>, which is a satisfying "
               "coincidence of a practical tool with a theoretical "
               "class.",
   "note": "The PEG row matters; students assume it is a CF subset."},

  {"t": "callout", "title": "Why real languages are not quite context-free, and it does not matter",
   "kind": "The engineering reality",
   "body": ["<b>No real programming language is context-free.</b> "
            "Declare-before-use, type agreement, and arity checking are "
            "all beyond it (Part 3).",
            "<b>So the standard architecture splits the work:</b> a "
            "regular lexer, a context-free parser, and a separate "
            "semantic phase for everything else "
            "(CSCE 605 §02–06).",
            "<b>Each phase uses the weakest machinery that suffices</b> "
            "— which gives linear lexing, near-linear parsing, and a "
            "general-purpose checker only where one is needed.",
            "<b>That layering is the practical lesson of this "
            "module:</b> <b>use the weakest model that expresses your "
            "problem</b>, because weaker models have better algorithms "
            "and better error messages."]},
 ],
 "takeaways": [
   "A context-free grammar generates and a pushdown automaton recognises "
   "the same class, and the stack is exactly what matched counting needs.",
   "Parsing's output is the tree, so an ambiguous grammar does not "
   "determine the meaning — and ambiguity is undecidable, which is "
   "why parser generators report conflicts rather than verdicts.",
   "A stack counts one thing at a time, so aⁿbⁿcⁿ and ww "
   "are beyond context-free — and those are exactly the real cases "
   "like declare-before-use.",
   "Context-free languages are not closed under intersection, and "
   "aⁿbⁿc* with a*bⁿcⁿ proves it in one line.",
   "Non-determinism buys power for pushdown automata and not for finite "
   "ones, which is why the analogous question for polynomial time is "
   "hard.",
   "LR(1) exactly characterises the deterministic context-free languages, "
   "and PEGs are incomparable with the context-free class rather than a "
   "subset.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Grammars and pushdown automata"),
  ("callout", "A context-free grammar generates; a pushdown automaton "
              "recognises",
   ["<b>A grammar is a finite set of rules, each rewriting a single "
    "non-terminal into a string of terminals and non-terminals.</b> A "
    "string is in the language if some sequence of rewrites starting from "
    "the start symbol produces it.",
    "<b>A pushdown automaton is a finite automaton with a stack</b> "
    "— it may push, pop, and branch on the symbol currently on top. "
    "<b>The stack is unbounded, and it is the only unbounded memory the "
    "machine has</b>, which is the entire difference from Module 02.",
    "<b>The two formalisms are equivalent</b>, and the proof is an "
    "explicit construction in each direction — <b>which is why "
    "'context-free' is used to describe both a generating device and a "
    "recognising one</b> without ambiguity.",
    "<b>And the stack is exactly what matched counting requires:</b> "
    "<b>push a marker for each a, pop one for each b, and accept if the "
    "stack is empty at the end</b> — so "
    "{a<super>n</super>b<super>n</super>} is context-free, and "
    "Module 02 &sect;2 proved it is not regular. <b>One bounded "
    "counter's worth of unbounded memory, in exactly the shape counting "
    "needs.</b>"]),
  ("table", ["Class", "Memory discipline", "Can express"],
   [["<b>Regular</b>", "<b>Finite state, and nothing else.</b>",
     "<b>Tokens, protocols, validation. Not nesting</b> (Module 02)."],
    ["<b>Context-free</b>", "<b>A stack.</b>",
     "<b>Nesting and matched brackets. Not cross-dependency</b> "
     "(&sect;3)."],
    ["<b>Context-sensitive</b>",
     "<b>A tape bounded by the input length.</b>",
     "<b>a<super>n</super>b<super>n</super>c<super>n</super>, "
     "declare-before-use, type agreement.</b>"],
    ["<b>Recognisable (Turing-recognisable)</b>",
     "<b>An unbounded tape.</b>",
     "<b>Anything a program can verify when the answer is yes</b> "
     "(Module 04)."],
    ["<b>Decidable</b>",
     "<b>An unbounded tape, plus a guarantee of halting.</b>",
     "<b>Anything a program can decide for every input</b> "
     "(Module 05)."]],
   [0.23, 0.31, 0.46]),
  ("p", "<b>The hierarchy is strict at every level</b> — each class "
        "properly contains the one above it — <b>and each separation "
        "is proved by one of the course's two techniques</b>, which is why "
        "Module 02's pumping argument was worth doing carefully. "
        "<b>Placing a problem in this hierarchy tells you what machinery "
        "it needs and therefore what algorithms are available</b>, which "
        "is the practical use of the whole picture."),

  ("h1", "2 &nbsp; Ambiguity"),
  ("code", """A grammar is AMBIGUOUS if some string in its language has
two distinct parse trees. The classic case:

    E -> E + E | E * E | id

Then "a + b * c" has two parse trees, and THEY MEAN
DIFFERENT THINGS. Parsing is not merely recognition: the
TREE is the output, and an ambiguous grammar does not
determine it.

THE USUAL FIXES
    stratify the grammar by precedence level
        E -> E + T | T ;   T -> T * F | F ;   F -> id
    or declare precedence and associativity and let the
        parser generator resolve the conflicts
    -- which is what the yacc family does, and the conflict
       report is telling you the grammar is ambiguous
       (CSCE 605 Module 03).

AND SOME LANGUAGES ARE INHERENTLY AMBIGUOUS: no unambiguous
grammar exists for them at all. Rare, and it establishes
that ambiguity is not always a grammar-writing mistake.

WORSE: WHETHER A GIVEN GRAMMAR IS AMBIGUOUS IS UNDECIDABLE
(Module 08). So a parser generator CANNOT tell you that
your grammar is unambiguous -- it can only report the
conflicts IT found with ITS particular method. Which is why
a conflict count is a diagnostic rather than a verdict, and
why "zero conflicts" does not mean "unambiguous"."""),
  ("p", "<b>The undecidability of ambiguity is why parser generators "
        "report conflicts rather than verdicts</b> — and it is the "
        "first concrete payoff in this course of a result we have not yet "
        "proved. <b>A practical tool's interface is shaped by a theorem "
        "about what no tool can do</b>, which is the pattern Module 12 "
        "generalises."),

  ("break",),
  ("h1", "3 &nbsp; What a stack cannot do"),
  ("callout", "A stack counts one thing at a time",
   ["<b>{a<super>n</super>b<super>n</super>c<super>n</super>} is not "
    "context-free.</b> The stack can match the a's against the b's, but "
    "doing so empties it, and it then has nothing left with which to "
    "match the c's. <b>One matched pair is what a stack affords.</b>",
    "<b>Nor is {ww : w over {a,b}} context-free</b> — <b>a stack "
    "reverses whatever it stores</b>, since the last pushed is the first "
    "popped, <b>so it can recognise ww<super>R</super> (a palindrome) and "
    "not ww (a repetition).</b> Which is a memorable illustration of what "
    "the <i>discipline</i> of the memory costs, independently of its "
    "size.",
    "<b>The pumping lemma for context-free languages is the formal "
    "tool:</b> it pumps <i>two</i> segments simultaneously, arising from "
    "a non-terminal that repeats along a path in the parse tree — "
    "which is Module 02's pigeonhole argument applied to tree depth "
    "rather than to string position.",
    "<b>And these are exactly the cases that arise in practice:</b> "
    "<b>declare-before-use, type agreement between a declaration and a "
    "use, and matching the number of arguments to the number of "
    "parameters are all beyond context-free</b> — <b>which is "
    "precisely why a compiler has a separate semantic analysis phase</b> "
    "(CSCE 605 Module 06) rather than encoding everything in the "
    "grammar. <b>The phase structure of a compiler is this "
    "hierarchy.</b>"]),
  ("ul", ["<b>Closed under union, concatenation, and Kleene star</b> "
          "— combine the grammars with a new start symbol, or "
          "concatenate the right-hand sides.",
          "<b>NOT closed under intersection.</b> "
          "<b>a<super>n</super>b<super>n</super>c* and "
          "a*b<super>n</super>c<super>n</super> are each context-free, "
          "and their intersection is "
          "a<super>n</super>b<super>n</super>c<super>n</super>, which "
          "&sect;3 just showed is not.</b> <b>A one-line proof of "
          "non-closure</b>, and a useful one.",
          "<b>NOT closed under complement</b>, which follows from the "
          "above together with closure under union.",
          "<b>Closed under intersection with a <i>regular</i> "
          "language</b> — which <b>preserves Module 02 &sect;3's "
          "best proof technique</b> for this class too, and is why that "
          "technique is worth the investment.",
          "<b>And the deterministic context-free languages are a strict "
          "subclass of the context-free languages.</b> <b>So unlike the "
          "regular case, here non-determinism genuinely buys power</b> "
          "— <b>which is worth noting carefully, because it shows "
          "that whether non-determinism matters depends on the model.</b> "
          "<b>That is exactly why P versus NP is hard</b>: the answer is "
          "no for finite automata, yes for pushdown automata, and unknown "
          "for polynomial-time Turing machines, so no general principle "
          "settles it."]),

  ("h1", "4 &nbsp; The classes parsers actually use"),
  ("table", ["Class", "Parsed by", "Property"],
   [["<b>LL(k)</b>",
     "<b>Recursive descent with k symbols of lookahead; predictive, no "
     "backtracking.</b>",
     "<b>Top-down, and left recursion must be eliminated first</b> "
     "— which is why hand-written parsers restructure their "
     "grammars."],
    ["<b>LR(k), LALR(1), SLR(1)</b>",
     "<b>Shift-reduce parsing driven by a state table.</b>",
     "<b>Strictly more powerful than LL</b>, and what the yacc family "
     "generates. Handles left recursion naturally."],
    ["<b>Deterministic context-free</b>", "<b>A deterministic PDA.</b>",
     "<b>Exactly the LR(1) languages</b> — a theoretical class and "
     "a practical tool coinciding precisely, which is satisfying and not "
     "accidental."],
    ["<b>General context-free</b>", "<b>Earley, CYK, or GLR.</b>",
     "<b>O(n&#179;) in general, and O(n<super>2.8</super>) by reduction "
     "to matrix multiplication</b> — which is a surprising "
     "connection and not a practical one."],
    ["<b>Parsing expression grammars (PEG)</b>",
     "<b>Packrat parsing with ordered choice.</b>",
     "<b>NOT a subclass of the context-free languages — the two "
     "classes are incomparable.</b> PEGs can express some non-CF "
     "languages and cannot express some CF ones, which students "
     "routinely assume otherwise."]],
   [0.22, 0.34, 0.44]),
  ("callout", "Why real languages are not quite context-free, and it does "
              "not matter",
   ["<b>No real programming language is context-free.</b> "
    "Declare-before-use, type agreement, arity checking, and definite "
    "assignment are all beyond the class (&sect;3) — and attempts to "
    "push them into the grammar produce grammars nobody can read.",
    "<b>So the standard architecture splits the work by what each phase "
    "needs:</b> a regular lexer, a context-free parser, and a separate "
    "semantic analysis phase for everything else (CSCE 605 Modules 02 "
    "through 06).",
    "<b>And each phase uses the weakest machinery that suffices</b> "
    "— which gives <b>linear-time lexing, near-linear parsing, and "
    "a general-purpose checker only where one is genuinely needed</b>, "
    "rather than running the most powerful tool over everything.",
    "<b>That layering is the practical lesson of this module:</b> "
    "<b>use the weakest model that expresses your problem</b>, because "
    "weaker models have better algorithms, better error messages, better "
    "tooling, and decidable questions. <b>It is the same argument as "
    "CSCE 625 Module 01's cheapest-sufficient-agent and CSCE 669 "
    "Module 02's prefer-convexity</b> — three courses arriving at "
    "one principle about choosing the least powerful adequate "
    "formalism."]),
 ],
 "resources": [
   ("Sipser &mdash; chapter 2",
    "https://math.mit.edu/~sipser/book.html",
    "<b>Grammars, pushdown automata, their equivalence, and the "
    "context-free pumping lemma</b> — the reference for "
    "&sect;1–&sect;3."),
   ("Hopcroft, Motwani & Ullman &mdash; chapters 5–7",
    "https://www.pearson.com/en-us/subject-catalog/p/introduction-to-automata-theory-languages-and-computation/P200000003517",
    "<b>Stronger on the parsing classes of &sect;4</b>, including the "
    "LR(1) characterisation."),
   ("Ford &mdash; Parsing Expression Grammars (free)",
    "https://bford.info/pub/lang/peg.pdf",
    "<b>&sect;4's PEG row</b>, including why the class is incomparable "
    "with the context-free languages."),
   ("Grune & Jacobs &mdash; Parsing Techniques, 2nd edition (first "
    "edition free)",
    "https://dickgrune.com/Books/PTAPG_1st_Edition/",
    "<b>The comprehensive survey of &sect;4</b>, with the first edition "
    "freely available from the author."),
 ],
 "exercises": [
   "<b>Write a grammar for balanced brackets</b> and derive three "
   "strings.",
   "<b>Implement a pushdown automaton</b> for the same language and trace "
   "it.",
   "<b>Write the ambiguous expression grammar</b> and exhibit both parse "
   "trees for one string.",
   "<b>Stratify it by precedence</b> and confirm the ambiguity is "
   "gone.",
   "<b>Run an ambiguous grammar through a parser generator</b> and read "
   "the conflict report.",
   "<b>Prove aⁿbⁿcⁿ not context-free</b> by the "
   "context-free pumping lemma.",
   "<b>Prove it again by the intersection non-closure argument</b>, and "
   "compare.",
   "<b>Show that a PDA can recognise wwᴿ and argue it cannot "
   "recognise ww.</b>",
   "<b>Find a PEG that accepts a non-context-free language.</b>",
   "<b>For a language you use, identify which checks are regular, which "
   "context-free, and which neither.</b>",
 ],
 "selfcheck": [
   "Relate grammars to pushdown automata and say why both names are "
   "used.",
   "Why is a stack exactly what matched counting needs?",
   "Give the five-level hierarchy and the memory each has.",
   "Why does parsing care about ambiguity more than recognition does?",
   "Why do parser generators report conflicts rather than verdicts?",
   "Why is aⁿbⁿcⁿ beyond a stack? Why is ww?",
   "Give the one-line proof of non-closure under intersection.",
   "Does non-determinism buy power here? What does that imply about P vs "
   "NP?",
   "Name five parsing classes, and which coincides with a theoretical "
   "class.",
   "Why is no real language context-free, and what architecture "
   "follows?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Turing Machines",
 "subtitle": "The model, and why it is the right one.",
 "question": "What is the simplest model that computes everything "
             "computable?",
 "outcomes": [
     "Define a Turing machine and trace a computation.",
     "Explain robustness — why variants add no power.",
     "Distinguish decidable from Turing-recognisable.",
     "Explain the universal Turing machine and what it established.",
     "Encode machines as strings and explain why that is "
     "essential.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "A tape, a head, and a finite control."},

  {"t": "callout", "title": "A Turing machine is a finite automaton with unbounded, rewritable memory",
   "kind": "The definition, and why it is shaped that way",
   "body": ["<b>An infinite tape, a head that reads and writes one cell "
            "and moves one step, and a finite control.</b> That is "
            "all.",
            "<b>The finite control is the program and the tape is the "
            "memory</b> — so the machine has a fixed-size description "
            "and unbounded working space, which is exactly the situation "
            "of a real computer.",
            "<b>Turing designed it to model a person computing with "
            "paper and pencil</b>, and the justification in his paper is "
            "an argument about what such a person can do — which is "
            "why the thesis is credible.",
            "<b>And the model is deliberately inefficient.</b> <b>It is "
            "a tool for proving what is possible, not for "
            "computing</b> — which is why its polynomial-time class "
            "matters (CSCE 637) and its constants do not."]},

  {"t": "code", "kicker": "Robustness", "title": "Every variant computes the same class",
   "lang": "text", "code": """
  MULTIPLE TAPES           -> simulate on one, interleaved.
      Costs a quadratic slowdown. Same class.
  TWO-WAY INFINITE TAPE    -> fold it, store both halves
      interleaved on a one-way tape. Same class.
  NON-DETERMINISM          -> breadth-first search the
      computation tree on a deterministic machine.
      EXPONENTIAL slowdown. SAME CLASS.
  RANDOM ACCESS            -> simulate addressing by
      scanning. Polynomial slowdown. Same class.
  A STACK INSTEAD OF A TAPE -> NOT the same class. That is
      Module 03, and it is strictly weaker.
  TWO STACKS               -> same class as one tape, which
      is a pleasant surprise.
  TWO COUNTERS             -> ALSO the same class (Minsky).
      Astonishing, and true.

  SO THE CLASS OF COMPUTABLE FUNCTIONS IS ROBUST to every
  reasonable change in the model, and only the TIME changes.

  WHICH IS WHY THIS COURSE AND CSCE 637 DIVIDE WHERE THEY
  DO: computability is model-independent, so it can be
  settled; complexity is model-sensitive, so it needs
  care -- and the non-determinism row is exactly where P vs
  NP lives.
""",
   "caption": "<b>Robustness is what makes the definition "
              "trustworthy</b> — a notion that changed under "
              "reformulation would not be worth proving things about.",
   "note": "The two-counters result is worth stating; it is "
           "genuinely surprising."},

  {"t": "section", "label": "Part 2", "title": "Two kinds of yes",
   "blurb": "The distinction everything in Module 05 rests on."},

  {"t": "table", "kicker": "The distinction", "title": "Decidable against recognisable",
   "header": ["", "Decidable", "Turing-recognisable"],
   "widths": [2.3, 4.4, 5.3],
   "rows": [
     ["<b>On a yes</b>", "<b>Halts and accepts</b>", "<b>Halts and accepts</b>"],
     ["<b>On a no</b>", "<b>Halts and rejects</b>", "<b>May run forever</b>"],
     ["<b>Also called</b>", "<b>Recursive; total</b>", "<b>Semi-decidable; recursively enumerable</b>"],
     ["<b>Closed under complement</b>", "<b>Yes</b>", "<b>NO — and that asymmetry is the key</b>"],
     ["<b>Example</b>", "<b>Primality, regular-language membership</b>", "<b>Halting, provability, Diophantine solvability</b>"],
   ],
   "footnote": "<b>The asymmetry is the whole subject:</b> <b>L and its "
               "complement both recognisable implies L decidable</b> "
               "— run both, one must halt — which is "
               "Module 05's main tool.",
   "note": "That one theorem does most of the work in Modules 05-07."},

  {"t": "callout", "title": "Recognisable means 'verifiable when the answer is yes'",
   "kind": "The useful intuition",
   "body": ["<b>A language is recognisable exactly when its members "
            "have finite certificates you can check.</b> 'This program "
            "halts' is witnessed by its halting computation.",
            "<b>So recognisable is the enumerable class:</b> you can "
            "list the members, in some order, eventually printing every "
            "one — <b>and never know whether a particular absent item "
            "is absent or merely late.</b>",
            "<b>That is why it is also called recursively "
            "enumerable</b>, and the enumeration view is frequently the "
            "easier one for proofs.",
            "<b>And the parallel with CSCE 637's NP is exact in "
            "form:</b> <b>NP is 'verifiable in polynomial time given a "
            "short certificate'; recognisable is 'verifiable "
            "eventually'</b> — the same structure with the resource "
            "bound removed."]},

  {"t": "section", "label": "Part 3", "title": "Universality",
   "blurb": "A machine that runs machines."},

  {"t": "callout", "title": "The universal machine is the idea that made computers possible",
   "kind": "And it was a theorem first",
   "body": ["<b>Encode a Turing machine as a string.</b> Then there is "
            "a single machine U that, given the encoding of M and an "
            "input w, simulates M on w.",
            "<b>So one fixed machine can do what any machine does</b>, "
            "given its description as data — which is the "
            "stored-program computer, stated as a theorem in 1936.",
            "<b>The encoding is what makes it possible</b>, and it is "
            "also what makes Module 05 possible: <b>once programs are "
            "data, a program can take itself as input</b>, which is "
            "where diagonalisation comes from.",
            "<b>And it means the halting problem is about a "
            "<i>language</i></b> — the set of encoded (M, w) pairs "
            "where M halts on w — <b>which is what lets the "
            "mathematics proceed.</b>"]},

  {"t": "code", "kicker": "Encoding", "title": "Why 'programs are data' is load-bearing",
   "lang": "text", "code": """
  A Turing machine is a finite object: a state set, an
  alphabet, and a transition table. So it can be written
  down as a string.

  THREE CONSEQUENCES, EACH ESSENTIAL:

  1. THE UNIVERSAL MACHINE exists -- one machine simulating
     any other from its description. The stored-program
     computer, proved before it was built.

  2. SELF-REFERENCE becomes available. A machine can be
     given ITS OWN description as input. Not a paradox and
     not a trick: just a string being passed to a program.
     -- This is where Module 05's diagonalisation and
        Module 09's recursion theorem both come from.

  3. PROPERTIES OF PROGRAMS BECOME LANGUAGES. "Does M halt
     on w?" is membership in a set of strings, so the whole
     apparatus of Modules 02-03 applies to questions ABOUT
     PROGRAMS.
     -- Which is what makes Module 06's reductions possible
        and Module 08's results about real tools meaningful.

  ALL THREE DEPEND ON ONE OBSERVATION: a program is a finite
  object, so it is a string. Everything after this module
  rests on it.
""",
   "caption": "<b>Programs-as-data is the hinge of the whole "
              "course</b> — and it is also why your compiler is a "
              "program that reads programs.",
   "note": "Students underestimate how much depends on the encoding."},

  {"t": "section", "label": "Part 4", "title": "Counting",
   "blurb": "An easy argument that most things are uncomputable."},

  {"t": "callout", "title": "Almost all functions are uncomputable, by counting",
   "kind": "The cheapest impossibility proof there is",
   "body": ["<b>There are countably many Turing machines</b>, because "
            "each is a finite string over a finite alphabet.",
            "<b>And there are uncountably many functions from strings "
            "to {0,1}</b>, by Cantor's diagonal argument.",
            "<b>So almost every such function is not computed by any "
            "machine.</b> <b>The computable functions are a measure-zero "
            "fragment of all functions.</b>",
            "<b>Which proves that uncomputable functions exist and "
            "names none of them.</b> <b>Module 05's contribution is a "
            "<i>specific</i>, natural, important uncomputable "
            "problem</b> — and that is much harder and much more "
            "useful than this counting argument."]},

  {"t": "bullets", "kicker": "Summary", "title": "What this module establishes",
   "items": [
     "<b>A simple model computes everything computable</b>, and every "
     "reasonable variant computes the same class.",
     "",
     "<b>So the class is robust</b>, which is what makes "
     "impossibility proofs about it worth having.",
     "",
     "<b>Decidable and recognisable are different</b>, and the "
     "complement asymmetry between them is Module 05's main tool.",
     "",
     "<b>Programs are data, so programs can be inputs</b> — "
     "which makes self-reference and the universal machine both "
     "available.",
     "",
     "<b>And uncomputable functions exist for cheap</b>, while "
     "finding an <i>interesting</i> one is Module 05's job.",
   ],
   "footnote": "<b>Everything from here uses the encoding.</b> If one "
               "thing from this module should stick, it is that a program "
               "is a finite object and therefore a string."},
 ],
 "takeaways": [
   "A Turing machine is a finite control plus unbounded rewritable memory, "
   "designed to model a person computing with paper.",
   "Every reasonable variant computes the same class and only the time "
   "changes — which is why computability is settled and complexity is "
   "not.",
   "Decidable halts on every input; recognisable may run forever on a no "
   "— and the complement asymmetry is the key tool.",
   "If a language and its complement are both recognisable, the language "
   "is decidable — run both and one must halt.",
   "Programs are finite objects and therefore strings, which gives the "
   "universal machine, self-reference, and properties-as-languages.",
   "Uncomputable functions exist by a one-line counting argument; finding "
   "an interesting one is much harder and is Module 05's contribution.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The model and its robustness"),
  ("callout", "A Turing machine is a finite automaton with unbounded, "
              "rewritable memory",
   ["<b>An infinite tape, a head that reads and writes a single cell and "
    "moves one step left or right, and a finite control.</b> That is the "
    "entire model, and its simplicity is deliberate.",
    "<b>The finite control is the program and the tape is the "
    "memory</b> — so the machine has a <i>fixed-size description</i> "
    "and <i>unbounded working space</i>, which is exactly the situation of "
    "a real computer and is what makes the model a reasonable idealisation "
    "rather than an arbitrary one.",
    "<b>Turing designed it to model a person computing with paper and "
    "pencil</b>, and section 9 of his 1936 paper is an argument about what "
    "such a person can do — finitely many states of mind, a bounded "
    "number of symbols attended to at once, local changes. <b>That "
    "argument, rather than any mathematical result, is why the "
    "Church–Turing thesis is credible</b> (Module 01 &sect;2).",
    "<b>And the model is deliberately inefficient.</b> <b>It is a tool "
    "for proving what is possible, not for computing</b> — which is "
    "why its <i>polynomial-time</i> class is meaningful (CSCE 637's "
    "subject, since polynomial-time is robust across models) and its "
    "constants and small-degree polynomials are not."]),
  ("code", """MULTIPLE TAPES            -> simulate on one tape with the
    tracks interleaved. Quadratic slowdown. SAME CLASS.
TWO-WAY INFINITE TAPE     -> fold it in half and store both
    halves interleaved on a one-way tape. SAME CLASS.
NON-DETERMINISM           -> breadth-first search the
    computation tree on a deterministic machine.
    EXPONENTIAL slowdown. SAME CLASS.
RANDOM ACCESS             -> simulate addressing by
    scanning for the address. Polynomial slowdown.
    SAME CLASS.
A STACK INSTEAD OF A TAPE -> NOT the same class. That is
    Module 03, and it is strictly weaker.
TWO STACKS                -> same class as one tape, which
    is a pleasant surprise (one stack for each side of
    the head).
TWO COUNTERS              -> ALSO the same class (Minsky),
    with only increment, decrement and test-for-zero.
    Astonishing, and true.

SO THE CLASS OF COMPUTABLE FUNCTIONS IS ROBUST under every
reasonable change to the model, and only the TIME changes.

WHICH IS WHY THIS COURSE AND CSCE 637 DIVIDE WHERE THEY DO:
computability is model-independent, so it can be settled
once; complexity is model-sensitive, so it needs care about
which model -- and the NON-DETERMINISM row above is exactly
where P vs NP lives."""),
  ("p", "<b>Robustness is what makes the definition trustworthy.</b> "
        "<b>A notion of computability that changed when you added a "
        "second tape would not be worth proving theorems about</b>, "
        "because the theorems would be about the formalism rather than "
        "about computation. <b>The fact that it does not change is the "
        "second pillar of the Church–Turing thesis</b>, alongside "
        "Module 01's independent-formalisation argument."),

  ("h1", "2 &nbsp; Decidable and recognisable"),
  ("table", ["", "Decidable", "Turing-recognisable"],
   [["<b>On an input in the language</b>", "<b>Halts and accepts.</b>",
     "<b>Halts and accepts.</b>"],
    ["<b>On an input not in the language</b>",
     "<b>Halts and rejects.</b>",
     "<b>May run forever without ever answering.</b>"],
    ["<b>Also called</b>", "<b>Recursive; total; solvable.</b>",
     "<b>Semi-decidable; recursively enumerable; computably "
     "enumerable.</b>"],
    ["<b>Closed under complement</b>", "<b>Yes</b> — swap the "
     "answers.",
     "<b>NO — and that asymmetry is the key to the whole "
     "subject.</b>"],
    ["<b>Examples</b>",
     "<b>Primality; membership in a regular or context-free "
     "language.</b>",
     "<b>Halting; provability in a formal system; whether a Diophantine "
     "equation has a solution.</b>"]],
   [0.24, 0.33, 0.43]),
  ("p", "<b>The asymmetry is the whole subject, and one theorem carries "
        "most of the weight:</b> <b>if a language and its complement are "
        "both Turing-recognisable, then the language is decidable.</b> "
        "The proof is one line — run both recognisers in parallel, "
        "and since every input is in one or the other, one of them must "
        "eventually halt and accept, which tells you the answer. "
        "<b>Module 05 uses this to deduce that the complement of the "
        "halting problem is not even recognisable</b>, and Module 07 "
        "builds the whole hierarchy on it."),
  ("callout", "Recognisable means 'verifiable when the answer is yes'",
   ["<b>A language is recognisable exactly when its members have finite "
    "certificates that can be checked.</b> 'This program halts on this "
    "input' is witnessed by the halting computation itself — a finite "
    "object you can verify step by step.",
    "<b>So recognisable is the <i>enumerable</i> class:</b> you can "
    "write a program that lists the members, in some order, eventually "
    "printing every one — <b>and you can never tell whether a "
    "particular item that has not appeared is absent or merely late.</b> "
    "That is precisely the content of 'may run forever'.",
    "<b>Which is why it is also called recursively enumerable</b>, and "
    "<b>the enumeration view is frequently the easier one for "
    "proofs</b> — showing a language is recognisable by exhibiting "
    "an enumerator is often simpler than designing a recogniser.",
    "<b>And the parallel with CSCE 637's NP is exact in form:</b> "
    "<b>NP is 'verifiable in polynomial time given a short certificate'; "
    "recognisable is 'verifiable eventually, given any finite "
    "certificate'</b> — <b>the same structure with the resource "
    "bound removed.</b> <b>Which is why the two courses' central "
    "distinctions feel similar, and why 'is checking easier than finding' "
    "is the question in both.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Universality and encoding"),
  ("callout", "The universal machine is the idea that made computers "
              "possible",
   ["<b>Encode a Turing machine as a string</b> — its states, "
    "alphabet, and transition table are a finite object, so this is "
    "routine. <b>Then there is a single machine U which, given the "
    "encoding of M together with an input w, simulates M on w.</b>",
    "<b>So one fixed machine can do whatever any machine does, given "
    "that machine's description as data</b> — <b>which is the "
    "stored-program computer, stated and proved as a theorem in "
    "1936</b>, a decade before one was built. The architecture followed "
    "the theorem rather than the reverse.",
    "<b>The encoding is what makes it possible</b>, and it is also what "
    "makes Module 05 possible: <b>once programs are data, a program can "
    "be given its own description as input</b>, which is where "
    "diagonalisation comes from and is not a trick.",
    "<b>And it means the halting problem is a question about a "
    "<i>language</i></b> — the set of encoded pairs (M, w) such that "
    "M halts on w — <b>which is what lets the mathematics of "
    "Modules 02 and 03 apply to questions about programs.</b> Without "
    "the encoding there would be nothing to prove theorems about."]),
  ("code", """A Turing machine is a finite object: a state set, an
alphabet, and a transition table. So it can be written down
as a string.

THREE CONSEQUENCES, EACH ESSENTIAL TO WHAT FOLLOWS:

1. THE UNIVERSAL MACHINE exists -- one machine simulating
   any other from its description. The stored-program
   computer, proved before it was built.

2. SELF-REFERENCE becomes available. A machine can be given
   ITS OWN description as input. This is not a paradox and
   not a trick: it is a string being passed to a program,
   which happens every time you run a compiler on its own
   source.
   -- Module 05's diagonalisation and Module 09's recursion
      theorem both come from here.

3. PROPERTIES OF PROGRAMS BECOME LANGUAGES. "Does M halt on
   w?" is membership in a set of strings, so the entire
   apparatus of Modules 02 and 03 applies to questions
   ABOUT PROGRAMS.
   -- Which is what makes Module 06's reductions possible,
      and Module 08's results about real tools meaningful.

ALL THREE DEPEND ON ONE OBSERVATION: a program is a finite
object, so it is a string. Everything after this module
rests on it."""),

  ("h1", "4 &nbsp; Counting, and what it does not give you"),
  ("callout", "Almost all functions are uncomputable, by counting",
   ["<b>There are countably many Turing machines</b>, because each is "
    "describable by a finite string over a finite alphabet, and the finite "
    "strings over a finite alphabet are countable.",
    "<b>And there are uncountably many functions from strings to "
    "{0,1}</b>, by Cantor's diagonal argument — there are as many as "
    "there are subsets of a countable set.",
    "<b>So almost every such function is computed by no machine "
    "whatsoever.</b> <b>The computable functions are a vanishingly small "
    "fragment of all functions</b>, and this takes two lines to "
    "establish.",
    "<b>Which proves that uncomputable functions exist and names "
    "none of them.</b> <b>Module 05's contribution is a <i>specific</i>, "
    "natural, and practically important uncomputable problem</b> — "
    "<b>and that is much harder and much more useful than this counting "
    "argument.</b> The distinction is worth holding: an existence proof "
    "by counting tells you nothing about which problems are affected, and "
    "the whole value of Modules 05 through 08 is that they identify the "
    "problems you actually care about."]),
  ("ul", ["<b>A simple model computes everything computable</b>, and "
          "every reasonable variant computes the same class (&sect;1).",
          "<b>So the class is robust</b>, which is what makes "
          "impossibility proofs about it worth having rather than being "
          "artefacts of a formalism.",
          "<b>Decidable and recognisable are genuinely different</b>, "
          "and <b>the complement asymmetry between them is Module 05's "
          "main tool</b> (&sect;2).",
          "<b>Programs are data, so programs can be inputs</b> — "
          "which makes self-reference and the universal machine both "
          "available, and both are needed (&sect;3).",
          "<b>And uncomputable functions exist for the price of a "
          "counting argument</b>, while <b>finding an <i>interesting</i> "
          "one is Module 05's job</b>. <b>If one thing from this module "
          "should stick, it is that a program is a finite object and "
          "therefore a string</b> — everything from here uses it."]),
 ],
 "resources": [
   ("Sipser &mdash; chapter 3",
    "https://math.mit.edu/~sipser/book.html",
    "<b>The machine, the variants of &sect;1, and the "
    "decidable/recognisable distinction of &sect;2.</b>"),
   ("Turing &mdash; On Computable Numbers, sections 1–7 and 9 "
    "(free)",
    "https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf",
    "<b>The model and the universal machine of &sect;3, in the "
    "original</b>, plus the section 9 argument that justifies the "
    "whole enterprise."),
   ("Minsky &mdash; Computation: Finite and Infinite Machines",
    "https://dl.acm.org/doi/book/10.5555/1095587",
    "<b>&sect;1's two-counter result</b>, and the clearest treatment of "
    "the minimal models. Library copy."),
   ("MIT 18.404J &mdash; lectures 5–7 (free)",
    "https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/",
    "<b>This module lectured</b>, with the encoding discussion of "
    "&sect;3 made careful."),
 ],
 "exercises": [
   "<b>Implement a Turing machine simulator</b> and run a machine that "
   "decides aⁿbⁿ.",
   "<b>Write a machine that adds two binary numbers</b> and trace it on a "
   "small input.",
   "<b>Implement a two-tape machine and simulate it on one tape</b>, and "
   "measure the slowdown.",
   "<b>Simulate a non-deterministic machine deterministically</b> and "
   "report the blow-up.",
   "<b>Design an encoding of Turing machines as strings</b> and write a "
   "decoder.",
   "<b>Implement a universal machine</b> that runs an encoded machine on "
   "an encoded input.",
   "<b>Feed a machine its own encoding</b> and confirm nothing "
   "paradoxical happens.",
   "<b>Give an example of a recognisable language that is not "
   "decidable</b>, and say why your recogniser may not halt.",
   "<b>Prove the complement theorem of &sect;2</b> in your own words.",
   "<b>Write out the counting argument</b> and state exactly what it "
   "does and does not establish.",
 ],
 "selfcheck": [
   "Define a Turing machine and say what Turing designed it to model.",
   "Name six variants and whether each changes the class.",
   "Which row is P versus NP, and why does that divide the courses?",
   "Distinguish decidable from recognisable on five axes.",
   "State and prove the complement theorem.",
   "What does recognisable mean intuitively, and what is the NP "
   "parallel?",
   "What is the universal machine, and what did it establish?",
   "Give the three consequences of encoding programs as strings.",
   "Give the counting argument and say what it fails to provide.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Undecidability",
 "subtitle": "The halting problem, proved.",
 "question": "Is there something no program can decide?",
 "outcomes": [
     "Prove the halting problem undecidable by diagonalisation.",
     "Explain the self-reference and why it is not a trick.",
     "Prove that the complement of halting is not recognisable.",
     "Explain the diagonal method in general.",
     "State precisely what the result forbids.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The proof",
   "blurb": "Four lines, and they are the most important four in the "
            "subject."},

  {"t": "code", "kicker": "The proof", "title": "The halting problem is undecidable",
   "lang": "text", "code": """
  HALT = { (M, w) : machine M halts on input w }

  Suppose H decides HALT. Then build D:

      D(X):                       # X is a machine encoding
          if H(X, X) says "halts":
              loop forever
          else:
              halt

  D takes a machine description and does the OPPOSITE of
  what that machine does on its own description.

  NOW RUN D ON ITS OWN DESCRIPTION, D(D):

      if D halts on D, then H(D,D) says "halts",
          so D loops forever.      CONTRADICTION.
      if D does not halt on D, then H(D,D) says "loops",
          so D halts.              CONTRADICTION.

  Both branches contradict. So D cannot exist. But D was
  built from H by an entirely mechanical construction --
  an if-statement and a loop. So H cannot exist.

  THEREFORE HALT IS UNDECIDABLE.

  THAT IS THE WHOLE PROOF. Four lines of construction and
  two cases.
""",
   "caption": "<b>Note where the impossibility lands:</b> D is "
              "unobjectionable code, so the contradiction falls on H "
              "— which is the step to be sure of.",
   "note": "Walk through why the contradiction blames H rather than D."},

  {"t": "callout", "title": "The self-reference is not a trick",
   "kind": "The objection, answered",
   "body": ["<b>D is given its own description as a string.</b> That is "
            "not a paradox — <b>it is Module 04 §3's "
            "encoding, used exactly as intended.</b>",
            "<b>You do this routinely:</b> a compiler compiling its own "
            "source, a diff of a file against itself, a hash of an "
            "executable. <b>Nothing unusual is happening.</b>",
            "<b>And the construction of D from H is mechanical</b> "
            "— if H existed as a program, D would be a twenty-line "
            "wrapper around it. <b>No cleverness is required to build "
            "D.</b>",
            "<b>Which is why the contradiction must fall on H.</b> "
            "<b>D's existence follows from H's by construction, and D "
            "cannot exist, so H cannot</b> — and that logical shape is "
            "what the proof actually is."]},

  {"t": "section", "label": "Part 2", "title": "The consequence",
   "blurb": "Recognisable but not decidable."},

  {"t": "callout", "title": "HALT is recognisable, and its complement is not",
   "kind": "Where the asymmetry shows up",
   "body": ["<b>HALT is recognisable:</b> simulate M on w. If it halts, "
            "accept. <b>If it never halts, run forever</b> — which "
            "is permitted for a recogniser.",
            "<b>So HALT is recognisable and not decidable</b>, which "
            "shows the two classes genuinely differ "
            "(Module 04 §2).",
            "<b>And the complement of HALT is not even "
            "recognisable</b> — because if it were, then by "
            "Module 04 §2's theorem HALT would be decidable, "
            "and it is not.",
            "<b>So 'M does not halt on w' has no finite "
            "certificate.</b> <b>There is nothing you could be shown "
            "that would verify non-termination in general</b> — which "
            "is a much stronger and more unsettling statement than "
            "undecidability alone."]},

  {"t": "table", "kicker": "Landscape", "title": "Where things sit",
   "header": ["Language", "Status", "Why"],
   "widths": [3.0, 3.6, 5.3],
   "rows": [
     ["<b>HALT</b>", "<b>Recognisable, undecidable</b>", "<b>Simulate; may not terminate</b>"],
     ["<b>Complement of HALT</b>", "<b>Not recognisable</b>", "<b>Else HALT decidable</b>"],
     ["<b>Aₜₘ (M accepts w)</b>", "<b>Recognisable, undecidable</b>", "<b>Same proof</b>"],
     ["<b>Eₜₘ (M accepts nothing)</b>", "<b>Not recognisable</b>", "<b>Needs all inputs to fail</b>"],
     ["<b>EQₜₘ (M₁ = M₂)</b>", "<b>Neither it nor its complement</b>", "<b>Harder than halting (M07)</b>"],
   ],
   "footnote": "<b>Equivalence of programs is harder than halting</b>, "
               "which Module 07's hierarchy makes precise — "
               "undecidable is not one level but infinitely many.",
   "note": "The EQ row previews the hierarchy and is worth flagging."},

  {"t": "section", "label": "Part 3", "title": "The method",
   "blurb": "Diagonalisation, in general."},

  {"t": "callout", "title": "Diagonalisation: build the thing that differs from everything in the list",
   "kind": "One technique, several famous theorems",
   "body": ["<b>Cantor:</b> given a list of reals, construct one "
            "differing from the nth in the nth digit. <b>So the reals "
            "are uncountable.</b>",
            "<b>Halting:</b> given a decider, construct a machine "
            "differing from what the decider predicts about it. <b>So no "
            "decider exists.</b>",
            "<b>Gödel:</b> given a proof system, construct a "
            "sentence asserting its own unprovability "
            "(Module 10).",
            "<b>Russell, the time hierarchy theorem, Rice's theorem, "
            "the undecidability of first-order "
            "validity</b> — <b>all the same method</b>: assume an "
            "enumeration, construct the element it misses."]},

  {"t": "section", "label": "Part 4", "title": "What it forbids",
   "blurb": "Precisely, and no more."},

  {"t": "bullets", "kicker": "Reading", "title": "What the halting theorem actually says",
   "items": [
     "<b>No single program decides halting for all (program, input) "
     "pairs.</b> That is the claim, exactly.",
     "",
     "<b>It does not say your program's termination is "
     "unknowable.</b> <b>Most are easy</b> — and tools that "
     "handle the easy cases are valuable (Module 12).",
     "",
     "<b>It does not forbid a partial decider</b> that answers yes, "
     "no, or 'do not know'. <b>Every termination checker is one.</b>",
     "",
     "<b>It does not forbid deciding halting for a restricted "
     "class</b> — primitive recursive programs, total functional "
     "languages, bounded loops.",
     "",
     "<b>And it does not depend on the machine model</b> "
     "(Module 04 §1), so no hardware or language escapes it.",
   ],
   "footnote": "<b>'Undecidable' is about the universal quantifier.</b> "
               "Every practical response in Module 12 works by weakening "
               "it — fewer inputs, or a third answer."},

  {"t": "callout", "title": "Why this is the most important result in the program",
   "kind": "Closing the module",
   "body": ["<b>Everything else you have learned could be "
            "superseded.</b> A better algorithm, a bigger model, a new "
            "architecture.",
            "<b>This cannot.</b> <b>It is a proof that no program "
            "exists, and it is as true in a century as it is now.</b>",
            "<b>And it has immediate practical content:</b> "
            "<b>Module 06 turns it into undecidability for almost every "
            "interesting property of programs</b>, and Module 08 finds "
            "those properties in tools you use daily.",
            "<b>So this is not philosophy.</b> <b>It is the reason your "
            "type checker rejects valid programs and your optimiser "
            "misses valid optimisations</b> — and knowing that is the "
            "difference between being surprised and being correct."]},
 ],
 "takeaways": [
   "The halting problem's proof is four lines of construction and two "
   "cases, and the contradiction falls on the decider because the "
   "contradictory machine is built from it mechanically.",
   "The self-reference is not a trick — it is a program being given a "
   "string, which happens whenever a compiler compiles itself.",
   "HALT is recognisable and undecidable, which shows the two classes "
   "genuinely differ.",
   "The complement of HALT is not even recognisable, so non-termination "
   "has no finite certificate at all.",
   "Diagonalisation is one method behind Cantor, halting, Gödel, "
   "Rice, and the time hierarchy theorem: assume an enumeration, construct "
   "what it misses.",
   "The theorem is about the universal quantifier, and every practical "
   "response weakens it — fewer inputs, or a third answer.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The proof"),
  ("code", """HALT = { (M, w) : machine M halts on input w }

Suppose H decides HALT. Then build D:

    D(X):                     # X is a machine encoding
        if H(X, X) says "halts":
            loop forever
        else:
            halt

D takes a machine description and does the OPPOSITE of what
that machine does when run on its own description.

NOW RUN D ON ITS OWN DESCRIPTION, D(D):

    if D halts on D, then H(D,D) says "halts",
        so by D's code D loops forever.   CONTRADICTION.
    if D does not halt on D, then H(D,D) says "loops",
        so by D's code D halts.           CONTRADICTION.

Both branches contradict. So D cannot exist. But D was
built from H by an entirely mechanical construction -- one
call, one if-statement, and one loop. So H cannot exist.

THEREFORE HALT IS UNDECIDABLE.

That is the whole proof: four lines of construction and two
cases."""),
  ("p", "<b>Note carefully where the impossibility lands.</b> <b>D is "
        "unobjectionable code</b> — a function call, a conditional, "
        "and a loop — <b>so the contradiction cannot be blamed on "
        "D</b>. <b>It falls on H</b>, the only assumed object in the "
        "argument. <b>That is the step to be certain of</b>, and it is "
        "where most first readings go wrong: the proof is not showing that "
        "self-reference is paradoxical, it is showing that <i>if H existed "
        "then a contradictory program would exist</i>, and therefore H "
        "does not."),
  ("callout", "The self-reference is not a trick",
   ["<b>D is given its own description as a string.</b> That is not a "
    "paradox and not sleight of hand — <b>it is Module 04 "
    "&sect;3's encoding, used exactly as intended.</b>",
    "<b>You do this routinely.</b> A compiler compiling its own source "
    "code; a diff of a file against itself; a hash of an executable "
    "computed by a program in that executable; a program printing its own "
    "source. <b>Nothing unusual is happening</b>, and the discomfort is "
    "unfamiliarity rather than a logical difficulty.",
    "<b>And the construction of D from H is mechanical.</b> <b>If H "
    "existed as a program, D would be a twenty-line wrapper around "
    "it</b> — <b>no cleverness, no insight, and no appeal to "
    "anything exotic is required to build D.</b> Which is precisely the "
    "property the proof needs.",
    "<b>Which is why the contradiction must fall on H.</b> <b>D's "
    "existence follows from H's by construction; D cannot exist; "
    "therefore H cannot</b> — <b>and that logical shape is what the "
    "proof actually is</b>, underneath the self-reference that draws all "
    "the attention."]),

  ("h1", "2 &nbsp; The consequences"),
  ("callout", "HALT is recognisable, and its complement is not",
   ["<b>HALT is recognisable:</b> simulate M on w using the universal "
    "machine (Module 04 &sect;3). If the simulation halts, accept. "
    "<b>If M never halts, the recogniser runs forever</b> — which is "
    "exactly what a recogniser is permitted to do.",
    "<b>So HALT is recognisable and not decidable</b>, which <b>proves "
    "that the two classes of Module 04 &sect;2 genuinely differ</b> and "
    "is the first witness to that distinction.",
    "<b>And the complement of HALT is not even recognisable.</b> The "
    "argument is one line: if it were, then HALT and its complement would "
    "both be recognisable, so by Module 04 &sect;2's theorem HALT "
    "would be decidable — and &sect;1 proved it is not.",
    "<b>So 'M does not halt on w' has no finite certificate.</b> "
    "<b>There is nothing that could be shown to you which would verify "
    "non-termination in general</b> — no proof, no trace, no "
    "invariant, nothing of finite size that works for every "
    "non-terminating program. <b>Which is a substantially stronger and "
    "more unsettling statement than undecidability alone</b>, and it is "
    "why proving termination is harder than proving almost anything "
    "else."]),
  ("table", ["Language", "Status", "Why"],
   [["<b>HALT</b>", "<b>Recognisable, undecidable.</b>",
     "<b>Simulate; the simulation may not terminate.</b>"],
    ["<b>The complement of HALT</b>", "<b>Not recognisable.</b>",
     "<b>Otherwise HALT would be decidable</b> (the callout)."],
    ["<b>A<sub>TM</sub> — does M accept w?</b>",
     "<b>Recognisable, undecidable.</b>",
     "<b>The same proof</b>, and this is the version Sipser uses."],
    ["<b>E<sub>TM</sub> — does M accept nothing at all?</b>",
     "<b>Not recognisable.</b>",
     "<b>A yes requires <i>every</i> input to fail</b>, which is an "
     "infinite condition with no finite witness."],
    ["<b>EQ<sub>TM</sub> — do M<sub>1</sub> and M<sub>2</sub> accept "
     "the same language?</b>",
     "<b>Neither it nor its complement is recognisable.</b>",
     "<b>Strictly harder than halting</b>, which Module 07's hierarchy "
     "makes precise — <b>'undecidable' is not one level but "
     "infinitely many.</b>"]],
   [0.26, 0.28, 0.46]),

  ("break",),
  ("h1", "3 &nbsp; Diagonalisation as a method"),
  ("callout", "Diagonalisation: build the thing that differs from "
              "everything in the list",
   ["<b>Cantor:</b> given a purported list of all real numbers, "
    "construct one that differs from the nth in the nth decimal digit. "
    "<b>It is not on the list, so no such list exists, so the reals are "
    "uncountable.</b>",
    "<b>Halting:</b> given a purported decider, construct a machine that "
    "differs from whatever the decider predicts about it. <b>So no such "
    "decider exists.</b> &sect;1 is Cantor's argument with programs in "
    "place of digits.",
    "<b>G&ouml;del:</b> given a formal proof system, construct a "
    "sentence asserting its own unprovability (Module 10) — the "
    "same construction, with provability in place of halting.",
    "<b>Russell's paradox, the time and space hierarchy theorems</b> "
    "(CSCE 637), <b>Rice's theorem</b> (Module 06), <b>and the "
    "undecidability of first-order validity are all the same "
    "method</b>: <b>assume an enumeration, and construct the element it "
    "misses.</b> <b>Learning it once is learning a large fraction of "
    "theoretical computer science</b>, which is why &sect;1 is worth "
    "reconstructing from memory rather than merely reading."]),

  ("h1", "4 &nbsp; What the theorem forbids"),
  ("ul", ["<b>No single program decides halting for all (program, input) "
          "pairs.</b> <b>That is the claim, exactly</b>, and nothing "
          "more follows from it than that.",
          "<b>It does not say that your program's termination is "
          "unknowable.</b> <b>Most programs are easy</b> — a loop "
          "with a decrementing bounded counter obviously terminates, and "
          "<b>a tool that handles the easy cases is genuinely valuable</b> "
          "(Module 12 &sect;1).",
          "<b>It does not forbid a partial decider</b> that answers yes, "
          "no, or 'I cannot determine this'. <b>Every termination checker "
          "and every static analyser is one of these</b>, and the third "
          "answer is what buys decidability.",
          "<b>It does not forbid deciding halting for a restricted class "
          "of programs</b> — primitive recursive functions "
          "(Module 09 &sect;1), total functional languages, programs "
          "whose loops have statically bounded counts. <b>All decidable, "
          "by construction</b>, which is Module 12 &sect;2's other "
          "engineering response.",
          "<b>And it does not depend on the machine model</b> "
          "(Module 04 &sect;1), <b>so no programming language, no "
          "hardware, and no future architecture escapes it</b> — "
          "including quantum (Module 11 &sect;4). <b>'Undecidable' is "
          "about the universal quantifier</b>, and <b>every practical "
          "response in Module 12 works by weakening it</b>: fewer "
          "inputs, or a third answer."]),
  ("callout", "Why this is the most important result in the program",
   ["<b>Everything else in this program could be superseded.</b> A "
    "better algorithm, a larger model, a new architecture, a faster "
    "renderer — all of it is contingent on the state of the art.",
    "<b>This cannot be.</b> <b>It is a proof that no program exists, and "
    "it will be as true in a century as it is now</b> — which is a "
    "kind of claim nothing else in twenty-two courses has made.",
    "<b>And it has immediate practical content.</b> <b>Module 06 turns "
    "it into undecidability for almost every interesting property of "
    "programs</b> (Rice's theorem), <b>and Module 08 finds those "
    "properties in tools you use daily.</b>",
    "<b>So this is not philosophy.</b> <b>It is the reason your type "
    "checker rejects programs that would have worked, your optimiser "
    "misses optimisations that were valid, and your race detector reports "
    "races that cannot occur</b> — <b>and knowing that is the "
    "difference between being surprised by your tools and understanding "
    "them.</b>"]),
 ],
 "resources": [
   ("Sipser &mdash; chapter 4",
    "https://math.mit.edu/~sipser/book.html",
    "<b>The diagonalisation argument and the undecidability of "
    "A<sub>TM</sub></b>, with the countability preliminaries of "
    "Module 04 &sect;4."),
   ("MIT 18.404J &mdash; lectures 8–9 (free)",
    "https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/",
    "<b>Sipser proving this himself</b>, which is worth watching even if "
    "you have read the chapter."),
   ("Turing &mdash; On Computable Numbers, section 8 (free)",
    "https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf",
    "<b>The original undecidability argument</b>, framed in terms of "
    "circle-free machines rather than halting."),
   ("Hofstadter &mdash; Gödel, Escher, Bach",
    "https://www.basicbooks.com/titles/douglas-r-hofstadter/godel-escher-bach/9780465026562/",
    "<b>&sect;3's method, explored at length and informally</b> — "
    "not a textbook, and a good companion to Module 10."),
 ],
 "exercises": [
   "<b>Write the halting proof out from memory</b> and check it against "
   "the text.",
   "<b>Identify exactly which step requires the encoding</b> of "
   "Module 04.",
   "<b>Explain to someone else why the contradiction blames H and not "
   "D</b>, and note where they object.",
   "<b>Implement a partial halting checker</b> that answers yes, no, or "
   "unknown, and run it on ten programs.",
   "<b>Report how many it could decide</b>, and construct one it "
   "cannot.",
   "<b>Write a recogniser for HALT</b> and demonstrate it running "
   "forever on a non-halting input.",
   "<b>Prove the complement of HALT is not recognisable</b>, in your own "
   "words.",
   "<b>Write out Cantor's diagonal argument</b> and map each step onto "
   "the halting proof.",
   "<b>State the halting theorem precisely</b>, then write four things it "
   "does not say.",
   "<b>Find a programming language in which all programs terminate</b> "
   "and explain what it gave up.",
 ],
 "selfcheck": [
   "Give the halting proof in full.",
   "Why does the contradiction fall on H?",
   "Why is the self-reference not a trick?",
   "Why is HALT recognisable?",
   "Prove its complement is not recognisable.",
   "What does it mean that non-termination has no finite certificate?",
   "Place five languages in the landscape table.",
   "State the diagonalisation method and name four theorems that use "
   "it.",
   "Give five things the halting theorem does not forbid.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Reductions",
 "subtitle": "One hard problem becomes many.",
 "question": "How do you prove a <i>new</i> problem undecidable?",
 "outcomes": [
     "Define a mapping reduction and state what it preserves.",
     "Get the direction right, which is where attempts fail.",
     "Construct reductions proving several problems undecidable.",
     "State and apply Rice's theorem.",
     "Explain the relationship to NP-hardness reductions.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The technique",
   "blurb": "Transform instances, and transfer the impossibility."},

  {"t": "callout", "title": "A reduction transforms instances, and the direction is everything",
   "kind": "Get this right and the rest is mechanical",
   "body": ["<b>A mapping reduction from A to B is a computable "
            "function f with x ∈ A if and only if f(x) ∈ "
            "B.</b> Write A ≤ B.",
            "<b>If A ≤ B and B is decidable, then A is "
            "decidable</b> — transform and ask. <b>So "
            "contrapositively, if A is undecidable then so is B.</b>",
            "<b>So to prove B undecidable, reduce a known undecidable "
            "problem TO it.</b> <b>A ≤ B, with A known hard. Not "
            "the other way round.</b>",
            "<b>That direction is where almost every attempt "
            "fails.</b> <b>Reducing B to HALT proves nothing about "
            "B</b> — it says B is no harder than halting, which is "
            "not what you wanted to show."]},

  {"t": "code", "kicker": "Template", "title": "The construction, as a recipe",
   "lang": "text", "code": """
  TO PROVE B UNDECIDABLE:

  Assume a decider R for B.
  Build a decider for HALT (or A_TM) using R.
  Conclude R cannot exist.

  THE STANDARD SHAPE: given (M, w), construct a NEW machine
  M' whose B-property holds exactly when M halts on w.

  EXAMPLE -- "does M accept the empty string?":

      Given (M, w), build M':
          M'(x):
              ignore x
              run M on w
              if that halts, accept

      Then M' accepts the empty string
           <=> M' accepts everything
           <=> M halts on w

      So a decider for "accepts the empty string" would
      decide HALT. Contradiction.
""",
   "caption": "<b>Note what M′ does: it ignores its own input and "
              "runs the machine you are asking about</b> — that one "
              "move generates most of the reductions in the subject.",
   "note": "Give students the template explicitly; it is reusable."},

  {"t": "section", "label": "Part 2", "title": "Rice's theorem",
   "blurb": "Everything interesting is undecidable, in one theorem."},

  {"t": "callout", "title": "Rice: every non-trivial semantic property of programs is undecidable",
   "kind": "The result that generalises all of them",
   "body": ["<b>Let P be a property of the <i>language</i> a machine "
            "recognises</b> — a property of behaviour, not of "
            "syntax. <b>If P is non-trivial (some machines have it, "
            "some do not), P is undecidable.</b>",
            "<b>So: does this program compute the identity? Does it "
            "ever output 7? Is it equivalent to that one? Does it halt "
            "on all inputs? Is this dead code?</b> <b>All "
            "undecidable</b>, in one stroke.",
            "<b>The conditions matter.</b> <b>'Semantic' excludes "
            "syntactic properties</b> — 'has fewer than 100 states' "
            "is decidable. <b>'Non-trivial' excludes 'always true' and "
            "'always false'.</b>",
            "<b>And that is why static analysis is hard in "
            "principle</b> (Module 12). <b>Rice's theorem says you are "
            "not failing to find the clever algorithm; there isn't "
            "one.</b>"]},

  {"t": "table", "kicker": "Applying Rice", "title": "Semantic or syntactic?",
   "header": ["Property", "Which", "Status"],
   "widths": [4.2, 2.6, 4.1],
   "rows": [
     ["<b>'Halts on every input'</b>", "<b>Semantic</b>", "<b>Undecidable</b>"],
     ["<b>'Accepts a finite language'</b>", "<b>Semantic</b>", "<b>Undecidable</b>"],
     ["<b>'Equivalent to this other program'</b>", "<b>Semantic</b>", "<b>Undecidable</b>"],
     ["<b>'Contains a while loop'</b>", "<b>Syntactic</b>", "<b>Decidable — just look</b>"],
     ["<b>'Has at most 50 states'</b>", "<b>Syntactic</b>", "<b>Decidable</b>"],
     ["<b>'Halts within 1000 steps'</b>", "<b>Neither, strictly</b>", "<b>Decidable — simulate 1000 steps</b>"],
   ],
   "footnote": "<b>The last row is the engineering escape:</b> <b>bound "
               "the resource and the question becomes decidable</b> "
               "— which is what every practical analyser and every "
               "bounded model checker does.",
   "note": "The bounded row is the bridge to Module 12."},

  {"t": "section", "label": "Part 3", "title": "More reductions",
   "blurb": "Problems far from programs."},

  {"t": "bullets", "kicker": "Reduced", "title": "Undecidable by reduction, and not obviously about computation",
   "items": [
     "<b>Post correspondence problem.</b> Given domino pairs, is "
     "there a sequence matching top and bottom? <b>Pure string "
     "manipulation, undecidable.</b>",
     "",
     "<b>Grammar ambiguity</b> (Module 03 §2), and whether two "
     "context-free grammars generate the same language.",
     "",
     "<b>Tiling the plane</b> with a given finite tile set. "
     "<b>Geometry, undecidable</b> — and connected to aperiodic "
     "tilings.",
     "",
     "<b>Hilbert's tenth:</b> does a Diophantine equation have an "
     "integer solution? <b>Number theory, undecidable</b> "
     "(Module 01 §1).",
     "",
     "<b>And matrix mortality:</b> can a product of given integer "
     "matrices be zero? <b>Linear algebra, undecidable.</b>",
   ],
   "footnote": "<b>Undecidability is not confined to questions about "
               "programs</b> — these problems make no reference to "
               "computation, and the reductions are how computation gets "
               "in."},

  {"t": "callout", "title": "Post correspondence is the bridge",
   "kind": "Why it matters disproportionately",
   "body": ["<b>PCP is undecidable, by a reduction from halting that "
            "encodes a computation history as a domino sequence.</b>",
            "<b>And PCP is then easy to reduce <i>to</i> other string "
            "and grammar problems</b>, which is why it is the "
            "intermediate step in so many proofs.",
            "<b>So grammar ambiguity's undecidability goes via PCP</b> "
            "rather than directly from halting — the reduction is far "
            "more natural that way.",
            "<b>Which is the general pattern:</b> <b>build a small "
            "library of hard problems in different shapes, and reduce "
            "from whichever one is closest</b> — exactly as "
            "CSCE 629 does with 3-SAT, vertex cover, and Hamiltonian "
            "cycle."]},

  {"t": "section", "label": "Part 4", "title": "The parallel",
   "blurb": "Same technique, different resource bound."},

  {"t": "table", "kicker": "Comparison", "title": "Undecidability against NP-hardness",
   "header": ["", "This course", "CSCE 629 / CSCE 637"],
   "widths": [2.3, 4.4, 5.3],
   "rows": [
     ["<b>Reduce from</b>", "<b>HALT or Aₜₘ</b>", "<b>3-SAT, or another NP-complete problem</b>"],
     ["<b>f must be</b>", "<b>Computable</b>", "<b>Computable in polynomial time</b>"],
     ["<b>Conclusion</b>", "<b>No algorithm at all</b>", "<b>No polynomial algorithm, unless P = NP</b>"],
     ["<b>Status</b>", "<b>Proved, unconditional</b>", "<b>Conditional on P ≠ NP</b>"],
     ["<b>Direction</b>", "<b>Known hard → your problem</b>", "<b>Known hard → your problem</b>"],
   ],
   "footnote": "<b>The technique is identical and only the resource "
               "bound on f differs</b> — which is why learning "
               "reductions here transfers directly, and why the direction "
               "error is the same error in both.",
   "note": "Making the identity explicit saves students relearning it."},

  {"t": "callout", "title": "The practical upshot",
   "kind": "What to do with this",
   "body": ["<b>When you meet a problem that resists solution, try to "
            "prove it impossible.</b> <b>An hour spent attempting a "
            "reduction is cheaper than a month of algorithm "
            "design.</b>",
            "<b>And a successful reduction redirects the effort</b> "
            "— toward restriction, approximation, or a partial "
            "answer (Module 12), all of which are productive.",
            "<b>Rice's theorem makes this unusually fast for program "
            "analysis:</b> <b>if the property is semantic and "
            "non-trivial, stop and design the approximation.</b>",
            "<b>Which is the professional value of this module</b> "
            "— <b>recognising impossibility early is a skill, and it "
            "saves more time than any optimisation.</b>"]},
 ],
 "takeaways": [
   "A mapping reduction from A to B means B is at least as hard, so to "
   "prove B undecidable you reduce a known undecidable problem TO it.",
   "The direction is where almost every attempt fails — reducing your "
   "problem to HALT proves nothing.",
   "The workhorse construction builds a machine that ignores its input and "
   "runs the machine in question, so its behaviour encodes halting.",
   "Rice's theorem: every non-trivial semantic property of programs is "
   "undecidable — which is why static analysis is hard in principle.",
   "Bounding the resource makes the question decidable, which is what "
   "every practical analyser and bounded model checker does.",
   "The technique is identical to NP-hardness reduction and only the "
   "resource bound on the transformation differs.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The technique"),
  ("callout", "A reduction transforms instances, and the direction is "
              "everything",
   ["<b>A mapping reduction from A to B is a computable function f such "
    "that x is in A if and only if f(x) is in B.</b> Written A &le; B, "
    "and read 'A reduces to B' or 'B is at least as hard as A'.",
    "<b>If A &le; B and B is decidable, then A is decidable</b> "
    "— transform the input with f and ask B's decider. <b>So "
    "contrapositively, if A is undecidable then B is undecidable.</b>",
    "<b>So to prove B undecidable, reduce a known undecidable problem "
    "TO it.</b> <b>A &le; B, with A already known to be hard.</b> "
    "<b>Not the other way round.</b>",
    "<b>And that direction is where almost every attempt fails.</b> "
    "<b>Reducing B to HALT proves nothing about B</b> — it "
    "establishes that B is no <i>harder</i> than halting, which is "
    "something you already suspected and is not what you set out to show. "
    "<b>State explicitly, in writing, what reduces to what, every "
    "time</b>; it is the single most effective guard against the error."]),
  ("code", """TO PROVE B UNDECIDABLE:

Assume a decider R for B.
Build a decider for HALT (or A_TM) using R.
Conclude R cannot exist.

THE STANDARD SHAPE: given an instance (M, w) of halting,
construct a NEW machine M' whose B-property holds exactly
when M halts on w.

EXAMPLE -- "does M accept the empty string?" is undecidable.

    Given (M, w), build M':
        M'(x):
            ignore x
            run M on w
            if that halts, accept

    Then M' accepts the empty string
         <=> M' accepts every string
         <=> M halts on w

    So a decider for "accepts the empty string" would
    decide HALT. Contradiction.

NOTE WHAT M' DOES: it IGNORES ITS OWN INPUT and runs the
machine you are asking about. That one move -- build a
machine whose behaviour is CONSTANT and determined entirely
by whether M halts -- generates most of the reductions in
this subject. Learn it once."""),

  ("h1", "2 &nbsp; Rice's theorem"),
  ("callout", "Rice: every non-trivial semantic property of programs is "
              "undecidable",
   ["<b>Let P be a property of the <i>language</i> that a machine "
    "recognises</b> — a property of its behaviour, not of its text. "
    "<b>If P is non-trivial, meaning some machines have it and some do "
    "not, then P is undecidable.</b> One theorem, proved by the "
    "construction of &sect;1.",
    "<b>So: does this program compute the identity function? Does it "
    "ever output 7? Is it equivalent to that other program? Does it halt "
    "on all inputs? Is this branch dead code? Can this variable ever be "
    "null?</b> <b>All undecidable, in one stroke</b>, without needing a "
    "separate reduction for each.",
    "<b>The conditions matter and are frequently misquoted.</b> "
    "<b>'Semantic' excludes syntactic properties</b> — 'has fewer "
    "than 100 states' or 'contains a goto' is decidable by inspection. "
    "<b>'Non-trivial' excludes the properties true of every machine or of "
    "none</b>, which are trivially decidable by answering yes or no.",
    "<b>And that is why static analysis is hard in principle</b> rather "
    "than in practice (Module 12). <b>Rice's theorem says you are not "
    "failing to find the clever algorithm; there is no clever "
    "algorithm.</b> <b>Which is a genuinely useful thing to know before "
    "spending a month looking for one.</b>"]),
  ("table", ["Property of a program", "Semantic or syntactic?", "Status"],
   [["<b>'Halts on every input'</b>", "<b>Semantic</b>",
     "<b>Undecidable</b>"],
    ["<b>'Accepts only finitely many strings'</b>", "<b>Semantic</b>",
     "<b>Undecidable</b>"],
    ["<b>'Computes the same function as this other program'</b>",
     "<b>Semantic</b>", "<b>Undecidable</b>"],
    ["<b>'Contains a while loop'</b>", "<b>Syntactic</b>",
     "<b>Decidable — look at the source.</b>"],
    ["<b>'Has at most 50 states'</b>", "<b>Syntactic</b>",
     "<b>Decidable</b>"],
    ["<b>'Halts within 1000 steps'</b>",
     "<b>Neither, strictly — it is a bounded behavioural "
     "property.</b>",
     "<b>Decidable — simulate for 1000 steps and look.</b>"]],
   [0.37, 0.26, 0.37]),
  ("p", "<b>The last row is the engineering escape, and it is the most "
        "important line in the table.</b> <b>Bound the resource and the "
        "question becomes decidable</b> — 'halts within 1000 steps', "
        "'uses at most 1 MB', 'no bug within 20 loop iterations'. "
        "<b>Which is exactly what every practical analyser and every "
        "bounded model checker does</b> (CSCE 625 Module 08 &sect;3), "
        "and it is Module 12 &sect;2's second engineering response. "
        "<b>The unbounded quantifier is what costs the decidability, "
        "every time.</b>"),

  ("break",),
  ("h1", "3 &nbsp; Undecidability far from programs"),
  ("ul", ["<b>The Post correspondence problem.</b> Given a finite set of "
          "domino pairs, each with a string on top and a string on the "
          "bottom, is there a sequence (with repeats allowed) whose "
          "concatenated tops equal its concatenated bottoms? <b>Pure "
          "string manipulation, no reference to computation, and "
          "undecidable.</b>",
          "<b>Grammar ambiguity</b> (Module 03 &sect;2), <b>and "
          "whether two context-free grammars generate the same "
          "language</b> — both of which have immediate consequences "
          "for parser tooling.",
          "<b>Tiling the plane</b> with a given finite set of tiles "
          "whose edges must match. <b>Geometry, and undecidable</b> "
          "— and the proof is connected to the existence of "
          "aperiodic tilings, which is why that question was interesting "
          "to logicians before it was interesting to crystallographers.",
          "<b>Hilbert's tenth problem:</b> does a given polynomial "
          "equation with integer coefficients have an integer solution? "
          "<b>Number theory, and undecidable</b> (Module 01 "
          "&sect;1) — by a reduction that took decades to "
          "construct.",
          "<b>And matrix mortality:</b> given a finite set of integer "
          "matrices, can some product of them (with repeats) be the zero "
          "matrix? <b>Linear algebra, and undecidable.</b> <b>So "
          "undecidability is not confined to questions about "
          "programs</b> — these problems make no reference to "
          "computation at all, <b>and the reductions are how computation "
          "gets into them.</b>"]),
  ("callout", "Post correspondence is the bridge",
   ["<b>PCP is undecidable, by a reduction from halting that encodes a "
    "machine's computation history as a sequence of dominoes</b> — "
    "the top string runs one step behind the bottom, so a matching "
    "sequence is exactly a valid halting computation.",
    "<b>And PCP is then easy to reduce <i>to</i> other string and "
    "grammar problems</b>, because it is already in the right shape "
    "— <b>which is why it is the intermediate step in so many "
    "proofs.</b>",
    "<b>So grammar ambiguity's undecidability goes via PCP</b> rather "
    "than directly from halting: build two grammars from a PCP instance "
    "such that they share a string exactly when the instance has a "
    "match. <b>The reduction is far more natural that way</b>, and "
    "attempting it directly from halting is painful.",
    "<b>Which is the general pattern worth taking away:</b> <b>build a "
    "small library of hard problems in different shapes, and reduce from "
    "whichever one is structurally closest to your target</b> — "
    "<b>exactly as CSCE 629 does with 3-SAT for logic, vertex cover for "
    "graphs, and Hamiltonian cycle for paths.</b> The library is the "
    "tool, not any single problem in it."]),

  ("h1", "4 &nbsp; The parallel with NP-hardness"),
  ("table", ["", "This course", "CSCE 629 and CSCE 637"],
   [["<b>Reduce from</b>",
     "<b>HALT or A<sub>TM</sub>, or PCP as an intermediate.</b>",
     "<b>3-SAT, or another known NP-complete problem.</b>"],
    ["<b>The function f must be</b>", "<b>Computable.</b>",
     "<b>Computable in polynomial time</b> — the only "
     "difference."],
    ["<b>The conclusion</b>",
     "<b>No algorithm exists at all.</b>",
     "<b>No polynomial-time algorithm exists, unless P = NP.</b>"],
    ["<b>Status of the conclusion</b>",
     "<b>Proved, unconditionally.</b>",
     "<b>Conditional on P &ne; NP</b>, which is unproved."],
    ["<b>Direction</b>", "<b>Known hard problem &rarr; your "
     "problem.</b>", "<b>Known hard problem &rarr; your problem.</b>"]],
   [0.22, 0.36, 0.42]),
  ("p", "<b>The technique is identical and only the resource bound on f "
        "differs</b> — which is why <b>learning reductions here "
        "transfers directly to complexity</b>, and why <b>the "
        "direction error is the same error in both subjects.</b> <b>It is "
        "also why the two courses are in the same semester.</b>"),
  ("callout", "The practical upshot",
   ["<b>When you meet a problem that resists solution, try to prove it "
    "impossible.</b> <b>An hour spent attempting a reduction is far "
    "cheaper than a month of algorithm design</b>, and the attempt "
    "frequently clarifies the problem even when it fails.",
    "<b>And a successful reduction redirects the effort productively</b> "
    "— toward restricting the input, accepting an approximation, or "
    "returning a partial answer (Module 12) — all of which are "
    "real engineering options rather than consolation prizes.",
    "<b>Rice's theorem makes this unusually fast for program "
    "analysis:</b> <b>if the property you want to decide is semantic and "
    "non-trivial, stop immediately and start designing the "
    "approximation.</b> No reduction needs to be constructed; the theorem "
    "has done it.",
    "<b>Which is the professional value of this module.</b> "
    "<b>Recognising impossibility early is a skill, and it saves more "
    "time than any optimisation</b> — and it is the one skill in "
    "this course that transfers to every other."]),
 ],
 "resources": [
   ("Sipser &mdash; chapter 5",
    "https://math.mit.edu/~sipser/book.html",
    "<b>Mapping reductions, Rice's theorem, and the Post correspondence "
    "problem</b> — the reference for this module, including the PCP "
    "reduction in full."),
   ("MIT 18.404J &mdash; lectures 10–12 (free)",
    "https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/",
    "<b>The reductions worked at the board</b>, which is the right way to "
    "see them the first time."),
   ("Rice &mdash; Classes of recursively enumerable sets (free via "
    "JSTOR listing)",
    "https://www.ams.org/journals/tran/1953-074-02/S0002-9947-1953-0053041-6/",
    "<b>&sect;2's theorem, in the original.</b> Short."),
   ("Berger &mdash; The undecidability of the domino problem; and the "
    "Wang tiles literature",
    "https://www.ams.org/books/memo/0066/",
    "<b>&sect;3's tiling result</b>, and its connection to aperiodic "
    "tilings is worth following."),
 ],
 "exercises": [
   "<b>Write out the definition of a mapping reduction</b> and state the "
   "direction rule in your own words.",
   "<b>Construct the 'accepts the empty string' reduction</b> yourself "
   "without looking.",
   "<b>Prove three more properties undecidable</b> by reduction: 'accepts "
   "a finite language', 'halts on all inputs', 'is equivalent to the "
   "always-reject machine'.",
   "<b>Deliberately do one reduction backwards</b> and explain precisely "
   "what it proves and does not.",
   "<b>Apply Rice's theorem to five properties</b> and verify the "
   "non-triviality condition each time.",
   "<b>Find a property that Rice does not cover</b> and say why.",
   "<b>Bound a property</b> — 'halts within n steps' — and "
   "write the decider.",
   "<b>Solve three small PCP instances by hand</b> and one that has no "
   "solution.",
   "<b>Sketch the PCP-to-grammar-ambiguity reduction.</b>",
   "<b>Take an unsolved problem from your own work</b> and spend an hour "
   "trying to prove it undecidable. Report what you learned either "
   "way.",
 ],
 "selfcheck": [
   "Define a mapping reduction and state what it preserves.",
   "Which direction proves B undecidable, and what does the other "
   "direction prove?",
   "Give the workhorse construction and explain the ignore-the-input "
   "move.",
   "State Rice's theorem with both conditions.",
   "Classify six properties as semantic, syntactic, or bounded.",
   "What does bounding a resource buy?",
   "Name five undecidable problems that are not about programs.",
   "Why is PCP the bridge?",
   "Compare undecidability and NP-hardness reductions on five axes.",
   "What is the practical upshot of this module?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Degrees of Unsolvability",
 "subtitle": "Undecidable is not one thing.",
 "question": "Are some undecidable problems harder than others?",
 "outcomes": [
     "Define an oracle machine and relative computability.",
     "Explain Turing reducibility and Turing degrees.",
     "Place problems in the arithmetic hierarchy.",
     "Explain why the hierarchy does not collapse.",
     "Explain why this structure matters for Module 08.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Oracles",
   "blurb": "What if you were given the answer to halting?"},

  {"t": "callout", "title": "An oracle machine can ask a question it cannot answer",
   "kind": "The idea",
   "body": ["<b>Give a Turing machine a black box that answers "
            "membership in some language A, in one step.</b> That is an "
            "oracle machine.",
            "<b>With a HALT oracle, halting becomes trivially "
            "decidable</b> — and new problems become undecidable "
            "<i>relative to it</i>.",
            "<b>'B is Turing reducible to A' (B ≤_T A) means "
            "an A-oracle machine decides B.</b> <b>A weaker and more "
            "general notion than Module 06's mapping "
            "reduction.</b>",
            "<b>And it gives a notion of equivalent difficulty:</b> "
            "<b>A and B have the same <i>Turing degree</i> if each "
            "reduces to the other</b> — so 'as hard as' becomes a "
            "precise relation."]},

  {"t": "callout", "title": "The halting problem relativises, and that is the key fact",
   "kind": "Why the structure is infinite",
   "body": ["<b>Module 05's proof used nothing about the machine model "
            "except that programs are data.</b> So it goes through "
            "unchanged for oracle machines.",
            "<b>So 'does this HALT-oracle machine halt?' is undecidable "
            "even with a HALT oracle.</b> <b>Call it HALT′, the "
            "jump.</b>",
            "<b>And you can do it again, forever.</b> HALT, "
            "HALT′, HALT″, … — <b>an infinite "
            "strictly increasing sequence of difficulties.</b>",
            "<b>So 'undecidable' names infinitely many distinct "
            "levels</b>, not one — <b>which is why Module 05's "
            "EQ_TM really is harder than halting</b> rather than "
            "being loosely described that way."]},

  {"t": "section", "label": "Part 2", "title": "The hierarchy",
   "blurb": "Counting quantifiers."},

  {"t": "code", "kicker": "Arithmetic hierarchy", "title": "Difficulty is quantifier alternation",
   "lang": "text", "code": """
  Write a problem as a formula over a DECIDABLE predicate R,
  and count the leading quantifiers.

  Sigma_1   exists y . R(x,y)
      RECOGNISABLE. "M halts on w" = exists a halting
      computation. One existential; a finite witness.

  Pi_1      forall y . R(x,y)
      CO-RECOGNISABLE. "M halts on EVERY input" --
      no finite witness, and the complement is Sigma_1.

  Sigma_2   exists y forall z . R(x,y,z)
      "M accepts a finite language": there EXISTS a bound
      such that FOR ALL longer strings M rejects.

  Pi_2      forall y exists z . R(x,y,z)
      "M halts on infinitely many inputs".

  AND SO ON, ALTERNATING. The hierarchy is STRICT: each
  level contains problems not in any lower one, proved by
  diagonalisation at that level (Module 05 Part 3).

  TO PLACE A PROBLEM: WRITE IT WITH QUANTIFIERS AND COUNT
  THE ALTERNATIONS. That is the whole method.
""",
   "caption": "<b>Quantifier alternation is the measure of "
              "difficulty</b>, and Σ₁ ∩ Π₁ is "
              "exactly the decidable problems — Module 04's "
              "complement theorem, restated.",
   "note": "The counting method is genuinely usable; make students do "
           "it."},

  {"t": "table", "kicker": "Placing", "title": "Where familiar problems sit",
   "header": ["Problem", "Level", "Why"],
   "widths": [4.0, 2.4, 4.5],
   "rows": [
     ["<b>Primality</b>", "<b>Decidable</b>", "<b>Σ₁ ∩ Π₁</b>"],
     ["<b>M halts on w</b>", "<b>Σ₁</b>", "<b>∃ a halting run</b>"],
     ["<b>M halts on all inputs</b>", "<b>Π₂</b>", "<b>∀w ∃ a run that halts</b>"],
     ["<b>M accepts nothing</b>", "<b>Π₁</b>", "<b>∀w, M does not accept w</b>"],
     ["<b>M accepts a finite set</b>", "<b>Σ₂</b>", "<b>∃ bound ∀ longer, rejects</b>"],
     ["<b>M₁ ≡ M₂</b>", "<b>Π₂</b>", "<b>∀w, both agree — each Σ₁</b>"],
   ],
   "footnote": "<b>Program equivalence is Π₂</b>, strictly "
               "above halting — which is the precise form of the "
               "intuition that 'do these two programs do the same thing' "
               "is the harder question.",
   "note": "Students enjoy placing problems once they see it is "
           "mechanical."},

  {"t": "section", "label": "Part 3", "title": "Why it matters",
   "blurb": "Beyond classification."},

  {"t": "bullets", "kicker": "Consequences", "title": "What the hierarchy buys",
   "items": [
     "<b>It distinguishes 'undecidable' from 'hopeless'.</b> "
     "<b>A Σ₁ problem has verifiable yes-instances</b>, so a "
     "semi-decision procedure exists and is useful.",
     "",
     "<b>It predicts which direction a tool can be sound in.</b> "
     "<b>Π₁ properties can be refuted by one counterexample "
     "and not confirmed</b> — which is exactly a testing "
     "asymmetry.",
     "",
     "<b>It explains why some verification is harder than "
     "others.</b> Safety is Π₁; liveness is "
     "Π₂ — and liveness really is harder, in a "
     "provable sense.",
     "",
     "<b>It is where the polynomial hierarchy comes from</b> "
     "(CSCE 637), by bounding the quantifiers.",
     "",
     "<b>And it tells you a hard problem is not necessarily "
     "equally hard</b> — Post's problem asked whether there is a "
     "degree strictly between, and the answer is yes.",
   ],
   "footnote": "<b>The safety/liveness distinction is the most useful "
               "practical consequence</b> — a tool that checks "
               "safety can be sound; a liveness checker faces a strictly "
               "harder problem."},

  {"t": "callout", "title": "Safety and liveness, and why the asymmetry is real",
   "kind": "The engineering payoff",
   "body": ["<b>A safety property says 'nothing bad happens' — "
            "∀ states, the state is good.</b> <b>Π₁:</b> "
            "one bad state refutes it, and no finite trace confirms "
            "it.",
            "<b>A liveness property says 'something good eventually "
            "happens' — ∀ paths ∃ a point.</b> "
            "<b>Π₂, strictly harder.</b>",
            "<b>Which is why testing finds safety violations and "
            "essentially never establishes liveness</b> — a failing "
            "test is a counterexample to safety and no test is evidence "
            "about eventuality.",
            "<b>And why model checkers treat the two "
            "differently</b> — safety by reachability, liveness by "
            "cycle detection on the product with a Büchi "
            "automaton. <b>The algorithms differ because the levels "
            "differ.</b>"]},

  {"t": "section", "label": "Part 4", "title": "The structure",
   "blurb": "What is known about the degrees."},

  {"t": "callout", "title": "The degree structure is rich, strange, and mostly settled",
   "kind": "A brief tour",
   "body": ["<b>There is a least degree (the decidable problems) and "
            "the jump operator always strictly increases</b>, so there "
            "is no greatest.",
            "<b>Post's problem:</b> is there a recognisable problem "
            "strictly between decidable and HALT? <b>Yes — proved "
            "independently by Friedberg and Muchnik in 1956, by the "
            "priority method.</b>",
            "<b>And the degrees are not a line.</b> <b>There are "
            "incomparable degrees</b> — two problems neither of which "
            "reduces to the other, which is non-transitivity of "
            "difficulty.",
            "<b>This is a deep and specialised field</b>, and "
            "<b>knowing that it exists and that difficulty is a partial "
            "order rather than a scale is the useful "
            "takeaway</b> — more than any particular result in it."]},
 ],
 "takeaways": [
   "An oracle machine gets membership in some language for free, which "
   "defines Turing reducibility — weaker and more general than "
   "mapping reduction.",
   "The halting proof relativises, so there is a strictly harder halting "
   "problem above every level, and the hierarchy is infinite.",
   "Difficulty is quantifier alternation: write the problem with "
   "quantifiers over a decidable predicate and count.",
   "Σ₁ and Π₁ intersect exactly in the decidable "
   "problems, which is Module 04's complement theorem restated.",
   "Safety is Π₁ and liveness is Π₂, which is why "
   "testing refutes safety and never establishes liveness.",
   "The degrees are a partial order rather than a scale — there are "
   "incomparable degrees, and a degree strictly between decidable and "
   "halting.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Oracles and relative computability"),
  ("callout", "An oracle machine can ask a question it cannot answer",
   ["<b>Give a Turing machine a black box that answers membership in some "
    "fixed language A, in a single step, correctly.</b> That is an oracle "
    "machine, and it is a thought experiment rather than a device.",
    "<b>With a HALT oracle, the halting problem becomes trivially "
    "decidable</b> — and new problems become undecidable "
    "<i>relative to that oracle</i>, which is the interesting part.",
    "<b>'B is Turing reducible to A', written B &le;<sub>T</sub> A, "
    "means an A-oracle machine decides B.</b> <b>This is a weaker and "
    "more general notion than Module 06's mapping reduction</b>: the "
    "machine may consult the oracle many times, adaptively, and may "
    "invert its answers — so <b>Turing reducibility does not "
    "distinguish a language from its complement, and mapping reducibility "
    "does.</b>",
    "<b>And it gives a notion of equivalent difficulty:</b> <b>A and B "
    "have the same <i>Turing degree</i> if each is Turing reducible to the "
    "other</b> — so 'as hard as' becomes a precise equivalence "
    "relation, and the equivalence classes can be partially ordered "
    "(&sect;4)."]),
  ("callout", "The halting problem relativises, and that is the key fact",
   ["<b>Module 05's proof used nothing about the machine model except "
    "that programs can be encoded as data</b> (Module 04 &sect;3) "
    "— so <b>it goes through unchanged for oracle machines.</b>",
    "<b>So 'does this HALT-oracle machine halt on this input?' is "
    "undecidable even by a machine with a HALT oracle.</b> <b>Call that "
    "language HALT&prime;, the <i>jump</i> of HALT.</b>",
    "<b>And you can do it again, forever.</b> HALT, HALT&prime;, "
    "HALT&Prime;, and so on — <b>an infinite, strictly increasing "
    "sequence of difficulties, each one undecidable relative to "
    "everything below it.</b>",
    "<b>So 'undecidable' names infinitely many distinct levels rather "
    "than one.</b> <b>Which is why Module 05's EQ<sub>TM</sub> really is "
    "harder than halting</b> — it sits strictly above it in "
    "&sect;2's hierarchy — <b>rather than being loosely described "
    "that way.</b>"]),

  ("h1", "2 &nbsp; The arithmetic hierarchy"),
  ("code", """Write the problem as a formula over a DECIDABLE predicate R,
and count the leading quantifiers.

Sigma_1   exists y . R(x,y)
    RECOGNISABLE. "M halts on w" = there EXISTS a halting
    computation. One existential, and a finite witness.

Pi_1      forall y . R(x,y)
    CO-RECOGNISABLE. "M halts on EVERY input" -- no finite
    witness exists, and the complement is Sigma_1.

Sigma_2   exists y forall z . R(x,y,z)
    "M accepts a finite language": there EXISTS a length
    bound such that FOR ALL longer strings M rejects.

Pi_2      forall y exists z . R(x,y,z)
    "M halts on infinitely many inputs".

AND SO ON, ALTERNATING. The hierarchy is STRICT: each level
contains problems not in any lower level, proved by
diagonalisation at that level (Module 05 section 3).

SO: TO PLACE A PROBLEM, WRITE IT OUT WITH QUANTIFIERS AND
COUNT THE ALTERNATIONS. That is the whole method, and it is
mechanical.

Sigma_1 and Pi_1 intersect in exactly the DECIDABLE
problems -- which is Module 04 section 2's complement
theorem, restated in this language."""),
  ("p", "<b>Quantifier alternation is the measure of difficulty</b>, and "
        "<b>the same idea measures complexity in CSCE 637's polynomial "
        "hierarchy</b>, with the quantifiers bounded to polynomial-length "
        "witnesses: &Sigma;<sub>1</sub><super>p</super> is NP, "
        "&Pi;<sub>1</sub><super>p</super> is co-NP, and the alternation "
        "continues. <b>So this module and CSCE 637's hierarchy are the "
        "same construction at two different resource bounds</b>, which is "
        "worth noticing because it means the intuition transfers."),
  ("table", ["Problem", "Level", "Why"],
   [["<b>Primality</b>", "<b>Decidable</b>",
     "<b>&Sigma;<sub>1</sub> &cap; &Pi;<sub>1</sub></b>"],
    ["<b>M halts on w</b>", "<b>&Sigma;<sub>1</sub></b>",
     "<b>There exists a halting run.</b>"],
    ["<b>M halts on all inputs</b>", "<b>&Pi;<sub>2</sub></b>",
     "<b>For all w, there exists a run that halts.</b>"],
    ["<b>M accepts nothing</b>", "<b>&Pi;<sub>1</sub></b>",
     "<b>For all w, M does not accept w.</b>"],
    ["<b>M accepts a finite set</b>", "<b>&Sigma;<sub>2</sub></b>",
     "<b>There exists a bound, for all longer strings M rejects.</b>"],
    ["<b>M<sub>1</sub> and M<sub>2</sub> are equivalent</b>",
     "<b>&Pi;<sub>2</sub></b>",
     "<b>For all w, the two agree — and each agreement is itself "
     "&Sigma;<sub>1</sub>.</b>"]],
   [0.34, 0.20, 0.46]),
  ("p", "<b>Program equivalence is &Pi;<sub>2</sub></b>, strictly above "
        "halting — <b>which is the precise form of the intuition "
        "that 'do these two programs do the same thing' is a harder "
        "question than 'does this program finish'</b>. The intuition was "
        "correct and the hierarchy says exactly how much."),

  ("break",),
  ("h1", "3 &nbsp; What the hierarchy buys"),
  ("ul", ["<b>It distinguishes 'undecidable' from 'hopeless'.</b> <b>A "
          "&Sigma;<sub>1</sub> problem has verifiable yes-instances</b>, "
          "so a semi-decision procedure exists and can be genuinely "
          "useful — run it, and if it answers you have a proof. "
          "<b>A &Pi;<sub>2</sub> problem has no such procedure in either "
          "direction.</b>",
          "<b>It predicts which direction a tool can be sound in.</b> "
          "<b>A &Pi;<sub>1</sub> property can be refuted by a single "
          "counterexample and never confirmed by finitely much "
          "evidence</b> — <b>which is exactly the asymmetry of "
          "testing</b>, and is why 'tests cannot prove the absence of "
          "bugs' is a theorem rather than a slogan.",
          "<b>It explains why some verification is harder than "
          "other verification.</b> Safety is &Pi;<sub>1</sub>; liveness "
          "is &Pi;<sub>2</sub> — <b>and liveness genuinely is "
          "harder, in a provable sense</b> (see the callout).",
          "<b>It is where the polynomial hierarchy comes from</b> "
          "(CSCE 637), by bounding the quantifiers to polynomial-length "
          "witnesses — so the structure recurs with resources "
          "attached.",
          "<b>And it tells you that hard problems are not all equally "
          "hard</b> — <b>Post's problem asked whether any "
          "recognisable problem lies strictly between decidable and "
          "halting, and the answer is yes</b> (&sect;4)."]),
  ("callout", "Safety and liveness, and why the asymmetry is real",
   ["<b>A safety property says 'nothing bad ever happens' — for all "
    "reachable states, the state is good.</b> <b>That is "
    "&Pi;<sub>1</sub>:</b> a single bad state refutes it, and no finite "
    "amount of good behaviour confirms it.",
    "<b>A liveness property says 'something good eventually happens' "
    "— for all executions, there exists a point at which it "
    "holds.</b> <b>That is &Pi;<sub>2</sub>, strictly harder.</b>",
    "<b>Which is why testing finds safety violations and essentially "
    "never establishes liveness.</b> <b>A failing test is a complete "
    "counterexample to a safety property</b>, and <b>no test of any "
    "length is evidence about eventuality</b> — the run you observed "
    "simply had not got there yet, and you cannot tell that from never "
    "getting there.",
    "<b>And it is why model checkers treat the two differently:</b> "
    "<b>safety by reachability analysis, and liveness by cycle detection "
    "on the product of the system with a B&uuml;chi automaton.</b> "
    "<b>The algorithms differ because the hierarchy levels differ</b>, "
    "which is a case of this module's abstract structure determining a "
    "concrete tool's architecture — and it is the most useful "
    "practical consequence in the module."]),

  ("h1", "4 &nbsp; The structure of the degrees"),
  ("callout", "The degree structure is rich, strange, and mostly settled",
   ["<b>There is a least degree — the decidable problems — and "
    "the jump operator always strictly increases</b> (&sect;1), <b>so "
    "there is no greatest degree</b> and the structure is unbounded "
    "above.",
    "<b>Post's problem</b> asked whether there is a recognisable problem "
    "whose degree lies strictly between the decidable problems and HALT. "
    "<b>The answer is yes — proved independently by Friedberg and "
    "Muchnik in 1956, by the <i>priority method</i></b>, which was "
    "invented for the purpose and became the field's central technique.",
    "<b>And the degrees are not a line.</b> <b>There are incomparable "
    "degrees — pairs of problems neither of which is Turing "
    "reducible to the other</b> — so <b>'harder than' is a partial "
    "order rather than a scale</b>, and two problems can be unsolvable in "
    "unrelated ways.",
    "<b>This is a deep and specialised field</b> (computability theory "
    "proper, and it continues), and <b>knowing that it exists and that "
    "difficulty is a partial order rather than a single axis is the useful "
    "takeaway</b> — more useful than any particular result in it, "
    "and enough to stop you from asking which of two undecidable problems "
    "is harder without checking that the question has an answer."]),
 ],
 "resources": [
   ("Sipser &mdash; sections 6.3–6.4",
    "https://math.mit.edu/~sipser/book.html",
    "<b>Oracles, Turing reducibility, and the hierarchy</b> — a "
    "brief but sufficient treatment."),
   ("Soare &mdash; Turing Computability: Theory and Applications",
    "https://link.springer.com/book/10.1007/978-3-642-31933-4",
    "<b>The modern reference for &sect;4</b>, including the priority "
    "method and Post's problem."),
   ("Rogers &mdash; Theory of Recursive Functions and Effective "
    "Computability",
    "https://mitpress.mit.edu/9780262680523/",
    "<b>The classical reference</b>, and still the clearest treatment of "
    "the arithmetic hierarchy of &sect;2. Library copy."),
   ("Baier & Katoen &mdash; Principles of Model Checking",
    "https://mitpress.mit.edu/9780262026499/principles-of-model-checking/",
    "<b>&sect;3's safety/liveness distinction, operationalised</b> "
    "— the two different algorithms and why. Library copy; the "
    "lecture notes from the authors' courses are free."),
 ],
 "exercises": [
   "<b>Define an oracle machine</b> and write a program sketch using a "
   "HALT oracle to decide something interesting.",
   "<b>Prove that halting relativises</b>, by checking Module 05's proof "
   "step by step.",
   "<b>Show that Turing reducibility does not distinguish a language from "
   "its complement</b>, and that mapping reducibility does.",
   "<b>Place six problems in the arithmetic hierarchy</b> by writing them "
   "with quantifiers.",
   "<b>Find a Σ₂ problem of your own</b> and justify the "
   "level.",
   "<b>Confirm Σ₁ ∩ Π₁ is the decidable "
   "problems</b> and relate it to Module 04's theorem.",
   "<b>Classify three properties of a system you have built</b> as safety "
   "or liveness, and state the level of each.",
   "<b>Write a test that refutes a safety property</b> and explain why no "
   "test establishes the corresponding liveness one.",
   "<b>Read about the priority method</b> and summarise what Post's "
   "problem asked.",
   "<b>Find two problems you believe are incomparable</b> and say why you "
   "cannot easily tell.",
 ],
 "selfcheck": [
   "Define an oracle machine and Turing reducibility.",
   "How does Turing reducibility differ from mapping reducibility?",
   "Why does the halting problem relativise, and what follows?",
   "Give the first four levels of the arithmetic hierarchy with "
   "examples.",
   "What is the method for placing a problem?",
   "What is Σ₁ ∩ Π₁?",
   "Why is program equivalence harder than halting, precisely?",
   "Give five things the hierarchy buys.",
   "Classify safety and liveness and explain the testing asymmetry.",
   "What did Post's problem ask, and what is the shape of the degree "
   "order?",
 ],
},

]
