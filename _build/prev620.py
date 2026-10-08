# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preview import pdf_png, pptx_png
C = r"C:\Users\csant\ClaudeU\Courses\CSCE620-Computational-Geometry"
print("\n".join(pdf_png(os.path.join(C, "Syllabus.pdf"), pages=(0,), tag="620syl")))
print("\n".join(pdf_png(os.path.join(C, r"Notes\M02-Exact-and-Adaptive-Predicates.pdf"),
                        pages=(0, 1), tag="620m02")))
print("\n".join(pptx_png(os.path.join(C, r"Slides\M01-Geometry-a-Machine-Can-Believe.pptx"))))
