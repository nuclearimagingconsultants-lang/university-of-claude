# -*- coding: utf-8 -*-
"""CSCE 649 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Articulated Bodies",
 "subtitle": "Jointed systems, and the two ways to represent them.",
 "question": "How do you simulate a skeleton that does not come apart?",
 "outcomes": [
     "Model common joints as constraints.",
     "Compare maximal and reduced coordinate formulations.",
     "Explain why long chains converge poorly and what to do about it.",
     "Add joint limits and motors.",
     "Build a ragdoll that behaves.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Joints are constraints",
   "blurb": "Module 04's machinery, applied to a skeleton."},

  {"t": "table", "kicker": "Joints", "title": "The standard joint types",
   "header": ["Joint", "Removes", "Leaves", "Example"],
   "widths": [2.6, 2.2, 2.2, 5.1],
   "rows": [
     ["Ball / spherical", "3 translation", "3 rotation", "Shoulder, hip"],
     ["<b>Hinge / revolute</b>", "3 + 2", "<b>1 rotation</b>", "<b>Knee, elbow, door</b>"],
     ["Prismatic / slider", "2 + 3", "1 translation", "Piston, drawer"],
     ["Fixed / weld", "all 6", "nothing", "Breakable joins"],
     ["Universal", "3 + 1", "2 rotation", "Drive shaft"],
   ],
   "footnote": "A rigid body has 6 degrees of freedom. A joint removes "
               "some; the constraint count equals the number removed.",
   "note": "Framing joints by degrees of freedom removed makes the "
           "constraint formulation obvious."},

  {"t": "callout", "title": "Every joint is a C(x) = 0 from Module 04",
   "kind": "Nothing new is needed",
   "body": ["A ball joint says two points — one fixed in each body — "
            "must coincide: <b>C = p_a − p_b = 0</b>. Three scalar "
            "constraints.",
            "A hinge adds that two axes must stay aligned, which removes two "
            "more rotational degrees of freedom.",
            "<b>So the solver from Module 04 and the contact solver from "
            "Module 06 handle joints without modification.</b> Joints are "
            "just more rows.",
            "<b>That unification is the practical point of this module.</b> "
            "A physics engine has one solver; joints, contacts, and friction "
            "all feed it."]},

  {"t": "section", "label": "Part 2", "title": "Two formulations",
   "blurb": "Represent every body, or represent only the freedoms."},

  {"t": "two", "kicker": "Coordinates", "title": "Maximal and reduced",
   "lh": "Maximal coordinates",
   "l": ["Every body has its full 6 DOF; joints are constraints.",
         "<b>Simple and uniform</b> — one code path for everything.",
         "<b>Joints can drift apart</b>; constraints are only approximately "
         "satisfied.",
         ("Scales well; handles loops naturally.", 1),
         "<b>What game engines use.</b>"],
   "rh": "Reduced coordinates",
   "r": ["Only the joint angles are state; positions are derived.",
         "<b>Joints cannot come apart</b> — they are not representable "
         "as broken.",
         "Fewer variables; no constraint drift.",
         ("Loops are awkward; contact is awkward.", 1),
         "<b>What robotics uses.</b>"],
   "note": "The trade is uniformity against exactness. Both are in "
           "production use for good reasons."},

  {"t": "callout", "title": "Featherstone: reduced coordinates in linear time",
   "kind": "The algorithm to know about",
   "body": ["The naive reduced-coordinate approach requires inverting a "
            "dense mass matrix — O(n³) in the number of joints.",
            "<b>Featherstone's articulated body algorithm does it in "
            "O(n)</b> by propagating articulated inertias along the "
            "kinematic tree, inward then outward.",
            "<b>It is exact</b>, not iterative, so joints are satisfied "
            "perfectly and there is no drift at any step size.",
            "<b>It is how every serious robotics simulator works</b> — "
            "MuJoCo, Drake, Bullet's featherstone path. Complicated to "
            "implement; the payoff is exactness and speed together."]},

  {"t": "section", "label": "Part 3", "title": "Chains",
   "blurb": "Where iterative solvers struggle."},

  {"t": "callout", "title": "Information travels one link per iteration",
   "kind": "The convergence problem",
   "body": ["Gauss–Seidel solves constraints in sequence. A correction at "
            "one end of a chain reaches the far end only after as many "
            "iterations as there are links.",
            "<b>A 100-link rope with 10 iterations</b> behaves as though the "
            "far end does not know the near end exists. It stretches "
            "visibly near the anchor.",
            "<b>This is not a bug and more iterations is not the "
            "answer</b> — the cost grows with chain length squared.",
            "<b>Fixes:</b> solve the chain in order rather than at random; "
            "use a hierarchical or multigrid solver; or use reduced "
            "coordinates, where the problem does not exist."]},

  {"t": "bullets", "kicker": "Mitigation", "title": "Making chains behave with an iterative solver",
   "items": [
     "<b>Order constraints along the chain</b>, root to tip. Information "
     "then propagates the full length in one pass.",
     "",
     "<b>Alternate direction</b> each iteration — forward, then backward. "
     "Removes the directional bias.",
     "",
     "<b>Increase mass toward the root.</b> A heavy anchor absorbs less "
     "correction, which is physically reasonable and helps convergence.",
     "",
     "<b>Hierarchical solve:</b> coarse chain first, then refine. The "
     "multigrid idea.",
     "",
     "<b>Substep.</b> Still the most reliable lever.",
   ],
   "footnote": "Ordering along the chain is nearly free and makes the "
               "largest difference."},

  {"t": "section", "label": "Part 4", "title": "Ragdolls",
   "blurb": "The application everyone wants."},

  {"t": "table", "kicker": "Ragdoll", "title": "What makes one look right",
   "header": ["Ingredient", "Why"],
   "widths": [3.6, 8.5],
   "rows": [
     ["<b>Joint limits</b>", "<b>Elbows that bend backwards look wrong immediately</b>"],
     ["Realistic mass ratios", "A head is ~8% of body mass; getting this wrong reads as odd"],
     ["Joint damping", "Real joints resist motion; undamped ragdolls flail"],
     ["<b>Self-collision</b>", "Limbs passing through the torso destroys the illusion"],
     ["<b>Blending to animation</b>", "<b>Pure ragdoll looks dead; blend in and out</b>"],
   ],
   "footnote": "The last row is why game ragdolls look better than physically "
               "more accurate ones.",
   "note": "Joint limits and mass ratios are the cheap wins. Blending is the "
           "production technique."},

  {"t": "callout", "title": "Joint limits are inequality constraints",
   "kind": "Which makes them contacts",
   "body": ["A knee may bend from 0° to 150°. That is "
            "<b>C = θ ≥ 0</b> and <b>C = 150° − θ ≥ 0</b> — two "
            "inequality constraints.",
            "<b>Inequality constraints are exactly what contact is</b> "
            "(Module 06), so they go into the same solver with the same "
            "treatment: active only when violated, non-negative impulse, "
            "slop.",
            "<b>Make them soft rather than hard.</b> A hard limit produces a "
            "sudden stop that looks mechanical; a small amount of compliance "
            "(Module 04) reads as flesh.",
            "<b>Limits are the single cheapest improvement to a ragdoll.</b>"]},

  {"t": "bullets", "kicker": "Motors", "title": "Driving a skeleton",
   "items": [
     "<b>A motor is a constraint with a target</b>: drive the joint toward a "
     "desired angle or angular velocity, with a maximum force.",
     "",
     "<b>The force limit matters.</b> An unlimited motor is a teleporter and "
     "will fight contacts until something breaks.",
     "",
     "<b>PD control</b> — proportional plus derivative — is the usual "
     "driver. Tuning it is most of the work.",
     "",
     "<b>This is how physically-driven characters work:</b> an animation "
     "supplies target angles and motors try to achieve them against gravity "
     "and contact.",
     "",
     "<b>And how they fail:</b> gains too low and the character collapses; "
     "too high and it fights the world rigidly.",
   ],
   "note": "PD gains are the thing nobody can tune on the first attempt. "
           "Worth saying."},
 ],
 "takeaways": [
   "A joint removes degrees of freedom, and each removed freedom is one "
   "scalar constraint — so Module 04's solver handles joints unchanged.",
   "Maximal coordinates give every body 6 DOF and enforce joints as "
   "constraints: simple, uniform, and joints can drift apart.",
   "Reduced coordinates store only joint angles, so joints cannot come "
   "apart; Featherstone's algorithm solves them exactly in O(n).",
   "In an iterative solver, information travels one link per iteration, so "
   "long chains stretch. Ordering along the chain is the cheap fix.",
   "Joint limits are inequality constraints — the same machinery as "
   "contact — and are the cheapest improvement to a ragdoll.",
   "Motors are constraints with a target and a force limit. Unlimited motors "
   "fight contacts until something breaks.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Joints are constraints"),
  ("p", "A free rigid body has six degrees of freedom: three translational "
        "and three rotational. A joint removes some of them, and <b>the "
        "number of scalar constraints a joint imposes equals the number of "
        "degrees of freedom it removes</b>."),
  ("table", ["Joint", "DOF removed", "DOF remaining", "Constraint"],
   [["<b>Ball / spherical</b>", "3 translational", "3 rotational",
     "Two points, one fixed in each body, must coincide: "
     "C = <b>p</b><sub>a</sub> &minus; <b>p</b><sub>b</sub> = 0."],
    ["<b>Hinge / revolute</b>", "3 translational + 2 rotational",
     "<b>1 rotational</b>",
     "Ball joint, plus two axes must remain aligned."],
    ["<b>Prismatic / slider</b>", "2 translational + 3 rotational",
     "1 translational",
     "Motion confined to a line; orientation fully locked."],
    ["<b>Fixed / weld</b>", "all 6", "none",
     "Used for joins that may later break under load — &lambda; from "
     "Module 04 gives you the force being transmitted, which is exactly the "
     "breaking criterion."],
    ["<b>Universal</b>", "3 translational + 1 rotational", "2 rotational",
     "Two perpendicular hinges sharing a point."]],
   [0.16, 0.22, 0.16, 0.46]),
  ("callout", "No new machinery is required",
   ["Every joint is a constraint function C(x) = 0 of exactly the kind "
    "Module 04 introduced. The gradient gives the direction, the Lagrange "
    "multiplier gives the magnitude, and the same projection or impulse "
    "solver enforces it.",
    "<b>So joints, contacts, friction, and joint limits all feed one "
    "solver.</b> A physics engine does not have a joint subsystem and a "
    "contact subsystem; it has a constraint solver, and these are different "
    "kinds of row.",
    "<b>This unification is the practical content of this module.</b> Once "
    "you see it, articulated bodies stop being a separate topic and become "
    "an application of what you already have."]),

  ("h1", "2 &nbsp; Maximal and reduced coordinates"),
  ("table", ["", "Maximal coordinates", "Reduced coordinates"],
   [["State", "Every body carries its full 6 DOF. Joints are enforced as "
     "constraints between them.",
     "Only the joint angles are state. Body positions are <i>derived</i> by "
     "walking the kinematic tree."],
    ["Simplicity", "<b>Simple and uniform.</b> Free bodies, jointed bodies, "
     "and contacts all go through the same path.",
     "More complex. The kinematic tree, its traversal, and the Jacobians all "
     "have to be built."],
    ["Joint exactness", "<b>Approximate.</b> The solver satisfies the "
     "constraint to within its tolerance, so joints visibly separate under "
     "load.",
     "<b>Exact.</b> A broken joint is not representable, because the "
     "coordinates cannot express one."],
    ["Variable count", "6 per body, plus constraints.",
     "1–3 per joint. Far fewer."],
    ["Closed loops", "<b>Natural</b> — just another constraint.",
     "<b>Awkward</b> — a loop breaks the tree structure and requires "
     "additional constraints anyway."],
    ["Contact", "Natural — contacts are constraints like any other.",
     "Awkward — contact acts on bodies, which are not the state "
     "variables."],
    ["Used by", "<b>Game engines.</b> Bullet, PhysX, Havok, Box2D.",
     "<b>Robotics.</b> MuJoCo, Drake, and control applications generally."]],
   [0.13, 0.43, 0.44]),
  ("callout", "Featherstone's algorithm",
   ["The direct reduced-coordinate approach requires forming and inverting "
    "the joint-space mass matrix, which is dense and gives an "
    "O(n&#179;) cost in the number of joints — prohibitive for a "
    "detailed character.",
    "<b>Featherstone's articulated body algorithm computes the same answer "
    "in O(n)</b> by propagating <i>articulated inertias</i> along the "
    "kinematic tree: an inward pass accumulating the effective inertia each "
    "link presents to its parent, then an outward pass computing "
    "accelerations.",
    "<b>It is exact rather than iterative.</b> Joints are satisfied "
    "perfectly at every step, at any step size, with no drift and no "
    "convergence parameter.",
    "<b>Every serious robotics simulator is built on it</b>, and Bullet "
    "offers it alongside its maximal-coordinate path. It is genuinely "
    "complicated to implement, and the payoff — exactness and linear "
    "cost simultaneously — is why it is worth knowing exists even if "
    "you never write one."]),

  ("break",),
  ("h1", "3 &nbsp; Chains"),
  ("callout", "Information travels one link per iteration",
   ["Gauss&ndash;Seidel satisfies constraints one at a time in sequence. "
    "When a correction is applied at one constraint, the neighbouring "
    "constraint sees it on the next visit — and the one after that on "
    "the visit after.",
    "<b>So a disturbance at one end of a chain reaches the other end only "
    "after as many iterations as there are links.</b> A 100-link rope "
    "solved with 10 iterations behaves as though the far end is unaware the "
    "anchor exists; the chain stretches visibly near the top, where the load "
    "is greatest.",
    "<b>This is not a bug, and raising the iteration count is not a "
    "solution.</b> Full convergence needs iterations proportional to chain "
    "length, and each iteration costs time proportional to chain length "
    "too — so the cost grows as the square.",
    "<b>It is also why PBD ropes look slightly elastic</b> however the "
    "stiffness is set, and why rigid chains are one of the places reduced "
    "coordinates genuinely win."]),
  ("ul", ["<b>Order the constraints along the chain</b>, from root to tip. "
          "A single forward pass then propagates information the entire "
          "length, because each constraint is visited after the one before "
          "it has already been corrected. <b>This is nearly free and makes "
          "the largest single difference.</b>",
          "<b>Alternate the direction</b> each iteration — forward, "
          "then backward. A purely forward sweep biases the solution toward "
          "the tip; alternating removes the asymmetry.",
          "<b>Increase mass toward the root.</b> A heavier anchor absorbs "
          "proportionally less correction, which is both physically "
          "reasonable for most real chains and helpful for convergence.",
          "<b>Solve hierarchically.</b> Treat the chain coarsely first "
          "— every fourth link — then refine. This is the "
          "multigrid idea, and it converges in O(log n) passes rather than "
          "O(n).",
          "<b>Substep.</b> As in every other module, smaller steps with "
          "fewer iterations outperform larger steps with more."]),

  ("h1", "4 &nbsp; Ragdolls"),
  ("table", ["Ingredient", "Why it matters"],
   [["<b>Joint limits</b>",
     "<b>An elbow that bends backwards is noticed instantly</b>, even by "
     "someone who could not say what is wrong. The cheapest single "
     "improvement."],
    ["<b>Realistic mass ratios</b>",
     "A human head is about 8% of body mass, a forearm about 2%. Uniform "
     "masses produce motion that reads as subtly wrong — limbs swing "
     "with the wrong period."],
    ["<b>Joint damping</b>",
     "Real joints resist motion through soft tissue. An undamped ragdoll "
     "flails in a way that reads as weightless rather than limp."],
    ["<b>Self-collision</b>",
     "An arm passing through the torso destroys the illusion completely. "
     "Expensive, and necessary."],
    ["<b>Blending with animation</b>",
     "<b>A pure ragdoll looks dead</b>, because a falling person is not "
     "passive — they brace, reach, and tense. Production systems blend "
     "from animation into ragdoll on impact and sometimes back out again, "
     "which is why game ragdolls often look better than physically more "
     "faithful ones."]],
   [0.22, 0.78]),
  ("callout", "Joint limits are inequality constraints, so they are contacts",
   ["A knee bends from roughly 0&deg; to 150&deg;. Expressed as constraints: "
    "C = &theta; &ge; 0 and C = 150&deg; &minus; &theta; &ge; 0. Two "
    "<b>inequality</b> constraints.",
    "<b>Inequality constraints are exactly what contact is</b> (Module 06), "
    "so they go into the same solver with the same treatment: active only "
    "when violated, impulse clamped to be non-negative, a small slop to "
    "prevent oscillation at the boundary.",
    "<b>Make them slightly soft.</b> A perfectly hard limit stops the "
    "joint dead, which reads as mechanical — a hinge rather than a "
    "body. A small compliance (Module 04's &alpha;) gives a short "
    "deceleration that reads as flesh and ligament.",
    "<b>This is the single cheapest improvement available to a ragdoll</b>, "
    "and it is routinely skipped in first implementations because the "
    "ragdoll 'works' without it."]),
  ("h1", "5 &nbsp; Motors"),
  ("ul", ["<b>A motor is a constraint with a target and a force limit:</b> "
          "drive this joint toward a desired angle, or a desired angular "
          "velocity, using no more than this much torque.",
          "<b>The force limit is the important part.</b> An unlimited motor "
          "is effectively a teleporter — it will achieve its target "
          "regardless of what is in the way, fighting contacts and other "
          "constraints until the solver fails or something is flung across "
          "the scene.",
          "<b>PD control</b> — torque proportional to angle error plus "
          "a term proportional to angular velocity error — is the "
          "standard driver. <b>Tuning the two gains is most of the work</b>, "
          "and nobody gets it right on the first attempt.",
          "<b>This is how physically-driven characters work:</b> an "
          "animation supplies target joint angles frame by frame, and motors "
          "attempt to achieve them while gravity, contact, and momentum act "
          "on the body. The character responds to being pushed because the "
          "motors are not infinitely strong.",
          "<b>And this is how they fail.</b> Gains too low and the character "
          "sags and collapses under its own weight; too high and it becomes "
          "a rigid armature that ignores the world and jitters against it. "
          "The usable range is narrower than it looks."]),
 ],
 "resources": [
   ("Featherstone &mdash; Rigid Body Dynamics Algorithms",
    "http://royfeatherstone.org/",
    "The reduced-coordinate algorithm of &sect;2, from its author. His site "
    "has free tutorial material and spatial-vector notes."),
   ("Erin Catto &mdash; joints and motors (GDC, free)",
    "https://box2d.org/publications/",
    "The maximal-coordinate side: joint constraints, limits, and motors as "
    "implemented in a production engine."),
   ("Bullet Physics manual and source",
    "https://github.com/bulletphysics/bullet3",
    "Both formulations in one codebase — compare "
    "<code>btGeneric6DofConstraint</code> against the Featherstone path."),
   ("Ten Minute Physics &mdash; chains and ragdoll episodes",
    "https://matthias-research.github.io/pages/tenMinutePhysics/",
    "The chain convergence problem of &sect;3, demonstrated interactively."),
 ],
 "exercises": [
   "Implement ball and hinge joints as constraints in your Module 04 solver. "
   "Verify the constrained degrees of freedom are actually removed.",
   "Build a chain of 100 links. Plot the stretch along its length for 1, 10, "
   "and 100 solver iterations.",
   "Reorder the constraints along the chain and repeat. Report the "
   "improvement.",
   "Implement alternating-direction sweeps and measure the difference "
   "against a single-direction sweep.",
   "Implement a hierarchical chain solve and compare convergence against the "
   "flat solver at equal cost.",
   "Build a ragdoll with realistic mass ratios, taken from published "
   "anthropometric data. Compare against uniform masses.",
   "Add joint limits as inequality constraints. Compare a hard limit against "
   "a compliant one and describe the difference in how the motion reads.",
   "Implement a PD motor on a single joint and tune the gains. Document the "
   "gain values at which the joint sags and at which it becomes rigid.",
   "Drive a ragdoll's joints toward an animated pose with limited motors. "
   "Push it and observe the recovery.",
   "Write a page comparing maximal and reduced coordinates for a specific "
   "application of your choosing, and justify a recommendation.",
 ],
 "selfcheck": [
   "How many constraints does a joint impose, and how do you know?",
   "Give the constraint functions for a ball joint and a hinge.",
   "Compare maximal and reduced coordinates on five axes.",
   "What does Featherstone's algorithm achieve, and why does it matter?",
   "Why do long chains converge poorly in an iterative solver, and why does "
   "raising the iteration count not solve it?",
   "Give four mitigations for the chain problem.",
   "Name five ingredients of a convincing ragdoll.",
   "Why are joint limits inequality constraints, and why make them soft?",
   "What is a motor, why does the force limit matter, and how do PD gains "
   "fail in each direction?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Deformable Solids",
 "subtitle": "Continuum mechanics, and why mass-spring was never going to "
             "work.",
 "question": "How do you simulate a material rather than a mesh?",
 "outcomes": [
     "Define strain and stress and explain what each measures.",
     "Explain why linear elasticity fails under rotation.",
     "Implement corotational FEM.",
     "Handle element inversion.",
     "Choose between FEM, mass-spring, and shape matching.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Strain",
   "blurb": "Measuring deformation without measuring motion."},

  {"t": "callout", "title": "The central problem: rotation is not deformation",
   "kind": "What strain must achieve",
   "body": ["Rotate a rubber block by 90°. Every vertex has moved a long "
            "way. <b>The material has not deformed at all.</b>",
            "<b>A strain measure must report zero for any rigid "
            "motion</b> — translation or rotation — and non-zero only "
            "for genuine stretching, compression, or shear.",
            "<b>Mass-spring models fail this test.</b> A spring sees only "
            "distance between endpoints, which is why a mass-spring cube can "
            "be inverted with every spring at rest length.",
            "<b>Getting this right is what continuum mechanics buys</b>, and "
            "it is the whole reason this module exists."]},

  {"t": "eq", "kicker": "Deformation", "title": "The deformation gradient",
   "eqs": [
     ("F  =  ∂x / ∂X",
      "How deformed positions x change with material positions X. A 3×3 "
      "matrix per element. Everything derives from it."),
     ("ε = ½(F + Fᵀ) − I",
      "Linear (Cauchy) strain. Cheap — and WRONG under rotation."),
     ("E = ½(FᵀF − I)",
      "Green strain. Exactly zero for any rotation, because RᵀR = I. "
      "Nonlinear in the displacements."),
   ],
   "caption": "FᵀF removes the rotation because rotations are orthogonal. "
              "That one identity is the whole trick.",
   "note": "Show RᵀR = I explicitly. The reason Green strain works is a "
           "one-line observation."},

  {"t": "callout", "title": "Linear strain fails visibly, and famously",
   "kind": "The artefact everyone has seen",
   "body": ["Cauchy strain is linear in displacement, which makes the solver "
            "a single linear system — fast and easy.",
            "<b>It reports non-zero strain for a pure rotation</b>, so the "
            "material resists being rotated.",
            "<b>The visible result is ghost forces and volume growth</b>: an "
            "arm rotating at the shoulder inflates. This is the classic "
            "linear-FEM artefact.",
            "<b>It is fine for small deformations</b> — a loaded beam, a "
            "vibrating plate. It is useless for animation, where everything "
            "rotates."]},

  {"t": "section", "label": "Part 2", "title": "Stress and energy",
   "blurb": "From deformation to force."},

  {"t": "table", "kicker": "Models", "title": "Constitutive models",
   "header": ["Model", "Description", "Use"],
   "widths": [2.9, 4.8, 4.4],
   "rows": [
     ["<b>St. Venant–Kirchhoff</b>", "Linear stress from Green strain", "<b>Collapses under compression</b>"],
     ["<b>Neo-Hookean</b>", "Nonlinear; resists compression strongly", "<b>The usual choice</b>"],
     ["Mooney–Rivlin", "More parameters, better fits", "Matching measured rubber"],
     ["<b>Corotational</b>", "<b>Linear, with rotation factored out</b>", "<b>Fast, stable, good enough</b>"],
   ],
   "footnote": "Parameters are Young's modulus E and Poisson's ratio "
               "ν — both measurable, both published for real "
               "materials.",
   "note": "That the parameters are real measurable quantities is the "
           "practical payoff over mass-spring."},

  {"t": "eq", "kicker": "Parameters", "title": "Real material parameters",
   "eqs": [
     ("E  —  Young's modulus",
      "Resistance to stretching, in pascals. Rubber ≈ 10⁷; steel "
      "≈ 2×10¹¹."),
     ("ν  —  Poisson's ratio",
      "How much it bulges sideways when squeezed. 0.5 is "
      "incompressible; rubber ≈ 0.49."),
     ("Look them up, do not tune them",
      "Unlike spring constants, these are published for real materials and "
      "transfer across meshes."),
   ],
   "caption": "ν near 0.5 makes the system nearly incompressible, which is "
              "numerically hard. 0.45 is the usual compromise.",
   "note": "The locking problem at ν→0.5 is worth mentioning — it is why "
           "nobody uses 0.499."},

  {"t": "section", "label": "Part 3", "title": "Corotational FEM",
   "blurb": "The method that made deformables practical."},

  {"t": "code", "kicker": "Corotational", "title": "Factor out the rotation, then go linear",
   "lang": "cpp", "code": """
// Per element, per step:
for (auto& e : elements) {
    // 1. Deformation gradient from the current vertex positions.
    mat3 F = compute_F(e, x);

    // 2. Polar decomposition F = R * S.  R is the rotation part;
    //    S is the symmetric stretch part. THIS is the key step.
    mat3 R = polar_decomposition_rotation(F);

    // 3. Rotate the element back to its rest orientation, apply the
    //    cheap LINEAR model there, then rotate the forces forward.
    //    Linear elasticity is correct when there is no rotation left.
    mat3 Fhat = R.transpose() * F;             // rotation removed
    mat3 P    = linear_stress(Fhat);           // cheap and now valid
    accumulate_forces(e, R * P);               // rotate forces back
}
// Cost: one polar decomposition per element per step. Result: linear
// elasticity's speed with none of its rotation artefacts.
""",
   "caption": "Linear elasticity is wrong only because of rotation. Remove "
              "the rotation and it becomes correct again.",
   "note": "The insight is almost embarrassingly simple and it is why "
           "corotational FEM is everywhere."},

  {"t": "callout", "title": "Polar decomposition is the whole method",
   "kind": "Why it works",
   "body": ["Any deformation gradient F factors as <b>F = R·S</b>: a "
            "rotation followed by a symmetric stretch.",
            "<b>R is the rotation the element has undergone</b>; S is the "
            "actual deformation.",
            "<b>Linear elasticity is accurate for small deformation with no "
            "rotation.</b> Factor R out and that condition is satisfied, so "
            "the cheap model becomes valid.",
            "<b>Cost is one polar decomposition per element per step</b> "
            "— a few iterations of a simple algorithm, or a closed form "
            "in 3D. You get linear speed with nonlinear correctness under "
            "rotation."]},

  {"t": "callout", "title": "Inverted elements must be handled, not prevented",
   "kind": "The robustness problem",
   "body": ["Under a large impact a tetrahedron can turn inside out: "
            "<b>det F < 0</b>.",
            "<b>Most models produce garbage there.</b> Forces point the "
            "wrong way, the element inverts further, and the simulation "
            "fails.",
            "<b>You cannot reliably prevent it</b>, so handle it: Irving, "
            "Teran and Fedkiw's method clamps the singular values of F and "
            "<b>extends the model smoothly into the inverted regime</b>, so "
            "forces push the element back out.",
            "<b>Without this, a deformable simulation is one bad frame away "
            "from failure.</b> With it, inversion is recoverable and often "
            "invisible."]},

  {"t": "section", "label": "Part 4", "title": "Alternatives",
   "blurb": "What else is used, and when."},

  {"t": "table", "kicker": "Comparison", "title": "Three approaches",
   "header": ["Method", "Strength", "Weakness"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["<b>FEM</b>", "<b>Real parameters; converges with mesh</b>", "Complex; needs a solver"],
     ["Mass-spring", "Trivial to implement; fast", "<b>Mesh-dependent; no volume</b>"],
     ["<b>Shape matching</b>", "<b>Unconditionally stable; very fast</b>", "Not a material model"],
     ["<b>MPM</b>", "<b>Handles topology change, plasticity</b>", "Expensive; grid artefacts"],
   ],
   "footnote": "Shape matching is to deformables what PBD is to constraints "
               "— theoretically weak, practically ubiquitous.",
   "note": "MPM is covered in Module 12. Mention it here as the "
           "topology-change answer."},

  {"t": "callout", "title": "Why FEM beats mass-spring, concretely",
   "kind": "The case",
   "body": ["<b>Parameters are real.</b> Young's modulus for rubber is "
            "published. There is no published spring constant for rubber.",
            "<b>Behaviour converges with mesh refinement</b> rather than "
            "changing, so a finer mesh is more detail and not a different "
            "material.",
            "<b>Volume is represented.</b> An element knows it has been "
            "inverted; a spring network does not.",
            "<b>Anisotropy can be specified</b> rather than emerging from "
            "the triangulation.",
            "<b>The cost is a linear solve per step</b> and considerably "
            "more implementation. For anything that must behave like a "
            "specific material, it is worth it."]},
 ],
 "takeaways": [
   "A strain measure must report zero for any rigid motion. Mass-spring "
   "models fail this, which is their fundamental defect.",
   "Everything derives from the deformation gradient F. Green strain "
   "&frac12;(F&#7488;F &minus; I) is zero under rotation because "
   "R&#7488;R = I.",
   "Linear Cauchy strain is cheap and reports non-zero strain for pure "
   "rotation, which produces ghost forces and inflating limbs.",
   "Material parameters are Young's modulus and Poisson's ratio — "
   "measurable, published, and transferable, unlike spring constants.",
   "Corotational FEM polar-decomposes F = R&middot;S, removes the rotation, "
   "and applies the cheap linear model where it is valid.",
   "Element inversion cannot be prevented, only handled — clamp the "
   "singular values and extend the model into the inverted regime.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Strain"),
  ("callout", "Rotation is not deformation, and that is the whole difficulty",
   ["Take a rubber block and rotate it by 90&deg;. Every vertex has moved "
    "a long way. <b>The material has not deformed in the slightest</b>, and "
    "no internal forces should arise.",
    "<b>So any strain measure must report exactly zero for a rigid "
    "motion</b> — translation or rotation — and non-zero only "
    "for genuine stretching, compression, or shear.",
    "<b>Mass-spring models fail this test fundamentally.</b> A spring "
    "measures only the distance between its endpoints, which carries no "
    "information about the configuration of the surrounding material. This "
    "is why a mass-spring cube can be turned inside out with every spring at "
    "its rest length: the springs are individually content and the material "
    "is destroyed.",
    "<b>Getting this right is precisely what continuum mechanics buys</b>, "
    "and it is why this module exists."]),
  ("eq", "F = &part;x / &part;X"),
  ("p", "The <b>deformation gradient</b> F relates deformed positions x to "
        "material (rest) positions X. For a tetrahedral element it is a "
        "3&times;3 matrix computed from the current and rest vertex "
        "positions, and <b>everything else in this module derives from "
        "it</b>."),
  ("table", ["Strain measure", "Definition", "Under pure rotation"],
   [["<b>Cauchy (linear)</b>",
     "&epsilon; = &frac12;(F + F<super>T</super>) &minus; I",
     "<b>Non-zero. Wrong.</b> Reports strain for a rotation, so the material "
     "resists being rotated."],
    ["<b>Green (nonlinear)</b>",
     "E = &frac12;(F<super>T</super>F &minus; I)",
     "<b>Exactly zero</b>, because a rotation R satisfies "
     "R<super>T</super>R = I, so F<super>T</super>F = I and E = 0."]],
   [0.19, 0.30, 0.51]),
  ("p", "<b>That identity is the entire trick.</b> Rotations are orthogonal, "
        "so forming F<super>T</super>F annihilates them and leaves only the "
        "stretch. The cost is that Green strain is quadratic in the "
        "displacements, so the resulting system is nonlinear and requires an "
        "iterative solve rather than a single linear one."),
  ("callout", "The linear-elasticity artefact everyone has seen",
   ["Cauchy strain is linear in displacement, which makes the whole system "
    "linear: assemble a stiffness matrix once, solve one linear system per "
    "step. It is fast, simple, and well understood.",
    "<b>And it reports non-zero strain for a pure rotation</b>, so the model "
    "generates internal forces resisting a motion that does not deform the "
    "material at all.",
    "<b>The visible result is ghost forces and volume growth.</b> A "
    "character's arm rotating at the shoulder <i>inflates</i> — the "
    "classic linear-FEM artefact, immediately recognisable once you know to "
    "look for it, and present in a great deal of early deformable-character "
    "work.",
    "<b>Linear elasticity is perfectly appropriate for small "
    "deformations</b> — a loaded beam deflecting a few millimetres, a "
    "vibrating plate — which is what it was developed for. It is "
    "useless for animation, where large rotations are the normal case."]),

  ("h1", "2 &nbsp; Stress and constitutive models"),
  ("p", "Strain measures deformation; <b>stress</b> is the internal force per "
        "unit area that results. The relationship between them is the "
        "<b>constitutive model</b>, and it is where the material's identity "
        "lives."),
  ("table", ["Model", "Character", "Assessment"],
   [["<b>St. Venant&ndash;Kirchhoff</b>",
     "Linear stress computed from Green strain. The simplest model that is "
     "rotation-correct.",
     "<b>Collapses under compression.</b> The energy is non-convex for "
     "compressed states, so a heavily squashed element is happy to collapse "
     "to zero volume. Not usable for large deformation."],
    ["<b>Neo-Hookean</b>",
     "Nonlinear, derived from a hyperelastic energy with a term that "
     "diverges as volume approaches zero.",
     "<b>The usual choice.</b> Resists compression strongly and correctly, "
     "behaves sensibly under large deformation, and has two parameters that "
     "map onto measurable quantities."],
    ["<b>Mooney&ndash;Rivlin</b>",
     "More parameters, fitted to measured stress&ndash;strain curves.",
     "Used when matching a specific real rubber matters. Rarely necessary "
     "in graphics."],
    ["<b>Corotational</b>",
     "<b>Linear elasticity with the rotation factored out</b> (&sect;3).",
     "<b>Fast, stable, and good enough for most animation.</b> The practical "
     "default."]],
   [0.19, 0.36, 0.45]),
  ("table", ["Parameter", "Measures", "Typical values"],
   [["<b>Young's modulus E</b>",
     "Resistance to stretching, in pascals.",
     "Rubber &asymp; 10<super>7</super> Pa; soft tissue "
     "10<super>4</super>&ndash;10<super>6</super>; steel &asymp; 2 &times; "
     "10<super>11</super>."],
    ["<b>Poisson's ratio &nu;</b>",
     "How much the material bulges sideways when compressed.",
     "0.5 is perfectly incompressible; rubber &asymp; 0.49; cork &asymp; 0; "
     "most metals &asymp; 0.3."]],
   [0.22, 0.33, 0.45]),
  ("p", "<b>These are real, published, measurable quantities</b>, and that "
        "is the practical payoff over mass-spring models. You can look up "
        "the Young's modulus of silicone rubber. There is no published "
        "spring constant for silicone rubber, and there could not be, "
        "because it would depend on your mesh."),
  ("p", "<b>A caution:</b> &nu; approaching 0.5 makes the material nearly "
        "incompressible, which is numerically difficult — the system "
        "becomes ill-conditioned and standard elements exhibit "
        "<b>locking</b>, becoming artificially stiff. Most practitioners use "
        "0.45 and accept slight compressibility rather than fight it."),

  ("break",),
  ("h1", "3 &nbsp; Corotational FEM"),
  ("code", """for (auto& e : elements) {
    mat3 F    = compute_F(e, x);                 // deformation gradient
    mat3 R    = polar_decomposition_rotation(F); // F = R * S
    mat3 Fhat = R.transpose() * F;               // rotation removed
    mat3 P    = linear_stress(Fhat);             // cheap model, now valid
    accumulate_forces(e, R * P);                 // rotate forces back
}"""),
  ("callout", "Polar decomposition is the entire method",
   ["Any deformation gradient factors uniquely as <b>F = R &middot; S</b>, "
    "where R is a rotation and S is a symmetric positive-definite stretch. "
    "This is the <b>polar decomposition</b>, and it separates 'how the "
    "element has been turned' from 'how it has been deformed'.",
    "<b>Linear elasticity is accurate for small deformations when there is "
    "no rotation.</b> Its only failure, as &sect;1 established, is under "
    "rotation. So: factor out R, apply the cheap linear model in the "
    "element's own rotated frame where it is valid, and rotate the resulting "
    "forces back into world space.",
    "<b>The cost is one polar decomposition per element per step</b> "
    "— a few iterations of a simple fixed-point algorithm, or a "
    "closed-form expression in 3D. Cheap.",
    "<b>The result is linear elasticity's speed and simplicity with none of "
    "its rotation artefacts.</b> The insight is almost embarrassingly "
    "simple, which is exactly why corotational FEM became the default for "
    "interactive deformables."]),
  ("callout", "Element inversion must be handled, not prevented",
   ["Under a sufficiently violent impact, a tetrahedron can turn inside out: "
    "its deformation gradient has <b>det F &lt; 0</b>.",
    "<b>Most constitutive models produce nonsense in that regime.</b> The "
    "forces point in the wrong direction, driving the element further "
    "inverted, which produces larger wrong forces. The simulation fails "
    "within a few steps, and the failure propagates to neighbouring "
    "elements.",
    "<b>You cannot reliably prevent inversion</b> — doing so would "
    "require bounding the forces the rest of the scene can apply, which is "
    "not under your control. So it has to be survivable.",
    "<b>Irving, Teran and Fedkiw's approach</b> takes the singular value "
    "decomposition of F, clamps the singular values away from zero, and "
    "<b>extends the constitutive model smoothly into the inverted "
    "regime</b> so that the forces push the element back out rather than "
    "further in. <b>Without this, a deformable simulation is one bad frame "
    "from failure; with it, inversion is recoverable and usually "
    "invisible.</b>"]),

  ("h1", "4 &nbsp; Alternatives"),
  ("table", ["Method", "Strengths", "Weaknesses"],
   [["<b>FEM</b>",
     "<b>Real material parameters.</b> Behaviour converges as the mesh "
     "refines. Volume is represented. Anisotropy can be specified.",
     "Substantially more complex. Requires a linear solver, and an implicit "
     "one for stiff materials."],
    ["<b>Mass-spring</b>",
     "Trivial to implement; fast; adequate when art-directed.",
     "<b>Mesh-dependent behaviour; no volume preservation; parameters are "
     "not material properties</b> (Module 03)."],
    ["<b>Shape matching</b>",
     "<b>Unconditionally stable and very fast.</b> Match the current point "
     "cloud to the rest shape with a best-fit rigid transform and pull "
     "toward it.",
     "<b>Not a material model at all.</b> No concept of stress; stiffness "
     "depends on solver settings. This is to deformables what PBD is to "
     "constraints — theoretically weak and practically ubiquitous."],
    ["<b>MPM</b>",
     "<b>Handles topology change, plasticity, fracture, granular "
     "materials</b> — snow, sand, mud. Module 12.",
     "Expensive, and inherits grid artefacts from its Eulerian half."]],
   [0.15, 0.42, 0.43]),
  ("callout", "The concrete case for FEM over mass-spring",
   ["<b>Parameters are real.</b> Young's modulus for silicone is in a "
    "handbook. A spring constant for silicone is not, and cannot be.",
    "<b>Behaviour converges under refinement.</b> A finer mesh gives more "
    "detail of the same material, rather than a different material "
    "(Module 03's three-resolution test).",
    "<b>Volume is represented.</b> An element knows its own volume and knows "
    "when it has been inverted. A spring network has no such concept, which "
    "is why mass-spring solids collapse.",
    "<b>Anisotropy is specifiable</b> rather than an accident of the "
    "triangulation — muscle fibre direction, wood grain, fabric warp.",
    "<b>The cost is a linear solve per step and considerably more code.</b> "
    "For anything that must behave like a <i>particular</i> material, or "
    "that must survive mesh changes, it is worth it. For a gelatinous blob "
    "that only has to look fun, it is not."]),
 ],
 "resources": [
   ("Sifakis & Barbi&#269; &mdash; FEM Simulation of 3D Deformable Solids "
    "(SIGGRAPH course, free)",
    "https://viterbi-web.usc.edu/~jbarbic/femdefo/",
    "The best free introduction to this module. Notes and slides covering "
    "everything from the deformation gradient to implicit integration."),
   ("M&uuml;ller et al. &mdash; Meshless Deformations Based on Shape "
    "Matching (free)",
    "https://matthias-research.github.io/pages/publications/publications.html",
    "The shape-matching method of &sect;4, from its authors."),
   ("Irving, Teran & Fedkiw &mdash; Invertible Finite Elements (2004, free)",
    "https://physbam.stanford.edu/~fedkiw/",
    "The inversion handling of &sect;3. Essential if you want a deformable "
    "simulation that survives contact."),
   ("M&uuml;ller & Gross &mdash; Interactive Virtual Materials (free)",
    "https://matthias-research.github.io/pages/publications/publications.html",
    "The corotational formulation of &sect;3, clearly presented."),
   ("Bargteil & Shinar &mdash; Introduction to Physics-Based Animation",
    "https://dl.acm.org/doi/10.1145/3214834.3214849",
    "The deformables chapters tie &sect;1&ndash;&sect;4 together well."),
 ],
 "exercises": [
   "Compute the deformation gradient for a tetrahedron and verify it is "
   "exactly the identity for a rigid translation and a rotation matrix for a "
   "rigid rotation.",
   "Implement both Cauchy and Green strain. Apply a pure 45&deg; rotation "
   "and report what each measure returns.",
   "Implement linear FEM and rotate a bar by 90&deg;. Measure the volume "
   "change and document the inflation artefact.",
   "Implement polar decomposition and verify F = R&middot;S with R "
   "orthogonal and S symmetric.",
   "Implement corotational FEM and repeat the rotating-bar test. The volume "
   "change should now be negligible — report both numbers side by "
   "side.",
   "Simulate the same object with Young's modulus spanning three orders of "
   "magnitude and confirm the behaviour matches expectation for the "
   "materials those values correspond to.",
   "Vary Poisson's ratio from 0 to 0.49 and observe the bulging. Then try "
   "0.499 and document the conditioning problem.",
   "Force an element to invert by driving a collider through the object. "
   "Document the failure, then implement singular value clamping and show "
   "recovery.",
   "Implement shape matching and compare against corotational FEM on the "
   "same mesh: stability, speed, and whether the parameters mean anything.",
   "Run the three-resolution test from Module 03 on your FEM solid. It "
   "should pass where mass-spring failed.",
 ],
 "selfcheck": [
   "Why must a strain measure report zero for rigid motion, and why do "
   "mass-spring models fail this?",
   "What is the deformation gradient, and what derives from it?",
   "Why is Green strain zero under rotation? Give the one-line reason.",
   "What artefact does linear elasticity produce, and when is it acceptable "
   "anyway?",
   "Name four constitutive models and say when each is appropriate.",
   "What are Young's modulus and Poisson's ratio, and why does it matter "
   "that they are measurable?",
   "Explain corotational FEM in three steps.",
   "What is polar decomposition and why does factoring out R make linear "
   "elasticity valid?",
   "Why can element inversion not be prevented, and how is it handled?",
   "Give four concrete advantages of FEM over mass-spring.",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Cloth and Hair",
 "subtitle": "Thin materials, where everything is harder.",
 "question": "Why is a bedsheet harder to simulate than a boulder?",
 "outcomes": [
     "Explain why thin materials are numerically difficult.",
     "Implement implicit integration for cloth.",
     "Apply strain limiting and explain what it costs.",
     "Handle cloth self-collision robustly.",
     "Explain why hair needs different methods from cloth.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why thin is hard",
   "blurb": "Three properties that fight each other."},

  {"t": "callout", "title": "Cloth is stiff in-plane and floppy out of plane",
   "kind": "The core difficulty",
   "body": ["<b>Stretching:</b> fabric extends by a few percent at most. "
            "Very stiff.",
            "<b>Bending:</b> fabric folds freely. Almost no resistance.",
            "<b>The ratio between them is enormous</b>, and that ratio is "
            "the definition of stiffness in the numerical sense "
            "(Module 02).",
            "<b>So cloth is stiff by construction.</b> An explicit "
            "integrator must resolve the fast in-plane modes while nothing "
            "visually interesting happens there — and the visible motion "
            "is all in the floppy direction."]},

  {"t": "bullets", "kicker": "Compounding", "title": "And then it collides with itself",
   "items": [
     "<b>Large surface area, thin</b> — a square metre of cloth has far "
     "more contact opportunity than a boulder of the same mass.",
     "",
     "<b>Self-collision everywhere</b> (Module 05): every triangle against "
     "every other, minus adjacency.",
     "",
     "<b>Once tangled, it does not recover.</b> There is no local "
     "information saying which way to separate.",
     "",
     "<b>Contact is the visible part.</b> Drape, folds, and wrinkles are "
     "all contact phenomena.",
     "",
     "<b>So cloth needs both the hardest integration and the hardest "
     "collision.</b>",
   ],
   "note": "The combination is what makes cloth a research area rather than "
           "a solved problem."},

  {"t": "section", "label": "Part 2", "title": "Implicit cloth",
   "blurb": "Baraff and Witkin, 1998."},

  {"t": "callout", "title": "The paper that made cloth practical",
   "kind": "What it did",
   "body": ["Before 1998, cloth required thousands of tiny explicit steps "
            "per frame. Baraff and Witkin used <b>backward Euler</b> and "
            "took one step per frame.",
            "<b>Unconditional stability</b> meant the step size was limited "
            "by what looked right, not by the stiffest spring.",
            "<b>The cost:</b> a large sparse linear system each step, solved "
            "with conjugate gradient — and substantial artificial damping "
            "(Module 02).",
            "<b>They also introduced filtered constraints</b>: a way to "
            "impose constraints inside the CG solve, which is how contact "
            "and pinning are handled without a separate solver."]},

  {"t": "table", "kicker": "Solving", "title": "What the implicit step needs",
   "header": ["Component", "Detail"],
   "widths": [3.4, 8.7],
   "rows": [
     ["Force Jacobian", "&part;f/&part;x per element; sparse and symmetric"],
     ["<b>Linear solve</b>", "<b>Conjugate gradient; the dominant cost</b>"],
     ["Preconditioner", "<b>Diagonal is cheap and helps a lot</b>"],
     ["Filtered constraints", "Pinning and contact imposed inside CG"],
     ["Warm start", "Previous step's solution as the initial guess"],
   ],
   "footnote": "CG needs only matrix-vector products, so the Jacobian never "
               "has to be assembled explicitly — a large saving.",
   "note": "The matrix-free point matters: you can compute Jv directly per "
           "element without ever forming J."},

  {"t": "section", "label": "Part 3", "title": "Strain limiting",
   "blurb": "Enforcing inextensibility without stiffness."},

  {"t": "callout", "title": "Limit the strain instead of resisting it",
   "kind": "The alternative to stiffness",
   "body": ["Rather than using a very stiff spring to resist stretching, use "
            "a moderate spring and then <b>directly clamp any edge that has "
            "stretched beyond a threshold</b> — typically 10%.",
            "<b>This is a constraint projection</b> (Module 04), not a "
            "force, so it costs nothing in stability.",
            "<b>Provot's original method</b> iterates over edges moving "
            "endpoints together. Simple and effective.",
            "<b>The cost is that it is not physical</b> and it can fight "
            "other constraints — a limiting pass can undo contact "
            "resolution, which is why ordering matters."]},

  {"t": "bullets", "kicker": "Bending", "title": "Bending is subtler than it looks",
   "items": [
     "<b>A spring between vertices two apart</b> (Module 03) is crude: it "
     "also resists stretching, so it couples the two behaviours.",
     "",
     "<b>Dihedral angle bending</b> measures the angle between adjacent "
     "triangles directly. Correct, and the derivatives are involved.",
     "",
     "<b>Real fabric is anisotropic in bending</b> — it folds more easily "
     "along the grain than across it.",
     "",
     "<b>And has hysteresis:</b> a crease stays. Simulating that requires "
     "plastic deformation in the bending model.",
     "",
     "<b>Most systems ignore both</b> and look acceptable.",
   ],
   "note": "Creases staying is one of those details that is obvious once "
           "mentioned and almost never simulated."},

  {"t": "section", "label": "Part 4", "title": "Collision and hair",
   "blurb": "The robust treatment, and what changes for strands."},

  {"t": "bullets", "kicker": "Robust cloth", "title": "Bridson's treatment",
   "items": [
     "<b>Give cloth a thickness</b> and keep surfaces apart by that "
     "distance, rather than detecting overlap after the fact.",
     "",
     "<b>Repulsion forces first:</b> gentle, applied early, prevent most "
     "contacts from ever becoming hard.",
     "",
     "<b>Then continuous collision</b> for whatever the repulsions missed. "
     "Vertex-triangle and edge-edge.",
     "",
     "<b>Then a rigid impact zone as a last resort:</b> freeze a tangled "
     "region into a single rigid body for the step. Unphysical and it "
     "guarantees termination.",
     "",
     "<b>The layering is the method.</b> Each stage catches what the "
     "previous missed, and the last one cannot fail.",
   ],
   "note": "The rigid impact zone is the fail-safe. Worth noting that "
           "production robustness often comes from such a backstop."},

  {"t": "callout", "title": "Hair is not thin cloth",
   "kind": "What changes",
   "body": ["<b>A strand is 1D</b>, so bending and twisting are both "
            "meaningful and must be represented separately. Cloth mostly "
            "ignores twist.",
            "<b>There are 100,000 of them</b>, which rules out per-strand "
            "collision against every other strand.",
            "<b>Strand-strand friction dominates the look.</b> Hair holds "
            "its shape because strands grip each other, not because strands "
            "are stiff.",
            "<b>So hair is usually simulated in guide strands and "
            "interpolated</b>, with friction modelled by a continuum "
            "approximation rather than pairwise. Cosserat rods are the "
            "accurate formulation."]},

  {"t": "table", "kicker": "Summary", "title": "Cloth techniques and what they cost",
   "header": ["Technique", "Buys", "Costs"],
   "widths": [3.2, 4.4, 4.5],
   "rows": [
     ["Implicit integration", "<b>Large stable steps</b>", "<b>Linear solve; heavy damping</b>"],
     ["Strain limiting", "<b>Inextensibility, cheaply</b>", "Unphysical; fights constraints"],
     ["XPBD (Module 04)", "Stability; real stiffness", "Not derived from mechanics"],
     ["Cloth thickness", "<b>Robust collision</b>", "Extra detection work"],
     ["Rigid impact zones", "<b>Guaranteed termination</b>", "Visibly frozen regions"],
   ],
   "note": "Every row is a trade. That is the honest summary of cloth "
           "simulation as it stands."},
 ],
 "takeaways": [
   "Cloth is very stiff in-plane and very floppy out of plane; that ratio is "
   "the numerical definition of stiffness, so cloth is stiff by "
   "construction.",
   "It also has enormous contact area and self-collides everywhere — "
   "so it needs both the hardest integration and the hardest collision.",
   "Baraff and Witkin's backward Euler made one step per frame possible, at "
   "the cost of a sparse linear solve and substantial damping.",
   "Conjugate gradient needs only matrix-vector products, so the force "
   "Jacobian never has to be assembled.",
   "Strain limiting enforces inextensibility by projection instead of "
   "stiffness — cheap, unphysical, and it can fight other constraints.",
   "Robust cloth collision is layered: thickness, then repulsion, then "
   "continuous detection, then rigid impact zones as a guaranteed backstop.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why thin materials are hard"),
  ("callout", "Stiff in one direction, floppy in another",
   ["<b>Stretching:</b> woven fabric extends by a few percent at most before "
    "the threads themselves must stretch. Very stiff in-plane.",
    "<b>Bending:</b> the same fabric folds almost freely — the "
    "resistance to bending is smaller than the resistance to stretching by "
    "several orders of magnitude.",
    "<b>That ratio is exactly the numerical definition of stiffness</b> "
    "(Module 02 &sect;3): timescales differing by orders of magnitude within "
    "one system.",
    "<b>So cloth is stiff by construction, not by parameter choice.</b> An "
    "explicit integrator must resolve the fast in-plane modes, where nothing "
    "visually interesting happens, while all the visible motion — "
    "draping, swinging, wrinkling — occurs in the slow floppy "
    "direction. There is no setting that avoids this."]),
  ("ul", ["<b>Large surface area for its mass.</b> A square metre of fabric "
          "has vastly more opportunity for contact than a boulder of the "
          "same weight, and contact is the expensive part.",
          "<b>Self-collision is everywhere.</b> Every triangle can contact "
          "every other triangle of the same mesh, minus the topologically "
          "adjacent ones (Module 05 &sect;5).",
          "<b>Once tangled, cloth does not recover.</b> There is no local "
          "information indicating which way to separate two interpenetrating "
          "layers, and pushing apart arbitrarily usually worsens the tangle.",
          "<b>Contact is the visible phenomenon.</b> Drape, folds, and "
          "wrinkles are all consequences of cloth contacting itself and "
          "other objects — so contact cannot be approximated away as it "
          "often can for rigid bodies.",
          "<b>The combination is what makes cloth hard:</b> it requires the "
          "most difficult integration and the most difficult collision "
          "handling simultaneously, and the two interact."]),

  ("h1", "2 &nbsp; Implicit cloth"),
  ("callout", "Baraff and Witkin, 1998",
   ["Before this paper, cloth simulation required thousands of tiny explicit "
    "time steps per rendered frame, because the stretch stiffness bounded "
    "the step size by Module 02's &Delta;t &lt; 2&radic;(m/k).",
    "<b>Baraff and Witkin applied backward Euler and took a single step per "
    "frame.</b> Unconditional stability meant the step size was limited by "
    "what looked right rather than by the stiffest spring in the mesh "
    "— a change of several orders of magnitude in cost.",
    "<b>The price is a large sparse linear system per step</b>, solved by "
    "conjugate gradient, and the substantial artificial damping inherent to "
    "backward Euler (Module 02 &sect;3). Cloth simulated this way can look "
    "over-damped, losing the high-frequency flutter that reads as fabric.",
    "<b>They also introduced filtered constraints:</b> a way to impose "
    "constraints — pinned vertices, contacts — by filtering the "
    "search directions inside the CG iteration, so no separate constraint "
    "solver is needed. It is an elegant trick and is why the paper is still "
    "read."]),
  ("table", ["Component", "Detail"],
   [["<b>Force Jacobian &part;f/&part;x</b>",
     "Derived per element and assembled. Sparse and symmetric. Deriving it "
     "correctly for bending forces is the tedious part of the "
     "implementation."],
    ["<b>Conjugate gradient solve</b>",
     "<b>The dominant per-step cost.</b> CG requires only matrix-vector "
     "products, so <b>the Jacobian never needs to be assembled "
     "explicitly</b> — compute Jv directly by looping over elements. "
     "This is a large saving in memory and time."],
    ["<b>Preconditioner</b>",
     "<b>A diagonal (Jacobi) preconditioner costs almost nothing and "
     "substantially reduces iteration count.</b> Do it."],
    ["<b>Filtered constraints</b>",
     "Pinning and contact imposed by projecting the CG search directions."],
    ["<b>Warm starting</b>",
     "Use the previous step's solution as the initial guess. The answer "
     "changes little between frames, so this reduces iterations "
     "considerably."]],
   [0.22, 0.78]),

  ("break",),
  ("h1", "3 &nbsp; Strain limiting"),
  ("callout", "Limit the strain rather than resisting it",
   ["The stiffness dilemma from Module 03: cloth must barely stretch, which "
    "requires a very stiff spring, which requires a tiny time step.",
    "<b>Strain limiting sidesteps it.</b> Use a spring of moderate "
    "stiffness, and then, as a separate pass, <b>directly clamp any edge "
    "that has stretched beyond a threshold</b> — Provot's original "
    "proposal used 10% — by moving its endpoints toward each other.",
    "<b>This is a constraint projection</b> (Module 04), not a force. It "
    "costs nothing in stability, because moving a point to a valid position "
    "cannot destabilise anything.",
    "<b>The costs are real.</b> It is not derived from any physical "
    "principle; it removes energy in an uncontrolled way; and <b>it can "
    "fight other constraints</b> — a strain-limiting pass can undo "
    "contact resolution performed immediately before it, so ordering and "
    "iteration between the passes matters."]),
  ("h2", "3.1 &nbsp; Bending"),
  ("ul", ["<b>A spring between vertices two apart</b> (Module 03) is the "
          "crude approach. It does resist folding, and it also resists "
          "stretching along the same direction, so the two behaviours are "
          "coupled and cannot be tuned independently.",
          "<b>Dihedral angle bending</b> measures the angle between adjacent "
          "triangles across their shared edge and applies a restoring "
          "torque. This is the correct formulation and decouples bending "
          "from stretching; the derivatives needed for an implicit solve are "
          "involved but standard.",
          "<b>Real fabric is anisotropic in bending.</b> Woven cloth folds "
          "more readily along the grain than across it, and more readily "
          "still on the bias. This is specifiable in a continuum model and "
          "not in a spring model.",
          "<b>And fabric has bending hysteresis:</b> a crease stays creased. "
          "Representing that requires plasticity in the bending model "
          "— a rest angle that updates when the bend exceeds a "
          "threshold.",
          "<b>Most production systems ignore both</b> and produce acceptable "
          "results, which is worth knowing before spending a week on it."]),

  ("h1", "4 &nbsp; Robust collision"),
  ("p", "Bridson, Fedkiw and Anderson's 2002 treatment is the standard, and "
        "its structure is more instructive than any individual component: "
        "<b>it is layered, and the final layer cannot fail.</b>"),
  ("ol", ["<b>Give the cloth a thickness.</b> Treat each triangle as having "
          "a small offset volume and keep surfaces separated by that "
          "distance, rather than detecting overlap after it has occurred. "
          "Most potential problems never become problems.",
          "<b>Repulsion forces.</b> Gentle forces applied early, as surfaces "
          "approach within the thickness. These resolve the large majority "
          "of contacts smoothly, before they become hard constraints.",
          "<b>Continuous collision detection</b> for whatever the repulsions "
          "did not catch — both vertex&ndash;triangle and "
          "edge&ndash;edge, with exact time-of-impact computation. "
          "Expensive, and applied to a much smaller set because of steps "
          "1 and 2.",
          "<b>Rigid impact zones as a last resort.</b> If a region is so "
          "tangled that collision resolution will not converge, <b>freeze "
          "the whole region into a single rigid body for the remainder of "
          "the step</b>. Completely unphysical, visible if it happens "
          "often — and it <b>guarantees termination</b>, which nothing "
          "else in the list does."]),
  ("p", "<b>The layering is the method.</b> Each stage handles what the "
        "previous missed, at increasing cost, and the final stage cannot "
        "fail. This pattern — a cheap common case backed by an "
        "expensive guaranteed fallback — recurs throughout production "
        "simulation and is worth adopting generally."),

  ("h1", "5 &nbsp; Hair"),
  ("callout", "Hair is not thin cloth",
   ["<b>A strand is one-dimensional</b>, so it has bending <i>and</i> "
    "twisting degrees of freedom, both of which matter for how it looks. "
    "Cloth largely ignores twist; a hair strand's twist determines whether a "
    "curl holds its shape.",
    "<b>There are on the order of 100,000 of them on a human head.</b> "
    "Pairwise strand&ndash;strand collision among 10<super>5</super> strands "
    "is not feasible, and that is before contact with the head and body.",
    "<b>Strand&ndash;strand friction dominates the appearance.</b> Hair "
    "holds a shape not because individual strands are stiff — they are "
    "not — but because strands grip each other. A simulation with "
    "correct strand mechanics and no inter-strand friction looks like "
    "wet hair, always.",
    "<b>So hair is simulated as a few hundred guide strands with the rest "
    "interpolated</b>, and friction modelled as a continuum effect — "
    "a density-dependent drag — rather than pairwise. <b>Cosserat "
    "rods</b> are the accurate formulation for a single strand, handling "
    "bending and twisting correctly, and are used where individual strands "
    "matter."]),
  ("table", ["Technique", "Buys", "Costs"],
   [["<b>Implicit integration</b>", "<b>Large stable time steps.</b>",
     "<b>A sparse linear solve per step, and heavy artificial damping.</b>"],
    ["<b>Strain limiting</b>", "<b>Inextensibility without stiffness.</b>",
     "Unphysical; removes energy uncontrollably; fights other constraints."],
    ["<b>XPBD</b> (Module 04)",
     "Unconditional stability with a meaningful stiffness parameter.",
     "Not derived from mechanics; material behaviour is approximate."],
    ["<b>Cloth thickness and repulsion</b>",
     "<b>Robust collision; most contacts never become hard.</b>",
     "Additional detection work every step."],
    ["<b>Rigid impact zones</b>", "<b>Guaranteed termination.</b>",
     "Visibly frozen regions when they trigger often."]],
   [0.21, 0.36, 0.43]),
  ("p", "<b>Every row is a trade, and none of them is free.</b> That is the "
        "honest summary of cloth simulation as it currently stands: a "
        "collection of techniques each solving one problem and introducing "
        "another, assembled into a pipeline that works well enough. There is "
        "no formulation that is simultaneously stable, fast, physically "
        "correct, and robust under contact, and anyone claiming otherwise "
        "has not tried it on a difficult shot."),
 ],
 "resources": [
   ("Baraff & Witkin &mdash; Large Steps in Cloth Simulation (1998, free)",
    "https://www.cs.cmu.edu/~baraff/papers/",
    "The implicit cloth paper of &sect;2, including filtered constraints. "
    "Still the standard reference."),
   ("Bridson, Fedkiw & Anderson &mdash; Robust Treatment of Collisions, "
    "Contact and Friction for Cloth Animation (2002, free)",
    "https://www.cs.ubc.ca/~rbridson/docs/cloth2002.pdf",
    "The layered collision treatment of &sect;4, including rigid impact "
    "zones. Essential reading."),
   ("Provot &mdash; Deformation Constraints in a Mass-Spring Model (free)",
    "https://graphics.stanford.edu/courses/cs468-02-winter/Papers/Rigidcloth.pdf",
    "The original strain limiting of &sect;3."),
   ("Bergou et al. &mdash; Discrete Elastic Rods (free)",
    "https://www.cs.columbia.edu/cg/rods/",
    "The standard formulation for hair and strands in &sect;5, handling "
    "bending and twisting correctly."),
   ("Ten Minute Physics &mdash; cloth episodes",
    "https://matthias-research.github.io/pages/tenMinutePhysics/",
    "XPBD cloth with working code — the practical alternative to "
    "implicit integration."),
 ],
 "exercises": [
   "Measure the stiffness ratio between stretching and bending for your "
   "cloth model and relate it to the stability limit from Module 02.",
   "Implement implicit (backward Euler) cloth with conjugate gradient. "
   "Report the step size now achievable against the explicit limit.",
   "Implement the matrix-free matrix-vector product and compare memory use "
   "and speed against assembling the Jacobian.",
   "Add a diagonal preconditioner and report the reduction in CG "
   "iterations.",
   "Measure the energy backward Euler removes at several step sizes, and "
   "describe how the cloth's appearance changes.",
   "Implement strain limiting. Compare the maximum stretch and the maximum "
   "stable step against a stiff-spring approach.",
   "Show strain limiting fighting contact: construct a case where the "
   "limiting pass pushes a vertex back into a collider, then fix it by "
   "iterating the two passes.",
   "Implement dihedral angle bending and compare against the "
   "two-apart-spring approach on a draping test.",
   "Implement cloth thickness and repulsion forces. Report what fraction of "
   "contacts are handled by repulsion alone.",
   "Implement a rigid impact zone fallback and construct a tangle that "
   "triggers it. Document how visible the freeze is.",
 ],
 "selfcheck": [
   "Why is cloth numerically stiff by construction rather than by parameter "
   "choice?",
   "Give four reasons cloth collision is harder than rigid body collision.",
   "What did Baraff and Witkin change, and what did it cost?",
   "Why does conjugate gradient not require the Jacobian to be assembled?",
   "What is strain limiting, what does it replace, and what are its three "
   "costs?",
   "Why is a two-apart spring an inadequate bending model?",
   "Give the four layers of Bridson's collision treatment and say what the "
   "last one guarantees.",
   "Give three ways hair differs from cloth.",
   "Why does hair hold its shape, and what does that imply for simulation?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Fluids I: Grid-Based",
 "subtitle": "Navier–Stokes, split into pieces you can actually solve.",
 "question": "How do you simulate smoke and water on a grid?",
 "outcomes": [
     "State the incompressible Navier–Stokes equations and interpret "
     "each term.",
     "Explain operator splitting and why it makes the problem tractable.",
     "Implement semi-Lagrangian advection and explain its dissipation.",
     "Implement pressure projection and explain what it enforces.",
     "Explain the MAC grid and why staggering matters.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The equations",
   "blurb": "Two lines, and one of them is almost trivial."},

  {"t": "eq", "kicker": "Navier–Stokes", "title": "Incompressible flow",
   "eqs": [
     ("∂u/∂t  =  −(u·∇)u  −  (1/ρ)∇p  +  ν∇²u  +  f",
      "Velocity changes by: self-advection, pressure gradient, viscosity, "
      "and external forces."),
     ("∇ · u  =  0",
      "Incompressibility: no net flow into or out of any region. This single "
      "constraint determines the pressure."),
   ],
   "caption": "The second equation has no time derivative. Pressure is not "
              "evolved — it is whatever makes the first equation respect "
              "the second.",
   "note": "That pressure is a constraint force, not a state variable, is "
           "the key conceptual point. Compare Module 04."},

  {"t": "callout", "title": "Pressure is a Lagrange multiplier",
   "kind": "The connection to Module 04",
   "body": ["Incompressibility is a <b>constraint</b>: ∇·u = 0 must hold "
            "everywhere, at all times.",
            "<b>Pressure is the force that enforces it</b> — exactly the "
            "role λ played in Module 04. It is not a material property being "
            "evolved; it is solved for, every step.",
            "<b>That is why the pressure solve is a global linear "
            "system.</b> Incompressibility couples the entire domain "
            "instantly: squeeze here and the fluid must move there.",
            "<b>And why it is the expensive part.</b> A Poisson solve over "
            "the whole grid, every step, with no locality to exploit."]},

  {"t": "section", "label": "Part 2", "title": "Operator splitting",
   "blurb": "Solve one term at a time."},

  {"t": "bullets", "kicker": "Stable Fluids", "title": "Jos Stam's decomposition, 1999",
   "items": [
     "<b>1. Add forces.</b> u += Δt·f. Trivial.",
     "<b>2. Advect.</b> Move the velocity field along itself. "
     "<b>Unconditionally stable if done semi-Lagrangianly.</b>",
     "<b>3. Diffuse.</b> Apply viscosity. An implicit solve, or skip it "
     "— numerical dissipation usually supplies more than enough.",
     "<b>4. Project.</b> Subtract the pressure gradient to make the field "
     "divergence-free. <b>The expensive step.</b>",
     "",
     "<b>Each step is individually tractable.</b> Splitting introduces "
     "error, and it is what made fluids practical in graphics.",
   ],
   "note": "Stam's paper is the single most influential in graphics fluids. "
           "The contribution is the splitting plus stable advection."},

  {"t": "callout", "title": "Semi-Lagrangian advection cannot blow up",
   "kind": "Stam's key move",
   "body": ["<b>Instead of pushing values forward, trace backwards.</b> For "
            "each grid cell, ask: where did this fluid come from one step "
            "ago? Then interpolate the old field there.",
            "<b>The result is a weighted average of existing values</b>, so "
            "it can never exceed the range already present.",
            "<b>Unconditionally stable at any time step</b>, which removed "
            "the CFL restriction that had limited earlier methods.",
            "<b>The cost is severe numerical dissipation.</b> Every step "
            "interpolates, every interpolation smooths, and smoke visibly "
            "loses its detail over time."]},

  {"t": "table", "kicker": "Dissipation", "title": "Fighting the smoothing",
   "header": ["Technique", "Idea", "Cost"],
   "widths": [3.0, 4.8, 4.3],
   "rows": [
     ["<b>Vorticity confinement</b>", "Detect vortices, push energy back in",
      "<b>Unphysical; cheap; everyone uses it</b>"],
     ["<b>BFECC / MacCormack</b>", "Advect forward then back; correct the error",
      "<b>2× cost; much less dissipation</b>"],
     ["Higher-order interpolation", "Cubic instead of linear", "Ringing; moderate gain"],
     ["<b>FLIP</b>", "Carry velocity on particles", "<b>Module 12</b>"],
   ],
   "footnote": "Vorticity confinement is a hack that adds energy at the "
               "scale it was lost. It works, and nobody pretends it is "
               "principled.",
   "note": "FLIP is the real answer and is why it took over. Flag it "
           "forward."},

  {"t": "section", "label": "Part 3", "title": "The grid",
   "blurb": "Where you store things matters more than it should."},

  {"t": "callout", "title": "The MAC grid: store velocity on faces",
   "kind": "Why staggering",
   "body": ["<b>Collocated grid:</b> all quantities at cell centres. "
            "Computing divergence needs a central difference spanning two "
            "cells.",
            "<b>That difference cannot see a checkerboard pattern</b>, so "
            "pressure can oscillate cell to cell with zero computed "
            "divergence. The classic checkerboard instability.",
            "<b>MAC (marker-and-cell) grid:</b> pressure at cell centres, "
            "velocity components on the corresponding <i>faces</i>.",
            "<b>Now divergence is a difference between adjacent faces</b> "
            "— it sees everything, the checkerboard mode is impossible, "
            "and the pressure gradient lands exactly where velocity lives."]},

  {"t": "eq", "kicker": "Projection", "title": "The pressure Poisson equation",
   "eqs": [
     ("∇²p  =  (ρ/Δt) ∇·u*",
      "Solve for the pressure whose gradient removes the divergence of the "
      "intermediate velocity u*."),
     ("u  =  u*  −  (Δt/ρ) ∇p",
      "Subtract it. The result is divergence-free to solver tolerance."),
     ("Sparse, symmetric, positive definite",
      "So conjugate gradient applies — and with a good preconditioner it "
      "is the dominant cost of the whole simulation."),
   ],
   "caption": "Preconditioned CG, usually with incomplete Cholesky or "
              "multigrid. This solve is where the time goes.",
   "note": "Multigrid is asymptotically optimal here and is what large "
           "production solvers use."},

  {"t": "section", "label": "Part 4", "title": "Liquids",
   "blurb": "What changes when there is a surface."},

  {"t": "bullets", "kicker": "Free surface", "title": "Smoke and water are different problems",
   "items": [
     "<b>Smoke fills the domain.</b> Every cell is fluid; boundary "
     "conditions are simple.",
     "",
     "<b>Water has a free surface</b> that moves, and must be tracked.",
     "",
     "<b>Level sets</b> represent the surface implicitly as the zero set of "
     "a signed distance field. Topology changes — splitting, merging — "
     "are automatic.",
     "",
     "<b>And they lose volume.</b> Advecting and reinitialising a level set "
     "is dissipative; a drop can simply evaporate.",
     "",
     "<b>Particle level sets</b> fix this by seeding particles near the "
     "surface to correct the implicit representation.",
   ],
   "note": "Volume loss is the defining practical problem of grid-based "
           "liquid, and it is why Project 2 asks for a volume plot."},

  {"t": "callout", "title": "Volume loss is the problem to measure",
   "kind": "What to plot",
   "body": ["A grid-based liquid simulation loses volume steadily: "
            "advection smooths, the level set reinitialisation smooths more, "
            "and thin features fall below the grid resolution and vanish.",
            "<b>A splash's droplets disappear.</b> A thin sheet of water "
            "evaporates mid-air.",
            "<b>Plot total volume every frame.</b> It is the single most "
            "informative diagnostic for a liquid solver, exactly as the "
            "energy plot is for a dynamics solver.",
            "<b>FLIP (Module 12) loses far less</b>, which is the main "
            "reason it displaced pure grid methods for liquid."]},
 ],
 "takeaways": [
   "Navier–Stokes has no time derivative for pressure: pressure is a "
   "Lagrange multiplier enforcing incompressibility, solved for each step.",
   "That constraint is global, which is why the pressure solve is a Poisson "
   "system over the whole domain and the dominant cost.",
   "Operator splitting solves force, advection, diffusion, and projection "
   "separately — each tractable, with splitting error accepted.",
   "Semi-Lagrangian advection traces backwards and interpolates, so it "
   "cannot exceed existing values and cannot blow up — at the cost of "
   "heavy dissipation.",
   "The MAC grid stores velocity on faces so the divergence stencil is "
   "compact, which eliminates the checkerboard pressure mode.",
   "Grid liquids lose volume through advection and level set "
   "reinitialisation. Plot volume every frame; it is the key diagnostic.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The equations"),
  ("eq", "&part;<b>u</b>/&part;t = &minus;(<b>u</b>&middot;&nabla;)<b>u</b> "
         "&minus; (1/&rho;)&nabla;p + &nu;&nabla;&#178;<b>u</b> + <b>f</b>"),
  ("eq", "&nabla; &middot; <b>u</b> = 0"),
  ("table", ["Term", "Meaning"],
   [["&minus;(<b>u</b>&middot;&nabla;)<b>u</b>",
     "<b>Advection.</b> The fluid carries its own velocity along with it. "
     "Nonlinear, and the source of turbulence."],
    ["&minus;(1/&rho;)&nabla;p", "<b>Pressure gradient.</b> Fluid "
     "accelerates from high pressure toward low."],
    ["&nu;&nabla;&#178;<b>u</b>", "<b>Viscosity.</b> Diffusion of "
     "momentum, smoothing velocity differences."],
    ["<b>f</b>", "External forces — gravity, buoyancy, user forces."],
    ["&nabla;&middot;<b>u</b> = 0",
     "<b>Incompressibility.</b> No net flow into or out of any region, so "
     "the fluid's volume is preserved exactly."]],
   [0.21, 0.79]),
  ("callout", "Pressure is a Lagrange multiplier, not a state variable",
   ["<b>The second equation has no time derivative.</b> It is a constraint "
    "that must hold at every instant, not an evolution equation.",
    "<b>Pressure is the force that enforces it</b> — precisely the role "
    "&lambda; played in Module 04. Pressure is not a property of the fluid "
    "being carried along and evolved; it is <i>solved for</i>, from scratch, "
    "every step, as whatever field makes the velocity update respect "
    "incompressibility.",
    "<b>This is why the pressure solve is a global linear system.</b> "
    "Incompressibility couples the entire domain instantaneously: squeeze "
    "the fluid in one place and it must move somewhere else <i>now</i>, "
    "however far away. There is no locality to exploit.",
    "<b>And it is why the pressure projection is the dominant cost</b> of "
    "almost every fluid simulation. Everything else is local; this is not."]),

  ("h1", "2 &nbsp; Operator splitting"),
  ("p", "Jos Stam's 1999 'Stable Fluids' is the most influential paper in "
        "graphics fluid simulation, and its contribution is a "
        "decomposition: rather than solving the full equation at once, "
        "apply each term in sequence, each with a method suited to it."),
  ("ol", ["<b>Add forces.</b> <b>u</b> += &Delta;t &middot; <b>f</b>. "
          "Trivial.",
          "<b>Advect.</b> Move the velocity field along itself. "
          "<b>Unconditionally stable if done semi-Lagrangianly</b>, which is "
          "the paper's other contribution.",
          "<b>Diffuse.</b> Apply viscosity by an implicit solve. <b>Often "
          "skipped entirely</b> in graphics, because the numerical "
          "dissipation introduced by advection already exceeds any physical "
          "viscosity you would have wanted.",
          "<b>Project.</b> Subtract a pressure gradient so the field becomes "
          "divergence-free. <b>The expensive step.</b>"]),
  ("p", "<b>Splitting introduces error</b> — applying the terms "
        "sequentially is not the same as solving them simultaneously, and "
        "the error is first order in &Delta;t. It is accepted universally, "
        "because each individual step is tractable and the combined method "
        "is stable, which the unsplit equation is not."),
  ("callout", "Semi-Lagrangian advection cannot blow up",
   ["The intuitive approach to advection pushes values forward: this parcel "
    "of fluid is moving, so move its velocity to where it will be. That is "
    "unstable at large time steps, because parcels can overtake one another "
    "and pile up.",
    "<b>Stam traced backwards instead.</b> For each grid cell, ask where the "
    "fluid now in this cell came from one step ago — follow the "
    "velocity field backwards — and interpolate the old field at that "
    "position.",
    "<b>The result is a weighted average of values that already existed</b>, "
    "so the new value cannot possibly exceed the range already present in "
    "the field. <b>It cannot blow up, at any time step.</b> This removed the "
    "CFL restriction that had made earlier methods expensive, and it is why "
    "the paper is titled 'Stable Fluids'.",
    "<b>The cost is severe numerical dissipation.</b> Every step performs an "
    "interpolation, every interpolation is a smoothing operation, and the "
    "smoothing accumulates. Smoke visibly loses its fine structure within a "
    "few seconds, and the velocity field loses its small-scale "
    "vortices — which are exactly what makes smoke look like smoke."]),
  ("table", ["Technique", "Mechanism", "Assessment"],
   [["<b>Vorticity confinement</b>",
     "Detect where vorticity is concentrated and add a force pushing energy "
     "back into those vortices.",
     "<b>Entirely unphysical</b> — it adds energy at the scale "
     "dissipation removed it. Cheap, effective, and universally used. Nobody "
     "pretends it is principled."],
    ["<b>BFECC / MacCormack</b>",
     "Advect forward, then advect the result backward, and use the "
     "discrepancy to estimate and correct the error.",
     "<b>Roughly twice the cost, and substantially less dissipation.</b> "
     "Principled, and the usual choice when the budget allows."],
    ["<b>Higher-order interpolation</b>",
     "Cubic rather than trilinear interpolation in the advection step.",
     "Moderate improvement; introduces ringing near discontinuities, which "
     "must be limited."],
    ["<b>FLIP</b>", "Carry velocity on particles and avoid interpolating the "
     "field at all.",
     "<b>The real answer, and why FLIP displaced pure grid methods.</b> "
     "Module 12."]],
   [0.19, 0.38, 0.43]),

  ("break",),
  ("h1", "3 &nbsp; The MAC grid"),
  ("callout", "Stagger the velocity onto cell faces",
   ["<b>The obvious layout</b> stores everything — pressure and all "
    "three velocity components — at cell centres. Computing the "
    "divergence then requires a central difference spanning <i>two</i> "
    "cells in each direction.",
    "<b>That stencil cannot see a checkerboard.</b> A pressure field "
    "alternating high-low-high-low between adjacent cells has, by the "
    "two-cell central difference, exactly zero gradient — so the solver "
    "cannot detect or correct it. The result is the classic <b>checkerboard "
    "instability</b>: a spurious oscillating pressure field that the method "
    "is blind to.",
    "<b>The MAC (marker-and-cell) grid</b> stores pressure at cell centres "
    "and each velocity component on the cell <i>faces</i> perpendicular to "
    "it. The x-velocity lives on the left and right faces, the y-velocity on "
    "the top and bottom, and so on.",
    "<b>Now the divergence of a cell is a difference between its own "
    "adjacent faces</b> — a compact stencil that sees everything, so "
    "the checkerboard mode is not in the null space and cannot arise. "
    "<b>And the pressure gradient naturally lands exactly where the velocity "
    "components are stored</b>, so no interpolation is needed in the "
    "projection. The layout makes two problems disappear at once, which is "
    "why it is universal."]),
  ("eq", "&nabla;&#178; p = (&rho;/&Delta;t) &nabla; &middot; "
         "<b>u</b>* &nbsp;&nbsp;&nbsp;&nbsp; <b>u</b> = <b>u</b>* &minus; "
         "(&Delta;t/&rho;) &nabla;p"),
  ("p", "Solve the Poisson equation for the pressure whose gradient exactly "
        "cancels the divergence of the intermediate velocity "
        "<b>u</b>*, then subtract it. The matrix is sparse, symmetric, and "
        "positive definite, so conjugate gradient applies — and "
        "<b>this solve is where the time goes.</b> An incomplete Cholesky "
        "preconditioner is the standard choice; <b>multigrid</b> is "
        "asymptotically optimal and is what large production solvers use."),

  ("h1", "4 &nbsp; Liquids"),
  ("table", ["", "Smoke", "Water"],
   [["Domain", "Fluid fills the whole grid. Every cell is fluid.",
     "<b>A free surface</b> separating liquid from air, which moves and "
     "must be tracked."],
    ["Boundary conditions", "Simple — the domain walls.",
     "The free surface is a pressure boundary condition that changes every "
     "step."],
    ["Representation", "A density field advected with the flow.",
     "<b>A level set</b> — the surface is the zero set of a signed "
     "distance field."],
    ["Topology change", "Not applicable.",
     "<b>Automatic.</b> Splitting droplets and merging pools require no "
     "special handling, which is the level set's great advantage."],
    ["Characteristic failure", "<b>Dissipation</b> — detail is lost.",
     "<b>Volume loss</b> — see below."]],
   [0.17, 0.40, 0.43]),
  ("callout", "Volume loss is the problem to measure",
   ["A grid-based liquid simulation loses volume steadily, from several "
    "compounding causes: the level set is advected by the same dissipative "
    "scheme as everything else; reinitialising it to a true distance field "
    "each step smooths it further; and any feature thinner than a grid cell "
    "simply cannot be represented and disappears.",
    "<b>The visible result is that a splash's droplets vanish in mid-air</b> "
    "and a thin sheet of water evaporates. Over a long simulation a pool can "
    "measurably drain.",
    "<b>Plot total volume every frame.</b> It is the single most informative "
    "diagnostic for a liquid solver — the exact counterpart of the "
    "energy plot for a dynamics solver — and it is what Project 2 asks "
    "for.",
    "<b>Particle level sets</b> mitigate it by seeding marker particles near "
    "the surface and using them to correct the implicit representation where "
    "it has drifted. <b>And FLIP (Module 12) loses far less volume</b> by "
    "carrying the fluid on particles in the first place, which is the "
    "principal reason it displaced pure grid methods for liquid."]),
 ],
 "resources": [
   ("Bridson &mdash; Fluid Simulation for Computer Graphics",
    "https://www.cs.ubc.ca/~rbridson/fluidsimulation/",
    "The standard reference for this module and the next. The free course "
    "notes cover the MAC grid, projection, and level sets completely."),
   ("Stam &mdash; Stable Fluids (1999, free)",
    "https://www.josstam.com/publications",
    "The splitting and semi-Lagrangian advection of &sect;2. Short, and it "
    "changed the field."),
   ("Stam &mdash; Real-Time Fluid Dynamics for Games (free, with code)",
    "https://www.josstam.com/publications",
    "A complete 2D solver in about a hundred lines. Implement this first."),
   ("Fedkiw, Stam & Jensen &mdash; Visual Simulation of Smoke (free)",
    "https://physbam.stanford.edu/~fedkiw/",
    "Vorticity confinement, from the paper that introduced it to graphics."),
   ("Ten Minute Physics &mdash; Eulerian fluid episodes",
    "https://matthias-research.github.io/pages/tenMinutePhysics/",
    "A working grid solver built up step by step, with code."),
 ],
 "exercises": [
   "Implement Stam's 2D solver from the 'Real-Time Fluid Dynamics for Games' "
   "paper. Get smoke moving before attempting anything else.",
   "Implement a collocated grid and demonstrate the checkerboard "
   "instability. Then switch to a MAC grid and show it disappears.",
   "Implement semi-Lagrangian advection and measure the dissipation: advect "
   "a sharp density blob in a uniform velocity field and plot its maximum "
   "value over time. It should decay — report how fast.",
   "Implement BFECC or MacCormack advection and repeat. Report the "
   "improvement and the added cost.",
   "Implement vorticity confinement and show the recovered detail. Then "
   "measure the energy it adds and be honest about it.",
   "Implement pressure projection with conjugate gradient. Plot residual "
   "against iteration count and report what tolerance is visually "
   "sufficient.",
   "Add an incomplete Cholesky preconditioner and report the reduction in "
   "iterations.",
   "Measure what fraction of total simulation time the pressure solve "
   "consumes, at three grid resolutions.",
   "Implement a level set free surface and simulate a dam break. <b>Plot "
   "total volume every frame</b> and report the loss over ten seconds.",
   "Halve the grid spacing and repeat the volume measurement. Report how "
   "volume loss scales with resolution.",
 ],
 "selfcheck": [
   "State the incompressible Navier–Stokes equations and interpret each "
   "term.",
   "Why is pressure a Lagrange multiplier, and what does that imply about "
   "the solve?",
   "List the four steps of operator splitting and say which is expensive.",
   "Why can semi-Lagrangian advection not blow up, and what does it cost?",
   "Name three ways of fighting advection dissipation and assess each.",
   "What is the checkerboard instability and how does the MAC grid prevent "
   "it?",
   "Write the pressure Poisson equation and say what is solved and what is "
   "subtracted.",
   "Give three differences between simulating smoke and simulating water.",
   "Why do grid-based liquids lose volume, and what should you plot?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Fluids II: Particles and Hybrids",
 "subtitle": "Carrying the fluid instead of sampling it.",
 "question": "What do particles fix, and what do they break?",
 "outcomes": [
     "Explain SPH and the role of the smoothing kernel.",
     "Explain why SPH struggles with incompressibility, and what PBF does "
     "about it.",
     "Explain PIC and FLIP and the trade between them.",
     "Explain MPM and what it enables.",
     "Choose a fluid method from the phenomenon being simulated.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Lagrangian fluids",
   "blurb": "Follow the fluid instead of watching fixed points."},

  {"t": "two", "kicker": "Viewpoints", "title": "Eulerian and Lagrangian",
   "lh": "Eulerian — fixed grid",
   "l": ["Watch fixed points in space; fluid flows past.",
         "<b>Incompressibility is easy</b> — a global solve on a regular "
         "structure.",
         "<b>Advection is dissipative</b> and the free surface must be "
         "tracked.",
         ("Good for smoke.", 1)],
   "rh": "Lagrangian — particles",
   "r": ["Follow parcels of fluid as they move.",
         "<b>Advection is free and exact</b> — particles simply move.",
         "<b>Incompressibility is hard</b> — no regular structure to solve "
         "on.",
         ("Good for splashing liquid.", 1)],
   "note": "The trade is exactly complementary, which is why hybrids won."},

  {"t": "eq", "kicker": "SPH", "title": "Smoothed particle hydrodynamics",
   "eqs": [
     ("A(x)  =  Σⱼ mⱼ (Aⱼ/ρⱼ) W(x − xⱼ, h)",
      "Any field is a kernel-weighted sum over nearby particles. The "
      "smoothing length h sets the support radius."),
     ("ρᵢ  =  Σⱼ mⱼ W(xᵢ − xⱼ, h)",
      "Density is just the kernel sum of mass — no separate equation "
      "needed."),
     ("∇A  =  Σⱼ mⱼ (Aⱼ/ρⱼ) ∇W",
      "Derivatives move onto the kernel, which is smooth and differentiable "
      "analytically."),
   ],
   "caption": "The whole method: replace field operations with weighted sums "
              "over neighbours, and differentiate the kernel instead of the "
              "data.",
   "note": "That derivatives hit the kernel rather than the data is the "
           "elegant part — the data is a point cloud and not "
           "differentiable."},

  {"t": "callout", "title": "SPH's problem is incompressibility",
   "kind": "The fundamental difficulty",
   "body": ["Incompressibility is a <b>global</b> constraint, and SPH has "
            "only <b>local</b> neighbour information.",
            "<b>Classic SPH fakes it</b> with a stiff equation of state: "
            "pressure rises steeply with density, so the fluid is "
            "<i>nearly</i> incompressible.",
            "<b>Stiff means tiny time steps</b> (Module 02) — and it "
            "still compresses visibly, which looks like a springy, bouncy "
            "liquid.",
            "<b>This is why SPH water often looks wrong</b>, and why PCISPH, "
            "IISPH, and PBF all exist. They are different ways of imposing "
            "the constraint rather than approximating it with stiffness."]},

  {"t": "callout", "title": "Position-based fluids: PBD applied to water",
   "kind": "The game-friendly answer",
   "body": ["<b>Treat constant density as a constraint</b>, C = ρᵢ/ρ₀ − 1 "
            "= 0, and solve it with the Module 04 machinery.",
            "<b>Unconditionally stable</b>, for exactly the reasons PBD "
            "is — positions are projected, not integrated.",
            "<b>Large time steps</b>, which is what real-time needs.",
            "<b>The same theoretical weaknesses as PBD:</b> the "
            "incompressibility achieved depends on iteration count, and it "
            "is not derived from fluid mechanics. <b>And it is in every game "
            "that has fluid.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Hybrids",
   "blurb": "Particles for advection, a grid for pressure."},

  {"t": "bullets", "kicker": "PIC / FLIP", "title": "Use each where it is strong",
   "items": [
     "<b>1. Transfer particle velocities to a grid.</b>",
     "<b>2. Solve pressure on the grid</b> — Module 11's machinery, where "
     "it is easy.",
     "<b>3. Transfer velocities back to the particles.</b>",
     "<b>4. Move the particles.</b> Advection is exact and free.",
     "",
     "<b>PIC</b> transfers the full grid velocity back. Stable, and heavily "
     "damped by the double interpolation.",
     "<b>FLIP</b> transfers only the <i>change</i> in velocity. <b>Almost no "
     "dissipation</b> — and noisy.",
   ],
   "note": "The PIC/FLIP distinction is one line of code and completely "
           "changes the character of the result."},

  {"t": "callout", "title": "Everyone blends PIC and FLIP",
   "kind": "The practical answer",
   "body": ["<b>Pure FLIP is too noisy:</b> particle velocities drift apart "
            "within a cell because nothing couples them, and the result is a "
            "jittery, sparkly liquid.",
            "<b>Pure PIC is too damped:</b> two interpolations per step "
            "smooth the velocity field heavily, and the splash dies.",
            "<b>So blend:</b> typically 95% FLIP and 5% PIC. The small PIC "
            "component acts as a filter removing the particle-scale noise "
            "while retaining almost all the energy.",
            "<b>That ratio is a tuning parameter in every production fluid "
            "solver</b>, and APIC/PolyPIC are principled alternatives that "
            "largely remove the need for it."]},

  {"t": "section", "label": "Part 3", "title": "MPM",
   "blurb": "The method that handles everything else."},

  {"t": "callout", "title": "The material point method",
   "kind": "Hybrid for solids too",
   "body": ["<b>Same transfer structure as FLIP</b> — particles to grid, "
            "solve, back to particles — but the particles carry "
            "<b>deformation gradients</b> (Module 09), not just velocity.",
            "<b>So it simulates solids, fluids, and everything between</b> "
            "with one solver and one code path.",
            "<b>Topology change is automatic.</b> Fracture, melting, "
            "merging, and tearing require no special handling, because the "
            "grid is rebuilt every step.",
            "<b>This is the snow in Disney's <i>Frozen</i></b>, and it is "
            "now the standard method for sand, mud, snow, and viscoelastic "
            "materials."]},

  {"t": "table", "kicker": "MPM", "title": "What it buys and costs",
   "header": ["Buys", "Costs"],
   "widths": [6.0, 6.1],
   "rows": [
     ["<b>One solver for solid, fluid, and granular</b>", "Expensive — a grid solve every step"],
     ["<b>Topology change for free</b>", "Grid artefacts; resolution-dependent detail"],
     ["Plasticity and fracture naturally", "Numerical cohesion — things stick"],
     ["<b>Multi-material coupling automatic</b>", "Many particles needed per cell"],
   ],
   "footnote": "Numerical cohesion is the characteristic MPM artefact: "
               "separated material clumps back together because the grid "
               "couples it.",
   "note": "The cohesion artefact is worth naming — it is visible in a lot "
           "of MPM work once you know it."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "The phenomenon determines the method."},

  {"t": "table", "kicker": "Selection", "title": "Method by phenomenon",
   "header": ["Phenomenon", "Method", "Why"],
   "widths": [3.0, 3.6, 5.5],
   "rows": [
     ["Smoke, fire", "<b>Eulerian grid</b>", "Fills the domain; no surface"],
     ["<b>Splashing liquid</b>", "<b>FLIP / APIC</b>", "<b>Advection and surface via particles</b>"],
     ["Real-time water", "<b>PBF</b>", "Stable at large steps"],
     ["Viscous, sticky", "SPH or MPM", "Viscosity is natural in SPH"],
     ["<b>Sand, snow, mud</b>", "<b>MPM</b>", "<b>Plasticity and topology change</b>"],
     ["Ocean surface", "FFT wave model", "<b>Not a fluid solve at all</b>"],
   ],
   "note": "The last row matters: large-scale water is usually not "
           "simulated. Tessendorf's spectral method is what films use."},

  {"t": "callout", "title": "Not everything that looks like fluid is simulated",
   "kind": "An important practical point",
   "body": ["<b>Ocean surfaces in film are usually spectral</b> — "
            "Tessendorf's FFT wave model synthesises a statistically correct "
            "ocean with no fluid solve at all.",
            "It is vastly cheaper, trivially tileable, controllable by wind "
            "parameters, and <b>it looks better</b> than a simulation at any "
            "affordable resolution.",
            "<b>A simulation is only worth it when the interaction "
            "matters</b> — a ship's wake, a splash, water hitting "
            "something.",
            "<b>Hybrid is the production answer:</b> spectral ocean, "
            "simulated splash where it is needed, composited together."]},
 ],
 "takeaways": [
   "Eulerian grids make incompressibility easy and advection dissipative; "
   "Lagrangian particles make advection exact and incompressibility hard.",
   "SPH expresses every field as a kernel-weighted neighbour sum, and "
   "derivatives fall on the smooth kernel rather than on the point data.",
   "SPH's difficulty is that incompressibility is global and its information "
   "is local; stiff equations of state fake it and look springy.",
   "PIC/FLIP transfers to a grid for the pressure solve and back. FLIP "
   "transfers the velocity <i>change</i>, which keeps energy and adds noise.",
   "Everyone blends about 95% FLIP with 5% PIC to get energy without "
   "jitter; APIC removes the need for that dial.",
   "MPM carries deformation gradients on particles, so one solver handles "
   "solids, fluids, sand, and snow with automatic topology change.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Lagrangian fluids"),
  ("table", ["", "Eulerian (grid)", "Lagrangian (particles)"],
   [["Viewpoint", "Watch fixed points in space; fluid flows past them.",
     "Follow parcels of fluid as they move."],
    ["Advection", "<b>Dissipative</b> — requires interpolation every "
     "step (Module 11).",
     "<b>Free and exact</b> — the particles simply move, carrying "
     "their quantities with them."],
    ["Incompressibility", "<b>Easy</b> — a global Poisson solve on a "
     "regular structure.",
     "<b>Hard</b> — the constraint is global and the information is "
     "local."],
    ["Free surface", "Must be tracked explicitly (level set), and loses "
     "volume.",
     "<b>Implicit</b> — the surface is wherever the particles are."],
    ["Best for", "Smoke, fire, confined flow.",
     "Splashing liquid, spray, scenes with lots of free surface."]],
   [0.15, 0.42, 0.43]),
  ("p", "<b>The strengths are exactly complementary</b>, which is the entire "
        "reason hybrid methods (&sect;2) came to dominate."),
  ("eq", "A(x) = &Sigma;<sub>j</sub> m<sub>j</sub> (A<sub>j</sub>/"
         "&rho;<sub>j</sub>) W(x &minus; x<sub>j</sub>, h)"),
  ("p", "<b>Smoothed particle hydrodynamics</b> represents every field as a "
        "kernel-weighted sum over nearby particles. The smoothing kernel W "
        "has compact support of radius h, so each sum runs only over "
        "neighbours — found with a spatial hash, exactly as in "
        "Module 05's broad phase."),
  ("p", "Density falls out as a special case: &rho;<sub>i</sub> = "
        "&Sigma;<sub>j</sub> m<sub>j</sub> W(x<sub>i</sub> &minus; "
        "x<sub>j</sub>, h), with no separate continuity equation needed. "
        "<b>And derivatives move onto the kernel:</b> &nabla;A = "
        "&Sigma;<sub>j</sub> m<sub>j</sub> (A<sub>j</sub>/&rho;<sub>j</sub>) "
        "&nabla;W. This is the elegant part — the data is an unordered "
        "point cloud and is not differentiable, but the kernel is smooth and "
        "its gradient is known analytically."),
  ("callout", "SPH's fundamental difficulty is incompressibility",
   ["<b>Incompressibility is a global constraint</b> — compressing "
    "fluid here requires it to move somewhere else, instantly, however far "
    "away. <b>SPH has only local information:</b> each particle knows about "
    "its neighbours within h, and nothing else.",
    "<b>Classic SPH approximates it with a stiff equation of state</b>: "
    "pressure rises steeply as density exceeds its rest value, so the fluid "
    "is strongly discouraged from compressing. It is <i>nearly</i> "
    "incompressible.",
    "<b>Stiff means tiny time steps</b> by Module 02's bound — and the "
    "fluid still compresses visibly, which reads as a springy, bouncy liquid "
    "that behaves more like gelatin than water.",
    "<b>This is why SPH water so often looks wrong</b>, and why a succession "
    "of methods — PCISPH, IISPH, DFSPH, and position-based fluids "
    "— exist. All of them replace the stiff-equation-of-state "
    "approximation with some way of actually imposing the constraint."]),
  ("callout", "Position-based fluids",
   ["<b>PBF applies Module 04's machinery directly:</b> treat constant "
    "density as a constraint, C<sub>i</sub> = &rho;<sub>i</sub>/"
    "&rho;<sub>0</sub> &minus; 1 = 0, and solve it by position projection.",
    "<b>Unconditionally stable</b>, for precisely the reason PBD is: "
    "positions are projected onto valid configurations rather than "
    "integrated from forces, so nothing can diverge.",
    "<b>Large time steps</b>, which is what interactive applications "
    "require, and it parallelises well on a GPU.",
    "<b>It inherits PBD's theoretical weaknesses:</b> the degree of "
    "incompressibility achieved depends on the iteration count and the time "
    "step, and the method is not derived from fluid mechanics. <b>And it is "
    "in essentially every game that has interactive fluid</b>, for the same "
    "reason PBD is in every game that has cloth."]),

  ("break",),
  ("h1", "2 &nbsp; PIC and FLIP"),
  ("p", "The hybrid idea is to use each representation where it is strong: "
        "<b>particles for advection, a grid for the pressure solve.</b>"),
  ("ol", ["<b>Transfer</b> particle velocities onto a MAC grid, by kernel "
          "weighting.",
          "<b>Solve</b> for pressure and project on the grid — "
          "Module 11's machinery, in the setting where it is "
          "straightforward.",
          "<b>Transfer</b> the resulting velocities back to the particles.",
          "<b>Move</b> the particles. Advection is exact and costs nothing."]),
  ("table", ["", "PIC", "FLIP"],
   [["Step 3 transfers", "The <b>full</b> grid velocity.",
     "Only the <b>change</b> in grid velocity, added to the particle's "
     "existing velocity."],
    ["Dissipation", "<b>Heavy.</b> Two interpolations per step smooth the "
     "field substantially, and a splash dies quickly.",
     "<b>Almost none.</b> The particle's velocity is preserved and only "
     "corrected."],
    ["Noise", "<b>None.</b> All particles in a cell agree.",
     "<b>Significant.</b> Nothing couples particles within a cell, so their "
     "velocities drift apart — producing a jittery, sparkling liquid."]],
   [0.17, 0.41, 0.42]),
  ("callout", "Everyone blends them",
   ["<b>Pure FLIP is too noisy</b> and <b>pure PIC is too damped</b>, and "
    "both failures are immediately visible.",
    "<b>So blend the two results:</b> typically 95% FLIP and 5% PIC. The "
    "small PIC component acts as a filter removing particle-scale noise, "
    "while 95% of the energy is retained. The blend costs one extra "
    "interpolation and one lerp.",
    "<b>That ratio is an exposed tuning parameter in every production fluid "
    "solver</b>, and artists adjust it per shot — more PIC for a calm "
    "pool, more FLIP for a violent splash.",
    "<b>APIC and PolyPIC are the principled alternatives.</b> They transfer "
    "additional information — an affine velocity field per "
    "particle — which eliminates the noise without the damping, "
    "largely removing the need for the blend parameter. They are the better "
    "answer and are increasingly standard."]),

  ("h1", "3 &nbsp; The material point method"),
  ("callout", "MPM: the same hybrid structure, applied to everything",
   ["MPM uses the same transfer structure as FLIP — particles to grid, "
    "solve on the grid, transfer back, move particles — but the "
    "particles carry <b>deformation gradients</b> (Module 09) rather than "
    "just velocity.",
    "<b>So the same solver handles solids, fluids, and everything between.</b> "
    "A constitutive model is evaluated per particle; change it and the same "
    "code simulates elastic rubber, viscous honey, or granular sand.",
    "<b>Topology change is automatic.</b> Fracture, melting, merging, and "
    "tearing require no special handling, because the grid is discarded and "
    "rebuilt every step — there is no mesh whose connectivity would "
    "have to be updated. This is the property that made it transformative "
    "for effects work.",
    "<b>This is the snow in Disney's Frozen</b>, which was the result that "
    "brought MPM into graphics, and it is now the standard approach for "
    "sand, mud, snow, and viscoelastic materials."]),
  ("table", ["Buys", "Costs"],
   [["<b>One solver for solid, fluid, and granular materials.</b>",
     "Expensive — a full grid solve every step, plus particle-grid "
     "transfers in both directions."],
    ["<b>Topology change for free.</b>",
     "Grid artefacts: detail is limited by cell size, and features aligned "
     "with the grid can be favoured."],
    ["Plasticity and fracture fall out of the constitutive model.",
     "<b>Numerical cohesion</b> — material that has separated tends to "
     "clump back together, because the grid couples anything within a cell "
     "of anything else. The characteristic MPM artefact, and visible in a "
     "great deal of published work once you know to look."],
    ["<b>Multi-material coupling is automatic.</b> Sand in water needs no "
     "special treatment.",
     "Many particles per cell are required for accuracy — typically "
     "four to eight — so memory grows quickly."]],
   [0.45, 0.55]),

  ("h1", "4 &nbsp; Choosing a method"),
  ("table", ["Phenomenon", "Method", "Reasoning"],
   [["Smoke, fire, gas.", "<b>Eulerian grid</b> (Module 11).",
     "Fills the domain, no free surface to track, and the grid's dissipation "
     "can be fought with vorticity confinement."],
    ["<b>Splashing liquid, spray.</b>", "<b>FLIP or APIC.</b>",
     "<b>Exact advection and an implicit free surface from the particles, "
     "with the pressure solve on the grid.</b> The standard choice in "
     "film."],
    ["Real-time or interactive water.", "<b>PBF.</b>",
     "Stable at large time steps and GPU-friendly. Accuracy is not the "
     "binding constraint."],
    ["Viscous or sticky fluid — honey, lava.", "SPH or MPM.",
     "Viscosity is natural in SPH; MPM if plasticity is also wanted."],
    ["<b>Sand, snow, mud, granular material.</b>", "<b>MPM.</b>",
     "<b>Plasticity and topology change are exactly what it provides.</b>"],
    ["Large ocean surface.", "<b>Spectral FFT wave model.</b>",
     "<b>Not a fluid simulation at all</b> — see below."]],
   [0.26, 0.22, 0.52]),
  ("callout", "Not everything that looks like fluid is simulated",
   ["<b>Ocean surfaces in film are almost never simulated.</b> "
    "Tessendorf's spectral method synthesises a statistically correct ocean "
    "surface directly in the frequency domain, using measured wave spectra, "
    "and transforms it with an FFT.",
    "<b>It is vastly cheaper than a simulation, trivially tileable over an "
    "unlimited area, directly controllable through wind speed and fetch "
    "parameters, and it looks better</b> than any fluid simulation at an "
    "affordable resolution — because it reproduces the correct "
    "statistics of a real ocean rather than approximating the dynamics.",
    "<b>A simulation is worth its cost only where the interaction "
    "matters:</b> a ship's wake, a breaking wave, water striking an object.",
    "<b>So the production answer is hybrid:</b> a spectral ocean for the "
    "bulk, a simulated region where something is happening, and the two "
    "blended and composited. Knowing when <i>not</i> to simulate is part of "
    "the skill, and it is the same judgement Module 01 described as the "
    "difference between a graphics simulation and a scientific one."]),
 ],
 "resources": [
   ("Bridson &mdash; Fluid Simulation for Computer Graphics",
    "https://www.cs.ubc.ca/~rbridson/fluidsimulation/",
    "The PIC/FLIP chapters are the reference for &sect;2, and the free notes "
    "cover the transfers in detail."),
   ("M&uuml;ller, Charypar & Gross &mdash; Particle-Based Fluid Simulation "
    "(SPH, free)",
    "https://matthias-research.github.io/pages/publications/publications.html",
    "The SPH formulation of &sect;1 as graphics uses it."),
   ("Macklin & M&uuml;ller &mdash; Position Based Fluids (2013, free)",
    "https://mmacklin.com/pubs.html",
    "PBF. Short, and the algorithm follows directly from Module 04."),
   ("Jiang et al. &mdash; The Material Point Method for Simulating Continuum "
    "Materials (SIGGRAPH course, free)",
    "https://www.seas.upenn.edu/~cffjiang/mpmcourse.html",
    "The definitive free introduction to &sect;3, with code."),
   ("Tessendorf &mdash; Simulating Ocean Water (free)",
    "https://people.computing.clemson.edu/~jtessen/",
    "The spectral ocean model of &sect;4. Read it before simulating an "
    "ocean."),
 ],
 "exercises": [
   "Implement SPH in 2D with a cubic spline kernel. Verify that the density "
   "sum reproduces the correct density for a uniform particle arrangement.",
   "Demonstrate SPH compressibility: drop a column of fluid and measure the "
   "maximum density excess. Then increase the stiffness and report the "
   "effect on both compression and the stable time step.",
   "Implement position-based fluids and compare stability and time step "
   "against your SPH implementation.",
   "Implement PIC. Simulate a dam break and observe the damping — "
   "report how quickly the splash dies.",
   "Change one line to make it FLIP. Observe the noise. Then implement the "
   "blend and find the ratio you prefer.",
   "Plot kinetic energy over time for pure PIC, pure FLIP, and a 95/5 blend "
   "on the same scenario.",
   "Measure volume conservation for your FLIP solver and compare against the "
   "grid-based liquid from Module 11. Report both.",
   "Implement APIC and compare against the FLIP/PIC blend on noise and "
   "energy retention.",
   "Implement a basic MPM solver with an elastic constitutive model, then "
   "change only the model to produce sand. Document that nothing else "
   "changed.",
   "Demonstrate MPM numerical cohesion: separate two pieces of material and "
   "show them clumping back together. Report the separation distance at "
   "which it stops.",
   "Implement Tessendorf's spectral ocean and compare against a FLIP "
   "simulation of the same ocean at the same cost. Be honest about which "
   "looks better.",
 ],
 "selfcheck": [
   "Compare Eulerian and Lagrangian representations on four axes.",
   "Write the SPH interpolation formula and say what the kernel does.",
   "Why do derivatives fall on the kernel rather than the data?",
   "Why is incompressibility fundamentally difficult for SPH, and what does "
   "classic SPH do about it?",
   "What constraint does PBF enforce, and what does it inherit from PBD?",
   "Give the four steps of PIC/FLIP and say what each representation "
   "contributes.",
   "What is the single difference between PIC and FLIP, and what are the two "
   "failure modes?",
   "Why does everyone blend them, and what does APIC change?",
   "What do MPM particles carry, and what three things does that enable?",
   "What is numerical cohesion?",
   "Why are film oceans usually not simulated?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Shipping a Simulator",
 "subtitle": "Determinism, time steps, sleeping, and the parts nobody "
             "writes papers about.",
 "question": "What stands between a working simulation and a usable one?",
 "outcomes": [
     "Decouple the simulation time step from the render frame rate.",
     "Implement sleeping and explain the hysteresis it needs.",
     "Achieve and maintain determinism.",
     "Build the debugging tools a simulator requires.",
     "Expose controls that an artist can actually use.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Time",
   "blurb": "The simulation step and the frame rate are different things."},

  {"t": "callout", "title": "Never step the simulation by the frame time",
   "kind": "The rule",
   "body": ["A variable time step means the physics changes with the "
            "hardware. The same scene behaves differently on a fast machine "
            "and a slow one.",
            "<b>Determinism is gone immediately</b> (Module 01), and with it "
            "replays, network sync, and reproducible bug reports.",
            "<b>And stability varies:</b> one long frame can exceed the "
            "stability limit and destroy the simulation.",
            "<b>Use a fixed step and accumulate.</b> Run as many fixed steps "
            "as the elapsed time allows, and interpolate the render state "
            "between the last two."]},

  {"t": "code", "kicker": "The pattern", "title": "Fixed step with interpolated rendering",
   "lang": "cpp", "code": """
const double DT = 1.0 / 120.0;     // fixed simulation step
double accumulator = 0.0;

void frame(double real_elapsed) {
    // Clamp: a long frame (a breakpoint, a stall) must not trigger
    // a hundred catch-up steps, which would stall further. Spiral
    // of death otherwise.
    accumulator += min(real_elapsed, 0.25);

    while (accumulator >= DT) {
        prev_state = current_state;      // keep for interpolation
        simulate(DT);
        accumulator -= DT;
    }

    // Render BETWEEN the two most recent states, not at the latest.
    double alpha = accumulator / DT;
    render(lerp(prev_state, current_state, alpha));
}
""",
   "caption": "The clamp prevents the spiral of death; the interpolation "
              "prevents visible temporal aliasing when the rates do not "
              "divide evenly.",
   "note": "Both details are necessary. Without interpolation you get "
           "judder; without the clamp you get a hang."},

  {"t": "section", "label": "Part 2", "title": "Sleeping",
   "blurb": "A settled object should cost nothing."},

  {"t": "callout", "title": "Sleeping needs hysteresis",
   "kind": "The design",
   "body": ["A body whose velocity has stayed below a threshold for several "
            "frames is <b>put to sleep</b>: removed from integration and "
            "from the solver entirely.",
            "<b>A single threshold oscillates.</b> The body sleeps, gravity "
            "or a neighbour wakes it, it sleeps again — and the wake/sleep "
            "churn costs more than never sleeping.",
            "<b>So use two thresholds and a timer:</b> sleep below a low "
            "velocity sustained for N frames; wake above a higher one "
            "immediately.",
            "<b>And wake islands together.</b> If one body in a contact "
            "group wakes, the whole group must — or a box wakes and the "
            "crate it is resting on does not."]},

  {"t": "bullets", "kicker": "Islands", "title": "Simulation islands",
   "items": [
     "<b>Group bodies connected by contacts or joints</b> into independent "
     "islands.",
     "",
     "<b>Solve each island separately.</b> They do not interact this step, "
     "by construction.",
     "",
     "<b>Sleep and wake per island</b>, not per body.",
     "",
     "<b>Solve islands in parallel</b> — they are independent, which is "
     "the cleanest parallelism available in a physics engine.",
     "",
     "<b>And a large island defeats all of this.</b> One long chain of "
     "contacts makes everything one island; this is why a big pile of "
     "objects is slow.",
   ],
   "note": "Island construction is a connected-components pass, cheap, and "
           "it enables three different optimisations at once."},

  {"t": "section", "label": "Part 3", "title": "Determinism",
   "blurb": "Harder than it sounds, and necessary."},

  {"t": "table", "kicker": "Threats", "title": "What breaks determinism",
   "header": ["Cause", "Fix"],
   "widths": [4.6, 7.5],
   "rows": [
     ["Variable time step", "<b>Fixed step (Part 1)</b>"],
     ["Hash container iteration order", "<b>Sort, or use ordered containers</b>"],
     ["Parallel reduction order", "<b>Fixed partitioning; deterministic reduce</b>"],
     ["Uninitialised memory", "Zero-initialise; run under a sanitiser"],
     ["Uncontrolled RNG seeds", "Seed explicitly; store the seed"],
     ["<b>Cross-platform float differences</b>", "<b>Very hard. Often abandoned</b>"],
   ],
   "footnote": "Floating-point addition is not associative, so summing in a "
               "different order gives a different answer.",
   "note": "Same-machine determinism is achievable and worth it. "
           "Cross-platform is a research-grade problem."},

  {"t": "callout", "title": "Same-machine determinism is the achievable goal",
   "kind": "Scope it correctly",
   "body": ["<b>Same binary, same machine, same input, bit-identical "
            "output</b> — this is achievable and is what debugging needs.",
            "<b>Cross-platform determinism is far harder.</b> Different "
            "compilers, SIMD widths, fused multiply-add availability, and "
            "transcendental implementations all produce different results.",
            "<b>Lockstep networked games need it</b> and pay a real price: "
            "fixed-point arithmetic, software transcendentals, strict "
            "compiler flags.",
            "<b>For everything else, aim at same-machine</b> and get the "
            "debugging benefit without the cost."]},

  {"t": "section", "label": "Part 4", "title": "Tools and controls",
   "blurb": "What the simulator needs around it."},

  {"t": "bullets", "kicker": "Debugging", "title": "The tools worth building",
   "items": [
     "<b>Frame stepping and rewind.</b> Non-negotiable. The interesting "
     "moment is always one frame before you noticed.",
     "",
     "<b>Visualise contacts:</b> points, normals, and impulse magnitudes. "
     "Most bugs are visible instantly this way.",
     "",
     "<b>Visualise islands and sleep state</b> by colour.",
     "",
     "<b>Record and replay:</b> capture the full input stream so a failure "
     "can be reproduced exactly.",
     "",
     "<b>Energy and momentum plots</b> (Module 01). Still the best "
     "diagnostic you have.",
     "",
     "<b>A stress scene</b> that runs in CI and asserts invariants.",
   ],
   "footnote": "Contact visualisation is the highest-value tool per hour of "
               "implementation."},

  {"t": "callout", "title": "Expose controls, not constants",
   "kind": "Module 01's requirement, concretely",
   "body": ["<b>Per-object gravity scale.</b> A cape that should drape "
            "faster than reality does.",
            "<b>Damping multipliers</b> separate from material parameters, "
            "so motion can be calmed without changing the material.",
            "<b>Time-ranged forces:</b> this wind acts on frames 40–90.",
            "<b>Target shapes</b> the simulation is attracted toward, with "
            "an adjustable strength. This is how simulations are made to hit "
            "a required pose.",
            "<b>Caching and sub-frame output</b>, so a simulation is run "
            "once and reviewed many times."]},

  {"t": "bullets", "kicker": "End", "title": "Where this course leaves you",
   "items": [
     "You can express any physical system as state and derivative, and "
     "choose an integrator for a reason.",
     "You can tell an instability from a constraint failure from a collision "
     "failure — which is most of the practical skill.",
     "You know which methods are physically derived and which are not, and "
     "why the latter often win.",
     "",
     "<b>CSCE 647</b> renders what you have simulated. <b>CSCE 641</b> is "
     "the pipeline it goes through. <b>CSCE 650</b> adds a frame budget and "
     "a person inside it.",
     "",
     "<b>And you have a simulator whose failures you can explain.</b> Every "
     "simulator has them.",
   ]},
 ],
 "takeaways": [
   "Never step the simulation by the frame time. Use a fixed step with an "
   "accumulator, a clamp against the spiral of death, and interpolated "
   "rendering.",
   "Sleeping needs two thresholds and a timer, or the wake/sleep churn costs "
   "more than never sleeping.",
   "Group connected bodies into islands: solve separately, sleep together, "
   "and parallelise across them.",
   "Determinism breaks on variable steps, hash ordering, parallel reduction "
   "order, uninitialised memory, and unseeded RNGs.",
   "Aim for same-machine determinism; cross-platform costs fixed-point "
   "arithmetic and is rarely worth it outside lockstep networking.",
   "Expose unphysical controls deliberately — per-object gravity, "
   "damping multipliers, time-ranged forces, target shapes. This is what "
   "makes a simulator usable.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Time"),
  ("callout", "Never step the simulation by the elapsed frame time",
   ["It is the obvious thing to do and it is wrong in three separate ways.",
    "<b>The physics becomes hardware-dependent.</b> The same scene behaves "
    "differently on a fast machine and a slow one, because the integration "
    "error and the solver's convergence both depend on the step size. A bug "
    "reported by a user with different hardware cannot be reproduced.",
    "<b>Determinism is destroyed immediately</b> (Module 01), and with it "
    "replays, networked lockstep, and reproducible bug reports.",
    "<b>Stability becomes a lottery.</b> One unusually long frame — a "
    "texture load, a garbage collection, a breakpoint — produces a "
    "step that exceeds the stability limit and destroys the simulation."]),
  ("code", """const double DT = 1.0 / 120.0;
double accumulator = 0.0;

void frame(double real_elapsed) {
    accumulator += min(real_elapsed, 0.25);   // CLAMP: no death spiral
    while (accumulator >= DT) {
        prev_state = current_state;
        simulate(DT);
        accumulator -= DT;
    }
    double alpha = accumulator / DT;
    render(lerp(prev_state, current_state, alpha));   // INTERPOLATE
}"""),
  ("table", ["Detail", "Why it is necessary"],
   [["<b>The clamp</b>",
     "Without it, a single very long frame — after a breakpoint, say "
     "— queues up hundreds of catch-up steps. Those take longer than "
     "real time, which makes the next frame longer still, which queues more "
     "steps. <b>The 'spiral of death'</b>: the application hangs and never "
     "recovers. Clamping accepts that time has been lost rather than trying "
     "to catch up."],
    ["<b>The interpolation</b>",
     "The simulation rate and the display rate rarely divide evenly, so at "
     "any given frame the simulation is partway between two states. "
     "Rendering the most recent state produces visible judder — "
     "objects move in slightly uneven increments. Interpolating between the "
     "two most recent states by the leftover fraction removes it entirely, "
     "for the cost of storing one extra state."]],
   [0.17, 0.83]),

  ("h1", "2 &nbsp; Sleeping and islands"),
  ("callout", "Sleeping requires hysteresis",
   ["A body whose velocity has remained below a threshold for several "
    "consecutive frames is <b>put to sleep</b>: removed from integration, "
    "from the broad phase's dynamic set, and from the constraint solver. A "
    "settled stack should cost nothing at all.",
    "<b>A single threshold oscillates.</b> The body falls below it and "
    "sleeps; a neighbouring body's contact or an accumulated penetration "
    "correction nudges it awake; it settles and sleeps again. The "
    "wake-and-sleep churn costs more than never sleeping, and produces "
    "visible twitching.",
    "<b>So use two thresholds and a timer:</b> sleep when velocity stays "
    "below a low threshold for N consecutive frames; wake immediately when "
    "it exceeds a higher one. The gap between them is the hysteresis.",
    "<b>And wake islands together.</b> If any body in a connected contact "
    "group wakes, the entire group must wake — otherwise a box wakes "
    "and the crate it is resting on does not, so the box falls through it."]),
  ("ul", ["<b>Group bodies connected by contacts or joints into "
          "islands</b> — a connected-components pass over the contact "
          "graph, which is cheap.",
          "<b>Solve each island independently.</b> By construction they do "
          "not interact during this step, so the solver works on a much "
          "smaller problem and converges faster for the same iteration "
          "count.",
          "<b>Sleep and wake per island</b>, which solves the problem "
          "above.",
          "<b>Solve islands in parallel.</b> They are genuinely independent, "
          "which makes this the cleanest parallelism available in a physics "
          "engine — no locks, no ordering concerns, no determinism "
          "risk if the per-island work is itself deterministic.",
          "<b>And a single large island defeats all three benefits.</b> One "
          "long chain of contacts — a big pile of objects all touching "
          "— makes everything a single island that cannot be split, "
          "cannot sleep partially, and cannot be parallelised. This is why a "
          "large pile is disproportionately slow, and it is a structural "
          "limit rather than an implementation problem."]),

  ("break",),
  ("h1", "3 &nbsp; Determinism"),
  ("table", ["Cause", "Remedy"],
   [["<b>Variable time step.</b>", "Fixed step with an accumulator "
     "(&sect;1)."],
    ["<b>Iteration order over hash containers.</b>",
     "The order depends on insertion history and allocation addresses. Sort "
     "before iterating, or use ordered containers, or iterate over a stable "
     "index array."],
    ["<b>Parallel reduction order.</b>",
     "<b>Floating-point addition is not associative</b>, so summing the same "
     "values in a different order gives a different answer. Use a fixed "
     "partitioning with a deterministic reduction tree rather than "
     "whatever order threads happen to finish in."],
    ["<b>Uninitialised memory.</b>",
     "Zero-initialise everything and run under a sanitiser. This is the "
     "cause that takes longest to find."],
    ["<b>Uncontrolled random seeds.</b>",
     "Seed explicitly and store the seed with the recording."],
    ["<b>Cross-platform floating-point differences.</b>",
     "<b>Genuinely hard.</b> See below."]],
   [0.27, 0.73]),
  ("callout", "Scope the goal to same-machine determinism",
   ["<b>Same binary, same machine, same input, bit-identical output.</b> "
    "This is achievable with the measures above, and it is what debugging "
    "actually requires: the ability to reproduce a failure exactly and to "
    "verify that a fix changed what you think it changed.",
    "<b>Cross-platform determinism is a different and much harder "
    "problem.</b> Different compilers reorder floating-point operations "
    "differently; SIMD widths differ; fused multiply-add is available on "
    "some targets and not others, and changes results; and the "
    "implementations of transcendental functions are not specified to the "
    "last bit.",
    "<b>Lockstep networked games genuinely need it</b> and pay substantially "
    "for it: fixed-point arithmetic throughout, software implementations of "
    "every transcendental, strict compiler flags that disable optimisations, "
    "and a great deal of testing.",
    "<b>For everything else, aim at same-machine determinism.</b> It costs "
    "little and provides nearly all the debugging benefit."]),

  ("h1", "4 &nbsp; Tools and controls"),
  ("table", ["Tool", "Value"],
   [["<b>Frame stepping, pausing, rewind.</b>",
     "Non-negotiable. The interesting frame is always the one before you "
     "noticed something was wrong."],
    ["<b>Contact visualisation</b> — points, normals, and impulse "
     "magnitudes drawn in the viewer.",
     "<b>The highest value per hour of implementation in this list.</b> A "
     "wrong normal, a missing contact, or an enormous impulse is visible "
     "instantly and essentially invisible otherwise."],
    ["<b>Island and sleep-state visualisation</b> by colour.",
     "Makes the structure of &sect;2 visible, and immediately shows when an "
     "island is larger than it should be."],
    ["<b>Record and replay.</b>",
     "Capture the complete input stream so any failure can be reproduced "
     "exactly — which requires the determinism of &sect;3."],
    ["<b>Energy and momentum plots.</b>",
     "Module 01's harness, still the best diagnostic available."],
    ["<b>A stress scene in CI</b> that runs every commit and asserts "
     "invariants — no NaNs, bounded energy, the stack still "
     "standing.",
     "Catches regressions that nobody would notice by eye until much later."]],
   [0.30, 0.70]),
  ("callout", "Expose controls, not constants",
   ["Module 01 argued that art-directability is a hard requirement. "
    "Concretely, that means these:",
    "<b>Per-object gravity scale.</b> A cape that should settle faster than "
    "physics allows, a feather that should drift longer. One multiplier, and "
    "it is requested constantly.",
    "<b>Damping multipliers separate from material parameters</b>, so motion "
    "can be calmed without changing what the material is.",
    "<b>Time-ranged forces.</b> 'This wind acts on frames 40 to 90.' "
    "Completely unphysical and exactly what a shot requires.",
    "<b>Target shapes with adjustable attraction strength.</b> The "
    "simulation is pulled toward a specified pose, which is how a simulation "
    "is made to hit a required silhouette at a required frame.",
    "<b>Caching and sub-frame output</b>, so an expensive simulation is run "
    "once and reviewed, retimed, and rendered many times without rerunning "
    "it."]),
  ("p", "<b>Where this course leaves you:</b> able to express any physical "
        "system as a state vector and a derivative function, and to choose "
        "an integrator for a stated reason rather than by habit; able to "
        "distinguish an instability from a constraint failure from a "
        "collision failure, which is most of the practical skill; and clear "
        "about which methods in this field are derived from mechanics and "
        "which are not, and why the latter frequently win."),
  ("p", "<b>CSCE 647</b> renders what you have simulated here, "
        "<b>CSCE 641</b> is the pipeline it travels through, and "
        "<b>CSCE 650</b> adds a frame budget with a person inside it. And "
        "you have a simulator whose failure modes you can explain — "
        "which is the deliverable, because every simulator has them."),
 ],
 "resources": [
   ("Glenn Fiedler &mdash; Fix Your Timestep! (free)",
    "https://gafferongames.com/post/fix_your_timestep/",
    "The accumulator pattern of &sect;1, including the spiral of death and "
    "the interpolation. Short and definitive."),
   ("Glenn Fiedler &mdash; the rest of Gaffer On Games (free)",
    "https://gafferongames.com/",
    "Determinism, networked physics, and lockstep. The practical "
    "counterpart to &sect;3."),
   ("Erin Catto &mdash; Box2D source and GDC talks",
    "https://box2d.org/publications/",
    "Islands, sleeping, and the engineering of a shipped solver. Read "
    "<code>b2World::Solve</code> for the island construction of &sect;2."),
   ("Bullet Physics manual",
    "https://github.com/bulletphysics/bullet3",
    "Production concerns: determinism caveats, sleeping thresholds, and "
    "debug drawing interfaces."),
   ("Christer Ericson &mdash; blog archive (free)",
    "https://realtimecollisiondetection.net/blog/",
    "Numerical robustness and the practicalities of shipping physics code."),
 ],
 "exercises": [
   "Implement the fixed-step accumulator with interpolated rendering. "
   "Demonstrate judder with the interpolation removed.",
   "Trigger the spiral of death by removing the clamp and stalling a frame. "
   "Then restore the clamp.",
   "Run the same scenario at 30, 60, and 144 render frames per second and "
   "confirm the simulation result is identical.",
   "Implement sleeping with a single threshold and demonstrate the "
   "oscillation. Then add hysteresis and a timer.",
   "Implement simulation islands. Measure solve time for a scene of 1,000 "
   "separate objects against one of 1,000 objects in a single pile, and "
   "explain the difference.",
   "Parallelise across islands and report the speedup. Verify the result is "
   "still bit-identical.",
   "Achieve same-machine determinism and prove it: run a 10,000-step "
   "simulation twice and compare final states bit for bit.",
   "Break it deliberately in each of the five ways in &sect;3 and confirm "
   "each one shows up.",
   "Implement contact visualisation. Then introduce a sign error in a "
   "contact normal and confirm you can see it immediately.",
   "Build a stress scene and an invariant-checking harness, and run it as a "
   "test.",
   "Add per-object gravity scale and a target-shape attractor. Use them to "
   "make a cloth simulation hit a specified pose at a specified frame.",
   "<b>Project 2 is now due.</b> Submit the simulator, the videos, the "
   "energy or volume plots, the stability study, and the documented failure "
   "case.",
 ],
 "selfcheck": [
   "Give three reasons never to step the simulation by the frame time.",
   "What does the accumulator clamp prevent, and what does the interpolation "
   "prevent?",
   "Why does sleeping need two thresholds, and why must islands wake "
   "together?",
   "Give four benefits of simulation islands and one case that defeats them "
   "all.",
   "Name five causes of non-determinism and the remedy for each.",
   "Why is floating-point summation order a determinism problem?",
   "Why is cross-platform determinism so much harder, and who needs it?",
   "Name four debugging tools and say which has the highest value per hour "
   "spent.",
   "Give four unphysical controls a production simulator should expose, and "
   "say why.",
 ],
},

]
