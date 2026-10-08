# -*- coding: utf-8 -*-
"""UC MATH 600 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Logic and Proof Technique",
 "subtitle": "Three techniques that cover almost everything.",
 "question": "You are stuck on a proof. What do you try first?",
 "outcomes": [
     "Read and write quantified statements precisely.",
     "Negate a statement correctly.",
     "Write direct and contrapositive proofs.",
     "Write proofs by contradiction, and know when not to.",
     "Choose a technique from the shape of the statement.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Statements",
   "blurb": "And the quantifiers that make them precise."},

  {"t": "callout", "title": "Almost every statement in this program has the form 'for all x, if P(x) then Q(x)'",
   "kind": "The shape to recognise",
   "body": ["<b>'Every even integer greater than two is the sum of "
            "two primes'</b>; <b>'if a graph is connected then it has a "
            "spanning tree'</b> — <b>the same shape</b>, and the shape "
            "tells you how to start.",
            "<b>The order of quantifiers matters "
            "absolutely:</b> <b>'for every x there is a y' and 'there "
            "is a y for every x' are different statements</b>, and the "
            "second is much stronger.",
            "<b>Which is the commonest source of a wrong proof in "
            "this course</b> — <b>proving the weak one and claiming "
            "the strong one</b> — and it happens because English hides "
            "the distinction.",
            "<b>So write the quantifiers out</b>, in order, before "
            "starting — <b>which costs a line and settles what you are "
            "actually trying to prove</b>."]},

  {"t": "code", "kicker": "Negation", "title": "Negating a statement, mechanically",
   "lang": "text", "code": """
  THE RULES
      not (for all x, P(x))     =  exists x, not P(x)
      not (exists x, P(x))      =  for all x, not P(x)
      not (P and Q)             =  not P or not Q
      not (P or Q)              =  not P and not Q
      not (if P then Q)         =  P and not Q
          <-- this one surprises people

  SO TO NEGATE
      walk the quantifiers left to right, flipping
      each, and negate the innermost statement.

  EXAMPLE
      "for every e > 0 there is an N such that for
       all n > N, |a_n - L| < e"
  negates to
      "there is an e > 0 such that for every N
       there is an n > N with |a_n - L| >= e"

  WHICH IS MECHANICAL. You never have to think about
  what the negation "means" -- apply the rules, then
  read the result.
""",
   "caption": "<b>Negation is mechanical</b> — flip each quantifier "
              "left to right and negate the inside; never reason about "
              "what the negation 'means'.",
   "note": "Negating correctly is what makes contradiction and "
           "contrapositive usable."},

  {"t": "section", "label": "Part 2", "title": "The three techniques",
   "blurb": "And what each is good for."},

  {"t": "table", "kicker": "Techniques", "title": "The three, and when each is the right first try",
   "header": ["Technique", "You assume", "Best when"],
   "widths": [2.7, 3.9, 4.4],
   "rows": [
     ["<b>Direct</b>", "<b>P, and derive Q</b>", "<b>P gives you something to work with</b>"],
     ["<b>Contrapositive</b>", "<b>not Q, and derive not P</b>", "<b>not Q is more concrete than P</b>"],
     ["<b>Contradiction</b>", "<b>P and not Q, derive nonsense</b>", "<b>The claim is a non-existence</b>"],
     ["<b>Cases</b>", "<b>Each possibility in turn</b>", "<b>The situation genuinely splits</b>"],
     ["<b>Counterexample</b>", "<b>—</b>", "<b>You suspect it is false (M01 §2)</b>"],
   ],
   "footnote": "<b>Try direct first, then contrapositive, then "
               "contradiction</b> — in that order, because each is "
               "harder to get right than the one before "
               "it.",
   "note": "The ordering is the practical content: most students "
           "reach for contradiction too early."},

  {"t": "callout", "title": "Contrapositive is underused, and it is frequently the whole difficulty",
   "kind": "The technique worth reaching for sooner",
   "body": ["<b>'If n² is even then n is even' is awkward "
            "directly</b> — you know something about n² and want "
            "something about n, which is the wrong "
            "direction.",
            "<b>The contrapositive is 'if n is odd then n² is "
            "odd'</b> — <b>and now you can write n = 2k + 1 and "
            "compute</b>, which takes one line.",
            "<b>So the rule of thumb: if the hypothesis is hard to "
            "use and the negated conclusion is easy to use, take the "
            "contrapositive</b> — which is a mechanical test you can "
            "apply before starting.",
            "<b>And it is logically identical</b>, not weaker — "
            "<b>'if P then Q' and 'if not Q then not P' are the same "
            "statement</b>, so nothing is given up."]},

  {"t": "section", "label": "Part 3", "title": "Contradiction",
   "blurb": "Powerful, overused, and worth being careful with."},

  {"t": "bullets", "kicker": "Contradiction", "title": "When it earns its keep, and when it hides a direct proof",
   "items": [
     "<b>It is the right tool for non-existence</b> — "
     "<b>'there is no largest prime', 'the square root of two is not "
     "rational'</b> — because assuming the thing exists gives you "
     "an object to work with.",
     "",
     "<b>And for minimal-counterexample arguments</b>, which are "
     "induction wearing a different hat "
     "(Module 03 §4).",
     "",
     "<b>But a great many contradiction proofs are direct proofs "
     "with an unused assumption</b> — <b>if you never actually "
     "used 'not Q' to reach the contradiction, you proved it "
     "directly</b> and should say so.",
     "",
     "<b>Which is worth checking every time</b>: <b>find the step "
     "where 'not Q' was used</b>, and if there is none, rewrite "
     "it.",
     "",
     "<b>And a contradiction proof is harder to read</b>, because "
     "the reader must hold a false assumption throughout — which "
     "is a cost to the reader you should pay only when it buys "
     "something.",
   ],
   "footnote": "<b>If you never used 'not Q', you proved it "
               "directly</b> — which is worth checking every time, "
               "and rewriting when it is "
               "true."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "From the shape, before you start."},

  {"t": "callout", "title": "The statement's shape tells you which technique to try, which turns being stuck into a procedure",
   "kind": "Closing",
   "body": ["<b>'For all x, if P then Q' → try direct; if P is "
            "unhelpful, contrapositive.</b>",
            "<b>'There is no x such that...' → "
            "contradiction</b>, almost always, because you need the "
            "object in order to argue about it.",
            "<b>'For all n ≥ 1' with n in the statement → "
            "induction</b> (Module 03), which is the "
            "single most reliable signal in this "
            "course.",
            "<b>And 'there exists an x' → construct one</b>, or "
            "count and show the count is non-zero — <b>which is the "
            "existence proof's two flavours</b>, constructive and "
            "not."]},
 ],
 "takeaways": [
   "Almost every statement in the program has the form 'for all x, if P(x) "
   "then Q(x)', and the shape tells you how to start.",
   "Quantifier order matters absolutely, and English hides the "
   "distinction.",
   "Negation is mechanical: flip each quantifier left to right and negate "
   "the inside.",
   "Try direct, then contrapositive, then contradiction — in that "
   "order, because each is harder to get right.",
   "If the hypothesis is hard to use and the negated conclusion is easy, "
   "take the contrapositive.",
   "If you never used 'not Q', you proved it directly and should say so.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Statements"),
  ("callout", "Almost every statement in this program has the form 'for all "
              "x, if P(x) then Q(x)'",
   ["<b>'Every even integer greater than two is the sum of two "
    "primes'</b>; <b>'if a graph is connected then it has a spanning "
    "tree'</b>; <b>'if the input is sorted then binary search "
    "terminates in O(log n) steps'</b> — <b>all the same "
    "shape</b>, <b>and the shape tells you how to start</b> "
    "(&sect;4).",
    "<b>The order of the quantifiers matters absolutely:</b> "
    "<b>'for every x there is a y such that R(x,y)' and 'there is a y "
    "such that for every x, R(x,y)' are different statements</b>, "
    "<b>and the second is much stronger</b> — it demands one y "
    "that works for all x at once.",
    "<b>Which is the commonest source of a wrong proof in this "
    "course</b> — <b>proving the weak one and claiming the strong "
    "one</b> — <b>and it happens because English hides the "
    "distinction</b>: 'everyone has a favourite colour' and 'there is a "
    "colour everyone favours' are both natural readings of a careless "
    "sentence.",
    "<b>So write the quantifiers out, in order, before you "
    "start</b> — <b>which costs one line and settles what you are "
    "actually trying to prove</b>, and which Project 1 asks you to do "
    "at the top of every proof."]),
  ("code", """THE RULES
    not (for all x, P(x))     =  exists x, not P(x)
    not (exists x, P(x))      =  for all x, not P(x)
    not (P and Q)             =  not P or not Q
    not (P or Q)              =  not P and not Q
    not (if P then Q)         =  P and not Q
        <-- this one surprises people

SO TO NEGATE
    walk the quantifiers left to right, flipping each
    one, and negate the innermost statement.

EXAMPLE
    "for every e > 0 there is an N such that for all
     n > N, |a_n - L| < e"
negates to
    "there is an e > 0 such that for every N there
     is an n > N with |a_n - L| >= e"

WHICH IS MECHANICAL. You never have to think about
what the negation "means" -- apply the rules, then
read the result and see what it says."""),
  ("p", "<b>Negation is mechanical</b> — <b>flip each quantifier "
        "left to right and negate the inside</b>, <b>and never reason "
        "about what the negation 'means'</b> until after you have "
        "written it down. <b>Negating correctly is what makes "
        "contradiction and contrapositive usable at all</b> (&sect;&sect;2 "
        "and 3), since both techniques begin by negating something, and "
        "a wrong negation produces a proof of a different "
        "statement."),

  ("h1", "2 &nbsp; The three techniques"),
  ("table", ["Technique", "You assume", "Best when"],
   [["<b>Direct</b>", "<b>P, and derive Q.</b>",
     "<b>P gives you something concrete to work with</b> — an "
     "equation, a structure, a number."],
    ["<b>Contrapositive</b>", "<b>not Q, and derive not P.</b>",
     "<b>'not Q' is more concrete than P</b> — see the "
     "callout."],
    ["<b>Contradiction</b>",
     "<b>P and not Q together, and derive something false.</b>",
     "<b>The claim is a non-existence or an impossibility</b> "
     "(&sect;3)."],
    ["<b>Cases</b>", "<b>Each possibility in turn, exhaustively.</b>",
     "<b>The situation genuinely splits</b> — and you must check "
     "the cases are exhaustive, which is where this goes wrong."],
    ["<b>Counterexample</b>", "<b>—</b>",
     "<b>You suspect the statement is false</b> (Module 01 "
     "&sect;2)."]],
   [0.20, 0.36, 0.44]),
  ("p", "<b>Try direct first, then contrapositive, then "
        "contradiction</b> — <b>in that order, because each is "
        "harder to get right than the one before it</b>, and because a "
        "direct proof is the easiest for a reader to check. <b>The "
        "ordering is this section's practical content</b>: most people "
        "learning proof reach for contradiction far too early, because it "
        "feels powerful and because it always <i>starts</i> easily."),
  ("callout", "Contrapositive is underused, and it is frequently the whole "
              "difficulty",
   ["<b>'If n<super>2</super> is even then n is even' is awkward "
    "directly</b> — you know something about n<super>2</super> and "
    "want a conclusion about n, <b>which is the wrong direction</b>: "
    "you would have to take a square root and argue about parity.",
    "<b>The contrapositive is 'if n is odd then n<super>2</super> "
    "is odd'</b> — <b>and now you can write n = 2k + 1, square it, "
    "and read off the answer</b>, which takes one line and no "
    "cleverness.",
    "<b>So the rule of thumb: if the hypothesis is hard to use and "
    "the negated conclusion is easy to use, take the "
    "contrapositive</b> — <b>which is a mechanical test you can "
    "apply before starting</b> rather than a judgement that comes with "
    "experience.",
    "<b>And it is logically identical, not weaker</b> — <b>'if "
    "P then Q' and 'if not Q then not P' are the same statement</b>, "
    "with the same truth value in every case — <b>so nothing is "
    "given up</b> by the substitution, which is why it is free."]),

  ("break",),
  ("h1", "3 &nbsp; Contradiction"),
  ("ul", ["<b>It is the right tool for non-existence</b> — "
          "<b>'there is no largest prime', 'the square root of two is "
          "not rational', 'no algorithm decides the halting "
          "problem'</b> — because <b>assuming the thing exists "
          "hands you an object to work with</b>, and otherwise you have "
          "nothing to argue about.",
          "<b>And for minimal-counterexample arguments</b>: assume "
          "the statement fails somewhere, take the smallest failure, and "
          "derive a smaller one — <b>which is induction wearing a "
          "different hat</b> (Module 03 &sect;4).",
          "<b>But a great many contradiction proofs are direct "
          "proofs with an unused assumption</b> — <b>if you never "
          "actually used 'not Q' anywhere in reaching the "
          "contradiction, then what you proved was Q directly</b>, and "
          "you should say so.",
          "<b>Which is worth checking every single time</b>: "
          "<b>find the step where 'not Q' was used</b>, point at it, "
          "and <b>if there is no such step, rewrite the proof as a "
          "direct one</b>. This is Module 01 &sect;3's "
          "where-was-the-hypothesis-used question, turned on your own "
          "work.",
          "<b>And a contradiction proof is harder to read</b>, "
          "because <b>the reader has to hold a false assumption in mind "
          "throughout and cannot trust any intermediate result</b> "
          "— which is a real cost to impose on a reader, and should "
          "be paid only when it buys something."]),

  ("h1", "4 &nbsp; Choosing"),
  ("callout", "The statement's shape tells you which technique to try, which "
              "turns being stuck into a procedure",
   ["<b>'For all x, if P then Q' &rarr; try direct</b>; <b>and if P "
    "turns out to be unhelpful, take the contrapositive</b> "
    "(&sect;2's callout gives the test).",
    "<b>'There is no x such that...' &rarr; contradiction</b>, "
    "almost always — <b>because you need the object in hand in "
    "order to argue about it</b>, and the assumption is what hands it "
    "to you.",
    "<b>'For all n &ge; 1' with n appearing in the statement "
    "&rarr; induction</b> (Module 03) — <b>which is the single "
    "most reliable signal in this course</b>: if the statement is "
    "indexed by a natural number, induction is the first thing to "
    "try.",
    "<b>And 'there exists an x such that...' &rarr; construct "
    "one</b>, explicitly, <b>or count the possibilities and show the "
    "count is non-zero</b> — <b>which is the existence proof's two "
    "flavours</b>, constructive and non-constructive, and the second is "
    "what Module 11 &sect;4's probabilistic method does."]),
 ],
 "resources": [
   ("Velleman &mdash; How to Prove It, chapters 1 to 3",
    "https://www.cambridge.org/9781108424189",
    "<b>The whole module</b> — and the quantifier chapter is worth "
    "more than its length suggests. Library copy."),
   ("Lehman, Leighton & Meyer, chapters 1 and 3 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>&sect;&sect;1 to 3</b>, free — with propositional logic "
    "developed enough to make the negation rules obvious."),
   ("MIT 6.042J lectures 1 and 2 (free video)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/video_galleries/video-lectures/",
    "<b>&sect;&sect;2 and 3</b> — the techniques demonstrated on real "
    "statements rather than described."),
   ("Hammack &mdash; Book of Proof (free)",
    "https://www.people.vcu.edu/~rhammack/BookOfProof/",
    "<b>The whole module, free in full</b> — and it has far more "
    "worked examples than this course can include."),
 ],
 "exercises": [
   "<b>Write five statements</b> from a textbook with their "
   "quantifiers made explicit.",
   "<b>Find a pair</b> where swapping two quantifiers changes the "
   "meaning, and say how.",
   "<b>Negate ten statements</b> mechanically, including three with "
   "nested quantifiers.",
   "<b>Negate 'if P then Q'</b> and explain why the result has no "
   "'if'.",
   "<b>Prove three things directly.</b>",
   "<b>Prove three by contrapositive</b>, and say why direct was "
   "awkward.",
   "<b>Prove that the square root of two is irrational.</b>",
   "<b>Find a published contradiction proof</b> that is really a "
   "direct proof, and rewrite it.",
   "<b>Prove something by cases</b>, and justify that the cases are "
   "exhaustive.",
   "<b>For ten statements, name the technique</b> you would try "
   "first, from the shape alone.",
 ],
 "selfcheck": [
   "What shape do most statements have, and why does that help?",
   "Why does quantifier order matter, and what is the common error?",
   "Give the five negation rules.",
   "Negate 'if P then Q', and explain the result.",
   "Name the techniques and the order to try them in.",
   "When is contrapositive the right move?",
   "Why is it not weaker than a direct proof?",
   "When does contradiction earn its keep?",
   "How do you check a contradiction proof is not secretly direct?",
   "Map four statement shapes onto techniques.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Induction",
 "subtitle": "The technique computer science uses most, and does "
             "worst.",
 "question": "Why is it enough to prove one case and one step?",
 "outcomes": [
     "State and apply ordinary induction.",
     "Explain why the base case is not a formality.",
     "Use strong induction and say when it is needed.",
     "Use structural induction on recursive objects.",
     "Recognise and avoid the standard induction errors.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The principle",
   "blurb": "And why it is not circular."},

  {"t": "callout", "title": "Prove it for the first case, and prove that each case forces the next — then every case follows",
   "kind": "The principle, and the reason it works",
   "body": ["<b>Base case: the statement holds for n = 1</b> (or "
            "wherever you start). <b>Inductive step: if it holds for n, "
            "it holds for n + 1.</b> <b>Conclusion: it holds for "
            "all n.</b>",
            "<b>And it is not circular, which is the thing to get "
            "clear:</b> <b>the step does not assume the statement is "
            "true</b> — <b>it proves an implication</b>, which is a "
            "different claim.",
            "<b>The image is dominoes</b>: you check the first falls, "
            "and you check that each falling knocks over the next — "
            "<b>and neither check assumes they all fall.</b>",
            "<b>Which is why both halves are "
            "required</b>: <b>dominoes correctly spaced but never "
            "pushed stay standing</b>, and that is a base case failure "
            "rather than a technicality "
            "(Part 2)."]},

  {"t": "code", "kicker": "Form", "title": "The shape to write, every time",
   "lang": "text", "code": """
  CLAIM: for all n >= 1, P(n).

  BASE CASE.  P(1): <show it, explicitly>

  INDUCTIVE STEP.  Let n >= 1 and SUPPOSE P(n).
      <this supposition is the inductive hypothesis;
       say so, and use the words>
      ... derivation ...
      Therefore P(n+1).

  By induction, P(n) holds for all n >= 1.  []

  THREE THINGS THAT MUST APPEAR
      1  the base case, computed and not asserted
      2  the words "suppose P(n)" -- naming the
         inductive hypothesis explicitly
      3  the place where you USED it

  AND IF YOU CANNOT POINT AT (3), THE PROOF IS WRONG.
  This is the single most common error in the course,
  and it is detectable in ten seconds.
""",
   "caption": "<b>Point at the place where the inductive hypothesis "
              "was used</b> — if you cannot, the proof is wrong, and "
              "this is detectable in ten "
              "seconds.",
   "note": "Project 1 marks every induction proof against these "
           "three requirements."},

  {"t": "section", "label": "Part 2", "title": "The base case",
   "blurb": "Which is not a formality."},

  {"t": "callout", "title": "A valid inductive step with a false base case proves a false statement",
   "kind": "Why the one-line case deserves attention",
   "body": ["<b>'All horses are the same colour' has a perfectly "
            "valid-looking inductive step</b> and fails at the "
            "transition from one horse to two — <b>which is a base case "
            "problem in disguise</b>.",
            "<b>And 'n = n + 1' has a flawless inductive "
            "step</b>: assume it, add one to both sides, done. "
            "<b>Only the base case stops it</b>, and there is no base "
            "case.",
            "<b>So check the base case by computing it</b>, not by "
            "asserting it — <b>and check that the step actually works "
            "from the base</b>, which is where the horses "
            "fail.",
            "<b>Which is a general discipline:</b> <b>the step from "
            "the base is the one most likely to be special</b>, and "
            "checking n = 2 explicitly costs nothing and catches "
            "it."]},

  {"t": "section", "label": "Part 3", "title": "Strong induction",
   "blurb": "When one predecessor is not enough."},

  {"t": "eq", "kicker": "Strong induction", "title": "Assuming all the way down",
   "eqs": [
     ("ordinary: assume P(n), prove P(n+1)",
      "One predecessor. Enough when the object of size n+1 decomposes "
      "into one of size n."),
     ("strong: assume P(1), ..., P(n), prove P(n+1)",
      "All predecessors. Needed when the decomposition is into two "
      "pieces of unknown size — which is what every "
      "divide-and-conquer argument does."),
     ("and they are equivalent in power, not in convenience",
      "Strong induction proves nothing ordinary induction cannot, "
      "and it is frequently the only one you can actually write."),
   ],
   "caption": "<b>Strong induction is needed whenever the object "
              "splits into two pieces of unknown size</b> — which is "
              "every divide-and-conquer "
              "argument.",
   "note": "CSCE 629 uses strong induction constantly and will not "
           "flag it."},

  {"t": "bullets", "kicker": "Structural", "title": "And structural induction, which is the same idea on trees",
   "items": [
     "<b>A recursively defined object has base cases and "
     "construction rules</b> — <b>and you induct on the "
     "construction</b> rather than on a number.",
     "",
     "<b>A tree is a leaf, or a node with two subtrees</b> — "
     "<b>so prove it for a leaf, and prove it for a node assuming both "
     "subtrees</b>.",
     "",
     "<b>Which is exactly how every property of a recursive data "
     "structure gets proved</b>, and is the form CSCE 629 and "
     "CSCE 605 use most.",
     "",
     "<b>And a recursive program's correctness is a structural "
     "induction on its input</b> — <b>base case is the base case, "
     "and the inductive hypothesis is that the recursive calls "
     "work</b>.",
     "",
     "<b>Which is why induction is the technique to be fluent "
     "in</b>: it is how you reason about recursion, and recursion is "
     "everywhere.",
   ],
   "footnote": "<b>A recursive program's correctness proof is a "
               "structural induction, and the inductive hypothesis is "
               "'the recursive calls work'</b> — which is why this "
               "feels like cheating and is not."},

  {"t": "section", "label": "Part 4", "title": "The standard errors",
   "blurb": "All five of them, which is most of what goes wrong."},

  {"t": "callout", "title": "Five errors account for nearly every broken induction proof",
   "kind": "Closing",
   "body": ["<b>1 · No base case, or asserted rather than "
            "computed</b> (Part 2). <b>2 · The inductive "
            "hypothesis never used</b> — the proof is something else "
            "(Part 1).",
            "<b>3 · Proving P(n+1) from scratch</b>, which is not "
            "induction and usually means you did not need "
            "it. <b>4 · Assuming what you are proving</b>, which is "
            "circular and feels fine while writing "
            "it.",
            "<b>5 · Using strong induction's extra assumptions "
            "without declaring it</b> — <b>which is the subtle one</b>, "
            "and is why Part 3 is worth being explicit "
            "about.",
            "<b>And all five are detectable by one "
            "question:</b> <b>point at the line where the hypothesis "
            "was used, and say which predecessors it needed</b> — "
            "which is the audit Project 2 asks you to run on your own "
            "earlier proofs."]},
 ],
 "takeaways": [
   "Induction is not circular: the step proves an implication, not the "
   "statement.",
   "Point at the place where the inductive hypothesis was used — if "
   "you cannot, the proof is wrong.",
   "A valid inductive step with a false base case proves a false "
   "statement.",
   "The step from the base is the one most likely to be special, so check "
   "n = 2 explicitly.",
   "Strong induction is needed whenever the object splits into two pieces "
   "of unknown size.",
   "A recursive program's correctness proof is a structural induction whose "
   "hypothesis is 'the recursive calls work'.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The principle"),
  ("callout", "Prove it for the first case, and prove that each case forces "
              "the next — then every case follows",
   ["<b>Base case: the statement holds for n = 1</b>, or wherever "
    "you start. <b>Inductive step: if it holds for n, then it holds for "
    "n + 1.</b> <b>Conclusion: it holds for every n from the base "
    "onward.</b>",
    "<b>And it is not circular, which is the thing to get clear "
    "early:</b> <b>the inductive step does not assume the statement is "
    "true</b> — <b>it proves an implication</b>, 'if P(n) then "
    "P(n+1)', <b>which is a different and weaker claim</b> that can be "
    "established without knowing whether P(n) holds.",
    "<b>The image is a line of dominoes</b>: you check that the "
    "first one falls, and you check that each one falling knocks over "
    "the next — <b>and neither of those checks assumes that they "
    "all fall.</b>",
    "<b>Which is also why both halves are genuinely "
    "required</b>: <b>dominoes correctly spaced but never pushed stay "
    "standing forever</b>, <b>and that is a base case failure rather "
    "than a technicality</b> (&sect;2)."]),
  ("code", """CLAIM: for all n >= 1, P(n).

BASE CASE.  P(1): <show it, explicitly>

INDUCTIVE STEP.  Let n >= 1 and SUPPOSE P(n).
    <this supposition is the inductive hypothesis;
     say so, and use the words>
    ... derivation ...
    Therefore P(n+1).

By induction, P(n) holds for all n >= 1.  []

THREE THINGS THAT MUST APPEAR
    1  the base case, computed and not asserted
    2  the words "suppose P(n)" -- naming the
       inductive hypothesis explicitly
    3  the place where you USED it

AND IF YOU CANNOT POINT AT (3), THE PROOF IS WRONG.
This is the single most common error in the course,
and it is detectable in about ten seconds."""),
  ("p", "<b>Point at the place where the inductive hypothesis was "
        "used</b> — <b>if you cannot, the proof is wrong</b>, and "
        "<b>this is detectable in ten seconds</b> by somebody who knows "
        "to look, including you. <b>Project 1 marks every induction "
        "proof against these three requirements</b>, and Project 2's "
        "self-audit is largely a matter of re-running this check on "
        "proofs you wrote six weeks earlier."),

  ("h1", "2 &nbsp; The base case"),
  ("callout", "A valid inductive step with a false base case proves a false "
              "statement",
   ["<b>'All horses are the same colour' has a perfectly "
    "valid-looking inductive step</b> — any n horses are the same "
    "colour, so overlap two groups of n to get n + 1 — <b>and it "
    "fails precisely at the transition from one horse to two</b>, where "
    "the two groups do not overlap. <b>Which is a base case problem in "
    "disguise</b>: the step is valid from n = 2 onward and the base is "
    "at n = 1.",
    "<b>And 'n = n + 1' has a flawless inductive step</b>: assume "
    "it, add one to both sides, and you have the next case. <b>Only the "
    "absence of a base case stops it</b>, and there is no base case to "
    "be had.",
    "<b>So check the base case by computing it</b>, not by "
    "asserting that it is obvious — and separately <b>check that "
    "the step actually works starting from the base</b>, <b>which is "
    "exactly where the horses fail</b> and where a valid-looking "
    "argument hides a gap.",
    "<b>Which generalises into a discipline:</b> <b>the step from "
    "the base is the one most likely to be special</b>, because it is "
    "the smallest and degenerate cases live there — <b>and checking "
    "n = 2 explicitly costs nothing and catches it</b>."]),

  ("break",),
  ("h1", "3 &nbsp; Strong induction"),
  ("eq", "ordinary: assume P(n), prove P(n+1)&nbsp;&nbsp;&nbsp;&nbsp; "
         "strong: assume P(1) &hellip; P(n), prove P(n+1)"),
  ("ul", ["<b>Ordinary induction gives you one predecessor</b>, and "
          "<b>that is enough whenever an object of size n + 1 "
          "decomposes into one of size n</b> plus something you can "
          "handle directly.",
          "<b>Strong induction gives you all the predecessors</b>, "
          "and <b>it is needed when the decomposition is into two "
          "pieces of unknown size</b> — <b>which is what every "
          "divide-and-conquer argument does</b>: a problem of size n "
          "splits into pieces of size k and n &minus; k, and you do not "
          "control k.",
          "<b>And the two are equivalent in power, not in "
          "convenience</b> — <b>strong induction proves nothing "
          "that ordinary induction cannot</b> (the standard trick is to "
          "induct on 'P holds for everything up to n') — <b>and it "
          "is frequently the only one you can actually write "
          "down</b>.",
          "<b>Strong induction is needed whenever the object splits "
          "into two pieces of unknown size</b>, and <b>CSCE 629 uses it "
          "constantly and will not flag it</b>: every merge sort, "
          "quicksort, and binary search correctness argument is a strong "
          "induction, usually written without the word."]),
  ("ul", ["<b>A recursively defined object has base cases and "
          "construction rules</b> — <b>and you induct on the "
          "construction</b> rather than on a natural number, which is "
          "structural induction.",
          "<b>A binary tree is a leaf, or a node with two "
          "subtrees</b> — <b>so prove the property for a leaf, and "
          "prove it for a node while assuming it holds for both "
          "subtrees</b>, and you are done.",
          "<b>Which is exactly how every property of a recursive "
          "data structure gets proved</b>, and <b>is the form CSCE 629 "
          "and CSCE 605 use most</b> — tree heights, parser "
          "correctness, and the properties of expression grammars are "
          "all this.",
          "<b>And a recursive program's correctness is a structural "
          "induction on its input</b> — <b>the base case is the "
          "program's base case, and the inductive hypothesis is that the "
          "recursive calls work</b> — <b>which is why this feels "
          "like cheating the first few times and is not</b>: you are "
          "proving an implication, as always.",
          "<b>Which is why induction is the technique to be fluent "
          "in rather than merely acquainted with</b>: <b>it is how you "
          "reason about recursion, and recursion is everywhere in this "
          "program.</b>"]),

  ("h1", "4 &nbsp; The standard errors"),
  ("callout", "Five errors account for nearly every broken induction proof",
   ["<b>1 &middot; No base case, or a base case asserted rather than "
    "computed</b> (&sect;2). <b>2 &middot; The inductive hypothesis is "
    "never used</b> — in which case the proof is something else, "
    "possibly a correct direct proof (&sect;1's three "
    "requirements).",
    "<b>3 &middot; Proving P(n+1) from scratch</b> — which is "
    "not induction at all, and usually means you did not need induction "
    "and should say so. <b>4 &middot; Assuming what you are "
    "proving</b> — assuming P(n+1) somewhere in the derivation of "
    "P(n+1), <b>which is circular and feels entirely fine while you are "
    "writing it.</b>",
    "<b>5 &middot; Using strong induction's extra assumptions "
    "without having declared strong induction</b> — reaching back "
    "to P(k) for some k &lt; n in a proof that only supposed "
    "P(n) — <b>which is the subtle one</b>, and is <b>why "
    "&sect;3 is worth being explicit about</b>: the fix is one word in "
    "the hypothesis.",
    "<b>And all five are detectable by a single question:</b> "
    "<b>point at the line where the hypothesis was used, and say which "
    "predecessors it needed</b> — <b>which is the audit Project 2 "
    "asks you to run on your own earlier proofs</b>, and which reliably "
    "finds something."]),
 ],
 "resources": [
   ("Lehman, Leighton & Meyer, chapter 5 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>The whole module</b>, free — and the false induction proofs "
    "it works through are the best part."),
   ("MIT 6.042J, the induction lectures (free video)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/video_galleries/video-lectures/",
    "<b>&sect;&sect;1 to 3</b>, with the horses example done "
    "properly."),
   ("Hammack &mdash; Book of Proof, chapter 10 (free)",
    "https://www.people.vcu.edu/~rhammack/BookOfProof/",
    "<b>&sect;&sect;1 and 3</b> — many worked examples, free, and "
    "strong induction is handled carefully."),
   ("CLRS, the loop invariant material (library copy)",
    "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/",
    "<b>&sect;3's application</b> — loop invariants are induction on "
    "iterations, and this is the form CSCE 629 will use from week "
    "one."),
 ],
 "exercises": [
   "<b>Explain why induction is not circular</b>, in three "
   "sentences.",
   "<b>Prove the sum of the first n integers</b> formula, with all "
   "three requirements visible.",
   "<b>Find the flaw in the horses proof</b> precisely, and say which "
   "step fails.",
   "<b>Construct your own false induction</b> with a valid-looking "
   "step.",
   "<b>Prove something needing strong induction</b>, and say why "
   "ordinary fails.",
   "<b>Prove every integer above 1 has a prime factorisation.</b>",
   "<b>Prove a property of binary trees</b> by structural "
   "induction.",
   "<b>Prove a recursive function correct</b>, stating the hypothesis "
   "explicitly.",
   "<b>Take five of your own induction proofs</b> and point at the "
   "hypothesis use in each.",
   "<b>Find one of your proofs that uses strong induction</b> without "
   "declaring it.",
 ],
 "selfcheck": [
   "State the principle and explain why it is not circular.",
   "Give the three things that must appear in the write-up.",
   "What is the ten-second check?",
   "Why is a base case not a formality? Give two examples.",
   "Where does the horses proof fail, exactly?",
   "Contrast ordinary and strong induction, and say when each is "
   "needed.",
   "Are they equivalent in power? In convenience?",
   "Describe structural induction on trees.",
   "What is the inductive hypothesis in a recursive correctness "
   "proof?",
   "Name the five standard errors and the question that finds them "
   "all.",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Sets, Functions, Relations",
 "subtitle": "The vocabulary every later course assumes you have.",
 "question": "What does it mean for two infinite sets to be the same "
             "size?",
 "outcomes": [
     "Work with sets, operations, and power sets.",
     "Define functions precisely, and classify them.",
     "Use relations, equivalence, and partial orders.",
     "Compare infinite sets by bijection.",
     "Explain the diagonal argument.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Sets",
   "blurb": "And the operations that get used constantly."},

  {"t": "bullets", "kicker": "Sets", "title": "What you need fluently, and the two traps",
   "items": [
     "<b>Membership, subset, union, intersection, difference, "
     "complement</b> — and <b>the distinction between ∈ and "
     "⊆</b>, which is the first trap: <b>a set can be both an "
     "element and a subset of something.</b>",
     "",
     "<b>The power set has 2 to the n elements</b> for an "
     "n-element set — <b>which is the counting fact used most "
     "often in this program</b>, from CSCE 637 to "
     "CSCE 640.",
     "",
     "<b>Cartesian products and tuples</b>, which is how every "
     "relation and every graph edge is defined.",
     "",
     "<b>And the empty set is a subset of everything</b>, which "
     "is the second trap — <b>vacuously true statements are true</b>, "
     "and a proof that forgets the empty case is "
     "incomplete.",
     "",
     "<b>Plus: a set has no order and no repetition</b>, so "
     "{1,2} = {2,1} = {1,1,2} — and if you need order or "
     "repetition you wanted a sequence or a multiset.",
   ],
   "footnote": "<b>Vacuously true statements are true</b> — and a "
               "proof that forgets the empty case is incomplete, which "
               "is a common and quiet "
               "error."},

  {"t": "section", "label": "Part 2", "title": "Functions",
   "blurb": "Defined properly, because the definition is used."},

  {"t": "callout", "title": "A function assigns exactly one output to every input of its domain — and both halves are checkable conditions",
   "kind": "Why the pedantic definition earns its keep",
   "body": ["<b>Every element of the domain gets an output</b> "
            "(totality), and <b>exactly one</b> "
            "(well-definedness) — <b>and both are things that can "
            "fail</b>, especially when you define a function by a "
            "formula on equivalence classes.",
            "<b>Injective: different inputs give different "
            "outputs.</b> <b>Surjective: every element of the codomain "
            "is hit.</b> <b>Bijective: both</b> — and only a bijection "
            "has an inverse.",
            "<b>Which is the vocabulary CSCE 627 and CSCE 637 use "
            "without definition</b>, and which "
            "Part 4 needs.",
            "<b>And 'well-defined' is a real obligation</b>: <b>if "
            "you define f on a class by picking a "
            "representative, you must show the answer does not depend "
            "on which one</b> — a proof step people routinely "
            "skip."]},

  {"t": "section", "label": "Part 3", "title": "Relations",
   "blurb": "Which are more general and just as common."},

  {"t": "table", "kicker": "Relations", "title": "The properties, and the two combinations that matter",
   "header": ["Property", "Meaning", "Where it shows up"],
   "widths": [2.6, 4.2, 4.2],
   "rows": [
     ["<b>Reflexive</b>", "<b>Every element relates to itself</b>", "<b>Both of the below</b>"],
     ["<b>Symmetric</b>", "<b>If a~b then b~a</b>", "<b>Equivalence relations</b>"],
     ["<b>Antisymmetric</b>", "<b>a≤b and b≤a force a=b</b>", "<b>Partial orders</b>"],
     ["<b>Transitive</b>", "<b>a~b and b~c give a~c</b>", "<b>Both</b>"],
     ["<b>Equivalence</b>", "<b>Refl + sym + trans</b>", "<b>Partitions the set into classes</b>"],
     ["<b>Partial order</b>", "<b>Refl + antisym + trans</b>", "<b>Scheduling, type systems, lattices</b>"],
   ],
   "footnote": "<b>An equivalence relation and a partition are the "
               "same thing</b> — every equivalence relation splits "
               "the set into classes, and every partition defines "
               "one.",
   "note": "The equivalence-equals-partition correspondence is the "
           "fact to carry forward."},

  {"t": "section", "label": "Part 4", "title": "Infinite sets",
   "blurb": "Where the diagonal argument lives."},

  {"t": "callout", "title": "Two sets have the same size if a bijection exists between them — and this gives surprising answers",
   "kind": "The definition, and what follows from it",
   "body": ["<b>The integers and the even integers have the same "
            "size</b>, by n ↦ 2n — <b>which offends intuition and is "
            "the definition's consequence</b>, not a "
            "paradox.",
            "<b>And the rationals are countable too</b>, by a "
            "zigzag enumeration — <b>so 'more spread out' does not mean "
            "'bigger'.</b>",
            "<b>But the reals are not</b> — <b>Cantor's diagonal "
            "argument</b>: given any list of reals, construct one "
            "differing from the n-th in the n-th digit, so no list is "
            "complete.",
            "<b>Which is the single most reused argument in "
            "theoretical computer science</b> — <b>CSCE 627's "
            "undecidability and CSCE 637's hierarchy theorems are both "
            "diagonal arguments</b>, and recognising the shape is worth "
            "more than the result."]},

  {"t": "callout", "title": "And the counting consequence that matters for computing",
   "kind": "Closing",
   "body": ["<b>There are countably many programs</b> — each is a "
            "finite string over a finite alphabet — <b>and "
            "uncountably many functions from naturals to {0,1}.</b>",
            "<b>So almost every function is not computable by any "
            "program</b>, by counting alone — <b>before any "
            "halting-problem argument.</b>",
            "<b>Which is CSCE 627's opening result</b>, and it "
            "follows from this module rather than from anything about "
            "computation.",
            "<b>And it is a good demonstration of what counting "
            "arguments buy</b>: <b>a sweeping conclusion from no "
            "machinery</b>, which is a pattern worth looking for."]},
 ],
 "takeaways": [
   "Vacuously true statements are true, and a proof that forgets the empty "
   "case is incomplete.",
   "A function must be total and well-defined, and both are conditions that "
   "can fail.",
   "'Well-defined' is a real obligation when you define something on "
   "equivalence classes.",
   "An equivalence relation and a partition are the same thing.",
   "Two sets have the same size if a bijection exists, which gives answers "
   "that offend intuition and are not paradoxes.",
   "There are countably many programs and uncountably many functions, so "
   "almost every function is uncomputable — by counting alone.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Sets"),
  ("ul", ["<b>Membership, subset, union, intersection, difference, and "
          "complement</b> — and <b>the distinction between "
          "&isin; and &sube;</b>, which is the first trap: <b>a set can "
          "be both an element of and a subset of the same thing</b>, and "
          "confusing the two produces statements that are not merely "
          "false but meaningless.",
          "<b>The power set of an n-element set has "
          "2<sup>n</sup> elements</b> — <b>which is the counting "
          "fact used most often in this program</b>, from CSCE 637's "
          "counting argument for circuit lower bounds to CSCE 640's "
          "amplitude count to CSCE 717's valuation functions.",
          "<b>Cartesian products and tuples</b>, <b>which is how "
          "every relation (&sect;3) and every graph edge "
          "(Module 07) is formally defined</b>, and is worth being "
          "comfortable with even though it is rarely written out.",
          "<b>And the empty set is a subset of every set</b>, which "
          "is the second trap — <b>vacuously true statements are "
          "true</b> ('every element of the empty set is purple' is "
          "true) — <b>and a proof that forgets the empty case is "
          "incomplete</b>, which is a common and very quiet error.",
          "<b>Plus: a set has no order and no repetition</b>, so "
          "{1,2} = {2,1} = {1,1,2} — <b>and if you need order or "
          "repetition, you wanted a sequence or a multiset</b> and "
          "should say so."]),

  ("h1", "2 &nbsp; Functions"),
  ("callout", "A function assigns exactly one output to every input of its "
              "domain — and both halves are checkable conditions",
   ["<b>Every element of the domain gets an output</b> "
    "(totality), and <b>exactly one output</b> (well-definedness) "
    "— <b>and both of these are things that can actually fail</b>, "
    "especially when you define a function by a formula applied to "
    "equivalence classes or by a procedure that might not "
    "terminate.",
    "<b>Injective (one-to-one): different inputs give different "
    "outputs.</b> <b>Surjective (onto): every element of the codomain "
    "is hit by something.</b> <b>Bijective: both</b> — and <b>only "
    "a bijection has an inverse function</b>, which is why &sect;4's "
    "size definition uses bijections specifically.",
    "<b>Which is the vocabulary CSCE 627 and CSCE 637 use without "
    "stopping to define</b>, and <b>which &sect;4 needs</b> "
    "immediately.",
    "<b>And 'well-defined' is a real proof obligation rather than a "
    "pleasantry</b>: <b>if you define f on an equivalence class by "
    "picking a representative and computing with it, you must show the "
    "answer does not depend on which representative you picked</b> "
    "— <b>a step people routinely skip</b>, and one of the places "
    "modular arithmetic (Module 05) requires care."]),

  ("break",),
  ("h1", "3 &nbsp; Relations"),
  ("table", ["Property", "Meaning", "Where it shows up"],
   [["<b>Reflexive</b>", "<b>Every element relates to itself.</b>",
     "<b>Both equivalences and partial orders.</b>"],
    ["<b>Symmetric</b>", "<b>If a ~ b then b ~ a.</b>",
     "<b>Equivalence relations.</b>"],
    ["<b>Antisymmetric</b>",
     "<b>a &le; b and b &le; a together force a = b.</b>",
     "<b>Partial orders</b> — and note this is not the negation of "
     "symmetric."],
    ["<b>Transitive</b>", "<b>a ~ b and b ~ c give a ~ c.</b>",
     "<b>Both.</b> This is the one most often assumed without "
     "checking."],
    ["<b>Equivalence relation</b>",
     "<b>Reflexive + symmetric + transitive.</b>",
     "<b>Partitions the set into disjoint classes</b> — see the "
     "note."],
    ["<b>Partial order</b>",
     "<b>Reflexive + antisymmetric + transitive.</b>",
     "<b>Scheduling and dependency graphs, type systems, lattices</b> "
     "— and CSCE 605 uses them heavily."]],
   [0.20, 0.38, 0.42]),
  ("p", "<b>An equivalence relation and a partition are the same "
        "thing</b> — <b>every equivalence relation splits its set "
        "into disjoint classes, and every partition into disjoint classes "
        "defines an equivalence relation</b> — which is worth "
        "proving once and then using freely. <b>The "
        "equivalence-equals-partition correspondence is the fact to carry "
        "forward</b>: modular arithmetic (Module 05) is entirely an "
        "application of it."),

  ("h1", "4 &nbsp; Infinite sets"),
  ("callout", "Two sets have the same size if a bijection exists between them "
              "— and this gives surprising answers",
   ["<b>The integers and the even integers have the same size</b>, "
    "by the bijection n &rarr; 2n — <b>which offends intuition, and "
    "is a consequence of the definition rather than a paradox</b>. For "
    "infinite sets, a proper subset can be the same size as the whole; "
    "that is what infinite means.",
    "<b>And the rationals are countable too</b>, by a zigzag "
    "enumeration of the grid of numerators and denominators — "
    "<b>so 'more densely packed' does not mean 'bigger'</b> "
    "either.",
    "<b>But the reals are not countable</b> — <b>Cantor's "
    "diagonal argument</b>: given any proposed list of all reals, "
    "construct a new one that differs from the first in its first digit, "
    "from the second in its second, and so on, <b>so no list can be "
    "complete</b>.",
    "<b>Which is the single most reused argument in theoretical "
    "computer science</b> — <b>CSCE 627's undecidability result "
    "and CSCE 637's hierarchy theorems are both diagonal "
    "arguments</b> — and <b>recognising the shape is worth more "
    "than remembering the result</b>."]),
  ("callout", "And the counting consequence that matters for computing",
   ["<b>There are countably many programs</b> — each one is a "
    "finite string over a finite alphabet, and the set of finite strings "
    "is countable — <b>and there are uncountably many functions "
    "from the naturals to {0,1}</b>, by the diagonal argument.",
    "<b>So almost every function is not computable by any "
    "program</b>, <b>by counting alone</b> — <b>before any "
    "halting-problem argument, and without any model of "
    "computation</b> beyond 'programs are finite strings'.",
    "<b>Which is CSCE 627's opening result</b>, and <b>it follows "
    "from this module rather than from anything about computation</b>, "
    "which is a surprising place for it to come from.",
    "<b>And it is a good demonstration of what counting arguments "
    "buy you</b>: <b>a sweeping conclusion from essentially no "
    "machinery</b> — <b>a pattern worth looking for</b>, and one "
    "Module 06 develops properly."]),
 ],
 "resources": [
   ("Lehman, Leighton & Meyer, chapters 4 and 8 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>&sect;&sect;1 to 4</b>, free — and the infinite-sets chapter "
    "is unusually careful."),
   ("Velleman, chapters 4 and 5",
    "https://www.cambridge.org/9781108424189",
    "<b>&sect;&sect;2 and 3</b> — relations and functions with the "
    "well-definedness obligation made explicit. Library copy."),
   ("Hammack &mdash; Book of Proof, chapters 11 and 14 (free)",
    "https://www.people.vcu.edu/~rhammack/BookOfProof/",
    "<b>&sect;&sect;3 and 4</b>, free — relations, and cardinality "
    "with the diagonal argument worked slowly."),
   ("Sipser, chapter 4 (library copy)",
    "https://www.cengage.com/c/introduction-to-the-theory-of-computation-3e-sipser/",
    "<b>&sect;4's consequence</b> — where the diagonal argument "
    "becomes undecidability, which is CSCE 627."),
 ],
 "exercises": [
   "<b>Give a set that is both an element and a subset</b> of "
   "another.",
   "<b>Prove the power set has 2ⁿ elements</b>, by induction.",
   "<b>Find a statement that is vacuously true</b> and explain why it "
   "is true.",
   "<b>Give a formula that fails to be well-defined</b> on "
   "equivalence classes.",
   "<b>Classify five functions</b> as injective, surjective, or "
   "bijective.",
   "<b>Check four relations</b> against all four properties.",
   "<b>Prove the equivalence-partition correspondence</b>, both "
   "directions.",
   "<b>Give a bijection</b> between the naturals and the "
   "integers.",
   "<b>Write out the diagonal argument</b> in full.",
   "<b>Count the programs and the functions</b>, and state the "
   "conclusion.",
 ],
 "selfcheck": [
   "Distinguish ∈ and ⊆ with an example.",
   "How many subsets does an n-element set have, and why?",
   "Why are vacuously true statements true, and what does that mean "
   "for proofs?",
   "Give the two conditions a function must satisfy.",
   "Define injective, surjective, bijective, and say which has an "
   "inverse.",
   "What is the well-definedness obligation?",
   "Name four relation properties and the two combinations.",
   "State the equivalence-partition correspondence.",
   "How are two infinite sets compared, and give a surprising "
   "consequence.",
   "State the diagonal argument and its counting consequence for "
   "programs.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Number Theory and Modular Arithmetic",
 "subtitle": "The arithmetic every hash, cipher, and index uses.",
 "question": "Why does the clock arithmetic you learned as a child "
             "underlie public-key cryptography?",
 "outcomes": [
     "Use the division algorithm and gcd fluently.",
     "Run the Euclidean algorithm, extended and not.",
     "Compute in modular arithmetic, including inverses.",
     "State and use Fermat's little theorem.",
     "Explain where this is used in the program.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Divisibility and gcd",
   "blurb": "The foundation, and the algorithm that computes it."},

  {"t": "code", "kicker": "Euclid", "title": "The oldest algorithm still in use",
   "lang": "text", "code": """
  DIVISION ALGORITHM
      for any a and b > 0 there are unique q, r with
          a = qb + r   and   0 <= r < b
      Unique. That uniqueness is what makes mod
      well-defined (Module 04 section 2).

  EUCLID'S ALGORITHM
      gcd(a, b) = gcd(b, a mod b),  gcd(a, 0) = a

      why it works: any common divisor of a and b
      divides a - qb = r, and conversely. So the
      pair (b, r) has the same common divisors as
      (a, b) -- and the numbers shrink.

      it runs in O(log min(a,b)) steps, which is
      why it is still used

  EXTENDED EUCLID
      also returns x, y with ax + by = gcd(a, b)
      -- Bezout's identity -- and x is how you
      compute modular inverses (section 3)
""",
   "caption": "<b>Extended Euclid gives you modular inverses</b>, "
              "which is the whole reason it matters for "
              "cryptography.",
   "note": "The uniqueness in the division algorithm is what makes "
           "everything later well-defined."},

  {"t": "section", "label": "Part 2", "title": "Modular arithmetic",
   "blurb": "Which is an equivalence relation, properly."},

  {"t": "callout", "title": "a ≡ b (mod n) means n divides a − b, and this is an equivalence relation",
   "kind": "Why Module 04's machinery was needed",
   "body": ["<b>It is reflexive, symmetric, and "
            "transitive</b> — so <b>it partitions the integers into n "
            "residue classes</b> "
            "(Module 04 §3).",
            "<b>And addition and multiplication are "
            "well-defined on the classes</b> — <b>which is the thing "
            "that has to be proved</b>, and which "
            "Module 04 §2 warned about.",
            "<b>So you can compute with remainders freely</b>, "
            "reducing at any point — <b>which is what makes modular "
            "exponentiation of enormous numbers "
            "tractable</b>.",
            "<b>But division is not automatic</b>: <b>a has a "
            "multiplicative inverse mod n exactly when "
            "gcd(a, n) = 1</b> — and extended Euclid computes it "
            "(Part 1)."]},

  {"t": "section", "label": "Part 3", "title": "The theorems",
   "blurb": "Three of them, and they do most of the work."},

  {"t": "eq", "kicker": "Theorems", "title": "What you actually use",
   "eqs": [
     ("Fermat: if p is prime and p does not divide a, "
      "then a^(p−1) ≡ 1 (mod p)",
      "Which gives inverses instantly mod a prime, and underlies "
      "primality testing."),
     ("Euler: a^φ(n) ≡ 1 (mod n) when gcd(a,n) = 1",
      "The generalisation to composite n. φ(n) counts the "
      "integers below n coprime to it — and RSA is this theorem."),
     ("Chinese remainder: congruences mod coprime moduli have a "
      "unique joint solution",
      "Which lets you work modulo the factors separately and "
      "recombine — used for speed, and in secret sharing."),
   ],
   "caption": "<b>RSA is Euler's theorem</b> — which is why "
              "CSCE 711 can treat it in one module rather than "
              "five.",
   "note": "These three are the whole number-theoretic toolkit this "
           "program needs."},

  {"t": "section", "label": "Part 4", "title": "Where it is used",
   "blurb": "Concretely, since the motivation is otherwise thin."},

  {"t": "bullets", "kicker": "Uses", "title": "Where this arithmetic turns up in the program",
   "items": [
     "<b>Hashing</b> — <b>every hash table's index is a mod "
     "operation</b>, and the choice of modulus determines the collision "
     "behaviour (CSCE 629, CSCE 658).",
     "",
     "<b>Public-key cryptography</b> — <b>RSA is Euler's "
     "theorem and Diffie-Hellman is modular "
     "exponentiation</b> (CSCE 711), and <b>Shor's algorithm attacks "
     "exactly the order-finding problem</b> "
     "(CSCE 640 §08).",
     "",
     "<b>Checksums and error detection</b> — CRC is "
     "polynomial arithmetic modulo a fixed polynomial, which is the "
     "same idea.",
     "",
     "<b>Random number generation</b> — linear congruential "
     "generators are a mod away from being useful, and understanding "
     "why they are weak needs this "
     "module.",
     "",
     "<b>And graphics</b>, less obviously — <b>wrapping texture "
     "coordinates, tiling, and hash-based procedural noise are all "
     "modular</b>.",
   ],
   "footnote": "<b>Hash-based procedural noise is modular "
               "arithmetic</b> — which is the one place this module "
               "touches the graphics track directly, and it touches it "
               "constantly."},

  {"t": "callout", "title": "And the thing to carry forward",
   "kind": "Closing",
   "body": ["<b>Modular arithmetic is the first place "
            "Module 04's well-definedness obligation is "
            "real</b> — <b>computing with a representative and "
            "claiming an answer about the class</b> is exactly the move "
            "that needs justifying.",
            "<b>And the Euclidean algorithm is the first "
            "non-trivial algorithm in the program</b> — <b>with a "
            "correctness argument and a complexity "
            "bound</b>, which is what CSCE 629 is "
            "about.",
            "<b>So prove Euclid correct and bound its "
            "running time</b>, by hand — <b>which is a complete "
            "exercise in everything Modules 01 through 03 "
            "taught</b>.",
            "<b>Which is why this module sits here</b> rather "
            "than later: <b>it is where the proof technique first pays "
            "for itself.</b>"]},
 ],
 "takeaways": [
   "The uniqueness in the division algorithm is what makes everything later "
   "well-defined.",
   "Euclid's algorithm works because (b, a mod b) has the same common "
   "divisors as (a, b), and runs in O(log min(a,b)).",
   "Extended Euclid gives you modular inverses, which is why it matters for "
   "cryptography.",
   "Congruence mod n is an equivalence relation, and addition and "
   "multiplication being well-defined on classes is a thing to prove.",
   "a has an inverse mod n exactly when gcd(a, n) = 1.",
   "RSA is Euler's theorem, which is why CSCE 711 can treat it in one "
   "module.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Divisibility and gcd"),
  ("code", """DIVISION ALGORITHM
    for any a and any b > 0 there are UNIQUE q, r
    with
        a = qb + r   and   0 <= r < b
    Unique. That uniqueness is exactly what makes
    "a mod b" well-defined (Module 04 section 2).

EUCLID'S ALGORITHM
    gcd(a, b) = gcd(b, a mod b),  gcd(a, 0) = a

    why it works: any common divisor of a and b also
    divides a - qb = r, and conversely any common
    divisor of b and r divides a. So the pair (b, r)
    has exactly the same common divisors as (a, b)
    -- and the numbers strictly shrink.

    it runs in O(log min(a,b)) steps, which is why
    it is still in use after two thousand years

EXTENDED EUCLID
    also returns x, y with ax + by = gcd(a, b)
    -- Bezout's identity -- and that x is how you
    compute modular inverses (section 3)"""),
  ("p", "<b>Extended Euclid gives you modular inverses</b>, <b>which "
        "is the whole reason it matters for cryptography</b>: if "
        "ax + ny = 1 then ax &equiv; 1 (mod n), so x is "
        "a<super>&minus;1</super>. <b>The uniqueness clause in the "
        "division algorithm is what makes everything later "
        "well-defined</b> — without it, 'a mod b' would not name a "
        "single number, and &sect;2's whole construction would "
        "collapse."),

  ("h1", "2 &nbsp; Modular arithmetic"),
  ("callout", "a &equiv; b (mod n) means n divides a &minus; b, and this is "
              "an equivalence relation",
   ["<b>It is reflexive, symmetric, and transitive</b> — each "
    "takes one line to check — <b>so it partitions the integers "
    "into n residue classes</b> (Module 04 &sect;3's "
    "equivalence-equals-partition correspondence, in its first serious "
    "application).",
    "<b>And addition and multiplication are well-defined on those "
    "classes</b> — <b>which is the thing that actually has to be "
    "proved</b>, and <b>which Module 04 &sect;2 warned about</b>: if "
    "a &equiv; a' and b &equiv; b', you must show "
    "ab &equiv; a'b', or computing with representatives is not "
    "legitimate.",
    "<b>Once proved, you can compute with remainders freely, "
    "reducing at any point in a calculation</b> — <b>which is what "
    "makes modular exponentiation of enormous numbers tractable</b>: "
    "you never hold the full value, only its residue (repeated squaring "
    "gives a<super>k</super> mod n in O(log k) multiplications).",
    "<b>But division is not automatic</b>: <b>a has a "
    "multiplicative inverse modulo n exactly when "
    "gcd(a, n) = 1</b> — and <b>extended Euclid computes it</b> "
    "(&sect;1), which is the practical payoff of the whole "
    "section."]),

  ("break",),
  ("h1", "3 &nbsp; The theorems"),
  ("eq", "Fermat: if p is prime and p does not divide a, then "
         "a<super>p&minus;1</super> &equiv; 1 (mod p)"),
  ("eq", "Euler: a<super>&phi;(n)</super> &equiv; 1 (mod n) whenever "
         "gcd(a, n) = 1"),
  ("ul", ["<b>Fermat's little theorem gives you inverses instantly "
          "modulo a prime</b> (since "
          "a &middot; a<super>p&minus;2</super> &equiv; 1) and "
          "<b>underlies the standard probabilistic primality "
          "tests</b> — which is CSCE 658's territory.",
          "<b>Euler's theorem is the generalisation to composite "
          "n</b>, where &phi;(n) counts the integers below n that are "
          "coprime to it — <b>and RSA is this theorem</b>: "
          "encryption raises to e, decryption raises to d, and "
          "ed &equiv; 1 mod &phi;(n) makes the round trip the "
          "identity.",
          "<b>The Chinese remainder theorem says congruences modulo "
          "coprime moduli have a unique joint solution</b> — "
          "<b>which lets you work modulo the factors separately and "
          "recombine</b>, and is used both for speed (RSA decryption is "
          "several times faster this way) and in secret sharing "
          "schemes.",
          "<b>RSA is Euler's theorem</b> — <b>which is why "
          "CSCE 711 can treat it in a single module rather than "
          "five</b>, and is a good illustration of how much a "
          "prerequisite buys. <b>These three theorems are the whole "
          "number-theoretic toolkit this program needs.</b>"]),

  ("h1", "4 &nbsp; Where it is used"),
  ("ul", ["<b>Hashing</b> — <b>every hash table's index is a "
          "mod operation</b>, and <b>the choice of modulus determines "
          "the collision behaviour</b> (a power of two throws away the "
          "high bits; a prime does not) — CSCE 629 and "
          "CSCE 658.",
          "<b>Public-key cryptography</b> — <b>RSA is Euler's "
          "theorem and Diffie-Hellman is modular exponentiation in a "
          "group</b> (CSCE 711) — and <b>Shor's algorithm attacks "
          "exactly the order-finding problem of this module</b> "
          "(CSCE 640 Module 08 &sect;1).",
          "<b>Checksums and error detection</b> — CRC is "
          "polynomial arithmetic modulo a fixed polynomial, which is "
          "structurally the same construction over a different "
          "ring.",
          "<b>Random number generation</b> — <b>linear "
          "congruential generators are one mod away from being "
          "useful</b>, and <b>understanding exactly why they are weak "
          "requires this module</b> (the low bits have short "
          "periods).",
          "<b>And graphics, less obviously</b> — <b>wrapping "
          "texture coordinates, tiling patterns, and hash-based "
          "procedural noise are all modular arithmetic</b>. <b>Hash-based "
          "procedural noise is the one place this module touches the "
          "graphics track directly, and it touches it constantly.</b>"]),
  ("callout", "And the thing to carry forward",
   ["<b>Modular arithmetic is the first place Module 04's "
    "well-definedness obligation becomes real</b> — <b>computing "
    "with a representative and then claiming an answer about the whole "
    "class is exactly the move that needs justifying</b>, and here it "
    "is justified rather than assumed.",
    "<b>And the Euclidean algorithm is the first non-trivial "
    "algorithm in the program</b> — <b>with a correctness argument "
    "and a complexity bound</b>, <b>which is precisely what CSCE 629 "
    "is about</b> and is a preview of its method.",
    "<b>So prove Euclid correct and bound its running time by "
    "hand</b> — <b>which is a complete exercise in everything "
    "Modules 01 through 03 taught</b>: a precise statement, an "
    "invariant, an induction, and an asymptotic claim.",
    "<b>Which is why this module sits here rather than "
    "later</b>: <b>it is the point at which the proof technique first "
    "visibly pays for itself</b>, on an object you already "
    "understood."]),
 ],
 "resources": [
   ("Lehman, Leighton & Meyer, chapters 8 and 9 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>The whole module</b>, free — and it develops RSA from this "
    "material, which is the right motivation."),
   ("MIT 6.042J, the number theory lectures (free video)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/video_galleries/video-lectures/",
    "<b>&sect;&sect;1 to 3</b>, with Euclid proved rather than "
    "asserted."),
   ("Silverman &mdash; A Friendly Introduction to Number Theory",
    "https://www.math.brown.edu/johsilve/frint.html",
    "<b>&sect;&sect;1 to 3</b> — patient, and the early chapters are "
    "available free from the author."),
   ("Project Euler, the early problems (free)",
    "https://projecteuler.net/",
    "<b>&sect;&sect;1 and 4</b> — problems where implementing Euclid "
    "and modular exponentiation is the natural solution."),
 ],
 "exercises": [
   "<b>State the division algorithm</b> and prove q and r are "
   "unique.",
   "<b>Run Euclid by hand</b> on three pairs, showing every step.",
   "<b>Prove Euclid correct</b> using the common-divisor "
   "argument.",
   "<b>Bound its running time</b> and justify the log.",
   "<b>Implement extended Euclid</b> and verify Bezout's identity.",
   "<b>Prove that addition is well-defined</b> on residue "
   "classes.",
   "<b>Compute five modular inverses</b>, and find one that does not "
   "exist.",
   "<b>Implement modular exponentiation</b> by repeated squaring.",
   "<b>Verify Fermat's little theorem</b> on several primes, then on "
   "a composite.",
   "<b>Work a small RSA example</b> end to end by hand.",
 ],
 "selfcheck": [
   "State the division algorithm and say what the uniqueness buys.",
   "Why does Euclid's algorithm work?",
   "What is its running time, and why?",
   "What does extended Euclid give you beyond the gcd?",
   "Show congruence is an equivalence relation.",
   "What has to be proved before computing with representatives?",
   "When does a have an inverse mod n?",
   "State Fermat, Euler, and the Chinese remainder theorem.",
   "Which theorem is RSA?",
   "Name five places this arithmetic is used in the program.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Counting",
 "subtitle": "Reasoning that looks like arithmetic.",
 "question": "How many ways, and how do you know you counted each "
             "once?",
 "outcomes": [
     "Use the sum, product, and bijection rules.",
     "Count permutations and combinations correctly.",
     "Correct for overcounting, including inclusion-exclusion.",
     "Prove identities by double counting.",
     "Use the pigeonhole principle.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The basic rules",
   "blurb": "Four of them, and they compose."},

  {"t": "code", "kicker": "Rules", "title": "The four rules everything else is built from",
   "lang": "text", "code": """
  SUM RULE
      disjoint choices add.
      |A union B| = |A| + |B|  when A and B are
      disjoint.   "or"

  PRODUCT RULE
      independent choices multiply.
      |A x B| = |A| * |B|.   "and then"

  BIJECTION RULE
      if you can biject A with B, then |A| = |B|.
      The most powerful of the four: count something
      ELSE that is easier, and exhibit the bijection.

  DIVISION RULE
      if every element of B is hit exactly k times by
      a map from A, then |A| = k |B|.
      This is the overcounting correction (section 2)

  AND THE DISCIPLINE: say which rule you are using at
  each step. A counting argument that does not name
  its rules is the kind that double-counts silently.
""",
   "caption": "<b>Name the rule at each step</b> — a counting "
              "argument that does not is the kind that double-counts "
              "silently.",
   "note": "The bijection rule is the one worth reaching for: count "
           "something easier."},

  {"t": "section", "label": "Part 2", "title": "Permutations and combinations",
   "blurb": "And the one distinction that causes all the trouble."},

  {"t": "table", "kicker": "Formulas", "title": "The four cases, which is the whole table",
   "header": ["", "Order matters", "Order does not"],
   "widths": [3.0, 4.0, 4.0],
   "rows": [
     ["<b>Without repetition</b>", "<b>n!/(n−k)! — permutations</b>", "<b>C(n,k) — combinations</b>"],
     ["<b>With repetition</b>", "<b>nᵏ</b>", "<b>C(n+k−1, k) — stars and bars</b>"],
   ],
   "footnote": "<b>Ask 'does order matter' and 'can things repeat' "
               "before reaching for a formula</b> — two questions, "
               "four cases, and almost every counting error is answering "
               "one of them wrong.",
   "note": "Two questions select the cell. That is the whole "
           "method."},

  {"t": "callout", "title": "And C(n,k) is the division rule: count the ordered ones, then divide by the overcount",
   "kind": "Why the formula is not something to memorise",
   "body": ["<b>There are n!/(n−k)! ordered selections</b>, and "
            "<b>each unordered set of k is counted exactly k! "
            "times</b> — once per ordering.",
            "<b>So divide by k!</b> — <b>which is the division rule "
            "of Part 1</b>, and gives "
            "C(n,k) = n!/(k!(n−k)!).",
            "<b>Which means you never need the formula</b>: <b>count "
            "with order, work out the overcount factor, and "
            "divide</b> — and that method handles cases the formula "
            "does not cover.",
            "<b>And it generalises directly</b>: <b>arrangements of "
            "a word with repeated letters divide by the factorial of "
            "each letter's multiplicity</b>, which is the same argument "
            "applied twice."]},

  {"t": "section", "label": "Part 3", "title": "Double counting",
   "blurb": "The technique that proves identities without algebra."},

  {"t": "callout", "title": "Count one set two ways, and the two answers are equal — which is a proof",
   "kind": "The technique worth being fluent in",
   "body": ["<b>'Sum over k of C(n,k) equals 2 to the n' is "
            "immediate</b>: both sides count the subsets of an "
            "n-element set, one by size and one by "
            "membership-choice.",
            "<b>And Pascal's identity C(n,k) = C(n−1,k−1) + "
            "C(n−1,k) is the same move</b>: split the subsets by "
            "whether they contain the last element.",
            "<b>Which is a proof, and a better one than the "
            "algebra</b> — <b>it explains why the identity holds</b> "
            "rather than verifying that it does.",
            "<b>And it is the technique Project 2 asks for</b>: "
            "<b>one counting problem solved two ways, with the two "
            "answers shown equal</b> — which is the clearest "
            "demonstration that counting is reasoning."]},

  {"t": "section", "label": "Part 4", "title": "Pigeonhole",
   "blurb": "Trivial to state, surprisingly hard to apply."},

  {"t": "bullets", "kicker": "Pigeonhole", "title": "The principle, and why it is not trivial",
   "items": [
     "<b>n + 1 objects in n boxes means some box has two</b> "
     "— <b>which is obvious, and the difficulty is always "
     "choosing the boxes.</b>",
     "",
     "<b>Generalised: n objects in k boxes means some box has at "
     "least ⌈n/k⌉</b>, which is the form actually "
     "used.",
     "",
     "<b>'Two people in London have the same number of hairs' "
     "— boxes are hair counts, objects are people</b>, and the "
     "whole argument is noticing that there are more people than "
     "possible counts.",
     "",
     "<b>And it gives non-constructive existence proofs</b>: "
     "<b>you learn something exists without finding it</b>, which is "
     "Module 02 §4's second flavour.",
     "",
     "<b>It is also how hash collisions are "
     "proved inevitable</b>, which is where CSCE 629 and CSCE 711 "
     "both use it.",
   ],
   "footnote": "<b>The difficulty is always choosing the "
               "boxes</b> — the principle itself is one line, and "
               "the entire content of any pigeonhole argument is what "
               "you decided to count."},

  {"t": "callout", "title": "And inclusion-exclusion, which is the sum rule repaired",
   "kind": "Closing",
   "body": ["<b>The sum rule needs disjointness</b>, and <b>when "
            "the sets overlap you subtract the pairwise intersections, "
            "add back the triples, and so on.</b>",
            "<b>Which is exactly the correction for having counted "
            "the overlaps twice</b> — and the alternating signs are "
            "that correction iterated.",
            "<b>And it is used constantly in probability</b> "
            "(Module 11 §2), where it is the same formula with "
            "measures instead of counts.",
            "<b>So the module's one-sentence summary:</b> <b>count "
            "carefully, name the rule, and check the overcount</b> — "
            "which is three habits rather than a set of "
            "formulas."]},
 ],
 "takeaways": [
   "Name the rule at each step; a counting argument that does not is the "
   "kind that double-counts silently.",
   "The bijection rule is the one to reach for — count something "
   "easier and exhibit the bijection.",
   "Ask 'does order matter' and 'can things repeat' before reaching for a "
   "formula.",
   "C(n,k) is the division rule applied to the ordered count, so you never "
   "need to memorise it.",
   "Counting one set two ways is a proof, and a better one than the algebra "
   "because it explains why.",
   "In a pigeonhole argument the entire content is what you decided to use "
   "as boxes.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The basic rules"),
  ("code", """SUM RULE
    disjoint choices add.
    |A union B| = |A| + |B|  when A and B are
    disjoint.   "or"

PRODUCT RULE
    independent choices multiply.
    |A x B| = |A| * |B|.   "and then"

BIJECTION RULE
    if you can biject A with B, then |A| = |B|.
    The most powerful of the four: count something
    ELSE that is easier, and exhibit the bijection.

DIVISION RULE
    if every element of B is hit exactly k times by a
    map from A, then |A| = k |B|.
    This is the overcounting correction (section 2).

AND THE DISCIPLINE: say which rule you are using at
each step. A counting argument that does not name its
rules is the kind that double-counts silently."""),
  ("p", "<b>Name the rule at each step</b> — <b>a counting "
        "argument that does not name its rules is the kind that "
        "double-counts silently</b>, and counting errors are unusually "
        "hard to spot because the answer is a plausible number either "
        "way. <b>The bijection rule is the one worth reaching for</b>: "
        "most elegant counting arguments are a bijection to something "
        "already counted, and &sect;3's double counting is the same "
        "instinct from the other side."),

  ("h1", "2 &nbsp; Permutations and combinations"),
  ("table", ["", "Order matters", "Order does not matter"],
   [["<b>Without repetition</b>",
     "<b>n! / (n &minus; k)!</b> — permutations",
     "<b>C(n, k) = n! / (k!(n&minus;k)!)</b> — combinations"],
    ["<b>With repetition</b>", "<b>n<sup>k</sup></b>",
     "<b>C(n + k &minus; 1, k)</b> — stars and bars"]],
   [0.26, 0.37, 0.37]),
  ("p", "<b>Ask 'does order matter' and 'can things repeat' before "
        "reaching for a formula</b> — <b>two questions, four cases, "
        "and almost every counting error is answering one of them "
        "wrong</b> rather than misremembering an expression. <b>Two "
        "questions select the cell; that is the whole method</b>, and it "
        "is worth writing both answers down explicitly on every problem "
        "until it becomes automatic."),
  ("callout", "And C(n,k) is the division rule: count the ordered ones, then "
              "divide by the overcount",
   ["<b>There are n! / (n &minus; k)! ordered selections of k items "
    "from n</b>, and <b>each unordered set of k is counted exactly k! "
    "times</b> — once for each ordering of its elements.",
    "<b>So divide by k!</b> — <b>which is precisely the "
    "division rule of &sect;1</b> — <b>and gives "
    "C(n,k) = n!/(k!(n&minus;k)!)</b> without any need to remember the "
    "expression.",
    "<b>Which means you never actually need the formula</b>: "
    "<b>count with order, work out the overcount factor, and "
    "divide</b> — and <b>that method handles cases the standard "
    "formula does not cover</b>, which is where it earns its "
    "keep.",
    "<b>And it generalises directly</b>: <b>the number of "
    "arrangements of a word with repeated letters is the factorial of "
    "its length divided by the factorial of each letter's "
    "multiplicity</b> — the same argument, applied once per "
    "repeated letter."]),

  ("break",),
  ("h1", "3 &nbsp; Double counting"),
  ("callout", "Count one set two ways, and the two answers are equal — "
              "which is a proof",
   ["<b>'The sum over k of C(n,k) equals 2<sup>n</sup>' is "
    "immediate</b> once you see it: <b>both sides count the subsets of "
    "an n-element set</b>, the left by grouping them according to size "
    "and the right by choosing in-or-out for each element.",
    "<b>And Pascal's identity, C(n,k) = C(n&minus;1,k&minus;1) + "
    "C(n&minus;1,k), is the same move</b>: split the k-subsets "
    "according to whether they contain the last element, and count each "
    "group.",
    "<b>Which is a proof, and a better one than the algebraic "
    "verification</b> — <b>it explains <i>why</i> the identity "
    "holds</b> rather than confirming that the two expressions happen to "
    "be equal, and it is usually shorter.",
    "<b>And it is the technique Project 2 asks for</b>: <b>one "
    "counting problem solved two ways, with the two answers shown equal "
    "algebraically</b> — <b>which is the clearest available "
    "demonstration that counting is reasoning rather than "
    "arithmetic.</b>"]),

  ("h1", "4 &nbsp; Pigeonhole"),
  ("ul", ["<b>n + 1 objects in n boxes means some box contains at "
          "least two</b> — <b>which is obvious, and the difficulty "
          "is always choosing the boxes</b>, never the principle.",
          "<b>Generalised: n objects in k boxes means some box "
          "contains at least &lceil;n/k&rceil;</b>, <b>which is the "
          "form actually used</b> in practice.",
          "<b>'Two people in London have exactly the same number of "
          "hairs on their heads' — the boxes are possible hair "
          "counts and the objects are people</b>, and <b>the entire "
          "argument is noticing that there are more people than possible "
          "counts</b>. Nothing else happens.",
          "<b>And it gives non-constructive existence "
          "proofs</b>: <b>you learn that something exists without any "
          "way to find it</b> — <b>which is Module 02 "
          "&sect;4's second flavour of existence proof</b>, and is "
          "philosophically interesting and practically "
          "frustrating.",
          "<b>It is also how hash collisions are proved "
          "inevitable</b> (more possible inputs than outputs), <b>which "
          "is where CSCE 629 and CSCE 711 both use it</b>. <b>The "
          "difficulty is always choosing the boxes</b>: the principle is "
          "one line, and the entire content of any pigeonhole argument is "
          "what you decided to count."]),
  ("callout", "And inclusion-exclusion, which is the sum rule repaired",
   ["<b>The sum rule requires disjointness</b> (&sect;1), and "
    "<b>when the sets overlap you subtract the pairwise intersections, "
    "add back the triple intersections, and so on with alternating "
    "signs.</b>",
    "<b>Which is exactly the correction for having counted the "
    "overlaps more than once</b> — subtract the double-counts, "
    "notice you have now removed the triples too many times, add them "
    "back — <b>and the alternating signs are that correction "
    "iterated to the end.</b>",
    "<b>And it is used constantly in probability</b> "
    "(Module 11 &sect;2), <b>where it is the identical formula with "
    "measures in place of counts</b>, which is a good example of the "
    "same combinatorial fact wearing two hats.",
    "<b>So this module's one-sentence summary:</b> <b>count "
    "carefully, name the rule, and check the overcount</b> — "
    "<b>which is three habits rather than a set of formulas to "
    "memorise</b>, and the habits survive problems the formulas do "
    "not cover."]),
 ],
 "resources": [
   ("Lehman, Leighton & Meyer, chapter 15 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>The whole module</b>, free — and the four rules are stated "
    "exactly as &sect;1 gives them."),
   ("MIT 6.042J, the counting lectures (free video)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/video_galleries/video-lectures/",
    "<b>&sect;&sect;1 to 3</b>, with the bijection rule used "
    "repeatedly."),
   ("Graham, Knuth & Patashnik &mdash; Concrete Mathematics",
    "https://www.pearson.com/en-us/subject-catalog/p/concrete-mathematics-a-foundation-for-computer-science/P200000000359",
    "<b>&sect;&sect;2 and 3 far beyond this course</b> — demanding, "
    "excellent, and the binomial coefficient chapter is the reference. "
    "Library copy."),
   ("Hammack &mdash; Book of Proof, chapter 3 (free)",
    "https://www.people.vcu.edu/~rhammack/BookOfProof/",
    "<b>&sect;&sect;1 and 2</b>, free, with many worked "
    "examples."),
 ],
 "exercises": [
   "<b>State the four rules</b> and give a problem using each.",
   "<b>Solve one problem by bijection</b> to something easier.",
   "<b>For ten problems, answer the two questions</b> before "
   "computing.",
   "<b>Derive C(n,k)</b> from the division rule.",
   "<b>Count the arrangements of a word with repeats</b>, from first "
   "principles.",
   "<b>Prove the subset-sum identity</b> by double counting.",
   "<b>Prove Pascal's identity</b> by double counting.",
   "<b>Solve one problem two ways</b> and show the answers agree "
   "algebraically.",
   "<b>Use pigeonhole</b> on three problems, naming the boxes "
   "each time.",
   "<b>Apply inclusion-exclusion</b> to a three-set problem.",
 ],
 "selfcheck": [
   "State the four counting rules and what each is for.",
   "Which is most powerful, and why?",
   "What two questions select the formula?",
   "Derive C(n,k) from the division rule.",
   "How does that generalise to repeated letters?",
   "What is double counting, and why is it a proof?",
   "Prove one identity by it.",
   "State pigeonhole, generalised, and say where the difficulty is.",
   "What kind of existence proof does it give?",
   "State inclusion-exclusion and what it repairs.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Graphs",
 "subtitle": "The data structure that is also a proof technique.",
 "question": "What problems become easy once you draw them as a "
             "graph?",
 "outcomes": [
     "Define graphs and their standard vocabulary.",
     "Prove the handshake lemma and use it.",
     "Explain connectivity, paths, and cycles.",
     "Model problems as graphs.",
     "Recognise bipartite and planar structure.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The vocabulary",
   "blurb": "Which every later course assumes."},

  {"t": "bullets", "kicker": "Vocabulary", "title": "What you need, stated once",
   "items": [
     "<b>A graph is a set of vertices and a set of edges</b>, "
     "each edge a pair of vertices — <b>directed if the pairs are "
     "ordered</b>, <b>weighted if edges carry numbers</b>.",
     "",
     "<b>Degree is the number of edges at a vertex</b>; in a "
     "directed graph, in-degree and out-degree "
     "separately.",
     "",
     "<b>A path is a walk with no repeated vertex</b>; a cycle "
     "is a path that returns to its start — and <b>the distinction "
     "between walk, trail, and path is where sloppy statements go "
     "wrong</b>.",
     "",
     "<b>Connected means a path exists between every pair</b>; "
     "<b>a component is a maximal connected piece</b>.",
     "",
     "<b>And simple means no loops and no repeated "
     "edges</b> — which most theorems assume and few state.",
   ],
   "footnote": "<b>Most graph theorems assume 'simple' and few of "
               "them say so</b> — which is worth checking before "
               "applying one to a multigraph."},

  {"t": "section", "label": "Part 2", "title": "The handshake lemma",
   "blurb": "The first real theorem, and it is a double count."},

  {"t": "eq", "kicker": "Handshake", "title": "Sum of degrees is twice the edges",
   "eqs": [
     ("Σ over vertices of deg(v) = 2|E|",
      "Because each edge contributes one to the degree at each of "
      "its two endpoints — which is Module 06 §3's double "
      "counting, in its first graph application."),
     ("corollary: the number of odd-degree vertices is even",
      "Since the total is even, the odd contributions must pair up. "
      "A one-line consequence with surprising reach."),
     ("and so: no graph has exactly one odd-degree vertex",
      "Which rules out a whole class of proposed constructions "
      "instantly, and is the usual way the lemma gets used."),
   ],
   "caption": "<b>The handshake lemma is a double count</b> — "
              "count edge-endpoint incidences by edge, and by vertex, "
              "and equate.",
   "note": "This is the clearest example of Module 06's technique "
           "producing a real theorem."},

  {"t": "section", "label": "Part 3", "title": "Modelling",
   "blurb": "Which is the skill, rather than the theorems."},

  {"t": "table", "kicker": "Modelling", "title": "Problems that become graph problems",
   "header": ["Problem", "Vertices", "Edges"],
   "widths": [3.4, 3.4, 4.2],
   "rows": [
     ["<b>Scheduling with conflicts</b>", "<b>Tasks</b>", "<b>Conflict — then colour the graph</b>"],
     ["<b>Dependency resolution</b>", "<b>Packages</b>", "<b>Depends-on — then topologically sort</b>"],
     ["<b>Routing</b>", "<b>Locations</b>", "<b>Links with weights — shortest path</b>"],
     ["<b>Matching</b>", "<b>Two groups</b>", "<b>Compatibility — bipartite matching</b>"],
     ["<b>State search</b>", "<b>Configurations</b>", "<b>Legal moves — then it is reachability</b>"],
   ],
   "footnote": "<b>The state-search row is the one that transfers "
               "furthest</b> — any puzzle with states and moves is a "
               "graph, and 'is it solvable' is "
               "reachability.",
   "note": "Modelling is the skill; the theorems are looked up."},

  {"t": "callout", "title": "And the modelling decision is which objects are vertices, which is not always obvious",
   "kind": "Where the thinking actually happens",
   "body": ["<b>The same situation can be modelled several ways</b>, "
            "and <b>the right choice makes a hard problem "
            "standard</b> — which is the whole art.",
            "<b>Edge colouring is vertex colouring of the line "
            "graph</b>; <b>a puzzle's states are vertices and its moves "
            "are edges</b> — two reframings that convert an unfamiliar "
            "problem into a looked-up one.",
            "<b>So the question to ask is: what are the objects, and "
            "what is the relation?</b> — <b>and then check whether "
            "the resulting graph has a name</b>.",
            "<b>Which is why this module is placed before "
            "CSCE 629</b>: <b>that course assumes you can already turn "
            "a problem into a graph</b>, and spends its time on "
            "algorithms instead."]},

  {"t": "section", "label": "Part 4", "title": "Two special structures",
   "blurb": "Bipartite and planar, both of which have tests."},

  {"t": "callout", "title": "Bipartite means two-colourable means no odd cycle — three equivalent statements",
   "kind": "Closing",
   "body": ["<b>A graph is bipartite if its vertices split into two "
            "sets with every edge crossing between "
            "them</b> — <b>equivalently, it is 2-colourable; "
            "equivalently, it has no odd-length cycle.</b>",
            "<b>And the equivalence gives you a test</b>: "
            "<b>two-colour it greedily by breadth-first search, and a "
            "conflict exhibits an odd cycle</b> — linear time, and the "
            "failure is informative.",
            "<b>Which matters because matching problems need "
            "bipartiteness</b> (CSCE 717 §09), and <b>a great many "
            "scheduling problems are bipartite without looking "
            "it.</b>",
            "<b>Planar graphs are the other special "
            "case</b> — <b>drawable without crossings, satisfying "
            "Euler's formula V − E + F = 2</b> — which bounds their "
            "edge count and is why planar problems are "
            "easier."]},
 ],
 "takeaways": [
   "Most graph theorems assume 'simple' and few of them say so.",
   "The handshake lemma is a double count: sum of degrees is twice the "
   "edges.",
   "The number of odd-degree vertices is always even, which rules out "
   "proposed constructions instantly.",
   "Modelling is the skill; the theorems are looked up.",
   "Any puzzle with states and moves is a graph, and 'is it solvable' is "
   "reachability.",
   "Bipartite, 2-colourable, and no-odd-cycle are three names for the same "
   "property, and the test is linear time.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The vocabulary"),
  ("ul", ["<b>A graph is a set of vertices together with a set of "
          "edges</b>, each edge being a pair of vertices — "
          "<b>directed if the pairs are ordered</b>, <b>weighted if the "
          "edges carry numbers</b>, and those two choices are "
          "independent.",
          "<b>The degree of a vertex is the number of edges meeting "
          "it</b>; in a directed graph, <b>in-degree and out-degree are "
          "counted separately</b> and their sum is the total "
          "degree.",
          "<b>A walk is any sequence of adjacent vertices; a trail "
          "repeats no edge; a path repeats no vertex</b>; <b>a cycle is "
          "a path that returns to its start</b> — and <b>the "
          "distinction between these is where sloppy statements go "
          "wrong</b>, since 'path' is used loosely in conversation and "
          "precisely in theorems.",
          "<b>Connected means a path exists between every pair of "
          "vertices</b>; <b>a component is a maximal connected "
          "piece</b>, and a disconnected graph is a disjoint union of "
          "its components.",
          "<b>And simple means no self-loops and no repeated "
          "edges</b> — <b>which most theorems assume and few of "
          "them state</b>, so it is worth checking before applying one "
          "to a multigraph or a graph with loops."]),

  ("h1", "2 &nbsp; The handshake lemma"),
  ("eq", "&Sigma;<sub>v</sub> deg(v) = 2|E|"),
  ("ul", ["<b>Because each edge contributes exactly one to the degree "
          "at each of its two endpoints</b> — so counting "
          "edge-endpoint incidences by vertex gives the left side and "
          "counting them by edge gives the right — <b>which is "
          "Module 06 &sect;3's double counting in its first graph "
          "application.</b>",
          "<b>Corollary: the number of odd-degree vertices is "
          "even.</b> <b>Since the total is even, the vertices "
          "contributing an odd amount must pair up</b> — a one-line "
          "consequence with a surprising amount of reach.",
          "<b>And therefore no graph has exactly one odd-degree "
          "vertex</b>, <b>which rules out a whole class of proposed "
          "constructions instantly</b> and <b>is the usual way the lemma "
          "gets used</b>: somebody describes a graph with specified "
          "degrees, and you check the parity before thinking about "
          "anything else.",
          "<b>The handshake lemma is a double count</b> — "
          "<b>count edge-endpoint incidences by edge, and by vertex, and "
          "equate</b> — and <b>it is the clearest example in this "
          "course of Module 06's technique producing a genuine "
          "theorem</b> rather than an identity."]),

  ("break",),
  ("h1", "3 &nbsp; Modelling"),
  ("table", ["Problem", "Vertices", "Edges, and what to do next"],
   [["<b>Scheduling with conflicts</b>", "<b>Tasks or exams.</b>",
     "<b>An edge for each conflict</b> — then the problem is graph "
     "colouring."],
    ["<b>Dependency resolution</b>", "<b>Packages or build targets.</b>",
     "<b>A directed edge for depends-on</b> — then topologically "
     "sort, and a cycle is a circular dependency."],
    ["<b>Routing and navigation</b>", "<b>Locations or routers.</b>",
     "<b>Weighted edges for links</b> — then it is a shortest-path "
     "problem (CSCE 629)."],
    ["<b>Assignment and matching</b>",
     "<b>Two groups: people and jobs, students and schools.</b>",
     "<b>An edge for each compatible pair</b> — then bipartite "
     "matching (CSCE 717 Module 09)."],
    ["<b>Puzzle or state search</b>",
     "<b>Every reachable configuration.</b>",
     "<b>An edge for each legal move</b> — then 'is it solvable' "
     "is simply reachability. See the note."]],
   [0.26, 0.28, 0.46]),
  ("p", "<b>The state-search row is the one that transfers "
        "furthest</b> — <b>any puzzle with states and legal moves is "
        "a graph, and 'is it solvable' becomes reachability</b>, which "
        "is a solved problem. <b>Modelling is the skill; the theorems "
        "are looked up</b> — which is why &sect;3 is longer than "
        "&sect;2 in a module about graph theory."),
  ("callout", "And the modelling decision is which objects are vertices, "
              "which is not always obvious",
   ["<b>The same situation can be modelled in several ways</b>, and "
    "<b>the right choice turns a hard problem into a standard "
    "one</b> — <b>which is the whole art of this section</b>, and "
    "the part that cannot be looked up.",
    "<b>Edge colouring a graph is vertex colouring of its line "
    "graph</b> (vertices become edges and vice versa); <b>a puzzle's "
    "states are vertices and its moves are edges</b> — <b>two "
    "reframings that convert an unfamiliar problem into one with a name "
    "and an algorithm.</b>",
    "<b>So the question to ask is always: what are the objects, and "
    "what is the relation between them?</b> — <b>and then check "
    "whether the resulting graph has a name</b> (bipartite, planar, "
    "acyclic, complete), because the name comes with theorems.",
    "<b>Which is why this module is placed before CSCE 629</b>: "
    "<b>that course assumes you can already turn a problem into a "
    "graph</b> and spends its time on the algorithms instead, so the "
    "modelling step is never taught there."]),

  ("h1", "4 &nbsp; Two special structures"),
  ("callout", "Bipartite means two-colourable means no odd cycle — "
              "three equivalent statements",
   ["<b>A graph is bipartite if its vertices split into two sets with "
    "every edge crossing between them</b> — <b>equivalently, it is "
    "2-colourable; equivalently, it contains no cycle of odd "
    "length</b> — and proving those three equivalent is a good "
    "exercise in this module's technique.",
    "<b>And the equivalence hands you a test</b>: <b>two-colour the "
    "graph greedily by breadth-first search, and any conflict you hit "
    "exhibits an odd cycle</b> — <b>linear time, and the failure "
    "case is informative</b> rather than merely negative, which is the "
    "mark of a good algorithm.",
    "<b>Which matters because matching problems require "
    "bipartiteness</b> (CSCE 717 Module 09's stable matching, and "
    "the maximum-matching algorithms of CSCE 629), and <b>a great many "
    "scheduling and assignment problems are bipartite without looking "
    "it.</b>",
    "<b>Planar graphs are the other special case worth "
    "knowing</b> — <b>drawable in the plane without crossing "
    "edges, and satisfying Euler's formula V &minus; E + F = 2</b> "
    "— <b>which bounds their edge count at roughly 3V and is why "
    "many problems are easier on planar inputs</b>, including some that "
    "are NP-hard in general."]),
 ],
 "resources": [
   ("Lehman, Leighton & Meyer, chapters 11 to 13 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>The whole module</b>, free — graphs, colouring, and matching "
    "developed together."),
   ("MIT 6.042J, the graph theory lectures (free video)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/video_galleries/video-lectures/",
    "<b>&sect;&sect;1 to 4</b>, with the modelling emphasised."),
   ("West &mdash; Introduction to Graph Theory",
    "https://www.pearson.com/en-us/subject-catalog/p/introduction-to-graph-theory/P200000006322",
    "<b>&sect;&sect;2 and 4 in depth</b> — the standard reference "
    "when you need a theorem. Library copy."),
   ("CLRS, the graph algorithm chapters (library copy)",
    "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/",
    "<b>&sect;3's 'what to do next' column</b> — which is "
    "CSCE 629's content, previewed."),
 ],
 "exercises": [
   "<b>Define walk, trail, path, and cycle</b>, with an example "
   "distinguishing each.",
   "<b>Find a theorem that assumes simple</b> without saying so.",
   "<b>Prove the handshake lemma</b> by double counting.",
   "<b>Prove the odd-degree corollary</b> and use it to rule out a "
   "construction.",
   "<b>Model five problems as graphs</b>, naming vertices and "
   "edges.",
   "<b>Model one puzzle as a state graph</b> and compute its size.",
   "<b>Find two different graph models</b> of the same problem, and "
   "say which is better.",
   "<b>Prove bipartite and no-odd-cycle equivalent.</b>",
   "<b>Implement the two-colouring test</b> and have it output the "
   "odd cycle on failure.",
   "<b>Verify Euler's formula</b> on three planar drawings.",
 ],
 "selfcheck": [
   "Define graph, degree, path, cycle, connected, component, and "
   "simple.",
   "Which assumption do most theorems make silently?",
   "State the handshake lemma and prove it.",
   "What is its corollary, and how is it used?",
   "Give five problems that become graph problems, with their "
   "vertices.",
   "Which modelling pattern transfers furthest?",
   "What is the modelling question to ask?",
   "Why is this module placed before CSCE 629?",
   "Give three equivalent characterisations of bipartite.",
   "State Euler's formula and what it bounds.",
 ],
},

]
