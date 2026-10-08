# -*- coding: utf-8 -*-
"""Build the continuation record: Semesters 5-12, the 24 post-degree courses."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "content"))

from uc import Doc
from make_index import main as build_index

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "00_Program")

_ONES = ("zero one two three four five six seven eight nine ten eleven "
         "twelve thirteen fourteen fifteen sixteen seventeen eighteen "
         "nineteen").split()
_TENS = ("", "", "twenty", "thirty", "forty", "fifty", "sixty",
         "seventy", "eighty", "ninety")


def words(n):
    """Small counts spelled out, to match the document's voice."""
    if n < 20:
        return _ONES[n]
    if n < 100:
        t, r = divmod(n, 10)
        return _TENS[t] + ("-" + _ONES[r] if r else "")
    return str(n)

SEMESTERS = [
    ("5", "Engine internals",
     [("CSCE 620", "Computational Geometry"),
      ("CSCE 605", "Compiler Design"),
      ("CSCE 678", "Distributed Systems and Cloud Computing")],
     "The three subjects an engine actually runs on once it stops being "
     "one program on one machine: <b>the geometry underneath every "
     "spatial structure, the compiler underneath every shader and "
     "script, and the distribution underneath every build farm and "
     "multiplayer session.</b>"),
    ("6", "Learning foundations",
     [("CSCE 633", "Machine Learning"),
      ("CSCE 636", "Deep Learning"),
      ("CSCE 669", "Computational Optimization")],
     "Learning from data, taken in the order that makes it "
     "tractable: <b>the statistical framing first, the architectures "
     "second, and the optimisation that both of them are instances of "
     "third.</b>"),
    ("7", "Perception and agents",
     [("CSCE 753", "Computer Vision"),
      ("CSCE 625", "Artificial Intelligence"),
      ("CSCE 642", "Deep Reinforcement Learning")],
     "Systems that take in the world and act in it \u2014 <b>which is "
     "the inverse of the rendering problem this track spent four "
     "semesters on</b>, and reads very differently once you have "
     "written a renderer."),
    ("8", "Theory",
     [("CSCE 627", "Theory of Computability"),
      ("CSCE 637", "Complexity Theory"),
      ("CSCE 658", "Randomized Algorithms")],
     "What cannot be computed, what can be computed only slowly, and "
     "what randomness buys you \u2014 <b>placed after the applied "
     "semesters deliberately</b>, because the negative results mean "
     "more once you have tried to build the things they rule out."),
    ("9", "Security",
     [("CSCE 701", "Foundations of Cybersecurity"),
      ("CSCE 711", "Applied Cryptography"),
      ("CSCE 713", "Software Security")],
     "All three written defensively: how systems fail, so that you can "
     "build ones that do not. <b>All three converge on the same "
     "conclusion</b> \u2014 make the defect unexpressible rather than "
     "training people not to write it: safe defaults, misuse-resistant "
     "APIs, and types that make the bug impossible to state."),
    ("10", "Data and language",
     [("CSCE 638", "Natural Language Processing"),
      ("CSCE 676", "Data Mining"),
      ("CSCE 670", "Information Retrieval")],
     "Three subjects that all run on a proxy. <b>All three converge on "
     "the proxy problem</b> \u2014 a metric standing in for quality, a "
     "score standing in for a pattern being real, a click standing in "
     "for relevance \u2014 and on what happens once the proxy becomes "
     "the target."),
    ("11", "Human-centred computing",
     [("CSCE 671", "Human-Computer Interaction"),
      ("CSCE 679", "Data Visualization"),
      ("CSCE 632", "Accessible Computing")],
     "<b>All three replace a judgement about taste with a cheap "
     "measurement</b> \u2014 five participants attempting a real task, "
     "the measured ranking of the visual channels, and the actual "
     "assistive technology \u2014 and <b>all three correct the same "
     "error</b>: designing for an imagined user who resembles the "
     "designer."),
    ("12", "Frontiers",
     [("CSCE 640", "Quantum Algorithms"),
      ("CSCE 628", "Computational Biology"),
      ("CSCE 717", "Algorithmic Game Theory")],
     "<b>In all three the computational model comes from outside "
     "computer science and is not yours to choose</b> \u2014 physics, "
     "biology, and self-interested agents \u2014 and <b>in all three "
     "the true state is unobservable</b>: the amplitudes cannot be "
     "read, the ground truth is not available, and the valuations are "
     "private."),
]


def continuation():
    # Counts come from whatever is actually built, so this document cannot
    # drift the way a typed-in figure does.
    ix = build_index()
    n_courses = ix["stats"]["courses_built"]
    n_modules = ix["stats"]["modules"]
    cont = [c for c in ix["courses"] if c["phase"] == "continuation"]
    n_built = sum(1 for c in cont if c["built"])
    sems_built = sorted({c["sem"] for c in cont if c["built"]})
    sems_plan = sorted({c["sem"] for c in cont if not c["built"]})
    span = "%d through %d" % (sems_built[0], sems_built[-1])

    d = Doc("The Continuation",
            "Semesters %s \u00b7 %s further courses "
            "\u00b7 built after the degree plan was complete"
            % (span, words(n_built)),
            course="Continuation Record",
            kicker="UNIVERSITY OF CLAUDE \u00b7 CONTINUATION RECORD "
                   "\u00b7 2026")

    d.callout("What this document is", [
        "The twelve-course MS described in the Program Handbook is a "
        "complete degree plan, and Semesters 1 through 4 are that plan. "
        "This document records the %s courses built after it."
        % words(n_built),
        "They are <b>not part of the degree</b> and are not required "
        "for it. They were written because the curriculum kept pointing "
        "at subjects it could not reach in four semesters, and because "
        "the cross-references between courses are what make the program "
        "read as one thing rather than as %s." % words(n_courses),
        "Same terms as everything else here: <b>every word written for "
        "this program is original and free to copy, adapt, and "
        "redistribute.</b> External courses are linked, never "
        "reproduced, and remain under their own licences. The "
        "University of Claude is not accredited and awards nothing.",
    ])

    d.h1("1 &nbsp; How the continuation is organised")
    d.p("Each semester after the fourth is <b>three courses chosen to "
        "converge</b>. They are not a list of electives: within a "
        "semester the three courses arrive at the same conclusion from "
        "different directions, and the convergence is stated explicitly "
        "in each one's final module.")
    d.p("That structure is the reason to take them in threes rather "
        "than individually. <b>A conclusion reached once is a claim; "
        "the same conclusion reached three times \u2014 from security, "
        "from statistics, and from design \u2014 is a result you "
        "keep.</b>")

    d.h2("Reading order")
    d.bullets([
        "<b>Semesters 5 through 8 are roughly ordered.</b> The later "
        "ones assume the earlier: Semester 7 uses Semester 6 heavily, "
        "and Semester 8 is deliberately placed after the applied work "
        "rather than before it.",
        "<b>Semesters 9 through 12 are largely independent of each "
        "other</b> and may be taken in any order, though each assumes "
        "Semesters 1 through 8.",
        "<b>Every course cross-references the others by module and "
        "section</b> \u2014 <i>CSCE nnn Module nn &sect;n</i> \u2014 so "
        "a forward reference is a pointer rather than a dependency, and "
        "nothing breaks if you read out of order.",
    ])

    d.pagebreak()
    d.h1("2 &nbsp; The eight semesters")
    for num, theme, courses, blurb in SEMESTERS:
        d.h2("Semester %s &mdash; %s" % (num, theme))
        d.table(["Course", "Title"],
                [["<b>%s</b>" % c, t] for c, t in courses],
                widths=[0.22, 0.78])
        d.p(blurb)

    d.pagebreak()
    d.h1("3 &nbsp; What every course does the same way")
    d.p("The %s courses share a structure, and it is worth stating "
        "plainly because it is what makes them usable without an "
        "instructor." % words(n_courses))
    d.bullets([
        "<b>Thirteen modules and two project weeks.</b> Each module is "
        "a slide deck and a set of lecture notes, and <b>the notes say "
        "more than the slides do rather than less</b>.",
        "<b>Every module ends in exercises you can actually run</b>, "
        "and a self-check list that is a list of questions rather than "
        "a summary.",
        "<b>Two projects per course</b>, one at the midpoint and one at "
        "the end, each with its requirements and its done-criteria "
        "stated separately \u2014 because <b>the second list is what "
        "distinguishes finished from submitted</b>.",
        "<b>Resources are linked, never reproduced</b>, and each link "
        "says which section it is for and why it is worth the time.",
        "<b>And every course closes on the same rule</b>, restated in "
        "that course's own vocabulary: <i>state what you measured, "
        "state what you assumed, and never claim more than you "
        "established.</i>",
    ])

    d.h1("4 &nbsp; The closing rule")
    d.p("That last point is the program's one piece of doctrine, and "
        "the final module of every course is an application of it. In "
        "CSCE 679 it is a five-clause figure caption. In CSCE 632 it is "
        "an accessibility statement with its exceptions named. In "
        "CSCE 640 it is the problem, the baseline, and the machine. In "
        "CSCE 628 it is the methods section and the artefact account. "
        "In CSCE 717 it is the solution concept, the agent model, and "
        "the impossibility you chose to live with.")
    d.p("<b>They are the same instruction.</b> A result is a claim "
        "about a procedure, and the procedure is the part a reader can "
        "check. Stating it is not modesty \u2014 it is the difference "
        "between work somebody can build on and work they can only "
        "believe.")

    d.h1("5 &nbsp; Status")
    d.p("<b>%d courses; %d modules.</b> The twelve-course MS in "
        "Semesters 1 through 4, its two prerequisites in Semester 0, and "
        "the %s-course continuation in Semesters %s. Every local link in "
        "the repository resolves, and every external link is free to "
        "access." % (n_courses, n_modules, words(n_built), span))
    if sems_plan:
        d.p("<b>Semesters %d through %d are planned and are not "
            "built.</b> They appear in the repository index and in the "
            "study app as unbuilt, and the catalog maps every one of "
            "them to free lectures and books, so any of them can be "
            "written later without disturbing what is here. <b>Nothing "
            "in Semesters 0 through %d depends on them.</b>"
            % (sems_plan[0], sems_plan[-1], sems_built[-1]))
    d.p("The README at the repository root is generated from the built "
        "material and is the current index. <b>If a course is listed "
        "there, its slides and notes exist</b>; if it is marked as not "
        "yet built, they do not.")
    return d.save(os.path.join(OUT, "UC-Continuation-Record.pdf"))


if __name__ == "__main__":
    print(continuation())
