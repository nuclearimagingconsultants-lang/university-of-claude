# -*- coding: utf-8 -*-
"""CSCE 649 — Modules 03-07."""

MODULES = [

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Particle Systems and Springs",
 "subtitle": "The simplest system, and most of cloth already.",
 "question": "What can you build out of masses and springs?",
 "outcomes": [
     "Implement a particle system with forces, emitters, and lifetimes.",
     "Derive the damped spring force and explain why damping must be "
     "relative.",
     "Build a mass-spring cloth with structural, shear, and bending "
     "springs.",
     "Explain why mass-spring models are fundamentally limited.",
     "Choose spring constants from material behaviour rather than by "
     "guessing.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Particles",
   "blurb": "Position, velocity, mass, and whatever else the effect needs."},

  {"t": "code", "kicker": "Force accumulation", "title": "The derivative function, in full",
   "lang": "cpp", "code": """
void ParticleSystem::derivative(const double* x, double t, double* dx) {
    unpack(x);                       // positions and velocities from state
    std::fill(force.begin(), force.end(), vec3(0));

    // 1. ACCUMULATE forces. Every force adds; none assigns.
    for (auto& f : force_generators) f->apply(pos, vel, force);

    // 2. Write the derivative: dp/dt = v,  dv/dt = F/m.
    for (int i = 0; i < n; i++) {
        dx_pos[i] = vel[i];
        dx_vel[i] = force[i] * inv_mass[i];     // inv_mass = 0 pins it
    }
}

// inv_mass rather than mass is deliberate: a pinned particle is
// inv_mass == 0, which needs no branch and no special case anywhere.
// This one choice removes a surprising amount of code later.
""",
   "caption": "Storing inverse mass rather than mass makes infinite mass "
              "free: a pinned particle is simply 1/m = 0.",
   "note": "The inverse mass trick pays off repeatedly — in constraints, "
           "in collision response, in rigid bodies."},

  {"t": "table", "kicker": "Forces", "title": "The standard force generators",
   "header": ["Force", "Form", "Note"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["Gravity", "F = m g", "Scales with mass, so all fall equally"],
     ["Drag (linear)", "F = −k v", "Cheap; correct at low speed"],
     ["Drag (quadratic)", "F = −k |v| v", "<b>Correct for air at speed</b>"],
     ["Spring", "<b>See Part 2</b>", "The one that needs care"],
     ["Viscous damping", "F = −k v", "<b>Removes energy globally</b>"],
     ["Vortex, wind, turbulence", "Procedural", "Art direction, not physics"],
   ],
   "footnote": "Global viscous damping is the simplest stabiliser and the "
               "easiest to overuse — it makes everything feel "
               "underwater.",
   "note": "Students reach for global damping to fix instability. It works "
           "and it is usually the wrong fix."},

  {"t": "section", "label": "Part 2", "title": "Springs",
   "blurb": "Where the subtlety is."},

  {"t": "eq", "kicker": "Hooke", "title": "The damped spring force",
   "eqs": [
     ("F = −k (|d| − L) · d̂",
      "The spring term. d is the vector between endpoints, L the rest "
      "length, d̂ the unit direction."),
     ("F = −k (|d| − L) · d̂  −  kd (v_rel · d̂) d̂",
      "With damping. Note: only the component of relative velocity ALONG "
      "the spring is damped."),
     ("F_a = +F,   F_b = −F",
      "Apply equal and opposite. Omitting this breaks momentum conservation "
      "immediately."),
   ],
   "caption": "Damping the full relative velocity rather than its axial "
              "component damps rotation too, and the cloth stops swinging.",
   "note": "The axial projection is the detail people omit. Show the "
           "difference in a swinging chain — it is unmistakable."},

  {"t": "callout", "title": "Three ways to get the damping wrong",
   "kind": "All of them common",
   "body": ["<b>Damping absolute velocity</b> instead of relative. The "
            "spring now resists motion through space, so a freely falling "
            "chain slows down. Momentum is not conserved.",
            "<b>Damping the full relative velocity</b> instead of its "
            "component along the spring. This resists rotation about the "
            "spring, so a pendulum stops swinging for no physical reason.",
            "<b>Applying force to only one endpoint.</b> Momentum is created "
            "from nothing, and the whole system drifts.",
            "<b>All three produce plausible-looking motion</b> and show up "
            "immediately in a momentum plot. This is what Module 01's "
            "harness is for."]},

  {"t": "section", "label": "Part 3", "title": "Mass-spring cloth",
   "blurb": "A grid of particles and three kinds of connection."},

  {"t": "table", "kicker": "Cloth", "title": "Three spring types, three jobs",
   "header": ["Type", "Connects", "Resists"],
   "widths": [2.6, 4.4, 5.1],
   "rows": [
     ["<b>Structural</b>", "Immediate neighbours (4-connected)", "<b>Stretching</b>"],
     ["<b>Shear</b>", "Diagonal neighbours", "<b>In-plane shearing</b>"],
     ["<b>Bending</b>", "Neighbours two apart", "<b>Folding out of plane</b>"],
   ],
   "footnote": "Without shear springs the grid collapses diagonally. "
               "Without bending springs it folds with no resistance at all.",
   "note": "Have them disable each type and watch what fails. It is the "
           "fastest way to understand what each one does."},

  {"t": "callout", "title": "Cloth should barely stretch, and that is the whole problem",
   "kind": "Why cloth is hard",
   "body": ["Real fabric stretches by a few percent at most. To get that "
            "from springs, the structural stiffness must be very high.",
            "<b>High stiffness means a tiny time step</b> (Module 02): "
            "Δt < 2√(m/k).",
            "<b>Low stiffness means visible stretching</b>, and cloth that "
            "looks like rubber. The 'super-elastic' look is the classic "
            "mass-spring failure.",
            "<b>There is no stiffness that is both affordable and "
            "correct.</b> The way out is implicit integration (Module 02), "
            "strain limiting (Module 10), or constraints (Module 04) — "
            "all three are responses to this slide."]},

  {"t": "bullets", "kicker": "Limits", "title": "Why mass-spring models are fundamentally limited",
   "items": [
     "<b>The behaviour depends on the mesh.</b> Rotate the triangulation and "
     "the material changes. Real cloth does not work that way.",
     "",
     "<b>No concept of volume.</b> A mass-spring cube can be inverted "
     "inside-out and the springs are perfectly happy.",
     "",
     "<b>Spring constants are not material parameters.</b> You cannot look "
     "up the k for silk; you tune until it looks right, then it breaks at a "
     "different resolution.",
     "",
     "<b>Anisotropy is accidental</b> rather than specified — it comes "
     "from the grid, not the material.",
     "",
     "<b>Module 09 fixes all of this</b> with continuum mechanics. "
     "Mass-spring is still everywhere because it is simple and fast.",
   ],
   "note": "Be honest that mass-spring is a practical model with no "
           "theoretical standing, and that it remains widely used anyway."},

  {"t": "section", "label": "Part 4", "title": "Choosing parameters",
   "blurb": "Deriving constants instead of guessing them."},

  {"t": "eq", "kicker": "Scaling", "title": "Make the material resolution-independent",
   "eqs": [
     ("k ∝ 1/L   for structural springs",
     "Halving the edge length should double the spring constant, or a finer "
     "mesh is a softer material."),
     ("m = ρ · A / n",
      "Distribute the real total mass over the particles by area, rather "
      "than assigning each particle a mass of 1."),
     ("ζ = kd / (2√(k m))",
      "Damping ratio. Target ζ ≈ 0.05–0.3; ζ = 1 is critically "
      "damped and looks dead."),
   ],
   "caption": "Parameterise by damping ratio rather than by raw damping "
              "constant, and the value stays meaningful across resolutions.",
   "note": "Resolution dependence is the bug that appears when the artist "
           "subdivides the mesh and the cloth changes behaviour."},

  {"t": "callout", "title": "Test at three resolutions, always",
   "kind": "The discipline",
   "body": ["Simulate the same scenario at coarse, medium, and fine "
            "resolution.",
            "<b>The gross behaviour should be similar.</b> If the fine mesh "
            "drapes completely differently, your parameters are "
            "resolution-dependent and the simulation is not a model of "
            "anything.",
            "<b>This will happen the first time.</b> It is the single most "
            "common defect in a hand-tuned mass-spring system.",
            "<b>It is also how an artist will find the bug</b> — by "
            "subdividing the mesh for a close-up and watching the cloth "
            "change character."]},

  {"t": "bullets", "kicker": "Effects", "title": "Particle systems as an effects tool",
   "items": [
     "<b>Emitters:</b> rate, initial velocity distribution, spawn region. "
     "Most of the look is here.",
     "",
     "<b>Lifetimes and fading:</b> particles age and are recycled. Use a "
     "free list, not allocation.",
     "",
     "<b>Forces that are not physical:</b> vortices, attractors, curl noise "
     "for turbulence. This is where art direction lives.",
     "",
     "<b>Sorting for rendering:</b> transparent particles need back-to-front "
     "ordering, which is a per-frame sort.",
     "",
     "<b>Scale:</b> millions of particles is routine. Structure of arrays, "
     "not array of structures.",
   ],
   "footnote": "Curl noise is the standard trick for divergence-free "
               "turbulence without simulating a fluid."},
 ],
 "takeaways": [
   "Store inverse mass rather than mass: a pinned particle is 1/m = 0, with "
   "no branch and no special case anywhere downstream.",
   "Forces accumulate; the derivative writes velocity and force over mass. "
   "Every force generator adds, never assigns.",
   "Damp only the component of <i>relative</i> velocity <i>along</i> the "
   "spring, and apply the force equally and oppositely.",
   "Cloth needs structural, shear, and bending springs — disable each "
   "and a different failure appears.",
   "Cloth must barely stretch, which needs high stiffness, which needs tiny "
   "steps. That tension drives Modules 04, 09, and 10.",
   "Spring constants are not material parameters. Scale k with edge length "
   "and parameterise damping by ratio, then test at three resolutions.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Particles"),
  ("p", "A particle is a position, a velocity, and a mass, plus whatever the "
        "effect requires: colour, age, size, temperature. The state vector "
        "is the concatenation of every particle's position and velocity, and "
        "the derivative function computes forces and divides by mass."),
  ("code", """void ParticleSystem::derivative(const double* x, double t, double* dx) {
    unpack(x);
    std::fill(force.begin(), force.end(), vec3(0));
    for (auto& f : force_generators) f->apply(pos, vel, force);  // accumulate
    for (int i = 0; i < n; i++) {
        dx_pos[i] = vel[i];
        dx_vel[i] = force[i] * inv_mass[i];
    }
}"""),
  ("callout", "Store inverse mass, not mass",
   ["This looks like a micro-optimisation and is not. <b>A particle with "
    "infinite mass — one that is pinned in place — has an inverse "
    "mass of exactly zero.</b>",
    "Multiplying the force by zero produces zero acceleration, with no "
    "branch, no special case, and no risk of a division by infinity.",
    "<b>The payoff compounds.</b> Constraint solvers (Module 04) weight "
    "corrections by inverse mass, and a pinned particle automatically "
    "receives none. Collision response (Module 06) divides impulses by the "
    "sum of inverse masses, and a collision with static geometry falls out "
    "as the case where one term is zero. Rigid bodies (Module 07) use "
    "inverse inertia tensors for exactly the same reason.",
    "<b>Choosing this representation at the start removes a surprising "
    "amount of special-case code later</b>, and every physics engine does "
    "it."]),
  ("table", ["Force", "Expression", "Notes"],
   [["Gravity", "F = m <b>g</b>",
     "Proportional to mass, so acceleration is independent of it — "
     "everything falls at the same rate, as it should."],
    ["Linear drag", "F = &minus;k <b>v</b>",
     "Cheap, and physically correct only at very low Reynolds number. Often "
     "used anyway as a stabiliser."],
    ["Quadratic drag", "F = &minus;k |<b>v</b>| <b>v</b>",
     "<b>The correct form for air at ordinary speeds.</b> Noticeably "
     "different for fast-moving particles."],
    ["Spring", "&sect;2", "The one that requires care."],
    ["Global viscous damping", "F = &minus;k <b>v</b> on everything",
     "<b>The simplest stabiliser and the easiest to overuse.</b> It removes "
     "energy from every mode indiscriminately, and a system with enough of "
     "it looks like it is moving underwater. Students reach for it to fix "
     "instability; it works, and it is almost always the wrong fix."],
    ["Wind, vortices, turbulence", "Procedural fields",
     "Art direction rather than physics, and entirely legitimate "
     "(Module 01)."]],
   [0.17, 0.25, 0.58]),

  ("h1", "2 &nbsp; Springs"),
  ("eq", "<b>F</b> = &minus;k ( |<b>d</b>| &minus; L ) "
         "<b>d&#770;</b> &nbsp;&minus;&nbsp; k<sub>d</sub> "
         "( <b>v</b><sub>rel</sub> &middot; <b>d&#770;</b> ) <b>d&#770;</b>"),
  ("p", "where <b>d</b> is the vector between the endpoints, L the rest "
        "length, <b>d&#770;</b> the unit vector along it, and "
        "<b>v</b><sub>rel</sub> the relative velocity of the endpoints. The "
        "force is applied <b>equally and oppositely</b> to the two ends."),
  ("callout", "Three ways the damping goes wrong, all common",
   ["<b>Damping absolute velocity rather than relative.</b> The spring then "
    "resists motion through space, so a chain falling freely under gravity "
    "slows down for no reason. Linear momentum is not conserved, and the "
    "momentum plot from Module 01 shows it immediately.",
    "<b>Damping the full relative velocity rather than its component along "
    "the spring.</b> This resists the endpoints moving <i>past</i> each "
    "other as well as toward and away, which means it resists rotation about "
    "the spring axis. A swinging pendulum made of such springs comes to rest "
    "for no physical reason, and cloth stops moving unnaturally quickly. "
    "<b>The projection onto <b>d&#770;</b> is what prevents this</b>, and it "
    "is the detail most often omitted.",
    "<b>Applying the force to only one endpoint.</b> Momentum is created "
    "from nothing and the whole assembly drifts across the screen.",
    "<b>All three produce motion that looks superficially plausible</b>, "
    "which is why they survive. All three are caught instantly by plotting "
    "total momentum, which is what the Module 01 harness is for."]),

  ("break",),
  ("h1", "3 &nbsp; Mass-spring cloth"),
  ("p", "Cloth, at its simplest, is a grid of particles connected by three "
        "kinds of spring. It is worth implementing even though Module 09 "
        "will explain why it is theoretically unsound, because almost every "
        "real-time cloth system is some descendant of it."),
  ("table", ["Spring type", "Connects", "Resists", "Without it"],
   [["<b>Structural</b>", "Each particle to its four immediate grid "
     "neighbours.", "<b>Stretching and compression.</b>",
     "The cloth has no integrity at all."],
    ["<b>Shear</b>", "Each particle to its four diagonal neighbours.",
     "<b>In-plane shearing.</b>",
     "The grid collapses diagonally like a parallelogram linkage — a "
     "square of fabric flattens into a line."],
    ["<b>Bending</b>", "Each particle to the neighbours two steps away.",
     "<b>Folding out of plane.</b>",
     "The cloth folds with no resistance and takes sharp creases that no "
     "fabric would."]],
   [0.15, 0.27, 0.22, 0.36]),
  ("p", "<b>Disable each type in turn and watch what fails.</b> It takes ten "
        "minutes and explains the roles better than any description."),
  ("callout", "The central difficulty: cloth should barely stretch",
   ["Real fabric extends by a few percent under its own weight, no more. "
    "Reproducing that with springs requires a very high structural "
    "stiffness.",
    "<b>High stiffness forces a tiny time step</b> — Module 02's bound "
    "&Delta;t &lt; 2&radic;(m/k) — and the cost of a simulation scales "
    "accordingly.",
    "<b>Low stiffness gives visible stretching</b>, and the result is the "
    "classic 'super-elastic' mass-spring look: a tablecloth that behaves "
    "like a sheet of rubber, sagging under its own weight in a way no fabric "
    "does.",
    "<b>There is no stiffness value that is both affordable and "
    "correct.</b> This single tension drives three later modules: implicit "
    "integration (Module 02 &sect;3) makes high stiffness affordable, "
    "position-based constraints (Module 04) sidestep stiffness entirely, and "
    "strain limiting (Module 10) enforces the inextensibility directly. All "
    "three are responses to this problem."]),
  ("h2", "3.1 &nbsp; Why mass-spring models are limited"),
  ("ul", ["<b>Behaviour depends on the mesh.</b> Rotate the triangulation by "
          "45&deg; and the material's stiffness changes direction with it. "
          "Real cloth has properties independent of how you chose to "
          "discretise it.",
          "<b>There is no notion of volume.</b> A mass-spring cube can be "
          "turned inside out — every spring can be at its rest length "
          "in an inverted configuration — and nothing in the model "
          "objects. Deformable solids built this way collapse.",
          "<b>Spring constants are not material parameters.</b> You cannot "
          "look up the spring constant of silk. You tune until it looks "
          "right at one resolution, and the tuning does not transfer.",
          "<b>Anisotropy is accidental.</b> Fabric genuinely is anisotropic "
          "— warp and weft behave differently — but in a "
          "mass-spring model the anisotropy comes from the grid rather than "
          "from the material, so it cannot be specified.",
          "<b>Module 09 fixes all of this</b> with continuum mechanics, "
          "where the parameters are measurable material properties and the "
          "behaviour converges as the mesh refines. Mass-spring remains "
          "ubiquitous because it is simple, fast, and adequate when "
          "art-directed."]),

  ("h1", "4 &nbsp; Choosing parameters"),
  ("p", "The usual approach — picking spring constants by trial until "
        "the motion looks acceptable — produces a simulation that "
        "breaks the moment anything changes. These three relations make the "
        "parameters mean something."),
  ("table", ["Relation", "Why"],
   [["<b>k &prop; 1/L</b> for structural springs.",
     "A finer mesh has shorter edges. If k is held constant, a subdivided "
     "mesh is a <i>softer</i> material, which is wrong. Scaling k inversely "
     "with rest length keeps the macroscopic stiffness fixed."],
    ["<b>m = &rho;A/n</b>, distributing real mass by area.",
     "Assigning every particle a mass of 1 means a finer mesh is a heavier "
     "cloth. Distribute the actual total mass across the particles."],
    ["<b>&zeta; = k<sub>d</sub> / (2&radic;(km))</b> — parameterise "
     "by damping <i>ratio</i>.",
     "The raw damping constant has no meaning independent of k and m. The "
     "damping ratio does: &zeta; = 1 is critically damped and looks "
     "lifeless; <b>&zeta; between 0.05 and 0.3 is the useful range</b> for "
     "most fabric. The value transfers across resolutions and materials."]],
   [0.33, 0.67]),
  ("callout", "Test at three resolutions, every time",
   ["Run the same scenario at coarse, medium, and fine mesh resolution and "
    "compare the results.",
    "<b>The gross behaviour must be similar.</b> The fine mesh will have "
    "more detail — smaller folds, finer wrinkles — but the "
    "cloth should drape to roughly the same shape and settle in roughly the "
    "same time.",
    "<b>If the fine mesh behaves like a different material, your parameters "
    "are resolution-dependent</b> and the simulation is not a model of "
    "anything. It is a one-off tuned to a single mesh.",
    "<b>This will happen the first time you try it</b>, and it is the most "
    "common defect in a hand-tuned mass-spring system. It is also how an "
    "artist will eventually find it — by subdividing a mesh for a "
    "close-up shot and discovering the cloth has changed character, three "
    "days before the deadline."]),
  ("h1", "5 &nbsp; Particles as an effects tool"),
  ("ul", ["<b>Emitters</b> define spawn rate, spawn region, and the "
          "distribution of initial velocities. <b>Most of a particle "
          "effect's character is decided here</b>, not in the simulation.",
          "<b>Lifetimes.</b> Particles age, fade, and are recycled. Use a "
          "free list and a fixed-capacity pool — allocating per "
          "particle at scale is the single most common performance mistake.",
          "<b>Unphysical forces.</b> Vortex rings, attractors, and "
          "<b>curl noise</b> for turbulence. Curl noise is the standard "
          "trick: take the curl of a noise field and the result is "
          "divergence-free by construction, which gives swirling, "
          "fluid-looking motion without simulating a fluid at all.",
          "<b>Rendering order.</b> Transparent particles must be drawn "
          "back-to-front, which means a per-frame sort by view depth. At a "
          "million particles this is a real cost and often the bottleneck.",
          "<b>Data layout.</b> Millions of particles is routine. Store "
          "structure-of-arrays rather than array-of-structures — the "
          "force loop touches positions and velocities and nothing else, and "
          "the difference in cache behaviour is several times."]),
 ],
 "resources": [
   ("Baraff & Witkin &mdash; Particle System Dynamics (free notes)",
    "https://graphics.pixar.com/tutorials/",
    "Section C of the course pack. Force generators, the architecture of "
    "&sect;1, and spring forces done correctly."),
   ("Provot &mdash; Deformation Constraints in a Mass-Spring Model (1995, "
    "free)",
    "https://graphics.stanford.edu/courses/cs468-02-winter/Papers/Rigidcloth.pdf",
    "The original three-spring cloth model of &sect;3, and the strain "
    "limiting idea that Module 10 develops."),
   ("Ten Minute Physics &mdash; cloth and softbody episodes",
    "https://matthias-research.github.io/pages/tenMinutePhysics/",
    "Working mass-spring cloth with code, and a clear demonstration of the "
    "stretching problem."),
   ("Bridson, Fedkiw & Anderson &mdash; Robust Treatment of Collisions, "
    "Contact and Friction for Cloth (free)",
    "https://www.cs.ubc.ca/~rbridson/docs/cloth2002.pdf",
    "Where mass-spring cloth has to go to become production-usable. Read "
    "before Module 10."),
   ("Robert Bridson &mdash; curl-noise for procedural flow (free)",
    "https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph2007-curlnoise.pdf",
    "The turbulence technique in &sect;5. Short paper, immediately "
    "useful."),
 ],
 "exercises": [
   "Implement a particle system with gravity and both linear and quadratic "
   "drag. Compare the terminal velocity of each against the analytic value.",
   "Implement a damped spring. Verify that total momentum is conserved for "
   "a free-floating chain of ten particles — the plot should be flat "
   "to floating-point precision.",
   "Deliberately implement each of the three damping errors from &sect;2 and "
   "show what each does to the momentum plot and to the motion.",
   "Build a mass-spring cloth with all three spring types. Disable each type "
   "in turn and record what fails.",
   "Find the maximum stable time step as a function of structural stiffness. "
   "Determine the stiffness at which the cloth stretches less than 5% under "
   "its own weight, and report the time step that requires.",
   "Implement the parameter scaling of &sect;4 and run the three-resolution "
   "test. Report whether the drape matches.",
   "Deliberately break the scaling — fix k regardless of edge length "
   "— and show how the material changes with resolution.",
   "Sweep the damping ratio from 0.01 to 1.0 and record the qualitative "
   "behaviour at each value. Identify the usable range for yourself.",
   "Implement curl noise turbulence for a particle effect and compare "
   "against plain Perlin noise applied as a force. The difference is "
   "striking.",
 ],
 "selfcheck": [
   "Why store inverse mass rather than mass? Give three places it pays off.",
   "Write the damped spring force and say what each term does.",
   "Give three ways spring damping is commonly implemented incorrectly and "
   "the symptom of each.",
   "Name the three cloth spring types and what fails without each.",
   "Why is cloth's inextensibility a problem for mass-spring models?",
   "Give four fundamental limitations of mass-spring models.",
   "Why must k scale with edge length, and what goes wrong otherwise?",
   "What is the damping ratio, and what range is useful?",
   "What is the three-resolution test and what does failing it mean?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Constraints",
 "subtitle": "Enforcing what must be true, instead of pushing toward it.",
 "question": "How do you make something exactly inextensible?",
 "outcomes": [
     "Distinguish hard constraints from penalty forces.",
     "Formulate constraints with Lagrange multipliers.",
     "Implement Gauss–Seidel constraint projection.",
     "Explain position-based dynamics and why it dominates in practice.",
     "Explain what XPBD fixes about PBD.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two ways to enforce a rule",
   "blurb": "Push toward it, or impose it."},

  {"t": "two", "kicker": "Approaches", "title": "Penalty and constraint",
   "lh": "Penalty forces",
   "l": ["Add a stiff spring that resists violation.",
         "<b>Simple</b> — it is just another force.",
         "<b>Never exactly satisfied.</b> Always some error.",
         ("Stiff spring ⟹ tiny time step (Module 02).", 1),
         "Stiffness is a tuning parameter with no physical meaning."],
   "rh": "Hard constraints",
   "r": ["Solve for the force that makes the constraint hold exactly.",
         "<b>Exactly satisfied</b> at every step.",
         "No stiffness, so no stiffness-induced step limit.",
         ("Requires solving a system of equations.", 1),
         "<b>The right answer, at the cost of a solver.</b>"],
   "note": "Penalty is what Module 03 did. This module replaces it, and the "
           "motivation is the cloth stiffness problem."},

  {"t": "eq", "kicker": "Formulation", "title": "Constraints as functions",
   "eqs": [
     ("C(x) = 0",
      "An equality constraint: distance fixed, point on a surface, two "
      "bodies joined."),
     ("C(x) ≥ 0",
      "An inequality constraint: do not penetrate. Active only when "
      "violated — which is what makes contact hard."),
     ("Example:  C = |p₁ − p₂| − L",
      "The inextensible rod. Zero when the distance equals the rest length."),
   ],
   "caption": "Writing the constraint as a scalar function is the step that "
              "makes everything else mechanical.",
   "note": "Emphasise that once C is written, the gradient gives the "
           "direction and the solver is generic."},

  {"t": "callout", "title": "The constraint force acts along the gradient",
   "kind": "The key structure",
   "body": ["A constraint force must not do work — it enforces a "
            "geometric condition, it does not add or remove energy.",
            "<b>That forces its direction:</b> it must be perpendicular to "
            "the allowed motion, which means parallel to ∇C.",
            "<b>So F = λ ∇C</b>, with a single unknown scalar λ per "
            "constraint — the Lagrange multiplier.",
            "<b>λ is the magnitude of the constraint force</b>, and it has "
            "physical meaning: for a contact it is the normal force, which "
            "is exactly what friction needs (Module 06)."]},

  {"t": "section", "label": "Part 2", "title": "Solving",
   "blurb": "Many constraints at once, cheaply."},

  {"t": "eq", "kicker": "The system", "title": "All constraints simultaneously",
   "eqs": [
     ("J M⁻¹ Jᵀ λ  =  −(J M⁻¹ F_ext + ...)",
      "J is the constraint Jacobian; each row is one constraint's gradient. "
      "Solve for all λ at once."),
     ("Sparse, symmetric, positive semi-definite",
      "So conjugate gradient works — but assembling and solving it every "
      "step is expensive."),
   ],
   "caption": "The global solve is correct and costly. Almost everyone "
              "iterates instead.",
   "note": "Present the global solve so they know what the iterative methods "
           "are approximating."},

  {"t": "code", "kicker": "Iterative", "title": "Gauss–Seidel projection",
   "lang": "cpp", "code": """
// Rather than solving all constraints at once, satisfy them one at a
// time, repeatedly. Each projection uses the results of the previous.
for (int iter = 0; iter < N_ITER; iter++) {
    for (auto& c : constraints) {
        double  Cval = c.evaluate(p);
        if (c.inequality && Cval >= 0) continue;   // inactive

        // Correction along the gradient, weighted by inverse mass.
        auto    grad = c.gradient(p);
        double  wsum = 0;
        for (int i : c.particles) wsum += inv_mass[i] * grad[i].sqnorm();
        if (wsum < 1e-12) continue;                // all bodies pinned

        double  s = Cval / wsum;                   // the scaling factor
        for (int i : c.particles)
            p[i] -= s * inv_mass[i] * grad[i];     // project
    }
}
// Converges to the true solution as N_ITER grows. In practice
// 4-20 iterations, and you accept the residual error.
""",
   "caption": "Inverse mass appears again: pinned particles have zero "
              "weight and absorb no correction, with no special case.",
   "note": "Gauss–Seidel uses updated values immediately, which converges "
           "faster than Jacobi but is order-dependent."},

  {"t": "callout", "title": "Iteration count becomes a stiffness dial",
   "kind": "A consequence to understand",
   "body": ["More iterations means constraints are satisfied more exactly, "
            "which means the material behaves more stiffly.",
            "<b>So stiffness depends on the solver settings</b>, not on a "
            "material parameter. The same cloth with 4 and 40 iterations is "
            "two different materials.",
            "<b>It also depends on the time step</b>, which is worse: change "
            "the frame rate and the material changes.",
            "<b>This is PBD's central flaw</b>, and XPBD exists to fix it. "
            "It is also, perversely, why PBD is popular — the dial is "
            "intuitive and never explodes."]},

  {"t": "section", "label": "Part 3", "title": "Position-based dynamics",
   "blurb": "The method that took over games."},

  {"t": "code", "kicker": "PBD", "title": "The whole algorithm",
   "lang": "cpp", "code": """
void step(double dt) {
    // 1. Predict positions with explicit integration, ignoring constraints.
    for (int i = 0; i < n; i++) {
        v[i] += dt * inv_mass[i] * f_ext[i];
        pred[i] = p[i] + dt * v[i];
    }

    // 2. PROJECT positions to satisfy constraints. Iterate.
    for (int it = 0; it < iters; it++)
        for (auto& c : constraints) c.project(pred, inv_mass);

    // 3. Derive velocity from the position change. This is the trick:
    //    velocity is an OUTPUT, not something we integrated.
    for (int i = 0; i < n; i++) {
        v[i] = (pred[i] - p[i]) / dt;
        p[i] = pred[i];
    }
}
""",
   "caption": "Step 3 is the idea. Because velocity is derived from the "
              "final positions, there is no mechanism by which the system "
              "can gain energy.",
   "note": "The 'velocity is an output' inversion is what makes PBD "
           "unconditionally stable. Make sure that lands."},

  {"t": "callout", "title": "PBD cannot explode, which is why it won",
   "kind": "The decisive property",
   "body": ["Positions are <b>projected</b>, never integrated forward from "
            "forces. A projection moves a point to a valid configuration; it "
            "cannot send it to infinity.",
            "<b>Velocity is then derived from the position change</b>, so it "
            "is bounded by construction.",
            "<b>There is no stiffness, so there is no stability limit.</b> "
            "Any time step, any material, any configuration — it will "
            "produce something.",
            "<b>For an interactive application that is worth more than "
            "physical correctness.</b> A game that is 10% wrong ships; a "
            "game that explodes when the player does something unexpected "
            "does not."]},

  {"t": "table", "kicker": "Honest", "title": "What PBD costs",
   "header": ["Problem", "Detail"],
   "widths": [4.0, 8.1],
   "rows": [
     ["<b>Stiffness is not a material</b>", "Depends on iteration count and &Delta;t"],
     ["Artificial damping", "Projection removes energy silently"],
     ["Order dependence", "Gauss–Seidel results depend on constraint ordering"],
     ["Poor convergence at scale", "Long chains propagate one link per iteration"],
     ["<b>Not a physical method</b>", "<b>You cannot derive it from mechanics</b>"],
   ],
   "footnote": "And it is in every major game engine, because none of these "
               "matter as much as never exploding.",
   "note": "The long-chain convergence problem is worth demonstrating — it "
           "is visually obvious and explains hierarchical solvers."},

  {"t": "callout", "title": "XPBD makes stiffness a real parameter",
   "kind": "The fix",
   "body": ["XPBD (extended PBD) reintroduces <b>compliance</b> α = 1/k "
            "— the inverse of stiffness — as an explicit parameter, "
            "and accumulates the Lagrange multiplier across iterations.",
            "<b>The result converges to a well-defined solution</b> that is "
            "independent of iteration count and time step.",
            "<b>α = 0 recovers a hard constraint</b>; larger α gives softer "
            "material, specified in real units.",
            "<b>It is a small change</b> — a few extra lines — and it "
            "removes PBD's worst defect. Use XPBD, not PBD."]},

  {"t": "bullets", "kicker": "Practice", "title": "Making constraint solvers behave",
   "items": [
     "<b>Substep rather than iterate.</b> Ten substeps with one iteration "
     "beats one step with ten iterations, and by a lot. This was the key "
     "finding of the 2019 small-steps paper.",
     "",
     "<b>Randomise or alternate constraint order</b> to reduce the bias from "
     "Gauss–Seidel's sequential nature.",
     "",
     "<b>Use graph colouring</b> to find independent constraint sets that "
     "can be solved in parallel.",
     "",
     "<b>Warm start:</b> begin each step from the previous step's "
     "multipliers. Large improvement for stacking.",
     "",
     "<b>Handle over-constrained systems</b> — they have no solution, and "
     "the solver must degrade rather than diverge.",
   ],
   "footnote": "Substepping over iterating is the single most valuable "
               "practical result in this module."},
 ],
 "takeaways": [
   "Penalty forces are simple and never exact, and their stiffness forces "
   "tiny time steps. Hard constraints are exact at the cost of a solver.",
   "Write the constraint as a scalar function C(x); the force acts along "
   "&nabla;C with magnitude &lambda;, which is physically meaningful.",
   "The global solve is a sparse symmetric system. Almost everyone uses "
   "Gauss–Seidel projection instead and accepts the residual.",
   "In PBD, iteration count and time step act as a stiffness dial — "
   "which means stiffness is not a material property. That is its central "
   "flaw.",
   "PBD projects positions and derives velocity from the change, so it "
   "cannot gain energy and cannot explode. That is why it dominates games.",
   "XPBD reintroduces compliance and accumulates multipliers, giving a "
   "solution independent of iterations and step size. Use XPBD.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two ways to enforce a rule"),
  ("table", ["", "Penalty forces", "Hard constraints"],
   [["Method", "Add a stiff spring that pushes back when the condition is "
     "violated.",
     "Solve for the force that makes the condition hold exactly."],
    ["Simplicity", "<b>Trivial</b> — it is just another force "
     "generator.",
     "Requires solving a system of equations each step."],
    ["Exactness", "<b>Never exact.</b> There is always a residual "
     "violation, because the restoring force is proportional to it.",
     "<b>Exact</b>, to solver tolerance."],
    ["Time step", "<b>Stiff spring forces a tiny step</b> (Module 02).",
     "No stiffness, so no stiffness-induced limit."],
    ["Parameters", "A stiffness with no physical meaning, tuned by hand.",
     "None, for a hard constraint."]],
   [0.13, 0.43, 0.44]),
  ("p", "Module 03 used penalty forces throughout, and ran directly into "
        "their limitation: cloth that should barely stretch needs a "
        "stiffness that makes the simulation unaffordable. Constraints are "
        "the way out."),
  ("eq", "C(x) = 0 &nbsp;&nbsp;(equality) &nbsp;&nbsp;&nbsp;&nbsp; "
         "C(x) &ge; 0 &nbsp;&nbsp;(inequality)"),
  ("p", "A constraint is a scalar function of the state that must be zero "
        "(or non-negative). The inextensible rod is "
        "C = |p&#8321; &minus; p&#8322;| &minus; L. Non-penetration is "
        "C = (p &minus; q)&middot;<b>n</b> &ge; 0. <b>Inequality constraints "
        "are harder</b> because they are active only sometimes, and "
        "determining which are active is itself part of the problem — "
        "which is why contact (Module 06) is the difficult case."),
  ("callout", "The constraint force acts along the gradient",
   ["A constraint force exists to enforce a geometric condition, not to add "
    "or remove energy. <b>So it must do no work</b>, which means it must be "
    "perpendicular to every motion the constraint permits.",
    "The directions the constraint permits are exactly those along which C "
    "does not change — the tangent space of the constraint surface. "
    "Perpendicular to that is the gradient. <b>So the constraint force must "
    "be parallel to &nabla;C.</b>",
    "<b>F = &lambda; &nabla;C</b>, where &lambda; is a single unknown scalar "
    "per constraint: the <b>Lagrange multiplier</b>. The direction is "
    "determined by geometry; only the magnitude has to be solved for, which "
    "is an enormous reduction in the size of the problem.",
    "<b>&lambda; is physically meaningful.</b> For a contact constraint it "
    "is the normal force, which is precisely the quantity Coulomb friction "
    "needs (Module 06). For a joint it is the force the joint is "
    "transmitting, which is what tells you when it should break."]),

  ("h1", "2 &nbsp; Solving"),
  ("eq", "J M<super>&minus;1</super> J<super>T</super> &lambda; = "
         "&minus;( J M<super>&minus;1</super> F<sub>ext</sub> + "
         "&#7775; J q&#775; )"),
  ("p", "Stacking every constraint's gradient as a row of the Jacobian J "
        "gives a linear system for all the multipliers simultaneously. The "
        "matrix is sparse, symmetric, and positive semi-definite, so "
        "conjugate gradient applies. <b>This is the correct solution</b>, "
        "and assembling and solving it every step is expensive enough that "
        "almost nobody does it in graphics."),
  ("code", """for (int iter = 0; iter < N_ITER; iter++)
  for (auto& c : constraints) {
    double Cval = c.evaluate(p);
    if (c.inequality && Cval >= 0) continue;        // inactive
    auto   grad = c.gradient(p);
    double wsum = 0;
    for (int i : c.particles) wsum += inv_mass[i] * grad[i].sqnorm();
    if (wsum < 1e-12) continue;                     // everything pinned
    double s = Cval / wsum;
    for (int i : c.particles) p[i] -= s * inv_mass[i] * grad[i];
  }"""),
  ("p", "<b>Gauss&ndash;Seidel projection</b> satisfies the constraints one "
        "at a time, repeatedly, each projection using the positions "
        "updated by the previous one. It converges to the true solution as "
        "the iteration count grows, and in practice four to twenty "
        "iterations are used and the residual error accepted."),
  ("p", "Note the inverse mass appearing again: the correction is "
        "distributed between the participating particles in proportion to "
        "their inverse masses, so a heavy particle moves less and a pinned "
        "particle (inverse mass zero) does not move at all — with no "
        "special case anywhere."),
  ("callout", "Iteration count becomes a stiffness dial, and that is a problem",
   ["With four iterations, the constraints are only approximately satisfied "
    "and the cloth stretches noticeably. With forty, they are nearly exact "
    "and the cloth is almost inextensible.",
    "<b>So the material's stiffness is determined by a solver setting "
    "rather than by a material parameter.</b> The same cloth at four and "
    "forty iterations is two different fabrics.",
    "<b>It also depends on the time step</b>, which is worse: the same "
    "simulation run at 30 Hz and 60 Hz produces materials of different "
    "stiffness. Changing the frame rate changes the physics.",
    "<b>This is position-based dynamics's central theoretical flaw</b>, and "
    "XPBD (&sect;4) exists to fix it. It is also, perversely, part of why "
    "PBD became popular: the dial is intuitive to an artist, responds "
    "predictably, and never explodes however far it is turned."]),

  ("break",),
  ("h1", "3 &nbsp; Position-based dynamics"),
  ("code", """void step(double dt) {
    for (int i = 0; i < n; i++) {                 // 1. predict
        v[i]   += dt * inv_mass[i] * f_ext[i];
        pred[i] = p[i] + dt * v[i];
    }
    for (int it = 0; it < iters; it++)            // 2. project
        for (auto& c : constraints) c.project(pred, inv_mass);
    for (int i = 0; i < n; i++) {                 // 3. derive velocity
        v[i] = (pred[i] - p[i]) / dt;
        p[i] = pred[i];
    }
}"""),
  ("callout", "Step 3 is the idea, and it is why PBD cannot explode",
   ["In a conventional simulator, velocity is integrated from forces and "
    "position is integrated from velocity. An error in the forces becomes an "
    "error in velocity, which becomes a larger error in position, which "
    "produces larger forces — the feedback loop that makes explicit "
    "methods unstable.",
    "<b>PBD inverts this.</b> Positions are <i>projected</i> onto valid "
    "configurations, and <b>velocity is then derived from how far the "
    "position actually moved</b>. Velocity is an output of the step, not "
    "something that was integrated.",
    "<b>A projection cannot send a point to infinity</b> — it moves it "
    "to a configuration satisfying the constraint, which is by construction "
    "a sensible place. And since velocity is computed from a bounded "
    "position change divided by the step, it too is bounded.",
    "<b>There is no stiffness parameter, so there is no stability limit.</b> "
    "Any time step, any material parameters, any configuration — PBD "
    "will produce <i>something</i>. For an interactive application that is "
    "worth more than physical fidelity: a game that is 10% wrong ships, and "
    "a game that explodes when a player wedges a crate into a doorway does "
    "not."]),
  ("table", ["Cost", "Detail"],
   [["<b>Stiffness is not a material property.</b>",
     "It depends on iteration count and time step. &sect;2."],
    ["<b>Artificial damping.</b>",
     "The projection step silently removes energy, and the amount depends on "
     "the solver settings. Bouncy things are hard to make bouncy."],
    ["<b>Order dependence.</b>",
     "Gauss&ndash;Seidel uses updated positions immediately, so the result "
     "depends on the order constraints are visited in. Deterministic, but "
     "biased — constraints solved last are satisfied best."],
    ["<b>Poor convergence on long chains.</b>",
     "Information propagates one constraint per iteration, so a chain of 100 "
     "links needs 100 iterations for a disturbance at one end to reach the "
     "other. A hanging rope visibly stretches near the anchor."],
    ["<b>It is not a physical method.</b>",
     "<b>You cannot derive PBD from Newtonian mechanics.</b> It is a "
     "procedure that produces plausible motion, and its parameters do not "
     "correspond to measurable quantities."]],
   [0.26, 0.74]),
  ("p", "<b>And it is in every major game engine</b>, because none of these "
        "defects matter as much as the guarantee of never exploding. This is "
        "Module 01's ordering — stability over accuracy — in its "
        "most extreme form, and it is worth being clear-eyed about: the "
        "theoretically indefensible method won on engineering grounds."),

  ("h1", "4 &nbsp; XPBD"),
  ("callout", "Compliance makes stiffness real again",
   ["<b>XPBD</b> (extended position-based dynamics, M&uuml;ller et al. 2016) "
    "reintroduces <b>compliance</b> &alpha; = 1/k — the inverse of "
    "stiffness — as an explicit per-constraint parameter, and "
    "accumulates the Lagrange multiplier across solver iterations rather "
    "than discarding it.",
    "<b>The result converges to a well-defined solution</b> determined by "
    "&alpha;, and independent of the iteration count and the time step. More "
    "iterations now improve <i>convergence</i> toward a fixed answer, rather "
    "than changing what the answer is.",
    "<b>&alpha; = 0 recovers an exactly hard constraint</b>; larger values "
    "give progressively softer material, specified in physically meaningful "
    "units that transfer between resolutions and frame rates.",
    "<b>The change is small</b> — a handful of extra lines per "
    "constraint and one accumulator — and it removes PBD's worst "
    "defect at essentially no cost. <b>There is no reason to implement plain "
    "PBD today.</b>"]),
  ("h1", "5 &nbsp; Making solvers behave"),
  ("ul", ["<b>Substep rather than iterate.</b> Given a fixed budget, taking "
          "ten substeps with one solver iteration each beats one step with "
          "ten iterations — substantially, and for materials across the "
          "whole stiffness range. This was the central finding of M&uuml;ller "
          "et al.'s 2019 'small steps' paper, and it is the most valuable "
          "practical result in this module.",
          "<b>Vary the constraint ordering</b> between iterations, by "
          "reversing or randomising. Gauss&ndash;Seidel's sequential nature "
          "biases the result toward constraints solved last, and alternating "
          "the order spreads that bias.",
          "<b>Use graph colouring to parallelise.</b> Constraints that share "
          "no particles are independent and can be projected simultaneously. "
          "Colouring the constraint graph identifies these sets, which is how "
          "PBD runs on a GPU.",
          "<b>Warm start.</b> Begin each step from the previous step's "
          "multipliers rather than from zero. For stacking and resting "
          "contact this is a large improvement, because the correct answer "
          "changes little between frames.",
          "<b>Handle over-constrained systems gracefully.</b> A particle "
          "pinned in two incompatible places has no valid configuration. The "
          "solver must settle into a compromise rather than oscillating or "
          "diverging — and this situation arises constantly in "
          "practice, usually from contact."]),
 ],
 "resources": [
   ("Baraff &mdash; Constrained Dynamics (free notes)",
    "https://graphics.pixar.com/tutorials/",
    "Section F of the course pack. The Lagrange multiplier formulation of "
    "&sect;1 and the global solve of &sect;2, derived properly."),
   ("M&uuml;ller et al. &mdash; Position Based Dynamics (2007, free)",
    "https://matthias-research.github.io/pages/publications/publications.html",
    "The original PBD paper. Short, and the algorithm is exactly &sect;3."),
   ("Macklin, M&uuml;ller & Chentanez &mdash; XPBD (2016, free)",
    "https://matthias-research.github.io/pages/publications/publications.html",
    "The compliance formulation of &sect;4. Read it immediately after the "
    "PBD paper."),
   ("M&uuml;ller et al. &mdash; Small Steps in Physics Simulation (2019, "
    "free)",
    "https://matthias-research.github.io/pages/publications/publications.html",
    "The substepping result in &sect;5. A short paper with a large practical "
    "payoff."),
   ("Erin Catto &mdash; Soft Constraints and Sequential Impulses (GDC, free)",
    "https://box2d.org/publications/",
    "The same ideas from the game-engine side, and the clearest explanation "
    "of warm starting."),
 ],
 "exercises": [
   "Implement a distance constraint by penalty force and by projection. "
   "Compare the residual violation and the maximum stable time step for "
   "each.",
   "Derive the gradient of the distance constraint by hand and verify it "
   "numerically by finite differences.",
   "Implement Gauss&ndash;Seidel projection for a chain of distance "
   "constraints. Plot the residual against iteration count.",
   "Build a hanging chain of 100 links and show the convergence problem: "
   "plot stretch along the chain for 1, 10, and 100 iterations.",
   "Demonstrate the stiffness problem: simulate the same cloth with 4, 10, "
   "and 40 iterations and measure the maximum stretch in each case.",
   "Repeat with the time step halved and show that the effective stiffness "
   "changes.",
   "Implement XPBD and repeat both experiments. Confirm the stretch now "
   "depends on compliance rather than on iterations or step size.",
   "Compare ten substeps with one iteration against one step with ten "
   "iterations, at equal cost. Report which is stiffer and which is more "
   "stable.",
   "Implement graph colouring for a cloth constraint set and report how many "
   "colours are needed and how large each independent set is.",
   "Construct an over-constrained system and show how your solver behaves. "
   "Then make it degrade gracefully.",
 ],
 "selfcheck": [
   "Compare penalty forces and hard constraints on four axes.",
   "Why must a constraint force act along the gradient of C?",
   "What is a Lagrange multiplier, and what does it mean physically for a "
   "contact?",
   "Describe Gauss&ndash;Seidel projection and the role of inverse mass in "
   "it.",
   "Why does iteration count act as a stiffness dial in PBD, and why is that "
   "a problem?",
   "Write the three steps of PBD and explain why step 3 makes it "
   "unconditionally stable.",
   "Give five costs of PBD, and say why it dominates anyway.",
   "What does XPBD add, and what does it fix?",
   "Why does substepping beat iterating, and what else improves a constraint "
   "solver?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Collision Detection",
 "subtitle": "Finding out what is touching what, fast enough.",
 "question": "How do you find all contacts among ten thousand moving "
             "objects?",
 "outcomes": [
     "Design a broad phase and justify the structure chosen.",
     "Implement the separating axis test and explain GJK.",
     "Distinguish discrete from continuous detection and explain "
     "tunnelling.",
     "Generate contact manifolds rather than single points.",
     "Handle self-collision for deformable objects.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Broad phase",
   "blurb": "Eliminating the pairs that obviously cannot touch."},

  {"t": "callout", "title": "n² pairs is the problem",
   "kind": "The arithmetic",
   "body": ["Ten thousand objects gives 50 million pairs per frame. At 60 Hz "
            "that is 3 billion pair tests per second before any real work.",
            "<b>Almost all of those pairs are nowhere near each other.</b>",
            "<b>The broad phase eliminates them cheaply</b> using bounding "
            "volumes, leaving a small candidate list for the expensive exact "
            "test.",
            "<b>Same structure as Module 04 of CSCE 647</b> — a cheap "
            "conservative test that lets you skip the overwhelming majority "
            "of the work. The pattern recurs throughout this field."]},

  {"t": "table", "kicker": "Structures", "title": "Broad phase options",
   "header": ["Structure", "Good for", "Weakness"],
   "widths": [2.9, 4.6, 4.6],
   "rows": [
     ["Uniform grid", "<b>Similar-sized objects</b>", "Wildly varying sizes"],
     ["Spatial hash", "Unbounded domains", "Hash collisions; cache behaviour"],
     ["<b>Sweep and prune</b>", "<b>Coherent motion</b>", "Degenerates when all move"],
     ["<b>Dynamic BVH</b>", "<b>Mixed sizes; the general answer</b>", "Rebuild or refit cost"],
     ["Octree / kd-tree", "Static scenes", "Poor for moving objects"],
   ],
   "footnote": "Sweep and prune exploits frame coherence: sorted order "
               "barely changes, so an insertion sort is nearly O(n).",
   "note": "Dynamic BVH with refitting is what most engines use, for the "
           "same reasons as CSCE 647 Module 04."},

  {"t": "callout", "title": "Exploit coherence — objects barely move",
   "kind": "The lever",
   "body": ["Between frames at 60 Hz, almost nothing moves far. <b>The "
            "answer is nearly the same as last frame.</b>",
            "<b>Sweep and prune</b> keeps endpoints sorted along each axis. "
            "Because the order barely changes, an insertion sort is almost "
            "linear and pair changes are incremental.",
            "<b>A dynamic BVH refits</b> rather than rebuilding: update node "
            "bounds bottom-up, and only rebuild subtrees whose quality has "
            "degraded.",
            "<b>Fatten the bounds</b> by a margin so an object can move a "
            "little without triggering an update at all. Standard in every "
            "engine."]},

  {"t": "section", "label": "Part 2", "title": "Narrow phase",
   "blurb": "The exact test, on the surviving pairs."},

  {"t": "callout", "title": "The separating axis theorem",
   "kind": "For convex shapes",
   "body": ["<b>Two convex shapes are disjoint if and only if there exists "
            "an axis on which their projections do not overlap.</b>",
            "For polyhedra, only a finite set of axes must be tested: each "
            "face normal of both shapes, plus the cross products of all edge "
            "pairs.",
            "<b>Finding a separating axis proves they are apart</b> and lets "
            "you exit immediately — which makes the common case cheap.",
            "<b>Finding none proves they overlap</b>, and the axis of "
            "minimum overlap gives the contact normal and the penetration "
            "depth for free."]},

  {"t": "table", "kicker": "Algorithms", "title": "The narrow-phase toolkit",
   "header": ["Method", "Handles", "Gives"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["Analytic", "Sphere–sphere, sphere–plane", "Exact, trivially cheap"],
     ["<b>SAT</b>", "Convex polyhedra", "Normal and depth"],
     ["<b>GJK</b>", "<b>Any convex shape</b>", "<b>Distance when separated</b>"],
     ["EPA", "GJK's companion", "Penetration depth when overlapping"],
     ["Triangle–triangle", "Meshes", "<b>The workhorse for deformables</b>"],
   ],
   "footnote": "GJK + EPA is the standard pairing: GJK for distance, EPA "
               "for depth once they overlap.",
   "note": "GJK operates on support functions, so it handles any shape you "
           "can write a support function for — including implicit ones."},

  {"t": "callout", "title": "GJK works on the Minkowski difference",
   "kind": "The idea in one slide",
   "body": ["<b>Two shapes intersect if and only if their Minkowski "
            "difference contains the origin.</b>",
            "GJK never builds that difference — it only needs a "
            "<b>support function</b>, which returns the furthest point of a "
            "shape in a given direction.",
            "It iteratively builds a simplex inside the difference, trying "
            "to enclose the origin. Converges in a handful of iterations.",
            "<b>Because it only needs support functions, it handles any "
            "convex shape</b>: boxes, cylinders, cones, convex hulls, and "
            "shapes defined implicitly. That generality is why it is "
            "everywhere."]},

  {"t": "section", "label": "Part 3", "title": "Time",
   "blurb": "The problem with testing only at frame boundaries."},

  {"t": "callout", "title": "Tunnelling: the bullet through the wall",
   "kind": "Why discrete detection fails",
   "body": ["Discrete detection tests only at the end of each step. A fast "
            "object can be in front of a wall at step n and behind it at "
            "step n+1.",
            "<b>No overlap is ever detected, so no collision occurs.</b> The "
            "bullet passes through.",
            "<b>It is not a bug in the test</b> — the test is correct at "
            "both instants. The failure is that the motion between them was "
            "never considered.",
            "<b>Worst for small fast objects and thin geometry</b>, which "
            "is exactly bullets and walls. Hence the name of the feature in "
            "most engines."]},

  {"t": "two", "kicker": "Two approaches", "title": "Discrete and continuous",
   "lh": "Discrete (a posteriori)",
   "l": ["Step, then look for overlap.",
         "<b>Cheap and simple.</b>",
         "<b>Tunnels.</b>",
         "Needs penetration recovery, which can pop.",
         ("The default everywhere.", 1)],
   "rh": "Continuous (a priori)",
   "r": ["Find the exact time of first contact in the interval.",
         "<b>No tunnelling. No penetration ever.</b>",
         "<b>Far more expensive</b>, and requires root finding.",
         "Can deadlock in dense contact.",
         ("Reserved for fast objects.", 1)],
   "note": "Nobody uses CCD for everything. Engines flag fast objects and "
           "use it selectively."},

  {"t": "bullets", "kicker": "Cheaper", "title": "Practical alternatives to full CCD",
   "items": [
     "<b>Substepping.</b> Smaller steps mean less movement per step. Often "
     "enough, and far simpler.",
     "",
     "<b>Speculative contacts.</b> Expand bounds by the distance that will "
     "be travelled and create constraints for contacts that <i>might</i> "
     "happen. Cheap and effective.",
     "",
     "<b>Swept bounds in the broad phase only.</b> Catches the pair; the "
     "narrow phase stays discrete.",
     "",
     "<b>Ray casting for small fast objects.</b> A bullet is better modelled "
     "as a ray than as a body.",
     "",
     "<b>Flag the objects that need it.</b> CCD on everything is "
     "unaffordable and unnecessary.",
   ],
   "note": "Speculative contacts are underrated — most of the benefit of "
           "CCD for a fraction of the complexity."},

  {"t": "section", "label": "Part 4", "title": "Manifolds and self-collision",
   "blurb": "What the narrow phase must actually produce."},

  {"t": "callout", "title": "One contact point is not enough",
   "kind": "Why manifolds matter",
   "body": ["A box resting flat on the ground touches along a face, not at a "
            "point.",
            "<b>With one contact point the box rocks</b>, because the solver "
            "can only resist rotation about a point. The stack jitters and "
            "eventually falls.",
            "<b>A contact manifold</b> is the full set of contact points "
            "— usually up to four for a face-face contact, after "
            "reduction.",
            "<b>Persist manifolds across frames</b> and match contact points "
            "by feature identity. This enables warm starting (Module 04) and "
            "is what makes stable stacking possible at all."]},

  {"t": "bullets", "kicker": "Self-collision", "title": "Cloth against itself",
   "items": [
     "<b>Every triangle can hit every other triangle</b>, so the broad phase "
     "operates within a single object.",
     "",
     "<b>Skip adjacent triangles</b> — they share vertices and always "
     "'intersect'. Topological adjacency must be excluded explicitly.",
     "",
     "<b>Vertex-triangle and edge-edge</b> are the two cases. Both are "
     "required; checking only vertex-triangle misses crossings.",
     "",
     "<b>Once interpenetrated, cloth rarely recovers.</b> Prevention beats "
     "resolution, which is why cloth uses CCD where rigid bodies do not.",
     "",
     "<b>Thickness.</b> Treat cloth as having a small thickness and "
     "separate before contact, not after.",
   ],
   "note": "The 'cannot recover' point justifies the extra expense — this "
           "is where cloth genuinely needs continuous detection."},
 ],
 "takeaways": [
   "n&#178; pair tests are infeasible; a cheap conservative broad phase "
   "eliminates almost all of them — the same pattern as a BVH in "
   "rendering.",
   "Exploit frame coherence: sweep and prune on nearly-sorted endpoints, BVH "
   "refitting, and fattened bounds that tolerate small motion.",
   "SAT proves separation by finding one axis; failing to find one gives the "
   "contact normal and penetration depth for free.",
   "GJK needs only a support function, so it handles any convex shape; EPA "
   "supplies penetration depth once they overlap.",
   "Discrete detection tunnels because the motion between tests is never "
   "considered. Substepping and speculative contacts are the cheap fixes.",
   "A single contact point makes a resting box rock. Generate and persist "
   "manifolds, which also enables warm starting.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Broad phase"),
  ("callout", "The arithmetic that forces a broad phase",
   ["Ten thousand objects give roughly 5 &times; 10<super>7</super> pairs. "
    "At 60 frames per second that is 3 &times; 10<super>9</super> pair tests "
    "per second — before any of them does useful work.",
    "<b>And almost every one of those pairs is nowhere near touching.</b> "
    "The great majority of the computation is spent establishing that "
    "objects on opposite sides of the level are not in contact.",
    "<b>The broad phase eliminates them cheaply</b> using bounding volumes "
    "— usually axis-aligned boxes — and passes a small candidate "
    "list to the exact narrow-phase test.",
    "<b>This is structurally identical to the acceleration structure "
    "argument in CSCE 647 Module 04</b>: a cheap conservative test that "
    "allows the overwhelming majority of work to be skipped. The pattern "
    "appears again in Module 10 of that course, for volume majorants, and it "
    "is worth recognising as a general technique rather than a "
    "domain-specific trick."]),
  ("table", ["Structure", "Suits", "Weakness"],
   [["<b>Uniform grid</b>", "Many objects of similar size in a bounded "
     "domain. Insertion and query are O(1).",
     "Objects much larger than a cell occupy many cells; objects much "
     "smaller waste them. Size variety is fatal."],
    ["<b>Spatial hash</b>", "An unbounded domain, by hashing cell "
     "coordinates rather than storing a grid.",
     "Hash collisions cause false candidate pairs; memory access is "
     "scattered, which hurts more than the asymptotic analysis suggests."],
    ["<b>Sweep and prune</b>",
     "<b>Coherent motion.</b> Keep interval endpoints sorted along each "
     "axis; overlapping intervals on all axes are candidate pairs.",
     "Degenerates when everything moves at once, and performs poorly when "
     "objects cluster densely along the sweep axis."],
    ["<b>Dynamic BVH</b>",
     "<b>Mixed object sizes and general scenes. The usual answer.</b>",
     "Requires refitting or periodic rebuilding as objects move."],
    ["<b>Octree / kd-tree</b>", "Largely static geometry.",
     "Poorly suited to moving objects — the same reason kd-trees lost "
     "to BVHs in rendering."]],
   [0.16, 0.42, 0.42]),
  ("callout", "Coherence is the lever",
   ["At 60 Hz, almost nothing moves far between frames. <b>The set of "
    "overlapping pairs this frame is nearly the set from last frame.</b> A "
    "broad phase that recomputes from scratch is discarding that "
    "information.",
    "<b>Sweep and prune</b> exploits it directly: the sorted order of "
    "endpoints barely changes, so an insertion sort — which is O(n) on "
    "nearly-sorted input — restores it, and the pairs that enter or "
    "leave the overlap set can be tracked incrementally.",
    "<b>A dynamic BVH refits rather than rebuilding:</b> update the leaf "
    "bounds and propagate upward, which is O(n) and preserves the tree "
    "topology. Quality degrades slowly as objects move apart, so subtrees "
    "are rebuilt selectively when a quality metric falls too far.",
    "<b>Fatten the bounds by a margin.</b> If an object's stored bound is "
    "larger than the object by some slack, the object can move within that "
    "slack without the structure needing any update at all. This single "
    "trick removes most of the update cost, and every engine does it."]),

  ("h1", "2 &nbsp; Narrow phase"),
  ("callout", "The separating axis theorem",
   ["<b>Two convex shapes are disjoint if and only if there exists an axis "
    "onto which their projections do not overlap.</b> Such an axis is called "
    "a separating axis.",
    "For convex polyhedra, only a finite set of candidate axes need be "
    "tested: the face normals of both shapes, and the cross products of "
    "every pair of edges, one from each. For two boxes that is 15 axes.",
    "<b>Finding a separating axis proves disjointness immediately</b>, so "
    "the test can return as soon as one is found — which makes the "
    "common case, where objects are far apart, very cheap.",
    "<b>Finding none proves the shapes overlap</b>, and the axis with the "
    "smallest overlap gives you the <b>contact normal</b> and the "
    "<b>penetration depth</b> directly, which is exactly what collision "
    "response (Module 06) needs. The test produces the answer and the "
    "response data together."]),
  ("table", ["Method", "Applies to", "Produces"],
   [["<b>Analytic tests</b>", "Sphere&ndash;sphere, sphere&ndash;plane, "
     "capsule&ndash;capsule.",
     "Exact answers in a few operations. Always special-case these."],
    ["<b>SAT</b>", "Convex polyhedra.",
     "Overlap or not; normal and depth when overlapping."],
    ["<b>GJK</b>", "<b>Any convex shape with a support function.</b>",
     "<b>Distance and closest points when separated.</b> Returns only "
     "'overlapping' when they intersect."],
    ["<b>EPA</b>", "GJK's companion, run when GJK reports overlap.",
     "Penetration depth and normal, by expanding a polytope within the "
     "Minkowski difference."],
    ["<b>Triangle&ndash;triangle</b>", "Arbitrary meshes.",
     "<b>The workhorse for deformables and cloth</b>, where nothing is "
     "convex."]],
   [0.16, 0.37, 0.47]),
  ("callout", "GJK operates on the Minkowski difference",
   ["The Minkowski difference of two sets is the set of all differences "
    "between a point in one and a point in the other. <b>Two shapes "
    "intersect if and only if their Minkowski difference contains the "
    "origin</b>, which converts an intersection question into a "
    "point-containment question.",
    "<b>GJK never constructs the difference</b>, which would be "
    "prohibitively expensive. It requires only a <b>support function</b>: "
    "given a direction, return the furthest point of the shape in that "
    "direction. The support function of the difference is the difference of "
    "the support functions.",
    "The algorithm iteratively builds a simplex — up to a tetrahedron "
    "— of points in the Minkowski difference, attempting to enclose the "
    "origin, and converges in a handful of iterations.",
    "<b>Because it needs only support functions, it handles any convex shape "
    "whatsoever:</b> boxes, spheres, capsules, cylinders, cones, convex "
    "hulls of point sets, and shapes defined only implicitly. That "
    "generality, more than its speed, is why it is in every physics engine."]),

  ("break",),
  ("h1", "3 &nbsp; The time dimension"),
  ("callout", "Tunnelling",
   ["Discrete collision detection tests for overlap at the end of each time "
    "step. A fast-moving object can be entirely in front of a thin wall at "
    "step n and entirely behind it at step n+1.",
    "<b>At no tested instant do the shapes overlap, so no collision is ever "
    "detected.</b> The bullet passes through the wall.",
    "<b>This is not a bug in the intersection test.</b> The test gave the "
    "correct answer at both instants. The failure is that the continuous "
    "motion between those instants was never considered at all.",
    "<b>It is worst for small fast objects against thin geometry</b> "
    "— which describes bullets and walls precisely, and is why the "
    "feature is labelled 'bullet' or 'continuous' in most engines."]),
  ("table", ["", "Discrete (a posteriori)", "Continuous (a priori)"],
   [["Method", "Advance the state, then test for overlap and resolve any "
     "that is found.",
     "Find the earliest time of contact within the step, advance to exactly "
     "that time, resolve, and continue."],
    ["Cost", "<b>Cheap.</b> One test per candidate pair per step.",
     "<b>Much more expensive.</b> Requires root finding on a function of "
     "time, per pair."],
    ["Tunnelling", "<b>Yes.</b>", "<b>No.</b>"],
    ["Penetration", "Objects interpenetrate and must be pushed apart, which "
     "can visibly pop.", "<b>Never occurs.</b>"],
    ["Failure mode", "Tunnelling; pops during recovery.",
     "Can deadlock: in dense contact, each resolution creates another "
     "contact at an earlier time and the step never completes."],
    ["Use", "<b>The default for essentially everything.</b>",
     "Selectively, for objects flagged as fast."]],
   [0.13, 0.42, 0.45]),
  ("ul", ["<b>Substepping.</b> Smaller steps mean less motion per step and "
          "proportionally less tunnelling. Often sufficient, and far simpler "
          "than CCD.",
          "<b>Speculative contacts.</b> Expand each object's bounds by the "
          "distance it will travel this step, and create contact constraints "
          "for collisions that <i>might</i> occur. The solver then prevents "
          "the penetration before it happens. Cheap, robust, and "
          "underrated — most of CCD's benefit for a fraction of the "
          "complexity.",
          "<b>Swept bounds in the broad phase only.</b> Use the union of the "
          "start and end bounds to catch the candidate pair, then run a "
          "discrete narrow phase. Catches the pair without the cost of a "
          "continuous exact test.",
          "<b>Ray casting for small fast objects.</b> A bullet has "
          "negligible extent; modelling it as a ray rather than a rigid body "
          "is both cheaper and more correct.",
          "<b>Flag objects individually.</b> Running CCD on every object is "
          "unaffordable and unnecessary — almost nothing in a scene "
          "moves fast enough to tunnel."]),

  ("h1", "4 &nbsp; Manifolds"),
  ("callout", "A single contact point is not enough",
   ["A box resting flat on the ground is in contact along an entire face, "
    "not at one point.",
    "<b>Given a single contact point, the solver can only resist rotation "
    "about that point</b>, so the box rocks. Next frame a different point is "
    "found, and it rocks the other way. The result is jitter, and in a stack "
    "the jitter compounds until the stack falls.",
    "<b>A contact manifold is the full set of contact points</b> between two "
    "shapes — typically reduced to at most four for a face-face "
    "contact, chosen to maximise the contact area they enclose. Four points "
    "are enough to resist rotation about every axis.",
    "<b>Persist manifolds between frames</b> and match contact points by "
    "feature identity (which face, which edge, which vertex), not by "
    "position. This enables the warm starting of Module 04, where each "
    "contact's accumulated impulse carries over, and <b>it is what makes "
    "stable stacking possible at all.</b> A stack of ten boxes standing for "
    "sixty seconds — Project 1's requirement — is a test of the "
    "manifold machinery more than of the solver."]),
  ("h1", "5 &nbsp; Self-collision"),
  ("ul", ["<b>The broad phase must operate within a single object.</b> For "
          "cloth, every triangle can potentially contact every other "
          "triangle of the same mesh, so a BVH over the object's own "
          "triangles is required — and it must be refitted every step, "
          "because the geometry deforms.",
          "<b>Adjacent triangles must be excluded explicitly.</b> Triangles "
          "sharing a vertex or an edge always 'intersect' by any geometric "
          "test, so topological adjacency has to be checked and skipped. "
          "Forgetting this produces a cloth that immediately locks solid.",
          "<b>Two cases are needed: vertex&ndash;triangle and "
          "edge&ndash;edge.</b> Checking only vertex&ndash;triangle misses "
          "configurations where two edges cross without any vertex being "
          "inside a triangle — which is exactly what happens when cloth "
          "folds.",
          "<b>Once cloth has interpenetrated, it rarely recovers.</b> There "
          "is no local information indicating which way to separate, and "
          "pushing apart arbitrarily tends to make the tangle worse. "
          "<b>Prevention is genuinely necessary here</b>, which is why cloth "
          "justifies continuous detection where rigid bodies do not.",
          "<b>Give cloth a thickness.</b> Treat each triangle as having a "
          "small offset volume and separate surfaces before they touch, "
          "rather than after they overlap. This is Bridson's approach and it "
          "is what makes production cloth robust."]),
 ],
 "resources": [
   ("Ericson &mdash; Real-Time Collision Detection",
    "https://realtimecollisiondetection.net/books/rtcd/",
    "The standard reference for this entire module. The author's errata and "
    "blog are free and substantial."),
   ("Gino van den Bergen &mdash; GJK materials (free)",
    "https://www.dtecta.com/",
    "GJK and its variants from someone who has implemented them repeatedly. "
    "The clearest free explanation of &sect;2."),
   ("Erin Catto &mdash; GDC talks on contact manifolds and continuous "
    "collision (free)",
    "https://box2d.org/publications/",
    "The manifold persistence of &sect;4 and speculative contacts of "
    "&sect;3, from production experience."),
   ("Bridson, Fedkiw & Anderson &mdash; Robust Treatment of Collisions, "
    "Contact and Friction for Cloth (free)",
    "https://www.cs.ubc.ca/~rbridson/docs/cloth2002.pdf",
    "The self-collision approach of &sect;5, including cloth thickness. The "
    "standard reference."),
 ],
 "exercises": [
   "Implement brute-force n&#178; broad phase and a uniform grid. Plot query "
   "time against object count for both and find the crossover.",
   "Implement sweep and prune. Measure the cost per frame with objects "
   "moving slowly and with objects moving randomly, and explain the "
   "difference.",
   "Implement a dynamic BVH with refitting and bound fattening. Report how "
   "the fattening margin trades update cost against candidate pair count.",
   "Implement SAT for boxes. Verify that the minimum-overlap axis gives a "
   "sensible contact normal in a variety of configurations.",
   "Implement GJK with support functions for a box, a sphere, and a "
   "cylinder. Verify distances against analytic values where available.",
   "Demonstrate tunnelling: fire a small sphere at a thin wall at increasing "
   "speeds and find the speed at which it passes through.",
   "Implement speculative contacts and show that the same test no longer "
   "tunnels. Report the cost.",
   "Implement manifold generation for box&ndash;box contact. Show that a box "
   "rests stably with four contact points and rocks with one.",
   "Build the ten-box stack from Project 1 and measure how long it stands "
   "with and without manifold persistence.",
   "Implement cloth self-collision with both vertex&ndash;triangle and "
   "edge&ndash;edge tests. Remove the edge&ndash;edge test and demonstrate a "
   "configuration it misses.",
 ],
 "selfcheck": [
   "Why is an n&#178; broad phase infeasible, and what does the broad phase "
   "replace it with?",
   "Compare four broad-phase structures and say when each is appropriate.",
   "What is coherence, and name three ways a broad phase exploits it?",
   "State the separating axis theorem and say what SAT produces besides a "
   "yes/no answer.",
   "What does GJK need from a shape, and why does that make it general?",
   "Explain tunnelling and say why it is not a bug in the intersection "
   "test.",
   "Give four alternatives to full continuous collision detection.",
   "Why does a single contact point make a resting box rock, and what is a "
   "manifold?",
   "Give three things that make cloth self-collision harder than "
   "object-object collision.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Collision Response",
 "subtitle": "What to do once you know two things are touching.",
 "question": "How do you make a stack of boxes stand still?",
 "outcomes": [
     "Derive the collision impulse with restitution.",
     "Implement Coulomb friction and explain the friction cone.",
     "Explain why resting contact is harder than collision.",
     "Implement sequential impulses with warm starting.",
     "Diagnose jitter, sinking, and drift in a contact solver.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Impulses",
   "blurb": "An instantaneous change in velocity."},

  {"t": "eq", "kicker": "Impulse", "title": "The collision impulse",
   "eqs": [
     ("v_rel = (v_a − v_b) · n",
      "Relative velocity along the contact normal. Negative means "
      "approaching."),
     ("j = −(1 + e) v_rel / (1/mₐ + 1/m_b)",
      "The impulse magnitude. e is the coefficient of restitution: 0 is "
      "perfectly inelastic, 1 perfectly elastic."),
     ("v_a += j n / mₐ,    v_b −= j n / m_b",
      "Apply equal and opposite. Inverse mass again: static geometry has "
      "1/m = 0 and does not move."),
   ],
   "caption": "An impulse changes velocity instantaneously — no force, no "
              "time step. That is what makes collision different from every "
              "other interaction.",
   "note": "Emphasise that impulse is the right abstraction because the "
           "collision duration is below the time step."},

  {"t": "callout", "title": "Why impulses rather than forces",
   "kind": "The reason",
   "body": ["A real collision lasts microseconds and involves enormous "
            "forces. Resolving it with forces would need a time step far "
            "below anything affordable.",
            "<b>An impulse is the integral of force over that short "
            "interval</b>, applied all at once.",
            "<b>So the collision is treated as instantaneous</b> and the "
            "deformation during it is not modelled — restitution stands "
            "in for all of it.",
            "<b>That is why e has no deep physical meaning.</b> It is a "
            "lumped parameter summarising energy lost to deformation, sound, "
            "and heat in a process we declined to simulate."]},

  {"t": "section", "label": "Part 2", "title": "Friction",
   "blurb": "The tangential half, and the harder half."},

  {"t": "eq", "kicker": "Coulomb", "title": "The friction model",
   "eqs": [
     ("|f_t|  ≤  μ |f_n|",
      "Tangential force is bounded by the normal force times the friction "
      "coefficient. An inequality, not an equation."),
     ("Static:  f_t resists motion, up to the limit",
      "If the required force is within the cone, contact sticks."),
     ("Kinetic: |f_t| = μ |f_n| opposing slide",
      "If it exceeds the limit, contact slides and friction saturates."),
   ],
   "caption": "The inequality is what makes friction hard: whether a contact "
              "sticks or slides is an unknown you must solve for.",
   "note": "The stick/slide decision is coupled across contacts, which is "
           "why friction cannot be solved independently per contact."},

  {"t": "callout", "title": "The friction cone, and the pyramid everyone uses",
   "kind": "A standard approximation",
   "body": ["Admissible contact forces lie inside a <b>cone</b> about the "
            "normal, with half-angle arctan μ.",
            "<b>A cone constraint is nonlinear</b>, which complicates the "
            "solver considerably.",
            "<b>So almost everyone uses a pyramid</b> — a linear "
            "approximation with four or eight sides — which turns it "
            "into linear constraints the existing solver handles.",
            "<b>The artefact is anisotropic friction:</b> an object slides "
            "slightly more easily along the pyramid's edges than along its "
            "faces. It is visible if you look for it, and almost nobody "
            "does."]},

  {"t": "section", "label": "Part 3", "title": "Resting contact",
   "blurb": "The case that is genuinely difficult."},

  {"t": "callout", "title": "Resting contact is not a sequence of collisions",
   "kind": "Why stacks are hard",
   "body": ["A box on the ground is not colliding. It is <b>in contact</b>, "
            "with zero relative velocity, and the ground must supply exactly "
            "enough force to cancel gravity.",
            "<b>Treating it as repeated tiny collisions gives jitter</b>: "
            "gravity pulls it in, the impulse pushes it out, every frame.",
            "<b>And the forces are coupled.</b> In a stack, the force on the "
            "bottom box depends on everything above it. You cannot solve "
            "contacts independently.",
            "<b>Formally this is a linear complementarity problem</b> — "
            "either the contact is separating with zero force, or touching "
            "with non-negative force. Never both."]},

  {"t": "code", "kicker": "Sequential impulses", "title": "How engines actually solve it",
   "lang": "cpp", "code": """
// Erin Catto's method: Gauss-Seidel over contacts, with accumulated
// impulses. Simple, fast, and good enough -- it is what Box2D does.
for (int iter = 0; iter < iterations; iter++) {
    for (auto& c : contacts) {
        double vn = relative_normal_velocity(c);

        // Baumgarte: push apart gently, proportional to penetration.
        double bias = BETA / dt * max(0.0, c.penetration - SLOP);

        double dj = -(vn + bias) / c.effective_mass;

        // CLAMP THE ACCUMULATED impulse, not this iteration's increment.
        // Contacts may only push, never pull -- but an individual
        // iteration may need to reduce a previous over-correction.
        double old = c.normal_impulse;
        c.normal_impulse = max(0.0, old + dj);
        dj = c.normal_impulse - old;

        apply_impulse(c, dj * c.normal);
    }
}
""",
   "caption": "Clamping the accumulated impulse rather than the increment is "
              "the detail that makes this work. Clamping the increment gives "
              "a visibly worse solver.",
   "note": "This clamp is the single most important line. It appears in "
           "every production implementation and is easy to get wrong."},

  {"t": "table", "kicker": "Stabilisation", "title": "Removing penetration without popping",
   "header": ["Method", "Idea", "Problem"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Projection", "Move objects apart directly", "<b>Adds energy; pops</b>"],
     ["Baumgarte", "Bias velocity by penetration", "<b>Adds energy; springy</b>"],
     ["<b>Split impulse</b>", "Separate position and velocity passes", "<b>No added energy</b>"],
     ["Slop", "Allow a small permanent overlap", "<b>Essential for stability</b>"],
   ],
   "footnote": "Slop is not a hack — without it, contacts oscillate "
               "between active and inactive every frame.",
   "note": "Split impulse is the right answer and is what modern engines "
           "use. Baumgarte is simpler and springier."},

  {"t": "section", "label": "Part 4", "title": "Diagnosis",
   "blurb": "Reading the failure modes."},

  {"t": "table", "kicker": "Symptoms", "title": "Contact solver failures",
   "header": ["Symptom", "Cause"],
   "widths": [4.6, 7.5],
   "rows": [
     ["<b>Stack jitters</b>", "Too few iterations; no warm start; no slop"],
     ["<b>Objects sink in</b>", "Not enough iterations to resolve the stack"],
     ["Objects drift sideways", "Friction too weak, or pyramid artefact"],
     ["Boxes slide down slopes slowly", "Friction not solved with the normal"],
     ["<b>Stack explodes</b>", "<b>Baumgarte bias too large</b>"],
     ["Objects never settle", "No sleeping (Module 13)"],
   ],
   "note": "Jitter is nearly always warm starting. Sinking is nearly always "
           "iteration count."},

  {"t": "callout", "title": "Warm starting is what makes stacking work",
   "kind": "The single biggest lever",
   "body": ["In a stable stack, the contact forces this frame are almost "
            "identical to last frame's.",
            "<b>Starting each solve from zero throws that away</b> and "
            "re-derives the answer from scratch every frame, which with ten "
            "iterations it cannot do.",
            "<b>Store the accumulated impulse on each persistent contact "
            "point and apply it before solving.</b> The solver starts near "
            "the answer and converges in a few iterations.",
            "<b>This requires manifold persistence</b> (Module 05) — "
            "contacts must be matched by feature across frames. The two "
            "features together are what make a tall stack possible."]},

  {"t": "bullets", "kicker": "Practice", "title": "Getting contact to behave",
   "items": [
     "<b>Solve friction after the normal</b> in each iteration — the "
     "friction bound depends on the normal impulse just computed.",
     "",
     "<b>Use a slop</b> of a few millimetres. Contacts that oscillate "
     "between active and inactive destroy stability.",
     "",
     "<b>Shock propagation</b> for tall stacks: solve bottom-up, treating "
     "already-solved bodies as static. Converges far faster.",
     "",
     "<b>Substep.</b> Again. It helps here as much as anywhere.",
     "",
     "<b>Sleep resting objects</b> (Module 13). A settled stack should cost "
     "nothing.",
   ],
   "footnote": "Shock propagation is the trick that makes hundred-box "
               "stacks feasible."},
 ],
 "takeaways": [
   "A collision lasts microseconds, so it is resolved with an impulse "
   "— the integral of force — applied instantaneously.",
   "Restitution is a lumped parameter standing in for deformation, sound, "
   "and heat that were deliberately not simulated.",
   "Coulomb friction is an inequality: whether a contact sticks or slides is "
   "an unknown, coupled across contacts, that must be solved for.",
   "The friction cone is nonlinear, so engines use a pyramid; the artefact "
   "is slightly anisotropic friction that almost nobody notices.",
   "Resting contact is not repeated collision. Forces are coupled through "
   "the stack, making it a linear complementarity problem.",
   "Clamp the accumulated impulse, not the increment; warm start from "
   "persistent manifolds. Those two details make stacking work.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Impulses"),
  ("eq", "j = &minus;(1 + e) v<sub>rel</sub> / "
         "( 1/m<sub>a</sub> + 1/m<sub>b</sub> )"),
  ("p", "where v<sub>rel</sub> is the relative velocity along the contact "
        "normal and e is the coefficient of restitution: 0 for a perfectly "
        "inelastic collision, 1 for a perfectly elastic one. The impulse is "
        "applied equally and oppositely, divided by each body's mass "
        "— so static geometry, with inverse mass zero, does not move."),
  ("callout", "Why impulses rather than forces",
   ["A real collision between rigid objects lasts on the order of "
    "microseconds and involves forces of enormous magnitude. Resolving it "
    "with forces would require a time step several orders of magnitude below "
    "anything affordable, for every collision in the scene.",
    "<b>An impulse is the integral of force over that brief interval</b>, "
    "applied in a single instant. It changes velocity discontinuously, which "
    "is exactly what we observe at the scale we care about.",
    "<b>The consequence is that the deformation during the collision is not "
    "modelled at all.</b> Everything that happens during the contact "
    "— elastic compression, plastic deformation, energy radiated as "
    "sound, heat — is summarised by a single number.",
    "<b>That is why the coefficient of restitution has no deep physical "
    "meaning.</b> It is a lumped parameter standing in for a process we "
    "declined to simulate, which is why measured values depend on impact "
    "speed, temperature, and geometry in ways a single constant cannot "
    "capture."]),

  ("h1", "2 &nbsp; Friction"),
  ("eq", "|f<sub>t</sub>| &le; &mu; |f<sub>n</sub>|"),
  ("table", ["Regime", "Condition", "Behaviour"],
   [["<b>Static friction</b>",
     "The tangential force required to prevent sliding is within the bound.",
     "<b>The contact sticks.</b> Relative tangential velocity is zero and "
     "friction supplies whatever force is needed, up to the limit."],
    ["<b>Kinetic friction</b>",
     "The required force exceeds the bound.",
     "<b>The contact slides.</b> Friction saturates at &mu;|f<sub>n</sub>|, "
     "opposing the relative motion."]],
   [0.19, 0.37, 0.44]),
  ("p", "<b>The inequality is what makes friction difficult.</b> Whether a "
        "given contact sticks or slides is not known in advance — it is "
        "an unknown that must be solved for. And the decisions are coupled: "
        "whether one contact slides affects the forces at others, which "
        "affects whether they slide. Friction cannot be resolved one contact "
        "at a time in a single pass."),
  ("callout", "The friction cone and the pyramid everyone substitutes",
   ["The set of admissible contact forces — normal plus tangential "
    "— forms a <b>cone</b> about the contact normal, with half-angle "
    "arctan&nbsp;&mu;. Forces inside the cone are achievable; forces outside "
    "it are not, and the contact slides instead.",
    "<b>A cone is a nonlinear constraint</b>, which complicates the solver "
    "considerably: the tangential bound depends on the normal force, which "
    "is itself being solved for simultaneously.",
    "<b>So almost every engine approximates the cone with a pyramid</b> "
    "— four or eight flat sides — which reduces it to linear "
    "constraints the existing machinery already handles.",
    "<b>The artefact is slightly anisotropic friction.</b> An object slides "
    "a little more easily along the pyramid's edge directions than along its "
    "face normals, so a box pushed across a floor drifts imperceptibly "
    "toward the diagonal. It is visible if you set up an experiment to look "
    "for it, and essentially nobody does — which is a reasonable trade, "
    "and worth knowing about."]),

  ("break",),
  ("h1", "3 &nbsp; Resting contact"),
  ("callout", "Resting contact is a different problem from collision",
   ["A box sitting on the ground is not colliding. It is <b>in contact</b>, "
    "with zero relative normal velocity, and the ground must supply exactly "
    "enough upward force to cancel gravity — no more, which would "
    "launch it, and no less, which would let it sink.",
    "<b>Treating it as a sequence of tiny collisions produces jitter.</b> "
    "Gravity pulls the box in during the step; an impulse pushes it out; the "
    "next step repeats. The box vibrates, and in a stack the vibration "
    "compounds upward.",
    "<b>And the forces are coupled through the stack.</b> The force the "
    "ground exerts on the bottom box depends on the weight of every box "
    "above it, which depends on the forces between them. <b>You cannot solve "
    "the contacts independently</b> — the answer at one depends on the "
    "answer at all the others.",
    "<b>Formally this is a linear complementarity problem:</b> at each "
    "contact, either the bodies are separating and the contact force is "
    "zero, or they are touching and the force is non-negative. Never both, "
    "and which case applies is part of the unknown."]),
  ("code", """for (int iter = 0; iter < iterations; iter++)
  for (auto& c : contacts) {
    double vn   = relative_normal_velocity(c);
    double bias = BETA / dt * max(0.0, c.penetration - SLOP);
    double dj   = -(vn + bias) / c.effective_mass;

    double old = c.normal_impulse;                 // ACCUMULATED
    c.normal_impulse = max(0.0, old + dj);         // clamp the TOTAL
    dj = c.normal_impulse - old;                   // apply the difference
    apply_impulse(c, dj * c.normal);
  }"""),
  ("callout", "Clamp the accumulated impulse, not the increment",
   ["Contacts may push but never pull, so the total normal impulse at a "
    "contact must be non-negative. The naive implementation clamps each "
    "iteration's increment to be non-negative, which is subtly and "
    "importantly wrong.",
    "<b>An individual iteration may legitimately need to reduce a previous "
    "over-correction.</b> If an earlier iteration applied too large an "
    "impulse — because contacts solved later changed the "
    "situation — a later iteration must be able to subtract from it. "
    "Clamping the increment forbids that, and the solver cannot recover from "
    "its own overshoot.",
    "<b>Clamping the accumulated total instead</b> permits negative "
    "increments while keeping the total non-negative, which is the correct "
    "condition.",
    "<b>This is the single most important detail in the whole solver</b>, it "
    "appears in every production implementation, and the difference between "
    "the two versions is visible immediately in how well a stack converges."]),
  ("table", ["Stabilisation method", "Mechanism", "Problem"],
   [["<b>Direct projection</b>", "Move the bodies apart to remove "
     "penetration.", "<b>Adds energy</b>, and produces a visible pop."],
    ["<b>Baumgarte stabilisation</b>",
     "Add a velocity bias proportional to penetration depth, so the solver "
     "naturally separates them.",
     "<b>Adds energy</b> too, and behaves like a stiff spring — too "
     "large a coefficient makes stacks explode."],
    ["<b>Split impulse</b>",
     "Run two passes: one for velocity, one for position correction, with "
     "the positional pass not feeding back into velocity.",
     "<b>No energy added.</b> The correct answer, and what modern engines "
     "use."],
    ["<b>Slop</b>", "Permit a small permanent overlap — a few "
     "millimetres — before correcting.",
     "<b>Essential rather than a hack.</b> Without it, contacts oscillate "
     "between active and inactive every frame as the correction overshoots, "
     "and nothing settles."]],
   [0.20, 0.42, 0.38]),

  ("h1", "4 &nbsp; Diagnosis"),
  ("table", ["Symptom", "Most likely cause"],
   [["<b>A stack jitters continuously.</b>",
     "Too few solver iterations, <b>no warm starting</b>, or no slop. Warm "
     "starting is the usual answer."],
    ["<b>Objects sink into each other over time.</b>",
     "Insufficient iterations to propagate force through the stack; or "
     "position correction too weak."],
    ["Objects drift sideways while at rest.",
     "Friction too weak, or the pyramid approximation's anisotropy."],
    ["Boxes creep slowly down a slope they should rest on.",
     "Friction being solved without reference to the just-computed normal "
     "impulse. Solve the normal first, every iteration."],
    ["<b>The stack explodes.</b>",
     "<b>Baumgarte bias coefficient too large.</b> It acts as a stiff "
     "spring; reduce it or switch to split impulse."],
    ["Objects never come fully to rest.",
     "No sleeping. A settled object should be deactivated (Module 13)."]],
   [0.37, 0.63]),
  ("callout", "Warm starting is the single biggest lever",
   ["In a stack that is not moving, <b>the contact forces this frame are "
    "almost exactly the forces from last frame.</b> The answer barely "
    "changes.",
    "<b>Starting each solve from zero discards that information entirely</b> "
    "and asks the solver to re-derive the whole force distribution from "
    "scratch, every frame, in ten iterations. For a tall stack it cannot, so "
    "the stack sags and jitters.",
    "<b>Store the accumulated impulse on each persistent contact point and "
    "apply it before the iterations begin.</b> The solver then starts very "
    "close to the answer and converges in a few iterations.",
    "<b>This requires manifold persistence from Module 05</b> — "
    "contact points must be matched across frames by feature identity, not "
    "by position, so the stored impulse attaches to the right contact. The "
    "two mechanisms together are what make a tall, stable stack possible, "
    "and neither works without the other."]),
  ("ul", ["<b>Solve friction after the normal impulse in each "
          "iteration</b>, since the friction bound &mu;|f<sub>n</sub>| "
          "depends on the normal impulse just computed. Solving them in the "
          "other order, or in separate passes, gives noticeably worse "
          "friction.",
          "<b>Use a slop</b> of a few millimetres, scaled to the scene. See "
          "the table above.",
          "<b>Shock propagation for tall stacks:</b> solve contacts from the "
          "bottom upward, treating already-solved bodies as though they were "
          "static. Information propagates through the whole stack in one "
          "pass rather than one level per iteration. <b>This is the trick "
          "that makes hundred-box stacks feasible.</b>",
          "<b>Substep.</b> As in Modules 02 and 04, several small steps beat "
          "one large step with more iterations.",
          "<b>Sleep resting objects.</b> A stack that has settled should "
          "consume no time at all; Module 13 covers the hysteresis needed to "
          "do this without objects freezing mid-motion."]),
 ],
 "resources": [
   ("Erin Catto &mdash; Sequential Impulses and contact solver talks (GDC, "
    "free)",
    "https://box2d.org/publications/",
    "The method of &sect;3, from its author. The clearest explanation of "
    "accumulated impulse clamping and warm starting anywhere."),
   ("Baraff &mdash; Rigid Body Simulation II: Nonpenetration Constraints "
    "(free notes)",
    "https://graphics.pixar.com/tutorials/",
    "The LCP formulation of resting contact, derived properly. Heavier going "
    "than Catto and worth it."),
   ("Mirtich &mdash; Impulse-based Dynamic Simulation (thesis, free)",
    "https://people.eecs.berkeley.edu/~jfc/mirtich/",
    "The impulse formulation of &sect;1 in full, including the friction "
    "cone treatment."),
   ("Box2D source",
    "https://github.com/erincatto/box2d",
    "A production contact solver you can read in an afternoon. Compare your "
    "implementation against <code>b2ContactSolver</code>."),
 ],
 "exercises": [
   "Implement impulse-based collision response with restitution. Verify "
   "energy behaviour for e = 0, 0.5, and 1 — at e = 1 a bouncing ball "
   "must return to its original height.",
   "Implement Coulomb friction with a pyramid approximation. Place a box on "
   "an inclined plane and find the angle at which it begins to slide; "
   "compare against arctan&nbsp;&mu;.",
   "Demonstrate the pyramid artefact: push a box across a floor in many "
   "directions and plot the resulting trajectory deviation against "
   "direction.",
   "Implement sequential impulses. Then change the clamp from accumulated to "
   "incremental and document how much worse the solver becomes.",
   "Build a stack of ten boxes. Measure how long it stands with 4, 10, and "
   "30 iterations.",
   "Implement warm starting and repeat. Report the iteration count now "
   "needed for the same stability.",
   "Sweep the Baumgarte coefficient and find the value at which the stack "
   "becomes springy, and the value at which it explodes.",
   "Implement split impulse position correction and compare the energy "
   "behaviour against Baumgarte.",
   "Implement shock propagation and build a stack of a hundred boxes. Report "
   "iterations and time against the non-shock version.",
   "Produce the Project 1 deliverable: a ten-box stack standing for sixty "
   "seconds, with the energy plot showing it is genuinely at rest.",
 ],
 "selfcheck": [
   "Why are collisions resolved with impulses rather than forces?",
   "What does the coefficient of restitution actually represent, and why is "
   "it not a fundamental constant?",
   "Write the Coulomb friction condition and explain why the inequality "
   "makes it hard.",
   "What is the friction cone, why is it approximated by a pyramid, and what "
   "is the artefact?",
   "Why is resting contact not a sequence of collisions?",
   "Why can contacts in a stack not be solved independently?",
   "Why must the accumulated impulse be clamped rather than the increment?",
   "Compare four penetration stabilisation methods.",
   "What is warm starting, what does it require, and why does it matter so "
   "much?",
   "Give four contact solver symptoms and their likely causes.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Rigid Body Dynamics",
 "subtitle": "Rotation, which is where the interesting mistakes are.",
 "question": "Why does a tumbling object flip over on its own?",
 "outcomes": [
     "Write the rigid body state and its derivative.",
     "Compute and transform an inertia tensor.",
     "Explain why angular momentum, not angular velocity, is the state "
     "variable.",
     "Integrate orientation with quaternions and renormalise correctly.",
     "Explain and reproduce the intermediate axis theorem.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The state",
   "blurb": "Thirteen numbers, and one of them is a choice."},

  {"t": "table", "kicker": "State", "title": "What a rigid body is",
   "header": ["Quantity", "Symbol", "Size", "Note"],
   "widths": [3.3, 1.8, 1.6, 5.4],
   "rows": [
     ["Position", "x", "3", "Of the centre of mass"],
     ["Orientation", "q", "4", "<b>Quaternion</b>"],
     ["Linear momentum", "P", "3", "P = m v"],
     ["<b>Angular momentum</b>", "<b>L</b>", "3", "<b>Not angular velocity</b>"],
   ],
   "footnote": "Store momentum, not velocity. The reason is the whole of "
               "Part 3.",
   "note": "The momentum-not-velocity choice is the main technical content "
           "of the module."},

  {"t": "eq", "kicker": "Derivative", "title": "The equations of motion",
   "eqs": [
     ("ẋ = P/m,     Ṗ = F",
      "Linear motion. Exactly as for a particle."),
     ("q̇ = ½ ω q,   L̇ = τ",
      "Rotational. Torque changes angular momentum directly, just as force "
      "changes linear momentum."),
     ("ω = I⁻¹(t) L",
      "Angular velocity is DERIVED from angular momentum through the "
      "current inertia tensor. It is not a state variable."),
   ],
   "caption": "The third line is the module. Angular velocity changes even "
              "with no torque, because I changes as the body rotates.",
   "note": "Spend time here. The derived-not-stored distinction is what "
           "makes the tumbling behaviour emerge correctly."},

  {"t": "section", "label": "Part 2", "title": "Inertia",
   "blurb": "Mass for rotation, except it is a tensor."},

  {"t": "callout", "title": "The inertia tensor is direction-dependent mass",
   "kind": "What it is",
   "body": ["Linear mass is a scalar: resistance to acceleration is the same "
            "in every direction.",
            "<b>Rotational inertia is not.</b> A long rod spins easily about "
            "its axis and with difficulty about its middle.",
            "<b>So inertia is a 3×3 symmetric matrix</b>, and the "
            "relationship L = I ω means <b>angular momentum and angular "
            "velocity are generally not parallel</b>.",
            "<b>That non-parallelism is the source of every interesting "
            "rotational phenomenon</b> in this module, including the one in "
            "Part 4."]},

  {"t": "eq", "kicker": "Transforming", "title": "Inertia in world space",
   "eqs": [
     ("I_world(t)  =  R(t) I_body Rᵀ(t)",
      "The body-space tensor is constant; the world-space one changes as the "
      "body rotates."),
     ("I⁻¹_world  =  R I⁻¹_body Rᵀ",
      "Store and transform the INVERSE. You need I⁻¹ every step and never "
      "need I itself."),
   ],
   "caption": "Precompute and diagonalise I_body once at load; recompute "
              "I⁻¹_world each step from the current rotation.",
   "note": "Diagonalising gives the principal axes, which also makes the "
           "Part 4 demonstration easy to set up."},

  {"t": "bullets", "kicker": "Computing", "title": "Getting the tensor right",
   "items": [
     "<b>From a mesh:</b> integrate over the volume, not the surface. "
     "Mirtich's method does it exactly from the boundary.",
     "",
     "<b>About the centre of mass</b>, always. Compute the centre first and "
     "translate the body so it sits at the origin.",
     "",
     "<b>Diagonalise it</b> at load time: the eigenvectors are the principal "
     "axes, the eigenvalues the principal moments.",
     "",
     "<b>Parallel axis theorem</b> for compound bodies: I about any point is "
     "I about the centre plus m d².",
     "",
     "<b>Sanity check against known shapes.</b> A solid sphere is "
     "(2/5)mr²; get that right before trusting a mesh.",
   ],
   "footnote": "An incorrect inertia tensor produces motion that looks "
               "wrong without any obvious error — verify it directly."},

  {"t": "section", "label": "Part 3", "title": "Orientation",
   "blurb": "Why quaternions, and how to integrate them."},

  {"t": "table", "kicker": "Representations", "title": "Three ways to store orientation",
   "header": ["Form", "Size", "Problem"],
   "widths": [3.0, 1.8, 7.3],
   "rows": [
     ["Euler angles", "3", "<b>Gimbal lock; order-dependent; bad to interpolate</b>"],
     ["Rotation matrix", "9", "Drifts from orthonormal; re-orthonormalising is awkward"],
     ["<b>Quaternion</b>", "<b>4</b>", "<b>Renormalise each step. Otherwise ideal</b>"],
   ],
   "footnote": "A quaternion carries one redundant number against three "
               "degrees of freedom; a matrix carries six.",
   "note": "The redundancy argument is the clean way to explain why "
           "quaternions drift less badly than matrices."},

  {"t": "code", "kicker": "Integration", "title": "Advancing orientation",
   "lang": "cpp", "code": """
void RigidBody::step(double dt) {
    // Linear part: exactly as for a particle.
    P += force * dt;
    x += (P / mass) * dt;

    // Rotational part.
    L += torque * dt;                       // torque changes MOMENTUM
    mat3 R      = q.to_matrix();
    mat3 Iinv_w = R * Iinv_body * R.transpose();   // recompute each step
    vec3 omega  = Iinv_w * L;               // DERIVE angular velocity

    // Quaternion derivative: q' = 0.5 * omega_quat * q
    quat omega_q(0, omega.x, omega.y, omega.z);
    q = q + (0.5 * dt) * (omega_q * q);
    q.normalize();                          // <-- REQUIRED, every step
}
""",
   "caption": "Three details: torque changes L not ω; I⁻¹ is recomputed from "
              "the current R; and the quaternion must be renormalised.",
   "note": "Forgetting the normalise is the classic bug — the body "
           "gradually scales and then degenerates."},

  {"t": "section", "label": "Part 4", "title": "The tumbling T-handle",
   "blurb": "The test that proves your rotational dynamics is correct."},

  {"t": "callout", "title": "The intermediate axis theorem",
   "kind": "The Dzhanibekov effect",
   "body": ["A rigid body with three <i>distinct</i> principal moments "
            "spins stably about the axes of largest and smallest moment.",
            "<b>Rotation about the intermediate axis is unstable.</b> A body "
            "spun about it flips over periodically, with no torque and no "
            "external influence whatsoever.",
            "<b>Angular momentum is conserved throughout.</b> Nothing is "
            "driving it; the flip is a consequence of the constant-L "
            "constraint and the geometry of the inertia ellipsoid.",
            "<b>If your simulator reproduces this, your rotational dynamics "
            "is correct.</b> If it does not, you are almost certainly "
            "storing angular velocity instead of angular momentum."]},

  {"t": "callout", "title": "Why storing angular velocity breaks it",
   "kind": "The diagnostic",
   "body": ["With no torque, <b>angular momentum L is constant</b> — but "
            "<b>angular velocity ω is not</b>, because ω = I⁻¹(t)L and I "
            "changes as the body rotates.",
            "<b>Store L</b> and ω comes out correctly every step for free, "
            "and the flip emerges.",
            "<b>Store ω</b> and you must add the gyroscopic term ω × (Iω) "
            "by hand — and it is easy to omit, numerically awkward, and "
            "frequently dropped.",
            "<b>So storing momentum is not a preference.</b> It is what "
            "makes the correct behaviour fall out instead of having to be "
            "added."]},

  {"t": "bullets", "kicker": "Contact", "title": "Rigid bodies with collision",
   "items": [
     "<b>Impulses apply at a point</b>, so they change angular momentum: "
     "ΔL = r × j, where r is from the centre of mass.",
     "",
     "<b>Effective mass is direction-dependent</b> now: it depends on where "
     "on the body the contact is and about which axis it would rotate.",
     "",
     "<b>Rolling without slipping</b> is a constraint, not an emergent "
     "behaviour. Friction alone gives rolling with some slip.",
     "",
     "<b>Spinning friction</b> — resistance to rotation about the "
     "contact normal — is separate and usually ignored, which is why "
     "spinning objects never slow down.",
   ],
   "footnote": "Module 06's machinery carries over; the only change is that "
               "r × j now matters."},
 ],
 "takeaways": [
   "A rigid body is position, quaternion orientation, linear momentum, and "
   "<b>angular momentum</b> — thirteen numbers.",
   "Torque changes angular momentum directly. Angular velocity is derived "
   "each step as &omega; = I&#8315;&#185;(t)L, not stored.",
   "The inertia tensor is direction-dependent mass, so L and &omega; are "
   "generally not parallel — which causes every interesting rotational "
   "effect.",
   "Transform the inverse tensor: I&#8315;&#185;_world = R I&#8315;&#185;_body "
   "R&#7488;, recomputed every step.",
   "Use quaternions and renormalise every step; Euler angles gimbal-lock and "
   "matrices drift off orthonormal.",
   "The intermediate axis theorem is the test: a body spun about its middle "
   "axis flips periodically with angular momentum conserved throughout.",
 ],
 "notes": [
  ("h1", "1 &nbsp; State and equations of motion"),
  ("table", ["Quantity", "Symbol", "Components", "Note"],
   [["Position of the centre of mass", "<b>x</b>", "3", "—"],
    ["Orientation", "q", "4", "<b>A unit quaternion.</b> &sect;3."],
    ["Linear momentum", "<b>P</b>", "3", "<b>P</b> = m<b>v</b>."],
    ["<b>Angular momentum</b>", "<b>L</b>", "3",
     "<b>Not angular velocity.</b> This choice is the main content of the "
     "module."]],
   [0.34, 0.12, 0.14, 0.40]),
  ("eq", "<b>x</b>&#775; = <b>P</b>/m, &nbsp;&nbsp; "
         "<b>P</b>&#775; = <b>F</b> &nbsp;&nbsp;&nbsp;&nbsp; "
         "q&#775; = &frac12; &omega; q, &nbsp;&nbsp; "
         "<b>L</b>&#775; = &tau;"),
  ("eq", "&omega; = I<super>&minus;1</super>(t) <b>L</b>"),
  ("p", "The linear equations are exactly a particle's. The rotational ones "
        "mirror them: <b>torque changes angular momentum</b> just as force "
        "changes linear momentum. <b>Angular velocity is derived</b> from "
        "angular momentum through the current inertia tensor, and is not "
        "part of the state."),
  ("p", "<b>This is the line that matters.</b> With no torque, <b>L</b> is "
        "constant — but &omega; is not, because I depends on the body's "
        "current orientation and therefore changes as it rotates. A body "
        "under no torque at all can have a continuously changing angular "
        "velocity, which is the source of &sect;4's behaviour."),

  ("h1", "2 &nbsp; The inertia tensor"),
  ("callout", "Direction-dependent mass",
   ["Linear mass is a scalar: a body resists acceleration equally in every "
    "direction, so F = m<b>a</b> with m a single number.",
    "<b>Rotational inertia is not a scalar.</b> A long rod is easy to spin "
    "about its own axis and hard to spin end over end. The resistance "
    "depends on the axis.",
    "<b>So inertia is a 3&times;3 symmetric matrix</b>, and L = I&omega; is "
    "a matrix equation. <b>The consequence is that angular momentum and "
    "angular velocity are generally not parallel</b> — a body can be "
    "spinning about one axis while its angular momentum points along "
    "another.",
    "<b>That non-parallelism is the origin of every interesting rotational "
    "phenomenon</b> in rigid body dynamics: precession, nutation, "
    "gyroscopic resistance, and the intermediate axis instability of "
    "&sect;4."]),
  ("eq", "I<sub>world</sub>(t) = R(t) I<sub>body</sub> "
         "R<super>T</super>(t) &nbsp;&nbsp;&nbsp;&nbsp; "
         "I<super>&minus;1</super><sub>world</sub> = R "
         "I<super>&minus;1</super><sub>body</sub> R<super>T</super>"),
  ("p", "The body-space tensor is a constant property of the shape and mass "
        "distribution. The world-space tensor changes continuously as the "
        "body rotates, and must be recomputed each step. <b>Store and "
        "transform the inverse</b>: every step needs "
        "I<super>&minus;1</super> to obtain &omega; from <b>L</b>, and "
        "nothing ever needs I itself."),
  ("ul", ["<b>Compute it from the volume, not the surface.</b> Integrating "
          "over the triangles of a mesh gives the inertia of a hollow shell, "
          "not a solid body. Mirtich's algorithm computes the volume "
          "integral exactly from the boundary representation and is the "
          "standard method.",
          "<b>Always about the centre of mass.</b> Compute the centre of "
          "mass first and translate the body so it lies at the origin, "
          "otherwise every equation in &sect;1 is wrong.",
          "<b>Diagonalise at load time.</b> The eigenvectors of I are the "
          "<b>principal axes</b> and the eigenvalues the <b>principal "
          "moments</b>. Rotating the body into this frame makes I diagonal, "
          "which simplifies everything and is how you set up &sect;4's "
          "demonstration.",
          "<b>Parallel axis theorem</b> for compound bodies: the inertia "
          "about any point equals the inertia about the centre of mass plus "
          "m d&#178; terms. This is how you assemble a body from parts.",
          "<b>Verify against known shapes.</b> A solid sphere is "
          "(2/5)mr&#178; about any axis; a solid box is "
          "(m/12)(h&#178;+d&#178;) about each principal axis. <b>An "
          "incorrect inertia tensor produces motion that looks subtly wrong "
          "with no identifiable error</b>, so check it directly rather than "
          "by eye."]),

  ("break",),
  ("h1", "3 &nbsp; Orientation"),
  ("table", ["Representation", "Numbers", "Problems"],
   [["<b>Euler angles</b>", "3",
     "<b>Gimbal lock</b> — a degree of freedom is lost at certain "
     "orientations. The result depends on the order of the three rotations, "
     "and interpolation between two sets of angles does not follow a "
     "sensible path."],
    ["<b>Rotation matrix</b>", "9",
     "Numerical integration drifts away from orthonormality, so the body "
     "gradually shears and scales. Re-orthonormalising is possible "
     "(Gram&ndash;Schmidt) and awkward, and six redundant numbers is a lot "
     "of drift to control."],
    ["<b>Quaternion</b>", "<b>4</b>",
     "<b>Must be renormalised every step.</b> That is the entire "
     "disadvantage. One redundant number against three degrees of freedom, "
     "no singularities, and clean interpolation."]],
   [0.17, 0.10, 0.73]),
  ("code", """void RigidBody::step(double dt) {
    P += force * dt;
    x += (P / mass) * dt;

    L += torque * dt;                              // torque -> MOMENTUM
    mat3 R      = q.to_matrix();
    mat3 Iinv_w = R * Iinv_body * R.transpose();   // recompute from R
    vec3 omega  = Iinv_w * L;                      // DERIVE omega

    quat omega_q(0, omega.x, omega.y, omega.z);
    q = q + (0.5 * dt) * (omega_q * q);
    q.normalize();                                 // required
}"""),
  ("p", "Three details to get right: torque integrates into <b>L</b> and not "
        "into &omega;; the inverse inertia tensor is recomputed from the "
        "current rotation every step; and the quaternion is renormalised "
        "every step. <b>Omitting the normalisation is the classic bug</b> "
        "— the quaternion's magnitude drifts from 1, which the "
        "to-matrix conversion interprets as a uniform scale, and the body "
        "slowly grows or shrinks before degenerating entirely."),

  ("h1", "4 &nbsp; The intermediate axis theorem"),
  ("callout", "The Dzhanibekov effect",
   ["A rigid body with three <i>distinct</i> principal moments of inertia "
    "— a T-handle, a tennis racket, a phone — spins stably about "
    "the axis of largest moment and about the axis of smallest moment.",
    "<b>Rotation about the intermediate axis is unstable.</b> A body set "
    "spinning about it will flip end over end, periodically, indefinitely, "
    "<b>with no torque acting and nothing driving it</b>. The cosmonaut "
    "Vladimir Dzhanibekov famously filmed this with a wingnut in orbit.",
    "<b>Angular momentum is exactly conserved throughout the flip.</b> "
    "Nothing is being added or removed. The motion is a consequence of the "
    "constraint that both <b>L</b> and the rotational kinetic energy are "
    "conserved, which confines &omega; to the intersection of two "
    "ellipsoids — and near the intermediate axis that intersection is a "
    "path that travels right round the body.",
    "<b>If your simulator reproduces this spontaneously, your rotational "
    "dynamics is correct.</b> It is a far better test than watching things "
    "fall over, because nothing about the implementation hints at it — "
    "the behaviour has to emerge."]),
  ("callout", "Storing angular velocity is what breaks it",
   ["With no torque, <b>L</b> is constant. &omega; is <i>not</i>, because "
    "&omega; = I<super>&minus;1</super>(t)<b>L</b> and I changes as the body "
    "rotates.",
    "<b>Store L</b>, recompute I<super>&minus;1</super> each step, and "
    "&omega; comes out correctly for free. The flip emerges from the "
    "equations without anything having been added.",
    "<b>Store &omega;</b> and the equation of motion acquires an extra "
    "<b>gyroscopic term</b>, &omega; &times; (I&omega;), which must be added "
    "explicitly. It is easy to omit, numerically awkward — it can "
    "destabilise an explicit integrator — and is frequently dropped "
    "from implementations for exactly that reason.",
    "<b>So storing momentum rather than velocity is not a stylistic "
    "preference.</b> It is the difference between the correct behaviour "
    "falling out of the formulation and having to be bolted on. This is why "
    "Baraff's notes insist on it, and why Project 1 asks for the "
    "Dzhanibekov effect as a deliverable."]),
  ("h1", "5 &nbsp; Rigid bodies in contact"),
  ("ul", ["<b>An impulse applied at a point changes angular momentum:</b> "
          "&Delta;<b>L</b> = <b>r</b> &times; <b>j</b>, where <b>r</b> is "
          "the vector from the centre of mass to the contact point. All of "
          "Module 06 carries over; this term is the only addition.",
          "<b>Effective mass is now direction- and position-dependent.</b> "
          "The denominator in the impulse formula gains terms involving "
          "I<super>&minus;1</super> and <b>r</b>, so the same collision at "
          "the corner of a box and at the centre of its face produce "
          "different results — correctly.",
          "<b>Rolling without slipping is a constraint, not an emergent "
          "behaviour.</b> Friction alone produces rolling with some slip, "
          "which is often acceptable; true rolling contact requires an "
          "explicit constraint tying the contact point's velocity to zero.",
          "<b>Spinning friction</b> — resistance to rotation about the "
          "contact normal — is a separate effect and is usually "
          "omitted, which is why a spinning top or coin in most simulators "
          "never slows down on its own. Adding it requires a torsional "
          "friction constraint at each contact."]),
 ],
 "resources": [
   ("Baraff &mdash; Rigid Body Simulation I and II (free notes)",
    "https://graphics.pixar.com/tutorials/",
    "Sections D and G of the course pack. The state formulation of &sect;1, "
    "the inertia tensor, and the argument for storing momentum. The primary "
    "reading."),
   ("Mirtich &mdash; Fast and Accurate Computation of Polyhedral Mass "
    "Properties (free)",
    "https://people.eecs.berkeley.edu/~jfc/mirtich/",
    "The exact volume-integral method of &sect;2 for computing inertia from "
    "a mesh. Complete code in the paper."),
   ("Dzhanibekov effect &mdash; NASA ISS footage",
    "https://www.youtube.com/watch?v=1n-HMSCDYtM",
    "The physical phenomenon of &sect;4, filmed in orbit. Watch it before "
    "implementing, then match it."),
   ("Erin Catto &mdash; Numerical Methods and rigid body GDC talks (free)",
    "https://box2d.org/publications/",
    "The practical side: quaternion integration, renormalisation, and what "
    "goes wrong in production."),
 ],
 "exercises": [
   "Implement rigid body state and integration with quaternions. Verify "
   "that a body with no torque conserves angular momentum to "
   "floating-point tolerance over 100,000 steps.",
   "Omit the quaternion renormalisation and plot the quaternion's magnitude "
   "over time. Report how long until the body visibly degenerates.",
   "Compute the inertia tensor for a solid box and a solid sphere "
   "analytically and from your mesh code. They must agree.",
   "Diagonalise the inertia tensor of an irregular mesh and visualise the "
   "principal axes. Confirm they are sensible.",
   "<b>Reproduce the Dzhanibekov effect:</b> a body with three distinct "
   "principal moments, given a small perturbation from pure intermediate "
   "axis rotation. Plot angular momentum magnitude to confirm it is "
   "conserved through the flips.",
   "Deliberately store angular velocity instead of angular momentum, without "
   "the gyroscopic term, and show that the flip does not occur.",
   "Add the gyroscopic term to the angular velocity formulation and show the "
   "flip returns. Then compare its stability against the momentum "
   "formulation at large time steps.",
   "Extend Module 06's collision response to rigid bodies with the "
   "<b>r</b> &times; <b>j</b> term. Verify that an off-centre impact imparts "
   "spin.",
   "Build the Project 1 stack of ten boxes using full rigid body dynamics, "
   "and keep it standing for sixty seconds.",
   "Implement a rolling constraint and compare against friction-only "
   "rolling. Measure the slip in each case.",
 ],
 "selfcheck": [
   "List the four components of rigid body state and their sizes.",
   "Write the four equations of motion and say which quantity is derived "
   "rather than stored.",
   "What is the inertia tensor, and why does it mean L and &omega; are not "
   "parallel?",
   "How is the inertia tensor transformed to world space, and why store the "
   "inverse?",
   "Give three rules for computing an inertia tensor correctly.",
   "Compare three orientation representations and give the problem with "
   "each.",
   "What happens if a quaternion is not renormalised each step?",
   "State the intermediate axis theorem and say what is conserved during the "
   "flip.",
   "Why does storing angular velocity instead of momentum break the flip, "
   "and what would have to be added?",
   "How does collision response change for rigid bodies?",
 ],
},

]
