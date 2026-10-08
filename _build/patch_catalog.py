# -*- coding: utf-8 -*-
"""Fold the student-supplied source list into the catalog. Asserts every hit."""
import io

P = "content/catalog.py"
s = io.open(P, encoding="utf-8").read()

EDITS = [
    # CSCE 641 — UCSD CSE167x
    ('  ("Scratchapixel — from-scratch graphics", "https://www.scratchapixel.com/")]),',
     '  ("UC San Diego CSE167x Computer Graphics (edX, free audit)", "https://www.edx.org/learn/computer-graphics/the-university-of-california-san-diego-computer-graphics"),\n'
     '  ("Scratchapixel — from-scratch graphics", "https://www.scratchapixel.com/")]),'),

    # CSCE 701 — RIT Cybersecurity Fundamentals
    ('  ("SEED Labs — free hands-on security labs", "https://seedsecuritylabs.org/")]),',
     '  ("RIT Cybersecurity Fundamentals (edX, free audit)", "https://www.edx.org/learn/cybersecurity/rochester-institute-of-technology-cybersecurity-fundamentals"),\n'
     '  ("SEED Labs — free hands-on security labs", "https://seedsecuritylabs.org/")]),'),

    # CSCE 608 — MIT 6.5830
    ('  ("Database Internals / readings list", "https://www.redbook.io/")]),',
     '  ("MIT 6.5830 Database Systems, Fall 2023 (OCW)", "https://dsg.csail.mit.edu/6.5830/"),\n'
     '  ("Database Internals / readings list", "https://www.redbook.io/")]),'),

    # CSCE 603 — Stanford CS145 archive
    ('  ("PostgreSQL Tutorial", "https://www.postgresqltutorial.com/")]),',
     '  ("Stanford CS145 Introduction to Databases (archived)", "https://web.archive.org/web/2017/http://web.stanford.edu/class/cs145/"),\n'
     '  ("PostgreSQL Tutorial", "https://www.postgresqltutorial.com/")]),'),

    # CSCE 611 — 6.S081 2020 + OSSU
    ('  ("Berkeley CS162 (free lectures)", "https://cs162.org/")]),',
     '  ("MIT 6.S081 Operating System Engineering, 2020 (lecture video + labs)", "https://pdos.csail.mit.edu/6.S081/2020/schedule.html"),\n'
     '  ("Berkeley CS162 (free lectures)", "https://cs162.org/")]),'),

    # CSCE 636 — MIT 6.S191
    ('  ("fast.ai Practical Deep Learning", "https://course.fast.ai/")]),',
     '  ("MIT 6.S191 Introduction to Deep Learning (free, annual)", "https://introtodeeplearning.com/"),\n'
     '  ("fast.ai Practical Deep Learning", "https://course.fast.ai/")]),'),

    # CSCE 605 — Neso Academy
    ('  ("LLVM Kaleidoscope tutorial", "https://llvm.org/docs/tutorial/")]),',
     '  ("Neso Academy, Compiler Design (free video series)", "https://www.youtube.com/playlist?list=PLBlnK6fEyqRjT3oJxFXRgjPNzeS-LFY-q"),\n'
     '  ("LLVM Kaleidoscope tutorial", "https://llvm.org/docs/tutorial/")]),'),

    # CSCE 614 — MIT 6.004 + 6.004.1x
    ('  ("Berkeley CS152/CS252", "https://inst.eecs.berkeley.edu/~cs152/")]),',
     '  ("MIT 6.004 Computation Structures (OCW, Spring 2017)", "https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/"),\n'
     '  ("MITx 6.004.1x Computation Structures: Digital Circuits (edX)", "https://www.edx.org/learn/computer-programming/massachusetts-institute-of-technology-computation-structures-1-digital-circuits"),\n'
     '  ("Berkeley CS152/CS252", "https://inst.eecs.berkeley.edu/~cs152/")]),'),

    # CSCE 629 — MIT 6.006
    ('  ("Tim Roughgarden, Algorithms Illuminated (free lectures)", "https://www.algorithmsilluminated.org/")]),',
     '  ("MIT 6.006 Introduction to Algorithms, Spring 2020 (OCW, full video)", "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"),\n'
     '  ("Tim Roughgarden, Algorithms Illuminated (free lectures)", "https://www.algorithmsilluminated.org/")]),'),

    # CSCE 625 — CS50 AI
    ('  ("MIT 6.034 — Patrick Winston lectures (OCW)", "https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/")]),',
     '  ("MIT 6.034 — Patrick Winston lectures (OCW)", "https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/"),\n'
     '  ("Harvard CS50\'s Introduction to AI with Python (free)", "https://cs50.harvard.edu/ai/")]),'),

    # CSCE 635 / 752 — Berkeley CS287
    ('  ("ROS 2 tutorials", "https://docs.ros.org/en/rolling/Tutorials.html")]),',
     '  ("UC Berkeley CS287 Advanced Robotics — Pieter Abbeel (free)", "https://people.eecs.berkeley.edu/~pabbeel/cs287-fa19/"),\n'
     '  ("ROS 2 tutorials", "https://docs.ros.org/en/rolling/Tutorials.html")]),'),
]

for old, new in EDITS:
    assert s.count(old) == 1, f"NO/AMBIGUOUS MATCH ({s.count(old)}): {old[:70]}"
    s = s.replace(old, new)

# New foundations entry: discrete math prerequisite
MATH = '''
("UC MATH 600", "Mathematics for Computer Science (program prerequisite)",
 "Proof technique, combinatorics, graphs, and discrete probability — the language every later course assumes.",
 [("MIT 6.1200J / 6.042J Mathematics for Computer Science (OCW, full video)", "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/"),
  ("MIT 6.1200J current lecture series", "https://www.youtube.com/watch?v=L3LMbpZIKhQ"),
  ("Lehman, Leighton & Meyer, Mathematics for CS (free book)", "https://people.csail.mit.edu/meyer/mcs.pdf")]),

("UC LINA 600", "Linear Algebra for Graphics (program prerequisite)",
 "Vectors, matrices, bases, eigen-decomposition, and projections — the entire vocabulary of the graphics pipeline.",
 [("MIT 18.06 Linear Algebra — Gilbert Strang (OCW, full video)", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/"),
  ("3Blue1Brown, Essence of Linear Algebra (free video)", "https://www.3blue1brown.com/topics/linear-algebra"),
  ("Immersive Math — interactive linear algebra (free)", "http://immersivemath.com/ila/")]),
'''
anchor = '# --- Core systems and theory ----------------------------------------------'
assert s.count(anchor) == 1
s = s.replace(anchor, MATH.strip() + "\n\n" + anchor)

io.open(P, "w", encoding="utf-8").write(s)
print("catalog patched OK")
