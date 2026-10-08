# -*- coding: utf-8 -*-
"""CSCE 649 Physically-Based Modeling — original course content."""

COURSE = {
    "code": "CSCE 649",
    "title": "Physically-Based Modeling",
    "tagline": "Particles, rigid bodies, deformables, constraints, and "
               "fluids — simulated well enough to ship",
    "term": "Semester 3 (with CSCE 647 and CSCE 608)",
    "prereqs": "CSCE 641 Computer Graphics; calculus and linear algebra; "
               "ordinary differential equations helpful but developed here "
               "as needed",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A simulation library: particles, constraints, collision "
                   "detection and response, rigid bodies, cloth, and a "
                   "fluid solver — written by you, with energy and "
                   "momentum behaviour measured rather than assumed",
    "description": [
        "CSCE 647 computed where light goes. This course computes where "
        "<i>everything else</i> goes. The subject is the numerical "
        "simulation of physical systems at the fidelity graphics needs, "
        "which is a specific and interesting standard: <b>plausible, "
        "stable, controllable, and fast</b> — in that order, and "
        "explicitly not 'accurate'.",
        "That ordering is the thing to understand early. An engineering "
        "simulation that is 2% wrong may be useless. A film simulation that "
        "is 2% wrong is fine, and one that is perfectly accurate but "
        "explodes on frame 180, or cannot be art-directed, is useless. "
        "Several of the most important techniques in this course are "
        "<i>provably less accurate</i> than the alternatives and are used "
        "anyway, for reasons the course will make precise.",
        "Everything here reduces to one structure: a state vector, a "
        "function that gives its derivative, and a scheme for advancing it "
        "in time. Particles, cloth, rigid bodies, and fluids differ in what "
        "is in the state vector and how the derivative is computed, and "
        "almost nothing else. <b>Once you see that, the field stops being a "
        "collection of unrelated tricks.</b>",
        "You will write all of it. By the end you will have a simulator you "
        "can reason about when it misbehaves — which it will, because "
        "every simulator does, and knowing whether you are looking at a "
        "stability problem, a constraint problem, or a collision problem is "
        "the skill this course exists to build.",
    ],
    "outcomes": [
        "Express any physical system as a state vector and a derivative "
        "function.",
        "Choose an integrator from the stability and energy behaviour a "
        "system requires.",
        "Explain stiffness and why it forces implicit integration.",
        "Implement constraints by projection and by Lagrange multipliers, "
        "and say when each is appropriate.",
        "Build a collision pipeline with correct broad and narrow phases.",
        "Compute collision response with restitution and Coulomb friction, "
        "including resting contact.",
        "Simulate rigid bodies with correct rotational dynamics.",
        "Implement a deformable solid and explain why mass-spring models "
        "fail.",
        "Implement both a grid-based and a particle-based fluid solver.",
        "Diagnose an unstable simulation and name the mechanism.",
    ],
    "materials": [
        ("Baraff & Witkin — Physically Based Modeling (SIGGRAPH course "
         "notes, free)",
         "https://graphics.pixar.com/tutorials/",
         "The primary text. Differential equation basics, particle systems, "
         "constraints, rigid bodies, and collision — written with unusual "
         "clarity and still the best free introduction to the field."),
        ("Matthias Müller — Ten Minute Physics (free video and code)",
         "https://matthias-research.github.io/pages/tenMinutePhysics/",
         "Short, complete, working implementations of almost every technique "
         "in this course, with the derivations. Watch the relevant episode "
         "before each module."),
        ("Bridson — Fluid Simulation for Computer Graphics (course notes, "
         "free)",
         "https://www.cs.ubc.ca/~rbridson/fluidsimulation/",
         "The standard reference for Modules 11 and 12. The full book is "
         "worth owning; the free course notes cover the essentials."),
        ("Erin Catto — GDC talks and Box2D (free)",
         "https://box2d.org/publications/",
         "How constraint solvers are built in practice, from the author of "
         "Box2D. The sequential impulse material is the clearest explanation "
         "of Module 06 that exists."),
        ("Bargteil & Shinar — An Introduction to Physics-Based Animation "
         "(SIGGRAPH course, free)",
         "https://dl.acm.org/doi/10.1145/3214834.3214849",
         "A modern survey tying the whole field together. Good second voice "
         "throughout, and strong on deformables."),
        ("Müller et al. — Position Based Dynamics papers (free)",
         "https://matthias-research.github.io/pages/publications/publications.html",
         "PBD and XPBD, from their authors. The primary sources for "
         "Module 04."),
    ],
    "tooling": [
        "<b>C++17</b> with <b>Eigen</b>. You will be solving sparse linear "
        "systems from Module 10 onward, and the performance matters once "
        "particle counts rise.",
        "<b>No physics engine.</b> Integration, constraints, collision, and "
        "solvers are the course. You may use a linear algebra library.",
        "<b>A real-time viewer</b> — Polyscope or a minimal OpenGL "
        "harness. You cannot debug a simulation you cannot watch, and "
        "stepping frame by frame is essential.",
        "<b>Plotting</b>: Python and matplotlib, or equivalent. <b>Energy "
        "and momentum plots are the primary diagnostic in this course</b> "
        "and you will make hundreds of them.",
        "<b>Bullet or Box2D installed as a reference</b>, not a dependency. "
        "When your stack of boxes jitters and theirs does not, the "
        "difference is informative.",
        "<b>A portfolio repository</b> with a video for every system, plus "
        "the energy plot that shows it is behaving.",
    ],
    "projects": [
        {"title": "Particles, constraints, and contact", "after": 7,
         "brief": "The core simulator. Rigid bodies and everything after "
                  "build on this machinery, so the integrator, the "
                  "constraint solver, and the contact handling all have to "
                  "be right rather than merely stable-looking.",
         "reqs": [
             "A generic integrator interface with explicit Euler, symplectic "
             "Euler, velocity Verlet, and RK4 behind it, selectable at "
             "runtime.",
             "A particle system with gravity, drag, and damped springs.",
             "A mass-spring cloth with structural, shear, and bending "
             "springs.",
             "Broad-phase collision detection with a spatial hash or sweep "
             "and prune, with the pair count reported.",
             "Impulse-based collision response with restitution and Coulomb "
             "friction.",
             "Rigid body dynamics with a correct inertia tensor and "
             "quaternion orientation.",
         ],
         "done": [
             "<b>An energy plot for an undamped orbiting particle under each "
             "integrator, over 10,000 steps.</b> Explicit Euler must gain "
             "energy, symplectic Euler must oscillate around a constant, "
             "RK4 must slowly lose it. Explain each curve.",
             "A cloth dropped onto a sphere, draping and coming to rest "
             "without jitter, with the resting energy reported.",
             "<b>A stack of ten boxes that remains standing for sixty "
             "seconds.</b> This is harder than it sounds and is the real "
             "test of the contact solver.",
             "<b>The Dzhanibekov effect reproduced:</b> a freely tumbling "
             "rigid body with three distinct principal moments flipping "
             "periodically. Angular momentum must be conserved to "
             "floating-point tolerance — report the drift.",
         ]},
        {"title": "Deformables or fluids", "after": 12,
         "brief": "Take one of the two hard systems to a standard you would "
                  "be willing to put in a reel, and measure it rather than "
                  "trusting it.",
         "reqs": [
             "<b>Either:</b> a corotational FEM deformable solid with "
             "collision handling and an implicit solver; <b>or</b> a fluid "
             "solver — Eulerian with pressure projection, or SPH/PBF, or "
             "FLIP.",
             "An implicit or semi-implicit time integration scheme, with the "
             "linear solve explained.",
             "Self-collision handling, or free-surface handling for a fluid.",
             "A demonstration that the solver converges, with iteration "
             "count against residual plotted.",
             "Parameters exposed in physically meaningful units.",
         ],
         "done": [
             "A video of the system under at least three qualitatively "
             "different conditions.",
             "<b>A volume-loss plot for a fluid, or an energy plot for a "
             "deformable</b>, with an honest account of what is lost and "
             "where.",
             "A stability study: the largest time step at which the system "
             "survives, for each integration scheme you implemented.",
             "<b>A documented failure.</b> Find the configuration that "
             "breaks your simulator, show it, and explain the mechanism. "
             "Every simulator has one; not knowing yours is the problem.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Simulation as an Initial Value Problem",
 "subtitle": "One structure underneath everything in this course.",
 "question": "What is a simulator actually doing?",
 "outcomes": [
     "Express a physical system as a state vector and a derivative "
     "function.",
     "Reduce a second-order ODE to a first-order system.",
     "Explain what 'physically based' means and what standard graphics "
     "holds it to.",
     "Identify which quantities a simulation should conserve.",
     "Set up the measurement harness used for the rest of the course.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The structure",
   "blurb": "State, derivative, step. That is all of it."},

  {"t": "eq", "kicker": "The form", "title": "Every simulation in this course",
   "eqs": [
     ("x' = f(x, t)",
      "A state vector x, and a function giving its rate of change. That is "
      "the entire abstraction."),
     ("x(t₀) = x₀",
      "Plus an initial condition. Together: an initial value problem."),
     ("x(t + Δt) ≈ step(x, f, Δt)",
      "A simulator is a loop that applies a stepping scheme repeatedly. "
      "Module 02 is about choosing it."),
   ],
   "caption": "Particles, cloth, rigid bodies, and fluids differ in what is "
              "in x and how f is computed. The loop is identical.",
   "note": "Return to this slide at the start of every module. It is the "
           "spine of the course."},

  {"t": "callout", "title": "Second order becomes first order by stacking",
   "kind": "The one trick you need",
   "body": ["Newton gives <b>a = F/m</b>, which is second order: "
            "x″ = F(x, x′)/m. Integrators are written for first-order "
            "systems.",
            "<b>Stack position and velocity into one state vector.</b> Then "
            "the derivative of position is velocity, and the derivative of "
            "velocity is force over mass.",
            "<b>x = [p, v]</b> &nbsp;⟹&nbsp; <b>x′ = [v, F(p,v)/m]</b>",
            "Now a general-purpose integrator applies. <b>Do this once, in "
            "the architecture</b>, and every system in the course fits the "
            "same interface."]},

  {"t": "code", "kicker": "Architecture", "title": "The interface worth building first",
   "lang": "cpp", "code": """
// Everything in this course implements this. Get it right once.
struct System {
    virtual int    dim() const = 0;              // size of the state vector
    virtual void   get_state(double* x) const = 0;
    virtual void   set_state(const double* x) = 0;
    virtual void   derivative(const double* x, double t, double* dx) = 0;
};

// And integrators take a System, not a particle or a body.
struct Integrator {
    virtual void step(System& s, double t, double dt) = 0;
};

// Consequence: you implement RK4 ONCE and it works for particles,
// cloth, rigid bodies, and fluids. Swapping integrators to compare
// them -- which this course does constantly -- becomes one line.
""",
   "caption": "The separation of state from derivative from stepping scheme "
              "is the whole architecture. Everything else is details.",
   "note": "Students usually hard-code Euler into a particle class and then "
           "cannot compare integrators. Insist on this early."},

  {"t": "section", "label": "Part 2", "title": "What 'physically based' means",
   "blurb": "A lower standard than it sounds, deliberately."},

  {"t": "table", "kicker": "Standards", "title": "Three fields, three requirements",
   "header": ["Field", "Requires", "Will accept"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["Engineering", "<b>Accuracy</b>, with error bounds", "Hours per solve"],
     ["Science", "<b>Validity</b> against experiment", "Supercomputers"],
     ["<b>Graphics</b>", "<b>Plausibility, stability, control, speed</b>",
      "<b>Being wrong, if it looks right</b>"],
   ],
   "footnote": "Not a lower standard so much as a different one: a "
               "graphics simulator must never explode and must be "
               "art-directable.",
   "note": "Set this up carefully. Several later techniques only make sense "
           "against this objective."},

  {"t": "callout", "title": "Stability outranks accuracy here",
   "kind": "The ordering that matters",
   "body": ["A simulation that is 5% wrong and runs for ten thousand frames "
            "is <b>useful</b>.",
            "A simulation that is exact and explodes on frame 180 is "
            "<b>worthless</b>, no matter how good the first 179 frames "
            "were.",
            "<b>So we will repeatedly accept provably less accurate methods "
            "for better stability.</b> Position-based dynamics (Module 04) "
            "is the extreme case — it is barely a physical method, and "
            "it is in every game engine.",
            "<b>Know that you are making the trade.</b> The failure mode of "
            "this field is making it without noticing, and then being unable "
            "to explain why the simulation does not match reality."]},

  {"t": "callout", "title": "Art direction is a hard requirement, not a compromise",
   "kind": "The constraint nobody mentions",
   "body": ["A director will ask for the explosion to be bigger, the cloth "
            "to settle sooner, and the splash to go left.",
            "<b>Physics does not have a 'go left' parameter.</b> A simulator "
            "that cannot be steered will not be used, however correct it "
            "is.",
            "So production methods expose controls that are not physical: "
            "damping multipliers, gravity per-object, stiffness that varies "
            "in space, forces that only act on frames 40–60.",
            "<b>Design for this from the start.</b> Hard-coding real "
            "constants into the solver is how you build something nobody can "
            "use."]},

  {"t": "section", "label": "Part 3", "title": "Measurement",
   "blurb": "What to watch, and why plotting it matters."},

  {"t": "table", "kicker": "Invariants", "title": "What a correct simulation conserves",
   "header": ["Quantity", "Conserved when", "If it drifts"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Linear momentum", "No external force", "<b>Forces are not equal and opposite</b>"],
     ["Angular momentum", "No external torque", "<b>Torque applied at the wrong point</b>"],
     ["<b>Energy</b>", "No damping or dissipation", "<b>The integrator (Module 02)</b>"],
     ["Volume", "Incompressible material", "A fluid or soft body leaking"],
   ],
   "footnote": "<b>Plot all of these.</b> They are the single most useful "
               "diagnostic in the course.",
   "note": "Energy drift is almost always the integrator; momentum drift is "
           "almost always a bug in force application."},

  {"t": "callout", "title": "Energy drift tells you which integrator you have",
   "kind": "The diagnostic that identifies everything",
   "body": ["Simulate an undamped orbit and plot total energy against time. "
            "The shape of the curve names the integrator.",
            "<b>Rising steadily:</b> explicit Euler. It injects energy, "
            "always, and the orbit spirals outward.",
            "<b>Oscillating around a constant:</b> a symplectic method. "
            "Bounded error forever — this is what you usually want.",
            "<b>Slowly decreasing:</b> RK4 or another high-order "
            "non-symplectic scheme. Accurate per step and dissipative over "
            "long runs.",
            "<b>Make this plot before anything else.</b> You will use it in "
            "every module."]},

  {"t": "bullets", "kicker": "Harness", "title": "Build these before you simulate anything",
   "items": [
     "<b>An energy and momentum logger</b> that runs every step and writes "
     "a CSV.",
     "",
     "<b>A plotting script.</b> You will produce hundreds of these plots; "
     "make it one command.",
     "",
     "<b>Frame stepping and rewind</b> in the viewer. A simulation that can "
     "only run forwards cannot be debugged.",
     "",
     "<b>Deterministic replay.</b> Same seed, same sequence, bit-identical "
     "result — otherwise an intermittent bug cannot be reproduced.",
     "",
     "<b>Analytic test cases:</b> free fall, a single undamped spring, a "
     "circular orbit. All three have closed-form answers.",
   ],
   "footnote": "The same argument as CSCE 647's validation suite, for the "
               "same reason.",
   "note": "Determinism is the one they skip, and it is the one that costs "
           "them a week later."},

  {"t": "callout", "title": "Determinism is not optional",
   "kind": "Why to insist on it",
   "body": ["A simulation bug often appears at frame 847 under one specific "
            "configuration.",
            "<b>If the run is not reproducible, you cannot bisect it, "
            "cannot test a fix, and cannot tell a fix from luck.</b>",
            "<b>The usual culprits:</b> uninitialised memory, iteration "
            "order over a hash container, parallel reduction order, and "
            "uncontrolled random seeds.",
            "<b>Fixed time steps help enormously.</b> A variable step tied "
            "to real frame time makes every run different by construction "
            "— which Module 13 returns to."]},
 ],
 "takeaways": [
   "Every system in this course is a state vector x and a derivative "
   "function f, advanced by a stepping scheme. Only x and f change.",
   "Second-order Newtonian dynamics becomes first order by stacking position "
   "and velocity into one state vector.",
   "Separate state, derivative, and integrator in the architecture, and you "
   "can swap integrators in one line — which this course does "
   "constantly.",
   "Graphics requires plausibility, stability, control, and speed, in that "
   "order. Accuracy is not on the list, and that is deliberate.",
   "Art direction is a hard requirement: a simulator that cannot be steered "
   "will not be used, however correct it is.",
   "Plot energy and momentum from the first day. The shape of the energy "
   "curve identifies the integrator, and momentum drift identifies a force "
   "bug.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The structure underneath everything"),
  ("p", "This course covers particles, springs, constraints, collisions, "
        "rigid bodies, deformable solids, cloth, and fluids. They look like "
        "eight unrelated subjects. They are one subject."),
  ("eq", "x&prime; = f(x, t), &nbsp;&nbsp;&nbsp; x(t&#8320;) = x&#8320;"),
  ("p", "A <b>state vector</b> x containing everything needed to describe "
        "the system at an instant, and a <b>derivative function</b> f giving "
        "its rate of change. With an initial condition this is an "
        "<b>initial value problem</b>, and a simulator is a loop that "
        "advances it."),
  ("table", ["System", "State vector contains", "Derivative computes"],
   [["Particles", "Position and velocity of each particle.",
     "Velocity, and force/mass from gravity, drag, and springs."],
    ["Cloth", "The same — cloth is a particle system with structured "
     "connectivity.", "The same, with spring forces from the mesh edges."],
    ["Rigid bodies", "Position, orientation, linear and angular momentum.",
     "Velocity, angular velocity, force, and torque (Module 07)."],
    ["Deformables", "Node positions and velocities.",
     "Internal forces from the strain energy (Module 09)."],
    ["Fluids (Eulerian)", "Velocity and other fields sampled on a grid.",
     "Advection, pressure, and viscosity terms (Module 11)."]],
   [0.16, 0.42, 0.42]),
  ("p", "<b>The loop is identical in every case.</b> Only the contents of x "
        "and the computation of f change. Recognising this turns the field "
        "from a collection of unrelated recipes into one idea with "
        "variations, and it is the single most useful thing in this module."),
  ("callout", "Reducing second order to first order",
   ["Newton's second law is second order: the acceleration, not the "
    "velocity, is what force determines. Integrators are written for "
    "first-order systems.",
    "<b>The reduction is mechanical.</b> Stack position and velocity "
    "together into a single state vector:",
    "<b>x = [p, v]</b> &nbsp;&rArr;&nbsp; <b>x&prime; = [v, F(p, v)/m]</b>",
    "The derivative of the position block is the velocity block, which we "
    "already have; the derivative of the velocity block is force over mass, "
    "which Newton gives us. The system is now first order and any "
    "general-purpose integrator applies.",
    "<b>Do this once, in the architecture.</b> Every system in the course "
    "then presents the same interface, and swapping integrators to compare "
    "them — which this course does in almost every module — "
    "becomes a one-line change rather than a rewrite."]),
  ("code", """struct System {
    virtual int  dim() const = 0;
    virtual void get_state(double* x) const = 0;
    virtual void set_state(const double* x) = 0;
    virtual void derivative(const double* x, double t, double* dx) = 0;
};

struct Integrator {
    virtual void step(System& s, double t, double dt) = 0;
};"""),
  ("p", "The common mistake is to write <code>particle.position += "
        "particle.velocity * dt</code> inside a particle class. It works, "
        "and it welds the integration scheme to the system so that "
        "comparing integrators requires rewriting everything. <b>Separate "
        "state, derivative, and stepping from the first line of code.</b>"),

  ("h1", "2 &nbsp; What 'physically based' means in graphics"),
  ("table", ["Field", "Primary requirement", "Acceptable cost", "Failure"],
   [["<b>Engineering</b>",
     "<b>Accuracy</b>, with quantified error bounds. A 2% error in a bridge "
     "simulation may be unacceptable.",
     "Hours or days per solve.",
     "Being wrong."],
    ["<b>Science</b>",
     "<b>Validity</b> — agreement with experiment, and predictions "
     "that can be falsified.",
     "Supercomputer time.",
     "Disagreeing with measurement."],
    ["<b>Graphics</b>",
     "<b>Plausibility, stability, controllability, speed</b> — in "
     "that order.",
     "Milliseconds to minutes.",
     "<b>Exploding, or being impossible to art-direct.</b>"]],
   [0.13, 0.42, 0.24, 0.21]),
  ("callout", "Stability outranks accuracy, and that drives everything",
   ["A simulation that is 5% wrong and runs reliably for ten thousand frames "
    "is <b>useful</b>. A simulation that is exact for 179 frames and then "
    "produces infinities is <b>worthless</b> — and worse than useless, "
    "because someone spent the render time.",
    "<b>So this course will repeatedly accept provably less accurate methods "
    "in exchange for better stability.</b> Position-based dynamics "
    "(Module 04) is the extreme case: it does not integrate forces at all, "
    "its material behaviour depends on the iteration count and the time "
    "step, and it is in essentially every game engine, because it cannot "
    "explode.",
    "<b>The important thing is to know you are making the trade.</b> The "
    "characteristic failure of this field is making it unconsciously, and "
    "then being unable to explain why the simulated result does not match a "
    "measured one — or, worse, assuming the simulator is right and the "
    "measurement is wrong."]),
  ("callout", "Art direction is a hard requirement",
   ["A director will say the explosion should be bigger, the cape should "
    "settle two seconds sooner, and the splash should go to the left of "
    "frame.",
    "<b>Physics has no 'go left' parameter.</b> A simulator that cannot be "
    "steered will not be used on a production, no matter how physically "
    "faithful it is — because the shot has to match the previous one "
    "and the storyboard.",
    "So production systems expose controls that are frankly unphysical: "
    "per-object gravity, damping multipliers, stiffness that varies across "
    "the mesh, forces that act only during a specified frame range, and "
    "target shapes the simulation is attracted toward.",
    "<b>Design for this from the beginning.</b> Burying real physical "
    "constants inside the solver, with no way to override them per object or "
    "per frame, is how you build something that is technically impressive "
    "and professionally unusable."]),

  ("break",),
  ("h1", "3 &nbsp; Measurement"),
  ("table", ["Quantity", "Conserved when", "Drift means"],
   [["<b>Linear momentum</b>", "No net external force acts.",
     "<b>Forces are not equal and opposite.</b> Usually a spring applying "
     "force to one endpoint and not the other, or a collision impulse "
     "applied asymmetrically."],
    ["<b>Angular momentum</b>", "No net external torque acts.",
     "<b>A force is being applied at the wrong point</b> — at the "
     "centre of mass rather than the contact point, typically."],
    ["<b>Energy</b>", "No damping, friction, or other dissipation.",
     "<b>Almost always the integrator</b> (Module 02). This is the most "
     "informative plot in the course."],
    ["<b>Volume</b>", "The material is incompressible.",
     "A fluid or soft body is leaking — usually a pressure solve that "
     "has not converged (Modules 09, 11)."]],
   [0.17, 0.26, 0.57]),
  ("callout", "The energy curve identifies the integrator",
   ["Simulate something with no dissipation — a particle in a circular "
    "orbit under an inverse-square force is ideal, because the exact "
    "solution is known — and plot total energy against time over ten "
    "thousand steps.",
    "<b>Rising steadily:</b> explicit Euler. It injects energy at every "
    "step, without exception, and the orbit spirals outward until it "
    "escapes.",
    "<b>Oscillating within a fixed band around the true value:</b> a "
    "<b>symplectic</b> method — symplectic Euler or velocity Verlet. "
    "The error is bounded for all time rather than accumulating, which is "
    "usually exactly what you want.",
    "<b>Slowly decreasing:</b> RK4 or another high-order non-symplectic "
    "scheme. Very accurate over a few steps, mildly dissipative over "
    "thousands.",
    "<b>Produce this plot before implementing anything else.</b> Module 02 "
    "explains why each curve has the shape it does, and you will refer to "
    "this diagnostic in every subsequent module."]),
  ("h2", "3.1 &nbsp; The harness to build first"),
  ("ul", ["<b>An energy and momentum logger</b> that runs every step and "
          "appends to a CSV. Cheap, and it costs nothing to leave running.",
          "<b>A plotting script</b> that turns that CSV into a figure in one "
          "command. You will make hundreds of these plots; friction here "
          "means you will stop making them, which is how simulations go "
          "wrong unnoticed.",
          "<b>Frame stepping, pausing, and rewind in the viewer.</b> A "
          "simulation that can only run forwards at full speed cannot be "
          "debugged, because the interesting moment is always one frame "
          "before you noticed.",
          "<b>Deterministic replay.</b> See below.",
          "<b>Analytic test cases.</b> Free fall under constant gravity, a "
          "single undamped spring, and a circular orbit all have closed-form "
          "solutions. Any error in these is unambiguous."]),
  ("callout", "Determinism is not optional",
   ["Simulation bugs are characteristically intermittent and late: the "
    "stack collapses at frame 847, but only sometimes.",
    "<b>If the run is not reproducible, you cannot bisect the failure, "
    "cannot verify a fix, and cannot distinguish a fix from luck.</b> You "
    "will spend days on something that a reproducible case resolves in an "
    "hour.",
    "<b>The usual causes of non-determinism:</b> reading uninitialised "
    "memory; iterating over a hash container whose order depends on "
    "allocation addresses; parallel reductions that sum in a "
    "non-deterministic order (floating-point addition is not associative); "
    "and uncontrolled random seeds.",
    "<b>Fixed time steps help enormously.</b> A step size tied to real frame "
    "time makes every run different by construction, and makes the "
    "simulation's behaviour depend on the machine it runs on. Module 13 "
    "covers how to keep a fixed simulation step while rendering at a "
    "variable rate."]),
 ],
 "resources": [
   ("Baraff & Witkin &mdash; Differential Equation Basics (free notes)",
    "https://graphics.pixar.com/tutorials/",
    "The first set of notes in the course pack, and the source of &sect;1's "
    "framing. Short and exceptionally clear."),
   ("Ten Minute Physics &mdash; episodes 1–3",
    "https://matthias-research.github.io/pages/tenMinutePhysics/",
    "Getting a first simulation running, with working code. Do this before "
    "Module 02."),
   ("Bargteil & Shinar &mdash; An Introduction to Physics-Based Animation",
    "https://dl.acm.org/doi/10.1145/3214834.3214849",
    "The survey's opening sections cover exactly this module's framing, with "
    "a wider view of where the field has gone."),
   ("Hairer, Lubich & Wanner &mdash; Geometric Numerical Integration "
    "(chapter 1 free)",
    "https://www.unige.ch/~hairer/",
    "Why symplectic integrators behave as they do. Heavy going, and the "
    "first chapter's figures explain the energy curves of &sect;3 better "
    "than anything else."),
 ],
 "exercises": [
   "Implement the <code>System</code> and <code>Integrator</code> interfaces "
   "of &sect;1 and a single particle under gravity. Verify against the "
   "closed-form solution for free fall.",
   "Add a spring and verify against the analytic solution for simple "
   "harmonic motion. Report the error after 1, 10, and 100 periods.",
   "Build the energy and momentum logger and the plotting script. This is "
   "infrastructure for the whole course — do it properly.",
   "Simulate a particle in a circular orbit with explicit Euler and plot "
   "total energy over 10,000 steps. Report the percentage gained.",
   "Write down the state vector and derivative function for three systems "
   "of your choosing that are <i>not</i> in the table in &sect;1 — a "
   "pendulum, a rocket losing mass, a population model.",
   "Make your simulation deterministic and prove it: run the same scenario "
   "twice and compare the final state bit for bit.",
   "Deliberately break determinism by iterating over an "
   "<code>unordered_map</code> of particles, and show the final states "
   "differ.",
   "Implement frame stepping and rewind in your viewer. You will use them "
   "constantly from Module 05 onward.",
   "Write a page on a simulation you have seen in a film or game, "
   "identifying where it was art-directed rather than simulated. The "
   "evidence is usually visible once you look.",
 ],
 "selfcheck": [
   "Write the general form every system in this course takes.",
   "How is a second-order Newtonian system reduced to first order, and why "
   "is that necessary?",
   "Why should state, derivative, and integrator be separated in the "
   "architecture?",
   "Give the primary requirement of engineering, scientific, and graphics "
   "simulation, and the failure mode of each.",
   "Why does stability outrank accuracy in graphics, and what does that "
   "licence?",
   "Why is art-directability a hard requirement rather than a nice-to-have?",
   "Name four conserved quantities and say what drift in each one indicates.",
   "What three shapes can an energy curve take, and what does each one "
   "identify?",
   "Give three causes of non-determinism in a simulator and say why it "
   "matters.",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Numerical Integration",
 "subtitle": "Why your simulation explodes, and which scheme stops it.",
 "question": "How do you advance a state vector in time without it blowing "
             "up?",
 "outcomes": [
     "Derive explicit Euler and explain why it gains energy.",
     "Distinguish accuracy from stability, and order from behaviour.",
     "Explain what symplectic means and why it matters over long runs.",
     "Define stiffness and explain why it forces implicit integration.",
     "Choose an integrator from a system's requirements.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The obvious method",
   "blurb": "And exactly why it fails."},

  {"t": "eq", "kicker": "Explicit Euler", "title": "The first thing anyone writes",
   "eqs": [
     ("x(t + Δt)  =  x(t)  +  Δt · f(x(t), t)",
      "Evaluate the derivative where you are, and step along it. First-order "
      "accurate: error per step is O(Δt²)."),
     ("p ← p + Δt·v    then    v ← v + Δt·a",
      "Written out for a particle. Note the order: both updates use the OLD "
      "values. That is what makes it explicit."),
   ],
   "caption": "Simple, obvious, and unconditionally unstable for "
              "oscillatory systems. It is wrong in a specific and "
              "instructive way.",
   "note": "Everyone writes this first. The point is to understand exactly "
           "why it fails, not to avoid writing it."},

  {"t": "callout", "title": "Explicit Euler always gains energy",
   "kind": "Why, geometrically",
   "body": ["Consider a particle in a circular orbit. The true motion curves "
            "continuously toward the centre.",
            "<b>Euler steps along the tangent</b>, which is a straight line, "
            "and a tangent to a circle always lands <i>outside</i> it.",
            "So every step moves the particle slightly further out than it "
            "should be, at slightly too much speed. <b>Energy increases "
            "monotonically</b> and the orbit spirals outward.",
            "<b>And no smaller time step fixes it.</b> A smaller step makes "
            "it slower, not stable. The error is systematic, not random — "
            "which is the whole lesson."]},

  {"t": "two", "kicker": "Two properties", "title": "Accuracy and stability are different",
   "lh": "Accuracy — order",
   "l": ["How fast error shrinks as Δt shrinks.",
         "Euler is O(Δt), RK4 is O(Δt⁴).",
         ("Matters over a few steps.", 1),
         "<b>A high-order method can still blow up.</b>"],
   "rh": "Stability — behaviour",
   "r": ["Whether error <b>grows</b> over many steps.",
         "Determines the maximum usable Δt.",
         ("Matters over thousands of steps.", 1),
         "<b>This is what you actually care about.</b>"],
   "note": "The distinction is the module's core. Students conflate them and "
           "then reach for RK4 to fix an instability."},

  {"t": "section", "label": "Part 2", "title": "Symplectic integrators",
   "blurb": "A one-line change with a disproportionate payoff."},

  {"t": "code", "kicker": "The fix", "title": "Symplectic Euler is Euler with the lines swapped",
   "lang": "cpp", "code": """
// EXPLICIT (forward) Euler -- unstable for oscillators:
    p += v * dt;          // uses OLD v
    v += a * dt;

// SYMPLECTIC (semi-implicit) Euler -- stable:
    v += a * dt;          // update velocity FIRST
    p += v * dt;          // then use the NEW v

// That is the entire difference. Same cost, same order of accuracy,
// completely different long-term behaviour: energy now oscillates
// within a bounded band instead of growing without limit.
//
// If you take one practical thing from this course, it is this.
""",
   "caption": "Same operations, same cost, one line reordered. Energy "
              "becomes bounded rather than divergent.",
   "note": "Show the two energy plots side by side immediately after this. "
           "The contrast is the most convincing thing in the module."},

  {"t": "callout", "title": "What symplectic actually means",
   "kind": "The property",
   "body": ["A symplectic integrator preserves the <b>phase-space volume</b> "
            "of the system — a geometric structure that Hamiltonian "
            "mechanics says the true dynamics preserves.",
            "<b>The practical consequence:</b> energy error is <i>bounded "
            "for all time</i> rather than accumulating. It oscillates; it "
            "does not drift.",
            "<b>It does not mean energy is conserved exactly.</b> The "
            "simulated system conserves a slightly different energy, which "
            "stays close to the true one.",
            "<b>This is why a symplectic first-order method beats a "
            "non-symplectic fourth-order one</b> for long simulations — "
            "a qualitative property beating three orders of accuracy."]},

  {"t": "table", "kicker": "The options", "title": "Explicit integrators compared",
   "header": ["Method", "Order", "Symplectic", "Use for"],
   "widths": [2.9, 1.5, 2.2, 5.5],
   "rows": [
     ["Explicit Euler", "1", "No", "<b>Nothing. Teaching only</b>"],
     ["<b>Symplectic Euler</b>", "1", "<b>Yes</b>", "<b>The default. Games, real time</b>"],
     ["Velocity Verlet", "2", "<b>Yes</b>", "<b>Better accuracy, same cost</b>"],
     ["Midpoint / RK2", "2", "No", "Smooth non-oscillatory systems"],
     ["RK4", "4", "No", "<b>Accuracy over short runs</b>"],
   ],
   "footnote": "RK4 costs four derivative evaluations per step. Four "
               "symplectic Euler steps are often better value.",
   "note": "The footnote matters: comparing integrators per-step rather "
           "than per-unit-work is misleading."},

  {"t": "section", "label": "Part 3", "title": "Stiffness",
   "blurb": "The reason some systems need a different approach entirely."},

  {"t": "callout", "title": "A stiff system has timescales that differ enormously",
   "kind": "The definition",
   "body": ["Stiff cloth: the stretch springs oscillate at kilohertz; the "
            "cloth visibly moves at a few hertz.",
            "<b>An explicit method must resolve the fastest timescale</b> or "
            "it goes unstable — even though nothing visually interesting "
            "happens there.",
            "<b>So Δt is limited by the stiffest spring in the mesh</b>, "
            "which may be thousands of times smaller than the motion "
            "requires.",
            "<b>Stiffer material means smaller steps means slower "
            "simulation.</b> Stiff cloth with explicit integration is "
            "unaffordable, and that is a property of the method, not the "
            "hardware."]},

  {"t": "eq", "kicker": "The limit", "title": "The explicit stability condition",
   "eqs": [
     ("Δt  <  2 √(m / k)",
      "For a mass-spring system: the step is bounded by the stiffest spring "
      "and the lightest mass."),
     ("k × 100  ⟹  Δt ÷ 10",
      "A hundred times stiffer needs ten times smaller steps. Stiffness is "
      "expensive, superlinearly in practice."),
   ],
   "caption": "This is a hard limit from the method, not a tuning "
              "suggestion. Exceed it and the system diverges.",
   "note": "Have them measure this empirically — the predicted threshold "
           "matches the observed one closely, which is satisfying."},

  {"t": "eq", "kicker": "Implicit", "title": "Backward Euler: evaluate the derivative at the destination",
   "eqs": [
     ("x(t + Δt)  =  x(t)  +  Δt · f( x(t + Δt) )",
      "The unknown appears on both sides, so each step requires solving a "
      "system of equations."),
     ("(I − Δt·∂f/∂x) Δx  =  Δt · f(x)",
      "Linearise and solve. A sparse linear system per step, usually with "
      "conjugate gradient."),
   ],
   "caption": "Unconditionally stable: any time step works. The cost is a "
              "linear solve per step and heavy artificial damping.",
   "note": "Baraff–Witkin 1998 is the paper that made cloth practical by "
           "doing exactly this."},

  {"t": "callout", "title": "Implicit methods trade energy for stability",
   "kind": "The honest cost",
   "body": ["<b>Backward Euler is unconditionally stable</b> — it will "
            "not explode at any time step, which is why Baraff and Witkin's "
            "1998 cloth paper changed the field.",
            "<b>But it is strongly dissipative.</b> It removes energy "
            "aggressively, and at large steps the result is visibly "
            "over-damped: cloth that looks like it is moving through "
            "treacle.",
            "<b>That damping is why it is stable.</b> It is not a bug to be "
            "fixed; it is the mechanism.",
            "<b>Implicit midpoint and BDF2</b> are less dissipative and "
            "harder to make robust. Most production cloth uses backward "
            "Euler and accepts the damping."]},

  {"t": "table", "kicker": "Choosing", "title": "Which integrator for which system",
   "header": ["System", "Choice", "Why"],
   "widths": [3.4, 3.6, 5.1],
   "rows": [
     ["Particles, loose springs", "<b>Symplectic Euler</b>", "Cheap, stable, good enough"],
     ["Rigid bodies", "<b>Symplectic Euler + substeps</b>", "Contact needs small steps anyway"],
     ["Stiff cloth", "<b>Implicit (backward Euler)</b>", "<b>Explicit is unaffordable</b>"],
     ["Orbital or long-run", "Velocity Verlet", "Bounded energy over millions of steps"],
     ["Accuracy over a short run", "RK4", "Highest order per step"],
     ["Games, everything", "<b>XPBD (Module 04)</b>", "<b>Cannot explode; tunable</b>"],
   ],
   "note": "The last row is where industry actually landed, and Module 04 "
           "explains why despite its theoretical weaknesses."},

  {"t": "bullets", "kicker": "Practice", "title": "Things that matter more than the choice",
   "items": [
     "<b>Substepping.</b> Several small steps per frame is usually better "
     "than one large step with a fancier method, and far simpler.",
     "",
     "<b>Fixed time step.</b> A variable step makes behaviour depend on "
     "frame rate and destroys determinism (Module 01).",
     "",
     "<b>Clamp velocities</b> as a safety net. Unphysical, and it stops one "
     "bad frame from destroying a simulation.",
     "",
     "<b>Detect NaN early.</b> One NaN propagates through the entire state "
     "within a few steps. Assert on it.",
     "",
     "<b>Measure, do not assume.</b> Plot the energy.",
   ],
   "footnote": "Substepping is the single most effective practical lever in "
               "this module."},
 ],
 "takeaways": [
   "Explicit Euler steps along the tangent, which for an orbit always lands "
   "outside — so it gains energy systematically, and no smaller step "
   "fixes it.",
   "Accuracy is how fast error shrinks with &Delta;t; stability is whether "
   "error grows over many steps. Stability is what you actually need.",
   "Symplectic Euler is explicit Euler with two lines swapped, and it turns "
   "unbounded energy growth into bounded oscillation.",
   "A symplectic first-order method beats a non-symplectic fourth-order one "
   "over long runs — a qualitative property beating three orders.",
   "Stiffness means timescales differing by orders of magnitude; explicit "
   "methods must resolve the fastest, so &Delta;t is bounded by 2&radic;(m/k).",
   "Implicit methods are unconditionally stable because they are "
   "dissipative. The damping is the mechanism, not a defect.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Explicit Euler, and exactly how it fails"),
  ("eq", "x(t + &Delta;t) = x(t) + &Delta;t &middot; f(x(t), t)"),
  ("p", "Evaluate the derivative where you currently are, and step along it. "
        "It is the first method anyone writes, it is first-order accurate "
        "— local error O(&Delta;t&#178;), global error O(&Delta;t) "
        "— and it is unstable for oscillatory systems regardless of "
        "step size."),
  ("callout", "The geometric reason it gains energy",
   ["Take a particle in a circular orbit under a central force. The true "
    "trajectory curves continuously toward the centre.",
    "<b>Explicit Euler steps along the tangent line</b>, because that is "
    "what the derivative at the current point describes. <b>A tangent to a "
    "circle always lies outside the circle.</b>",
    "So after each step the particle is slightly further from the centre "
    "than it should be, and moving slightly too fast for its new radius. "
    "<b>Total energy increases, monotonically, every single step.</b> Over "
    "thousands of steps the orbit spirals outward and eventually escapes.",
    "<b>Reducing the time step does not fix this.</b> It slows the growth "
    "— halving &Delta;t roughly halves the rate — but the sign of "
    "the error is always the same, so the energy still grows without bound. "
    "<b>The error is systematic, not random, and that is the entire "
    "lesson:</b> no amount of refinement rescues a method whose error does "
    "not cancel."]),
  ("table", ["", "Accuracy (order)", "Stability"],
   [["Asks", "How fast does error shrink as &Delta;t shrinks?",
     "Does error <b>grow</b> as steps accumulate?"],
    ["Measured by", "The exponent: Euler is O(&Delta;t), RK4 is "
     "O(&Delta;t&#8308;).",
     "The largest &Delta;t for which the system does not diverge."],
    ["Matters over", "A few steps.", "<b>Thousands of steps.</b>"],
    ["Relationship", "<b>Independent.</b> A fourth-order method can be "
     "unstable; a first-order method can be perfectly stable.",
     "<b>This is what you actually care about in a simulator</b>, which runs "
     "for hours."]],
   [0.13, 0.43, 0.44]),
  ("p", "<b>Conflating these two is the most common conceptual error in "
        "this module.</b> Someone whose simulation explodes reaches for RK4, "
        "because it is 'more accurate'. RK4 is not symplectic and will also "
        "lose energy over long runs; it buys accuracy, which was not the "
        "problem."),

  ("h1", "2 &nbsp; Symplectic integrators"),
  ("code", """// Explicit (forward) Euler -- unstable for oscillators
p += v * dt;          // uses OLD v
v += a * dt;

// Symplectic (semi-implicit) Euler -- stable
v += a * dt;          // update velocity FIRST
p += v * dt;          // then use the NEW v"""),
  ("p", "The two lines are swapped. The cost is identical, the order of "
        "accuracy is identical, and the long-term behaviour is completely "
        "different: energy now oscillates within a bounded band instead of "
        "growing without limit. <b>If you take one practical result from "
        "this course, it is this one.</b>"),
  ("callout", "What 'symplectic' means and does not mean",
   ["A symplectic integrator preserves the <b>phase-space volume</b> of the "
    "system — a geometric structure that Hamiltonian mechanics shows "
    "the true dynamics preserves exactly. Liouville's theorem is the formal "
    "statement.",
    "<b>The practical consequence is that the energy error is bounded for "
    "all time.</b> It oscillates with the system's period; it does not "
    "accumulate. A symplectic simulation of the solar system can run for "
    "millions of years without the planets drifting away.",
    "<b>It does not mean energy is conserved exactly.</b> What the method "
    "conserves exactly is the energy of a slightly <i>different</i> system "
    "— a 'shadow Hamiltonian' close to the true one. That is why the "
    "error oscillates rather than vanishing.",
    "<b>This is why a symplectic first-order method outperforms a "
    "non-symplectic fourth-order one over long runs.</b> A qualitative "
    "structural property beats three orders of accuracy, which is a "
    "genuinely surprising result and one of the more satisfying facts in "
    "numerical analysis."]),
  ("table", ["Method", "Order", "Symplectic", "Cost per step", "Use for"],
   [["<b>Explicit Euler</b>", "1", "No", "1 derivative",
     "<b>Nothing in production.</b> Teaching, and as a baseline for the "
     "energy plot."],
    ["<b>Symplectic Euler</b>", "1", "<b>Yes</b>", "1 derivative",
     "<b>The sensible default.</b> Games, real-time, anything with "
     "contact."],
    ["<b>Velocity Verlet</b>", "2", "<b>Yes</b>", "1 derivative",
     "<b>Strictly better than symplectic Euler</b> for the same cost when "
     "forces do not depend on velocity. Molecular dynamics uses it "
     "universally."],
    ["<b>Midpoint / RK2</b>", "2", "No", "2 derivatives",
     "Smooth non-oscillatory systems."],
    ["<b>RK4</b>", "4", "No", "4 derivatives",
     "High accuracy over short runs. <b>Compare it against four symplectic "
     "Euler steps</b>, not against one — that is the fair "
     "comparison, and it often loses."]],
   [0.17, 0.07, 0.12, 0.16, 0.48]),

  ("break",),
  ("h1", "3 &nbsp; Stiffness"),
  ("callout", "What stiffness is",
   ["A system is <b>stiff</b> when it contains processes whose "
    "characteristic timescales differ by orders of magnitude.",
    "Cloth is the canonical example. The stretch springs that stop the "
    "fabric from extending are very strong, so they oscillate at kilohertz "
    "frequencies. The cloth's visible motion — draping, swinging "
    "— happens at a few hertz.",
    "<b>An explicit integrator must resolve the fastest timescale present, "
    "or it goes unstable</b>, even though nothing visually interesting "
    "happens at that frequency. The method cannot ignore a mode simply "
    "because we are uninterested in it.",
    "<b>So &Delta;t is dictated by the stiffest spring in the mesh</b>, "
    "which may be thousands of times smaller than the visible motion "
    "requires. Stiffer cloth means smaller steps means a slower simulation "
    "— and this is a property of the method, not of the hardware."]),
  ("eq", "&Delta;t &lt; 2 &radic;(m / k)"),
  ("p", "For a mass-spring system with explicit integration, the step is "
        "bounded by the stiffest spring constant k and the smallest mass m. "
        "<b>Making a material a hundred times stiffer requires a ten times "
        "smaller step</b>, so a hundred times the work for the same "
        "simulated duration. This is a hard limit derived from the method's "
        "stability region, not a tuning guideline, and it is worth measuring "
        "empirically — the predicted threshold matches the observed one "
        "closely."),
  ("h2", "3.1 &nbsp; Implicit integration"),
  ("eq", "x(t + &Delta;t) = x(t) + &Delta;t &middot; f( x(t + &Delta;t) )"),
  ("p", "<b>Backward Euler</b> evaluates the derivative at the destination "
        "rather than the origin. The unknown now appears on both sides, so "
        "each step requires solving a system of equations rather than "
        "evaluating an expression. Linearising about the current state "
        "gives:"),
  ("eq", "( I &minus; &Delta;t &middot; &part;f/&part;x ) &Delta;x = "
         "&Delta;t &middot; f(x)"),
  ("p", "A sparse linear system, solved each step — typically by "
        "conjugate gradient, since the matrix is large, sparse, and usually "
        "symmetric positive definite. The Jacobian "
        "&part;f/&part;x must be assembled, which is the fiddly part."),
  ("callout", "Implicit methods buy stability with dissipation",
   ["<b>Backward Euler is unconditionally stable:</b> it will not diverge at "
    "<i>any</i> time step. Baraff and Witkin's 1998 cloth paper applied "
    "exactly this and changed what was possible — cloth that had "
    "required thousands of tiny explicit steps could now be advanced one "
    "frame at a time.",
    "<b>But it is strongly dissipative.</b> It removes energy aggressively, "
    "and at large time steps the result is visibly over-damped: cloth that "
    "moves as though through treacle, losing the high-frequency flutter that "
    "makes fabric look like fabric.",
    "<b>The damping is not a defect to be fixed — it is the "
    "mechanism.</b> The method is stable precisely because it drives "
    "high-frequency modes to zero, and those modes include ones you might "
    "have wanted.",
    "<b>Less dissipative implicit schemes exist</b> — implicit "
    "midpoint, BDF2 — and are harder to make robust in the presence of "
    "contact and collision. Most production cloth uses backward Euler and "
    "compensates artistically for the damping."]),

  ("h1", "4 &nbsp; Choosing, and what matters more"),
  ("table", ["System", "Integrator", "Reasoning"],
   [["Particles, loose springs, general dynamics.",
     "<b>Symplectic Euler.</b>",
     "Cheap, stable for non-stiff systems, bounded energy. The right "
     "default."],
    ["Rigid bodies with contact.",
     "<b>Symplectic Euler with substepping.</b>",
     "Contact resolution requires small steps regardless, so a "
     "higher-order method buys nothing."],
    ["Stiff cloth.", "<b>Implicit (backward Euler).</b>",
     "<b>Explicit integration is unaffordable</b> by &sect;3's bound."],
    ["Orbital mechanics, molecular dynamics, very long runs.",
     "<b>Velocity Verlet.</b>",
     "Symplectic, second order, one derivative evaluation. Energy bounded "
     "over millions of steps."],
    ["High accuracy over a short interval.", "<b>RK4.</b>",
     "Highest order per step — but compare against four symplectic "
     "steps for fairness."],
    ["Games, interactive, robustness above all.",
     "<b>XPBD (Module 04).</b>",
     "<b>Cannot explode under any circumstances</b>, and the stiffness is "
     "directly tunable. Theoretically weak and practically dominant."]],
   [0.26, 0.26, 0.48]),
  ("ul", ["<b>Substepping is the most effective practical lever here.</b> "
          "Taking four small symplectic Euler steps per frame is usually "
          "better, simpler, and more robust than one large step with a "
          "sophisticated method — and it composes with everything "
          "else.",
          "<b>Use a fixed time step.</b> A step tied to real frame time "
          "makes the simulation's behaviour depend on the machine's "
          "performance and destroys determinism (Module 01). Module 13 "
          "covers decoupling simulation rate from render rate.",
          "<b>Clamp velocities</b> as a safety net. It is unphysical and it "
          "prevents one bad frame — an interpenetration, a degenerate "
          "contact — from destroying an otherwise good simulation.",
          "<b>Assert on NaN every step, in debug builds.</b> A single NaN "
          "propagates through the entire state within a few steps, at which "
          "point the original cause is unrecoverable. Catching it on the "
          "step it appears turns an impossible bug into an easy one.",
          "<b>Measure rather than assume.</b> Plot the energy. The curve "
          "will tell you whether the integrator is behaving as the theory "
          "says it should, and it is the only way to know."]),
 ],
 "resources": [
   ("Baraff & Witkin &mdash; Differential Equation Basics and Implicit "
    "Methods (free notes)",
    "https://graphics.pixar.com/tutorials/",
    "Sections B and E of the course pack. The implicit cloth derivation of "
    "&sect;3 is in the 1998 paper linked from the same page."),
   ("Ten Minute Physics &mdash; integration and stability episodes",
    "https://matthias-research.github.io/pages/tenMinutePhysics/",
    "The energy behaviour of &sect;1 and &sect;2, demonstrated interactively "
    "— which is far more convincing than reading about it."),
   ("Hairer, Lubich & Wanner &mdash; Geometric Numerical Integration",
    "https://www.unige.ch/~hairer/",
    "The authoritative account of why symplectic methods behave as they do. "
    "Chapter 1 is free and its figures are the best illustration of "
    "&sect;2."),
   ("Baraff & Witkin &mdash; Large Steps in Cloth Simulation (1998, free)",
    "https://www.cs.cmu.edu/~baraff/papers/",
    "The paper that made implicit cloth practical. Read it before "
    "Module 10."),
   ("Erin Catto &mdash; Numerical Integration (GDC, free slides)",
    "https://box2d.org/publications/",
    "The game-development view: why symplectic Euler and substepping beat "
    "cleverness in practice."),
 ],
 "exercises": [
   "Implement explicit Euler, symplectic Euler, velocity Verlet, and RK4 "
   "behind the interface from Module 01.",
   "<b>Produce the energy plot:</b> a particle in a circular orbit under "
   "each integrator, 10,000 steps, total energy against time on one figure. "
   "Explain the shape of each curve. This figure belongs in your portfolio.",
   "Halve the time step for explicit Euler and show that the energy still "
   "grows, only more slowly. Report the relationship.",
   "Measure the stability limit for a single mass-spring system "
   "experimentally and compare against 2&radic;(m/k). Report the agreement.",
   "Vary the spring constant over three orders of magnitude and plot the "
   "maximum stable time step against it on log-log axes. The slope should "
   "be &minus;0.5.",
   "Compare RK4 at &Delta;t against symplectic Euler at &Delta;t/4 — "
   "equal derivative evaluations. Report accuracy and energy behaviour for "
   "both.",
   "Implement backward Euler for a mass-spring system. Confirm it is stable "
   "at a time step a hundred times larger than the explicit limit, and "
   "measure the energy it removes.",
   "Build a stiff cloth patch and find the explicit stability limit "
   "empirically. Estimate the cost of simulating one second of it.",
   "Introduce a NaN deliberately and count how many steps until the entire "
   "state is corrupted. Then add the assertion.",
 ],
 "selfcheck": [
   "Write explicit Euler and explain geometrically why it gains energy on an "
   "orbit.",
   "Why does reducing the time step not make explicit Euler stable?",
   "Distinguish accuracy from stability, and say which matters for a "
   "simulator.",
   "What is the difference between explicit and symplectic Euler, and what "
   "does it change?",
   "What does symplectic mean, and what does it <i>not</i> guarantee?",
   "Why can a symplectic first-order method beat a non-symplectic "
   "fourth-order one?",
   "Define stiffness and explain why it limits explicit time steps.",
   "State the explicit stability bound and say what happens when stiffness "
   "increases a hundredfold.",
   "Why are implicit methods unconditionally stable, and what is the cost?",
   "Name three practical measures that matter more than the choice of "
   "integrator.",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c649_b2", "c649_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
