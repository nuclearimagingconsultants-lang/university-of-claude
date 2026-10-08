# -*- coding: utf-8 -*-
"""CSCE 650 Virtual Reality — original course content."""

COURSE = {
    "code": "CSCE 650",
    "title": "Virtual Reality",
    "tagline": "Perception, tracking, latency, and the design of experience "
               "that does not make people ill",
    "term": "Semester 4 (with CSCE 748 and CSCE 735)",
    "prereqs": "CSCE 641 Computer Graphics; CSCE 649 helpful for the "
               "interaction work; no hardware assumed beyond a consumer "
               "headset",
    "effort": "10–12 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A VR application that holds its frame budget, tracks "
                   "correctly, renders stereo without error, and has been "
                   "tested on people other than you — with their comfort "
                   "ratings reported",
    "description": [
        "Every other course in this program had a correctness criterion you "
        "could compute. A renderer converges to the rendering equation; a "
        "simulator conserves momentum; a database survives "
        "<code>kill -9</code>. <b>Virtual reality's criterion is a claim "
        "about a person</b> — whether they feel present, and whether they "
        "feel ill — and that changes the discipline.",
        "The central fact is that <b>you are rendering to the vestibular "
        "system as much as to the eye</b>. A frame delivered 40 ms late is "
        "not a performance problem; it is a conflict between what the inner "
        "ear reports and what the eyes show, and the body resolves that "
        "conflict by inducing nausea. This is why VR has a hard real-time "
        "requirement that ordinary graphics does not, and why 'it runs at "
        "45 fps, close enough' is not an acceptable sentence.",
        "The second fact is that <b>most of the hard problems are "
        "perceptual rather than computational</b>. Why a corridor feels "
        "wrong, why a hand that passes through a table breaks presence, why "
        "teleport locomotion is comfortable and smooth locomotion is not, "
        "and why some people are fine and others are not — none of these "
        "are answered by profiling. They are answered by knowing how human "
        "perception works and by testing on humans.",
        "You will build in a real engine rather than from scratch, because "
        "the compositor, the timewarp, and the driver stack are not things "
        "it is useful to reimplement. <b>The work is in the parts the "
        "engine does not do for you</b>, which is most of what determines "
        "whether an application is good.",
    ],
    "outcomes": [
        "Explain presence and the conditions that sustain and break it.",
        "Apply the relevant properties of human vision to display and "
        "rendering decisions.",
        "Implement correct stereo rendering with asymmetric frusta.",
        "Explain lens distortion correction and why it interacts with "
        "timewarp.",
        "Explain tracking, sensor fusion, and prediction.",
        "Account for every millisecond of the motion-to-photon budget.",
        "Explain cybersickness mechanistically and design to reduce it.",
        "Compare locomotion schemes against the comfort/presence trade.",
        "Apply VR-specific rendering optimisations and say what each costs.",
        "Design and run an honest evaluation on real users.",
    ],
    "materials": [
        ("LaValle — Virtual Reality (free book and Illinois lectures)",
         "http://lavalle.pl/vr/",
         "The primary text, free and complete. Unusually strong on "
         "perception and on the mathematics of tracking, written by someone "
         "who worked on the Oculus tracking system."),
        ("Stanford EE267 — Virtual Reality, build your own HMD (free)",
         "https://web.stanford.edu/class/ee267/",
         "Course notes, slides, and assignments that build a headset from "
         "parts. The optics and display material is the best free treatment "
         "of Modules 03 and 04."),
        ("Oculus/Meta Developer Documentation — performance and comfort "
         "(free)",
         "https://developers.meta.com/horizon/documentation/",
         "The practical engineering: frame budgets, timewarp, guardian, and "
         "the comfort guidelines. Vendor documentation, and genuinely good "
         "on the hard numbers."),
        ("Unreal Engine XR documentation (free)",
         "https://dev.epicgames.com/documentation/en-us/unreal-engine/xr-development",
         "What you will actually build in. Read the performance and "
         "stereo-rendering sections before Module 10."),
        ("Michael Abrash — blog archive and talks (free)",
         "http://blogs.valvesoftware.com/abrash/",
         "The latency and display analysis that shaped modern VR. 'Latency "
         "— the sine qua non of AR and VR' is required reading for "
         "Module 06."),
        ("Jerald — The VR Book (chapters and talks free)",
         "https://www.nextgeninteractions.com/",
         "The human-factors and design side, which the engineering sources "
         "underweight. Good for Modules 07, 08, and 13."),
    ],
    "tooling": [
        "<b>A headset.</b> Any PC-connected or standalone consumer headset "
        "is sufficient. <b>You cannot do this course without one</b> — "
        "every claim in it is about an experience.",
        "<b>Unreal or Unity</b> with OpenXR. Do not write a VR runtime; the "
        "compositor and timewarp are not useful things to reimplement, and "
        "getting them wrong makes people ill.",
        "<b>A frame profiler that reports per-eye GPU time</b> — "
        "RenderDoc, PIX, or the engine's own. <b>Frame time is the "
        "subject of this course</b> and you must be able to see it.",
        "<b>A way to record what the user saw</b>, with timing. Spectator "
        "capture plus a log of frame times is enough.",
        "<b>Test subjects.</b> At least six people who are not you, "
        "including at least one who has never used VR. <b>Your own "
        "tolerance is not data.</b>",
        "<b>A simulator-sickness questionnaire</b> (SSQ or the shorter "
        "VRSQ). Free, standard, and it makes comfort claims comparable.",
    ],
    "projects": [
        {"title": "A scene that holds its budget", "after": 7,
         "brief": "No interaction, no locomotion. A static scene the user "
                  "can look around in, rendered correctly and comfortably. "
                  "Everything later depends on this being right, and it is "
                  "harder than it sounds.",
         "reqs": [
             "Correct stereo with asymmetric frusta and the user's measured "
             "IPD, not a hard-coded default.",
             "Frame budget held at the headset's native rate, with per-eye "
             "GPU time reported and headroom stated.",
             "Measured motion-to-photon latency, by whatever method you can "
             "manage, with the method described.",
             "No frame drops over a five-minute session. Report the frame "
             "time distribution, not the mean.",
             "A deliberate comparison: the same scene with a correct IPD "
             "and with one 15 mm wrong, described from the inside.",
         ],
         "done": [
             "<b>A frame time histogram over five minutes with the 99th "
             "percentile under the budget.</b> Means hide exactly the "
             "frames that cause discomfort.",
             "Six people report no discomfort after five minutes, on a "
             "standard questionnaire.",
             "A written account of what the wrong-IPD version felt like. "
             "<b>Most people cannot say what is wrong, only that something "
             "is</b> — which is the lesson.",
             "An honest statement of what you could not measure and why.",
         ]},
        {"title": "An application people can use", "after": 12,
         "brief": "Interaction, locomotion, and audio, evaluated on real "
                  "people with real instruments rather than on your own "
                  "impression.",
         "reqs": [
             "Hand or controller interaction with grab, release, and at "
             "least one tool, with affordances a first-time user discovers "
             "unaided.",
             "At least two locomotion schemes, selectable, with the comfort "
             "trade documented.",
             "Spatialised audio with HRTF, and a demonstration of what is "
             "lost without it.",
             "One VR-specific rendering optimisation applied and measured "
             "— foveated rendering, variable rate shading, or stereo "
             "instancing.",
             "A comfort and usability evaluation with at least six "
             "participants, including novices.",
         ],
         "done": [
             "<b>Six participants' questionnaire scores, reported in full "
             "rather than averaged</b> — including anyone who had to stop.",
             "A video of a first-time user, with the moments they were "
             "confused marked and discussed.",
             "Before-and-after frame timings for the optimisation, with the "
             "visual cost shown honestly.",
             "<b>A written account of something that worked for you and not "
             "for others.</b> There will be one, and finding it is the "
             "point of testing on other people.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Presence, and What VR Must Deliver",
 "subtitle": "A correctness criterion that lives in somebody's head.",
 "question": "What makes virtual reality work, and what makes it fail?",
 "outcomes": [
     "Define presence and distinguish it from immersion.",
     "Explain why VR has a hard real-time requirement.",
     "State the frame budget and what it is spent on.",
     "Identify what breaks presence and what does not.",
     "Explain why the evaluation criterion is perceptual.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Presence",
   "blurb": "The thing the whole medium is for."},

  {"t": "two", "kicker": "Two words", "title": "Immersion and presence",
   "lh": "Immersion — the system",
   "l": ["A property of the <b>technology</b>.",
         "Field of view, resolution, tracking fidelity, latency.",
         "<b>Measurable</b>, and comparable between headsets.",
         ("A spec sheet describes immersion.", 1)],
   "rh": "Presence — the person",
   "r": ["A property of the <b>experience</b>.",
         "The feeling of <i>being there</i>; responding as if it were "
         "real.",
         "<b>Reported, not measured</b> — though behaviour correlates.",
         ("Immersion enables presence. It does not guarantee it.", 1)],
   "note": "The distinction matters because people buy immersion and "
           "experience presence, and the relationship is weak."},

  {"t": "callout", "title": "Presence is fragile and asymmetric",
   "kind": "The practical consequence",
   "body": ["<b>Building presence takes minutes.</b> It accumulates from "
            "consistency: things behave as expected, over and over.",
            "<b>Breaking it takes one frame.</b> A hand passes through a "
            "table, a sound comes from the wrong place, the world judders "
            "once.",
            "<b>And it does not come back immediately.</b> Once a user has "
            "been reminded they are wearing a headset, they are watching "
            "for the next failure.",
            "<b>So the design rule is not 'maximise the best moments' but "
            "'eliminate the worst ones'.</b> A consistently adequate "
            "experience beats an excellent one with a flaw."]},

  {"t": "bullets", "kicker": "Breaks", "title": "What actually breaks presence",
   "items": [
     "<b>Latency.</b> The world lags the head. Module 06.",
     "<b>Tracking failure.</b> Position jumps, or drifts.",
     "<b>Penetration.</b> A hand or object passes through solid geometry "
     "— the single most common break.",
     "<b>Wrong scale.</b> A room that is subtly the wrong size reads as "
     "dreamlike.",
     "<b>Mismatched audio.</b> Sound from the wrong direction, or no "
     "sound where there should be one.",
     "",
     "<b>Not on this list: polygon count, texture resolution, lighting "
     "quality.</b> They matter less than any item above.",
   ],
   "note": "The last line is the one that surprises graphics people. "
           "Fidelity is not what presence rests on."},

  {"t": "section", "label": "Part 2", "title": "The real-time requirement",
   "blurb": "Why this is not ordinary graphics."},

  {"t": "callout", "title": "You are rendering to the vestibular system",
   "kind": "The fact that changes everything",
   "body": ["The inner ear measures head acceleration directly, "
            "continuously, with latency in single-digit milliseconds.",
            "<b>The display reports where the head was, some milliseconds "
            "ago.</b>",
            "<b>When those two disagree, the brain has a conflict to "
            "resolve</b> — and one of its responses to sustained sensory "
            "conflict is nausea (Module 07).",
            "<b>So a late frame is not a performance issue. It is a "
            "physiological one</b>, and no amount of visual quality "
            "compensates. This is why VR's frame requirement is hard rather "
            "than soft."]},

  {"t": "table", "kicker": "Budget", "title": "The frame budget is not negotiable",
   "header": ["Rate", "Budget per frame", "Note"],
   "widths": [2.4, 3.4, 6.3],
   "rows": [
     ["60 Hz", "16.7 ms", "<b>Below the comfortable floor</b>"],
     ["<b>72 Hz</b>", "<b>13.9 ms</b>", "Common standalone minimum"],
     ["<b>90 Hz</b>", "<b>11.1 ms</b>", "<b>The usual target</b>"],
     ["120 Hz", "8.3 ms", "Noticeably better; expensive"],
     ["144 Hz", "6.9 ms", "Diminishing returns for most content"],
   ],
   "footnote": "<b>And that budget covers two eyes.</b> Effectively 5.5 ms "
               "per eye at 90 Hz, for everything.",
   "note": "The two-eyes point is the one students underestimate. It is "
           "not 11 ms of work; it is 11 ms for roughly double the work."},

  {"t": "callout", "title": "Missing the budget is worse than lowering quality",
   "kind": "The ordering",
   "body": ["A dropped frame means the compositor must reproject — or, "
            "worse, show the previous frame again. <b>The world "
            "judders.</b>",
            "<b>Users notice a single dropped frame</b> in a way they do "
            "not notice a 30% reduction in texture resolution.",
            "<b>So the order is: hit the budget first, then spend what is "
            "left on quality.</b> Not the other way around.",
            "<b>And profile the 99th percentile, not the mean.</b> The mean "
            "frame time tells you nothing about the frames that cause "
            "discomfort — which are, by definition, the slow ones."]},

  {"t": "section", "label": "Part 3", "title": "What is different",
   "blurb": "Assumptions from CSCE 641 that no longer hold."},

  {"t": "table", "kicker": "Changes", "title": "What VR invalidates",
   "header": ["In ordinary graphics", "In VR"],
   "widths": [5.6, 6.5],
   "rows": [
     ["One view per frame", "<b>Two, with shared setup</b>"],
     ["The camera is authored", "<b>The user controls it absolutely</b>"],
     ["Dropped frames are a stutter", "<b>Dropped frames make people ill</b>"],
     ["The screen is at a fixed distance", "<b>Depth is perceived; errors are visible</b>"],
     ["Post-processing is free-ish", "<b>Motion blur and heavy TAA are harmful</b>"],
     ["Field of view is a design choice", "<b>Fixed by the hardware</b>"],
   ],
   "note": "The camera-control row is the one with the widest design "
           "consequences — you cannot frame anything."},

  {"t": "callout", "title": "You have lost control of the camera",
   "kind": "The largest design consequence",
   "body": ["<b>Every cinematic technique that depends on framing is "
            "gone.</b> No cuts, no camera moves, no controlling what is on "
            "screen.",
            "<b>The user will look at the thing you did not finish</b>, "
            "stand where you did not expect, and put their face through the "
            "wall.",
            "<b>So: everything must be finished, in every direction</b>, "
            "and attention must be directed by light, sound, and motion "
            "rather than by framing.",
            "<b>Taking the camera away from the user to show them "
            "something is the classic beginner mistake</b>, and it is both "
            "unpleasant and a reliable way to induce sickness."]},

  {"t": "callout", "title": "The criterion is perceptual, so the method must be empirical",
   "kind": "How this course differs",
   "body": ["<b>There is no equation whose answer tells you the experience "
            "is correct.</b> CSCE 647 had one; this course does not.",
            "<b>The measurements that exist are proxies:</b> frame time, "
            "latency, tracking error. Necessary, and not sufficient.",
            "<b>The criterion is whether people feel present and do not "
            "feel ill</b>, and the only way to establish that is to ask "
            "people — several of them, including people unlike you.",
            "<b>Your own tolerance is not data.</b> VR developers are a "
            "self-selected population with unusually high tolerance, which "
            "is precisely why so much uncomfortable VR ships."]},
 ],
 "takeaways": [
   "Immersion is a property of the system and is measurable; presence is a "
   "property of the experience and is reported. The first enables the second "
   "and does not guarantee it.",
   "Presence builds over minutes and breaks in one frame, so the design goal "
   "is eliminating the worst moments rather than maximising the best.",
   "VR renders to the vestibular system as well as the eye — a late "
   "frame is a sensory conflict, not a performance complaint.",
   "The frame budget covers two eyes: about 5.5 ms per eye at 90 Hz. Hit the "
   "budget first, then spend what is left on quality.",
   "Profile the 99th percentile. The mean frame time says nothing about the "
   "frames that cause discomfort.",
   "You have lost control of the camera, so everything must be finished in "
   "every direction and attention directed by light, sound, and motion.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Presence"),
  ("table", ["", "Immersion", "Presence"],
   [["Belongs to", "<b>The system.</b>",
     "<b>The person.</b>"],
    ["Means", "The objective extent to which the display and tracking "
     "replace real sensory input: field of view, resolution, refresh rate, "
     "tracking degrees of freedom, latency.",
     "The subjective sense of <i>being there</i> — and, more usefully, "
     "the tendency to respond to virtual events as though they were real: "
     "flinching, stepping back, reaching out."],
    ["Established by", "<b>Measurement.</b> A spec sheet describes "
     "immersion.",
     "<b>Report and behaviour.</b> Questionnaires, and observed responses."],
    ["Relationship", "Immersion <i>enables</i> presence.",
     "<b>It does not guarantee it.</b> A technically excellent system with "
     "one consistent flaw produces less presence than a modest one without "
     "it."]],
   [0.15, 0.40, 0.45]),
  ("callout", "Presence is fragile, and the asymmetry is the design rule",
   ["<b>Presence accumulates slowly.</b> It is built from consistency "
    "— things behaving as expected, repeatedly, until the user stops "
    "checking. Minutes, typically.",
    "<b>It breaks in a single frame.</b> A hand passes through a table; a "
    "footstep comes from the wrong direction; the world judders once. The "
    "user is instantly aware of the headset again.",
    "<b>And it does not immediately return.</b> Having been reminded the "
    "world is synthetic, the user begins watching for the next failure, "
    "which makes the next failure easier to notice.",
    "<b>So the design objective is not to maximise the best moments but to "
    "eliminate the worst ones.</b> A uniformly adequate experience sustains "
    "more presence than an excellent one with a recurring flaw — which "
    "inverts the usual instinct in graphics, where the impressive moment is "
    "what gets built."]),
  ("table", ["Breaks presence", "Why"],
   [["<b>Latency</b>", "The world lags the head, so it feels attached to "
     "you rather than independent of you. Module 06."],
    ["<b>Tracking failure</b>", "Position jumps or drifts. The world moves "
     "when you did not."],
    ["<b>Penetration</b>", "A hand or held object passes through solid "
     "geometry. <b>The most common break by a wide margin</b>, because "
     "users test it deliberately within the first minute."],
    ["<b>Wrong scale</b>", "A room subtly the wrong size, or a doorway too "
     "small. Users rarely identify what is wrong, only that the space feels "
     "dreamlike."],
    ["<b>Mismatched audio</b>", "A sound from the wrong direction, or "
     "silence where a sound was expected. Module 11."],
    ["<b>Not on this list</b>",
     "<b>Polygon count, texture resolution, shadow quality, lighting "
     "fidelity.</b> They contribute, and they matter less than every item "
     "above. This surprises people arriving from CSCE 641, where those are "
     "the whole subject."]],
   [0.21, 0.79]),

  ("h1", "2 &nbsp; The real-time requirement"),
  ("callout", "You are rendering to the vestibular system",
   ["The vestibular system in the inner ear measures head rotation and "
    "linear acceleration <b>directly and continuously</b>, with a latency of "
    "a few milliseconds. It does not need to recognise anything or process "
    "an image; it is an accelerometer wired to the brainstem.",
    "<b>The display, meanwhile, reports where the head was some "
    "milliseconds ago</b> — however many the pipeline takes.",
    "<b>When those two signals disagree, the brain has a conflict to "
    "resolve.</b> One of its established responses to sustained sensory "
    "conflict is nausea, for reasons Module 07 covers.",
    "<b>So a late frame is not a performance complaint; it is a "
    "physiological event.</b> No amount of visual quality compensates for "
    "it, and the usual engineering instinct — 'it runs at 45, that is "
    "playable' — is simply wrong here. <b>This is the single most "
    "important difference between VR and every other kind of real-time "
    "graphics.</b>"]),
  ("table", ["Refresh rate", "Budget per frame", "Assessment"],
   [["60 Hz", "16.7 ms", "<b>Below the comfortable floor</b> for most "
     "people. Early headsets used it and the discomfort was notorious."],
    ["<b>72 Hz</b>", "<b>13.9 ms</b>",
     "The minimum on most standalone headsets. Acceptable for seated, "
     "low-motion content."],
    ["<b>90 Hz</b>", "<b>11.1 ms</b>",
     "<b>The usual target.</b> Where most people stop noticing the "
     "display's discreteness."],
    ["120 Hz", "8.3 ms", "Noticeably better for fast motion; expensive."],
    ["144 Hz", "6.9 ms", "Diminishing returns for most content."]],
   [0.18, 0.21, 0.61]),
  ("p", "<b>And that budget covers both eyes.</b> At 90 Hz you have 11.1 ms "
        "to produce two views, which — after the setup that can be "
        "shared between them — is on the order of 5.5 ms per eye for "
        "everything: geometry, shading, post, and submission. This is the "
        "figure students consistently underestimate, because the number "
        "quoted is per frame and the work is per eye."),
  ("callout", "Hit the budget first; spend the remainder on quality",
   ["When a frame misses its deadline, the compositor must do something. At "
    "best it reprojects the previous frame to the current head pose "
    "(Module 06); at worst it displays the previous frame unchanged. "
    "<b>Either way the world judders</b>, and the judder is correlated with "
    "head motion, which is exactly the condition that causes discomfort.",
    "<b>Users reliably notice a single dropped frame.</b> They do not "
    "reliably notice a 30% reduction in texture resolution, or one fewer "
    "shadow cascade, or a cheaper reflection.",
    "<b>So the ordering is fixed: meet the frame budget first, then spend "
    "whatever remains on visual quality.</b> In ordinary real-time graphics "
    "these can be traded against each other; here one of them is a hard "
    "constraint and the other is not.",
    "<b>And profile the 99th percentile rather than the mean.</b> A mean "
    "frame time of 9 ms is consistent with one frame in fifty taking 20 ms, "
    "and those are precisely the frames that cause discomfort. <b>The mean "
    "is the statistic that hides the problem</b>, which is why Project 1 "
    "asks for a histogram."]),

  ("break",),
  ("h1", "3 &nbsp; What VR invalidates"),
  ("table", ["Assumption from CSCE 641", "In VR"],
   [["One view rendered per frame.",
     "<b>Two</b>, with some setup shareable and most work doubled."],
    ["The camera is authored — the developer decides what is on "
     "screen.",
     "<b>The user controls it absolutely.</b> See below."],
    ["A dropped frame is a visible stutter and a minor annoyance.",
     "<b>A dropped frame is a physiological event.</b> &sect;2."],
    ["The screen is a flat surface at a fixed distance; depth is implied by "
     "cues.",
     "<b>Depth is genuinely perceived</b> through stereopsis and parallax, "
     "so errors in it are directly visible rather than merely incorrect."],
    ["Post-processing effects are a matter of taste and budget.",
     "<b>Motion blur and heavy temporal antialiasing are actively "
     "harmful</b> — they add perceived latency and smear during head "
     "motion, which is constant."],
    ["Field of view is a design decision.",
     "<b>Fixed by the hardware</b>, and changing it is both wrong and "
     "nauseating."]],
   [0.37, 0.63]),
  ("callout", "You have lost control of the camera",
   ["This is the design consequence with the widest reach, and it is "
    "consistently underestimated by people arriving from games or film.",
    "<b>Every technique that depends on framing is unavailable.</b> No cuts, "
    "no camera moves, no composition, no control over what is on screen at "
    "any moment. The user decides, continuously.",
    "<b>So they will look at the thing you did not finish</b>, stand "
    "somewhere you did not anticipate, lean through a wall to see what is "
    "behind it, and examine the back of an object you modelled from one "
    "side. Everything must be finished in every direction, and the budget "
    "has to accommodate that.",
    "<b>Attention must be directed by light, sound, and motion</b> — "
    "the techniques of theatre rather than cinema. A moving object, a sound "
    "from a direction, a brightening: these draw the eye without taking "
    "control.",
    "<b>Taking the camera from the user to show them something is the "
    "classic beginner mistake.</b> It is unpleasant, it breaks presence "
    "completely, and because the motion is unanticipated by the vestibular "
    "system it is a reliable way to make someone ill (Module 07)."]),
  ("callout", "A perceptual criterion demands an empirical method",
   ["<b>There is no equation whose value tells you the experience is "
    "correct.</b> CSCE 647 could difference an image against a converged "
    "reference; CSCE 649 could plot conserved energy; CSCE 608 could kill "
    "the process and check. This course has no equivalent.",
    "<b>The measurements that do exist are proxies.</b> Frame time, "
    "motion-to-photon latency, tracking jitter, stereo disparity error "
    "— all necessary, none sufficient. A system can be correct on every "
    "one and still be unpleasant.",
    "<b>The actual criterion is whether people feel present and do not feel "
    "ill</b>, and the only way to establish that is to ask people: several "
    "of them, including people who are not like you.",
    "<b>Your own tolerance is not data.</b> People who build VR are a "
    "self-selected population with unusually high tolerance — they "
    "acclimatised early and kept going precisely because it did not bother "
    "them. <b>This is a large part of why so much uncomfortable VR "
    "ships</b>, and it is why both projects in this course require testing "
    "on people who are not you, including at least one novice."]),
 ],
 "resources": [
   ("LaValle &mdash; Virtual Reality, Chapters 1 and 12 (free)",
    "http://lavalle.pl/vr/",
    "The definition of presence, the history, and the evaluation chapter. "
    "Chapter 12 is the empirical-method argument of &sect;3, properly "
    "developed."),
   ("Michael Abrash &mdash; What VR Could, Should, and Almost Certainly "
    "Will Be (free talk)",
    "http://blogs.valvesoftware.com/abrash/",
    "The clearest statement of why the requirements are what they are, from "
    "the period when they were being discovered."),
   ("Meta &mdash; VR design guidelines and comfort documentation (free)",
    "https://developers.meta.com/horizon/resources/",
    "The practical rules, with the numbers. Read the comfort section before "
    "Module 07."),
   ("Slater &mdash; Place illusion and plausibility (free)",
    "https://royalsocietypublishing.org/doi/10.1098/rstb.2009.0138",
    "The research framing of presence as two separable illusions — "
    "being there, and the events being real. More precise than the usual "
    "treatment."),
 ],
 "exercises": [
   "Put on a headset and write down, within the first two minutes, every "
   "moment you became aware of the hardware. This list is your design "
   "brief.",
   "Find a VR application and deliberately try to break presence: reach "
   "through geometry, look behind objects, stand where you should not. "
   "Record what succeeded.",
   "Measure your own IPD, and then try an application with it set 10 mm too "
   "wide and 10 mm too narrow. Describe each from the inside.",
   "Take a frame-time capture from any VR application over five minutes. "
   "Plot the histogram and report the mean, the 95th, and the 99th "
   "percentile. Note how different the story is.",
   "Compute the per-eye budget at 72, 90, and 120 Hz, and compare against a "
   "measured per-eye GPU time from a scene you build.",
   "Show a VR application to someone who has never used one. Say nothing and "
   "record what they do in the first sixty seconds.",
   "Find a VR application that moves the camera without user input. Describe "
   "the sensation precisely.",
   "Write a page on an experience that produced strong presence for you, and "
   "identify which of &sect;1's factors it got right.",
 ],
 "selfcheck": [
   "Distinguish immersion from presence, and say how they are each "
   "established.",
   "Why is presence asymmetric, and what design rule follows?",
   "Name five things that break presence, and three things that matter less "
   "than people expect.",
   "Why does rendering to the vestibular system change the frame "
   "requirement?",
   "State the per-frame and per-eye budget at 90 Hz.",
   "Why profile the 99th percentile rather than the mean?",
   "Give five assumptions from ordinary real-time graphics that VR "
   "invalidates.",
   "What follows from losing control of the camera, and what replaces "
   "framing?",
   "Why must the evaluation method be empirical, and why is your own "
   "tolerance not data?",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Human Vision for VR",
 "subtitle": "The specification you are actually building against.",
 "question": "What does the eye require, and what can you get away with?",
 "outcomes": [
     "State the relevant limits of human vision in numbers.",
     "Explain acuity falloff and what it permits.",
     "Distinguish the depth cues and say which VR provides.",
     "Explain the vergence-accommodation conflict.",
     "Explain flicker fusion and persistence.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The numbers",
   "blurb": "What the eye actually resolves."},

  {"t": "table", "kicker": "Vision", "title": "The specification",
   "header": ["Property", "Human", "Consumer headset"],
   "widths": [3.4, 4.2, 4.5],
   "rows": [
     ["Horizontal FOV", "~200&deg; binocular", "<b>~100–110&deg;</b>"],
     ["<b>Foveal acuity</b>", "<b>~60 pixels/degree</b>", "<b>~15–35 ppd</b>"],
     ["Acuity at 20&deg;", "~10 pixels/degree", "Same as centre — wasteful"],
     ["Flicker fusion", "60–90 Hz, higher in periphery", "72–120 Hz"],
     ["Stereo depth limit", "~10 m useful", "Beyond that, monocular cues"],
   ],
   "footnote": "<b>'Retinal resolution' means ~60 ppd across ~200&deg;</b> "
               "— roughly 10&times; current pixel counts per eye.",
   "note": "These numbers anchor every later decision. Have them "
           "memorise the acuity figure at least."},

  {"t": "callout", "title": "Acuity collapses outside the fovea",
   "kind": "The fact that foveated rendering exploits",
   "body": ["<b>The fovea is about 2&deg; wide</b> — roughly a thumbnail "
            "at arm's length — and is where all detailed vision happens.",
            "<b>At 20&deg; off-axis, acuity is about a sixth of foveal.</b> "
            "At 40&deg; it is far worse still.",
            "<b>Yet a headset renders the entire field at uniform "
            "resolution</b>, which means the overwhelming majority of "
            "pixels are far more detailed than the eye can use.",
            "<b>Foveated rendering (Module 10) recovers that waste</b> "
            "— and the reason it works is entirely this slide."]},

  {"t": "callout", "title": "You do not perceive the periphery the way you think",
   "kind": "A useful demonstration",
   "body": ["<b>Hold up a playing card at arm's length, look straight "
            "ahead, and move it sideways.</b> You cannot identify it past "
            "about 10&deg; — yet the world does not appear blurry.",
            "<b>The brain fills in</b>, using memory, saccades, and "
            "assumption. The vivid detailed field you experience is largely "
            "constructed.",
            "<b>But the periphery is extremely sensitive to motion and "
            "flicker</b> — more so than the fovea.",
            "<b>So: detail can be cut in the periphery; motion and flicker "
            "cannot.</b> That asymmetry governs both foveated rendering and "
            "comfort design."]},

  {"t": "section", "label": "Part 2", "title": "Depth",
   "blurb": "Many cues, and VR provides some of them."},

  {"t": "table", "kicker": "Depth cues", "title": "How depth is perceived",
   "header": ["Cue", "Range", "VR provides?"],
   "widths": [3.4, 3.6, 5.1],
   "rows": [
     ["<b>Stereopsis</b>", "To ~10 m", "<b>Yes — the headline feature</b>"],
     ["<b>Motion parallax</b>", "All", "<b>Yes — and underrated</b>"],
     ["<b>Vergence</b>", "To ~2 m", "<b>Yes, and conflicted</b>"],
     ["Accommodation", "To ~2 m", "<b>No — fixed focal plane</b>"],
     ["Occlusion", "All", "Yes"],
     ["Relative size, perspective", "All", "Yes"],
     ["Shading, shadows", "All", "<b>Yes — cheap and effective</b>"],
   ],
   "footnote": "Stereo gets the attention; <b>motion parallax does more "
               "work</b>, and shadows are the cheapest depth cue you have.",
   "note": "Students over-weight stereopsis. Parallax from head motion is "
           "what makes a space feel real."},

  {"t": "callout", "title": "The vergence-accommodation conflict",
   "kind": "The unsolved hardware problem",
   "body": ["<b>Vergence:</b> the eyes rotate inward to converge on an "
            "object. <b>Accommodation:</b> the lens changes shape to focus "
            "at that distance.",
            "<b>In the real world they are coupled</b> — the brain uses "
            "each as a cue for the other, and they always agree.",
            "<b>In a headset the display is at a fixed optical distance</b> "
            "— typically 1.5 to 2 m. So the eyes verge on a virtual "
            "object at 30 cm while still accommodating at 2 m.",
            "<b>The conflict causes eye strain and fatigue</b>, and it is "
            "why close-up work is uncomfortable. <b>No shipping headset "
            "solves it</b>; varifocal and light-field displays are the "
            "research directions."]},

  {"t": "bullets", "kicker": "Mitigation", "title": "Designing around the conflict",
   "items": [
     "<b>Keep interactive content at 0.5–2 m</b>, near the display's "
     "focal distance. This is the single most effective measure.",
     "",
     "<b>Avoid sustained close work.</b> Text at 30 cm is uncomfortable "
     "within minutes.",
     "",
     "<b>Put UI at a comfortable depth</b> and keep it there. UI that "
     "floats at a different depth from what it labels is tiring.",
     "",
     "<b>Reduce stereo separation for very close objects</b> if you must "
     "have them — physically wrong, and more comfortable.",
     "",
     "<b>Do not put anything closer than ~20 cm.</b> Fusion fails and the "
     "image doubles.",
   ],
   "note": "The 0.5-2 m rule is the practical takeaway and explains a lot "
           "of VR UI design."},

  {"t": "section", "label": "Part 3", "title": "Time",
   "blurb": "Flicker, persistence, and motion."},

  {"t": "callout", "title": "Low persistence is why modern VR is not a smeared mess",
   "kind": "The key display insight",
   "body": ["<b>A full-persistence display holds each frame lit for the "
            "whole frame period.</b> During head motion, the eye moves "
            "across a stationary image, and the result smears.",
            "<b>Low-persistence displays illuminate for ~2 ms</b> and are "
            "dark the rest of the time — so the image is a brief flash at "
            "a definite position.",
            "<b>Motion blur from eye movement disappears.</b> This was one "
            "of the decisive changes between early and modern headsets.",
            "<b>The cost is brightness and flicker.</b> Lit 2 ms in 11 is "
            "dim, and the flicker is visible in the periphery at lower "
            "rates — which is one reason 90 Hz rather than 72."]},

  {"t": "bullets", "kicker": "Consequences", "title": "What follows for rendering",
   "items": [
     "<b>Do not add motion blur.</b> The display's low persistence exists "
     "to remove blur; adding it back is perverse and adds perceived "
     "latency.",
     "",
     "<b>Be careful with temporal antialiasing.</b> It smears during head "
     "motion, which is constant, and the smear reads as latency.",
     "",
     "<b>MSAA is often the right choice in VR</b> despite being "
     "unfashionable, because it does not accumulate across frames.",
     "",
     "<b>Flickering content is worse in the periphery</b>, where "
     "sensitivity is highest. Avoid high-frequency flicker anywhere, and "
     "especially at the edges.",
     "",
     "<b>High-contrast edges in the periphery induce vection</b> "
     "(Module 07) and therefore sickness.",
   ],
   "footnote": "The MSAA point reverses a decade of real-time rendering "
               "practice, and the reason is persistence."},

  {"t": "callout", "title": "Binocular rivalry: the eyes must agree",
   "kind": "A failure mode to know",
   "body": ["If the two eyes receive sufficiently different images, the "
            "brain does not blend them. <b>It alternates between them</b>, "
            "which is deeply unpleasant.",
            "<b>Causes:</b> an effect rendered in one eye only, a "
            "view-dependent effect computed from the wrong eye, a UI element "
            "with incorrect disparity.",
            "<b>Specular highlights and reflections legitimately differ "
            "between eyes</b> — that is correct and fine. Gross "
            "differences are not.",
            "<b>Test by closing one eye, then the other.</b> If the two "
            "images differ in anything but viewpoint, something is wrong."]},
 ],
 "takeaways": [
   "Foveal acuity is about 60 pixels per degree over a ~200&deg; field; "
   "consumer headsets deliver 15–35 ppd over ~110&deg;.",
   "Acuity collapses outside the 2&deg; fovea — about a sixth at "
   "20&deg; — which is the entire basis of foveated rendering.",
   "The periphery is poor at detail and excellent at motion and flicker, so "
   "cut detail there and never flicker.",
   "Stereopsis gets the attention; motion parallax does more work, and "
   "shadows are the cheapest depth cue available.",
   "Vergence and accommodation are coupled in reality and decoupled in a "
   "headset, causing fatigue. Keep interactive content between 0.5 and 2 m.",
   "Low-persistence displays flash each frame for ~2 ms, removing "
   "eye-motion smear — so do not add motion blur back, and prefer MSAA "
   "to heavy TAA.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The numbers"),
  ("table", ["Property", "Human visual system", "Typical consumer headset"],
   [["Horizontal field of view",
     "About 200&deg; total, of which roughly 120&deg; is binocular.",
     "<b>100–110&deg;</b>, with the periphery absent entirely."],
    ["<b>Foveal acuity</b>",
     "<b>About 60 pixels per degree</b> for someone with 20/20 vision "
     "— the limit at which a pixel grid becomes invisible.",
     "<b>15–35 pixels per degree.</b> The gap is the reason the screen "
     "door effect and visible aliasing persist."],
    ["Acuity 20&deg; off-axis", "Roughly a sixth of foveal.",
     "Identical to the centre, since rendering is uniform — which is "
     "pure waste."],
    ["Flicker fusion threshold",
     "60–90 Hz, and <b>higher in the periphery</b> than at the "
     "centre.", "72–120 Hz refresh."],
    ["Useful stereo depth range",
     "To about 10 m; beyond that the disparity is too small to use.",
     "Same — and beyond 10 m you are relying on monocular cues, which "
     "is worth knowing when designing distant content."]],
   [0.21, 0.40, 0.39]),
  ("p", "<b>'Retinal resolution'</b> — the point at which the display "
        "ceases to be the limiting factor — means roughly 60 pixels "
        "per degree across the full 200&deg;. That is on the order of ten "
        "times the pixel count of current headsets <i>per eye</i>, which is "
        "a useful thing to know when evaluating claims about how close the "
        "technology is."),
  ("callout", "Acuity collapses outside the fovea",
   ["<b>The fovea is about 2&deg; across</b> — approximately a "
    "thumbnail held at arm's length — and essentially all detailed "
    "vision happens there. It is also where the cone density is highest by a "
    "large factor.",
    "<b>At 20&deg; off-axis acuity has fallen to roughly a sixth of "
    "foveal</b>, and it continues to drop steeply. At the edge of the field "
    "it is negligible.",
    "<b>A headset nonetheless renders the entire field at uniform "
    "resolution.</b> The overwhelming majority of the pixels it produces "
    "are far more detailed than the eye looking at them can resolve "
    "— the work is done and then discarded by the visual system.",
    "<b>Foveated rendering (Module 10) recovers that waste</b>, either "
    "fixed (assuming the user looks mostly forward) or eye-tracked. The "
    "entire justification for the technique is on this page."]),
  ("callout", "The periphery is poor at detail and excellent at motion",
   ["<b>A demonstration worth doing:</b> hold a playing card at arm's "
    "length, fix your gaze straight ahead, and move the card sideways. You "
    "will be unable to identify the card past roughly 10&deg; — and yet "
    "the world does not appear blurry at the edges.",
    "<b>The brain fills in.</b> The vivid, uniformly detailed visual field "
    "you experience is substantially constructed from memory, from rapid "
    "saccades you are unaware of, and from assumption.",
    "<b>But peripheral sensitivity to motion and flicker is higher than "
    "foveal</b>, not lower. This is evolutionarily sensible — the "
    "periphery is a threat detector — and it has direct design "
    "consequences.",
    "<b>So detail can be reduced in the periphery; motion and flicker "
    "cannot.</b> That asymmetry governs both foveated rendering (Module 10) "
    "and comfort design (Module 07), where peripheral motion is precisely "
    "what induces vection and therefore sickness."]),

  ("h1", "2 &nbsp; Depth"),
  ("table", ["Cue", "Mechanism", "Useful range", "Provided by VR?"],
   [["<b>Stereopsis</b>",
     "Disparity between the two retinal images.", "To about 10 m.",
     "<b>Yes</b> — the medium's headline feature."],
    ["<b>Motion parallax</b>",
     "Nearer objects move further across the retina as the head moves.",
     "All distances.",
     "<b>Yes, and underrated.</b> See below."],
    ["<b>Vergence</b>", "The inward rotation of the eyes.", "To about 2 m.",
     "<b>Yes, and in conflict with accommodation.</b>"],
    ["<b>Accommodation</b>", "The focusing effort of the lens.",
     "To about 2 m.",
     "<b>No.</b> The display sits at one fixed optical distance."],
    ["Occlusion", "Nearer objects hide further ones.", "All.",
     "Yes — and it is the strongest cue of all, which is why "
     "penetration breaks presence so completely (Module 01)."],
    ["Relative size, linear perspective, texture gradient", "Geometric.",
     "All.", "Yes, for free."],
    ["Shading and shadows", "Light falloff and contact shadows.", "All.",
     "<b>Yes — and the cheapest depth cue you have.</b> A contact "
     "shadow under an object does more for its apparent position than a "
     "great deal of geometric accuracy."]],
   [0.17, 0.30, 0.17, 0.36]),
  ("p", "<b>Stereopsis receives most of the attention and motion parallax "
        "does more of the work.</b> A user moving their head even slightly "
        "gets continuous, high-precision depth information across the entire "
        "range, where stereo is useful only to about ten metres. This is why "
        "a six-degree-of-freedom headset feels so much more convincing than "
        "a three-degree-of-freedom one, even though both provide stereo."),
  ("callout", "The vergence-accommodation conflict",
   ["<b>Vergence</b> is the inward rotation of the eyes to converge on an "
    "object. <b>Accommodation</b> is the change in the lens's shape to bring "
    "that distance into focus.",
    "<b>In the real world the two are coupled</b> — neurally, as well "
    "as physically. The brain uses each as a cue to drive the other, and "
    "they are always consistent.",
    "<b>In a headset the display is at a single fixed optical distance</b>, "
    "typically 1.5 to 2 m. So when a virtual object appears at 30 cm, the "
    "eyes verge as though it were at 30 cm while continuing to accommodate "
    "at 2 m. The two signals disagree, persistently.",
    "<b>The result is eye strain and fatigue</b>, and it is the principal "
    "reason that sustained close-up work in VR is uncomfortable. <b>No "
    "shipping consumer headset solves it.</b> Varifocal displays (which move "
    "the focal plane to match vergence) and light-field displays (which "
    "present a genuine focal range) are the active research directions, and "
    "neither has reached production."]),
  ("ul", ["<b>Keep interactive content between about 0.5 and 2 m</b>, near "
          "the display's focal distance. <b>This is the single most "
          "effective mitigation</b> and it explains a great deal of VR "
          "interface design — why menus hover at arm's length rather "
          "than close to the face.",
          "<b>Avoid sustained close work.</b> Reading text at 30 cm becomes "
          "uncomfortable within minutes, however crisp the text is.",
          "<b>Place UI at a consistent, comfortable depth.</b> A UI element "
          "at a different depth from the object it labels forces repeated "
          "vergence changes, which is tiring in a way users cannot "
          "articulate.",
          "<b>Consider reducing stereo separation for very close "
          "objects.</b> It is physically incorrect and measurably more "
          "comfortable, and several shipped applications do it.",
          "<b>Place nothing closer than roughly 20 cm.</b> Below that, "
          "binocular fusion fails outright and the image doubles."]),

  ("break",),
  ("h1", "3 &nbsp; Time, flicker, and persistence"),
  ("callout", "Low persistence is why modern VR is not a smeared mess",
   ["<b>A full-persistence display holds each frame illuminated for the "
    "entire frame period.</b> When the head turns, the eye tracks the world "
    "and therefore sweeps across a stationary image during those 11 "
    "milliseconds — and the result is smeared across the retina. Early "
    "headsets had this problem badly, and it was one of the main reasons "
    "they felt wrong.",
    "<b>A low-persistence display illuminates for roughly 2 ms per "
    "frame</b> and is dark for the remainder. Each frame is a brief flash at "
    "a definite position, so the eye receives a sharp image regardless of "
    "head motion.",
    "<b>Eye-motion smear disappears.</b> This was one of the decisive "
    "changes between the first-generation and modern headsets, and it is "
    "why the image stays sharp when you turn your head quickly.",
    "<b>The costs are brightness and flicker.</b> A display lit for 2 ms in "
    "every 11 is, other things equal, considerably dimmer — and the "
    "flicker becomes perceptible, particularly in the periphery where "
    "flicker sensitivity is highest (&sect;1). <b>This is a significant part "
    "of why 90 Hz rather than 72 Hz is the comfortable target.</b>"]),
  ("ul", ["<b>Do not add motion blur.</b> The display's low persistence "
          "exists specifically to eliminate motion blur; reintroducing it in "
          "a post-process is perverse, and it adds perceived latency because "
          "the blur trails behind the true position.",
          "<b>Be careful with temporal antialiasing.</b> TAA accumulates "
          "across frames and therefore smears during head motion — "
          "which in VR is constant rather than occasional. The smear reads "
          "to the user as latency even when the frame timing is correct.",
          "<b>MSAA is frequently the right choice in VR</b>, despite having "
          "fallen out of fashion in flat real-time rendering, precisely "
          "because it is a within-frame technique that accumulates nothing. "
          "<b>This reverses a decade of practice, and the reason is "
          "persistence.</b>",
          "<b>Avoid high-frequency flickering content</b>, and especially "
          "avoid it near the edges of the field where sensitivity is "
          "highest. Thin high-contrast geometry that aliases temporally is "
          "the usual culprit.",
          "<b>High-contrast edges and textures in the periphery induce "
          "vection</b> — the illusion of self-motion — and "
          "therefore sickness (Module 07). This is why comfort vignettes "
          "darken the periphery during movement."]),
  ("callout", "Binocular rivalry: the two eyes must agree",
   ["If the two eyes receive sufficiently different images, the brain does "
    "not average them. <b>It alternates</b> — perceiving one, then the "
    "other, in an unstable rhythm. The experience is disorienting and "
    "quickly unpleasant.",
    "<b>The usual causes are bugs:</b> an effect rendered into one eye's "
    "buffer only; a view-dependent effect such as a reflection computed from "
    "a single eye's position and applied to both; a UI element composited "
    "with incorrect or zero disparity; a post-process applied "
    "asymmetrically.",
    "<b>Note that some difference is correct.</b> Specular highlights and "
    "reflections genuinely differ between the eyes, and that difference is "
    "part of what makes a surface look wet or polished. The problem is gross "
    "disagreement, not disagreement as such.",
    "<b>The test is trivial and worth doing routinely:</b> close one eye, "
    "then the other, and compare. <b>If the two images differ in anything "
    "beyond viewpoint, something is wrong</b> — and this is a class of "
    "bug that is invisible with both eyes open, because the brain works hard "
    "to conceal it."]),
 ],
 "resources": [
   ("LaValle &mdash; Virtual Reality, Chapters 4 and 6 (free)",
    "http://lavalle.pl/vr/",
    "Light, optics, and the visual physiology of this module, with the "
    "numbers and their sources."),
   ("Stanford EE267 &mdash; human visual system and stereo lectures (free)",
    "https://web.stanford.edu/class/ee267/",
    "The acuity, depth cue, and vergence-accommodation material, with "
    "demonstrations you can run."),
   ("Hoffman et al. &mdash; Vergence-accommodation conflicts hinder visual "
    "performance and cause visual fatigue (free)",
    "https://jov.arvojournals.org/article.aspx?articleid=2122610",
    "The study that quantified &sect;2's conflict. The measurements are "
    "what justify the 0.5–2 m rule."),
   ("Abrash &mdash; Down the VR rabbit hole: fixing judder (free)",
    "http://blogs.valvesoftware.com/abrash/",
    "Persistence, judder, and why low persistence mattered so much. The "
    "best explanation of &sect;3 anywhere."),
 ],
 "exercises": [
   "Measure your own visual acuity falloff: fix your gaze, have someone move "
   "a card of text sideways, and record the angle at which you can no longer "
   "read it.",
   "Compute the pixels per degree of a headset you have access to, from its "
   "resolution and field of view. Compare against 60 ppd.",
   "Compute how many pixels per eye a retinal-resolution headset would need "
   "at 200&deg;, and what that implies for rendering cost.",
   "In a VR scene, disable stereo (render both eyes from the same point). "
   "Describe what is lost, and then move your head and describe what is "
   "retained.",
   "Add a contact shadow under a floating object and compare the apparent "
   "depth with and without. This is the cheapest depth cue and the "
   "difference is larger than expected.",
   "Place text at 30 cm, 1 m, and 2 m in VR and read each for two minutes. "
   "Record the fatigue.",
   "Find the distance at which binocular fusion fails for you, by moving a "
   "virtual object steadily toward your face.",
   "Compare MSAA and TAA in a VR scene while turning your head. Describe the "
   "difference during motion rather than when still.",
   "Deliberately render an effect into one eye only and experience binocular "
   "rivalry. Then fix it.",
 ],
 "selfcheck": [
   "Give foveal acuity, human field of view, and typical headset figures for "
   "each.",
   "How does acuity vary with eccentricity, and what technique does that "
   "enable?",
   "What is the periphery good at and bad at, and what two design rules "
   "follow?",
   "Name seven depth cues and say which VR provides.",
   "Why does motion parallax do more work than stereopsis?",
   "Explain the vergence-accommodation conflict and give four mitigations.",
   "What is low persistence, what does it fix, and what does it cost?",
   "Why is motion blur wrong in VR, and why might MSAA beat TAA?",
   "What is binocular rivalry, what causes it, and how do you test for it?",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c650_b2", "c650_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
