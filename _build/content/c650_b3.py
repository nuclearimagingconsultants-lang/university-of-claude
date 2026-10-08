# -*- coding: utf-8 -*-
"""CSCE 650 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Locomotion",
 "subtitle": "Moving through a space larger than the room.",
 "question": "How do you let someone walk a kilometre in a 3 m room?",
 "outcomes": [
     "Compare locomotion schemes on comfort and presence.",
     "Explain why teleport is comfortable and what it costs.",
     "Explain redirected walking and its space requirements.",
     "Apply the comfort techniques that make smooth locomotion viable.",
     "Choose a locomotion model from the experience being built.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The constraint",
   "blurb": "Real rooms are small."},

  {"t": "callout", "title": "Real walking is best and does not scale",
   "kind": "The problem statement",
   "body": ["<b>Walking in the physical space is perfectly comfortable</b> "
            "— the vestibular and visual signals agree exactly, because "
            "they are both real.",
            "<b>It also produces the strongest presence</b> of any "
            "locomotion method, by a wide margin.",
            "<b>And a typical play space is 2 by 2 metres.</b> Many users "
            "have less, and many are seated.",
            "<b>So everything in this module is a way of covering more "
            "distance than the room allows</b>, and every one of them is "
            "worse than real walking in some respect."]},

  {"t": "table", "kicker": "Schemes", "title": "The locomotion options",
   "header": ["Scheme", "Comfort", "Presence", "Space needed"],
   "widths": [3.2, 2.6, 2.6, 3.7],
   "rows": [
     ["<b>Real walking</b>", "<b>Perfect</b>", "<b>Highest</b>", "<b>Impractical</b>"],
     ["<b>Teleport</b>", "<b>Excellent</b>", "Low", "Any, incl. seated"],
     ["Dash / blink", "Very good", "Low-moderate", "Any"],
     ["<b>Smooth (continuous)</b>", "<b>Poor without help</b>", "<b>High</b>", "Any"],
     ["Arm swinging", "Good", "Moderate", "Any"],
     ["<b>Redirected walking</b>", "<b>Excellent</b>", "<b>Highest</b>", "<b>~6×6 m minimum</b>"],
     ["Vehicle / cockpit", "Very good", "High in context", "Seated"],
   ],
   "footnote": "<b>The comfort and presence columns are in tension</b>, "
               "which is the whole design problem.",
   "note": "That tension is the module. There is no scheme that is top of "
           "both columns and fits in a bedroom."},

  {"t": "section", "label": "Part 2", "title": "Teleport",
   "blurb": "The default, and why."},

  {"t": "callout", "title": "Teleport works because there is no motion to conflict with",
   "kind": "The mechanism",
   "body": ["<b>The user points, confirms, and is instantly elsewhere.</b> "
            "No visual motion occurs, so no vection, so no conflict "
            "(Module 07).",
            "<b>It is comfortable for essentially everyone</b>, including "
            "people who cannot tolerate any other scheme.",
            "<b>The cost is presence.</b> Discontinuous movement is "
            "nothing like being in a place, and users lose their spatial "
            "mental map.",
            "<b>A brief fade or blink helps the disorientation</b> without "
            "reintroducing motion — it signals the transition rather than "
            "animating it."]},

  {"t": "bullets", "kicker": "Design", "title": "Making teleport good",
   "items": [
     "<b>Show the destination clearly</b> before committing — an arc, a "
     "marker, and a preview of the facing direction.",
     "",
     "<b>Indicate validity.</b> The arc should change colour or break when "
     "the target is invalid, before the user tries.",
     "",
     "<b>Let the user choose the facing direction</b> during the "
     "aim — rotating after arriving is an extra step and a comfort "
     "problem.",
     "",
     "<b>Keep the transition short</b> — a 100 ms fade, not a second.",
     "",
     "<b>Preserve the spatial relationship.</b> Teleporting should not "
     "change the user's height or orientation unexpectedly.",
   ],
   "note": "Facing-direction selection during aim is the refinement that "
           "distinguishes a good teleport from a basic one."},

  {"t": "section", "label": "Part 3", "title": "Smooth locomotion",
   "blurb": "What people want, and how to make it survivable."},

  {"t": "callout", "title": "Smooth locomotion is high presence and high risk",
   "kind": "The trade",
   "body": ["<b>Continuous movement feels like being in a place</b> in a "
            "way teleport does not, and experienced users strongly prefer "
            "it.",
            "<b>And it produces vection continuously</b>, which is the "
            "exact mechanism of Module 07.",
            "<b>It is the single largest cause of VR sickness in shipped "
            "applications.</b>",
            "<b>So it must be offered as an option, never as the only "
            "mode</b> — and it must be built with the mitigations below "
            "rather than having them added later."]},

  {"t": "table", "kicker": "Mitigations", "title": "Making smooth locomotion tolerable",
   "header": ["Technique", "Effect"],
   "widths": [4.0, 8.1],
   "rows": [
     ["<b>Constant velocity, no acceleration</b>", "<b>Large. The most important one</b>"],
     ["<b>Dynamic vignette</b>", "<b>Large. Reduces peripheral vection</b>"],
     ["<b>Snap turning</b>", "<b>Large. Removes visual rotation</b>"],
     ["Lower speed", "Moderate; too slow becomes frustrating"],
     ["A cockpit or frame", "Moderate (Module 07)"],
     ["Head-relative rather than controller-relative direction", "Modest; more predictable"],
   ],
   "footnote": "<b>The first three together make smooth locomotion viable "
               "for most people.</b> Omitting them makes it viable for "
               "developers only.",
   "note": "Snap turning matters more than people expect — rotation is "
           "the worst provocation."},

  {"t": "callout", "title": "Snap turning is not a compromise",
   "kind": "Why rotation is special",
   "body": ["<b>Visually rotating the world while the head is still is the "
            "most provocative thing in Module 07's table</b> — the "
            "semicircular canals are extremely sensitive to rotation.",
            "<b>Snap turning jumps by a fixed increment</b> — 30&deg; or "
            "45&deg; — with a brief fade. No continuous rotation "
            "occurs.",
            "<b>Users adapt to it within a minute</b> and generally stop "
            "noticing.",
            "<b>And physical turning should always be available too.</b> "
            "Many users will simply turn their body, which is free and "
            "perfect — the design should not assume a forward-facing "
            "user."]},

  {"t": "section", "label": "Part 4", "title": "Redirected walking",
   "blurb": "Letting people walk further than the room."},

  {"t": "callout", "title": "Exploit the fact that vision dominates",
   "kind": "How redirection works",
   "body": ["<b>When vision and proprioception disagree slightly, vision "
            "wins</b> and the user does not notice.",
            "<b>So rotate the virtual world slowly while the user walks a "
            "straight line</b>, and they will walk a curve in the real room "
            "while believing they walked straight.",
            "<b>Detection thresholds are known:</b> roughly 10&deg; per "
            "second of added rotation while turning, and a radius of about "
            "22 m for curvature, go unnoticed.",
            "<b>The catch is the space requirement.</b> That curvature "
            "radius implies a room of roughly 6 by 6 metres at minimum, "
            "which almost nobody has."]},

  {"t": "bullets", "kicker": "Variants", "title": "Practical redirection techniques",
   "items": [
     "<b>Rotation gain:</b> amplify the user's turns so a 90&deg; physical "
     "turn becomes 100&deg; virtual. Subtle and effective.",
     "",
     "<b>Curvature gain:</b> bend the virtual path so the real path "
     "curves. Needs the most space.",
     "",
     "<b>Change blindness:</b> move a doorway or corridor while the user is "
     "not looking at it. Works remarkably well.",
     "",
     "<b>Portals and impossible spaces:</b> rooms that overlap in physical "
     "space, connected so the user never notices.",
     "",
     "<b>Resetting:</b> when the user approaches a wall, intervene — "
     "distract them into turning around.",
   ],
   "note": "Impossible spaces are the most practical of these for ordinary "
           "room sizes and are underused."},

  {"t": "callout", "title": "Choose the locomotion model before anything else",
   "kind": "The design ordering",
   "body": ["<b>Locomotion determines what the experience can be.</b> A "
            "teleport game and a smooth-locomotion game are different games, "
            "not the same game with a setting.",
            "<b>It constrains level design</b> — teleport needs valid "
            "destinations and sightlines; smooth locomotion needs navigable "
            "geometry.",
            "<b>It constrains the fiction.</b> Why can this character "
            "teleport? Many designs answer with a cockpit or a vehicle, "
            "which solves the comfort problem too.",
            "<b>Retrofitting it is a redesign.</b> This is why Module 07 "
            "said to decide it first, and it is the most consequential early "
            "decision in a VR project."]},
 ],
 "takeaways": [
   "Real walking is perfectly comfortable and produces the highest presence, "
   "and a typical play space is 2 by 2 metres.",
   "Comfort and presence are in tension across every scheme, which is the "
   "whole design problem.",
   "Teleport is comfortable because no visual motion occurs, and it costs "
   "presence and spatial awareness.",
   "Smooth locomotion gives the highest presence and is the largest single "
   "cause of sickness in shipped applications — offer it, never force "
   "it.",
   "Constant velocity, a dynamic vignette, and snap turning together make "
   "smooth locomotion viable for most people.",
   "Redirected walking exploits vision dominating proprioception, and the "
   "curvature thresholds imply a room about 6 by 6 metres.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The constraint"),
  ("callout", "Real walking is the best option and does not scale",
   ["<b>Walking in the physical space is perfectly comfortable.</b> The "
    "vestibular and visual signals agree exactly, because both are "
    "reporting a real motion that is genuinely occurring. There is no "
    "conflict to resolve (Module 07).",
    "<b>It also produces the strongest sense of presence of any locomotion "
    "method</b>, by a considerable margin — the body's own "
    "proprioceptive and effort cues are present and consistent.",
    "<b>And a typical play space is about 2 metres square.</b> Many users "
    "have less; many are seated; some are on an aeroplane.",
    "<b>So every technique in this module is a way of covering more "
    "distance than the room physically permits</b>, and every one of them is "
    "worse than real walking in at least one respect. There is no solution "
    "here, only a set of trades."]),
  ("table", ["Scheme", "Comfort", "Presence", "Space", "Notes"],
   [["<b>Real walking</b>", "<b>Perfect</b>", "<b>Highest</b>",
     "<b>As much as the virtual space</b>",
     "The benchmark everything else is measured against."],
    ["<b>Teleport</b>", "<b>Excellent</b>", "Low",
     "Any, including seated", "&sect;2. The safe default."],
    ["<b>Dash / blink</b>", "Very good", "Low to moderate", "Any",
     "A very fast movement with a fade — between teleport and smooth, "
     "and a reasonable compromise."],
    ["<b>Smooth (continuous)</b>", "<b>Poor without mitigation</b>",
     "<b>High</b>", "Any", "&sect;3. What experienced users ask for."],
    ["<b>Arm swinging</b>", "Good", "Moderate", "Any",
     "Swing the controllers to walk. The physical effort appears to help, "
     "and it is tiring."],
    ["<b>Redirected walking</b>", "<b>Excellent</b>", "<b>Highest</b>",
     "<b>~6&times;6 m minimum</b>", "&sect;4. Wonderful and rarely "
     "applicable."],
    ["<b>Vehicle / cockpit</b>", "Very good", "High within the fiction",
     "Seated",
     "The cockpit supplies a stable reference frame (Module 07), which is "
     "why driving and flying worked in VR years before walking did."]],
   [0.17, 0.15, 0.14, 0.18, 0.36]),
  ("p", "<b>The comfort and presence columns are in tension throughout</b>, "
        "and that tension is the entire design problem of this module. No "
        "scheme is top of both columns and fits in an ordinary room."),

  ("h1", "2 &nbsp; Teleport"),
  ("callout", "Teleport works because there is no motion to conflict with",
   ["<b>The user aims, confirms, and is instantly somewhere else.</b> No "
    "visual motion occurs at all, so no vection is induced, so there is "
    "nothing for the vestibular system to contradict.",
    "<b>It is comfortable for essentially everyone</b>, including the "
    "substantial group of people who cannot tolerate any continuous scheme. "
    "For an application that needs to be usable by an unselected audience, "
    "this is decisive.",
    "<b>The cost is presence and spatial awareness.</b> Moving "
    "discontinuously through a space is nothing like being in it, and users "
    "lose track of where they are relative to where they were — the "
    "cognitive map that real walking builds for free does not form.",
    "<b>A brief fade or blink mitigates the disorientation</b> without "
    "reintroducing motion. It signals that a transition has occurred rather "
    "than animating the transit, which is the important distinction."]),
  ("ul", ["<b>Show the destination clearly before committing.</b> A "
          "projected arc, a marker on the ground, and an indication of which "
          "way the user will be facing. Uncertainty about where you will "
          "arrive is the main usability failure of bad teleport.",
          "<b>Indicate validity during the aim.</b> The arc should change "
          "colour or visibly break when the target is unreachable, so the "
          "user learns the rules without having to fail.",
          "<b>Let the user choose their facing direction during the "
          "aim</b> — typically by the thumbstick's direction. Arriving "
          "and then having to turn is both an extra interaction and a "
          "comfort problem, since turning is the provocative motion. <b>This "
          "is the refinement that distinguishes a good teleport "
          "implementation from a basic one.</b>",
          "<b>Keep the transition brief</b> — a fade of around 100 ms. "
          "A long fade is an animation, and animations of motion are what we "
          "are avoiding.",
          "<b>Preserve the spatial relationship.</b> Teleporting should not "
          "silently change the user's height, their orientation relative to "
          "the room, or their position within the play space, all of which "
          "are disorienting in ways users cannot diagnose."]),

  ("break",),
  ("h1", "3 &nbsp; Smooth locomotion"),
  ("callout", "High presence, high risk",
   ["<b>Continuous movement feels like being in a place</b> in a way "
    "teleport simply does not. The space is traversed rather than sampled, "
    "distances are felt, and the cognitive map forms. Experienced VR users "
    "strongly prefer it and frequently ask for it.",
    "<b>And it produces vection continuously</b>, which is precisely the "
    "mechanism Module 07 identified. The user is visually moving and "
    "physically still, for as long as they hold the stick.",
    "<b>It is the single largest cause of sickness in shipped VR "
    "applications.</b> Not latency, not frame drops — locomotion.",
    "<b>So it must be offered as an option and never imposed as the only "
    "mode</b>, and it must be built with the mitigations below from the "
    "start rather than having them retrofitted. An application whose only "
    "locomotion is unmitigated smooth movement has excluded a large "
    "fraction of its potential users by construction."]),
  ("table", ["Technique", "Effect", "Notes"],
   [["<b>Constant velocity, no acceleration</b>", "<b>Large</b>",
     "<b>The most important single measure</b> (Module 07). Reach full "
     "speed immediately and stop immediately; a gentle ramp is worse than "
     "an abrupt one."],
    ["<b>Dynamic vignette during movement</b>", "<b>Large</b>",
     "Darken and narrow the periphery while moving, restore it when "
     "stationary. Attacks vection at its strongest point. Make the strength "
     "adjustable."],
    ["<b>Snap turning</b>", "<b>Large</b>", "See below."],
    ["<b>Lower movement speed</b>", "Moderate",
     "Less visual flow per second. Too slow becomes frustrating and users "
     "turn it up, so this trades against itself."],
    ["<b>A cockpit or helmet frame</b>", "Moderate",
     "A stable reference frame (Module 07)."],
    ["<b>Head-relative rather than controller-relative direction</b>",
     "Modest",
     "Moving where you look is more predictable than moving where the "
     "controller points, and predictability reduces conflict. Offer both; "
     "preferences differ strongly."]],
   [0.28, 0.14, 0.58]),
  ("callout", "Snap turning is not a compromise",
   ["<b>Visually rotating the world while the head is stationary is the "
    "most provocative item in Module 07's table.</b> The semicircular canals "
    "are exquisitely sensitive to rotation, and a smooth stick-driven turn "
    "produces a large, sustained, entirely uncontradicted visual rotation "
    "signal.",
    "<b>Snap turning jumps the view by a fixed increment</b> — 30 or "
    "45 degrees — usually with a brief fade. <b>No continuous rotation "
    "ever occurs</b>, so the canals have nothing to object to.",
    "<b>Users adapt within a minute</b> and generally stop noticing it. The "
    "common objection — that it is unnatural — turns out to "
    "matter much less in practice than it does in discussion.",
    "<b>And physical turning should always remain available.</b> Many users "
    "will simply rotate their body, which costs nothing and is perfectly "
    "comfortable. <b>Designs that assume a forward-facing user</b> — "
    "by placing important content only ahead, or by binding a cable "
    "awkwardly — discard the best turning method available."]),

  ("h1", "4 &nbsp; Redirected walking"),
  ("callout", "Vision dominates proprioception, and that can be exploited",
   ["<b>When visual and proprioceptive signals disagree slightly, vision "
    "wins</b> and the discrepancy goes unnoticed. This is a robust finding "
    "and it is the basis of the entire technique.",
    "<b>So rotate the virtual world slowly while the user walks what they "
    "believe is a straight line.</b> They will in fact walk a curve in the "
    "physical room, continuously correcting without awareness, while "
    "experiencing a straight path through the virtual space.",
    "<b>The detection thresholds have been measured:</b> roughly 10 degrees "
    "per second of added rotation while the user is already turning, and a "
    "curvature radius of about 22 metres while walking straight, both go "
    "unnoticed by most people.",
    "<b>The catch is the space requirement.</b> A 22-metre curvature radius "
    "implies a physical room of roughly 6 by 6 metres at absolute minimum to "
    "keep a user walking indefinitely — and realistically more. <b>This "
    "is why redirected walking, which is genuinely excellent, appears almost "
    "exclusively in research labs and location-based venues.</b>"]),
  ("ul", ["<b>Rotation gain</b> amplifies the user's own turns: a 90-degree "
          "physical turn produces a 100-degree virtual one. Subtle, "
          "effective, and it accumulates usable reorientation over a session "
          "without any single turn being detectable.",
          "<b>Curvature gain</b> bends the virtual path so the physical path "
          "curves. The most powerful technique and the one with the largest "
          "space requirement.",
          "<b>Change blindness</b> moves geometry while the user is not "
          "looking at it — a doorway relocated to the other end of a "
          "room while the user's back is turned. <b>It works remarkably "
          "well</b>, because people do not monitor the parts of an "
          "environment they are not attending to.",
          "<b>Impossible spaces</b> let rooms overlap in physical space, "
          "connected by corridors whose virtual length exceeds their "
          "physical one. A user walks between two rooms that could not both "
          "fit. <b>This is the most practical of these techniques for "
          "ordinary room sizes and is underused.</b>",
          "<b>Resetting</b> handles the failure case: when the user "
          "approaches a physical wall despite everything, intervene — "
          "distract them into turning around, or present an in-fiction "
          "reason to reorient. Inelegant, and necessary."]),
  ("callout", "Choose the locomotion model before anything else",
   ["<b>Locomotion determines what the experience can be.</b> A teleport "
    "game and a smooth-locomotion game are different games that happen to "
    "share assets — not one game with a settings toggle.",
    "<b>It constrains level design directly.</b> Teleport requires valid "
    "destinations, clear sightlines to them, and spaces that read correctly "
    "when sampled discontinuously. Smooth locomotion requires continuously "
    "navigable geometry and tolerable sightline changes. These produce "
    "different level geometry.",
    "<b>It constrains the fiction.</b> Why can this character teleport? "
    "Many designs answer by making the player a machine, a ghost, or a "
    "pilot — and the cockpit answer solves the comfort problem at the "
    "same time, which is not a coincidence.",
    "<b>Retrofitting locomotion is a redesign, not an adjustment.</b> This "
    "is why Module 07 said to decide it first, and it is the single most "
    "consequential early decision in a VR project."]),
 ],
 "resources": [
   ("LaValle &mdash; Virtual Reality, Chapter 10 (free)",
    "http://lavalle.pl/vr/",
    "Locomotion and its relationship to sickness, with the research "
    "framing."),
   ("Steinicke et al. &mdash; Estimation of Detection Thresholds for "
    "Redirected Walking (free)",
    "https://ieeexplore.ieee.org/document/5461720",
    "Where &sect;4's threshold numbers come from. The experimental design is "
    "worth reading on its own."),
   ("Suma et al. &mdash; Impossible Spaces and Change Blindness Redirection "
    "(free)",
    "https://ict.usc.edu/pubs/",
    "The two most practical redirection techniques for small rooms."),
   ("Meta &mdash; locomotion design guidelines (free)",
    "https://developers.meta.com/horizon/resources/",
    "The practical comfort rules for each scheme, with vendor testing "
    "behind them."),
 ],
 "exercises": [
   "Implement teleport with an arc, a validity indicator, and "
   "facing-direction selection during the aim. Test on a novice.",
   "Implement smooth locomotion with and without a dynamic vignette and "
   "compare comfort scores across six people.",
   "Implement acceleration ramps and instant velocity changes, and compare. "
   "The result is counterintuitive.",
   "Implement snap turning and smooth turning. Measure how long it takes "
   "users to stop noticing snap turning.",
   "Implement rotation gain and find your own detection threshold by "
   "increasing it until you notice.",
   "Implement an impossible space: two rooms that overlap physically, "
   "connected by a corridor. Measure whether anyone notices.",
   "Implement change-blindness redirection by moving a doorway while the "
   "user is not looking at it.",
   "Measure how far a user can actually walk before hitting a wall, with and "
   "without redirection, in your available space.",
   "Write the locomotion section of a design document for an application of "
   "your choosing, justifying the choice from this module and Module 07.",
 ],
 "selfcheck": [
   "Why is real walking the benchmark, and why is it impractical?",
   "Compare seven locomotion schemes on comfort, presence, and space.",
   "Why is teleport comfortable, and what does it cost?",
   "Give five design rules for good teleport, and say which is most often "
   "missed.",
   "Why is smooth locomotion both preferred and dangerous?",
   "Name the three mitigations that make smooth locomotion viable.",
   "Why is snap turning not a compromise?",
   "How does redirected walking work, what are the thresholds, and what "
   "space does it need?",
   "Name four redirection techniques and say which suits a small room.",
   "Why must locomotion be chosen first?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Interaction and Input",
 "subtitle": "Hands in a world that does not push back.",
 "question": "How do you let someone manipulate things that are not there?",
 "outcomes": [
     "Compare direct manipulation with ray-based selection.",
     "Apply Fitts's law in three dimensions.",
     "Design affordances a first-time user discovers unaided.",
     "Explain why hands pass through objects and what to do about it.",
     "Compare hand tracking with controllers honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two interaction models",
   "blurb": "Reach and touch, or point and select."},

  {"t": "two", "kicker": "Models", "title": "Direct and ray-based",
   "lh": "Direct manipulation",
   "l": ["Reach out and touch the thing.",
         "<b>Immediately understood</b> — no instruction needed.",
         "<b>Limited to arm's reach.</b>",
         ("Tiring if sustained — 'gorilla arm'.", 1),
         "Best for close, physical, tactile interaction."],
   "rh": "Ray / pointer",
   "r": ["Point a ray and select at a distance.",
         "Needs a moment of learning, then it is natural.",
         "<b>Unlimited range.</b>",
         ("Precision falls with distance — angular error "
          "amplifies.", 1),
         "Best for menus, distant objects, and seated use."],
   "note": "Most applications need both, and switching between them "
           "smoothly is a real design problem."},

  {"t": "callout", "title": "Fitts's law still applies, and distance is now depth",
   "kind": "The quantitative part",
   "body": ["<b>Time to acquire a target grows with distance and falls "
            "with target size</b> — the same law as on a desktop.",
            "<b>In VR, angular size is what matters for ray pointing.</b> A "
            "distant object is a small target however large it is.",
            "<b>And the hand is less precise than a mouse</b> — there is "
            "no surface to rest on, and tremor is unfiltered.",
            "<b>So: make targets angularly large, bring them close, and "
            "filter the input.</b> Interface elements that would be fine on "
            "a monitor are frequently too small in VR."]},

  {"t": "bullets", "kicker": "Precision", "title": "Helping an unsupported hand",
   "items": [
     "<b>Filter the pose</b> — a one-euro filter or similar removes "
     "tremor without adding noticeable lag.",
     "",
     "<b>Snapping and magnetism:</b> pull the ray or the held object "
     "toward valid targets.",
     "",
     "<b>Larger hit volumes than visual volumes.</b> The collider can be "
     "generous; the user judges by the visual.",
     "",
     "<b>Support the arm where possible</b> — design for elbows on a "
     "desk, or for brief rather than sustained reaching.",
     "",
     "<b>Avoid tasks requiring sub-centimetre precision</b> unless you "
     "have a physical surface to brace against.",
   ],
   "footnote": "Gorilla arm is a real constraint — sustained "
               "unsupported reaching is tiring within a couple of minutes."},

  {"t": "section", "label": "Part 2", "title": "Grabbing",
   "blurb": "The interaction everyone implements first."},

  {"t": "callout", "title": "Your hand will pass through the object",
   "kind": "The fundamental problem",
   "body": ["<b>There is nothing to stop it.</b> The virtual object is "
            "solid; the physical hand is not constrained by anything.",
            "<b>If the virtual hand tracks the real hand exactly, it "
            "penetrates</b> — which is the most common presence break "
            "(Module 01).",
            "<b>If it stops at the surface, it diverges from the real "
            "hand</b>, which is visually wrong but usually preferable.",
            "<b>This is the standard solution</b>: a physics-driven hand "
            "that stops at surfaces, with the real hand's position shown "
            "faintly or not at all. Users accept the divergence readily."]},

  {"t": "table", "kicker": "Grab", "title": "Grab implementations",
   "header": ["Approach", "Behaviour", "Use"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Snap to hand", "Object jumps to a fixed pose", "<b>Tools, weapons — predictable</b>"],
     ["<b>Preserve offset</b>", "Object keeps its relative pose", "<b>Natural for most objects</b>"],
     ["Physics joint", "A spring connects object to hand", "<b>Heavy objects; collisions work</b>"],
     ["Two-handed", "Both hands constrain position and rotation", "Large objects; aiming"],
   ],
   "footnote": "Physics joints let a held object collide with the world, "
               "which is what makes a held object feel real.",
   "note": "The physics-joint approach is what makes held objects feel "
           "weighty, and it is more work than it looks."},

  {"t": "section", "label": "Part 3", "title": "Affordances",
   "blurb": "Making it obvious without instructions."},

  {"t": "callout", "title": "Nobody reads instructions in VR",
   "kind": "The design constraint",
   "body": ["<b>Text is uncomfortable to read</b> (Module 02), the user is "
            "looking around, and there is no manual.",
            "<b>So interactions must be discoverable</b> — the object "
            "must look like it can be grabbed, and the handle must look "
            "like a handle.",
            "<b>Highlight on proximity.</b> The simplest and most effective "
            "technique: objects that respond when a hand approaches teach "
            "their own interactivity.",
            "<b>Use real-world forms.</b> A lever, a dial, a button, a "
            "handle — people already know what to do with these, and that "
            "knowledge transfers completely."]},

  {"t": "bullets", "kicker": "Feedback", "title": "Feedback matters more than in flat applications",
   "items": [
     "<b>Visual:</b> highlight on hover, change on grab, animate on "
     "release. The minimum.",
     "",
     "<b>Audio:</b> a click on contact, a sound on grab. <b>Cheap and "
     "disproportionately effective</b> at making an interaction feel "
     "real.",
     "",
     "<b>Haptic:</b> a controller pulse on contact. Crude, and it "
     "substantially improves the sense of touching something.",
     "",
     "<b>And they compound.</b> Visual plus audio plus haptic together "
     "feel far more solid than any one of them.",
     "",
     "<b>Because there is no force feedback</b>, these are all you have to "
     "signal contact.",
   ],
   "note": "The compounding point is worth stressing — the three "
           "channels together are more than additive."},

  {"t": "section", "label": "Part 4", "title": "Hands and controllers",
   "blurb": "An honest comparison."},

  {"t": "table", "kicker": "Input", "title": "Hand tracking and controllers",
   "header": ["", "Controllers", "Hand tracking"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["Precision", "<b>High and consistent</b>", "Lower; varies with pose"],
     ["Buttons", "<b>Many, unambiguous</b>", "<b>None — gestures only</b>"],
     ["Haptics", "<b>Yes</b>", "<b>None</b>"],
     ["Occlusion", "Tracked when hidden (IMU)", "<b>Fails when hidden</b>"],
     ["Learning", "Requires a moment", "<b>Immediate</b>"],
     ["Fatigue", "Lower — something to hold", "Higher"],
     ["Feels natural", "Less", "<b>More, when it works</b>"],
   ],
   "footnote": "<b>Hand tracking is better for demos and controllers are "
               "better for applications</b> — which is an "
               "uncomfortable fact.",
   "note": "Be honest here. Hand tracking demos superbly and the lack of "
           "haptics and buttons is a real cost in sustained use."},

  {"t": "callout", "title": "The missing button problem",
   "kind": "Why hand tracking is harder than it looks",
   "body": ["<b>A controller has an unambiguous binary input.</b> The "
            "trigger is pressed or it is not.",
            "<b>A hand has no such thing.</b> Pinch detection is a "
            "classifier with a threshold, and it has both false positives "
            "and false negatives.",
            "<b>So every interaction must tolerate misdetection</b> — "
            "accidental grabs, failed grabs, and releases that did not "
            "happen.",
            "<b>And there is no haptic confirmation</b>, so the user cannot "
            "feel whether the system registered their action. Visual and "
            "audio feedback must carry the whole load."]},
 ],
 "takeaways": [
   "Direct manipulation is immediately understood and limited to arm's "
   "reach; ray pointing has unlimited range and loses precision with "
   "distance.",
   "Fitts's law applies with angular size as the target measure, and an "
   "unsupported hand is less precise than a mouse — so make targets "
   "large and filter the input.",
   "The virtual hand will pass through objects because nothing stops the "
   "real one; a physics hand that stops at surfaces is the standard answer "
   "and users accept the divergence.",
   "Nobody reads instructions in VR, so interactions must be discoverable "
   "— proximity highlighting and real-world forms carry most of it.",
   "Visual, audio, and haptic feedback compound, and together they are the "
   "only signal of contact available without force feedback.",
   "Hand tracking demos better and controllers work better: no buttons, no "
   "haptics, and failure under occlusion are real costs.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two interaction models"),
  ("table", ["", "Direct manipulation", "Ray / pointer"],
   [["Method", "Reach out and touch the object with a virtual hand.",
     "Project a ray from the hand or controller and select what it hits."],
    ["Discoverability", "<b>Immediate.</b> No instruction required; people "
     "reach for things.",
     "Requires a moment of learning, after which it feels natural."],
    ["Range", "<b>Arm's length.</b>", "<b>Unlimited.</b>"],
    ["Precision", "Good at close range; limited by hand steadiness.",
     "<b>Falls with distance</b> — a fixed angular error in hand "
     "orientation becomes a larger positional error further away."],
    ["Fatigue", "<b>High if sustained</b> — the 'gorilla arm' "
     "problem. Holding an arm out is tiring within a couple of minutes.",
     "Lower — the hand can rest at the side or on a lap."],
    ["Best for", "Close, physical, tactile interaction — picking "
     "things up, operating controls.",
     "Menus, distant objects, and seated use."]],
   [0.15, 0.42, 0.43]),
  ("p", "<b>Most applications need both</b>, and switching between them "
        "cleanly — so the user is never unsure which model is active "
        "— is a genuine design problem. A common solution is proximity: "
        "direct manipulation when the hand is near an object, ray pointing "
        "otherwise, with a visible transition."),
  ("callout", "Fitts's law applies, with angular size as the measure",
   ["<b>Time to acquire a target grows with distance and falls with target "
    "size</b> — the same relationship that governs desktop interfaces, "
    "and it holds in three dimensions.",
    "<b>For ray pointing, angular size is what matters.</b> A large object "
    "far away subtends a small angle and is therefore a small target, "
    "however large it looks in world units. This is why distant menus are "
    "frustrating even when they appear big.",
    "<b>And an unsupported hand is substantially less precise than a "
    "mouse.</b> There is no surface to rest on, the arm is a long lever "
    "amplifying shoulder tremor, and none of it is filtered by friction the "
    "way a mouse on a desk is.",
    "<b>So: make targets angularly large, bring interactive content within "
    "reach where possible, and filter the input.</b> Interface elements "
    "sized reasonably for a monitor are frequently far too small in VR, and "
    "this is one of the most common failures in ported applications."]),
  ("ul", ["<b>Filter the pose.</b> A one-euro filter, or any "
          "speed-adaptive low-pass, removes hand tremor while adding "
          "negligible lag during deliberate motion. This is cheap and "
          "noticeably improves precision.",
          "<b>Snapping and magnetism.</b> Pull the ray toward valid targets, "
          "or snap a held object into a socket when it is close and roughly "
          "aligned. Users read this as the system being helpful rather than "
          "as imprecision being hidden.",
          "<b>Make hit volumes larger than visual volumes.</b> The user "
          "judges by what they see, so a generous collider costs nothing "
          "perceptually and measurably improves acquisition.",
          "<b>Design for a supported arm where you can</b> — elbows on "
          "a desk, or interactions brief enough that sustained reaching is "
          "not required. <b>Gorilla arm is a real constraint</b>, not a "
          "theoretical one.",
          "<b>Avoid tasks needing sub-centimetre precision</b> unless the "
          "user has a physical surface to brace against. Threading a virtual "
          "needle in mid-air is not a reasonable thing to ask."]),

  ("h1", "2 &nbsp; Grabbing"),
  ("callout", "Your hand will pass through the object",
   ["<b>There is nothing to stop it.</b> The virtual object is solid; the "
    "physical hand is moving through empty air and is constrained by "
    "nothing.",
    "<b>If the virtual hand tracks the real hand exactly, it penetrates "
    "geometry</b> — which Module 01 identified as the single most "
    "common break of presence, and the one users test for deliberately "
    "within the first minute.",
    "<b>If the virtual hand stops at the surface, it diverges from the real "
    "hand's position.</b> The user's proprioception says the hand is at one "
    "place and the display says another.",
    "<b>The divergence is the lesser evil, and it is the standard "
    "solution:</b> a physics-driven virtual hand that collides with the "
    "world and stops at surfaces, with the true tracked position either "
    "hidden entirely or shown as a faint ghost. <b>Users accept this "
    "readily</b> — far more readily than they accept a hand inside a "
    "table — and most do not consciously notice it."]),
  ("table", ["Approach", "Behaviour", "Appropriate for"],
   [["<b>Snap to a fixed pose</b>",
     "The object jumps to a predetermined position and orientation in the "
     "hand.",
     "<b>Tools and weapons</b>, where a predictable grip matters more than "
     "a natural one. A pistol should always be held the same way."],
    ["<b>Preserve the offset</b>",
     "The object maintains its pose relative to the hand at the moment of "
     "grabbing.",
     "<b>Natural for most objects.</b> Picking up a mug by its rim keeps it "
     "held by the rim."],
    ["<b>Physics joint</b>",
     "A spring or configurable joint connects the object to the hand, so "
     "the object is driven toward the hand rather than attached to it.",
     "<b>Heavy objects, and anything that should collide with the "
     "world.</b> The object can be blocked by a wall while the hand "
     "continues, which is what makes a held object feel like it has mass. "
     "<b>More work than it appears</b>, and it is what distinguishes a "
     "convincing object from a floating one."],
    ["<b>Two-handed</b>",
     "Both hands constrain the object — one gives position, the pair "
     "give orientation.",
     "Large objects, rifles, steering. Noticeably more precise for aiming "
     "than one hand."]],
   [0.19, 0.36, 0.45]),

  ("break",),
  ("h1", "3 &nbsp; Affordances"),
  ("callout", "Nobody reads instructions in VR",
   ["<b>Text is uncomfortable to read in a headset</b> (Module 02), the "
    "user is occupied looking around a new environment, and there is no "
    "manual to consult. Any instruction you write will be skipped.",
    "<b>So interactions must be discoverable from the objects "
    "themselves.</b> A grabbable object must look grabbable; a handle must "
    "read as a handle; a button must look pressable.",
    "<b>Highlight on proximity</b> is the simplest and most effective "
    "technique available: objects that visibly respond when a hand "
    "approaches teach their own interactivity, immediately and without "
    "words. If you implement one affordance technique, implement this one.",
    "<b>Use real-world forms.</b> A lever, a dial, a toggle switch, a "
    "doorknob, a drawer handle — people already know what to do with "
    "these, and that knowledge transfers completely and instantly into VR. "
    "<b>Inventing novel interaction metaphors is expensive</b> and almost "
    "never repays the cost."]),
  ("ul", ["<b>Visual feedback:</b> highlight on hover, a visible change on "
          "grab, an animation on release. This is the minimum, and alone it "
          "is thin.",
          "<b>Audio feedback:</b> a click on contact, a sound on grab, a "
          "thud on release. <b>Cheap and disproportionately effective</b> "
          "— a click when a virtual hand touches a virtual surface does "
          "a remarkable amount of work toward making the surface feel "
          "present.",
          "<b>Haptic feedback:</b> a short controller pulse on contact. The "
          "actuator is crude and cannot simulate texture or resistance, and "
          "it still substantially improves the sense of having touched "
          "something.",
          "<b>And the three compound.</b> Visual plus audio plus haptic "
          "together feel considerably more solid than the sum of their "
          "individual contributions — the brain is integrating across "
          "modalities, and agreement across modalities is what it treats as "
          "evidence of reality.",
          "<b>Because there is no force feedback</b>, these three are the "
          "entire vocabulary available for signalling contact. A hand that "
          "touches a wall and nothing happens is a hand that has touched "
          "nothing."]),

  ("h1", "4 &nbsp; Hand tracking and controllers"),
  ("table", ["", "Controllers", "Hand tracking"],
   [["Precision", "<b>High and consistent.</b>",
     "Lower, and it varies with hand pose and lighting."],
    ["Discrete input", "<b>Buttons, triggers, grips — unambiguous "
     "and plentiful.</b>",
     "<b>None.</b> Only gestures, which must be classified. See below."],
    ["Haptics", "<b>Yes.</b>", "<b>None at all.</b>"],
    ["Occlusion", "Tracked through occlusion by the controller's own IMU "
     "for a useful period.",
     "<b>Fails when the hand is hidden</b> — behind the body, behind "
     "the other hand, outside the camera field."],
    ["Learning", "A moment to learn which button does what.",
     "<b>Immediate.</b> People already have hands."],
    ["Fatigue", "Lower — there is something to hold and rest.",
     "Higher — nothing to grip, and hands must stay in the tracking "
     "volume."],
    ["Feels natural", "Less so.",
     "<b>Considerably more, when it works.</b>"]],
   [0.15, 0.41, 0.44]),
  ("p", "<b>Hand tracking demonstrates better and controllers work "
        "better</b>, which is an uncomfortable conclusion and a reliable "
        "one. A five-minute demonstration with hand tracking is magical; a "
        "two-hour application is markedly easier with controllers."),
  ("callout", "The missing button problem",
   ["<b>A controller provides an unambiguous binary input.</b> The trigger "
    "is pressed or it is not, the system knows which, and the user can feel "
    "which.",
    "<b>A hand provides nothing of the kind.</b> Pinch detection is a "
    "classifier operating on an estimated hand pose with a threshold, and "
    "like every classifier it has false positives and false negatives. "
    "Fingers that happen to come close produce a grab; a deliberate pinch at "
    "an awkward angle does not.",
    "<b>So every interaction must tolerate misdetection:</b> accidental "
    "grabs, failed grabs, and releases that the user intended but the system "
    "did not register. Designs that assume reliable discrete input will fail "
    "in ways that feel like the user's fault but are not.",
    "<b>And there is no haptic confirmation.</b> The user cannot feel "
    "whether their action registered, so visual and audio feedback must "
    "carry the entire load — which makes &sect;3's feedback discipline "
    "not merely desirable but structurally necessary."]),
 ],
 "resources": [
   ("LaValle &mdash; Virtual Reality, Chapter 10.2 (free)",
    "http://lavalle.pl/vr/",
    "Interaction mechanics and the research framing of manipulation in VR."),
   ("Meta &mdash; interaction and hand tracking design guidelines (free)",
    "https://developers.meta.com/horizon/resources/",
    "The practical rules, including hit volumes, gesture reliability, and "
    "the feedback recommendations of &sect;3."),
   ("Casiez et al. &mdash; 1€ Filter (free, with code)",
    "https://gery.casiez.net/1euro/",
    "The input filter of &sect;1. A page of code, immediately useful, and "
    "it works well."),
   ("Bowman et al. &mdash; 3D User Interfaces: Theory and Practice",
    "https://www.google.com/books/edition/_/MIDeAQAAIAAJ",
    "The standard text on 3D interaction. Library, not free, and the "
    "selection and manipulation taxonomy is worth knowing."),
 ],
 "exercises": [
   "Implement both direct manipulation and ray pointing, with a clean "
   "transition between them based on proximity. Test whether users ever "
   "become confused about which is active.",
   "Measure Fitts's law in VR: time selections of targets at several "
   "angular sizes and distances, and fit the model.",
   "Implement a one-euro filter on controller pose and measure the "
   "improvement in a precision task.",
   "Implement a hand that tracks exactly and one that stops at surfaces. "
   "Have six people use both and ask which felt wrong.",
   "Implement all four grab approaches from &sect;2 and compare them on the "
   "same object.",
   "Implement a physics-joint grab and demonstrate a held object colliding "
   "with a wall.",
   "Build an interaction with no instructions at all and watch a novice "
   "attempt it. Record every moment of confusion.",
   "Add visual, then audio, then haptic feedback to a single interaction, "
   "and have people rate solidity after each addition.",
   "Compare hand tracking and controllers on the same task, measuring "
   "completion time and error rate.",
   "Measure the false positive and false negative rate of pinch detection "
   "across several hand orientations.",
 ],
 "selfcheck": [
   "Compare direct manipulation and ray pointing on six axes.",
   "How does Fitts's law apply in VR, and what is the relevant measure of "
   "target size?",
   "Give five techniques for helping an unsupported hand.",
   "Why does the virtual hand penetrate objects, and what is the standard "
   "solution?",
   "Name four grab implementations and say what each suits.",
   "Why does nobody read instructions in VR, and what replaces them?",
   "Name the three feedback channels and say why they compound.",
   "Compare hand tracking and controllers on seven axes.",
   "What is the missing button problem, and what two consequences follow?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Rendering for VR",
 "subtitle": "Twice the pixels, half the time.",
 "question": "How do you render two eyes within the budget?",
 "outcomes": [
     "Apply stereo rendering optimisations and say what each saves.",
     "Explain foveated rendering, fixed and eye-tracked.",
     "Explain variable rate shading and where to apply it.",
     "Choose antialiasing appropriately for VR.",
     "Build a VR performance budget and defend it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two eyes, cheaply",
   "blurb": "Exploiting what the eyes share."},

  {"t": "table", "kicker": "Stereo", "title": "Stereo rendering techniques",
   "header": ["Technique", "How", "Saves"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Sequential", "Render twice, independently", "<b>Nothing — the baseline</b>"],
     ["<b>Instanced stereo</b>", "One draw call, instanced per eye", "<b>CPU draw calls; ~40% CPU</b>"],
     ["<b>Multiview</b>", "GPU renders both views from one submission", "<b>CPU and vertex work</b>"],
     ["Single-pass", "Both eyes in one wide render target", "Setup and state changes"],
   ],
   "footnote": "<b>Fragment work is never shared</b> — the two eyes "
               "genuinely see different pixels. Only setup and vertex work "
               "can be.",
   "note": "The 'fragment work cannot be shared' point bounds how much "
           "these techniques can possibly save."},

  {"t": "callout", "title": "What can and cannot be shared",
   "kind": "The limit on stereo optimisation",
   "body": ["<b>Fully shareable:</b> shadow map generation, lightmaps, "
            "culling (mostly), animation and skinning, physics, and all CPU "
            "simulation.",
            "<b>Partly shareable:</b> vertex processing — multiview "
            "transforms once and projects twice.",
            "<b>Not shareable:</b> fragment shading. The two eyes see "
            "different pixels, and that difference <i>is</i> stereo.",
            "<b>So the ceiling is bounded by your fragment cost.</b> A "
            "vertex-bound scene benefits enormously from multiview; a "
            "fragment-bound one barely at all — and most VR scenes are "
            "fragment-bound."]},

  {"t": "section", "label": "Part 2", "title": "Foveated rendering",
   "blurb": "Spending pixels where the eye can use them."},

  {"t": "two", "kicker": "Two kinds", "title": "Fixed and eye-tracked",
   "lh": "Fixed foveated",
   "l": ["Assume the user looks mostly forward.",
         "Reduce shading rate toward the edges.",
         "<b>No eye tracking required.</b>",
         ("Conservative — the fovea could be anywhere.", 1),
         "<b>Typical saving 20–40%.</b>"],
   "rh": "Eye-tracked foveated",
   "r": ["Follow the actual gaze.",
         "Full rate only at the real fovea.",
         "<b>Needs eye tracking with low latency.</b>",
         ("Aggressive — the fovea is known.", 1),
         "<b>Typical saving 50–70%.</b>"],
   "note": "The latency requirement for eye-tracked foveation is strict "
           "— saccades are fast and a late update is visible."},

  {"t": "callout", "title": "Foveated rendering must beat the saccade",
   "kind": "The hard requirement",
   "body": ["<b>A saccade takes 20–50 ms and can cover 20&deg;.</b> If "
            "the foveal region updates after the eye arrives, the user sees "
            "low-resolution content at the centre of vision.",
            "<b>Which is immediately obvious</b> — far more noticeable "
            "than uniformly lower resolution would be.",
            "<b>So the eye tracker's latency plus the rendering latency "
            "must fit inside the saccade</b>, which is demanding.",
            "<b>Saccadic suppression helps</b> — vision is substantially "
            "suppressed during a saccade, which buys some of the time back "
            "and is actively exploited."]},

  {"t": "bullets", "kicker": "VRS", "title": "Variable rate shading",
   "items": [
     "<b>Shade one value per 2×2 or 4×4 block of pixels</b> instead of "
     "per pixel, where detail is not needed.",
     "",
     "<b>Hardware support makes it nearly free</b> — it is a rasteriser "
     "feature, not a post-process.",
     "",
     "<b>Drive it by eccentricity</b> (foveation), by motion, or by "
     "material — a flat wall needs less shading rate than a detailed "
     "surface.",
     "",
     "<b>Geometry and depth remain full rate</b>, so edges stay sharp "
     "— which is why the artefacts are subtle.",
     "",
     "<b>It composes with everything else</b>, which makes it unusually "
     "easy to adopt.",
   ],
   "note": "VRS is the most practical of these techniques because the "
           "hardware does it and edges stay sharp."},

  {"t": "section", "label": "Part 3", "title": "Choices that differ from flat rendering",
   "blurb": "Where VR inverts the usual advice."},

  {"t": "table", "kicker": "Reversals", "title": "VR-specific rendering decisions",
   "header": ["Usual practice", "In VR"],
   "widths": [5.4, 6.7],
   "rows": [
     ["TAA is the default antialiasing", "<b>MSAA often wins</b> — TAA smears under constant head motion"],
     ["Deferred rendering for many lights", "<b>Forward+ often wins</b> — MSAA, bandwidth, transparency"],
     ["Motion blur adds realism", "<b>Never use it</b> (Module 02)"],
     ["Post-processing is cheap", "<b>Doubled, and bandwidth-bound</b>"],
     ["Dynamic resolution on demand", "<b>Essential, and must be smooth</b>"],
   ],
   "footnote": "Three of these reverse advice that is correct for flat "
               "rendering, which makes them easy to get wrong when porting.",
   "note": "The deferred/forward reversal is the one with the biggest "
           "architectural consequences."},

  {"t": "callout", "title": "Why forward rendering came back for VR",
   "kind": "The architectural reversal",
   "body": ["<b>MSAA works with forward rendering and not with "
            "deferred</b> — and VR wants MSAA (Module 02).",
            "<b>Deferred's G-buffer bandwidth is doubled</b> by stereo, and "
            "VR is frequently bandwidth-bound rather than shading-bound.",
            "<b>Transparency is awkward in deferred</b>, and VR content "
            "tends to have a lot of it.",
            "<b>Forward+ or clustered forward gets many lights without the "
            "G-buffer</b>, which is why several VR-focused renderers moved "
            "back. This is a genuine architectural decision, not a tuning "
            "one."]},

  {"t": "callout", "title": "Dynamic resolution is not optional",
   "kind": "The practical necessity",
   "body": ["<b>Content is not uniform.</b> Some views are cheap and some "
            "are expensive, and the user controls which they are looking "
            "at.",
            "<b>Fixed resolution means either wasting headroom or missing "
            "frames</b>, and missing frames is the one thing you cannot do "
            "(Module 01).",
            "<b>So scale the render target per frame</b> to hit the budget, "
            "and let quality vary instead of frame time.",
            "<b>Change it smoothly.</b> A sudden resolution change is "
            "visible as a pop; ramping over several frames is not. This is "
            "the detail implementations get wrong."]},

  {"t": "bullets", "kicker": "Budget", "title": "Building a VR performance budget",
   "items": [
     "<b>Start from the frame budget</b> — 11.1 ms at 90 Hz — and "
     "subtract the compositor's share.",
     "",
     "<b>Allocate explicitly:</b> so much for shadows, so much for opaque, "
     "so much for transparency, so much for post.",
     "",
     "<b>Leave 20% headroom.</b> The expensive view exists, and the user "
     "will find it.",
     "",
     "<b>Measure per eye and in the worst case</b>, not the average view.",
     "",
     "<b>Profile on the target hardware.</b> Standalone headsets are mobile "
     "GPUs with mobile thermal limits, and they throttle.",
   ],
   "footnote": "Thermal throttling on standalone hardware means a scene "
               "that passes for two minutes may fail after ten."},
 ],
 "takeaways": [
   "Instanced stereo and multiview share setup and vertex work; fragment "
   "work can never be shared, which bounds what they can save.",
   "Fixed foveated rendering assumes a forward gaze and saves 20–40%; "
   "eye-tracked foveation knows the gaze and saves 50–70%.",
   "Eye-tracked foveation must update faster than a saccade completes, or "
   "the user sees low resolution at the centre of vision.",
   "Variable rate shading reduces shading rate per block while keeping "
   "geometry and depth at full rate, so the artefacts stay subtle.",
   "VR reverses several defaults: MSAA over TAA, forward over deferred, and "
   "never motion blur.",
   "Dynamic resolution is necessary because the user chooses the view; ramp "
   "it smoothly or the change is visible.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Rendering two eyes"),
  ("table", ["Technique", "Mechanism", "What it saves"],
   [["<b>Sequential stereo</b>",
     "Render the scene twice, independently, once per eye.",
     "<b>Nothing.</b> The naive baseline, and roughly twice the cost of a "
     "single view."],
    ["<b>Instanced stereo</b>",
     "Issue one draw call with an instance count of two; a vertex shader "
     "selects the eye's view matrix by instance index.",
     "<b>CPU draw call submission</b> — commonly around 40% of CPU "
     "render time, which matters because VR is frequently CPU-bound."],
    ["<b>Multiview</b>",
     "A hardware and API feature: one submission, and the GPU produces both "
     "views, transforming each vertex once and projecting it twice.",
     "<b>CPU submission and a large share of vertex processing.</b> The "
     "best of the stereo techniques where it is supported."],
    ["<b>Single-pass / double-wide</b>",
     "Both eyes rendered into one wide render target with a viewport per "
     "eye.", "Render target switches and associated state changes."]],
   [0.18, 0.42, 0.40]),
  ("callout", "What can and cannot be shared",
   ["<b>Fully shareable between the eyes:</b> shadow map generation, "
    "lightmap and probe lookups, most culling, animation and skinning, "
    "particle simulation, physics, and every other CPU-side computation. "
    "None of this depends on which eye is being rendered.",
    "<b>Partly shareable:</b> vertex processing. Multiview transforms each "
    "vertex to world space once and then projects it twice, which recovers "
    "most of the duplicated work.",
    "<b>Not shareable at all:</b> fragment shading. The two eyes genuinely "
    "see different pixels of different surfaces at different angles, and "
    "<b>that difference is precisely what stereo is</b>. There is no "
    "legitimate way to share it.",
    "<b>So the achievable saving is bounded by how fragment-bound your "
    "scene is.</b> A vertex-heavy or draw-call-heavy scene benefits "
    "enormously from multiview; a fragment-bound one barely at all. <b>And "
    "most VR scenes are fragment-bound</b>, because the render targets are "
    "large and oversized for distortion (Module 04) — which is why "
    "&sect;2's techniques matter more than &sect;1's."]),

  ("h1", "2 &nbsp; Foveated rendering"),
  ("table", ["", "Fixed foveated", "Eye-tracked foveated"],
   [["Assumption", "The user looks mostly toward the centre of the display.",
     "<b>None</b> — the gaze is measured."],
    ["Method", "Reduce shading rate in concentric regions toward the edges.",
     "Full rate only in a small region around the measured gaze point."],
    ["Hardware", "<b>None beyond VRS support.</b>",
     "<b>Eye tracking, with low latency.</b>"],
    ["Aggressiveness", "Conservative — the fovea might be anywhere "
     "within the central region, so the full-rate area must be generous.",
     "Aggressive — the fovea's location is known to within a degree."],
    ["Typical saving", "<b>20–40%</b>", "<b>50–70%</b>"]],
   [0.17, 0.41, 0.42]),
  ("callout", "Foveated rendering must beat the saccade",
   ["<b>A saccade — a rapid eye movement between fixation points "
    "— takes 20 to 50 ms and can traverse 20 degrees or more.</b> They "
    "happen several times a second, continuously, without conscious "
    "awareness.",
    "<b>If the high-resolution region updates after the eye has arrived, "
    "the user sees low-resolution content at the centre of vision</b> "
    "— exactly where acuity is highest and the deficiency is most "
    "visible.",
    "<b>And that is far more noticeable than uniformly lower resolution "
    "would have been.</b> A brief blur at the fovea is conspicuous in a way "
    "that a permanently softer image is not, which means a foveation system "
    "that is too slow is worse than no foveation at all.",
    "<b>So the eye tracker's latency plus the rendering pipeline's latency "
    "must fit within the saccade</b>, which is a demanding constraint on "
    "both. <b>Saccadic suppression helps:</b> visual sensitivity is "
    "substantially reduced during the movement itself, which buys back some "
    "of the budget, and systems exploit it deliberately."]),
  ("ul", ["<b>Variable rate shading</b> computes one shaded value per "
          "2&times;2, 4&times;4, or larger block of pixels, instead of per "
          "pixel, in regions where full detail is not required.",
          "<b>Hardware support makes it nearly free.</b> It is a rasteriser "
          "feature rather than a post-process, so the saved work is genuinely "
          "never done rather than being done and discarded.",
          "<b>Drive it by eccentricity</b> (which is foveation), <b>by "
          "motion</b> (fast-moving content is perceptually blurred anyway), "
          "or <b>by material</b> (a flat painted wall needs less shading "
          "rate than a detailed normal-mapped surface).",
          "<b>Geometry and depth remain at full rate.</b> Only shading is "
          "coarsened, so silhouettes and edges stay sharp — which is "
          "why the artefacts are subtle and why VRS degrades gracefully "
          "where a straightforward resolution reduction does not.",
          "<b>It composes with everything else</b>, which makes it unusually "
          "easy to adopt incrementally: it can be enabled on part of a scene "
          "without restructuring the renderer."]),

  ("break",),
  ("h1", "3 &nbsp; Where VR reverses the usual advice"),
  ("table", ["Standard practice in flat rendering", "In VR"],
   [["<b>TAA is the default antialiasing.</b>",
     "<b>MSAA frequently wins.</b> TAA accumulates across frames and smears "
     "under head motion, which is continuous in VR, and the smear reads as "
     "latency (Module 02)."],
    ["<b>Deferred rendering, for many dynamic lights.</b>",
     "<b>Forward+ or clustered forward frequently wins.</b> See below."],
    ["<b>Motion blur adds cinematic realism.</b>",
     "<b>Never use it.</b> The display's low persistence exists to remove "
     "motion blur; adding it back increases perceived latency (Module 02)."],
    ["<b>Post-processing is comparatively cheap.</b>",
     "<b>Doubled by stereo, and VR is frequently bandwidth-bound</b> "
     "because of the oversized render targets. Full-screen passes cost more "
     "here than the instruction counts suggest."],
    ["<b>Dynamic resolution is a nice-to-have.</b>",
     "<b>Essential</b> — see below."]],
   [0.37, 0.63]),
  ("callout", "Why forward rendering returned for VR",
   ["<b>MSAA works with forward rendering and does not work with "
    "deferred</b> — and VR wants MSAA for the persistence reasons in "
    "Module 02. This alone is close to decisive.",
    "<b>The G-buffer's bandwidth cost is doubled by stereo.</b> A deferred "
    "renderer writes several full-screen targets per eye, at render "
    "resolutions already inflated 30 to 40% for distortion — and VR is "
    "frequently bandwidth-bound rather than arithmetic-bound, particularly "
    "on standalone hardware with mobile memory systems.",
    "<b>Transparency is awkward in deferred rendering</b> and requires a "
    "separate forward path anyway, and VR content — interfaces, "
    "effects, foliage — tends to have a great deal of it.",
    "<b>Forward+ and clustered forward supply many dynamic lights without a "
    "G-buffer</b>, which is why several VR-focused renderers moved back to "
    "forward architectures after the industry had largely settled on "
    "deferred. <b>This is a genuine architectural decision with wide "
    "consequences</b>, not a tuning switch, and it is one of the harder "
    "things to change later."]),
  ("callout", "Dynamic resolution is not optional",
   ["<b>Content cost is not uniform across views.</b> Facing a wall is "
    "cheap; facing the detailed vista with all the transparency is "
    "expensive. <b>And the user chooses which</b>, continuously, without "
    "warning (Module 01).",
    "<b>A fixed render resolution therefore means either leaving headroom "
    "unused in the cheap views or missing frames in the expensive ones</b> "
    "— and missing frames is the one thing that is genuinely "
    "unacceptable.",
    "<b>So scale the render target resolution per frame to hit the "
    "budget</b>, allowing image quality rather than frame time to be the "
    "variable. This is the correct trade in VR and the opposite of the usual "
    "instinct.",
    "<b>Change it smoothly.</b> A sudden resolution change is visible as a "
    "pop in sharpness; ramping over several frames is essentially "
    "undetectable. <b>This is the detail implementations most often get "
    "wrong</b> — the mechanism works and the transitions are "
    "distracting."]),
  ("ul", ["<b>Start from the frame budget</b> — 11.1 ms at 90 Hz "
          "— and subtract the compositor's share, leaving roughly 9 ms "
          "for the application.",
          "<b>Allocate explicitly</b>: a millisecond for shadows, so much "
          "for opaque geometry, so much for transparency, so much for "
          "post-processing. An unallocated budget is an overspent one.",
          "<b>Leave about 20% headroom.</b> The expensive view exists, and "
          "the user will find it within the first minute.",
          "<b>Measure per eye and in the worst case</b>, not the average. "
          "The average view's cost tells you nothing about whether you will "
          "drop frames.",
          "<b>Profile on the target hardware.</b> Standalone headsets are "
          "mobile GPUs with mobile thermal envelopes, and <b>they "
          "throttle</b> — a scene that holds its budget for two minutes "
          "may fail after ten, which is a failure mode that does not exist "
          "on a desktop GPU and is not visible in a short test."]),
 ],
 "resources": [
   ("Unreal Engine &mdash; XR performance and rendering documentation "
    "(free)",
    "https://dev.epicgames.com/documentation/en-us/unreal-engine/xr-development",
    "Instanced stereo, multiview, and the engine's VR rendering path. What "
    "you will actually configure."),
   ("Meta &mdash; fixed foveated rendering and performance guidelines "
    "(free)",
    "https://developers.meta.com/horizon/documentation/",
    "Fixed foveation on mobile hardware, with the measured savings of "
    "&sect;2."),
   ("Patney et al. &mdash; Towards Foveated Rendering for Gaze-Tracked "
    "Virtual Reality (free)",
    "https://research.nvidia.com/publication/2016-11_towards-foveated-rendering-gaze-tracked-virtual-reality",
    "The perceptual basis of foveated rendering and the saccade constraint "
    "in &sect;2."),
   ("NVIDIA &mdash; Variable Rate Shading documentation (free)",
    "https://developer.nvidia.com/vrworks",
    "VRS in practice, including the shading-rate image interface."),
 ],
 "exercises": [
   "Measure the cost of sequential stereo against instanced stereo in your "
   "engine. Report CPU and GPU time separately.",
   "Enable multiview and measure the vertex processing saved. Then make the "
   "scene fragment-bound and measure again — the benefit should "
   "largely disappear.",
   "Enable fixed foveated rendering at several strengths. Measure the saving "
   "and look for the boundary between shading rates.",
   "Implement variable rate shading driven by eccentricity and measure the "
   "GPU time saved at each strength.",
   "Drive VRS by motion instead and compare.",
   "Compare MSAA and TAA while turning your head quickly. Describe the "
   "difference during motion rather than when stationary.",
   "Implement dynamic resolution scaling with a smooth ramp. Then make the "
   "ramp instant and confirm the pop is visible.",
   "Build a written frame budget for a scene, allocate it by stage, and "
   "then measure whether the allocation held.",
   "Run a standalone headset for fifteen minutes and plot frame time. "
   "Identify where thermal throttling begins.",
 ],
 "selfcheck": [
   "Name four stereo rendering techniques and say what each saves.",
   "What can be shared between eyes, what cannot, and what bounds the "
   "saving?",
   "Compare fixed and eye-tracked foveation on assumption, hardware, and "
   "saving.",
   "Why must foveated rendering beat the saccade, and what helps?",
   "What does variable rate shading coarsen, what stays full rate, and why "
   "does that matter?",
   "Give five ways VR reverses standard rendering practice.",
   "Give three reasons forward rendering returned for VR.",
   "Why is dynamic resolution necessary, and what must be done smoothly?",
   "Give five rules for building a VR frame budget.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Spatial Audio",
 "subtitle": "The half of presence that gets a tenth of the effort.",
 "question": "Why does audio matter more in VR than anyone expects?",
 "outcomes": [
     "Explain how humans localise sound.",
     "Explain HRTFs and why they are personal.",
     "Explain the role of room acoustics in distance perception.",
     "Apply the audio techniques that most improve presence.",
     "Explain why audio is a disproportionate return on effort.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Localisation",
   "blurb": "How two ears locate a point in three dimensions."},

  {"t": "table", "kicker": "Cues", "title": "How humans localise sound",
   "header": ["Cue", "Means", "Resolves"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["<b>ITD</b>", "Interaural time difference", "<b>Left/right, below ~1.5 kHz</b>"],
     ["<b>ILD</b>", "Interaural level difference", "<b>Left/right, above ~1.5 kHz</b>"],
     ["<b>Spectral (HRTF)</b>", "Filtering by head, pinna, torso", "<b>Up/down, front/back</b>"],
     ["Head movement", "How cues change as you turn", "<b>Resolves ambiguity</b>"],
     ["Reverberation", "Direct-to-reverberant ratio", "<b>Distance</b>"],
   ],
   "footnote": "<b>ITD and ILD alone leave a 'cone of confusion'</b> "
               "— front and back, up and down are ambiguous without "
               "spectral cues.",
   "note": "The cone of confusion is why simple stereo panning sounds "
           "inside your head rather than in the world."},

  {"t": "callout", "title": "The pinna is why you can tell up from down",
   "kind": "Where HRTFs come from",
   "body": ["<b>Sound arriving from different directions reflects "
            "differently off the folds of your outer ear</b>, your head, and "
            "your shoulders.",
            "<b>This imposes a direction-dependent filter</b> — "
            "reinforcing some frequencies and cancelling others, "
            "differently for every direction.",
            "<b>The brain has learned your particular filter</b> over a "
            "lifetime, and uses it to resolve elevation and front/back.",
            "<b>A head-related transfer function is a measurement of that "
            "filter.</b> Convolving a sound with the right HRTF places it "
            "convincingly in space over headphones."]},

  {"t": "callout", "title": "HRTFs are personal, and generic ones are used anyway",
   "kind": "The practical compromise",
   "body": ["<b>Your HRTF depends on the shape of your ears, head, and "
            "shoulders</b>, which are as individual as fingerprints.",
            "<b>Measuring one properly requires an anechoic chamber</b> and "
            "a few hours per person.",
            "<b>So generic HRTFs are used</b> — measured from a dummy head "
            "or averaged across people — and they work reasonably for "
            "most listeners.",
            "<b>The failure mode is elevation and front/back confusion</b>: "
            "sounds that should be in front appear behind. <b>Head movement "
            "largely rescues it</b>, which is why VR audio works better "
            "than static binaural audio."]},

  {"t": "section", "label": "Part 2", "title": "Space",
   "blurb": "Why a room sounds like a room."},

  {"t": "callout", "title": "Reverberation is how you hear distance and size",
   "kind": "The underrated cue",
   "body": ["<b>Direct sound tells you the direction. Reflections tell you "
            "the room</b> — its size, its materials, and your distance "
            "from the source.",
            "<b>The direct-to-reverberant ratio is the primary distance "
            "cue.</b> A distant source is mostly reverberation; a near one "
            "is mostly direct.",
            "<b>Early reflections (under ~80 ms) convey room geometry</b> "
            "— the first few bounces say how big the space is and what it "
            "is made of.",
            "<b>Late reverberation conveys the overall character.</b> "
            "Together they are why a cathedral and a cupboard sound "
            "unmistakably different even with your eyes shut."]},

  {"t": "bullets", "kicker": "Implementation", "title": "Making a space sound right",
   "items": [
     "<b>Per-source HRTF spatialisation</b> for the direct path. The "
     "baseline, and every audio engine provides it.",
     "",
     "<b>Early reflections from the actual geometry</b> — image-source "
     "or ray-traced. This is what makes a room sound like <i>that</i> room.",
     "",
     "<b>A reverb matched to the space</b>, varying by room, with smooth "
     "transitions between zones.",
     "",
     "<b>Occlusion and obstruction:</b> a sound behind a wall should be "
     "muffled, not merely quieter. Low-pass filtering is most of it.",
     "",
     "<b>Distance attenuation with air absorption</b> — distant sounds "
     "lose high frequencies, not just volume.",
   ],
   "note": "The occlusion low-pass is cheap and is the single most "
           "noticeable improvement after basic spatialisation."},

  {"t": "section", "label": "Part 3", "title": "Why it matters so much",
   "blurb": "The disproportionate return."},

  {"t": "callout", "title": "Audio is 360&deg;, and vision is not",
   "kind": "The structural argument",
   "body": ["<b>The user sees about 110&deg; and hears everything.</b> "
            "Audio is the only sense covering the whole sphere.",
            "<b>So it is how a space feels inhabited</b> — things behind "
            "you, above you, and out of sight exist because you hear them.",
            "<b>And it directs attention without taking control</b> "
            "(Module 01). A sound to the left makes people look left, "
            "voluntarily.",
            "<b>It is therefore the primary tool for guiding a user</b> in "
            "a medium where you cannot cut, frame, or point the camera."]},

  {"t": "bullets", "kicker": "Evidence", "title": "What good audio buys",
   "items": [
     "<b>Measurably increased presence.</b> Studies consistently find "
     "spatial audio raises presence ratings more than equivalent visual "
     "improvements.",
     "",
     "<b>Perceived visual quality rises.</b> Good audio makes people rate "
     "the <i>graphics</i> higher, which is a robust and slightly absurd "
     "finding.",
     "",
     "<b>Reduced sickness</b> in some studies — plausibly through "
     "providing a stable reference frame (Module 07).",
     "",
     "<b>Better spatial understanding</b> of the environment.",
     "",
     "<b>For a fraction of the engineering cost of the graphics.</b>",
   ],
   "footnote": "<b>Audio is the highest return per unit of effort in VR</b> "
               "and is routinely the last thing anyone does.",
   "note": "The 'better audio makes graphics look better' finding is worth "
           "stating — it is real and it is persuasive to sceptics."},

  {"t": "callout", "title": "Audio must be head-tracked, with low latency",
   "kind": "The requirement that is easy to miss",
   "body": ["<b>When the head turns, the sound field must stay fixed in the "
            "world</b> — exactly as the visuals do.",
            "<b>If it rotates with the head, sounds are locked to you</b>, "
            "which destroys the illusion completely and is immediately "
            "obvious.",
            "<b>Audio latency budget is tighter than people assume</b> "
            "— perceptible above roughly 30 ms, and audio buffers are "
            "often sized generously by default.",
            "<b>And audio-visual synchrony matters:</b> a sound arriving "
            "noticeably after its visual cause breaks the association "
            "between them."]},
 ],
 "takeaways": [
   "ITD and ILD resolve left and right; spectral filtering by the pinna "
   "resolves up/down and front/back, which is what an HRTF captures.",
   "HRTFs are as individual as ear shape, generic ones are used anyway, and "
   "head movement rescues most of the resulting confusion.",
   "Reverberation carries distance and room size; the direct-to-reverberant "
   "ratio is the primary distance cue.",
   "Early reflections convey geometry and materials; late reverberation "
   "conveys overall character.",
   "Audio covers the full sphere while vision covers 110&deg;, so it is how "
   "a space feels inhabited and the main way to direct attention without "
   "taking control.",
   "Good audio raises presence more than equivalent visual work, and "
   "measurably raises how highly people rate the graphics.",
 ],
 "notes": [
  ("h1", "1 &nbsp; How humans localise sound"),
  ("table", ["Cue", "Mechanism", "What it resolves"],
   [["<b>Interaural time difference (ITD)</b>",
     "Sound from the left reaches the left ear fractionally earlier — "
     "up to about 0.7 ms.",
     "<b>Left and right</b>, for frequencies below roughly 1.5 kHz, where "
     "the wavelength exceeds the head's width and phase is unambiguous."],
    ["<b>Interaural level difference (ILD)</b>",
     "The head shadows the far ear, reducing the level there.",
     "<b>Left and right</b>, for frequencies above roughly 1.5 kHz, where "
     "the head is large enough relative to the wavelength to cast an "
     "acoustic shadow."],
    ["<b>Spectral cues (the HRTF)</b>",
     "Direction-dependent filtering by the pinna, head, and torso.",
     "<b>Up and down, front and back.</b> &sect;1.1."],
    ["<b>Head movement</b>",
     "How the above cues change as the head turns.",
     "<b>Resolves ambiguity</b> — a sound in front and one behind "
     "produce opposite changes when you turn, so a small movement "
     "disambiguates them immediately."],
    ["<b>Reverberation</b>", "The ratio of direct to reflected energy.",
     "<b>Distance</b>, and the size and material of the space. &sect;2."]],
   [0.23, 0.35, 0.42]),
  ("p", "<b>ITD and ILD alone leave a 'cone of confusion'.</b> For any given "
        "pair of time and level differences there is a whole cone of "
        "directions producing them — front and back, up and down are "
        "indistinguishable. <b>This is why naive stereo panning sounds like "
        "it is inside your head</b> rather than out in the world: the cues "
        "are present but incomplete, and the brain declines to place the "
        "sound externally."),
  ("callout", "The pinna is why you can tell up from down",
   ["<b>Sound arriving from different directions reflects and diffracts "
    "differently off the folds of the outer ear, the head, and the "
    "shoulders.</b> The pinna's convolutions are not decorative; they are a "
    "direction-encoding filter.",
    "<b>This imposes a direction-dependent frequency response</b> — "
    "certain frequencies reinforced, others notched out, with the pattern "
    "varying continuously with direction. A sound from above has a different "
    "spectral signature from the same sound in front.",
    "<b>The brain has learned your particular filter</b> over a lifetime of "
    "hearing things whose positions it could verify, and uses it to resolve "
    "elevation and front/back — the dimensions ITD and ILD cannot "
    "reach.",
    "<b>A head-related transfer function is a measurement of that "
    "filter</b>, as a function of direction. Convolving a monophonic sound "
    "with the appropriate HRTF for a given direction places it convincingly "
    "in space over headphones, which is the whole basis of VR audio."]),
  ("callout", "HRTFs are personal, and generic ones are used anyway",
   ["<b>Your HRTF is determined by the shape of your ears, head, and "
    "shoulders</b>, which vary as much between people as fingerprints do. "
    "Pinna shape in particular is highly individual.",
    "<b>Measuring one properly requires an anechoic chamber</b>, a speaker "
    "array or a moving source, microphones in the ear canals, and a few "
    "hours of the subject's time. This is not going to happen for your "
    "users.",
    "<b>So generic HRTFs are used</b> — measured from a dummy head, or "
    "averaged across a population, with some systems offering a small set to "
    "choose between or fitting one from a photograph of the ear. They work "
    "reasonably well for most listeners.",
    "<b>The characteristic failure is elevation error and front/back "
    "confusion:</b> a sound that should be in front is perceived behind, or "
    "a sound overhead is heard at ear level. <b>Head movement largely "
    "rescues it</b> — the cues change in opposite ways for front and "
    "back, so a small turn resolves the ambiguity. <b>Which is precisely why "
    "VR audio works better than static binaural recordings</b>: the listener "
    "moves, continuously, and every movement disambiguates."]),

  ("h1", "2 &nbsp; Room acoustics"),
  ("callout", "Reverberation is how you hear distance and size",
   ["<b>The direct sound tells you the direction. The reflections tell you "
    "the room</b> — how large it is, what it is made of, and how far "
    "away the source is.",
    "<b>The direct-to-reverberant ratio is the primary distance cue.</b> A "
    "nearby source is dominated by its direct sound; a distant one is "
    "dominated by reverberation, because the direct path has attenuated "
    "while the reflected energy in the room has not. <b>Loudness alone is a "
    "poor distance cue</b> — a quiet sound nearby and a loud sound far "
    "away have the same level — and this ratio is what disambiguates "
    "them.",
    "<b>Early reflections, within roughly the first 80 ms, convey "
    "geometry.</b> The first few bounces arrive from specific directions "
    "with specific delays, and they encode the size of the space and the "
    "materials of its surfaces.",
    "<b>Late reverberation conveys overall character</b> — the "
    "decaying diffuse tail. Together, early and late reverberation are why a "
    "cathedral and a cupboard are unmistakably different with your eyes "
    "closed, before anyone has said a word."]),
  ("ul", ["<b>Per-source HRTF spatialisation of the direct path.</b> The "
          "baseline, and every modern audio engine provides it. Without it "
          "nothing else matters.",
          "<b>Early reflections computed from the actual geometry</b> "
          "— by the image-source method for simple rooms, or by ray "
          "tracing for complex ones. <b>This is what makes a room sound like "
          "<i>that</i> room</b> rather than like a generic room-shaped "
          "reverb, and it is the step that most distinguishes convincing VR "
          "audio from adequate VR audio.",
          "<b>A reverb matched to the space</b>, varying between rooms, with "
          "smooth interpolation as the listener moves between zones. An "
          "abrupt reverb change at a doorway is as jarring as a visual pop.",
          "<b>Occlusion and obstruction.</b> A sound behind a wall should be "
          "<i>muffled</i>, not merely quieter — walls attenuate high "
          "frequencies far more than low ones. <b>A simple low-pass filter "
          "is most of the effect</b>, it is cheap, and it is the single most "
          "noticeable improvement available after basic spatialisation.",
          "<b>Distance attenuation with air absorption.</b> Distant sounds "
          "lose high frequencies as well as level, which is why a far-off "
          "voice sounds dull as well as quiet."]),

  ("break",),
  ("h1", "3 &nbsp; Why audio matters disproportionately"),
  ("callout", "Audio covers the whole sphere; vision covers 110 degrees",
   ["<b>The user sees roughly 110 degrees and hears everything.</b> Audio is "
    "the only sense in a headset that covers the full sphere, continuously, "
    "without the user having to orient toward anything.",
    "<b>So audio is how a space feels inhabited.</b> Things behind you, "
    "above you, around a corner, and out of sight exist because you can hear "
    "them. A visually detailed room with no sound behind the listener feels "
    "like a diorama; the same room with footsteps and distant activity feels "
    "like a place.",
    "<b>And it directs attention without taking control</b> — which "
    "Module 01 identified as the central design problem of a medium where "
    "you cannot cut or frame. A sound from the left makes people look left, "
    "voluntarily and immediately, and they experience it as their own "
    "choice.",
    "<b>It is therefore the primary tool for guiding a user</b> through an "
    "experience, and the one that most reliably works without breaking "
    "presence."]),
  ("ul", ["<b>Measurably increased presence.</b> Studies consistently find "
          "that adding spatial audio raises presence ratings more than "
          "comparable investment in visual fidelity does.",
          "<b>Perceived visual quality rises.</b> Good audio makes people "
          "rate the <i>graphics</i> more highly — a robust, "
          "well-replicated, and slightly absurd finding that is worth "
          "knowing when arguing for audio budget.",
          "<b>Reduced sickness in some studies</b>, plausibly because a "
          "stable, world-locked sound field acts as a reference frame "
          "consistent with the vestibular signal (Module 07).",
          "<b>Better spatial understanding.</b> Users build more accurate "
          "mental maps of environments with good spatial audio.",
          "<b>And all of it for a small fraction of the engineering cost of "
          "the graphics.</b> <b>Audio is the highest return per unit of "
          "effort available in VR</b>, and it is routinely the last thing "
          "anyone does, assigned to whoever is free in the final week."]),
  ("callout", "Audio must be head-tracked, with low latency",
   ["<b>When the head turns, the sound field must remain fixed in the "
    "world</b> — exactly as the visual scene does. A sound source to "
    "the user's left must move to in front of them when they turn left.",
    "<b>If the sound field rotates with the head, every source is locked to "
    "the listener</b>, which destroys the spatial illusion completely. It is "
    "immediately obvious once you know to listen for it, and it is a common "
    "bug in applications where the audio engine was not informed of the head "
    "pose.",
    "<b>The audio latency budget is tighter than people assume.</b> "
    "Head-tracked audio lag becomes perceptible above roughly 30 ms, and "
    "<b>audio buffers are frequently sized generously by default</b> because "
    "flat applications have no reason to care — so this is a setting "
    "that must be checked rather than assumed.",
    "<b>And audio-visual synchrony matters.</b> A sound arriving "
    "noticeably after its visible cause breaks the perceptual association "
    "between them, and the object stops being the thing that made the "
    "sound."]),
 ],
 "resources": [
   ("Meta &mdash; Audio design and spatialisation documentation (free)",
    "https://developers.meta.com/horizon/documentation/",
    "Practical VR audio: HRTF spatialisation, reverb zones, occlusion, and "
    "the latency requirements of &sect;3."),
   ("Steam Audio documentation (free, with SDK)",
    "https://valvesoftware.github.io/steam-audio/",
    "Geometry-based early reflections and occlusion — &sect;2's "
    "implementation, free and usable in both major engines."),
   ("Begault &mdash; 3-D Sound for Virtual Reality and Multimedia (NASA, "
    "free)",
    "https://ntrs.nasa.gov/citations/20010044352",
    "The foundational text on binaural audio and HRTFs, free from NASA. "
    "Thorough on &sect;1."),
   ("SOFA HRTF databases (free)",
    "https://www.sofaconventions.org/",
    "Measured HRTF sets in a standard format, including several public "
    "databases. Useful for experimenting with individual variation."),
 ],
 "exercises": [
   "Listen to a sound spatialised by simple stereo panning and by HRTF "
   "convolution. Describe where each appears to be.",
   "Find your own front/back confusion: have a spatialised sound placed "
   "directly in front and directly behind, without visuals, and try to "
   "distinguish them. Then allow head movement and repeat.",
   "Try three different generic HRTFs from a public database and report "
   "which localises best for you.",
   "Implement direct-to-reverberant ratio as a distance cue and verify that "
   "listeners can judge distance without level changes.",
   "Implement early reflections by the image-source method for a simple "
   "rectangular room and compare against a generic reverb.",
   "Add a low-pass occlusion filter for sounds behind walls and measure how "
   "much it improves the sense of the space.",
   "<b>Break head tracking in the audio</b> — rotate the sound field "
   "with the head — and confirm how obvious it is.",
   "Measure your audio pipeline's latency and compare against the 30 ms "
   "threshold.",
   "Show the same VR scene to six people with and without spatial audio, and "
   "ask them to rate the <i>graphics</i>. Report whether the finding in "
   "&sect;3 replicates.",
 ],
 "selfcheck": [
   "Name five localisation cues and say what each resolves.",
   "What is the cone of confusion, and why does stereo panning sound "
   "internal?",
   "What does the pinna do, and what is an HRTF?",
   "Why are generic HRTFs acceptable, and what rescues their failure mode?",
   "What is the primary distance cue, and why is loudness insufficient?",
   "Distinguish early reflections from late reverberation.",
   "Give five elements of a convincing spatial audio implementation.",
   "Why does audio matter disproportionately in VR? Give the structural "
   "argument.",
   "Name four measured benefits of good VR audio.",
   "What must be true of head tracking in audio, and what is the latency "
   "threshold?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Augmented Reality and Passthrough",
 "subtitle": "Registering the virtual to the real.",
 "question": "What changes when the real world is still visible?",
 "outcomes": [
     "Compare optical and video see-through.",
     "Explain registration and why it is AR's hard problem.",
     "Explain the occlusion problem and the approaches to it.",
     "Explain lighting estimation and why it matters.",
     "Identify the AR-specific interaction and social issues.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two kinds of see-through",
   "blurb": "Look through glass, or look at a camera feed."},

  {"t": "two", "kicker": "Approaches", "title": "Optical and video",
   "lh": "Optical see-through",
   "l": ["Transparent combiner; you see the real world directly.",
         "<b>Real world has zero latency</b> and full resolution.",
         "<b>Cannot render black</b> — only add light.",
         ("So no true occlusion of real objects.", 1),
         "Limited field of view; the classic AR glasses problem."],
   "rh": "Video see-through (passthrough)",
   "r": ["Cameras capture the world; the display shows the composite.",
         "<b>Real world has latency</b> and camera-limited quality.",
         "<b>Can render anything</b>, including full occlusion.",
         ("Complete control over the composite.", 1),
         "What current headsets do, and it works surprisingly well."],
   "note": "The 'cannot render black' limitation of optical see-through is "
           "fundamental and is why passthrough won for now."},

  {"t": "callout", "title": "Optical see-through cannot render black",
   "kind": "The fundamental limitation",
   "body": ["<b>A combiner adds light to the scene.</b> It cannot "
            "subtract.",
            "<b>So a virtual object can only ever be brighter than what is "
            "behind it</b> — it is additive, like a reflection in a "
            "window.",
            "<b>Dark virtual objects are impossible</b>, and virtual "
            "objects are always somewhat transparent.",
            "<b>Which means a virtual object can never properly occlude a "
            "real one.</b> Occlusion is the strongest depth cue (Module 02), "
            "so this is a deep problem and not a quality issue."]},

  {"t": "section", "label": "Part 2", "title": "Registration",
   "blurb": "AR's central problem."},

  {"t": "callout", "title": "Registration error is obvious in a way VR error is not",
   "kind": "Why AR is harder",
   "body": ["<b>In VR there is no reference.</b> If the whole world is 2 cm "
            "off, nothing reveals it.",
            "<b>In AR the real world is right there</b>, and a virtual "
            "object that should sit on a real table either does or visibly "
            "does not.",
            "<b>Sub-centimetre accuracy and sub-degree orientation are "
            "needed</b> for objects at arm's length to look attached.",
            "<b>And latency becomes registration error</b> — any lag "
            "makes virtual content swim relative to the real world during "
            "head motion, which is the characteristic AR artefact."]},

  {"t": "bullets", "kicker": "Requirements", "title": "What registration demands",
   "items": [
     "<b>Accurate tracking</b> — the same problem as Module 05, with a "
     "tighter tolerance.",
     "",
     "<b>Scene understanding:</b> where are the planes, the walls, the "
     "objects? Virtual content must relate to real geometry.",
     "",
     "<b>Low latency specifically for the virtual layer</b>, which must "
     "stay locked to a real world that has its own latency.",
     "",
     "<b>Camera and display calibration</b>, so what the cameras see maps "
     "correctly to what the eye sees.",
     "",
     "<b>Persistence across sessions</b> — content placed yesterday "
     "should still be there, which requires relocalisation.",
   ],
   "note": "Persistent anchors are what makes AR useful rather than a demo, "
           "and they are harder than they look."},

  {"t": "callout", "title": "Occlusion: the virtual must go behind the real",
   "kind": "The hardest rendering problem in AR",
   "body": ["<b>A virtual ball rolled under a real table must disappear "
            "under it.</b> If it draws on top, the illusion fails "
            "immediately.",
            "<b>This requires knowing the depth of the real world</b>, per "
            "pixel, in real time.",
            "<b>Approaches:</b> a depth sensor, stereo from the passthrough "
            "cameras, or learned monocular depth — each with error at "
            "exactly the edges where it matters most.",
            "<b>Hands are the critical case.</b> A user's real hand in "
            "front of a virtual object must occlude it, and hand "
            "segmentation is therefore given special treatment in every "
            "system."]},

  {"t": "section", "label": "Part 3", "title": "Appearance",
   "blurb": "Making the virtual belong."},

  {"t": "bullets", "kicker": "Lighting", "title": "Lighting estimation",
   "items": [
     "<b>A virtual object lit differently from the room looks pasted "
     "on</b> — more obviously than it would in a fully virtual scene.",
     "",
     "<b>Estimate ambient light colour and intensity</b> from the camera "
     "feed. Cheap and immediately effective.",
     "",
     "<b>Estimate the dominant light direction</b>, so shadows fall the "
     "right way.",
     "",
     "<b>Build an environment map</b> from the passthrough cameras for "
     "reflections.",
     "",
     "<b>And cast shadows onto the real world</b> — a contact shadow "
     "under a virtual object does more than any other single cue.",
   ],
   "footnote": "The contact shadow is the cheapest and most effective "
               "technique here, exactly as in Module 02."},

  {"t": "callout", "title": "Passthrough quality is the current limit",
   "kind": "An honest assessment",
   "body": ["<b>Passthrough cameras are low resolution, noisy in dim light, "
            "and have limited dynamic range</b> compared with the eye.",
            "<b>And they are not at your eyes</b>, so the view must be "
            "reprojected to the correct viewpoint — which introduces "
            "distortion and artefacts at depth discontinuities.",
            "<b>The result is a world that is usable and visibly "
            "degraded.</b> Reading text through passthrough is "
            "uncomfortable; recognising faces is fine.",
            "<b>This is improving quickly</b>, and it is currently the "
            "binding constraint on how long people will wear a passthrough "
            "headset."]},

  {"t": "bullets", "kicker": "Social", "title": "Problems VR does not have",
   "items": [
     "<b>Other people are present.</b> They can see you gesturing at "
     "nothing, and they cannot see what you see.",
     "",
     "<b>Cameras in social spaces</b> raise privacy questions that a "
     "closed headset does not.",
     "",
     "<b>Your attention is divided</b> between the real and the virtual, "
     "with real safety consequences.",
     "",
     "<b>Content must respect the real environment</b> — a virtual "
     "window on a real wall is fine; one floating in a doorway is not.",
     "",
     "<b>And the device is worn in public</b>, which is a design "
     "constraint with a poor track record.",
   ],
   "note": "The social dimension is genuinely why AR adoption has lagged "
           "the technology, and it is worth naming."},
 ],
 "takeaways": [
   "Optical see-through shows the real world directly with zero latency and "
   "cannot render black; video passthrough can composite anything and adds "
   "latency to reality.",
   "Because a combiner only adds light, optical see-through can never "
   "properly occlude a real object — and occlusion is the strongest "
   "depth cue.",
   "Registration error is obvious in AR because the real world is the "
   "reference, so tolerances are sub-centimetre and latency becomes visible "
   "swimming.",
   "Occluding virtual content behind real geometry requires per-pixel "
   "real-world depth in real time, and hands are the critical case.",
   "Lighting estimation makes virtual objects belong; a contact shadow is "
   "the cheapest and most effective single cue.",
   "Passthrough image quality is the current binding constraint, and AR has "
   "social and privacy problems that VR does not.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two kinds of see-through"),
  ("table", ["", "Optical see-through", "Video see-through (passthrough)"],
   [["Method", "A transparent combiner — a half-silvered mirror or "
     "waveguide — through which the real world is seen directly, with "
     "virtual light added.",
     "Cameras capture the real world; the display shows a composite of "
     "camera feed and virtual content."],
    ["Real world latency", "<b>Zero.</b> It is light from the actual "
     "world.",
     "<b>Nonzero</b> — capture, processing, and display, typically "
     "tens of milliseconds."],
    ["Real world quality", "<b>Full acuity and dynamic range.</b>",
     "Limited by the cameras — resolution, noise, dynamic range."],
    ["Virtual content", "<b>Additive only.</b> See below.",
     "<b>Anything, including pure black and full occlusion.</b>"],
    ["Field of view", "Typically narrow — the classic limitation of "
     "AR glasses, and difficult to widen.",
     "As wide as the headset's display."],
    ["Current status", "Research and specialist devices.",
     "<b>What current consumer headsets do</b>, and it works considerably "
     "better than most people expect."]],
   [0.17, 0.41, 0.42]),
  ("callout", "Optical see-through cannot render black",
   ["<b>A combiner adds light to what is already reaching the eye. It has "
    "no mechanism for subtracting light.</b>",
    "<b>So a virtual object can only ever be brighter than the real "
    "background behind it.</b> The effect is exactly like a reflection in a "
    "window: you see the reflected image superimposed on the view through "
    "the glass, and the reflection is always translucent.",
    "<b>Dark virtual objects are therefore impossible</b>, and all virtual "
    "content is somewhat transparent, with real detail showing through.",
    "<b>Which means a virtual object can never properly occlude a real "
    "one.</b> Module 02 established that occlusion is the strongest depth "
    "cue the visual system has — so this is a fundamental limitation "
    "on the realism achievable, not an image-quality issue that better "
    "components will resolve. <b>It is the main reason video passthrough "
    "has won for the present generation</b>, despite its own disadvantages."]),

  ("h1", "2 &nbsp; Registration"),
  ("callout", "Registration error is obvious in AR and invisible in VR",
   ["<b>In VR there is no external reference.</b> If the entire virtual "
    "world is positioned two centimetres from where it should be, nothing "
    "reveals it — the user has nothing to compare against, and the "
    "error is simply where the world is.",
    "<b>In AR the real world is right there, continuously, as a "
    "reference.</b> A virtual object that should be resting on a real table "
    "either is resting on it or is visibly floating above or sinking into "
    "it.",
    "<b>The tolerances are correspondingly tight:</b> sub-centimetre "
    "positional accuracy and sub-degree orientation accuracy are needed for "
    "content at arm's length to read as genuinely attached to the world.",
    "<b>And latency converts directly into registration error.</b> Any lag "
    "between head motion and the virtual layer's update makes virtual "
    "content swim relative to the real world — and because the real "
    "world is the reference, the swimming is immediately visible. <b>This is "
    "the characteristic AR artefact</b>, and it is why AR's latency "
    "requirements are even tighter than VR's."]),
  ("ul", ["<b>Accurate tracking</b> — the problem of Module 05, with a "
          "substantially tighter tolerance and no opportunity to hide error.",
          "<b>Scene understanding.</b> Where are the floors, walls, tables, "
          "and objects? Virtual content that must relate to real geometry "
          "requires that geometry to be known, which means plane detection, "
          "mesh reconstruction, and object recognition.",
          "<b>Low latency for the virtual layer specifically</b>, which must "
          "stay locked to a real world that — in video passthrough "
          "— has a latency of its own. Matching the two matters as much "
          "as minimising either.",
          "<b>Camera and display calibration</b>, so that what the cameras "
          "capture maps correctly onto what the eye sees through the optics. "
          "Errors here produce a systematic offset that no amount of "
          "tracking accuracy corrects.",
          "<b>Persistence across sessions.</b> Content placed on a real "
          "table yesterday should still be on that table today, which "
          "requires recognising the space again — relocalisation "
          "against a saved map. <b>Persistent anchors are what make AR "
          "useful rather than a demonstration</b>, and they are considerably "
          "harder than they appear."]),
  ("callout", "Occlusion: the virtual must go behind the real",
   ["<b>A virtual ball rolled under a real table must disappear under "
    "it.</b> If it continues to draw on top of the table, the illusion that "
    "it occupies the room fails instantly and completely.",
    "<b>This requires knowing the depth of the real world, per pixel, in "
    "real time</b> — a considerably harder requirement than knowing "
    "where the planes are.",
    "<b>The approaches each fail where it matters.</b> A dedicated depth "
    "sensor is accurate and has limited range and resolution. Stereo from "
    "the passthrough cameras works and is unreliable on textureless surfaces. "
    "Learned monocular depth is improving quickly and is least accurate at "
    "depth discontinuities — which are precisely the edges where "
    "occlusion is decided.",
    "<b>Hands are the critical case.</b> A user's real hand passing in front "
    "of a virtual object must occlude it, and users test this constantly and "
    "unconsciously. <b>Hand segmentation is therefore given dedicated "
    "treatment in every AR system</b>, separate from general depth "
    "estimation, because getting it right matters more than getting "
    "everything else right."]),

  ("break",),
  ("h1", "3 &nbsp; Making virtual content belong"),
  ("ul", ["<b>A virtual object lit differently from the room it sits in "
          "looks pasted on</b> — and far more obviously than the same "
          "inconsistency would in a fully virtual scene, because the real "
          "lighting is right there for comparison.",
          "<b>Estimate ambient light colour and intensity</b> from the "
          "camera feed. This is cheap, requires no scene understanding, and "
          "is immediately effective — a virtual object that is warm in "
          "a warm room and cool in a cool one already looks substantially "
          "more present.",
          "<b>Estimate the dominant light direction</b>, so that shading and "
          "shadows fall consistently with the real lighting. Errors here are "
          "noticed even by people who cannot say what is wrong.",
          "<b>Build an environment map from the passthrough cameras</b> for "
          "reflections on glossy virtual surfaces. A virtual chrome object "
          "reflecting the actual room is strikingly convincing.",
          "<b>And cast shadows onto the real world.</b> <b>A contact shadow "
          "beneath a virtual object does more to make it appear to rest on a "
          "real surface than any other single technique</b> — exactly "
          "as Module 02 said of depth cues generally, and it is cheap."]),
  ("callout", "Passthrough image quality is the current binding constraint",
   ["<b>Passthrough cameras are low resolution, noisy in dim light, and "
    "limited in dynamic range</b> compared with the human eye, which handles "
    "a room with a bright window without difficulty.",
    "<b>And the cameras are not located at your eyes.</b> They sit on the "
    "front of the headset, several centimetres away, so the captured view "
    "must be reprojected to each eye's actual viewpoint — which "
    "requires depth, and introduces warping and artefacts at depth "
    "discontinuities, particularly around the user's own hands and at the "
    "edges of near objects.",
    "<b>The result is a view of the world that is usable and visibly "
    "degraded.</b> Reading small text through passthrough is uncomfortable; "
    "recognising faces and navigating a room are entirely fine.",
    "<b>This is improving quickly</b>, and it is at present the binding "
    "constraint on how long anyone will keep a passthrough headset on — "
    "more so than weight, battery, or content."]),
  ("ul", ["<b>Other people are present.</b> They can see you gesturing at "
          "objects they cannot see, and they have no way to know what you "
          "are attending to. This is socially awkward in a way that a "
          "closed VR headset — which at least unambiguously signals "
          "unavailability — is not.",
          "<b>Cameras in social spaces raise privacy questions</b> that a "
          "sealed headset does not. Whether the device is recording is not "
          "visible to the people around it, and this has a poor history.",
          "<b>Attention is divided</b> between the real and virtual, with "
          "genuine safety consequences — the user is walking around a "
          "real environment while partly attending to something else.",
          "<b>Content must respect the real environment.</b> A virtual "
          "window placed on a real wall is fine; one floating in a real "
          "doorway is not, both aesthetically and because people walk "
          "through doorways.",
          "<b>And the device is worn in public</b>, which is a design "
          "constraint with a conspicuously poor track record. <b>The social "
          "dimension is a substantial part of why AR adoption has lagged "
          "behind the technology</b>, and treating it as a problem outside "
          "engineering is how products fail."]),
 ],
 "resources": [
   ("Azuma &mdash; A Survey of Augmented Reality (free)",
    "https://www.cs.unc.edu/~azuma/ARpresence.pdf",
    "The foundational survey. The registration analysis of &sect;2 is "
    "clearer here than in most modern treatments."),
   ("Meta &mdash; Passthrough and Mixed Reality documentation (free)",
    "https://developers.meta.com/horizon/documentation/",
    "The current practice: passthrough APIs, scene understanding, anchors, "
    "and depth."),
   ("Apple &mdash; visionOS human interface guidelines (free)",
    "https://developer.apple.com/design/human-interface-guidelines/",
    "The most carefully considered published thinking on &sect;3's social "
    "and environmental design questions, whatever you make of the device."),
   ("Google &mdash; ARCore lighting estimation documentation (free)",
    "https://developers.google.com/ar",
    "Practical lighting estimation, including environment map generation "
    "from a camera feed."),
 ],
 "exercises": [
   "Use a passthrough headset and assess the image quality honestly: read "
   "text at several sizes, judge distances, and note where reprojection "
   "artefacts appear.",
   "Place a virtual object on a real table and walk around it. Record every "
   "moment where registration error became visible.",
   "Measure registration error: place a virtual marker on a real one and "
   "photograph the offset from several angles.",
   "Implement occlusion using the headset's depth API and test it with your "
   "own hand. Note where the edges fail.",
   "Place a virtual object in a brightly lit and a dimly lit room without "
   "lighting estimation, then with it, and compare.",
   "Add a contact shadow under a virtual object resting on a real surface. "
   "Judge the improvement.",
   "Build an environment map from passthrough and apply it to a reflective "
   "virtual object.",
   "Implement a persistent anchor, close the application, and confirm the "
   "content returns to the same real-world position.",
   "Wear a passthrough headset in a room with another person for ten "
   "minutes. Write a page on the social experience from both sides.",
 ],
 "selfcheck": [
   "Compare optical and video see-through on six axes.",
   "Why can optical see-through not render black, and what follows?",
   "Why is registration error obvious in AR and invisible in VR?",
   "What tolerances does registration require, and how does latency "
   "contribute?",
   "Give five requirements of good registration.",
   "Why is occlusion hard in AR, and why are hands the critical case?",
   "Name five elements of lighting estimation and say which is cheapest and "
   "most effective.",
   "Why is passthrough quality the current binding constraint?",
   "Give five social or environmental problems AR has that VR does not.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Designing and Evaluating VR",
 "subtitle": "Conventions, accessibility, and finding out whether it works.",
 "question": "How do you know whether what you built is any good?",
 "outcomes": [
     "Apply the established VR interface conventions.",
     "Design for accessibility in VR specifically.",
     "Run an honest user evaluation.",
     "Choose measures appropriate to a perceptual claim.",
     "State the ethical considerations the medium raises.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Conventions",
   "blurb": "What users already expect."},

  {"t": "table", "kicker": "Conventions", "title": "Established VR interface patterns",
   "header": ["Convention", "Why it settled"],
   "widths": [4.0, 8.1],
   "rows": [
     ["<b>World-space UI at 1–2 m</b>", "<b>Comfortable depth (Module 02); occludable</b>"],
     ["<b>Grab to move, trigger to select</b>", "Near-universal; violating it confuses users"],
     ["<b>Teleport on the thumbstick</b>", "Expected; make it the default"],
     ["<b>Menus attached to a hand</b>", "Always reachable; never in the way"],
     ["Proximity highlighting", "Teaches interactivity without words (Module 09)"],
     ["<b>A visible guardian boundary</b>", "<b>Safety; and users rely on it</b>"],
   ],
   "footnote": "<b>Conventions are worth following</b> unless you have a "
               "specific reason — novelty in interaction costs the "
               "user, not you.",
   "note": "The 'novelty costs the user' framing is the useful one. "
           "Inventing interaction metaphors is expensive."},

  {"t": "callout", "title": "Comfort settings are an accessibility feature",
   "kind": "Not a nicety",
   "body": ["<b>Given the variation in Module 07</b>, a single locomotion "
            "scheme excludes part of your audience by construction.",
            "<b>The standard set:</b> teleport and smooth locomotion; snap "
            "and smooth turning; vignette strength; seated and standing "
            "modes; dominant hand.",
            "<b>And height calibration</b> — assuming a standing adult "
            "excludes children, wheelchair users, and anyone sitting down.",
            "<b>These are cheap to implement and expensive to retrofit</b>, "
            "which is why they belong in the design from the start."]},

  {"t": "bullets", "kicker": "Accessibility", "title": "Accessibility in VR specifically",
   "items": [
     "<b>Seated play</b> for everything that can support it — "
     "wheelchair users, people with balance issues, and anyone on a sofa.",
     "",
     "<b>One-handed modes.</b> Requiring two hands excludes people and is "
     "rarely necessary.",
     "",
     "<b>Reachability:</b> do not require reaching above the head or to the "
     "floor. Offer adjustable interaction heights.",
     "",
     "<b>Subtitles that work in 3D</b> — positioned where they can be "
     "read, with an indicator of which direction the speaker is in.",
     "",
     "<b>Colour and contrast</b>, as anywhere — and VR displays have "
     "their own contrast limitations.",
   ],
   "footnote": "VR accessibility is substantially less developed than "
               "flat-screen accessibility, which is an opportunity."},

  {"t": "section", "label": "Part 2", "title": "Evaluation",
   "blurb": "Measuring a claim about an experience."},

  {"t": "callout", "title": "You are the worst possible test subject",
   "kind": "Restating Module 07",
   "body": ["<b>You know where everything is</b>, you know what the "
            "interaction model is, and you built the mental model you are "
            "testing.",
            "<b>And you are maximally acclimatised</b> to VR discomfort "
            "(Module 07).",
            "<b>So your judgement of both usability and comfort is the "
            "least reliable available</b>, on exactly the two dimensions "
            "that matter most.",
            "<b>This is not a failure of care.</b> It is structural, it "
            "applies to everyone who builds VR, and the only remedy is "
            "testing on other people."]},

  {"t": "table", "kicker": "Measures", "title": "What to measure, and how",
   "header": ["Claim", "Instrument"],
   "widths": [4.2, 7.9],
   "rows": [
     ["<b>Comfort</b>", "<b>SSQ or VRSQ, before and after</b>"],
     ["<b>Presence</b>", "Witmer-Singer or Slater-Usoh-Steed questionnaire"],
     ["Usability", "Task completion, time, errors; think-aloud"],
     ["Discoverability", "<b>Time to first successful interaction, unaided</b>"],
     ["Performance", "<b>Frame time distribution, not the mean</b>"],
     ["Latency", "Physical measurement (Module 06)"],
   ],
   "footnote": "<b>Use the standard instruments.</b> An invented scale is "
               "not comparable to anything.",
   "note": "Time-to-first-successful-interaction is the single most "
           "informative usability number in VR."},

  {"t": "callout", "title": "Watch them in silence",
   "kind": "The most useful method",
   "body": ["<b>Give a novice the headset, say nothing beyond 'have a "
            "look', and watch for sixty seconds.</b>",
            "<b>Record every moment of hesitation</b> — where they looked "
            "for something and did not find it, where they tried an "
            "interaction that did not work.",
            "<b>Resist explaining.</b> The moment you say 'press the "
            "trigger', you have destroyed the data and learned nothing about "
            "discoverability.",
            "<b>Six people is enough to find most usability problems</b>, "
            "and the first two will find most of them. This is cheap and "
            "almost nobody does it."]},

  {"t": "section", "label": "Part 3", "title": "Ethics",
   "blurb": "What this medium can do that others cannot."},

  {"t": "bullets", "kicker": "Ethics", "title": "Considerations the medium raises",
   "items": [
     "<b>Physical safety.</b> Users cannot see the room. Guardian systems, "
     "and designs that do not encourage large movements.",
     "",
     "<b>Intensity.</b> VR experiences are more affecting than screen-based "
     "ones — including in ways users do not anticipate. Warn, and allow "
     "exit.",
     "",
     "<b>Data.</b> Eye tracking, hand tracking, and room scanning are "
     "unusually personal. Gaze reveals attention and intent.",
     "",
     "<b>Harassment in social VR</b> has a physicality that text does not. "
     "Personal space tools exist because they were needed.",
     "",
     "<b>Children.</b> Developing visual systems, unknown long-term "
     "effects, and headsets built for adult IPDs.",
   ],
   "note": "The eye-tracking data point is the one that will matter most "
           "over the next decade."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["You can account for every millisecond between a head movement "
            "and a photon, and you know why that matters physiologically.",
            "You can tell a <i>rendering</i> problem from a "
            "<i>tracking</i> problem from a <i>perceptual</i> problem "
            "— which is most of the skill.",
            "<b>And you know that your own judgement of comfort is the "
            "least reliable available</b>, which is the single most useful "
            "thing this course teaches.",
            "<b>CSCE 641 and 647</b> render it; <b>CSCE 649</b> moves it; "
            "<b>CSCE 735</b> makes it fast enough. This course is where a "
            "person is put inside the result and the constraint becomes "
            "physiological."]},
 ],
 "takeaways": [
   "Follow the established conventions — world-space UI at 1–2 m, "
   "grab and trigger, teleport on the stick — unless you have a "
   "specific reason.",
   "Comfort settings are an accessibility feature: a single locomotion "
   "scheme excludes part of the audience by construction.",
   "Seated play, one-handed modes, reachability, and 3D subtitles are the "
   "VR-specific accessibility requirements.",
   "You are the worst available test subject on exactly the two dimensions "
   "that matter: usability and comfort.",
   "Use standard instruments — SSQ for comfort, a validated presence "
   "questionnaire — so results are comparable to published work.",
   "Watch a novice in silence for sixty seconds and record every "
   "hesitation. Six people find most usability problems and almost nobody "
   "does it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Conventions"),
  ("table", ["Convention", "Why it settled", "Cost of violating it"],
   [["<b>World-space UI at 1–2 m</b>",
     "A comfortable vergence distance near the display's focal plane "
     "(Module 02), and it can be occluded correctly (Module 03).",
     "Eye strain, and an interface that fights the depth cues."],
    ["<b>Grip to grab, trigger to select</b>",
     "Near-universal across applications and platforms.",
     "Users will try the expected mapping first and conclude the "
     "application is broken."],
    ["<b>Teleport on the thumbstick, as the default</b>",
     "Expected by anyone who has used VR before, and the safe choice for "
     "anyone who has not (Module 08).",
     "A novice's first experience is a smooth-locomotion one, which is the "
     "worst possible introduction."],
    ["<b>Menus attached to a hand or wrist</b>",
     "Always reachable, never in the way, and they move with the user.",
     "A menu fixed in the world is lost the moment the user turns around."],
    ["<b>Proximity highlighting</b>",
     "Teaches interactivity without words (Module 09).",
     "Users do not discover what is interactive."],
    ["<b>A visible guardian boundary</b>",
     "<b>Safety</b> — and users come to rely on it to know how far "
     "they can move.",
     "People walk into walls. This is not hypothetical."]],
   [0.22, 0.43, 0.35]),
  ("p", "<b>Conventions are worth following unless you have a specific "
        "reason not to.</b> Novelty in interaction is paid for by the user, "
        "not by the designer — every unfamiliar mapping is a thing "
        "someone must discover, and the discovery happens in the first "
        "minute when they are least able to afford it."),
  ("callout", "Comfort settings are an accessibility feature",
   ["<b>Given the variation documented in Module 07</b> — where some "
    "people tolerate smooth locomotion indefinitely and others cannot manage "
    "two minutes — <b>an application with a single locomotion scheme "
    "has excluded part of its audience by construction.</b>",
    "<b>The standard set</b>: teleport and smooth locomotion, both offered; "
    "snap and smooth turning, with snap as the default; adjustable vignette "
    "strength; seated and standing modes; and dominant-hand selection.",
    "<b>And height calibration.</b> Assuming a standing adult of average "
    "height excludes children, wheelchair users, anyone sitting on a sofa, "
    "and anyone unusually short or tall. An adjustable height offset is a few "
    "lines of code.",
    "<b>These are cheap to implement at design time and expensive to "
    "retrofit</b>, because locomotion choice propagates into level design "
    "(Module 08). <b>Which is why they belong in the design from the "
    "start</b> rather than in a patch after the complaints arrive."]),
  ("ul", ["<b>Seated play for everything that can support it.</b> This "
          "covers wheelchair users, people with balance or mobility "
          "difficulties, and the large number of people who simply want to "
          "sit down.",
          "<b>One-handed modes.</b> Requiring two functioning hands excludes "
          "people, and it is rarely genuinely necessary — most "
          "two-handed interactions have a reasonable one-handed equivalent.",
          "<b>Reachability.</b> Do not require reaching above the head, to "
          "the floor, or behind the body. Offer an adjustable interaction "
          "height so content can be brought within a user's range.",
          "<b>Subtitles that work in three dimensions</b> — positioned "
          "at a readable depth and angle, legible against arbitrary "
          "backgrounds, and <b>with an indicator of which direction the "
          "speaker is in</b>, since a deaf or hard-of-hearing user loses the "
          "audio cue that would otherwise direct their attention "
          "(Module 11).",
          "<b>Colour and contrast</b>, as in any medium — with the "
          "added consideration that VR displays have their own contrast "
          "limitations and that god rays (Module 04) make high-contrast "
          "content worse. <b>VR accessibility is substantially less "
          "developed than flat-screen accessibility</b>, which is both a "
          "problem and an opportunity."]),

  ("h1", "2 &nbsp; Evaluation"),
  ("callout", "You are the worst available test subject",
   ["<b>You know where everything is.</b> You know which objects are "
    "interactive, what the control mapping is, and where the experience "
    "intends you to look — because you decided all of it.",
    "<b>You built the mental model you would be testing for.</b> There is no "
    "way to un-know it, and no amount of care substitutes.",
    "<b>And you are maximally acclimatised to VR discomfort</b> "
    "(Module 07), having spent more hours in a headset than any of your "
    "users will.",
    "<b>So your judgement is the least reliable available on exactly the "
    "two dimensions that matter most</b> — usability and comfort. "
    "<b>This is not a failure of care or attention.</b> It is structural, it "
    "applies equally to everyone who builds VR, and the only remedy is to "
    "test on other people."]),
  ("table", ["Claim you want to make", "Appropriate instrument"],
   [["<b>'It is comfortable'</b>",
     "<b>The Simulator Sickness Questionnaire or the shorter VRSQ, "
     "administered before and after</b> (Module 07). Free, validated, and "
     "comparable to published work."],
    ["<b>'It is immersive' / 'users feel present'</b>",
     "A validated presence questionnaire — Witmer&ndash;Singer, or "
     "Slater&ndash;Usoh&ndash;Steed. Presence is subjective and these make "
     "it comparable."],
    ["<b>'It is usable'</b>",
     "Task completion rate, time on task, error counts, and a think-aloud "
     "protocol for the reasoning behind failures."],
    ["<b>'It is discoverable'</b>",
     "<b>Time to first successful interaction, with no instruction.</b> The "
     "single most informative usability number in VR."],
    ["<b>'It performs well'</b>",
     "<b>The frame time distribution, including the 99th percentile</b> "
     "— never the mean (Module 01)."],
    ["<b>'It is responsive'</b>",
     "Physically measured motion-to-photon latency (Module 06), not an "
     "estimate from frame time."]],
   [0.33, 0.67]),
  ("callout", "Watch them in silence",
   ["<b>Give a person who has never seen your application the headset, say "
    "nothing beyond 'have a look around', and watch for sixty seconds.</b>",
    "<b>Record every hesitation.</b> Where did they look for something and "
    "not find it? What did they try that did not work? What did they not "
    "notice at all? What did they reach for first?",
    "<b>Resist explaining.</b> The instant you say 'press the trigger', the "
    "session has stopped measuring discoverability and started measuring "
    "whether they can follow instructions — and you have learned "
    "nothing you did not already know. This is genuinely difficult to do and "
    "it is where the value is.",
    "<b>Six participants will find most usability problems</b>, and the "
    "first two will find the majority of those. <b>This is cheap, it takes "
    "an afternoon, and almost nobody does it</b> — which is why so many "
    "VR applications have a first minute that nobody can get through."]),

  ("break",),
  ("h1", "3 &nbsp; Ethics"),
  ("ul", ["<b>Physical safety.</b> Users cannot see the room they are "
          "standing in. Guardian and boundary systems exist for this reason "
          "and should never be worked around; designs that encourage large, "
          "fast, or backward movements are designs that will injure "
          "somebody.",
          "<b>Intensity.</b> VR experiences are substantially more affecting "
          "than screen-based ones — heights produce genuine fear "
          "responses, and threatening content produces genuine startle. "
          "<b>Including in ways users do not anticipate</b>, because their "
          "expectations are calibrated on screens. Warn in advance, and make "
          "exiting easy and obvious.",
          "<b>Data.</b> Eye tracking, hand tracking, and room scanning "
          "produce unusually intimate data. <b>Gaze in particular reveals "
          "attention, interest, and intent</b> at a resolution no other "
          "consumer sensor approaches — what someone looked at, for how "
          "long, and what they looked away from. This is the consideration "
          "most likely to matter over the next decade, and it is "
          "underdiscussed.",
          "<b>Harassment in social VR has a physicality that text-based "
          "harassment does not.</b> Proximity, gesture, and voice combine "
          "into something users report as qualitatively worse. Personal "
          "space tools and blocking exist in social VR because they were "
          "found to be necessary, not as a precaution.",
          "<b>Children.</b> Developing visual systems, unknown long-term "
          "effects, headsets built around adult IPDs (Module 03) that do not "
          "adjust far enough, and age ratings that are routinely ignored. "
          "<b>The honest position is that the long-term effects are not "
          "known</b>, which is itself a reason for caution rather than a "
          "reason to proceed."]),
  ("callout", "Where this course leaves you",
   ["<b>You can account for every millisecond between a head movement and a "
    "photon</b>, and explain why that accounting is physiological rather "
    "than aesthetic.",
    "<b>You can distinguish a rendering problem from a tracking problem "
    "from a perceptual problem</b> — which, as in every other course in "
    "this program, is most of the practical skill. A juddering world, a "
    "swimming world, and a nauseating world have three different causes and "
    "three different fixes.",
    "<b>And you know that your own judgement of comfort and usability is "
    "the least reliable available.</b> If this course teaches one thing that "
    "survives, it should be that — because it is the belief that most "
    "reliably prevents shipping something that makes people ill.",
    "<b>CSCE 641 and 647 render it; CSCE 649 moves it; CSCE 735 makes it "
    "fast enough.</b> This course is where a person is placed inside the "
    "result, and the constraint stops being a frame budget and becomes a "
    "physiological one."]),
 ],
 "resources": [
   ("LaValle &mdash; Virtual Reality, Chapter 12 (free)",
    "http://lavalle.pl/vr/",
    "Evaluation methodology, the standard instruments, and experimental "
    "design for perceptual claims."),
   ("Meta &mdash; VR design and accessibility guidelines (free)",
    "https://developers.meta.com/horizon/resources/",
    "The convention set of &sect;1 and a growing accessibility section."),
   ("XR Access &mdash; accessibility resources (free)",
    "https://xraccess.org/",
    "The most active community work on &sect;1's accessibility material, "
    "including guidelines and user research."),
   ("Nielsen &mdash; Why You Only Need to Test with 5 Users (free)",
    "https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/",
    "The basis for &sect;2's claim about six participants. Short, and the "
    "argument generalises to VR."),
   ("Slater & Sanchez-Vives &mdash; Enhancing Our Lives with Immersive "
    "Virtual Reality (free)",
    "https://www.frontiersin.org/articles/10.3389/frobt.2016.00074/full",
    "A survey of what the medium can do, including the ethical questions in "
    "&sect;3, from researchers who have studied them."),
 ],
 "exercises": [
   "Audit three VR applications against the convention table in &sect;1 and "
   "note every violation and its consequence.",
   "Implement the full standard comfort settings set and justify each option "
   "from Modules 07 and 08.",
   "Add height calibration and test your application seated, standing, and "
   "at a child's height.",
   "Add a one-handed mode to an interaction that assumed two hands.",
   "Implement 3D subtitles with a speaker direction indicator and test them "
   "with the audio muted.",
   "<b>Run the silent-observation test</b> on six people, at least two of "
   "whom have never used VR. Record every hesitation and resist explaining.",
   "Administer an SSQ before and after, and a presence questionnaire after, "
   "for the same six people. Report every score individually.",
   "Measure time to first successful interaction for each participant, and "
   "identify the single change that would most reduce it.",
   "Write the ethics section of a design document for your Project 2 "
   "application, addressing each item in &sect;3 that applies.",
   "<b>Project 2 is now due.</b> Submit the application, the frame timing "
   "data, the participant results in full, the optimisation measurements, "
   "and the account of something that worked for you and not for others.",
 ],
 "selfcheck": [
   "Name six VR interface conventions and say why each settled.",
   "Why are comfort settings an accessibility feature rather than a "
   "courtesy?",
   "Give five VR-specific accessibility requirements.",
   "Why are you the worst available test subject, on which two dimensions?",
   "Name the appropriate instrument for each of six claims you might want to "
   "make.",
   "Describe the silent observation method and say what destroys the data.",
   "How many participants find most usability problems?",
   "Name five ethical considerations the medium raises, and say which is "
   "most likely to matter over the next decade.",
   "What are the three categories of problem you should be able to "
   "distinguish?",
 ],
},

]
