# -*- coding: utf-8 -*-
"""CSCE 717 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Combinatorial Auctions",
 "subtitle": "Where computation and incentives pull against each "
             "other.",
 "question": "What happens when approximating the allocation destroys "
             "truthfulness?",
 "outcomes": [
     "Explain why bundles make the problem hard.",
     "State the winner determination problem and its complexity.",
     "Explain the tension between approximation and truthfulness.",
     "Explain restricted valuation classes and what they buy.",
     "Explain why practical designs use indirect mechanisms.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Complements and substitutes",
   "blurb": "Why selling items separately is not enough."},

  {"t": "callout", "title": "A bidder's value for a bundle need not be the sum of its parts, which is what makes this a separate subject",
   "kind": "The source of the difficulty",
   "body": ["<b>Complements: a pair of adjacent spectrum licences, "
            "or a departure and a return flight</b> — <b>worth far "
            "more together than separately</b>, so winning one alone "
            "can be worthless or harmful.",
            "<b>Substitutes: two interchangeable time "
            "slots</b> — <b>worth much less together than "
            "separately</b>, so winning both is wasted "
            "money.",
            "<b>Which means separate auctions expose bidders to "
            "exposure risk</b>: <b>bid aggressively for a complement "
            "and you may win only half of what you "
            "needed.</b>",
            "<b>So bundles have to be expressible</b>, and <b>a "
            "valuation over m items is a function on 2 to the m "
            "bundles</b> — <b>which cannot even be written down</b>, "
            "and is Part 3's problem before it is "
            "Part 2's."]},

  {"t": "section", "label": "Part 2", "title": "Winner determination",
   "blurb": "Which is NP-hard, and that is the easy difficulty."},

  {"t": "callout", "title": "Finding the value-maximising allocation is NP-hard, and VCG needs it solved exactly",
   "kind": "The tension this module is about",
   "body": ["<b>Winner determination is a set packing "
            "problem</b> — <b>NP-hard, and hard to approximate in "
            "general</b> (CSCE 629 §12, CSCE 637 "
            "§11).",
            "<b>And VCG requires the exact optimum, n + 1 "
            "times</b> (Module 06 §3) — <b>so VCG is unavailable at "
            "any realistic scale.</b>",
            "<b>But swapping in an approximation algorithm breaks "
            "the truthfulness proof</b> — <b>which used exact "
            "optimality essentially</b> — and the resulting mechanism "
            "is manipulable.",
            "<b>So the field's central question "
            "became:</b> <b>which approximation algorithms can be made "
            "truthful, and at what loss in approximation "
            "ratio?</b> — which is a genuinely new kind of "
            "algorithmic question."]},

  {"t": "section", "label": "Part 3", "title": "What can be done",
   "blurb": "Three routes, each giving something up."},

  {"t": "code", "kicker": "Approaches", "title": "The three ways out, and their costs",
   "lang": "text", "code": """
  1  RESTRICT THE VALUATIONS
         single-minded bidders (one bundle each),
         gross substitutes, submodular valuations.
         Under these, truthful approximations exist
         and are sometimes optimal.
         COST: the restriction may not hold.

  2  ACCEPT A WEAKER INCENTIVE PROPERTY
         truthful in expectation, or truthful under
         a Bayesian model, or approximately truthful
         COST: the guarantee now assumes something
         about beliefs (Module 02 section 2)

  3  USE AN INDIRECT MECHANISM
         ascending auctions, where bidders respond
         to prices rather than reporting a whole
         valuation function
         COST: no clean truthfulness theorem, and
         strategic behaviour is possible
         GAIN: bidders only reveal what the prices
         require, which is the real reason they are
         used (section 4)

  AND THE SPECTRUM AUCTIONS USE ROUTE 3.
""",
   "caption": "<b>The deployed spectrum auctions use indirect "
              "ascending mechanisms</b>, not VCG — which is the "
              "field's most instructive practical "
              "fact."},

  {"t": "section", "label": "Part 4", "title": "Why indirect wins in practice",
   "blurb": "For a reason the theory does not emphasise."},

  {"t": "bullets", "kicker": "Practice", "title": "What an ascending auction gives that a direct one does not",
   "items": [
     "<b>Bidders never state a full valuation "
     "function</b> — <b>which they could not compute and would "
     "not want to disclose</b> — they only respond to the prices "
     "they actually face.",
     "",
     "<b>Which addresses the preference elicitation "
     "problem</b>: <b>determining a bidder's own value for a bundle "
     "may itself be expensive</b>, and prices "
     "tell them which bundles to bother "
     "evaluating.",
     "",
     "<b>And it reveals less</b> — <b>commercially "
     "sensitive valuations stay private</b> except as the prices force "
     "them out, which bidders care about a great "
     "deal.",
     "",
     "<b>Plus it is comprehensible</b> — <b>participants "
     "understand an ascending price</b>, and a mechanism nobody "
     "understands is not truthful in practice "
     "(Module 07 §4).",
     "",
     "<b>At the cost of no clean theorem</b>, which is a trade "
     "the designers made deliberately.",
   ],
   "footnote": "<b>Determining your own value for a bundle may "
               "itself be expensive</b> — which is the preference "
               "elicitation problem, and the direct-revelation framing "
               "assumes it away."},

  {"t": "callout", "title": "And the lesson generalises past auctions",
   "kind": "Closing",
   "body": ["<b>The theoretically dominant mechanism lost to "
            "practical considerations the model omitted</b> — "
            "<b>computability, elicitation cost, privacy, and "
            "comprehensibility</b> — all four of which are "
            "real.",
            "<b>Which is not a failure of the "
            "theory</b>: <b>the theory identified the benchmark, and "
            "the practical designs are evaluated against "
            "it.</b>",
            "<b>And it is the shape of this whole "
            "semester</b> — <b>the model comes from outside, and the "
            "parts the model omits are where the engineering "
            "is</b> (CSCE 640 §13 §3, CSCE 628 §13 §4).",
            "<b>So when you design one:</b> <b>state the "
            "benchmark, state what you gave up, and state why</b> — "
            "which is Module 13 §3's form and Project 2's "
            "requirement."]},
 ],
 "takeaways": [
   "A valuation over m items is a function on 2 to the m bundles, which "
   "cannot even be written down.",
   "Separate auctions expose bidders to exposure risk when items are "
   "complements.",
   "VCG requires the exact optimum n + 1 times, and winner determination is "
   "NP-hard.",
   "Swapping in an approximation breaks the truthfulness proof, which used "
   "exact optimality essentially.",
   "Determining your own value for a bundle may itself be expensive, which "
   "direct revelation assumes away.",
   "The deployed spectrum auctions use indirect ascending mechanisms rather "
   "than VCG.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Complements and substitutes"),
  ("callout", "A bidder's value for a bundle need not be the sum of its "
              "parts, which is what makes this a separate subject",
   ["<b>Complements: a pair of adjacent spectrum licences, or an "
    "outbound and a return flight</b> — <b>worth far more together "
    "than separately</b>, <b>so winning one of them alone can be "
    "worthless or actively harmful</b>, since you paid for something "
    "unusable.",
    "<b>Substitutes: two interchangeable delivery slots, or two "
    "equivalent servers</b> — <b>worth much less together than the "
    "sum of their individual values</b>, so winning both is money "
    "wasted.",
    "<b>Which means running separate auctions exposes bidders to "
    "exposure risk</b>: <b>bid aggressively for a complement and you "
    "may end up winning only half of what you needed</b>, which makes "
    "rational bidders bid timidly and makes the outcome "
    "inefficient.",
    "<b>So bundles have to be expressible</b>, and <b>a general "
    "valuation over m items is a function on 2<sup>m</sup> "
    "bundles</b> — <b>which cannot even be written down</b> for "
    "any realistic m — and <b>that is &sect;4's elicitation "
    "problem arriving before &sect;2's computational one</b>, and is "
    "arguably the more fundamental of the two."]),

  ("h1", "2 &nbsp; Winner determination"),
  ("callout", "Finding the value-maximising allocation is NP-hard, and VCG "
              "needs it solved exactly",
   ["<b>Winner determination is essentially a weighted set packing "
    "problem</b> — <b>NP-hard, and hard to approximate within any "
    "reasonable factor in the general case</b> (CSCE 629 "
    "Module 12's reductions, CSCE 637 Module 11's inapproximability "
    "results).",
    "<b>And VCG requires the exact optimum, computed n + 1 "
    "times</b> — once overall and once with each agent removed "
    "(Module 06 &sect;3) — <b>so VCG is simply unavailable at "
    "any realistic scale</b>, which is a computational objection to an "
    "economic result and is what algorithmic game theory was founded to "
    "notice.",
    "<b>But swapping in an approximation algorithm breaks the "
    "truthfulness proof</b> — <b>which used exact optimality in an "
    "essential way</b> (the agent's utility equalled the total welfare "
    "up to a constant only because the allocation was optimal) — "
    "<b>and the resulting mechanism is manipulable</b>, sometimes "
    "severely.",
    "<b>So the field's central question became:</b> <b>which "
    "approximation algorithms can be made truthful, and at what loss in "
    "the approximation ratio?</b> — <b>which is a genuinely new "
    "kind of algorithmic question</b>, and one that has produced "
    "techniques (monotone allocation rules, critical-value payments) "
    "with no classical counterpart."]),

  ("break",),
  ("h1", "3 &nbsp; What can be done"),
  ("code", """1  RESTRICT THE VALUATIONS
       single-minded bidders (each wants exactly one
       bundle), gross substitutes, submodular
       valuations.
       Under these restrictions, truthful
       approximations exist and are sometimes
       essentially optimal.
       COST: the restriction may not hold, and
       checking whether it does may be hard.

2  ACCEPT A WEAKER INCENTIVE PROPERTY
       truthful in expectation, or truthful under a
       Bayesian model, or approximately truthful
       COST: the guarantee now assumes something
       about beliefs (Module 02 section 2), which
       is exactly what dominant strategies avoided

3  USE AN INDIRECT MECHANISM
       ascending auctions, in which bidders respond
       to posted prices rather than reporting a
       whole valuation function
       COST: no clean truthfulness theorem, and
       strategic behaviour is possible
       GAIN: bidders reveal only what the prices
       require, which is the real reason they are
       used (section 4)

AND THE DEPLOYED SPECTRUM AUCTIONS USE ROUTE 3."""),
  ("p", "<b>The deployed spectrum auctions use indirect ascending "
        "mechanisms, not VCG</b> — <b>which is the field's most "
        "instructive practical fact</b>, given that those auctions were "
        "designed by people who knew the theory extremely well and had "
        "every reason to use the optimal mechanism if it had been usable. "
        "The reasons are &sect;4's, and they are not "
        "computational."),

  ("h1", "4 &nbsp; Why indirect wins in practice"),
  ("ul", ["<b>Bidders never have to state a full valuation "
          "function</b> — <b>which they could not compute and "
          "would not want to disclose</b> — <b>they respond only to "
          "the prices they actually face</b>, which is a vastly smaller "
          "demand.",
          "<b>Which addresses the preference elicitation "
          "problem</b>: <b>determining a bidder's own value for a "
          "particular bundle may itself be expensive</b> — "
          "requiring engineering studies, market analysis, or "
          "negotiation — <b>and prices tell them which bundles are "
          "worth the trouble of evaluating.</b>",
          "<b>And it reveals less</b> — <b>commercially "
          "sensitive valuations stay private except insofar as the "
          "prices force them out</b> — <b>which bidders care about "
          "a great deal</b>, and which a direct revelation mechanism "
          "ignores entirely.",
          "<b>Plus it is comprehensible</b> — <b>participants "
          "understand an ascending price</b> — and <b>a mechanism "
          "nobody understands is not truthful in practice</b>, whatever "
          "the theorem says (Module 07 &sect;4's shading, and "
          "Module 13 &sect;1).",
          "<b>At the cost of having no clean truthfulness "
          "theorem</b>, <b>which is a trade the designers made "
          "deliberately and defended in writing</b>. <b>Determining "
          "your own value for a bundle may itself be expensive</b> "
          "— <b>which is the preference elicitation problem, and "
          "the direct-revelation framing assumes it away</b> "
          "entirely."]),
  ("callout", "And the lesson generalises past auctions",
   ["<b>The theoretically dominant mechanism lost to practical "
    "considerations that the model omitted</b> — "
    "<b>computability, elicitation cost, privacy, and "
    "comprehensibility</b> — <b>all four of which are real and "
    "none of which appears in the VCG theorem.</b>",
    "<b>Which is not a failure of the theory</b>: <b>the theory "
    "identified the benchmark, and the practical designs are evaluated "
    "against it</b> — you cannot say how much a design gives up "
    "without knowing what the optimum was.",
    "<b>And it is the shape of this whole semester</b> — "
    "<b>the model comes from outside, and the parts the model omits are "
    "where the engineering lives</b> (CSCE 640 Module 13 &sect;3's "
    "baselines, CSCE 628 Module 13 &sect;4's external model).",
    "<b>So when you design one:</b> <b>state the benchmark, state "
    "what you gave up, and state why</b> — <b>which is "
    "Module 13 &sect;3's claim form and Project 2's "
    "requirement.</b>"]),
 ],
 "resources": [
   ("Cramton, Shoham & Steinberg &mdash; Combinatorial Auctions (free "
    "chapters)",
    "https://www.cramton.umd.edu/papers/combinatorial-auctions/",
    "<b>The whole module</b> — the standard collection, with "
    "chapters on each of &sect;3's routes."),
   ("Lehmann, O'Callaghan & Shoham &mdash; Truth revelation in "
    "approximately efficient combinatorial auctions (free)",
    "https://dl.acm.org/doi/10.1145/585265.585266",
    "<b>&sect;&sect;2 and 3</b> — the single-minded case, and the "
    "monotonicity technique that makes approximation truthful."),
   ("Nisan et al., chapters 11 and 12 (free PDF)",
    "https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf",
    "<b>&sect;&sect;2 and 3</b> — computationally efficient "
    "mechanisms, with the tension developed carefully."),
   ("Milgrom &mdash; Putting Auction Theory to Work",
    "https://www.cambridge.org/9780521536721",
    "<b>&sect;4</b> — by a designer of the spectrum auctions, on why "
    "the practical choices were made. Library copy."),
 ],
 "exercises": [
   "<b>Construct a complements example</b> and compute the exposure "
   "risk.",
   "<b>Construct a substitutes example.</b>",
   "<b>Count the numbers needed</b> to express a general valuation "
   "over 20 items.",
   "<b>Reduce set packing to winner determination</b>, or the other "
   "way.",
   "<b>Implement VCG</b> for a small combinatorial instance and time "
   "it as m grows.",
   "<b>Replace the exact solver with a greedy one</b> and find a "
   "profitable misreport.",
   "<b>Implement the single-minded truthful approximation</b> and "
   "verify monotonicity.",
   "<b>Run an ascending auction</b> on the same instance and compare "
   "the outcome.",
   "<b>Estimate the elicitation cost</b> for a real bundle valuation "
   "you can imagine.",
   "<b>Name the four practical considerations</b> and find a system "
   "where each binds.",
 ],
 "selfcheck": [
   "Define complements and substitutes, with an example of each.",
   "What is exposure risk?",
   "How large is a general valuation function?",
   "What is winner determination, and how hard is it?",
   "Why does approximation break VCG's truthfulness?",
   "State the field's central question.",
   "Give the three routes out, with their costs.",
   "Which route do the spectrum auctions use?",
   "Give four reasons indirect mechanisms win in practice.",
   "State the general lesson.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Matching",
 "subtitle": "Allocation without money, and the one place this theory "
             "is routinely deployed.",
 "question": "How do you allocate when you cannot charge?",
 "outcomes": [
     "State the stable matching problem and Gale-Shapley.",
     "Explain which side the algorithm favours and why.",
     "Explain strategy-proofness for one side only.",
     "Explain school choice and kidney exchange.",
     "State what a matching mechanism guarantees.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Stable matching",
   "blurb": "The problem, and the algorithm that solves it."},

  {"t": "callout", "title": "A matching is stable if no pair would both rather have each other than their assigned partners",
   "kind": "The definition, and why stability is the right goal",
   "body": ["<b>A blocking pair is two agents who each prefer the "
            "other to their current assignment</b> — <b>and if one "
            "exists they will simply arrange it privately</b>, which "
            "destroys the matching.",
            "<b>So stability is not an aesthetic criterion</b> "
            "— <b>it is the condition under which the matching "
            "survives contact with the participants</b>, which is why "
            "unstable mechanisms have historically "
            "unravelled.",
            "<b>And Gale-Shapley produces one</b>: <b>each "
            "unmatched agent on the proposing side proposes to its most "
            "preferred acceptable partner not yet rejected; the "
            "receiving side holds the best offer and rejects the "
            "rest.</b>",
            "<b>Which terminates in O(n²) and always yields a stable "
            "matching</b> — <b>so a stable matching always "
            "exists</b>, which was not obvious and is the "
            "theorem."]},

  {"t": "section", "label": "Part 2", "title": "Who it favours",
   "blurb": "Which is not symmetric, and matters practically."},

  {"t": "callout", "title": "The proposing side gets its best stable partner and the receiving side its worst",
   "kind": "A result with direct policy consequences",
   "body": ["<b>Among all stable matchings, deferred acceptance "
            "gives every proposer the best partner it has in any of "
            "them</b> — <b>and every receiver the worst</b>, "
            "simultaneously.",
            "<b>So the side that proposes matters</b>, and <b>it is "
            "a policy choice rather than an implementation "
            "detail</b> — which is how the medical residency match was "
            "reformed.",
            "<b>And truthful reporting is a dominant strategy for "
            "the proposing side</b> — <b>and not for the receiving "
            "side</b>, which can sometimes gain by truncating its "
            "list.",
            "<b>Which is a specific and useful "
            "asymmetry</b>: <b>'strategy-proof' here means "
            "strategy-proof for one side</b>, and saying which is part "
            "of describing the mechanism honestly "
            "(Module 13 §1)."]},

  {"t": "section", "label": "Part 3", "title": "Deployments",
   "blurb": "Where this is actually used, and what it took."},

  {"t": "code", "kicker": "Deployed", "title": "Three real systems, and the complication in each",
   "lang": "text", "code": """
  MEDICAL RESIDENCY MATCHING
      the original large deployment. Complication:
      couples wanting positions in the same city,
      which makes a stable matching possibly
      NONEXISTENT and the problem NP-hard.
      Handled in practice by a heuristic.

  SCHOOL CHOICE
      students to schools. Complication: schools
      are objects, not agents with preferences, so
      "stability" means respecting priorities.
      The older Boston mechanism rewarded strategic
      ranking heavily; deferred acceptance replaced
      it, explicitly so families need not game it.

  KIDNEY EXCHANGE
      incompatible donor-patient pairs swapped in
      cycles and chains. No money, by law.
      Complication: cycles must be short (all
      surgeries simultaneous), which makes the
      optimisation NP-hard, and the altruistic-donor
      chains relax it.

  IN ALL THREE THE THEORY GOT DEPLOYED, which is
  rare, and in all three it needed real engineering.
""",
   "caption": "<b>In all three the theory was deployed and needed "
              "real engineering</b> — which makes matching the "
              "field's best evidence that any of this "
              "works.",
   "note": "School choice is the clearest case of a mechanism "
           "changed to remove the incentive to "
           "game."},

  {"t": "section", "label": "Part 4", "title": "What it guarantees",
   "blurb": "And the standard misreading."},

  {"t": "bullets", "kicker": "The claim", "title": "What a stable matching is and is not",
   "items": [
     "<b>It is stable</b> — <b>no pair can profitably deviate "
     "together</b> — which is what makes it survive.",
     "",
     "<b>It is not optimal in any aggregate sense</b> — "
     "<b>stability is a constraint, not an objective</b>, and the "
     "stable matchings can differ a great deal in total "
     "welfare.",
     "",
     "<b>It is not fair</b> — <b>the proposing side does "
     "systematically better</b> (Part 2), by "
     "construction.",
     "",
     "<b>And it is only as good as the reported "
     "preferences</b> — <b>which are truthful for one side and "
     "not necessarily the other</b>, and which people may not know "
     "accurately in the first place.",
     "",
     "<b>Plus the preferences themselves are shaped by the "
     "mechanism</b>: <b>people rank differently when they believe "
     "ranking matters</b>, which is the effect the reforms "
     "removed.",
   ],
   "footnote": "<b>Stability is a constraint, not an "
               "objective</b> — so a stable matching is not "
               "optimising anything, and saying it is is the standard "
               "misreading."},

  {"t": "callout", "title": "And this is the field's best evidence",
   "kind": "Closing",
   "body": ["<b>Matching is where mechanism design is routinely "
            "deployed and demonstrably improved outcomes</b> — "
            "<b>residency matching, school choice, and kidney "
            "exchange</b>, all operating at scale.",
            "<b>And in each case the deployment required handling "
            "something the clean theory excluded</b> — <b>couples, "
            "priorities, cycle length limits</b> — which is the "
            "engineering (Module 08 §4's "
            "pattern).",
            "<b>Which is the right note on which to assess this "
            "subject</b>: <b>the theory is not merely elegant, and it "
            "is also not sufficient on its own.</b>",
            "<b>So when claiming a matching mechanism works:</b> "
            "<b>name the side it favours, the side it is strategy-proof "
            "for, and the complication you handled "
            "heuristically</b> — three things, and "
            "Module 13 wants all three."]},
 ],
 "takeaways": [
   "A blocking pair will simply arrange things privately, which is why "
   "stability is the condition for a matching to survive.",
   "Deferred acceptance gives the proposing side its best stable partner "
   "and the receiving side its worst.",
   "Truthfulness is a dominant strategy for the proposing side only, so "
   "'strategy-proof' here needs a side named.",
   "In residency matching, school choice, and kidney exchange the theory "
   "was deployed and needed real engineering.",
   "Stability is a constraint, not an objective, so a stable matching is "
   "not optimising anything.",
   "Preferences are shaped by the mechanism: people rank differently when "
   "they believe ranking matters.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Stable matching"),
  ("callout", "A matching is stable if no pair would both rather have each "
              "other than their assigned partners",
   ["<b>A blocking pair is two agents who each strictly prefer the "
    "other to their current assignment</b> — <b>and if such a pair "
    "exists they will simply arrange it privately</b>, outside the "
    "mechanism, <b>which destroys the matching</b> and the mechanism's "
    "authority with it.",
    "<b>So stability is not an aesthetic criterion</b> — "
    "<b>it is precisely the condition under which the matching survives "
    "contact with the participants</b> — <b>which is why unstable "
    "mechanisms have historically unravelled</b>, with participants "
    "matching earlier and earlier outside the process until it "
    "collapsed.",
    "<b>And Gale-Shapley (deferred acceptance) produces "
    "one</b>: <b>each unmatched agent on the proposing side proposes to "
    "its most preferred acceptable partner that has not yet rejected it; "
    "each agent on the receiving side holds its best offer so far and "
    "rejects the others</b>, repeating until nobody is "
    "proposing.",
    "<b>It terminates in O(n<sup>2</sup>) and always produces a "
    "stable matching</b> — <b>so a stable matching always "
    "exists</b>, <b>which was not obvious and is the theorem</b>: an "
    "existence proof that is also an algorithm, which is the opposite "
    "situation from Module 03."]),

  ("h1", "2 &nbsp; Who it favours"),
  ("callout", "The proposing side gets its best stable partner and the "
              "receiving side its worst",
   ["<b>Among all stable matchings, deferred acceptance gives every "
    "agent on the proposing side the best partner it has in any stable "
    "matching</b> — <b>and every agent on the receiving side its "
    "worst</b> — <b>simultaneously</b>, which is a strong and "
    "somewhat surprising result.",
    "<b>So which side proposes matters a great deal</b>, and <b>it "
    "is a policy choice rather than an implementation detail</b> "
    "— <b>which is exactly how the medical residency match was "
    "reformed</b> when it was changed to be applicant-proposing.",
    "<b>And truthful reporting is a dominant strategy for the "
    "proposing side</b> — <b>and is not for the receiving "
    "side</b>, which can sometimes benefit by truncating its preference "
    "list to make itself appear more selective.",
    "<b>Which is a specific and useful asymmetry</b>: "
    "<b>'strategy-proof' here means strategy-proof for one side</b>, "
    "<b>and saying which side is part of describing the mechanism "
    "honestly</b> (Module 13 &sect;1's requirement). A paper or "
    "system that says only 'strategy-proof' has omitted half the "
    "claim."]),

  ("break",),
  ("h1", "3 &nbsp; Deployments"),
  ("code", """MEDICAL RESIDENCY MATCHING
    the original large-scale deployment.
    Complication: couples wanting positions in the
    same city, which makes a stable matching
    possibly NONEXISTENT and the problem NP-hard.
    Handled in practice by a well-tested heuristic.

SCHOOL CHOICE
    students to schools. Complication: schools are
    objects with priorities, not agents with
    preferences, so "stability" means respecting
    those priorities rather than mutual preference.
    The older Boston mechanism rewarded strategic
    ranking heavily -- families who ranked their
    true first choice could lose their second --
    and deferred acceptance replaced it explicitly
    so that families would not need to game it.

KIDNEY EXCHANGE
    incompatible donor-patient pairs swapped in
    cycles and chains. No money, by law.
    Complication: cycles must be short because all
    surgeries in a cycle happen simultaneously,
    which makes the optimisation NP-hard; chains
    started by altruistic donors relax the
    simultaneity requirement.

IN ALL THREE THE THEORY GOT DEPLOYED, which is rare,
and in all three it needed real engineering."""),
  ("p", "<b>In all three the theory was deployed and needed real "
        "engineering</b> — <b>which makes matching the field's best "
        "evidence that any of this works</b>, and the best available "
        "answer to somebody who regards mechanism design as an elegant "
        "irrelevance. <b>School choice is the clearest case of a "
        "mechanism changed specifically to remove the incentive to "
        "game</b>: the reform's stated goal was that families should be "
        "able to report their true preferences safely, which is "
        "Module 01 &sect;1's whole argument, enacted."),

  ("h1", "4 &nbsp; What it guarantees"),
  ("ul", ["<b>It is stable</b> — <b>no pair can profitably "
          "deviate together</b> — which is what makes it survive, "
          "and is the property the whole construction is for.",
          "<b>It is not optimal in any aggregate sense</b> — "
          "<b>stability is a constraint, not an objective</b>, <b>and "
          "the set of stable matchings can differ a great deal in total "
          "welfare</b>. Nothing in the algorithm is maximising anything "
          "global.",
          "<b>It is not fair</b> — <b>the proposing side does "
          "systematically better</b> (&sect;2), <b>by construction and "
          "not by accident</b> — which is why the choice of "
          "proposing side is a distributive decision.",
          "<b>And it is only as good as the reported "
          "preferences</b> — <b>which are truthful for one side "
          "and not necessarily for the other</b>, <b>and which people "
          "may not know accurately about themselves</b> in the first "
          "place (Module 01 &sect;4's agent model).",
          "<b>Plus the preferences themselves are shaped by the "
          "mechanism</b>: <b>people rank differently when they believe "
          "the ranking matters strategically</b> — <b>which is "
          "precisely the effect the school choice reforms removed</b>, "
          "and which means comparing pre- and post-reform preference "
          "data is not comparing like with like. <b>Stability is a "
          "constraint, not an objective</b>, and saying otherwise is the "
          "standard misreading."]),
  ("callout", "And this is the field's best evidence",
   ["<b>Matching is where mechanism design is routinely deployed and "
    "has demonstrably improved outcomes</b> — <b>residency "
    "matching, school choice, and kidney exchange</b>, all operating at "
    "national scale and all with measurable results.",
    "<b>And in each case the deployment required handling something "
    "the clean theory excluded</b> — <b>couples, school "
    "priorities, cycle length limits</b> — <b>which is the "
    "engineering</b> (Module 08 &sect;4's pattern, in a second "
    "setting).",
    "<b>Which is the right note on which to assess this "
    "subject</b>: <b>the theory is not merely elegant, and it is also "
    "not sufficient on its own</b> — both halves, and the second "
    "half is why the deployments took decades.",
    "<b>So when claiming a matching mechanism works:</b> <b>name "
    "the side it favours, the side it is strategy-proof for, and the "
    "complication you handled heuristically</b> — <b>three things, "
    "and Module 13 wants all three.</b>"]),
 ],
 "resources": [
   ("Gale & Shapley &mdash; College admissions and the stability of "
    "marriage (free)",
    "https://www.jstor.org/stable/2312726",
    "<b>&sect;1 in the original</b> — nine pages, and entirely "
    "readable."),
   ("Roth &mdash; Who Gets What and Why",
    "https://www.hmhbooks.com/shop/books/who-gets-what-and-why/9780544705289",
    "<b>&sect;3</b> — the deployments described by the person who "
    "built several of them, including the failures. Library "
    "copy."),
   ("Abdulkadiroglu & Sönmez &mdash; School choice: a mechanism "
    "design approach (free)",
    "https://www.aeaweb.org/articles?id=10.1257/000282803322157061",
    "<b>&sect;3's second case</b> — the Boston mechanism's problem, "
    "and the reform argument."),
   ("Nisan et al., chapter 10 (free PDF)",
    "https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf",
    "<b>&sect;&sect;1, 2, and 4</b> — the computational treatment, "
    "including the NP-hard variants."),
 ],
 "exercises": [
   "<b>Define stability</b> and give a blocking pair in a small "
   "instance.",
   "<b>Run Gale-Shapley by hand</b> on a four-by-four instance.",
   "<b>Run it with the other side proposing</b> and compare the "
   "outcomes.",
   "<b>Enumerate all stable matchings</b> of a small instance and "
   "verify the extremal result.",
   "<b>Find a profitable truncation</b> for a receiving-side "
   "agent.",
   "<b>Implement deferred acceptance</b> and test it at scale.",
   "<b>Add couples</b> and find an instance with no stable "
   "matching.",
   "<b>Simulate the Boston mechanism</b> and find a family that is "
   "punished for honesty.",
   "<b>Implement kidney exchange</b> with a cycle length cap, and "
   "measure what the cap costs.",
   "<b>Write the three-part claim</b> for a matching mechanism you "
   "design.",
 ],
 "selfcheck": [
   "Define stability and a blocking pair.",
   "Why is stability the right criterion rather than an aesthetic "
   "one?",
   "Describe Gale-Shapley and state what it guarantees.",
   "Which side does it favour, and how strongly?",
   "For which side is it strategy-proof?",
   "Name three deployments and the complication in each.",
   "What did the school choice reform set out to remove?",
   "Give four things a stable matching does not guarantee.",
   "What is the standard misreading?",
   "What three things should a matching claim name?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Voting and Social Choice",
 "subtitle": "The impossibility results, and what they actually "
             "forbid.",
 "question": "Is there a fair voting rule?",
 "outcomes": [
     "Describe the standard voting rules and their behaviour.",
     "State Arrow's theorem precisely.",
     "State Gibbard-Satterthwaite and what follows.",
     "Explain the computational escape and its limits.",
     "Evaluate a voting rule honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The rules",
   "blurb": "And the fact that they disagree."},

  {"t": "table", "kicker": "Rules", "title": "Standard voting rules and their characteristic failure",
   "header": ["Rule", "How it works", "Its characteristic problem"],
   "widths": [2.5, 3.9, 4.6],
   "rows": [
     ["<b>Plurality</b>", "<b>Most first-place votes wins</b>", "<b>Vote splitting; ignores all other information</b>"],
     ["<b>Borda count</b>", "<b>Points by rank position</b>", "<b>Highly manipulable; clones distort it</b>"],
     ["<b>Condorcet methods</b>", "<b>Beat every other in pairwise</b>", "<b>A winner may not exist (cycles)</b>"],
     ["<b>Instant runoff</b>", "<b>Eliminate last, redistribute</b>", "<b>Non-monotone: more support can hurt</b>"],
     ["<b>Approval</b>", "<b>Approve any subset; most wins</b>", "<b>Where the approval threshold goes is strategic</b>"],
   ],
   "footnote": "<b>The same ballots can elect different winners "
               "under different rules</b> — which is the fact that "
               "makes rule choice a substantive decision rather than a "
               "formality.",
   "note": "Instant runoff's non-monotonicity surprises people and "
           "is real."},

  {"t": "callout", "title": "And a Condorcet cycle shows the difficulty is in the preferences, not the rule",
   "kind": "The example to internalise",
   "body": ["<b>Three voters, three options: A>B>C, B>C>A, "
            "C>A>B</b> — <b>A beats B two to one, B beats C two to "
            "one, and C beats A two to one.</b>",
            "<b>So the collective preference is cyclic even though "
            "every individual's is transitive</b> — <b>which no voting "
            "rule can fix</b>, because there is nothing coherent to "
            "report.",
            "<b>Which means the impossibility results are not about "
            "clumsy rules</b> — <b>they are about what aggregation can "
            "do</b>, and that is why they are "
            "theorems.",
            "<b>And it takes three voters and three options to "
            "construct</b> — <b>so this is not a corner case</b>, it "
            "is the generic situation whenever preferences are "
            "genuinely diverse."]},

  {"t": "section", "label": "Part 2", "title": "Arrow",
   "blurb": "What exactly is impossible."},

  {"t": "eq", "kicker": "Arrow 1951", "title": "The theorem, with its conditions",
   "eqs": [
     ("No rule aggregating 3+ options satisfies all of:",
      "The theorem is about ranking rules — producing a full "
      "social ordering from individual orderings."),
     ("unanimity, independence of irrelevant alternatives,",
      "If everyone prefers A to B then society does; and the social "
      "ranking of A and B depends only on individuals' rankings of A "
      "and B."),
     ("and non-dictatorship — except a dictatorship.",
      "So one of the three must go. Independence is the one usually "
      "given up, and giving it up is exactly what admits "
      "manipulation."),
   ],
   "caption": "<b>Independence of irrelevant alternatives is the "
              "condition usually given up</b> — and giving it up is "
              "precisely what admits "
              "manipulation.",
   "note": "Which condition a rule abandons is the useful way to "
           "classify it."},

  {"t": "section", "label": "Part 3", "title": "Gibbard-Satterthwaite",
   "blurb": "The version that matters for mechanism design."},

  {"t": "callout", "title": "Any non-dictatorial voting rule over three or more outcomes is manipulable",
   "kind": "The result that bounds Module 06 without money",
   "body": ["<b>If the rule can elect any of at least three outcomes "
            "and is not a dictatorship, then some voter sometimes "
            "benefits from misreporting</b> — which is a theorem, not "
            "an observation.",
            "<b>So there is no strategy-proof voting rule</b> "
            "— <b>and 'this rule is strategy-proof' is therefore "
            "false or the rule is restricted in one of the stated "
            "ways.</b>",
            "<b>Which is exactly Module 06 §4's "
            "limit without money</b>: <b>payments are what makes VCG "
            "possible, and voting has none</b>, so the ordinal setting "
            "is much more constrained.",
            "<b>And the escape routes are "
            "narrow:</b> <b>restrict the preference domain (single "
            "peaked preferences admit the median rule), use money, or "
            "accept manipulability and manage it</b> — which is what "
            "every real system does."]},

  {"t": "section", "label": "Part 4", "title": "The computational escape",
   "blurb": "Which is real and is weaker than it first looked."},

  {"t": "bullets", "kicker": "Complexity", "title": "Can hardness of manipulation substitute for impossibility?",
   "items": [
     "<b>The idea: if finding a profitable misreport is NP-hard, "
     "manipulation is impractical</b> — <b>which was the field's "
     "most attractive proposal</b> and is why computational social "
     "choice exists.",
     "",
     "<b>And manipulation is NP-hard for some rules</b>, "
     "including some in use — which is a genuine "
     "result.",
     "",
     "<b>But NP-hardness is worst case</b> "
     "(CSCE 637 §03) — <b>and typical instances are "
     "frequently easy</b>, with heuristics succeeding most of "
     "the time.",
     "",
     "<b>Which is the standard critique and it "
     "holds</b>: <b>average-case hardness is what would be needed, and "
     "it is much harder to establish.</b>",
     "",
     "<b>So the escape is partial</b> — <b>a real obstacle "
     "and not a guarantee</b>, which is the honest summary.",
   ],
   "footnote": "<b>NP-hardness of manipulation is worst case, and "
               "typical instances are frequently easy</b> — which is "
               "the standard critique and it "
               "holds."},

  {"t": "callout", "title": "So how to evaluate a voting rule",
   "kind": "Closing",
   "body": ["<b>Which Arrow condition does it give up?</b> — "
            "<b>almost always independence</b>, and that tells you where "
            "it is manipulable.",
            "<b>What is its characteristic "
            "manipulation?</b> — <b>every rule has one, and it should "
            "be stated</b> rather than discovered by "
            "participants.",
            "<b>Does it satisfy monotonicity, and does it elect a "
            "Condorcet winner when one exists?</b> — two properties "
            "people assume and several rules "
            "lack.",
            "<b>And what does it do with a cycle?</b> "
            "(Part 1) — <b>because something has to, and "
            "the answer is a design decision rather than a "
            "detail.</b>"]},
 ],
 "takeaways": [
   "The same ballots can elect different winners under different rules, "
   "which makes rule choice substantive.",
   "A Condorcet cycle needs three voters and three options, so cyclic "
   "collective preference is generic rather than a corner case.",
   "Arrow: unanimity, independence, and non-dictatorship cannot hold "
   "together for three or more options.",
   "Independence is the condition usually given up, and giving it up is "
   "precisely what admits manipulation.",
   "Gibbard-Satterthwaite: any non-dictatorial rule over three or more "
   "outcomes is manipulable.",
   "NP-hardness of manipulation is worst case, and typical instances are "
   "frequently easy.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The rules"),
  ("table", ["Rule", "How it works", "Its characteristic problem"],
   [["<b>Plurality</b>", "<b>The option with the most first-place "
     "votes wins.</b>",
     "<b>Vote splitting between similar options, and it discards all "
     "information below first place.</b>"],
    ["<b>Borda count</b>",
     "<b>Points assigned by rank position, summed.</b>",
     "<b>Highly manipulable, and adding clones of an option distorts "
     "the result.</b>"],
    ["<b>Condorcet methods</b>",
     "<b>Elect the option that beats every other in a pairwise "
     "comparison.</b>",
     "<b>Such a winner may not exist</b> — cycles, see the "
     "callout."],
    ["<b>Instant runoff / single transferable vote</b>",
     "<b>Eliminate the last-placed option and redistribute, "
     "repeat.</b>",
     "<b>Non-monotone: gaining support can cause a candidate to "
     "lose.</b> See the note."],
    ["<b>Approval voting</b>",
     "<b>Approve any subset; the most approvals wins.</b>",
     "<b>Where a voter sets the approval threshold is itself a "
     "strategic decision.</b>"]],
   [0.20, 0.34, 0.46]),
  ("p", "<b>The same set of ballots can elect different winners under "
        "different rules</b> — which is easy to demonstrate with "
        "five voters — <b>and is the fact that makes rule choice a "
        "substantive political decision rather than a formality</b>. "
        "<b>Instant runoff's non-monotonicity surprises people and is "
        "real</b>: there are constructible profiles in which a candidate "
        "loses because some voters ranked them higher, which follows from "
        "the elimination order changing."),
  ("callout", "And a Condorcet cycle shows the difficulty is in the "
              "preferences, not the rule",
   ["<b>Three voters and three options: A&gt;B&gt;C, B&gt;C&gt;A, "
    "C&gt;A&gt;B</b> — <b>A beats B two to one, B beats C two to "
    "one, and C beats A two to one</b>, in pairwise majority "
    "votes.",
    "<b>So the collective preference is cyclic even though every "
    "individual's preference is perfectly transitive</b> — <b>which "
    "no voting rule can fix</b>, <b>because there is nothing coherent "
    "for it to report</b>: the majority relation itself is not an "
    "ordering.",
    "<b>Which means the impossibility results of &sect;&sect;2 and "
    "3 are not about clumsy or badly designed rules</b> — <b>they "
    "are about what aggregation can do in principle</b> — <b>and "
    "that is why they are theorems rather than criticisms.</b>",
    "<b>And it takes only three voters and three options to "
    "construct</b> — <b>so this is not a corner case</b>, <b>it is "
    "the generic situation whenever preferences are genuinely "
    "diverse</b>, which is when voting is needed at all."]),

  ("h1", "2 &nbsp; Arrow"),
  ("eq", "No rule aggregating individual rankings over 3 or more "
         "options satisfies unanimity, independence of irrelevant "
         "alternatives, and non-dictatorship together."),
  ("ul", ["<b>The theorem is about ranking rules</b> — those "
          "producing a full social ordering from individual orderings "
          "— which is worth noting, since rules that produce only a "
          "winner are covered by &sect;3 instead.",
          "<b>Unanimity: if every individual prefers A to B, the "
          "social ranking does too</b> — which nobody wants to give "
          "up.",
          "<b>Independence of irrelevant alternatives: the social "
          "ranking of A and B depends only on the individuals' rankings "
          "of A against B</b>, and not on where C sits — which is "
          "the condition that sounds technical and is "
          "load-bearing.",
          "<b>And non-dictatorship: no single individual's ranking "
          "determines the social one regardless of everybody "
          "else's</b> — which also nobody wants to give up.",
          "<b>So one of the three must go, and independence is the "
          "one usually given up</b> — <b>and giving it up is "
          "precisely what admits manipulation</b>, because a rule whose "
          "verdict on A versus B depends on C can be moved by "
          "misreporting about C. <b>Which condition a rule abandons is "
          "the useful way to classify it</b> (&sect;4's first "
          "question)."]),

  ("break",),
  ("h1", "3 &nbsp; Gibbard-Satterthwaite"),
  ("callout", "Any non-dictatorial voting rule over three or more outcomes is "
              "manipulable",
   ["<b>If the rule can elect any of at least three outcomes and is "
    "not a dictatorship, then there exists some preference profile in "
    "which some voter benefits from misreporting</b> — <b>which is "
    "a theorem, not an observation about existing rules</b>, and it "
    "follows from Arrow.",
    "<b>So there is no strategy-proof voting rule</b> — and "
    "<b>'this voting rule is strategy-proof' is therefore either false "
    "or the rule is restricted in one of the stated ways</b> (fewer "
    "than three reachable outcomes, a restricted preference domain, or "
    "a dictator).",
    "<b>Which is exactly Module 06 &sect;4's limit in the "
    "no-money setting</b>: <b>payments are what make VCG "
    "possible</b>, and <b>voting has none</b>, so <b>the ordinal "
    "setting is substantially more constrained than the quasilinear "
    "one</b> — which is the structural reason money matters so "
    "much in mechanism design.",
    "<b>And the escape routes are narrow:</b> <b>restrict the "
    "preference domain (single-peaked preferences admit the median "
    "voter rule, which is strategy-proof), introduce money, or accept "
    "manipulability and manage it</b> — <b>which is what every "
    "real system does</b>, mostly without saying so."]),

  ("h1", "4 &nbsp; The computational escape"),
  ("ul", ["<b>The idea: if finding a profitable misreport is "
          "NP-hard, then manipulation is impractical even though it is "
          "possible</b> — <b>which was this field's most attractive "
          "proposal</b> and <b>is why computational social choice exists "
          "as a subfield.</b>",
          "<b>And manipulation is indeed NP-hard for some "
          "rules</b>, including some that are actually used, "
          "particularly with weighted voters or many candidates — "
          "<b>which is a genuine result</b> and was reasonably "
          "exciting.",
          "<b>But NP-hardness is a worst-case notion</b> "
          "(CSCE 637 Module 03's framing) — <b>and typical "
          "instances are frequently easy</b>, <b>with simple heuristics "
          "succeeding on the great majority of profiles</b> drawn from "
          "plausible distributions.",
          "<b>Which is the standard critique and it holds</b>: "
          "<b>average-case hardness is what would actually be needed, "
          "and it is very much harder to establish</b> — the same "
          "gap that limits worst-case hardness as a basis for "
          "cryptography (CSCE 711 Module 02).",
          "<b>So the computational escape is partial</b> — "
          "<b>a real obstacle and not a guarantee</b> — <b>which is "
          "the honest summary</b>, and is more useful than either the "
          "original enthusiasm or a flat dismissal."]),
  ("callout", "So how to evaluate a voting rule",
   ["<b>Which Arrow condition does it give up?</b> — <b>almost "
    "always independence</b> — <b>and that tells you where it is "
    "manipulable</b>, since the manipulation will involve misreporting "
    "about an option that is not in contention.",
    "<b>What is its characteristic manipulation?</b> — "
    "<b>every rule has one, and it should be stated in the "
    "documentation</b> <b>rather than discovered by participants</b>, "
    "which is the difference between a known limitation and a "
    "scandal.",
    "<b>Does it satisfy monotonicity, and does it elect a Condorcet "
    "winner when one exists?</b> — <b>two properties people assume "
    "and that several widely used rules lack</b> (&sect;1's "
    "table).",
    "<b>And what does it do when there is a cycle?</b> "
    "(&sect;1) — <b>because something has to be done, and the "
    "answer is a design decision rather than an implementation "
    "detail</b>: different Condorcet completion methods resolve cycles "
    "differently and defensibly."]),
 ],
 "resources": [
   ("Brandt et al. &mdash; Handbook of Computational Social Choice "
    "(free PDF)",
    "https://www.cambridge.org/core/books/handbook-of-computational-social-choice/",
    "<b>The whole module</b>, free — and the manipulation-complexity "
    "chapters cover &sect;4 including the critique."),
   ("Arrow &mdash; Social Choice and Individual Values",
    "https://yalebooks.yale.edu/book/9780300013641/social-choice-and-individual-values/",
    "<b>&sect;2</b> — the original, and the conditions are stated "
    "more carefully there than in most summaries. Library copy."),
   ("Satterthwaite &mdash; Strategy-proofness and Arrow's conditions",
    "https://www.sciencedirect.com/science/article/pii/0022053175900502",
    "<b>&sect;3</b> — and the connection to Arrow is made "
    "explicit."),
   ("Shoham & Leyton-Brown, chapter 9 (free PDF)",
    "http://www.masfoundations.org/",
    "<b>&sect;&sect;1 to 3</b>, free — the rules and the "
    "impossibilities, with worked examples."),
 ],
 "exercises": [
   "<b>Construct ballots</b> where five rules elect five different "
   "winners.",
   "<b>Construct a Condorcet cycle</b> and verify all three pairwise "
   "results.",
   "<b>Construct a non-monotone instance</b> for instant runoff.",
   "<b>State Arrow's three conditions</b> in your own words.",
   "<b>Show that plurality violates independence</b>, with an "
   "example.",
   "<b>Find the manipulation</b> for Borda, concretely.",
   "<b>State Gibbard-Satterthwaite</b> and its three escape routes.",
   "<b>Verify the median rule is strategy-proof</b> for single-peaked "
   "preferences.",
   "<b>Implement a manipulation heuristic</b> for one rule and measure "
   "its success rate.",
   "<b>Evaluate one real voting rule</b> against §4's four "
   "questions.",
 ],
 "selfcheck": [
   "Name five voting rules and each one's characteristic problem.",
   "Construct a Condorcet cycle and say what it shows.",
   "Why are the impossibilities not about clumsy rules?",
   "State Arrow's three conditions.",
   "Which is usually given up, and what does that admit?",
   "State Gibbard-Satterthwaite.",
   "How does it relate to Module 06's limit?",
   "Name the three escape routes.",
   "State the computational escape and the standard critique.",
   "Give the four questions for evaluating a rule.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Fair Division",
 "subtitle": "Dividing without money, and what fairness can mean.",
 "question": "What exactly do you mean by fair?",
 "outcomes": [
     "Define proportionality, envy-freeness, and equitability.",
     "Explain divide-and-choose and its generalisations.",
     "Explain the indivisible case and its approximations.",
     "Explain the complexity of envy-free division.",
     "Choose a fairness criterion and defend it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The criteria",
   "blurb": "Which are different, and are frequently conflated."},

  {"t": "table", "kicker": "Criteria", "title": "What fairness can mean, precisely",
   "header": ["Criterion", "Definition", "Note"],
   "widths": [2.7, 4.5, 3.8],
   "rows": [
     ["<b>Proportional</b>", "<b>Each of n agents gets at least 1/n by its own valuation</b>", "<b>The weakest useful notion</b>"],
     ["<b>Envy-free</b>", "<b>Nobody prefers another's share to their own</b>", "<b>Implies proportional</b>"],
     ["<b>Equitable</b>", "<b>Everyone's own-valuation of their share is equal</b>", "<b>Independent of envy-freeness</b>"],
     ["<b>Efficient (Pareto)</b>", "<b>No reallocation helps someone without hurting another</b>", "<b>Not a fairness notion at all</b>"],
     ["<b>Maximin share</b>", "<b>At least what you'd get cutting and choosing last</b>", "<b>The indivisible analogue (§3)</b>"],
   ],
   "footnote": "<b>These are different properties and can "
               "conflict</b> — so 'fair' is not a specification, and "
               "naming which one you mean is the first step of any such "
               "design.",
   "note": "Pareto efficiency is in the table because it is "
           "constantly mistaken for a fairness "
           "criterion."},

  {"t": "section", "label": "Part 2", "title": "The divisible case",
   "blurb": "Where good procedures exist."},

  {"t": "callout", "title": "Divide-and-choose is envy-free for two agents and needs no knowledge of the other's preferences",
   "kind": "The model protocol",
   "body": ["<b>One cuts, the other chooses</b> — <b>the cutter "
            "makes the pieces equal by its own valuation, so is content "
            "with either; the chooser takes its preferred "
            "one.</b>",
            "<b>So neither envies the other</b>, and <b>neither "
            "needed to know anything about the other's "
            "preferences</b> — which is the dominant-strategy property "
            "(Module 02 §2) in a procedural "
            "form.",
            "<b>And it generalises to n agents for "
            "proportionality</b> — <b>moving-knife and "
            "last-diminisher protocols</b> — <b>but envy-freeness for "
            "n agents is far harder</b>, and bounded protocols were "
            "found only recently.",
            "<b>Which is the shape of the divisible "
            "case:</b> <b>proportionality is easy, envy-freeness is "
            "hard, and both are possible</b> — unlike "
            "Part 3."]},

  {"t": "section", "label": "Part 3", "title": "The indivisible case",
   "blurb": "Where exact fairness is simply unavailable."},

  {"t": "code", "kicker": "Indivisible", "title": "What goes wrong, and what is settled for instead",
   "lang": "text", "code": """
  THE OBSTACLE
      one item, two agents, both want it.
      No allocation is envy-free. Not hard --
      impossible.

  SO THE NOTIONS ARE RELAXED
      EF1  envy-free up to one item: any envy
           disappears if one item is removed from
           the envied bundle. ALWAYS ACHIEVABLE,
           by a simple round-robin.
      EFX  envy-free up to ANY item: stronger, and
           existence was open for a long time.
      MMS  maximin share: what you could guarantee
           yourself by partitioning and choosing
           last. NOT always achievable, which was a
           surprise; constant approximations exist.

  AND THE COMPUTATION
      maximising welfare subject to fairness is
      typically NP-hard, so this is an approximation
      problem like Module 08's.

  PLUS: agents report valuations, so the incentive
  problem of Module 06 applies on top.
""",
   "caption": "<b>EF1 is always achievable by a simple "
              "round-robin</b> — which is a rare case of a fairness "
              "guarantee with a trivial "
              "algorithm.",
   "note": "Maximin share not always being achievable was a genuine "
           "surprise."},

  {"t": "section", "label": "Part 4", "title": "Choosing a criterion",
   "blurb": "Which is the actual design decision."},

  {"t": "bullets", "kicker": "Design", "title": "The questions, for a real allocation problem",
   "items": [
     "<b>Divisible or indivisible?</b> — <b>which determines "
     "whether exact fairness is even available</b> "
     "(Part 3).",
     "",
     "<b>Which fairness notion, and why that one?</b> — "
     "<b>and are you willing to lose efficiency for it</b>, which you "
     "frequently must.",
     "",
     "<b>Is there money?</b> — <b>side payments make almost "
     "everything easier</b> (Module 06 §4), and their absence is "
     "usually a policy constraint rather than a technical "
     "one.",
     "",
     "<b>Are the valuations additive?</b> — <b>most results "
     "assume it, and most real preferences are not</b> "
     "(Module 08 §1's complements).",
     "",
     "<b>And is the mechanism truthful?</b> — <b>most fair "
     "division procedures are not</b>, and that should be stated rather "
     "than left to be discovered.",
   ],
   "footnote": "<b>Most fair division procedures are not "
               "truthful</b> — which is rarely stated alongside "
               "their fairness guarantees and should "
               "be."},

  {"t": "callout", "title": "And 'fair' without a definition is not a specification",
   "kind": "Closing",
   "body": ["<b>The criteria in Part 1 are genuinely "
            "different and sometimes incompatible</b> — <b>so a "
            "requirement to 'allocate fairly' has not said what to "
            "build.</b>",
            "<b>Which is this module's practical "
            "contribution:</b> <b>a vocabulary precise enough to turn "
            "a value judgement into a specification</b> that can be "
            "checked.",
            "<b>And the choice among them is a value "
            "judgement</b> — <b>which the mathematics does not "
            "make</b> and should not be presented as "
            "making.",
            "<b>So state the criterion, state what it costs in "
            "efficiency, and state whether the procedure is "
            "truthful</b> — <b>three things, and Module 13 "
            "wants them.</b>"]},
 ],
 "takeaways": [
   "Proportional, envy-free, equitable, and efficient are different "
   "properties that can conflict, so 'fair' is not a specification.",
   "Pareto efficiency is not a fairness criterion, and is constantly "
   "mistaken for one.",
   "Divide-and-choose is envy-free and requires no knowledge of the other "
   "agent's preferences.",
   "With indivisible items, envy-freeness is impossible rather than hard "
   "— one item and two agents suffice.",
   "EF1 is always achievable by a simple round-robin, which is a rare "
   "trivial algorithm for a real guarantee.",
   "Most fair division procedures are not truthful, which is rarely stated "
   "alongside their fairness guarantees.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The criteria"),
  ("table", ["Criterion", "Definition", "Note"],
   [["<b>Proportional</b>",
     "<b>Each of n agents receives at least 1/n of the total by its "
     "own valuation.</b>",
     "<b>The weakest useful notion</b>, and the easiest to "
     "achieve."],
    ["<b>Envy-free</b>",
     "<b>No agent prefers another agent's share to its own.</b>",
     "<b>Implies proportionality</b>, and is strictly stronger for "
     "three or more agents."],
    ["<b>Equitable</b>",
     "<b>Every agent's own valuation of its own share is the same "
     "number.</b>",
     "<b>Independent of envy-freeness</b> — neither implies the "
     "other, which surprises people."],
    ["<b>Efficient (Pareto optimal)</b>",
     "<b>No reallocation makes someone better off without making "
     "someone worse off.</b>",
     "<b>Not a fairness notion at all</b> — giving everything to "
     "one agent is Pareto optimal. See the note."],
    ["<b>Maximin share</b>",
     "<b>At least what you could guarantee by partitioning the items "
     "yourself and choosing last.</b>",
     "<b>The natural indivisible analogue of proportionality</b> "
     "(&sect;3)."]],
   [0.20, 0.42, 0.38]),
  ("p", "<b>These are genuinely different properties and they can "
        "conflict</b> — an allocation can be equitable and envious, "
        "or envy-free and inefficient — <b>so 'fair' is not a "
        "specification, and naming which one you mean is the first step "
        "of any such design</b>. <b>Pareto efficiency is in the table "
        "because it is constantly mistaken for a fairness "
        "criterion</b>, including in engineering requirements: it "
        "constrains waste, not distribution."),

  ("h1", "2 &nbsp; The divisible case"),
  ("callout", "Divide-and-choose is envy-free for two agents and needs no "
              "knowledge of the other's preferences",
   ["<b>One agent cuts and the other chooses</b> — <b>the "
    "cutter makes the two pieces equal by its own valuation, and is "
    "therefore content with either; the chooser takes whichever it "
    "prefers</b>, and is content by construction.",
    "<b>So neither agent envies the other</b>, and crucially "
    "<b>neither needed to know anything whatsoever about the other's "
    "preferences</b> — <b>which is the dominant-strategy property "
    "(Module 02 &sect;2) appearing in a procedural rather than a "
    "direct-revelation form</b>, and is why the protocol is three "
    "thousand years old and still correct.",
    "<b>And it generalises to n agents for "
    "proportionality</b> — <b>moving-knife protocols and the "
    "last-diminisher procedure</b> both achieve it — <b>but "
    "envy-freeness for n agents is very much harder</b>, and <b>bounded "
    "protocols for it were found only recently</b>, which is a striking "
    "fact about a problem that sounds elementary.",
    "<b>Which is the shape of the divisible case:</b> "
    "<b>proportionality is easy, envy-freeness is hard, and both are "
    "achievable</b> — <b>unlike &sect;3's indivisible case</b>, "
    "where one of them is simply unavailable."]),

  ("break",),
  ("h1", "3 &nbsp; The indivisible case"),
  ("code", """THE OBSTACLE
    one item, two agents, and both want it.
    No allocation is envy-free. Not hard --
    impossible.

SO THE NOTIONS ARE RELAXED
    EF1  envy-free up to one item: any envy
         disappears if one item is removed from the
         envied bundle. ALWAYS ACHIEVABLE, by a
         simple round-robin draft.
    EFX  envy-free up to ANY item: strictly
         stronger, and its existence was open for a
         long time.
    MMS  maximin share: what you could guarantee
         yourself by partitioning the items and
         choosing last. NOT always achievable,
         which was a genuine surprise; constant
         factor approximations exist.

AND THE COMPUTATION
    maximising welfare subject to a fairness
    constraint is typically NP-hard, so this is an
    approximation problem like Module 08's.

PLUS: agents report their valuations, so the
incentive problem of Module 06 applies on top."""),
  ("p", "<b>EF1 is always achievable by a simple round-robin "
        "draft</b> — agents take turns picking their favourite "
        "remaining item — <b>which is a rare case of a real "
        "fairness guarantee with a trivial algorithm</b>, and is worth "
        "knowing because it is immediately implementable. <b>Maximin "
        "share not always being achievable was a genuine surprise</b> "
        "to the field, since the definition is constructed precisely so "
        "that the agent could guarantee it for itself — and the "
        "counterexamples are intricate, which is why it took a "
        "while."),

  ("h1", "4 &nbsp; Choosing a criterion"),
  ("ul", ["<b>Divisible or indivisible?</b> — <b>which "
          "determines whether exact fairness is even available</b> "
          "(&sect;3's obstacle), and is the first thing to "
          "establish.",
          "<b>Which fairness notion, and why that one?</b> — "
          "<b>and are you willing to lose efficiency for it</b>, "
          "<b>which you frequently must</b>: the most efficient "
          "allocation is rarely the fairest under any of &sect;1's "
          "criteria.",
          "<b>Is there money?</b> — <b>side payments make "
          "almost everything easier</b> (Module 06 &sect;4, "
          "Module 10 &sect;3) — <b>and their absence is usually "
          "a policy or legal constraint rather than a technical "
          "one</b>, which is worth confirming before designing around "
          "it.",
          "<b>Are the valuations additive?</b> — <b>most "
          "results in this module assume it, and most real preferences "
          "are not</b> (Module 08 &sect;1's complements and "
          "substitutes), so check before applying a theorem.",
          "<b>And is the mechanism truthful?</b> — <b>most fair "
          "division procedures are not</b>, including divide-and-choose "
          "in the n-agent generalisations — <b>and that should be "
          "stated rather than left for participants to "
          "discover</b>. <b>This is rarely stated alongside the "
          "fairness guarantees and should be.</b>"]),
  ("callout", "And 'fair' without a definition is not a specification",
   ["<b>The criteria in &sect;1 are genuinely different and are "
    "sometimes mutually incompatible</b> — <b>so a requirement to "
    "'allocate fairly' has not said what to build</b>, and two engineers "
    "will build different things from it.",
    "<b>Which is this module's practical contribution:</b> <b>a "
    "vocabulary precise enough to turn a value judgement into a "
    "specification that can be checked</b> — and checked "
    "automatically, in most cases.",
    "<b>And the choice among the criteria is a value "
    "judgement</b> — <b>which the mathematics does not make</b>, "
    "<b>and should not be presented as making</b>: a paper that proves "
    "its mechanism is EF1 has not shown that EF1 is what anybody "
    "wanted.",
    "<b>So state the criterion, state what it costs in efficiency, "
    "and state whether the procedure is truthful</b> — <b>three "
    "things, and Module 13 wants all of them</b> (as it does for every "
    "other module's mechanisms)."]),
 ],
 "resources": [
   ("Brams & Taylor &mdash; Fair Division",
    "https://www.cambridge.org/9780521556446",
    "<b>&sect;&sect;1 and 2</b> — the procedures, including the "
    "moving-knife constructions. Library copy."),
   ("Procaccia &mdash; Cake cutting algorithms, in the Handbook "
    "(free PDF)",
    "https://www.cambridge.org/core/books/handbook-of-computational-social-choice/",
    "<b>&sect;2</b> — the computational treatment, including the "
    "query complexity of envy-freeness."),
   ("Caragiannis et al. &mdash; The unreasonable fairness of maximum "
    "Nash welfare (free)",
    "https://dl.acm.org/doi/10.1145/2940716.2940726",
    "<b>&sect;3</b> — a rule that is simultaneously EF1 and "
    "efficient, which is a satisfying result."),
   ("Spliddit (free)",
    "http://www.spliddit.org/",
    "<b>&sect;&sect;3 and 4</b> — these algorithms as a working "
    "service, which makes the criteria concrete."),
 ],
 "exercises": [
   "<b>Define all five criteria</b> and give an allocation satisfying "
   "each but not the others.",
   "<b>Show that envy-freeness implies proportionality.</b>",
   "<b>Find an equitable allocation with envy</b>, and the "
   "converse.",
   "<b>Show that giving everything to one agent is Pareto "
   "optimal.</b>",
   "<b>Run divide-and-choose</b> and verify envy-freeness.",
   "<b>Implement a proportional n-agent protocol.</b>",
   "<b>Prove no envy-free allocation exists</b> for one item and two "
   "agents.",
   "<b>Implement the round-robin</b> and verify EF1.",
   "<b>Find a maximin share counterexample</b> in the literature and "
   "work through it.",
   "<b>Find a profitable misreport</b> in one fair division "
   "procedure.",
 ],
 "selfcheck": [
   "Define five fairness criteria.",
   "Which implies which, and which are independent?",
   "Why is Pareto efficiency not a fairness notion?",
   "Describe divide-and-choose and why it works.",
   "What does it require knowing about the other agent?",
   "What generalises to n agents, and what does not?",
   "Why is envy-freeness impossible with indivisible items?",
   "Define EF1, EFX, and MMS, and say which is always achievable.",
   "Give the five design questions.",
   "Why is 'fair' not a specification?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Learning in Games",
 "subtitle": "What adaptive agents actually reach.",
 "question": "If nobody can compute the equilibrium, what happens "
             "instead?",
 "outcomes": [
     "Explain no-regret learning and its guarantee.",
     "State what no-regret dynamics converge to.",
     "Explain why that answers Module 03's objection.",
     "Explain best-response dynamics and when they converge.",
     "Simulate learning agents against a mechanism.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "No-regret learning",
   "blurb": "A guarantee that needs no model of the opponent."},

  {"t": "callout", "title": "An algorithm has no regret if its average payoff approaches that of the best fixed action in hindsight",
   "kind": "The definition, and why it is the right one",
   "body": ["<b>Regret is the gap between what you got and what the "
            "single best fixed action would have "
            "got</b> — <b>chosen with hindsight over the whole "
            "sequence.</b>",
            "<b>And no-regret means that gap goes to zero per round "
            "as the horizon grows</b> — <b>which is achievable, by "
            "multiplicative weights and its relatives</b> "
            "(CSCE 658 §11, CSCE 669 §09).",
            "<b>Crucially it requires no assumption about the "
            "environment</b> — <b>the other players may be adversarial, "
            "adaptive, or irrational</b>, and the guarantee still "
            "holds.",
            "<b>Which makes it a far more defensible behavioural "
            "assumption than equilibrium</b>: <b>it says agents are not "
            "persistently leaving money on the table</b>, which is "
            "modest and plausible."]},

  {"t": "section", "label": "Part 2", "title": "Where it converges",
   "blurb": "To something, and the something is interesting."},

  {"t": "eq", "kicker": "Convergence", "title": "What no-regret play reaches",
   "eqs": [
     ("if all players use no-regret algorithms, the empirical "
      "distribution of play converges to the set of coarse "
      "correlated equilibria",
      "Not to Nash. A weaker and larger set — and one that is "
      "computable by linear programming, unlike Nash."),
     ("with a stronger (swap-regret) guarantee: correlated equilibria",
      "Still weaker than Nash, still computable, and still reached "
      "by simple adaptive agents."),
     ("and in zero-sum games: the time-averaged play approaches "
      "the minimax value",
      "Which recovers the Nash prediction in exactly the case where "
      "Nash is computable (Module 03 §4)."),
   ],
   "caption": "<b>Simple adaptive agents reach correlated "
              "equilibrium, which is computable</b> — while Nash, "
              "which they do not reach, is "
              "not.",
   "note": "The computable concept is the one that is actually "
           "reached. That is not a coincidence."},

  {"t": "callout", "title": "Which answers Module 03's objection rather than evading it",
   "kind": "Why this module matters for the whole course",
   "body": ["<b>Module 03 said computing Nash is "
            "intractable, so predicting it is "
            "unjustified</b> — <b>and this module says agents reach a "
            "different concept, which is tractable</b>, and reach it by "
            "simple means.",
            "<b>So the prediction is rescued by weakening "
            "it</b> — <b>which is the right move</b>, and is more "
            "honest than assuming agents solve a PPAD-complete problem "
            "overnight.",
            "<b>And Module 04 §3's smoothness bounds apply to "
            "the no-regret outcomes</b> — <b>so the price of anarchy "
            "guarantees survive</b>, which is the result that ties the "
            "course together.",
            "<b>Which means the analysis half of this course rests "
            "on learning rather than on equilibrium</b> — a "
            "reorientation worth stating plainly, and one the field made "
            "deliberately."]},

  {"t": "section", "label": "Part 3", "title": "Best response dynamics",
   "blurb": "Simpler, and with weaker guarantees."},

  {"t": "bullets", "kicker": "Dynamics", "title": "The other natural process, and when it works",
   "items": [
     "<b>Each agent in turn switches to its best response to the "
     "current profile</b> — <b>which is the obvious thing to "
     "simulate</b> and is what Project 1 uses.",
     "",
     "<b>It converges in potential games</b> "
     "(Module 05 §2) — <b>because the potential strictly "
     "decreases</b> — and that is the main "
     "positive case.",
     "",
     "<b>And it can cycle forever in general games</b> — "
     "<b>rock-paper-scissors is the two-line example</b>, and nothing "
     "stops it.",
     "",
     "<b>Plus the order of play matters</b>: <b>simultaneous "
     "updates can oscillate where sequential ones "
     "converge</b>, which is an implementation "
     "detail with real consequences.",
     "",
     "<b>So: use it where a potential function exists, and use "
     "no-regret otherwise</b> — which is a clean practical "
     "rule.",
   ],
   "footnote": "<b>Simultaneous updates can oscillate where "
               "sequential ones converge</b> — an implementation "
               "detail that changes the "
               "outcome."},

  {"t": "section", "label": "Part 4", "title": "Using it",
   "blurb": "To test a mechanism you designed."},

  {"t": "callout", "title": "Simulate learning agents against your mechanism, because honest agents will not tell you much",
   "kind": "Closing",
   "body": ["<b>A mechanism tested with agents who report truthfully "
            "tests nothing</b> — <b>truthfulness was the property you "
            "were trying to establish</b>, so assuming it begs the "
            "question.",
            "<b>So run no-regret or best-response learners against "
            "it</b>, and <b>see what they find</b> — <b>which is "
            "Project 2's requirement</b> and is the "
            "cheapest attack available.",
            "<b>And compare the outcome to the honest-agent "
            "case</b>: <b>the gap is what strategic behaviour costs "
            "your design</b>, measured rather than "
            "assumed.",
            "<b>Which is this course's version of CSCE 628 §13's "
            "negative control</b> — <b>test the system under conditions "
            "where it might fail, and report what happened</b>, "
            "whatever it was."]},
 ],
 "takeaways": [
   "No-regret requires no assumption about the environment, so the "
   "guarantee holds against adversarial or irrational opponents.",
   "It is a far more defensible behavioural assumption than equilibrium: "
   "agents are not persistently leaving money on the table.",
   "No-regret play converges to correlated equilibria, not to Nash — a "
   "weaker, larger, and computable set.",
   "The computable concept is the one that is actually reached, which is "
   "not a coincidence.",
   "The price of anarchy bounds survive, because smoothness arguments apply "
   "to no-regret outcomes.",
   "A mechanism tested with honest agents tests nothing, because "
   "truthfulness was what you were establishing.",
 ],
 "notes": [
  ("h1", "1 &nbsp; No-regret learning"),
  ("callout", "An algorithm has no regret if its average payoff approaches "
              "that of the best fixed action in hindsight",
   ["<b>Regret is the gap between the payoff you actually received "
    "and the payoff the single best fixed action would have "
    "received</b> — <b>chosen with full hindsight over the whole "
    "sequence of rounds</b>, which is a demanding benchmark and is "
    "nonetheless achievable.",
    "<b>And no-regret means that gap, divided by the number of "
    "rounds, goes to zero as the horizon grows</b> — <b>which is "
    "achieved by multiplicative weights and its many relatives</b> "
    "(CSCE 658 Module 11's randomised weighted majority, CSCE 669 "
    "Module 09's online convex optimisation — the same algorithm "
    "appearing for the third time in this program).",
    "<b>Crucially it requires no assumption whatsoever about the "
    "environment</b> — <b>the other players may be adversarial, "
    "adaptive, irrational, or not players at all</b>, <b>and the "
    "guarantee still holds</b>, which is what makes it usable as a "
    "behavioural model.",
    "<b>Which makes it a far more defensible behavioural assumption "
    "than equilibrium</b>: <b>it says only that agents are not "
    "persistently leaving money on the table</b> — <b>which is "
    "modest, plausible, and consistent with agents who do not know they "
    "are in a game at all.</b>"]),

  ("h1", "2 &nbsp; Where it converges"),
  ("ul", ["<b>If every player uses a no-regret algorithm, the "
          "empirical distribution of joint play converges to the set of "
          "coarse correlated equilibria</b> — <b>not to Nash</b> "
          "— <b>a weaker and larger set</b>, <b>and one that is "
          "computable by linear programming</b>, unlike Nash "
          "(Module 03).",
          "<b>With a stronger guarantee — no swap regret, which "
          "is also achievable — the play converges to the set of "
          "correlated equilibria</b>, which is a tighter set, <b>still "
          "weaker than Nash, still computable, and still reached by "
          "simple adaptive agents.</b>",
          "<b>And in two-player zero-sum games the time-averaged "
          "play approaches the minimax value</b> — <b>which "
          "recovers the Nash prediction in exactly the case where Nash "
          "is computable</b> (Module 03 &sect;4), and that coincidence "
          "is not a coincidence.",
          "<b>Simple adaptive agents reach correlated equilibrium, "
          "which is computable</b> — <b>while Nash, which they do "
          "not reach, is not</b>. <b>The computable concept is the one "
          "that is actually reached</b>, which is a satisfying piece of "
          "structure and a good argument for taking computational "
          "constraints seriously as modelling constraints."]),
  ("callout", "Which answers Module 03's objection rather than evading it",
   ["<b>Module 03 said that computing a Nash equilibrium is "
    "intractable, so predicting that agents play one is "
    "unjustified</b> — <b>and this module says that agents reach a "
    "different solution concept, which is tractable</b>, <b>and reach "
    "it by simple and well-understood means.</b>",
    "<b>So the prediction is rescued by weakening it</b> — "
    "<b>which is the right move</b>, <b>and is considerably more honest "
    "than assuming agents solve a PPAD-complete problem between "
    "rounds</b>.",
    "<b>And Module 04 &sect;3's smoothness bounds apply directly "
    "to the no-regret outcomes</b> — <b>so the price of anarchy "
    "guarantees survive the weakening</b> — <b>which is the result "
    "that ties this course's analysis half together</b> and is why the "
    "smoothness framework was such a significant development.",
    "<b>Which means the analysis half of this course rests on "
    "learning rather than on equilibrium</b> — <b>a reorientation "
    "worth stating plainly</b>, and one the field made deliberately in "
    "response to the complexity results rather than ignoring "
    "them."]),

  ("break",),
  ("h1", "3 &nbsp; Best response dynamics"),
  ("ul", ["<b>Each agent in turn switches to its best response "
          "against the current profile of everybody else</b> — "
          "<b>which is the obvious thing to simulate</b> and <b>is what "
          "Project 1 uses</b> to find an equilibrium of a congestion "
          "game.",
          "<b>It converges in potential games</b> (Module 05 "
          "&sect;2) — <b>because every improving move strictly "
          "decreases the potential, which is bounded</b> — and "
          "<b>that is the main positive case</b>, covering routing, load "
          "balancing, and congestion generally.",
          "<b>And it can cycle forever in general games</b> — "
          "<b>rock-paper-scissors is the two-line example</b>, with each "
          "agent endlessly best-responding to the last move — "
          "<b>and nothing in the dynamics prevents it.</b>",
          "<b>Plus the order of play matters</b>: <b>simultaneous "
          "updates can oscillate where sequential updates "
          "converge</b>, because simultaneous best responses can "
          "overshoot together — <b>an implementation detail with "
          "real consequences for a simulation's conclusions.</b>",
          "<b>So the practical rule: use best-response dynamics "
          "where a potential function exists, and no-regret "
          "otherwise</b> — <b>which is clean, and is what "
          "Project 2's simulation should follow.</b>"]),

  ("h1", "4 &nbsp; Using it"),
  ("callout", "Simulate learning agents against your mechanism, because "
              "honest agents will not tell you much",
   ["<b>A mechanism tested with agents who report truthfully tests "
    "nothing</b> — <b>truthfulness was precisely the property you "
    "were trying to establish</b>, <b>so assuming it begs the "
    "question</b>, and a simulation built that way will always "
    "succeed.",
    "<b>So run no-regret or best-response learners against it, and "
    "see what they find</b> — <b>which is Project 2's "
    "requirement</b> and <b>is the cheapest attack available on your "
    "own design</b>, requiring no cleverness about where the "
    "vulnerability might be.",
    "<b>And compare the resulting outcome to the honest-agent "
    "case</b>: <b>the gap between them is what strategic behaviour "
    "costs your design</b>, <b>measured rather than assumed</b>, and "
    "it is the number to report.",
    "<b>Which is this course's version of CSCE 628 Module 13's "
    "negative control</b> — <b>test the system under conditions "
    "where it might fail, and report what happened</b>, <b>whatever it "
    "was</b> — and it is the same argument: a test that cannot fail "
    "is not evidence."]),
 ],
 "resources": [
   ("Nisan et al., chapter 4 (free PDF)",
    "https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf",
    "<b>&sect;&sect;1 and 2</b> — learning, regret, and the "
    "convergence results, with the proofs."),
   ("Roughgarden &mdash; Twenty Lectures, lectures 17 to 18 (free)",
    "http://timroughgarden.org/notes.html",
    "<b>&sect;2</b> — no-regret dynamics and the connection to the "
    "price of anarchy bounds, which is the key link."),
   ("Blum & Mansour &mdash; From external to internal regret (free)",
    "https://www.jmlr.org/papers/v8/blum07a.html",
    "<b>&sect;2's swap-regret result</b>, which is what gets you to "
    "correlated equilibrium."),
   ("Cesa-Bianchi & Lugosi &mdash; Prediction, Learning, and Games",
    "https://www.cambridge.org/9780521841085",
    "<b>&sect;1</b> — the regret framework in full, and the same "
    "material CSCE 669 Module 09 uses. Library copy."),
 ],
 "exercises": [
   "<b>Define regret</b> and compute it for a short action "
   "sequence.",
   "<b>Implement multiplicative weights</b> and verify the regret "
   "bound empirically.",
   "<b>Run it against an adversarial opponent</b> and confirm the "
   "guarantee holds.",
   "<b>Run two no-regret learners against each other</b> in a small "
   "game and plot the empirical distribution.",
   "<b>Check whether it is a correlated equilibrium.</b>",
   "<b>Run them in a zero-sum game</b> and watch the average approach "
   "minimax.",
   "<b>Implement best-response dynamics</b> in a potential game and "
   "plot the potential.",
   "<b>Run it on rock-paper-scissors</b> and observe the cycle.",
   "<b>Compare simultaneous and sequential updates</b> on the same "
   "game.",
   "<b>Attack one of your own mechanisms</b> with a learner and report "
   "the gap.",
 ],
 "selfcheck": [
   "Define regret and no-regret.",
   "What does the guarantee assume about the environment?",
   "Why is it a better behavioural assumption than equilibrium?",
   "What do no-regret dynamics converge to?",
   "What does swap-regret buy, and what about zero-sum games?",
   "Why is the computable concept the reached one?",
   "How does this answer Module 03?",
   "Why do the price of anarchy bounds survive?",
   "When does best-response dynamics converge, and when does it "
   "cycle?",
   "Why must a mechanism be tested against strategic agents?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming a Mechanism Works",
 "subtitle": "The solution concept, the agent model, and the "
             "impossibility you chose.",
 "question": "'It's incentive compatible.' Under what model of the "
             "agents?",
 "outcomes": [
     "State what a mechanism claim must specify.",
     "Identify the standard overclaims.",
     "Explain why a manipulation claim needs an exhibit.",
     "Place this course in the semester and the program.",
     "Evaluate a deployed mechanism.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a claim must name",
   "blurb": "Three things, and most claims name one."},

  {"t": "callout", "title": "A mechanism claim names a solution concept, a model of the agents, and the impossibility it lives with",
   "kind": "The honest reading",
   "body": ["<b>The solution concept</b> — <b>dominant strategy, "
            "Bayes-Nash, or ex-post</b> — <b>because they assume "
            "wildly different things</b> about what agents "
            "know (Module 02 §2).",
            "<b>The agent model</b> — <b>that agents know their own "
            "values, compute best responses, do not collude, and have no "
            "outside interests</b> — <b>four assumptions, each of "
            "which fails somewhere.</b>",
            "<b>And the impossibility it lives with</b> — "
            "<b>every mechanism gives something "
            "up</b> (Modules 06 §4, 10 §3) — <b>and naming which is "
            "what makes a design defensible rather than "
            "merely described.</b>",
            "<b>Plus the benchmark and the approximation ratio</b>, "
            "where the allocation is approximate "
            "(Module 08) — because <b>a ratio without a stated "
            "optimum is not a number.</b>"]},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["The claim", "The correction"],
   "widths": [4.2, 6.8],
   "rows": [
     ["<b>'It is incentive compatible'</b>", "<b>In which solution concept, under what agent model?</b>"],
     ["<b>'It is strategy-proof'</b>", "<b>For which side? (M09 §2)</b>"],
     ["<b>'It is optimal'</b>", "<b>For which objective — welfare, revenue, fairness?</b>"],
     ["<b>'It is fair'</b>", "<b>Which fairness notion? (M11 §1)</b>"],
     ["<b>'Agents will play the equilibrium'</b>", "<b>Which one, and can they compute it? (M03, M12)</b>"],
     ["<b>'It is manipulable'</b>", "<b>Show the manipulation (Part 2)</b>"],
   ],
   "footnote": "<b>'It is optimal' is the one that hides "
               "most</b> — efficiency, revenue, and fairness are "
               "different objectives with different optimal "
               "mechanisms.",
   "note": "Each correction asks for a qualifier the claim "
           "omitted."},

  {"t": "section", "label": "Part 2", "title": "Manipulations need exhibits",
   "blurb": "In both directions."},

  {"t": "callout", "title": "'It is manipulable' without a specific profitable misreport is not a finding",
   "kind": "The standard of evidence this course asks for",
   "body": ["<b>Gibbard-Satterthwaite already tells you almost "
            "everything is manipulable</b> "
            "(Module 10 §3) — <b>so the general claim carries no "
            "information</b> and is not worth "
            "making.",
            "<b>What is informative is: which agent, what true "
            "preferences, what misreport, and how much it "
            "gains</b> — <b>four things, and that is an exhibit "
            "somebody can check.</b>",
            "<b>And it is what distinguishes a serious criticism "
            "from a gesture</b> — <b>a mechanism that is manipulable "
            "only with full knowledge of everybody else's reports is "
            "practically quite different from one manipulable by a "
            "simple rule.</b>",
            "<b>Which is why Project 2 requires a concrete "
            "manipulation or a proof</b> — <b>and the proof is easier "
            "to produce than a convincing "
            "exhibit.</b>"]},

  {"t": "section", "label": "Part 3", "title": "The semester and the program",
   "blurb": "Where this course sits."},

  {"t": "table", "kicker": "Semester 12", "title": "Three courses, one shape",
   "header": ["Course", "Who sets the rules", "The adaptation required"],
   "widths": [2.3, 3.5, 5.2],
   "rows": [
     ["<b>CSCE 640</b>", "<b>Physics</b>", "<b>Design within a gate set and a measurement rule you cannot change</b>"],
     ["<b>CSCE 628</b>", "<b>Biology</b>", "<b>Validate by controls, because no ground truth is available</b>"],
     ["<b>CSCE 717</b>", "<b>Strategic agents</b>", "<b>Make honesty optimal, because you cannot observe the truth</b>"],
   ],
   "footnote": "<b>In all three the true state is unobservable and "
               "the model is not yours to choose</b> — which is the "
               "semester's common structure and its transferable "
               "lesson.",
   "note": "Unobservable truth is what the three courses actually "
           "share."},

  {"t": "section", "label": "Part 4", "title": "Evaluating a deployed mechanism",
   "blurb": "In about ten minutes."},

  {"t": "bullets", "kicker": "Checklist", "title": "The questions, in order",
   "items": [
     "<b>What is the designer's objective?</b> — <b>and is "
     "it the one you assumed?</b> A revenue-maximising auction is "
     "deliberately inefficient "
     "(Module 07 §3).",
     "",
     "<b>What is reported, and what is the incentive to "
     "misreport?</b> (Module 01 §2) — which is the first thing "
     "to ask of any system.",
     "",
     "<b>Which solution concept, and can agents reach "
     "it?</b> (Modules 03 and 12).",
     "",
     "<b>Which impossibility is it living with, and is that the "
     "right one to give up here?</b> (Modules 06 §4, 10 §3).",
     "",
     "<b>And what happens with collusion, false identities, and "
     "repeated play?</b> — <b>three things the single-shot model "
     "omits</b> and that practice does not.",
   ],
   "footnote": "<b>Collusion, false identities, and repetition are "
               "the three things the model omits and practice does "
               "not</b> — and they are where deployed mechanisms "
               "actually fail."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can recognise a strategic input when you see "
            "one</b> (Module 01) — <b>which is the single most "
            "transferable thing here</b>, and applies to systems you "
            "build that have nothing to do with "
            "auctions.",
            "<b>You can measure what decentralisation costs</b> "
            "(Module 04) and <b>decide whether to intervene</b>, "
            "which is a decision engineers make "
            "constantly by instinct.",
            "<b>And you can design a mechanism, name its guarantee "
            "precisely, and name what it gives "
            "up</b> (Modules 06 to 11) — <b>which is the "
            "engineering skill this course is for.</b>",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it is the solution "
            "concept, the agent model, and the impossibility</b> — "
            "because <b>'incentive compatible' is a claim about a model "
            "of people.</b>"]},
 ],
 "takeaways": [
   "A mechanism claim names a solution concept, an agent model, and the "
   "impossibility it lives with.",
   "'It is optimal' hides the most: efficiency, revenue, and fairness are "
   "different objectives with different optimal mechanisms.",
   "'It is manipulable' without a specific profitable misreport carries no "
   "information, since almost everything is manipulable.",
   "An informative manipulation names the agent, the true preferences, the "
   "misreport, and the gain.",
   "Collusion, false identities, and repetition are the three things the "
   "model omits and practice does not.",
   "In all three Semester 12 courses the true state is unobservable and the "
   "model is not yours to choose.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a claim must name"),
  ("callout", "A mechanism claim names a solution concept, a model of the "
              "agents, and the impossibility it lives with",
   ["<b>The solution concept</b> — <b>dominant strategy, "
    "Bayes-Nash, or ex-post equilibrium</b> — <b>because they "
    "assume wildly different things about what each agent knows about "
    "the others</b> (Module 02 &sect;2), and a Bayes-Nash guarantee "
    "requires a common prior that may not exist.",
    "<b>The agent model</b> — <b>that agents know their own "
    "valuations, can compute best responses, do not collude, and have no "
    "interests outside the mechanism</b> — <b>four assumptions, "
    "each of which fails somewhere</b> (Module 07 &sect;4's "
    "measured shading).",
    "<b>And the impossibility it lives with</b> — <b>every "
    "mechanism gives something up</b> (Module 06 &sect;4's "
    "Myerson-Satterthwaite, Module 10 &sect;3's "
    "Gibbard-Satterthwaite) — <b>and naming which one is what "
    "makes a design defensible rather than merely described.</b>",
    "<b>Plus the benchmark and the approximation ratio</b>, wherever "
    "the allocation is computed approximately (Module 08) — "
    "because <b>a ratio stated without the optimum it is a ratio to is "
    "not a number</b>, which is CSCE 629's discipline arriving "
    "here."]),
  ("table", ["The claim", "The correction"],
   [["<b>'The mechanism is incentive compatible.'</b>",
     "<b>In which solution concept, and under what model of the "
     "agents?</b> (&sect;1.)"],
    ["<b>'It is strategy-proof.'</b>",
     "<b>For which side?</b> (Module 09 &sect;2 — deferred "
     "acceptance is strategy-proof for the proposers only.)"],
    ["<b>'It is optimal.'</b>",
     "<b>For which objective — welfare, revenue, or fairness?</b> "
     "See the note."],
    ["<b>'The allocation is fair.'</b>",
     "<b>Which fairness notion?</b> (Module 11 &sect;1's five, "
     "which can conflict.)"],
    ["<b>'Agents will play the equilibrium.'</b>",
     "<b>Which equilibrium, and can they compute it?</b> "
     "(Module 03, and Module 12's answer.)"],
    ["<b>'The mechanism is manipulable.'</b>",
     "<b>Show the manipulation.</b> (&sect;2.)"]],
   [0.34, 0.66]),
  ("p", "<b>'It is optimal' is the one that hides the most</b> "
        "— <b>efficiency, revenue, and fairness are different "
        "objectives with genuinely different optimal mechanisms</b>, and "
        "a revenue-optimal auction is deliberately inefficient "
        "(Module 07 &sect;3). <b>Each correction above asks for a "
        "qualifier the claim omitted</b>, which is the same pattern as "
        "the other two Semester 12 courses' closing tables."),

  ("h1", "2 &nbsp; Manipulations need exhibits"),
  ("callout", "'It is manipulable' without a specific profitable misreport is "
              "not a finding",
   ["<b>Gibbard-Satterthwaite already tells you that almost every "
    "mechanism without money is manipulable</b> (Module 10 "
    "&sect;3) — <b>so the bare general claim carries no "
    "information at all</b> and is not worth making.",
    "<b>What is informative is: which agent, with what true "
    "preferences, submitting what misreport, gaining how much</b> "
    "— <b>four things, and together they are an exhibit somebody "
    "else can check and reproduce.</b>",
    "<b>And it is what distinguishes a serious criticism from a "
    "gesture</b>: <b>a mechanism manipulable only by an agent with full "
    "knowledge of everybody else's reports is practically very different "
    "from one manipulable by a simple rule any participant could "
    "follow</b> — and only the exhibit tells you which you "
    "have.",
    "<b>Which is why Project 2 requires either a proof of "
    "truthfulness or a concrete manipulation</b> — and it is worth "
    "noticing that <b>the proof is frequently easier to produce than a "
    "convincing exhibit</b>, which is a good sign about the standard of "
    "evidence being asked for."]),

  ("break",),
  ("h1", "3 &nbsp; The semester and the program"),
  ("table", ["Course", "Who sets the rules", "The adaptation required"],
   [["<b>CSCE 640</b>", "<b>Physics.</b>",
     "<b>Design within a gate set, a measurement rule, and a noise "
     "model you cannot change</b> — and state the resource "
     "cost."],
    ["<b>CSCE 628</b>", "<b>Biology.</b>",
     "<b>Validate by controls and proxies, because no ground truth is "
     "available to check against.</b>"],
    ["<b>CSCE 717 (this one)</b>", "<b>Strategic agents.</b>",
     "<b>Make honesty optimal, because you cannot observe the true "
     "input and never will.</b>"]],
   [0.22, 0.26, 0.52]),
  ("p", "<b>In all three courses the true state is unobservable and "
        "the model is not yours to choose</b> — the amplitudes "
        "cannot be read, the ground truth is not available, the "
        "valuations are private — <b>which is the semester's common "
        "structure and its transferable lesson</b>. <b>Unobservable "
        "truth is what the three courses actually share</b>, and each "
        "answers it differently: interference engineering, negative "
        "controls, and incentive compatibility are three responses to the "
        "same predicament."),

  ("h1", "4 &nbsp; Evaluating a deployed mechanism"),
  ("ul", ["<b>What is the designer's objective?</b> — <b>and is "
          "it the one you assumed?</b> <b>A revenue-maximising auction "
          "is deliberately inefficient</b> (Module 07 &sect;3), and "
          "reading it as a failed attempt at efficiency is a "
          "misdiagnosis.",
          "<b>What is reported, and what is the incentive to "
          "misreport it?</b> (Module 01 &sect;2's table) — "
          "<b>which is the first thing to ask of any system</b> and "
          "takes thirty seconds.",
          "<b>Which solution concept does the guarantee use, and can "
          "the agents actually reach it?</b> (Module 03's hardness, "
          "and Module 12's answer about what they reach instead).",
          "<b>Which impossibility is it living with, and is that the "
          "right thing to give up in this setting?</b> (Module 06 "
          "&sect;4, Module 10 &sect;3) — since something must "
          "be given up, the question is only whether the choice "
          "suits.",
          "<b>And what happens under collusion, false identities, and "
          "repeated play?</b> — <b>three things the single-shot "
          "model omits and that practice does not</b>. <b>They are where "
          "deployed mechanisms actually fail</b>, rather than at the "
          "points the theory worries about."]),
  ("callout", "Where this course leaves you",
   ["<b>You can recognise a strategic input when you see one</b> "
    "(Module 01) — <b>which is the single most transferable thing "
    "in this course</b>, and <b>applies to systems you build that have "
    "nothing to do with auctions</b>: priority fields, quotas, resource "
    "requests, and every metric that determines an allocation.",
    "<b>You can measure what decentralisation costs</b> "
    "(Module 04's price of anarchy) <b>and decide whether to "
    "intervene</b> — <b>which is a decision engineers make "
    "constantly by instinct</b> and can now make with a number.",
    "<b>And you can design a mechanism, state its guarantee "
    "precisely, and name what it gives up</b> (Modules 06 through 11) "
    "— <b>which is the engineering skill this course exists "
    "for</b>, and is what Project 2 assesses.",
    "<b>The closing rule is the program's, unchanged across "
    "thirty-six courses:</b> <b>state what you measured, state what you "
    "assumed, and never claim more than you established.</b> <b>In this "
    "subject it is the solution concept, the agent model, and the "
    "impossibility</b> — because <b>'incentive compatible' is a "
    "claim about a model of people</b>, and the people are the part the "
    "model is least sure about."]),
 ],
 "resources": [
   ("Roughgarden &mdash; Twenty Lectures, the closing lectures (free)",
    "http://timroughgarden.org/notes.html",
    "<b>&sect;&sect;1 and 4</b> — what the guarantees mean and where "
    "they stop, stated by somebody careful about it."),
   ("Milgrom &mdash; Discovering Prices",
    "https://cup.columbia.edu/book/discovering-prices/9780231175982",
    "<b>&sect;4</b> — a deployed mechanism described by its designer, "
    "including what had to be given up and why. Library copy."),
   ("Rothkopf &mdash; Thirteen reasons why the Vickrey-Clarke-Groves "
    "process is not practical",
    "https://pubsonline.informs.org/doi/10.1287/opre.1070.0401",
    "<b>&sect;&sect;1 and 4</b> — the practical objections to the "
    "theoretically optimal mechanism, enumerated."),
   ("The ACM EC proceedings (free preprints)",
    "https://dl.acm.org/conference/ec",
    "<b>&sect;&sect;1 and 2</b> — current work, and the better papers "
    "state all three of &sect;1's items in the abstract."),
 ],
 "exercises": [
   "<b>State the three things a mechanism claim must name</b>, for a "
   "mechanism you have seen.",
   "<b>Find three published mechanism claims</b> and check which of "
   "the three each names.",
   "<b>Correct six overclaims</b> in your own words.",
   "<b>Take a 'strategy-proof' claim</b> and identify the side.",
   "<b>Produce a concrete manipulation exhibit</b> for one mechanism, "
   "with all four components.",
   "<b>Compare its difficulty</b> to proving truthfulness for a "
   "different one.",
   "<b>State each Semester 12 course's unobservable truth.</b>",
   "<b>Evaluate one deployed mechanism</b> against §4's five "
   "questions.",
   "<b>Find a mechanism that failed in practice</b> for one of "
   "§4's last three reasons.",
   "<b>Project 2 is now due.</b> Submit the mechanism, its incentive "
   "proof or concrete manipulation, the approximation ratio against a "
   "named benchmark, the strategic simulation compared to the honest "
   "baseline, and the impossibility you chose to live with.",
 ],
 "selfcheck": [
   "Name the three things a mechanism claim must specify.",
   "What fourth thing is needed when the allocation is approximate?",
   "Correct six standard overclaims.",
   "Which overclaim hides the most, and why?",
   "Why is a general manipulability claim uninformative?",
   "What four things make a manipulation exhibit?",
   "Why does the exhibit matter practically?",
   "State each Semester 12 course's external model and unobservable "
   "truth.",
   "Give the five questions for evaluating a deployed mechanism.",
   "Where do deployed mechanisms actually fail?",
 ],
},

]
