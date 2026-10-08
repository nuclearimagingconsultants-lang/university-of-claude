# -*- coding: utf-8 -*-
"""Build the program handbook and the free-resource catalog PDF."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "content"))

from uc import Doc, link
from catalog import CATALOG

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "00_Program")

CORE = [
    ("CSCE 629", "Analysis of Algorithms", "S1"),
    ("CSCE 614", "Computer Architecture", "S1"),
    ("CSCE 611", "Operating Systems", "S2"),
    ("CSCE 606", "Software Engineering", "S2"),
    ("CSCE 608", "Database Systems", "S3"),
]
TRACK = [
    ("CSCE 641", "Computer Graphics", "S1"),
    ("CSCE 645", "Geometric Modeling", "S2"),
    ("CSCE 647", "Image Synthesis", "S3"),
    ("CSCE 649", "Physically-Based Modeling", "S3"),
    ("CSCE 650", "Virtual Reality", "S4"),
    ("CSCE 748", "Computational Photography", "S4"),
]
ELECT = [("CSCE 735", "Parallel Computing", "S4")]


# ---------------------------------------------------------------- handbook
def handbook():
    d = Doc("Master of Science in Computer Science",
            "Graphics &amp; Game Engines track \u00b7 36 credit-equivalents \u00b7 "
            "self-paced, entirely free",
            course="Program Handbook",
            kicker="UNIVERSITY OF CLAUDE \u00b7 PROGRAM HANDBOOK \u00b7 2026")

    d.callout("Read this first", [
        "The University of Claude is not an accredited institution. This "
        "program awards no degree, transcript, or credential, and nothing "
        "here is recognised by a registrar anywhere.",
        "What it is: a complete, rigorously sequenced graduate curriculum "
        "with original lecture materials, mapped onto free university "
        "courseware \u2014 so that the <i>learning</i> is equivalent even "
        "though the paperwork is not. The portfolio you build is the "
        "credential.",
        "All material written for this program is original and free to copy, "
        "adapt, and redistribute. No institution's copyrighted lecture "
        "slides, notes, or problem sets are reproduced; external courses are "
        "referenced by link only, and remain under their own licences.",
    ])

    d.h1("1 &nbsp; What this program is for")
    d.p("A graduate curriculum is not a list of topics. It is a <b>dependency "
        "graph with a deadline</b>: a sequence in which each course makes the "
        "next one tractable, compressed enough that you are still holding the "
        "earlier material when the later material needs it. Most self-study "
        "fails not from bad resources \u2014 the free resources are "
        "extraordinary \u2014 but from an absent sequence, no forcing "
        "function, and no artifact at the end.")
    d.p("This program supplies the three things a university actually "
        "provides that a playlist does not: <b>an order</b>, <b>a standard</b>, "
        "and <b>an artifact</b>. The lectures you can get free. The structure "
        "is what has been missing.")

    d.h2("Design principles")
    d.bullets([
        "<b>Build, don't watch.</b> Every module ends in code that runs. A "
        "module you cannot demonstrate is a module you have not finished.",
        "<b>One renderer, four semesters.</b> The track courses compound into "
        "a single codebase rather than twelve disconnected toy projects.",
        "<b>Theory where it pays rent.</b> Core courses are included because "
        "graphics work breaks on them \u2014 cache behaviour, scheduling, "
        "asymptotics \u2014 not for completeness.",
        "<b>Free, permanently.</b> Every external resource is open "
        "courseware, an author-released book, a public lecture recording, or "
        "a free-audit MOOC. No resource in this program requires payment.",
    ])

    d.h1("2 &nbsp; Admission and prerequisites")
    d.p("Two mathematics prerequisites and one programming prerequisite are "
        "assumed. They are not part of the 36 credits. If you are confident "
        "in all three, begin at Semester 1; if not, spend four to six weeks "
        "here first \u2014 skipping them is the single most common cause of "
        "failure in Semester 1.")
    d.table(
        ["Prerequisite", "Why it is required", "Free resource"],
        [["Discrete mathematics &amp; proof",
          "CSCE 629 is unreadable without proof technique, induction, and "
          "asymptotic reasoning.",
          link("https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/",
               "MIT 6.042J / 6.1200J Mathematics for CS (OCW, full video)")],
         ["Linear algebra",
          "The graphics pipeline <i>is</i> linear algebra. Bases, change of "
          "basis, projection, and eigenstructure are used daily from week 2.",
          link("https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
               "MIT 18.06 \u2014 Strang (OCW)") + " &middot; " +
          link("https://www.3blue1brown.com/topics/linear-algebra",
               "3Blue1Brown, Essence of Linear Algebra")],
         ["C++ fluency",
          "Every track project is C++ with a graphics API. You need RAII, "
          "templates, and comfort with manual memory.",
          link("https://www.learncpp.com/", "learncpp.com (complete, free)")]],
        widths=[0.21, 0.42, 0.37])

    d.pagebreak()
    d.h1("3 &nbsp; Degree structure")
    d.p("Twelve courses, thirty-six credit-equivalents, plus a capstone. "
        "Five core courses establish the systems and theory foundation; six "
        "track courses build graphics depth; one computation elective covers "
        "the parallel hardware all modern rendering runs on.")

    d.h2("Core \u2014 5 courses, 15 credits")
    d.table(["Course", "Title", "Why it is in a graphics degree"],
            [["CSCE 629", "Analysis of Algorithms",
              "Spatial data structures, BVH construction, and visibility are "
              "algorithm-design problems with hard asymptotic limits."],
             ["CSCE 614", "Computer Architecture",
              "Cache lines, memory bandwidth, and SIMD decide real frame "
              "times far more often than algorithmic cleverness does."],
             ["CSCE 611", "Operating Systems",
              "Scheduling, virtual memory, and synchronisation underlie every "
              "render thread, streaming system, and frame pacing bug."],
             ["CSCE 606", "Software Engineering",
              "An engine is a long-lived codebase with many contributors. "
              "This is the course that keeps it from collapsing."],
             ["CSCE 608", "Database Systems",
              "Asset pipelines, scene databases, and streaming are indexing "
              "and query-planning problems wearing different clothes."]],
            widths=[0.13, 0.26, 0.61])

    d.h2("Graphics &amp; Game Engines track \u2014 6 courses, 18 credits")
    d.table(["Course", "Title", "What you build"],
            [["CSCE 641", "Computer Graphics",
              "A software rasteriser, then a real-time GPU pipeline: "
              "transforms, shading, texturing, shadows."],
             ["CSCE 645", "Geometric Modeling",
              "A mesh-processing library: splines, subdivision, "
              "simplification, parameterisation, remeshing."],
             ["CSCE 647", "Image Synthesis",
              "A physically based path tracer with importance sampling, "
              "multiple importance sampling, and participating media."],
             ["CSCE 649", "Physically-Based Modeling",
              "A simulation layer: particles, rigid bodies, cloth, "
              "position-based dynamics, and a FLIP fluid."],
             ["CSCE 650", "Virtual Reality",
              "A stereo renderer with tracking, lens correction, and a "
              "latency budget you measure rather than guess."],
             ["CSCE 748", "Computational Photography",
              "An imaging pipeline: RAW processing, HDR merge, tonemapping, "
              "and lightfield reconstruction."]],
            widths=[0.13, 0.26, 0.61])

    d.h2("Computation elective \u2014 1 course, 3 credits")
    d.table(["Course", "Title", "What you build"],
            [["CSCE 735", "Parallel Computing",
              "GPU compute kernels: a parallel BVH builder and a compute-"
              "shader particle system, profiled and optimised."]],
            widths=[0.13, 0.26, 0.61])

    d.h2("Capstone \u2014 UC 691")
    d.p("A sustained research-and-build project spanning Semesters 3 and 4, "
        "carried out in a real engine codebase. The deliverable is a working "
        "system, a written technical report in the format of a graphics "
        "conference paper, and a recorded demonstration. This is the artifact "
        "that stands in for the credential.")

    d.pagebreak()
    d.h1("4 &nbsp; Four-semester sequence")
    d.p("Each semester is fifteen weeks: thirteen teaching modules plus two "
        "weeks for projects and review. Three courses at a time is a full "
        "load at roughly 25\u201335 hours per week. At half pace \u2014 "
        "one or two courses per term \u2014 the program takes three years "
        "instead of two, and that is a perfectly good way to do it.")
    rows = []
    for sem, label in [("S1", "Semester 1 \u2014 Foundations"),
                       ("S2", "Semester 2 \u2014 Systems &amp; geometry"),
                       ("S3", "Semester 3 \u2014 Light &amp; motion"),
                       ("S4", "Semester 4 \u2014 Perception &amp; parallelism")]:
        courses = [f"<b>{c}</b> {t}" for c, t, s in CORE + TRACK + ELECT
                   if s == sem]
        extra = ""
        if sem == "S3":
            extra = "<br/><i>Capstone begins: literature review and proposal.</i>"
        if sem == "S4":
            extra = "<br/><i>Capstone: implementation, report, demonstration.</i>"
        rows.append([label, "<br/>".join(courses) + extra])
    d.table(["Semester", "Courses"], rows, widths=[0.28, 0.72])

    d.callout("The through-line", [
        "Semester 1 gets triangles on screen and teaches you to reason about "
        "cost. Semester 2 gives you the geometry to feed the renderer and the "
        "engineering discipline to keep it alive. Semester 3 replaces "
        "approximations with physics \u2014 real light transport, real "
        "dynamics. Semester 4 closes the loop to human perception and to the "
        "parallel hardware that makes any of it real time.",
        "By the end you do not have twelve projects. You have one engine, and "
        "you understand every layer of it.",
    ], color=None)

    d.h1("5 &nbsp; How each course is delivered")
    d.p("Every course in this program ships as a folder containing four "
        "kinds of document. The slide decks and notes are original material "
        "written for this program; the resource map points at the free "
        "university courseware that covers the same ground in a different "
        "voice.")
    d.table(["Document", "What it is", "How to use it"],
            [["<b>Syllabus</b> (PDF)",
              "Learning outcomes, the thirteen-module schedule, projects, and "
              "the assessment standard.",
              "Read once at the start of the course; revisit at each project "
              "deadline."],
             ["<b>Resource map</b> (PDF)",
              "Module-by-module mapping onto free lectures, books, and "
              "problem sets, with specific lecture numbers where possible.",
              "This is your lecture hall. Watch the mapped lecture, then read "
              "the module notes."],
             ["<b>Module slides</b> (PPTX)",
              "One deck per module \u2014 the lecture, in the form you would "
              "see it in a classroom. Editable.",
              "Work through before or after the external lecture. Speaker "
              "notes carry the argument the slide compresses."],
             ["<b>Module notes</b> (PDF)",
              "A dense written treatment with derivations, worked examples, "
              "code, exercises, and a self-check.",
              "The reference you return to. Do the exercises \u2014 they are "
              "the assessment."]],
            widths=[0.17, 0.44, 0.39])

    d.h2("Assessment without a registrar")
    d.p("Nobody is going to grade you, so the standard has to be mechanical "
        "and honest. A module is complete when all three hold:")
    d.bullets([
        "<b>The code runs</b> and produces the output the module specifies "
        "\u2014 an image, a measurement, a passing test.",
        "<b>The self-check is answered from memory</b>, in writing, without "
        "looking at the notes. Writing it down is not optional; recognition "
        "feels like knowledge and is not.",
        "<b>You can explain the failure modes</b> \u2014 what breaks the "
        "method, and what you would reach for instead.",
    ], numbered=True)
    d.p("A course is complete when its projects are in the portfolio with "
        "written notes on what was hard. Keep the portfolio in public version "
        "control from day one. In this field the repository <i>is</i> the "
        "transcript, and it is a better one.")

    d.pagebreak()
    d.h1("6 &nbsp; Sources and licensing")
    d.p("Two categories of material appear in this program, under different "
        "terms. The distinction matters, so it is stated plainly.")
    d.table(["Material", "Origin", "Terms"],
            [["Slides, notes, syllabi, this handbook",
              "Written originally for the University of Claude.",
              "<b>Free to copy, adapt, redistribute, and sell.</b> No "
              "attribution required. No rights reserved."],
             ["Linked courses, books, lectures, labs",
              "MIT OCW, Stanford, CMU, Berkeley, ETH, edX, and individual "
              "authors who published them free.",
              "<b>Each remains under its own licence.</b> Linked, never "
              "reproduced. Read each site's terms before redistributing "
              "anything from it."]],
            widths=[0.26, 0.34, 0.40])

    d.h2("Student-supplied sources")
    d.p("The following were nominated for inclusion and are mapped into the "
        "curriculum at the courses indicated:")
    d.bullets([
        "UC San Diego CSE167x Computer Graphics (edX) \u2014 <i>CSCE 641</i>",
        "MIT 6.5830 Database Systems, Fall 2023 \u2014 <i>CSCE 608</i>",
        "MIT 6.S081 Operating System Engineering, 2020 \u2014 <i>CSCE 611</i>",
        "MIT 6.824 / 6.5840 Distributed Systems \u2014 <i>CSCE 662, 678</i>",
        "MIT 6.034 Artificial Intelligence, Fall 2010 \u2014 <i>CSCE 625</i>",
        "MIT 6.S191 Introduction to Deep Learning \u2014 <i>CSCE 636</i>",
        "MIT 6.006 Introduction to Algorithms, Spring 2020 \u2014 <i>CSCE 629</i>",
        "MIT 6.004 / MITx 6.004.1x Computation Structures \u2014 <i>CSCE 614</i>",
        "MIT 6.1200J Mathematics for Computer Science \u2014 <i>prerequisite</i>",
        "Stanford CS145 Introduction to Databases (archived) \u2014 <i>CSCE 603</i>",
        "Stanford CS144 Introduction to Computer Networking \u2014 <i>CSCE 612</i>",
        "Stanford CS229 Machine Learning \u2014 <i>CSCE 633</i>",
        "Stanford CS231n CNNs for Visual Recognition \u2014 <i>CSCE 636</i>",
        "UC Berkeley CS287 Advanced Robotics \u2014 <i>CSCE 635, 752</i>",
        "ETH Z\u00fcrich \u2014 Onur Mutlu, Computer Architecture \u2014 <i>CSCE 614</i>",
        "RIT Cybersecurity Fundamentals (edX) \u2014 <i>CSCE 701</i>",
        "Harvard CS50 and CS50 AI with Python \u2014 <i>CSCE 706, 708, 625</i>",
        "Neso Academy, Compiler Design \u2014 <i>CSCE 605</i>",
        "OSSU Open Source Computer Science \u2014 <i>general reference</i>",
    ])
    d.p("Two further nominated sources are curricula rather than courses "
        "\u2014 " + link("https://github.com/ossu/computer-science",
                         "OSSU Open Source Computer Science") + " and "
        + link("https://www.mrcomputerscience.com/",
               "mrcomputerscience.com") + " \u2014 and are worth reading "
        "alongside this handbook as alternative degree structures. The "
        "breadth-requirement model used here follows the common American "
        "graduate pattern of core breadth plus a declared specialisation.")

    d.h1("7 &nbsp; Where to begin")
    d.bullets([
        "Verify the three prerequisites honestly. Fix gaps now, not in week 6.",
        "Open <i>Courses/CSCE641-Computer-Graphics/</i> and read the syllabus.",
        "Create the portfolio repository. First commit before first lecture.",
        "Start Module 1. Build something that draws a triangle by week 2.",
    ], numbered=True)
    return d.save(os.path.join(OUT, "UC-MSCS-Program-Handbook.pdf"))


# ---------------------------------------------------------------- catalog
def catalog():
    d = Doc("Free-Resource Catalog",
            "Every course in the CSCE graduate catalog, mapped to open "
            "courseware, free books, and public lecture recordings",
            course="Catalog Map",
            kicker="UNIVERSITY OF CLAUDE \u00b7 COMPLETE CATALOG MAP")

    d.callout("How to read this", [
        "Each entry gives the course, a one-line statement of what the "
        "subject actually is, and the best freely available ways to learn it.",
        "Every link is free: open courseware, an author-released book, a "
        "public lecture recording, or a free-audit MOOC. Nothing here "
        "requires payment. Resources remain under their own licences.",
        f"<b>{len(CATALOG)} courses &middot; "
        f"{sum(len(c[3]) for c in CATALOG)} resources.</b> Courses in the "
        "Graphics &amp; Game Engines degree plan are marked \u25b6.",
    ])

    plan = {c for c, _, _ in CORE + TRACK + ELECT}
    rows = []
    for code, title, gist, res in CATALOG:
        mark = "\u25b6 " if code in plan else ""
        links = "<br/>".join(
            "\u00b7 " + link(u, lbl) for lbl, u in res)
        rows.append([f"<b>{mark}{code}</b><br/>{title}",
                     f"<i>{gist}</i><br/><br/>{links}"])
    d.table(["Course", "What it is, and where to learn it free"],
            rows, widths=[0.24, 0.76])
    return d.save(os.path.join(OUT, "Free-Resource-Catalog.pdf"))


if __name__ == "__main__":
    print(handbook())
    print(catalog())
