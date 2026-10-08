# -*- coding: utf-8 -*-
"""CSCE 717 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Games and Equilibria",
 "subtitle": "The solution concepts, and what Nash's theorem does not "
             "promise.",
 "question": "What does it mean to predict what agents will do?",
 "outcomes": [
     "Define a game in normal form.",
     "Define dominance, Nash, and the relations between them.",
     "State Nash's theorem precisely and its three caveats.",
     "Explain mixed strategies and what they model.",
     "Analyse small games correctly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The objects",
   "blurb": "A game is three things."},

  {"t": "callout", "title": "Players, strategies, payoffs — and every modelling decision is in the payoffs",
   "kind": "The definition, and where the content hides",
   "body": ["<b>A normal-form game is a set of players, a strategy "
            "set per player, and a payoff function from strategy "
            "profiles to a number per player</b> — three "
            "objects.",
            "<b>And the payoffs encode everything you believe about "
            "what the agents want</b> — <b>which is the modelling "
            "step, and is where most disagreements about a game-theoretic "
            "analysis actually live.</b>",
            "<b>So 'the prisoner's dilemma shows cooperation is "
            "irrational' is a claim about a payoff matrix</b>, not "
            "about people — <b>and the matrix was "
            "chosen.</b>",
            "<b>Which is this course's first "
            "caution:</b> <b>argue about the payoffs before arguing "
            "about the equilibrium</b>, because the equilibrium follows "
            "mechanically and the payoffs do not."]},

  {"t": "section", "label": "Part 2", "title": "Solution concepts",
   "blurb": "In decreasing order of how much they assume."},

  {"t": "table", "kicker": "Concepts", "title": "What each concept predicts, and what it requires",
   "header": ["Concept", "Definition", "What it assumes"],
   "widths": [3.0, 4.2, 3.8],
   "rows": [
     ["<b>Dominant strategy</b>", "<b>Best regardless of others</b>", "<b>Nothing. Rare and ideal</b>"],
     ["<b>Iterated dominance</b>", "<b>Remove dominated, repeat</b>", "<b>Common knowledge of rationality</b>"],
     ["<b>Pure Nash</b>", "<b>No single player gains by deviating</b>", "<b>Correct beliefs. May not exist</b>"],
     ["<b>Mixed Nash</b>", "<b>Same, over randomised strategies</b>", "<b>Correct beliefs. Always exists</b>"],
     ["<b>Correlated equilibrium</b>", "<b>Obey a shared signal</b>", "<b>A coordinating device (M12)</b>"],
   ],
   "footnote": "<b>A dominant strategy equilibrium needs no "
               "assumption about what others do</b> — which is why "
               "mechanism design aims for it "
               "(Module 06 §2).",
   "note": "The assumption column is why dominant strategies are "
           "the design target."},

  {"t": "callout", "title": "And Nash equilibrium assumes agents have correct beliefs about each other, which is a lot",
   "kind": "What the concept actually requires",
   "body": ["<b>A Nash equilibrium is a profile where nobody gains "
            "by deviating alone</b> — <b>which presupposes each agent "
            "correctly anticipates the others' "
            "strategies.</b>",
            "<b>So it is a consistency condition rather than a "
            "prediction of behaviour</b> — <b>it says what is stable, "
            "not how anybody gets there</b>, which is "
            "Module 12's question.",
            "<b>And games may have many equilibria</b>, with <b>no "
            "principle within the concept selecting among "
            "them</b> — which is a serious limitation for anybody "
            "wanting a prediction.",
            "<b>Which is why this course prefers dominant "
            "strategies where it can get them</b> — <b>they require "
            "no belief about anybody</b>, and a mechanism that relies on "
            "correct mutual beliefs is relying on a "
            "lot."]},

  {"t": "section", "label": "Part 3", "title": "Nash's theorem",
   "blurb": "Stated precisely, with the three things it does not say."},

  {"t": "eq", "kicker": "Nash 1950", "title": "The theorem, and its caveats",
   "eqs": [
     ("Every finite game has at least one mixed Nash equilibrium.",
      "Finitely many players, finitely many strategies each. Proved "
      "by a fixed-point argument, which is why Module 03's "
      "complexity result has the shape it does."),
     ("It does not say the equilibrium is unique, or good,",
      "or that agents will find it, or that it can be computed "
      "efficiently. All four are separate questions, and three of "
      "them have discouraging answers."),
     ("and mixed means randomising, which has to be interpreted",
      "As deliberate randomisation, as a population frequency, or "
      "as other players' uncertainty — three readings, and the "
      "right one depends on the application."),
   ],
   "caption": "<b>Existence is not uniqueness, quality, "
              "reachability, or computability</b> — and the last "
              "three are Modules 03, 04, and 12.",
   "note": "The four caveats structure the next three modules."},

  {"t": "section", "label": "Part 4", "title": "Reading a game",
   "blurb": "The analytical habits worth having."},

  {"t": "bullets", "kicker": "Practice", "title": "How to analyse a small game, in order",
   "items": [
     "<b>Look for dominant strategies first</b> — <b>if one "
     "exists the analysis is finished</b>, and no belief assumptions "
     "are needed.",
     "",
     "<b>Then iterated removal of dominated "
     "strategies</b> — which often shrinks the game "
     "dramatically and sometimes solves it.",
     "",
     "<b>Then pure Nash by inspection</b>: <b>check every cell "
     "against both players' deviations</b>, which is mechanical and "
     "catches errors.",
     "",
     "<b>Then mixed, by making the opponent "
     "indifferent</b> — <b>which is the standard trick and is "
     "worth deriving once</b> rather than "
     "memorising.",
     "",
     "<b>And then ask whether the payoffs were right</b> "
     "(Part 1), which is the step that is never taken "
     "and matters most.",
   ],
   "footnote": "<b>In a mixed equilibrium each player randomises so "
               "as to make the <i>other</i> indifferent</b> — which "
               "is counterintuitive and is the key to computing "
               "them."},

  {"t": "callout", "title": "And a solution concept is a modelling choice, which should be named",
   "kind": "Closing",
   "body": ["<b>'The equilibrium of this game is X' means 'under this "
            "solution concept, with these payoffs'</b> — <b>and both "
            "qualifiers do real work.</b>",
            "<b>Which matters because the concepts "
            "disagree</b>: <b>a game can have a unique correlated "
            "equilibrium and several Nash equilibria</b>, and the "
            "predictions differ.",
            "<b>So name the concept</b>, as you would name a "
            "statistical model — which is "
            "CSCE 628 §13's methods discipline in a "
            "theoretical setting.",
            "<b>And prefer the concept with the weakest "
            "assumptions that still answers your "
            "question</b> — <b>which is almost always dominant "
            "strategies when you are the designer</b> "
            "(Module 06)."]},
 ],
 "takeaways": [
   "A game is players, strategies, and payoffs — and every modelling "
   "decision is in the payoffs.",
   "Argue about the payoffs before arguing about the equilibrium, because "
   "the equilibrium follows mechanically.",
   "A dominant strategy equilibrium needs no assumption about what others "
   "do, which is why mechanism design aims for it.",
   "Nash equilibrium is a consistency condition rather than a prediction of "
   "behaviour.",
   "Existence is not uniqueness, quality, reachability, or computability "
   "— and the last three are the next modules.",
   "In a mixed equilibrium each player randomises so as to make the other "
   "indifferent.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The objects"),
  ("callout", "Players, strategies, payoffs — and every modelling "
              "decision is in the payoffs",
   ["<b>A normal-form game is a set of players, a strategy set for "
    "each, and a payoff function mapping strategy profiles to a real "
    "number per player</b> — three objects, and the first two are "
    "usually uncontroversial.",
    "<b>And the payoffs encode everything you believe about what the "
    "agents want</b> — <b>which is the modelling step</b>, and "
    "<b>is where essentially all disagreements about a game-theoretic "
    "analysis actually live</b>, though they are frequently conducted as "
    "disagreements about the solution concept.",
    "<b>So 'the prisoner's dilemma shows cooperation is irrational' "
    "is a claim about a particular payoff matrix</b>, not about "
    "people — <b>and the matrix was chosen by somebody</b>, with "
    "the assumption that the players care about nothing except their own "
    "sentence built into it.",
    "<b>Which is this course's first caution:</b> <b>argue about "
    "the payoffs before arguing about the equilibrium</b>, because <b>the "
    "equilibrium follows mechanically from the payoffs and the payoffs "
    "do not follow from anything</b> — they are an "
    "assumption."]),

  ("h1", "2 &nbsp; Solution concepts"),
  ("table", ["Concept", "Definition", "What it assumes about the agents"],
   [["<b>Dominant strategy equilibrium</b>",
     "<b>Each player's strategy is best regardless of what others "
     "do.</b>",
     "<b>Nothing at all about beliefs.</b> Rare, and ideal — see "
     "the note."],
    ["<b>Iterated dominance</b>",
     "<b>Remove strictly dominated strategies, repeat.</b>",
     "<b>Common knowledge of rationality</b> — everyone is "
     "rational, everyone knows that, and so on."],
    ["<b>Pure Nash equilibrium</b>",
     "<b>No single player gains by deviating alone.</b>",
     "<b>Correct beliefs about the others.</b> <b>May not "
     "exist.</b>"],
    ["<b>Mixed Nash equilibrium</b>",
     "<b>The same, allowing randomised strategies.</b>",
     "<b>Correct beliefs.</b> <b>Always exists</b> in a finite game "
     "(&sect;3)."],
    ["<b>Correlated equilibrium</b>",
     "<b>Obey a recommendation from a shared signal.</b>",
     "<b>A coordinating device, and that obeying is best given the "
     "signal</b> — and it is what no-regret dynamics converge to "
     "(Module 12)."]],
   [0.24, 0.38, 0.38]),
  ("p", "<b>A dominant strategy equilibrium needs no assumption "
        "whatsoever about what the other agents do</b> — <b>which is "
        "exactly why mechanism design aims for it</b> (Module 06 "
        "&sect;2) rather than for Nash. <b>The assumption column is why "
        "dominant strategies are the design target</b>: a mechanism whose "
        "guarantee requires every participant to correctly model every "
        "other participant is guaranteeing very little in practice."),
  ("callout", "And Nash equilibrium assumes agents have correct beliefs about "
              "each other, which is a lot",
   ["<b>A Nash equilibrium is a strategy profile in which no player "
    "gains by deviating alone</b> — <b>which presupposes that each "
    "agent correctly anticipates the strategies the others are "
    "playing</b>, since otherwise 'gains by deviating' is evaluated "
    "against the wrong thing.",
    "<b>So it is a consistency condition rather than a prediction of "
    "behaviour</b> — <b>it says what is stable once reached, not "
    "how anybody would get there</b> — <b>which is Module 12's "
    "question</b> and is a genuinely different one.",
    "<b>And games may have many equilibria</b>, with <b>no "
    "principle within the concept itself that selects among them</b> "
    "— <b>which is a serious limitation for anybody who wanted a "
    "prediction</b>, and has generated a large literature on "
    "refinements that mostly did not settle it.",
    "<b>Which is why this course prefers dominant strategies "
    "wherever it can get them</b> — <b>they require no belief "
    "about anybody</b> — and <b>a mechanism that relies on correct "
    "mutual beliefs is relying on a great deal</b> that the designer "
    "cannot verify."]),

  ("break",),
  ("h1", "3 &nbsp; Nash's theorem"),
  ("eq", "Every finite game has at least one mixed Nash equilibrium."),
  ("ul", ["<b>Finitely many players, finitely many strategies "
          "each</b> — <b>proved by a fixed-point argument</b> "
          "(Brouwer or Kakutani), <b>which is why Module 03's "
          "complexity result has the shape it does</b>: the problem is "
          "complete for a class defined by exactly that kind of "
          "existence proof.",
          "<b>It does not say the equilibrium is unique</b>, "
          "<b>or that it is good for anybody</b> (Module 04's price "
          "of anarchy), <b>or that agents will find it</b> "
          "(Module 12), <b>or that it can be computed "
          "efficiently</b> (Module 03) — <b>four separate "
          "questions, and three of them have discouraging "
          "answers.</b>",
          "<b>And 'mixed' means randomising, which has to be "
          "interpreted</b>: <b>as deliberate randomisation by a player, "
          "as a frequency within a population of players, or as the "
          "other players' uncertainty about what this one will "
          "do</b> — <b>three readings</b>, and <b>the right one "
          "depends entirely on the application</b>, which is worth "
          "settling before quoting a mixed equilibrium at anybody.",
          "<b>Existence is not uniqueness, quality, reachability, or "
          "computability</b> — and <b>the last three are "
          "Modules 03, 04, and 12 respectively</b>. <b>The four "
          "caveats structure the next three modules</b>, which is a "
          "convenient way to remember what each is for."]),

  ("h1", "4 &nbsp; Reading a game"),
  ("ul", ["<b>Look for dominant strategies first</b> — <b>if "
          "one exists, the analysis is finished</b>, the prediction is "
          "robust, and no assumption about beliefs is needed.",
          "<b>Then iterated removal of strictly dominated "
          "strategies</b> — <b>which often shrinks the game "
          "dramatically and sometimes solves it outright</b>, and is "
          "cheap to do.",
          "<b>Then pure Nash by inspection</b>: <b>check every cell "
          "against each player's possible deviations</b> — "
          "mechanical, tedious, and it catches the errors that "
          "cleverness introduces.",
          "<b>Then mixed equilibria, by making the opponent "
          "indifferent</b> — <b>which is the standard technique "
          "and is worth deriving once from the definition</b> rather "
          "than memorising: a player only randomises if the strategies "
          "being mixed give equal expected payoff, so the <i>other</i> "
          "player's mixture must be the one that equalises them.",
          "<b>And then ask whether the payoffs were right</b> "
          "(&sect;1) — <b>which is the step that is never taken and "
          "matters most</b>. <b>In a mixed equilibrium each player "
          "randomises so as to make the <i>other</i> "
          "indifferent</b> — <b>which is counterintuitive and is "
          "the key to computing them.</b>"]),
  ("callout", "And a solution concept is a modelling choice, which should be "
              "named",
   ["<b>'The equilibrium of this game is X' means 'under this "
    "solution concept, with these payoffs'</b> — <b>and both "
    "qualifiers do real work</b>, which is why both belong in the "
    "sentence.",
    "<b>Which matters because the concepts genuinely "
    "disagree</b>: <b>a game can have a unique correlated equilibrium "
    "and several Nash equilibria</b>, or a dominant strategy that "
    "iterated dominance would also find but that a casual Nash analysis "
    "obscures — and the predictions differ.",
    "<b>So name the concept</b>, as you would name a statistical "
    "model or a distributional assumption — which is <b>CSCE 628 "
    "Module 13's methods discipline arriving in a purely theoretical "
    "setting</b>, and is the same habit.",
    "<b>And prefer the concept with the weakest assumptions that "
    "still answers your question</b> — <b>which is almost always "
    "dominant strategies when you are the designer</b> rather than the "
    "analyst (Module 06 &sect;2), because you get to choose the "
    "game."]),
 ],
 "resources": [
   ("Shoham & Leyton-Brown, chapters 3 and 4 (free PDF)",
    "http://www.masfoundations.org/",
    "<b>&sect;&sect;1 to 3</b> — the solution concepts, carefully "
    "distinguished, which is what this module is about."),
   ("Nash &mdash; Equilibrium points in n-person games (free)",
    "https://www.pnas.org/doi/10.1073/pnas.36.1.48",
    "<b>&sect;3</b> — one page, and the proof is the fixed-point "
    "argument in its original form."),
   ("Osborne & Rubinstein &mdash; A Course in Game Theory (free "
    "from the authors, after a one-step registration)",
    "https://www.economics.utoronto.ca/osborne/cgt/",
    "<b>&sect;&sect;2 and 4</b> — rigorous, free, and unusually "
    "careful about what each concept assumes."),
   ("The Gambit game solver (free)",
    "http://www.gambit-project.org/",
    "<b>&sect;4</b> — compute equilibria of small games, and watch it "
    "become infeasible, which is Module 03's point made "
    "experimentally."),
 ],
 "exercises": [
   "<b>Write three games in normal form</b>, with the payoffs "
   "justified.",
   "<b>Change one payoff in the prisoner's dilemma</b> so that "
   "cooperation is dominant, and say what you assumed.",
   "<b>Find the dominant strategies</b> in five games, or show there "
   "are none.",
   "<b>Solve a game by iterated dominance.</b>",
   "<b>Find all pure Nash equilibria</b> of a 3 by 3 game by "
   "inspection.",
   "<b>Find a game with no pure equilibrium</b> and compute its mixed "
   "one.",
   "<b>Derive the indifference condition</b> from the definition.",
   "<b>Find a game with multiple equilibria</b> and say which one you "
   "would predict, and why.",
   "<b>Run a solver</b> on games of increasing size and record where "
   "it stops.",
   "<b>Take a published game-theoretic claim</b> and identify its "
   "payoff assumptions.",
 ],
 "selfcheck": [
   "Give the three components of a game.",
   "Where does the modelling happen, and why does that matter?",
   "Name five solution concepts and what each assumes.",
   "Why are dominant strategies the design target?",
   "What does a Nash equilibrium presuppose?",
   "Why is it a consistency condition rather than a prediction?",
   "State Nash's theorem precisely.",
   "Give its four caveats and which modules address them.",
   "Give three interpretations of a mixed strategy.",
   "Give the analysis order for a small game.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Computing Equilibria",
 "subtitle": "Existence without an algorithm, and a complexity class "
             "built for it.",
 "question": "If it always exists, why can't you find it?",
 "outcomes": [
     "Explain why fixed-point existence gives no algorithm.",
     "Define PPAD and explain what makes it the right class.",
     "State the hardness of computing Nash equilibria.",
     "Explain what the hardness means for prediction.",
     "Identify the tractable special cases.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Existence without construction",
   "blurb": "A gap this course takes seriously."},

  {"t": "callout", "title": "Nash's proof is a fixed-point argument, which establishes existence and provides no way to find the point",
   "kind": "The gap, and why it matters here",
   "body": ["<b>Brouwer's theorem says a continuous map of a ball to "
            "itself has a fixed point</b> — <b>and the proof is "
            "non-constructive</b>, which is a familiar situation in "
            "mathematics and an unfamiliar one in "
            "algorithms.",
            "<b>So 'an equilibrium exists' is compatible with 'no "
            "efficient algorithm finds it'</b> — <b>and this course "
            "takes that gap seriously</b> rather than treating existence "
            "as sufficient.",
            "<b>Which matters practically:</b> <b>if agents cannot "
            "find the equilibrium, predicting that they will play it is "
            "unjustified</b> — <b>a prediction that requires solving an "
            "intractable problem is not a prediction.</b>",
            "<b>And that is this module's real "
            "content</b> — <b>a computational critique of a solution "
            "concept</b>, which is what algorithmic game theory "
            "contributed to economics."]},

  {"t": "section", "label": "Part 2", "title": "PPAD",
   "blurb": "The class, and why it had to be invented."},

  {"t": "code", "kicker": "PPAD", "title": "A class for problems that are guaranteed to have an answer",
   "lang": "text", "code": """
  THE PROBLEM WITH NP
      NP-completeness is about problems where an
      answer might not exist. Nash equilibrium
      ALWAYS has one, so "is there an equilibrium"
      is trivially yes -- there is nothing to
      decide.

  THE IDEA
      define a class by the ARGUMENT that proves
      existence, not by the decision problem.

  PPAD: Polynomial Parity Argument, Directed
      the existence proof is: in a directed graph
      where every node has in-degree and out-degree
      at most one, if there is a source there must
      be another unbalanced node.
      Finding it is the problem. The graph is
      exponential and given implicitly by a circuit.

  AND NASH IS COMPLETE FOR IT
      even for two players (Chen and Deng, 2006)
      which was the surprising part -- two-player
      zero-sum is in P, by linear programming
""",
   "caption": "<b>PPAD is defined by the existence argument rather "
              "than by the decision problem</b> — which is why it "
              "had to be invented for this.",
   "note": "Two-player zero-sum is in P; general two-player is "
           "PPAD-complete. That contrast is the result."},

  {"t": "callout", "title": "And PPAD-hardness is weaker evidence than NP-hardness, which is worth saying",
   "kind": "The honest statement of what is known",
   "body": ["<b>PPAD is contained in NP ∩ coNP-like territory and is "
            "not known to be NP-hard</b> — <b>so a polynomial algorithm "
            "for Nash would not imply P = NP</b>, and the evidence of "
            "difficulty is correspondingly "
            "weaker.",
            "<b>But it is a well-studied class with many natural "
            "complete problems</b> — <b>Brouwer, Sperner, market "
            "equilibria, and Nash</b> — and none of them has yielded, "
            "which is the usual kind of evidence "
            "(CSCE 637 §01).",
            "<b>So the honest claim is: believed hard, on the same "
            "kind of evidence as most complexity "
            "conjectures</b> — <b>and the belief is well "
            "founded.</b>",
            "<b>Which is CSCE 640 §12's "
            "proved/believed/assumed distinction in a second "
            "setting</b> — and the habit transfers "
            "exactly."]},

  {"t": "section", "label": "Part 3", "title": "What follows",
   "blurb": "For anybody using equilibrium as a prediction."},

  {"t": "bullets", "kicker": "Consequences", "title": "The implications, which are genuinely useful",
   "items": [
     "<b>A solution concept that cannot be computed is a weak "
     "predictor</b> — <b>if the analyst cannot find it, assuming "
     "the agents did is not defensible</b>.",
     "",
     "<b>Which pushes attention toward dynamics</b> "
     "(Module 12): <b>what do agents who adapt actually reach, and "
     "how fast?</b>",
     "",
     "<b>And toward approximate equilibria</b>, where nobody gains "
     "more than epsilon — <b>easier, and still not known to be "
     "polynomial for small epsilon.</b>",
     "",
     "<b>And toward designing games whose equilibria are "
     "easy</b> — <b>which is the designer's privilege</b> and is "
     "Module 06's whole approach.",
     "",
     "<b>Which is the constructive reading:</b> <b>if you are "
     "building the mechanism, build one whose equilibrium is "
     "obvious.</b>",
   ],
   "footnote": "<b>If you are building the mechanism, build one "
               "whose equilibrium is obvious</b> — which is the "
               "designer's answer to this module's bad "
               "news."},

  {"t": "section", "label": "Part 4", "title": "The tractable cases",
   "blurb": "Which are the ones worth knowing."},

  {"t": "callout", "title": "Two-player zero-sum is a linear program, and that is the one case that is genuinely easy",
   "kind": "Closing",
   "body": ["<b>Von Neumann's minimax theorem gives the value of a "
            "two-player zero-sum game</b>, and <b>the equilibrium is "
            "the solution of a linear program</b> — <b>which is "
            "CSCE 669 §05's duality, and the two "
            "players' programs are duals.</b>",
            "<b>So zero-sum games are solved</b>, completely and "
            "efficiently — which is why they dominate the applications "
            "where this theory is actually "
            "used.",
            "<b>And potential games are the other good case</b> "
            "(Module 05 §2): <b>best-response dynamics converge, "
            "because every improvement decreases a global "
            "function.</b>",
            "<b>Which is the practical "
            "summary:</b> <b>zero-sum and potential games are "
            "tractable, and general games are not</b> — <b>so check "
            "which you have before assuming an equilibrium will be "
            "reached.</b>"]},
 ],
 "takeaways": [
   "Nash's proof is a fixed-point argument: existence without "
   "construction.",
   "A prediction that requires solving an intractable problem is not a "
   "prediction.",
   "PPAD is defined by the existence argument rather than the decision "
   "problem, which is why it had to be invented.",
   "Two-player zero-sum is in P; general two-player Nash is PPAD-complete, "
   "and that contrast is the result.",
   "PPAD-hardness is weaker evidence than NP-hardness, and the belief is "
   "still well founded.",
   "If you are building the mechanism, build one whose equilibrium is "
   "obvious.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Existence without construction"),
  ("callout", "Nash's proof is a fixed-point argument, which establishes "
              "existence and provides no way to find the point",
   ["<b>Brouwer's theorem says a continuous map from a ball to "
    "itself has a fixed point</b> — <b>and the standard proofs are "
    "non-constructive</b> — <b>which is a familiar situation in "
    "mathematics and a distinctly unfamiliar one in an algorithms "
    "course</b>, where existence proofs are usually algorithms.",
    "<b>So 'an equilibrium exists' is entirely compatible with 'no "
    "efficient algorithm finds it'</b> — <b>and this course takes "
    "that gap seriously</b> rather than treating existence as settling "
    "the matter, which is what distinguishes the algorithmic treatment "
    "from the classical one.",
    "<b>Which matters practically, not just aesthetically:</b> <b>if "
    "the agents cannot find the equilibrium, predicting that they will "
    "play it is unjustified</b> — <b>a prediction that requires "
    "solving an intractable problem is not a prediction</b>, it is a "
    "description of a hypothetical.",
    "<b>And that is this module's real content</b> — <b>a "
    "computational critique of a solution concept</b> — <b>which is "
    "what algorithmic game theory contributed back to economics</b>, and "
    "is a good example of a complexity result changing how a concept is "
    "used rather than only classifying it."]),

  ("h1", "2 &nbsp; PPAD"),
  ("code", """THE PROBLEM WITH NP
    NP-completeness is about problems where an answer
    might not exist. A Nash equilibrium ALWAYS
    exists, so "is there an equilibrium" is
    trivially yes -- there is nothing to decide, and
    the decision framing is useless.

THE IDEA
    define a complexity class by the ARGUMENT that
    proves existence, rather than by the decision
    problem.

PPAD: Polynomial Parity Argument, Directed
    the existence proof is: in a directed graph
    where every node has in-degree and out-degree at
    most one, if there is an unbalanced node then
    there must be another one.
    FINDING the other one is the problem. The graph
    is exponentially large and given implicitly by a
    circuit.

AND NASH IS COMPLETE FOR IT
    even for two players (Chen and Deng, 2006)
    which was the surprising part -- two-player
    zero-sum is in P, by linear programming"""),
  ("p", "<b>PPAD is defined by the existence argument rather than by "
        "the decision problem</b> — <b>which is why it had to be "
        "invented for this</b>, and is a genuinely novel move in "
        "complexity theory (CSCE 637 Module 08's class zoo did not "
        "have a slot for it). <b>Two-player zero-sum is in P; general "
        "two-player Nash is PPAD-complete</b>, <b>and that contrast is "
        "the result</b>: the hardness does not come from many players, "
        "which is where everybody expected it."),
  ("callout", "And PPAD-hardness is weaker evidence than NP-hardness, which "
              "is worth saying",
   ["<b>PPAD sits in territory where a polynomial algorithm would "
    "not collapse anything famous</b> — <b>so a polynomial "
    "algorithm for Nash would not imply P = NP</b>, <b>and the evidence "
    "of difficulty is correspondingly weaker</b> than for an NP-hard "
    "problem.",
    "<b>But it is a well-studied class with many natural complete "
    "problems</b> — <b>Brouwer fixed points, Sperner's lemma, "
    "Arrow-Debreu market equilibria, and Nash</b> — <b>and none of "
    "them has yielded to decades of attention</b>, which is the usual "
    "and perfectly respectable kind of evidence (CSCE 637 "
    "Module 01's framing of conditional hardness).",
    "<b>So the honest claim is: believed hard, on the same kind of "
    "evidence as most complexity conjectures</b> — <b>and the "
    "belief is well founded</b> — which is a more careful statement "
    "than 'computing Nash equilibria is hard' and means the same thing "
    "to anyone who reads it carefully.",
    "<b>Which is CSCE 640 Module 12's "
    "proved/believed-with-evidence/assumed distinction arriving in a "
    "second setting</b> — and <b>the habit transfers exactly</b>, "
    "which is part of why the two courses sit in the same "
    "semester."]),

  ("break",),
  ("h1", "3 &nbsp; What follows"),
  ("ul", ["<b>A solution concept that cannot be computed is a weak "
          "predictor</b> — <b>if the analyst with a computer cannot "
          "find it, assuming the agents found it is not "
          "defensible</b>, and this is the argument that gave the "
          "hardness result its influence.",
          "<b>Which pushes attention toward dynamics</b> "
          "(Module 12): <b>what do agents who adapt over time "
          "actually reach, and how quickly?</b> — a question with "
          "better answers, and ones that do not require anybody to solve "
          "a hard problem.",
          "<b>And toward approximate equilibria</b>, in which no "
          "agent gains more than &epsilon; by deviating — "
          "<b>easier than exact, and still not known to be polynomial "
          "for small &epsilon;</b>, which is a sobering refinement of "
          "the bad news.",
          "<b>And toward designing games whose equilibria are "
          "easy to find</b> — <b>which is the designer's "
          "privilege</b>, since the designer chooses the game, <b>and is "
          "Module 06's entire approach</b>.",
          "<b>Which is the constructive reading of this "
          "module:</b> <b>if you are building the mechanism, build one "
          "whose equilibrium is obvious</b> — ideally one where "
          "each agent has a dominant strategy and does not need to reason "
          "about anybody else at all (Module 02 &sect;2)."]),

  ("h1", "4 &nbsp; The tractable cases"),
  ("callout", "Two-player zero-sum is a linear program, and that is the one "
              "case that is genuinely easy",
   ["<b>Von Neumann's minimax theorem gives a well-defined value for "
    "any two-player zero-sum game</b>, and <b>the equilibrium "
    "strategies are the solution of a linear program</b> — "
    "<b>which is CSCE 669 Module 05's duality</b>, and <b>the two "
    "players' programs are duals of each other</b>, which is where the "
    "minimax theorem comes from.",
    "<b>So zero-sum games are solved</b>, completely and "
    "efficiently, for any size — <b>which is why they dominate the "
    "applications where this theory is actually deployed</b>: security "
    "games, some auction analyses, and the game-playing work in "
    "CSCE 625 and CSCE 642.",
    "<b>And potential games are the other good case</b> "
    "(Module 05 &sect;2): <b>best-response dynamics converge, "
    "because every improving deviation decreases a single global "
    "potential function</b> — which both guarantees a pure "
    "equilibrium exists and gives an algorithm that finds one.",
    "<b>Which is the practical summary:</b> <b>zero-sum and "
    "potential games are tractable, and general games are not</b> "
    "— <b>so check which kind you have before assuming an "
    "equilibrium will be reached</b>, which is a two-minute check with a "
    "large payoff."]),
 ],
 "resources": [
   ("Daskalakis, Goldberg & Papadimitriou &mdash; The complexity of "
    "computing a Nash equilibrium (free)",
    "https://people.csail.mit.edu/costis/simplified.pdf",
    "<b>&sect;2</b> — the hardness result, with a simplified proof by "
    "the authors."),
   ("Papadimitriou &mdash; On the complexity of the parity argument "
    "(free)",
    "https://www.sciencedirect.com/science/article/pii/S0022000005800637",
    "<b>&sect;2</b> — where PPAD was defined, and the motivation is "
    "stated plainly."),
   ("Nisan et al., chapter 2 (free PDF)",
    "https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf",
    "<b>&sect;&sect;1 to 3</b> — the computational treatment of "
    "equilibrium, including the algorithms that do work."),
   ("Roughgarden &mdash; lectures on complexity of equilibria (free)",
    "http://timroughgarden.org/notes.html",
    "<b>&sect;&sect;3 and 4</b> — including the argument for why "
    "hardness matters for the concept's use."),
 ],
 "exercises": [
   "<b>State why a non-constructive existence proof is unsatisfying "
   "here.</b>",
   "<b>Explain why NP-completeness is the wrong framing</b> for Nash.",
   "<b>Describe the PPAD existence argument</b> in your own words.",
   "<b>Name three other PPAD-complete problems.</b>",
   "<b>Explain why PPAD-hardness is weaker evidence than "
   "NP-hardness.</b>",
   "<b>Solve a zero-sum game by linear programming</b> and verify "
   "minimax.",
   "<b>Show that the two players' programs are duals.</b>",
   "<b>Find a potential function</b> for a small congestion game.",
   "<b>Run best-response dynamics</b> on it and watch the potential "
   "decrease.",
   "<b>Try the same on a general game</b> and find a cycle.",
 ],
 "selfcheck": [
   "Why does Nash's proof give no algorithm?",
   "Why does that matter for prediction?",
   "Why is NP the wrong class for this problem?",
   "What is PPAD defined by, and what is its existence argument?",
   "What is complete for it, and what was surprising?",
   "Why is PPAD-hardness weaker evidence, and is the belief still "
   "sound?",
   "Give three consequences of the hardness.",
   "What is the constructive reading?",
   "Why is two-player zero-sum easy, and what does it reduce to?",
   "What is the other tractable class, and why does it converge?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "The Price of Anarchy",
 "subtitle": "What selfish behaviour costs, measured.",
 "question": "How much worse is the equilibrium than the optimum?",
 "outcomes": [
     "Define the price of anarchy and the price of stability.",
     "Compute both for small examples.",
     "Explain the smoothness framework.",
     "State the routing bound and its conditions.",
     "Use the measure to decide whether to intervene.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The definition",
   "blurb": "A ratio, and the choice of which equilibrium matters."},

  {"t": "eq", "kicker": "Definition", "title": "Two ratios, and the difference between them",
   "eqs": [
     ("price of anarchy = (worst equilibrium cost) / (optimal cost)",
      "The guarantee: however badly the agents coordinate, the "
      "outcome is no worse than this factor."),
     ("price of stability = (best equilibrium cost) / (optimal cost)",
      "The best you could hope for if you could suggest an "
      "equilibrium. Relevant when a designer can propose a starting "
      "point."),
     ("both ≥ 1, and both depend on the solution concept used",
      "A price of anarchy over mixed equilibria may exceed the one "
      "over pure equilibria, since there are more of them."),
   ],
   "caption": "<b>Price of anarchy is a worst case over "
              "equilibria</b>, so it is a guarantee — and price of "
              "stability is a best case, so it is an "
              "aspiration.",
   "note": "Which ratio you want depends on whether you can "
           "coordinate the agents."},

  {"t": "callout", "title": "And it turns a qualitative complaint into a number, which is why the measure matters",
   "kind": "What the framework contributed",
   "body": ["<b>'Selfish behaviour is inefficient' was known and was "
            "not actionable</b> — <b>'selfish routing costs at most "
            "33% more with linear latencies' is a bound you can design "
            "against.</b>",
            "<b>So the measure converts a general worry into an "
            "engineering quantity</b> — <b>which is this semester's "
            "recurring move</b> (CSCE 679 §02's channel ranking, "
            "CSCE 632 §13's measurement).",
            "<b>And a small price of anarchy is a licence to do "
            "nothing</b>: <b>if the equilibrium is within a few percent "
            "of optimal, centralised control is not worth "
            "its cost.</b>",
            "<b>Which is the practical use of the "
            "concept</b> — <b>it tells you when to intervene and when "
            "the decentralised system is already good "
            "enough.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Examples",
   "blurb": "Where the ratio is small and where it is unbounded."},

  {"t": "code", "kicker": "Examples", "title": "The range, which is wide",
   "lang": "text", "code": """
  PIGOU'S EXAMPLE
      two parallel roads, unit traffic
      road 1: latency 1, regardless of load
      road 2: latency = x, the fraction using it
      equilibrium: everyone takes road 2 (always
          at most 1), total cost 1
      optimum: split half and half, total cost 3/4
      price of anarchy = 4/3

  AND WITH NONLINEAR LATENCY
      replace x with x^d and the ratio grows without
      bound as d grows. The bound DEPENDS ON THE
      CLASS OF LATENCY FUNCTIONS.

  LOAD BALANCING, identical machines
      price of anarchy is small and constant

  AND UNBOUNDED CASES EXIST
      some network design and scheduling games have
      equilibria arbitrarily worse than optimal,
      which is the case for intervening
""",
   "caption": "<b>The bound depends on the class of latency "
              "functions allowed</b> — which is the condition most "
              "often dropped when the 33% figure is "
              "quoted."},

  {"t": "section", "label": "Part 3", "title": "Smoothness",
   "blurb": "The technique that made the bounds general."},

  {"t": "callout", "title": "A smoothness argument bounds the price of anarchy without analysing the equilibrium at all",
   "kind": "Why the framework is elegant",
   "body": ["<b>If the game satisfies an inequality relating any "
            "outcome to the optimum</b> — <b>roughly, that deviating "
            "toward the optimum does not cost too much</b> — <b>a "
            "bound follows mechanically.</b>",
            "<b>And the bound then applies to every "
            "equilibrium concept that satisfies the deviation "
            "condition</b> — <b>pure Nash, mixed Nash, correlated, and "
            "the outcomes of no-regret learning</b> "
            "(Module 12 §3).",
            "<b>Which is the remarkable "
            "part:</b> <b>one inequality, proved once about the game, "
            "bounds a whole family of behaviours</b> including ones you "
            "did not analyse.",
            "<b>And it means the bound survives agents who do not "
            "play equilibrium</b> — <b>which answers "
            "Module 03's objection directly</b>, and is why the "
            "framework mattered."]},

  {"t": "section", "label": "Part 4", "title": "Using it",
   "blurb": "To decide whether to build the centralised thing."},

  {"t": "bullets", "kicker": "Practice", "title": "The questions, for a real system",
   "items": [
     "<b>What is the benchmark?</b> — <b>'optimal' means "
     "optimal for a stated objective</b>, and the objective is a "
     "design choice (total cost, maximum cost, "
     "fairness).",
     "",
     "<b>Which equilibrium concept?</b> — <b>and does the "
     "bound hold for the behaviour you actually expect</b> "
     "(Part 3's answer is often "
     "yes).",
     "",
     "<b>What class of cost functions?</b> — <b>which is "
     "where the bound comes from</b> (Part 2), and is "
     "the condition that gets dropped.",
     "",
     "<b>Is the worst case the relevant case?</b> — "
     "<b>a bad worst case with good typical behaviour may not justify "
     "intervention</b>, which Project 1 measures.",
     "",
     "<b>And what would the centralised alternative actually "
     "cost?</b> — <b>in latency, in trust, and in the "
     "incentive to misreport to the "
     "coordinator</b> (Module 01).",
   ],
   "footnote": "<b>The centralised alternative has its own incentive "
               "problem</b> — agents report to the coordinator, and "
               "now the coordinator's input is strategic "
               "too."},

  {"t": "callout", "title": "And the honest summary",
   "kind": "Closing",
   "body": ["<b>The price of anarchy is frequently small, which is "
            "genuinely good news</b> — <b>decentralised systems are "
            "often nearly optimal</b>, and that is worth knowing before "
            "building a coordinator.",
            "<b>And where it is large, the measure tells you how "
            "much a fix is worth</b> — <b>which bounds the budget for "
            "the intervention.</b>",
            "<b>Plus the bounds are worst case over "
            "instances</b> — <b>so a measured distribution on your "
            "actual instances is more useful than the "
            "theorem</b> (Project 1).",
            "<b>Which is this module's version of the program's "
            "rule:</b> <b>name the benchmark, the concept, and the "
            "function class</b> — <b>and a ratio quoted without all "
            "three is not a number.</b>"]},
 ],
 "takeaways": [
   "Price of anarchy is a worst case over equilibria, so it is a guarantee; "
   "price of stability is a best case, so it is an aspiration.",
   "The measure converts a general worry into an engineering quantity you "
   "can design against.",
   "A small price of anarchy is a licence to do nothing, which is its most "
   "useful practical consequence.",
   "The bound depends on the class of cost functions allowed, which is the "
   "condition most often dropped.",
   "A smoothness argument bounds a whole family of behaviours, including "
   "ones you did not analyse.",
   "The centralised alternative has its own incentive problem, because now "
   "the coordinator's input is strategic.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The definition"),
  ("eq", "price of anarchy = (cost of worst equilibrium) / (optimal "
         "cost);&nbsp;&nbsp; price of stability = (cost of best "
         "equilibrium) / (optimal cost)"),
  ("ul", ["<b>The price of anarchy is a worst case over "
          "equilibria</b>, <b>so it is a guarantee</b>: however badly "
          "the agents coordinate among the stable outcomes, the result is "
          "no worse than that factor.",
          "<b>The price of stability is a best case</b>, <b>so it is "
          "an aspiration</b>: it is what you could achieve if you were "
          "able to suggest which equilibrium to play — <b>relevant "
          "whenever a designer can propose a starting configuration</b> "
          "and the agents have no reason to move away from it.",
          "<b>Both are at least 1, and both depend on the solution "
          "concept used</b> — <b>a price of anarchy taken over "
          "mixed equilibria may exceed the one over pure "
          "equilibria</b>, simply because there are more mixed "
          "equilibria to be worst over (Module 02 &sect;2's "
          "hierarchy).",
          "<b>Which ratio you want depends on whether you can "
          "coordinate the agents at all</b> — and in most "
          "engineered systems you can suggest a default configuration, "
          "which makes the price of stability the more relevant "
          "number."]),
  ("callout", "And it turns a qualitative complaint into a number, which is "
              "why the measure matters",
   ["<b>'Selfish behaviour is inefficient' was known for decades and "
    "was not actionable</b> — <b>'selfish routing costs at most "
    "33% more than optimal when latencies are linear' is a bound you can "
    "design against</b>, budget against, and check.",
    "<b>So the measure converts a general worry into an engineering "
    "quantity</b> — <b>which is this semester's and this "
    "program's recurring move</b> (CSCE 679 Module 02's measured "
    "channel ranking, CSCE 632 Module 13's substituted "
    "measurement).",
    "<b>And a small price of anarchy is a licence to do "
    "nothing</b>: <b>if the equilibrium is within a few percent of "
    "optimal, centralised control is not worth its cost</b> in latency, "
    "complexity, and the new incentive problem it creates (&sect;4).",
    "<b>Which is the genuinely practical use of the "
    "concept</b> — <b>it tells you when to intervene and when the "
    "decentralised system you already have is good enough</b>, which is "
    "a question engineers face constantly and usually answer by "
    "intuition."]),

  ("h1", "2 &nbsp; Examples"),
  ("code", """PIGOU'S EXAMPLE
    two parallel roads, one unit of traffic
    road 1: latency 1, regardless of load
    road 2: latency = x, the fraction using it
    equilibrium: everyone takes road 2 (it is always
        at most 1), total cost 1
    optimum: split half and half, total cost 3/4
    price of anarchy = 4/3

AND WITH NONLINEAR LATENCY
    replace x with x^d and the ratio grows without
    bound as d grows. The bound DEPENDS ON THE CLASS
    OF LATENCY FUNCTIONS ALLOWED.

LOAD BALANCING, identical machines
    the price of anarchy is small and constant

AND UNBOUNDED CASES EXIST
    some network design and scheduling games have
    equilibria arbitrarily worse than optimal, which
    is precisely the case for intervening"""),
  ("p", "<b>The bound depends on the class of latency functions "
        "allowed</b> — <b>which is the condition most often dropped "
        "when the 33% figure is quoted</b>, and it is not a technicality: "
        "with polynomial latencies of degree d the ratio grows roughly "
        "like d / ln d, which is unbounded. Pigou's example is worth "
        "working by hand: it is two roads and four lines of arithmetic, "
        "and it contains the whole phenomenon."),

  ("break",),
  ("h1", "3 &nbsp; Smoothness"),
  ("callout", "A smoothness argument bounds the price of anarchy without "
              "analysing the equilibrium at all",
   ["<b>If the game satisfies a particular inequality relating any "
    "outcome to the optimal one</b> — <b>roughly, that each agent "
    "deviating toward its role in the optimum does not cost the system "
    "too much</b> — <b>then a bound on the price of anarchy "
    "follows mechanically</b> from the definition of equilibrium.",
    "<b>And the resulting bound applies to every solution concept "
    "that satisfies the deviation condition</b> — <b>pure Nash, "
    "mixed Nash, correlated equilibria, and the time-averaged outcomes "
    "of no-regret learning</b> (Module 12 &sect;3) — because all "
    "of them satisfy the one inequality the proof uses.",
    "<b>Which is the remarkable part:</b> <b>one inequality, proved "
    "once about the game itself, bounds an entire family of "
    "behaviours</b> — <b>including ones you never analysed and "
    "ones that had not been defined when the bound was proved.</b>",
    "<b>And it means the bound survives agents who do not play "
    "equilibrium at all</b> — <b>which answers Module 03's "
    "objection directly</b>: you no longer need the agents to solve a "
    "PPAD-complete problem for the guarantee to hold, only to not "
    "persistently regret their choices. <b>That is why the framework "
    "mattered</b> rather than being one more bounding "
    "technique."]),

  ("h1", "4 &nbsp; Using it"),
  ("ul", ["<b>What is the benchmark?</b> — <b>'optimal' means "
          "optimal with respect to a stated objective</b>, <b>and the "
          "objective is a design choice</b>: total cost, maximum cost "
          "(makespan), or some fairness criterion give different "
          "optima and different ratios.",
          "<b>Which equilibrium concept?</b> — <b>and does the "
          "bound hold for the behaviour you actually expect</b> from "
          "your agents? <b>&sect;3's answer is frequently yes</b>, which "
          "is the smoothness framework's practical payoff.",
          "<b>What class of cost functions?</b> — <b>which is "
          "where the bound comes from</b> (&sect;2), <b>and is the "
          "condition that gets dropped in summary</b>, turning a "
          "conditional theorem into a false general claim.",
          "<b>Is the worst case the relevant case?</b> — "
          "<b>a bad worst-case bound with good typical behaviour may not "
          "justify intervention</b>, <b>which is what Project 1 "
          "measures</b> by reporting the distribution of ratios rather "
          "than the maximum.",
          "<b>And what would the centralised alternative actually "
          "cost?</b> — <b>in latency, in trust, in operational "
          "complexity, and in the incentive to misreport to the "
          "coordinator</b> (Module 01 &sect;2). <b>The centralised "
          "alternative has its own incentive problem</b>: <b>agents now "
          "report to the coordinator, and the coordinator's input is "
          "strategic too</b> — which is the trap in 'just centralise "
          "it'."]),
  ("callout", "And the honest summary",
   ["<b>The price of anarchy is frequently small, which is genuinely "
    "good news</b> — <b>decentralised systems are often nearly "
    "optimal</b> — <b>and that is worth knowing before building a "
    "coordinator</b> that will be expensive and will introduce a new "
    "strategic surface.",
    "<b>And where it is large, the measure tells you how much a fix "
    "is worth</b> — <b>which bounds the sensible budget for the "
    "intervention</b> and makes the decision quantitative rather than "
    "architectural taste.",
    "<b>Plus the bounds are worst case over instances</b> — "
    "<b>so a measured distribution over your actual instances is more "
    "useful than the theorem</b> for an engineering decision "
    "(Project 1's requirement), while the theorem is what tells you the "
    "measurement cannot be arbitrarily bad.",
    "<b>Which is this module's version of the program's rule:</b> "
    "<b>name the benchmark, the solution concept, and the function "
    "class</b> — <b>and a ratio quoted without all three is not a "
    "number</b>, which is the same shape as CSCE 640 Module 13's "
    "three requirements."]),
 ],
 "resources": [
   ("Koutsoupias & Papadimitriou &mdash; Worst-case equilibria (free)",
    "https://link.springer.com/chapter/10.1007/3-540-49116-3_38",
    "<b>&sect;1</b> — where the measure was introduced, in a load "
    "balancing setting."),
   ("Roughgarden & Tardos &mdash; How bad is selfish routing? (free)",
    "https://dl.acm.org/doi/10.1145/506147.506153",
    "<b>&sect;2's routing bound</b> — with the latency function "
    "condition made explicit, as it should be."),
   ("Roughgarden &mdash; Intrinsic robustness of the price of anarchy "
    "(free)",
    "https://dl.acm.org/doi/10.1145/2806883",
    "<b>&sect;3's smoothness framework</b> — and the extension to "
    "no-regret outcomes is the result that matters."),
   ("Nisan et al., chapters 17 to 19 (free PDF)",
    "https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf",
    "<b>&sect;&sect;2 and 4</b> — the bounds for routing, load "
    "balancing, and network design."),
 ],
 "exercises": [
   "<b>Define both ratios</b> and give a game where they differ.",
   "<b>Work Pigou's example</b> by hand, both costs.",
   "<b>Replace the latency with x³</b> and recompute the ratio.",
   "<b>Find the ratio for x^d</b> as a function of d.",
   "<b>Compute the price of anarchy</b> for a two-machine load "
   "balancing game.",
   "<b>Find a game with unbounded price of anarchy.</b>",
   "<b>State the smoothness inequality</b> and what it gives you.",
   "<b>Explain why the bound extends to no-regret play.</b>",
   "<b>For one real system you know, name the benchmark, the concept, "
   "and the function class.</b>",
   "<b>Estimate what centralising it would cost</b>, including the new "
   "incentive problem.",
 ],
 "selfcheck": [
   "Define both ratios and say which is a guarantee.",
   "Why does the concept used change the number?",
   "What did the measure contribute over 'selfishness is "
   "inefficient'?",
   "When is a small price of anarchy actionable?",
   "Work Pigou's example and give the ratio.",
   "What happens with nonlinear latencies?",
   "Which condition is usually dropped when quoting the bound?",
   "What does a smoothness argument prove, and over what family?",
   "Why does that answer the computability objection?",
   "Give the five questions for applying this to a real system.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Routing and Congestion",
 "subtitle": "The canonical application, and the paradox worth "
             "building.",
 "question": "Can adding a road make everyone slower?",
 "outcomes": [
     "Model routing as a congestion game.",
     "Explain potential functions and what they guarantee.",
     "Construct and explain Braess's paradox.",
     "Explain tolls and other interventions.",
     "Apply the framework to a computing system.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "Which covers far more than traffic."},

  {"t": "callout", "title": "A congestion game is agents choosing resource sets, where each resource's cost depends only on how many chose it",
   "kind": "The model, and why it is general",
   "body": ["<b>Each agent picks a subset of resources</b> — a "
            "path, a set of machines, a set of "
            "links — <b>and each resource's cost is a function of "
            "its load</b>, identical for everyone using "
            "it.",
            "<b>Which covers traffic, network routing, load "
            "balancing, shared caches, bandwidth, and any contended "
            "resource</b> — <b>the structure is the same and the "
            "vocabulary differs.</b>",
            "<b>And the key property is that an agent's cost depends "
            "on others only through the counts</b> — <b>not on who "
            "they are</b>, which is what makes the analysis "
            "work.",
            "<b>So the model is narrow enough to prove things about "
            "and wide enough to apply</b> — <b>which is an unusually "
            "good position for a model</b> and is why this is the "
            "canonical case."]},

  {"t": "section", "label": "Part 2", "title": "Potential functions",
   "blurb": "Which give existence and convergence together."},

  {"t": "eq", "kicker": "Rosenthal", "title": "The potential, and what it buys",
   "eqs": [
     ("Φ(S) = Σ over resources r of Σ from i=1 to load(r) of c_r(i)",
      "Sum, over each resource, of its cost at each load level up to "
      "the current one. A single global function of the whole "
      "profile."),
     ("any single agent's improving deviation decreases Φ by exactly "
      "its own gain",
      "Which is the magic: a selfish improvement and a decrease in "
      "the global potential are the same event."),
     ("so: pure Nash equilibria exist, and best-response dynamics "
      "converge",
      "Φ is bounded and strictly decreases, so the process "
      "terminates — at a local minimum of Φ, which is a pure "
      "equilibrium."),
   ],
   "caption": "<b>A selfish improvement and a decrease in the global "
              "potential are the same event</b> — which is what "
              "makes congestion games tractable "
              "(Module 03 §4).",
   "note": "The potential is not the social cost; the two differ, "
           "and that gap is the price of anarchy."},

  {"t": "callout", "title": "And the potential is not the social cost, which is exactly where the inefficiency lives",
   "kind": "A point worth being precise about",
   "body": ["<b>Φ sums each resource's cost over every load level up "
            "to the current one</b>; <b>the social cost is load times "
            "cost at the current load</b> — <b>different "
            "functions.</b>",
            "<b>So minimising Φ, which is what the dynamics do, is "
            "not minimising social cost</b> — <b>and the discrepancy "
            "is precisely the price of anarchy</b> "
            "(Module 04).",
            "<b>Which gives an intuition for the "
            "inefficiency:</b> <b>an agent joining a resource pays the "
            "current cost and ignores the increase it imposes on "
            "everybody already there</b> — the "
            "externality.",
            "<b>And that observation is the design "
            "fix</b> (Part 4): <b>charge the "
            "externality</b>, and selfish choice becomes socially "
            "optimal."]},

  {"t": "section", "label": "Part 3", "title": "Braess's paradox",
   "blurb": "Which is worth constructing yourself."},

  {"t": "code", "kicker": "Braess", "title": "Adding capacity makes everyone worse off",
   "lang": "text", "code": """
  THE NETWORK, one unit of traffic from s to t
      s -> v : latency x      v -> t : latency 1
      s -> w : latency 1      w -> t : latency x

      equilibrium: half take s-v-t, half s-w-t
      each pays 1/2 + 1 = 3/2

  NOW ADD a zero-latency link v -> w
      s -> v -> w -> t has latency x + 0 + x
      for any single agent this is better than 3/2
      so EVERYONE switches
      new equilibrium: all use s-v-w-t, cost
          1 + 0 + 1 = 2

  EVERYBODY IS WORSE OFF (2 > 3/2) AFTER ADDING
  CAPACITY. No one behaved irrationally; the new
  route is genuinely better given what others do.

  AND IT IS NOT A CURIOSITY: removing roads has
  improved traffic in real cities.
""",
   "caption": "<b>Nobody behaved irrationally</b> — the new route "
              "is genuinely better for each agent given what the others "
              "are doing, and the result is worse for "
              "all.",
   "note": "Project 1 asks you to construct and verify this."},

  {"t": "section", "label": "Part 4", "title": "Interventions",
   "blurb": "What a designer can actually do."},

  {"t": "bullets", "kicker": "Fixes", "title": "The options, and what each costs",
   "items": [
     "<b>Marginal cost tolls</b> — <b>charge each agent the "
     "externality it imposes</b>, and the equilibrium becomes "
     "optimal — <b>which is clean and requires knowing the cost "
     "functions.</b>",
     "",
     "<b>Capacity: add it carefully</b> — "
     "<b>Part 3 shows that adding capacity can hurt</b>, "
     "so network changes need checking rather than "
     "assuming.",
     "",
     "<b>Restrict the strategy space</b> — remove the "
     "problematic route, which is crude and is what cities do.",
     "",
     "<b>Stackelberg routing</b> — <b>centrally control a "
     "fraction of the traffic and let the rest "
     "choose</b>, which improves the equilibrium with partial "
     "control.",
     "",
     "<b>And doing nothing</b>, when the price of anarchy is "
     "small (Module 04 §4) — which is frequently the right "
     "answer.",
   ],
   "footnote": "<b>Marginal cost pricing requires knowing the cost "
               "functions</b> — and in a computing system you often "
               "do, which makes this more applicable here than in "
               "traffic."},

  {"t": "callout", "title": "And the computing applications are direct",
   "kind": "Closing",
   "body": ["<b>Load balancers, content delivery routing, BGP, "
            "shared caches, and database connection "
            "pools</b> — <b>all congestion games</b>, and all exhibit "
            "the same inefficiency.",
            "<b>And the externality framing is the useful "
            "one</b>: <b>a client retrying aggressively imposes cost on "
            "everybody else and bears a fraction of "
            "it</b> — which is why retry storms "
            "happen.",
            "<b>So backoff, admission control, and rate limiting are "
            "all externality pricing in disguise</b> — <b>and seeing "
            "them that way suggests when they will and will not "
            "work.</b>",
            "<b>Which is the value of the model "
            "here</b> — <b>not the traffic examples, but recognising "
            "the structure in systems you build</b> "
            "(Module 01 §2)."]},
 ],
 "takeaways": [
   "A congestion game covers any contended resource whose cost depends only "
   "on how many agents chose it.",
   "A selfish improvement and a decrease in the global potential are the "
   "same event, which gives existence and convergence together.",
   "The potential is not the social cost, and the gap is where the "
   "inefficiency lives.",
   "An agent joining a resource ignores the increase it imposes on everybody "
   "already there — the externality.",
   "In Braess's paradox nobody behaves irrationally and everybody ends up "
   "worse off after capacity is added.",
   "Backoff, admission control, and rate limiting are externality pricing "
   "in disguise.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The model"),
  ("callout", "A congestion game is agents choosing resource sets, where each "
              "resource's cost depends only on how many chose it",
   ["<b>Each agent picks a subset of resources</b> — a path "
    "through a network, a set of machines, a set of links — "
    "<b>and each resource's cost is a function of its load</b>, "
    "<b>identical for everyone using it</b>.",
    "<b>Which covers road traffic, network routing, load balancing, "
    "shared caches, bandwidth allocation, and essentially any contended "
    "resource</b> — <b>the structure is identical and only the "
    "vocabulary differs</b>, which is what makes this the canonical "
    "application of the whole field.",
    "<b>And the key property is that an agent's cost depends on the "
    "others only through the counts</b> — <b>not on who they "
    "are</b> — <b>which is exactly what makes the potential "
    "function argument work</b> (&sect;2) and is the condition to check "
    "before applying any of this.",
    "<b>So the model is narrow enough to prove strong things about "
    "and wide enough to apply to real systems</b> — <b>which is an "
    "unusually good position for a model to be in</b>, and is why "
    "congestion games get a module of their own rather than an "
    "example."]),

  ("h1", "2 &nbsp; Potential functions"),
  ("eq", "&Phi;(S) = &Sigma;<sub>r</sub> "
         "&Sigma;<sub>i=1</sub><sup>load(r)</sup> c<sub>r</sub>(i)"),
  ("ul", ["<b>Sum, over each resource, of that resource's cost at "
          "each load level from 1 up to its current load</b> — "
          "<b>a single global function of the entire strategy "
          "profile</b>, due to Rosenthal.",
          "<b>And any single agent's improving deviation decreases "
          "&Phi; by exactly that agent's own gain</b> — <b>which "
          "is the magic of the construction</b>: <b>a selfish "
          "improvement and a decrease in the global potential are the "
          "same event</b>, so the two perspectives coincide move by "
          "move.",
          "<b>So pure Nash equilibria exist, and best-response "
          "dynamics converge to one</b>: <b>&Phi; takes finitely many "
          "values and strictly decreases at every step, so the process "
          "must terminate</b> — <b>at a local minimum of &Phi;, "
          "which is precisely a pure equilibrium.</b>",
          "<b>Which is Module 03 &sect;4's second tractable "
          "case</b>, and it is why congestion games are the setting in "
          "which equilibrium analysis is actually usable rather than "
          "merely definable."]),
  ("callout", "And the potential is not the social cost, which is exactly "
              "where the inefficiency lives",
   ["<b>&Phi; sums each resource's cost over every load level up to "
    "the current one</b>; <b>the social cost is the load multiplied by "
    "the cost at the current load</b> — <b>two different functions "
    "of the same profile</b>, and they are only equal for constant cost "
    "functions.",
    "<b>So minimising &Phi;, which is what the dynamics actually "
    "do, is not minimising social cost</b> — <b>and the "
    "discrepancy between them is precisely the price of anarchy</b> "
    "(Module 04), which gives that ratio a mechanical "
    "explanation.",
    "<b>Which gives the right intuition for the "
    "inefficiency:</b> <b>an agent joining a resource pays the current "
    "cost and ignores the increase it thereby imposes on everybody "
    "already using it</b> — <b>the externality</b> — and sums "
    "of private costs are not the social cost.",
    "<b>And that observation is immediately the design fix</b> "
    "(&sect;4): <b>charge each agent the externality it imposes</b>, "
    "<b>and selfish choice becomes socially optimal</b> — which is "
    "one of the cleanest results in the subject."]),

  ("break",),
  ("h1", "3 &nbsp; Braess's paradox"),
  ("code", """THE NETWORK, one unit of traffic from s to t
    s -> v : latency x      v -> t : latency 1
    s -> w : latency 1      w -> t : latency x

    equilibrium: half take s-v-t, half take s-w-t
    each pays 1/2 + 1 = 3/2

NOW ADD a zero-latency link v -> w
    s -> v -> w -> t has latency x + 0 + x
    for any single agent this is better than 3/2
    so EVERYONE switches
    new equilibrium: all use s-v-w-t, with cost
        1 + 0 + 1 = 2

EVERYBODY IS WORSE OFF (2 > 3/2) AFTER ADDING
CAPACITY. No one behaved irrationally; the new route
really is better for each agent given what the others
are doing.

AND IT IS NOT A CURIOSITY: removing roads has
improved traffic flow in real cities."""),
  ("p", "<b>Nobody behaved irrationally</b> — the new route is "
        "genuinely better for each individual agent given what the others "
        "are doing, at every point in the process, <b>and the result is "
        "worse for all of them</b>. That is the whole content of the "
        "paradox, and it is why 'the agents should just coordinate' is "
        "not an analysis. <b>Project 1 asks you to construct and verify "
        "this</b>, because building it is considerably more convincing "
        "than reading it."),

  ("h1", "4 &nbsp; Interventions"),
  ("ul", ["<b>Marginal cost tolls</b> — <b>charge each agent "
          "the externality it imposes on the others</b>, and <b>the "
          "resulting equilibrium is socially optimal</b> — "
          "<b>which is clean, provable, and requires knowing the cost "
          "functions</b>.",
          "<b>Capacity: add it carefully</b> — <b>&sect;3 shows "
          "that adding capacity can make things worse</b>, <b>so network "
          "changes need checking rather than assuming</b>, which is an "
          "unusual engineering conclusion and a correct one.",
          "<b>Restrict the strategy space</b> — remove the "
          "problematic route entirely — <b>which is crude, "
          "effective, and is what cities do</b> when they close a "
          "road.",
          "<b>Stackelberg routing</b> — <b>centrally control "
          "some fraction of the traffic and let the remainder choose "
          "freely</b> — <b>which improves the equilibrium with only "
          "partial control</b>, and is directly applicable when you own "
          "some of the clients.",
          "<b>And doing nothing, when the price of anarchy is "
          "small</b> (Module 04 &sect;4) — <b>which is frequently "
          "the right answer</b> and is the one an engineer is least "
          "likely to propose. <b>Marginal cost pricing requires knowing "
          "the cost functions</b> — <b>and in a computing system "
          "you frequently do</b>, which makes this far more applicable "
          "here than in road traffic."]),
  ("callout", "And the computing applications are direct",
   ["<b>Load balancers, content delivery routing, inter-domain "
    "routing, shared caches, database connection pools, and thread "
    "pools</b> — <b>all congestion games</b>, and all exhibiting "
    "the same structural inefficiency once clients choose for "
    "themselves.",
    "<b>And the externality framing is the useful one</b>: <b>a "
    "client retrying aggressively imposes cost on everybody else and "
    "bears only a fraction of it</b> — <b>which is exactly why "
    "retry storms happen</b>, and why they are not fixed by asking "
    "clients to be considerate.",
    "<b>So exponential backoff, admission control, and rate limiting "
    "are all externality pricing in disguise</b> — <b>and seeing "
    "them that way suggests when they will and will not work</b>: they "
    "work when the price tracks the externality, and fail when it does "
    "not (a fixed rate limit under-prices at low load and over-prices at "
    "high).",
    "<b>Which is the real value of this model for this "
    "program</b> — <b>not the traffic examples, but recognising the "
    "structure in systems you build</b> (Module 01 &sect;2's table, "
    "and CSCE 678's distributed systems material, where these "
    "mechanisms appear without the game-theoretic "
    "vocabulary)."]),
 ],
 "resources": [
   ("Rosenthal &mdash; A class of games possessing pure-strategy Nash "
    "equilibria",
    "https://link.springer.com/article/10.1007/BF01737559",
    "<b>&sect;2's potential function</b>, in the original — three "
    "pages."),
   ("Braess (1968), translated (free)",
    "https://homepage.ruhr-uni-bochum.de/Dietrich.Braess/paradox.pdf",
    "<b>&sect;3</b> — the paradox in its original form, with the "
    "translation and commentary."),
   ("Roughgarden &mdash; Selfish Routing and the Price of Anarchy",
    "https://mitpress.mit.edu/9780262182430/",
    "<b>&sect;&sect;1 to 4</b> — the book-length treatment, including "
    "tolls and Stackelberg routing. Library copy."),
   ("Nisan et al., chapters 18 and 19 (free PDF)",
    "https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf",
    "<b>&sect;&sect;2 and 4</b> — potential games and the "
    "interventions, with the proofs."),
 ],
 "exercises": [
   "<b>Model three computing systems</b> as congestion games.",
   "<b>Check the counts-only condition</b> in each, and find one where "
   "it fails.",
   "<b>Compute Rosenthal's potential</b> for a small instance.",
   "<b>Verify that an improving move decreases it by the agent's "
   "gain.</b>",
   "<b>Run best-response dynamics</b> and plot the potential.",
   "<b>Compare the potential to the social cost</b> along that "
   "path.",
   "<b>Construct Braess's paradox</b> and verify both equilibria.",
   "<b>Compute the marginal cost toll</b> for Pigou's example and "
   "check it restores optimality.",
   "<b>Implement Stackelberg routing</b> for a fraction of the "
   "traffic.",
   "<b>Analyse a retry storm</b> as an externality problem.",
 ],
 "selfcheck": [
   "Define a congestion game and give the key property.",
   "Name four computing systems with this structure.",
   "Give Rosenthal's potential and what it guarantees.",
   "Why does a selfish improvement decrease it?",
   "Why is the potential not the social cost?",
   "State the externality, and what it explains.",
   "Construct Braess's paradox and give both costs.",
   "Why is nobody irrational in it?",
   "Name five interventions and what each requires.",
   "Why are backoff and rate limiting externality pricing?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Mechanism Design",
 "subtitle": "Choosing the rules so that honesty is optimal.",
 "question": "Can you always make truth-telling the best strategy?",
 "outcomes": [
     "State the mechanism design problem.",
     "Define incentive compatibility and individual rationality.",
     "Derive the VCG mechanism and explain its payments.",
     "State the revelation principle and what it simplifies.",
     "State the impossibility results that bound the field.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "Which is algorithm design with an extra constraint."},

  {"t": "callout", "title": "Choose an allocation rule and a payment rule so that reporting truthfully is optimal for every agent",
   "kind": "The design problem, stated",
   "body": ["<b>Agents have private types</b> — valuations, costs, "
            "preferences — <b>and report something</b>; <b>the "
            "mechanism maps reports to an outcome and to "
            "payments.</b>",
            "<b>Incentive compatibility:</b> <b>reporting the true "
            "type is optimal</b> — <b>in dominant strategies if "
            "possible</b>, which requires nothing about the other "
            "agents (Module 02 §2).",
            "<b>Individual rationality:</b> <b>participating is at "
            "least as good as not</b> — <b>otherwise agents leave and "
            "the mechanism is irrelevant.</b>",
            "<b>And then the objective:</b> <b>efficiency "
            "(maximise total value), revenue, or fairness</b> — "
            "<b>and the payments are the instrument that buys the "
            "incentive property.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The revelation principle",
   "blurb": "Which makes the search space manageable."},

  {"t": "callout", "title": "Anything implementable by any mechanism is implementable by a truthful direct one",
   "kind": "Why only truthful mechanisms need to be studied",
   "body": ["<b>Given any mechanism and the agents' equilibrium "
            "strategies, build a new mechanism that asks for types and "
            "then plays those strategies on the agents' "
            "behalf</b> — <b>same outcome, and now honesty is "
            "optimal.</b>",
            "<b>So the search can be restricted to truthful direct "
            "mechanisms without loss</b> — <b>which is an enormous "
            "simplification</b> and is why the field is "
            "tractable.",
            "<b>And it means an impossibility proved for truthful "
            "mechanisms holds for all of them</b> — <b>which is what "
            "gives Part 4's results their "
            "force.</b>",
            "<b>But note the practical "
            "caveat:</b> <b>the constructed mechanism requires the "
            "designer to know the equilibrium strategies</b>, and in "
            "practice indirect mechanisms (ascending auctions) are "
            "easier for people to use."]},

  {"t": "section", "label": "Part 3", "title": "VCG",
   "blurb": "The general truthful mechanism, and what it charges."},

  {"t": "eq", "kicker": "VCG", "title": "The construction, which is one idea",
   "eqs": [
     ("allocate to maximise total reported value",
      "The efficient allocation, computed as if the reports were "
      "true."),
     ("charge agent i the externality it imposes on the others",
      "payment = (best total value for everyone else without i) "
      "− (their value in the chosen allocation with i)"),
     ("so i's net utility = (total value with i) − (total value "
      "without i)",
      "Which i maximises exactly by reporting truthfully, since "
      "truthful reports make the mechanism maximise the first term. "
      "That is the proof."),
   ],
   "caption": "<b>Each agent pays the externality it imposes</b> "
              "— which is Module 05 §2's fix, arriving as a "
              "general mechanism.",
   "note": "VCG is the externality idea, generalised."},

  {"t": "bullets", "kicker": "VCG", "title": "What it gives, and what it costs",
   "items": [
     "<b>Truthful in dominant strategies</b>, and <b>efficient</b> "
     "— which is a great deal to get at once, and is why it is the "
     "field's central construction.",
     "",
     "<b>But it requires computing the optimal "
     "allocation</b> — <b>n + 1 times</b> — <b>which is "
     "NP-hard in combinatorial settings</b> "
     "(Module 08 §1).",
     "",
     "<b>And approximating the allocation breaks "
     "truthfulness</b> — <b>the proof uses exact optimality</b>, "
     "which is the central tension of "
     "Module 08.",
     "",
     "<b>Plus it is vulnerable to collusion and to false-name "
     "bidding</b>, and <b>its revenue can be zero or "
     "very low</b> in plausible cases.",
     "",
     "<b>Which is why it is used less than its theoretical "
     "standing suggests</b> — a useful corrective.",
   ],
   "footnote": "<b>Approximating the allocation breaks "
               "truthfulness</b>, because the proof uses exact "
               "optimality — which is the central tension of "
               "Module 08."},

  {"t": "section", "label": "Part 4", "title": "The limits",
   "blurb": "Which are theorems, and bound the whole field."},

  {"t": "callout", "title": "Myerson-Satterthwaite: no mechanism for bilateral trade is efficient, truthful, individually rational, and budget balanced",
   "kind": "Closing",
   "body": ["<b>A buyer and a seller with private values</b> — "
            "<b>you cannot have all four properties at once</b>, and "
            "the proof is constructive about why: <b>the payments "
            "needed for truthfulness do not balance.</b>",
            "<b>So every real trading mechanism gives one of them "
            "up</b> — <b>an outside subsidy, some inefficiency, or "
            "some manipulability</b> — and <b>knowing which is how to "
            "evaluate one.</b>",
            "<b>And Gibbard-Satterthwaite is the ordinal analogue</b> "
            "(Module 10 §3): <b>without money, truthfulness forces "
            "dictatorship</b>, which is why money matters so much "
            "here.",
            "<b>Which is the field's "
            "shape:</b> <b>with money, a lot is possible and VCG is "
            "the general answer; without it, very little "
            "is</b> — and Modules 09 and 11 work within "
            "that."]},
 ],
 "takeaways": [
   "Incentive compatibility in dominant strategies requires nothing about "
   "the other agents, which is why it is the target.",
   "The revelation principle restricts the search to truthful direct "
   "mechanisms without loss.",
   "An impossibility proved for truthful mechanisms therefore holds for all "
   "mechanisms.",
   "VCG allocates efficiently and charges each agent the externality it "
   "imposes — the externality idea, generalised.",
   "Approximating the allocation breaks truthfulness, because the proof "
   "uses exact optimality.",
   "Every real trading mechanism gives up one of efficiency, truthfulness, "
   "participation, or budget balance.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The problem"),
  ("callout", "Choose an allocation rule and a payment rule so that reporting "
              "truthfully is optimal for every agent",
   ["<b>Agents have private types</b> — valuations, costs, "
    "preferences, capacities — <b>and report something to the "
    "mechanism</b>; <b>the mechanism maps the reports to an outcome and "
    "to a payment for each agent</b>. Those two rules are the whole "
    "design.",
    "<b>Incentive compatibility:</b> <b>reporting the true type is "
    "optimal for each agent</b> — <b>in dominant strategies if "
    "possible</b>, <b>which requires nothing at all about what the "
    "other agents do</b> (Module 02 &sect;2), and in Bayes-Nash "
    "equilibrium if not, which requires a lot more.",
    "<b>Individual rationality:</b> <b>participating must be at "
    "least as good as not participating</b> — <b>otherwise agents "
    "simply leave and the mechanism is irrelevant</b> however elegant "
    "its properties are.",
    "<b>And then the designer's objective:</b> <b>efficiency "
    "(maximise total value), revenue, or some fairness criterion</b> "
    "— <b>and the payments are the instrument that buys the "
    "incentive property</b>, which is why mechanisms without money "
    "(Modules 09 and 11) are so much more constrained."]),

  ("h1", "2 &nbsp; The revelation principle"),
  ("callout", "Anything implementable by any mechanism is implementable by a "
              "truthful direct one",
   ["<b>Given any mechanism and the agents' equilibrium strategies in "
    "it, construct a new mechanism that asks each agent for its type and "
    "then plays that agent's equilibrium strategy on its "
    "behalf</b> — <b>the outcome is identical, and now reporting "
    "honestly is optimal</b>, because the simulation does the "
    "strategising.",
    "<b>So the search for mechanisms can be restricted to truthful "
    "direct mechanisms without any loss of generality</b> — "
    "<b>which is an enormous simplification</b> <b>and is a large part "
    "of why the field is tractable at all</b>: the space of all possible "
    "rule systems is unmanageable, and this cuts it to a space with "
    "structure.",
    "<b>And it means that an impossibility proved for truthful "
    "mechanisms holds for all mechanisms</b> — <b>which is exactly "
    "what gives &sect;4's results their force</b>, and is why they are "
    "stated about truthful mechanisms without that being a "
    "restriction.",
    "<b>But note the practical caveat:</b> <b>the constructed "
    "mechanism requires the designer to know the agents' equilibrium "
    "strategies</b> in order to simulate them — and <b>in practice "
    "indirect mechanisms, such as ascending auctions, are considerably "
    "easier for real people to participate in</b> than a direct "
    "revelation of a full valuation function (Module 08 "
    "&sect;4)."]),

  ("break",),
  ("h1", "3 &nbsp; VCG"),
  ("eq", "payment<sub>i</sub> = (best total value for the others "
         "without i) &minus; (the others' value in the chosen allocation "
         "with i)"),
  ("ul", ["<b>Allocate so as to maximise the total reported "
          "value</b> — the efficient allocation, computed as though "
          "the reports were true.",
          "<b>And charge each agent the externality it imposes on "
          "everybody else</b>: the difference between how well the "
          "others would have done without this agent and how well they "
          "do in the chosen allocation — <b>which is Module 05 "
          "&sect;2's marginal cost fix, arriving as a fully general "
          "mechanism.</b>",
          "<b>So agent i's net utility equals the total value with i "
          "minus the total value without i</b> — and <b>the second "
          "term does not depend on i's report at all</b>, so i "
          "maximises its utility exactly by making the mechanism "
          "maximise the first term, <b>which truthful reporting does. "
          "That is the entire proof</b>, and it is worth reconstructing "
          "once.",
          "<b>VCG is the externality idea, generalised</b> — "
          "and recognising it as the same idea as marginal cost pricing "
          "makes both easier to remember and to apply."]),
  ("ul", ["<b>Truthful in dominant strategies, and efficient</b> "
          "— <b>which is a great deal to obtain simultaneously</b>, "
          "and is why VCG is the field's central construction and the "
          "benchmark everything else is compared against.",
          "<b>But it requires computing the optimal "
          "allocation</b> — <b>n + 1 times, once overall and once "
          "with each agent removed</b> — <b>which is NP-hard in "
          "combinatorial settings</b> (Module 08 &sect;1) and is "
          "therefore frequently not available.",
          "<b>And approximating the allocation breaks "
          "truthfulness</b> — <b>the proof above uses exact "
          "optimality in an essential way</b> — <b>which is the "
          "central tension of Module 08</b> and one of the most "
          "productive problems in the field.",
          "<b>Plus it is vulnerable to collusion and to false-name "
          "bidding</b> (one agent bidding under several identities), "
          "<b>and its revenue can be zero or very low</b> in plausible "
          "cases, which matters enormously to anybody actually running "
          "an auction.",
          "<b>Which is why VCG is used much less often than its "
          "theoretical standing would suggest</b> — <b>a useful "
          "corrective</b>, and a good instance of a theoretically "
          "dominant solution losing to practical considerations "
          "(Module 13 &sect;2)."]),

  ("h1", "4 &nbsp; The limits"),
  ("callout", "Myerson-Satterthwaite: no mechanism for bilateral trade is "
              "efficient, truthful, individually rational, and budget "
              "balanced",
   ["<b>One buyer and one seller, each with a private value for the "
    "good</b> — <b>you cannot have all four properties at "
    "once</b>, and <b>the proof is constructive about why</b>: <b>the "
    "payments required to make both sides truthful do not balance</b>, "
    "so somebody must subsidise the trade.",
    "<b>So every real trading mechanism gives one of them up</b> "
    "— <b>an outside subsidy (a platform fee structure that runs a "
    "deficit on some trades), some inefficiency (trades that should "
    "happen and do not), or some manipulability</b> — and "
    "<b>knowing which one is exactly how to evaluate a real "
    "mechanism.</b>",
    "<b>And Gibbard-Satterthwaite is the ordinal analogue</b> "
    "(Module 10 &sect;3): <b>without money, truthfulness over a "
    "sufficiently rich preference domain forces dictatorship</b> "
    "— <b>which is why money matters so much in this field</b>, and "
    "is not a moral claim but a structural one.",
    "<b>Which is the field's shape in one sentence:</b> <b>with "
    "money, a great deal is possible and VCG is the general answer; "
    "without money, very little is</b> — <b>and Modules 09 and "
    "11 work within that constraint</b> rather than escaping it."]),
 ],
 "resources": [
   ("Nisan et al., chapters 9 and 11 (free PDF)",
    "https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf",
    "<b>&sect;&sect;1 to 3</b> — mechanism design and VCG, with the "
    "computational constraints treated seriously."),
   ("Vickrey, Clarke, and Groves &mdash; the three original papers",
    "https://www.jstor.org/stable/2977633",
    "<b>&sect;3</b> — and it is worth seeing how differently the "
    "three authors arrived at the same construction."),
   ("Myerson & Satterthwaite &mdash; Efficient mechanisms for "
    "bilateral trading",
    "https://www.sciencedirect.com/science/article/pii/0022053183900148",
    "<b>&sect;4</b> — the impossibility, in the original."),
   ("Roughgarden &mdash; Twenty Lectures, lectures 2 to 7 (free)",
    "http://timroughgarden.org/notes.html",
    "<b>The whole module</b> — and the development of VCG from "
    "single-item auctions is the clearest route to it."),
 ],
 "exercises": [
   "<b>State the four components</b> of a mechanism design "
   "problem.",
   "<b>Give an example</b> where individual rationality binds.",
   "<b>Prove the revelation principle</b> in your own words.",
   "<b>Explain why it strengthens impossibility results.</b>",
   "<b>Compute VCG payments</b> for a three-agent, two-item "
   "example.",
   "<b>Verify truthfulness</b> by checking one agent's misreports.",
   "<b>Construct a VCG instance with zero revenue.</b>",
   "<b>Show that false-name bidding profits</b> in some VCG "
   "instance.",
   "<b>State Myerson-Satterthwaite</b> and identify which property "
   "three real marketplaces give up.",
   "<b>Explain why money matters</b>, using the two impossibility "
   "results.",
 ],
 "selfcheck": [
   "State the mechanism design problem's four components.",
   "Define incentive compatibility, and say which form is "
   "preferable.",
   "Why does individual rationality matter?",
   "State the revelation principle and what it buys.",
   "Why does it strengthen impossibilities?",
   "Give VCG's allocation and payment rules.",
   "Sketch the truthfulness proof.",
   "Name four costs of VCG.",
   "State Myerson-Satterthwaite and its four properties.",
   "What is the field's shape, with and without money?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Single-Item Auctions",
 "subtitle": "Where the theory is sharpest, and most deployed.",
 "question": "Why does the second-highest bid set the price?",
 "outcomes": [
     "Analyse the four standard auction formats.",
     "Prove the second-price auction is truthful.",
     "State and explain revenue equivalence.",
     "Explain reserve prices and revenue maximisation.",
     "Explain why the theory's predictions sometimes fail.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The formats",
   "blurb": "Four of them, and two pairs that coincide."},

  {"t": "table", "kicker": "Formats", "title": "The standard auctions and their strategies",
   "header": ["Format", "Rule", "Optimal strategy"],
   "widths": [2.7, 4.0, 4.3],
   "rows": [
     ["<b>First price, sealed</b>", "<b>Highest bid wins, pays its bid</b>", "<b>Shade below your value</b>"],
     ["<b>Second price, sealed</b>", "<b>Highest wins, pays second bid</b>", "<b>Bid your value. Dominant</b>"],
     ["<b>Dutch (descending)</b>", "<b>Price falls until someone accepts</b>", "<b>Strategically same as first price</b>"],
     ["<b>English (ascending)</b>", "<b>Price rises until one bidder left</b>", "<b>Stay in up to your value</b>"],
   ],
   "footnote": "<b>Dutch is strategically identical to first "
               "price</b>, and <b>English to second price</b> in the "
               "private value setting — which is why there are two "
               "ideas rather than four.",
   "note": "Two formats, two strategies, and the pairing is the "
           "first result."},

  {"t": "callout", "title": "In a second-price auction, bidding your true value is a dominant strategy",
   "kind": "The proof, which is two cases and worth doing",
   "body": ["<b>Your bid determines only whether you win, never what "
            "you pay</b> — <b>the price is set by somebody "
            "else</b>, which is the whole "
            "mechanism.",
            "<b>So consider bidding above your value:</b> <b>it only "
            "changes the outcome when you win at a price above your "
            "value</b>, which is a loss — and otherwise changes "
            "nothing.",
            "<b>And bidding below:</b> <b>it only changes the "
            "outcome when you lose an auction you would have won "
            "profitably</b> — also a loss, and otherwise "
            "nothing.",
            "<b>So truthful bidding weakly dominates every "
            "alternative</b> — <b>requiring no assumption about the "
            "other bidders at all</b>, which is why this is the model "
            "mechanism (Module 06 §3's VCG with one "
            "item)."]},

  {"t": "section", "label": "Part 2", "title": "Revenue equivalence",
   "blurb": "A surprising theorem with precise conditions."},

  {"t": "callout", "title": "Under its conditions, all four formats give the seller the same expected revenue",
   "kind": "The result, and the conditions that carry it",
   "body": ["<b>Any two mechanisms that allocate to the same bidder "
            "and give a zero-value bidder zero expected utility yield "
            "the same expected revenue</b> — which is "
            "remarkable.",
            "<b>So the format does not matter for "
            "revenue</b> — <b>under independent private values, "
            "risk-neutral bidders, symmetric distributions, and no "
            "budget constraints.</b>",
            "<b>And every one of those conditions fails "
            "somewhere</b>: <b>correlated values favour the English "
            "auction, risk aversion favours first price, and budget "
            "constraints change everything.</b>",
            "<b>Which is why real auction design is about the "
            "conditions rather than the formats</b> — <b>and why "
            "quoting revenue equivalence without them is the "
            "characteristic error</b> here."]},

  {"t": "section", "label": "Part 3", "title": "Reserve prices",
   "blurb": "Where revenue and efficiency come apart."},

  {"t": "code", "kicker": "Revenue", "title": "Maximising revenue is not maximising efficiency",
   "lang": "text", "code": """
  THE EFFICIENT AUCTION
      always sell, to the highest bidder.
      Maximises total value.

  THE REVENUE-MAXIMISING AUCTION
      set a reserve price, and do NOT sell below it.
      Sometimes the item goes unsold even though a
      bidder values it above the seller's cost --
      which is INEFFICIENT ON PURPOSE.

  WHY IT RAISES REVENUE
      the reserve extracts more from the cases where
      you do sell, at the cost of the cases where
      you do not. With one bidder it is the whole
      mechanism.

  MYERSON'S RESULT
      the optimal auction allocates by VIRTUAL
      value, not value -- a transformation of the
      bid by the distribution it is drawn from.
      Which means the optimal auction DEPENDS ON THE
      DISTRIBUTION, and a seller who does not know
      it cannot run it.
""",
   "caption": "<b>The optimal auction depends on the value "
              "distribution</b>, so a seller who does not know it cannot "
              "run it — which is why simple near-optimal auctions "
              "matter.",
   "note": "Efficiency and revenue are different objectives, and "
           "the reserve price is where they visibly "
           "diverge."},

  {"t": "section", "label": "Part 4", "title": "When it fails",
   "blurb": "Which it does, and for reasons worth knowing."},

  {"t": "bullets", "kicker": "Reality", "title": "Why bidders do not always behave as the theory says",
   "items": [
     "<b>Bidders shade in second-price auctions anyway</b> — "
     "<b>because they do not believe the rule, or do not understand "
     "it</b>, which is measured in laboratory and field "
     "settings.",
     "",
     "<b>Repeated interaction changes everything</b> — "
     "<b>today's bid reveals information that affects tomorrow's "
     "price</b>, which a single-shot analysis omits "
     "entirely.",
     "",
     "<b>Collusion is profitable and happens</b> — "
     "<b>and second-price auctions are particularly vulnerable</b>, "
     "since a ring need only suppress one "
     "bid.",
     "",
     "<b>Common values create the winner's curse</b> — "
     "<b>winning means you were the most optimistic</b>, so bidding "
     "your estimate loses money.",
     "",
     "<b>And budget constraints break the model</b>, which is why "
     "deployed ad auctions depart substantially from the textbook "
     "versions.",
   ],
   "footnote": "<b>Winning means you were the most "
               "optimistic</b> — which is the winner's curse, and is "
               "a selection effect rather than a "
               "mistake."},

  {"t": "callout", "title": "So the honest summary of this module",
   "kind": "Closing",
   "body": ["<b>The single-item theory is unusually "
            "complete</b> — <b>truthfulness, revenue equivalence, and "
            "the optimal auction are all settled</b>, which is rare in "
            "any field.",
            "<b>And its predictions hold approximately, under "
            "conditions that are frequently violated</b> — <b>which "
            "is the normal situation for an applied "
            "theory.</b>",
            "<b>So the practical skill is knowing which condition is "
            "binding</b>: <b>correlated values, risk aversion, budgets, "
            "repetition, or collusion</b> — <b>five candidates, and "
            "usually one of them explains the "
            "deviation.</b>",
            "<b>Which is this module's version of the "
            "rule:</b> <b>name the auction, name the value model, and "
            "name the condition you are assuming</b> — because <b>'the "
            "second-price auction is truthful' is a theorem with "
            "hypotheses.</b>"]},
 ],
 "takeaways": [
   "Dutch is strategically identical to first price and English to second "
   "price, so there are two ideas rather than four.",
   "Your bid determines only whether you win, never what you pay — "
   "which is the whole second-price mechanism.",
   "Revenue equivalence holds under independent private values, risk "
   "neutrality, symmetry, and no budgets, and each of those fails "
   "somewhere.",
   "The revenue-maximising auction is inefficient on purpose, via a reserve "
   "price.",
   "The optimal auction depends on the value distribution, so a seller who "
   "does not know it cannot run it.",
   "Winning a common-value auction means you were the most optimistic, "
   "which is a selection effect rather than a mistake.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The formats"),
  ("table", ["Format", "The rule", "The optimal strategy"],
   [["<b>First price, sealed bid</b>",
     "<b>Highest bid wins and pays its own bid.</b>",
     "<b>Shade below your true value</b> — by how much depends on "
     "your beliefs about the others, which makes it strategically "
     "demanding."],
    ["<b>Second price, sealed bid (Vickrey)</b>",
     "<b>Highest bid wins and pays the second-highest bid.</b>",
     "<b>Bid your value. Dominant strategy</b> — see the "
     "callout."],
    ["<b>Dutch (descending clock)</b>",
     "<b>The price falls until somebody accepts.</b>",
     "<b>Strategically identical to first price</b> — accepting at "
     "price p is the same decision as bidding p."],
    ["<b>English (ascending)</b>",
     "<b>The price rises until one bidder remains.</b>",
     "<b>Stay in until the price reaches your value</b> — which "
     "gives the second-price outcome."]],
   [0.24, 0.34, 0.42]),
  ("p", "<b>Dutch is strategically identical to first price</b>, and "
        "<b>English to second price</b>, <b>in the independent private "
        "value setting</b> — <b>which is why there are two ideas "
        "here rather than four</b>. <b>Two formats, two strategies, and "
        "the pairing is the first result</b> of auction theory; it also "
        "breaks when values are correlated (&sect;4), which is "
        "informative about where the equivalence comes from."),
  ("callout", "In a second-price auction, bidding your true value is a "
              "dominant strategy",
   ["<b>Your bid determines only whether you win, and never what you "
    "pay</b> — <b>the price is set entirely by somebody "
    "else</b> — <b>which is the whole mechanism</b>, and the rest "
    "is two cases.",
    "<b>Consider bidding above your value:</b> <b>it changes the "
    "outcome only in the cases where you now win at a price above your "
    "value</b>, which is a loss, <b>and otherwise changes nothing at "
    "all.</b>",
    "<b>And bidding below your value:</b> <b>it changes the outcome "
    "only in the cases where you now lose an auction you would have won "
    "profitably</b> — <b>also a loss, and otherwise "
    "nothing.</b>",
    "<b>So truthful bidding weakly dominates every "
    "alternative</b> — <b>requiring no assumption whatsoever about "
    "the other bidders</b>, their numbers, or their values — "
    "<b>which is why this is the model mechanism of the entire "
    "field</b> and is exactly Module 06 &sect;3's VCG specialised to "
    "one item."]),

  ("h1", "2 &nbsp; Revenue equivalence"),
  ("callout", "Under its conditions, all four formats give the seller the "
              "same expected revenue",
   ["<b>Any two mechanisms that allocate the item to the same bidder "
    "(as a function of values) and give a bidder with the lowest "
    "possible value zero expected utility yield the same expected "
    "revenue</b> — which is a genuinely remarkable theorem, since "
    "the formats look so different.",
    "<b>So the choice of format does not matter for "
    "revenue</b> — <b>under independent private values, "
    "risk-neutral bidders, symmetric value distributions, and no budget "
    "constraints</b>, which is the list of hypotheses and is the part "
    "that matters.",
    "<b>And every one of those conditions fails "
    "somewhere</b>: <b>correlated values favour the English auction "
    "(the linkage principle), risk aversion favours first price, "
    "asymmetry breaks the symmetry assumption, and budget constraints "
    "change everything</b> including who can win at all.",
    "<b>Which is why real auction design is about the conditions "
    "rather than about the formats</b> — and <b>why quoting "
    "revenue equivalence without its hypotheses is the characteristic "
    "error in this area</b>, exactly as dropping the latency function "
    "class is in Module 04 &sect;2."]),

  ("break",),
  ("h1", "3 &nbsp; Reserve prices"),
  ("code", """THE EFFICIENT AUCTION
    always sell, to the highest bidder.
    Maximises total value.

THE REVENUE-MAXIMISING AUCTION
    set a reserve price, and do NOT sell below it.
    Sometimes the item goes unsold even though a
    bidder values it above the seller's cost --
    which is INEFFICIENT ON PURPOSE.

WHY IT RAISES REVENUE
    the reserve extracts more from the cases where
    you do sell, at the cost of the cases where you
    do not. With a single bidder it is the whole
    mechanism: the reserve is the only thing
    standing between the seller and a price of zero.

MYERSON'S RESULT
    the optimal auction allocates by VIRTUAL value
    rather than value -- a transformation of the bid
    by the distribution it is drawn from.
    Which means the optimal auction DEPENDS ON THE
    DISTRIBUTION, and a seller who does not know it
    cannot run it."""),
  ("p", "<b>The optimal auction depends on the value "
        "distribution</b>, <b>so a seller who does not know that "
        "distribution cannot run it</b> — <b>which is why simple "
        "near-optimal auctions matter</b> and is a substantial research "
        "area (a second-price auction with a well-chosen reserve gets "
        "most of the way, which is a satisfying result). <b>Efficiency "
        "and revenue are different objectives, and the reserve price is "
        "where they visibly diverge</b> — which is worth knowing "
        "before assuming an auction designer wants efficiency."),

  ("h1", "4 &nbsp; When it fails"),
  ("ul", ["<b>Bidders shade their bids in second-price auctions "
          "anyway</b> — <b>because they do not believe the rule, or "
          "do not understand it, or suspect the seller of shill "
          "bidding</b> — <b>which is measured in both laboratory "
          "and field settings</b> and is a real limitation on "
          "'provably truthful'.",
          "<b>Repeated interaction changes everything</b> — "
          "<b>today's bid reveals information that affects tomorrow's "
          "price and tomorrow's competitors</b> — <b>which a "
          "single-shot analysis omits entirely</b>, and which explains "
          "much of the shading above.",
          "<b>Collusion is profitable and does happen</b> — "
          "<b>and second-price auctions are particularly "
          "vulnerable</b>, since <b>a bidding ring need only suppress "
          "one competing bid to lower the price</b>, with no need to "
          "coordinate on anything else.",
          "<b>Common values create the winner's curse</b>: when all "
          "bidders are estimating the same unknown value, <b>winning "
          "means you were the most optimistic estimator</b>, <b>so "
          "bidding your estimate loses money on average</b>. <b>This is "
          "a selection effect rather than a mistake</b>, and the "
          "correction is to bid below your estimate by an amount growing "
          "with the number of bidders.",
          "<b>And budget constraints break the model</b> in ways that "
          "cannot be patched, <b>which is why deployed advertising "
          "auctions depart substantially from the textbook "
          "versions</b> (CSCE 670's sponsored search material is the "
          "applied side of this)."]),
  ("callout", "So the honest summary of this module",
   ["<b>The single-item theory is unusually complete</b> — "
    "<b>truthfulness, revenue equivalence, and the revenue-optimal "
    "auction are all settled results</b> — <b>which is rare in any "
    "applied field</b> and is why this is where the subject is taught "
    "from.",
    "<b>And its predictions hold approximately, under conditions "
    "that are frequently violated in practice</b> — <b>which is "
    "the normal situation for an applied theory</b> and is not a "
    "criticism of it, provided the conditions are stated.",
    "<b>So the practical skill is knowing which condition is binding "
    "in your case</b>: <b>correlated values, risk aversion, budget "
    "constraints, repetition, or collusion</b> — <b>five "
    "candidates, and usually exactly one of them explains the observed "
    "deviation</b>, which makes it a tractable diagnosis.",
    "<b>Which is this module's version of the program's rule:</b> "
    "<b>name the auction, name the value model, and name the condition "
    "you are assuming</b> — because <b>'the second-price auction "
    "is truthful' is a theorem with hypotheses</b>, and the hypotheses "
    "are where the engineering is."]),
 ],
 "resources": [
   ("Vickrey &mdash; Counterspeculation, auctions, and competitive "
    "sealed tenders",
    "https://www.jstor.org/stable/2977633",
    "<b>&sect;1</b> — the second-price auction in the original, and "
    "the argument is the one in the callout."),
   ("Myerson &mdash; Optimal auction design",
    "https://pubsonline.informs.org/doi/10.1287/moor.6.1.58",
    "<b>&sect;3</b> — virtual values and the revenue-optimal auction. "
    "Library copy."),
   ("Krishna &mdash; Auction Theory",
    "https://www.elsevier.com/books/auction-theory/krishna/978-0-12-374507-1",
    "<b>&sect;&sect;2 and 4</b> — revenue equivalence derived "
    "properly, with every condition made explicit. Library "
    "copy."),
   ("Kagel & Levin &mdash; the experimental auction literature",
    "https://press.princeton.edu/books/paperback/9780691016672/common-value-auctions-and-the-winners-curse",
    "<b>&sect;4</b> — what bidders actually do, measured, including "
    "the winner's curse in the field. Library copy."),
 ],
 "exercises": [
   "<b>Describe all four formats</b> and their optimal strategies.",
   "<b>Show that Dutch and first price are strategically "
   "identical.</b>",
   "<b>Prove second-price truthfulness</b>, both cases, in your own "
   "words.",
   "<b>Simulate all four</b> with the same value draws and compare "
   "revenue.",
   "<b>Violate one revenue equivalence condition</b> and watch the "
   "equivalence break.",
   "<b>Compute the optimal reserve</b> for a uniform value "
   "distribution.",
   "<b>Show that a reserve price is sometimes inefficient.</b>",
   "<b>Simulate a common-value auction</b> and measure the winner's "
   "curse.",
   "<b>Simulate a two-bidder ring</b> in a second-price auction.",
   "<b>Find a deployed auction</b> and identify which condition it "
   "violates.",
 ],
 "selfcheck": [
   "Name the four formats and their strategies.",
   "Which pairs coincide, and under what assumption?",
   "Prove second-price truthfulness.",
   "Why does the bid not affect the price?",
   "State revenue equivalence and its four conditions.",
   "Give a case where each condition fails.",
   "Why is the revenue-maximising auction inefficient?",
   "What does Myerson's optimal auction depend on, and why does that "
   "matter?",
   "Give five reasons the theory's predictions fail.",
   "Explain the winner's curse as a selection effect.",
 ],
},

]
