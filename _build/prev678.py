# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preview import pdf_png, pptx_png
C = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "Courses", "CSCE678-Distributed-Systems-and-Cloud-Computing")
print("\n".join(pdf_png(os.path.join(C, r"Notes\M01-Partial-Failure.pdf"),
                        pages=(0, 1), tag="678m01")))
print("\n".join(pptx_png(os.path.join(C, r"Slides\M11-Trust-Cheating-and-Fairness.pptx"))))
