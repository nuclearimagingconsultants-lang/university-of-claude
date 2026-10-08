# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preview import pdf_png, pptx_png
C = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "Courses", "CSCE605-Compiler-Design")
print("\n".join(pdf_png(os.path.join(C, r"Notes\M07-Intermediate-Representation-and-SSA.pdf"),
                        pages=(1, 2), tag="605m07")))
print("\n".join(pptx_png(os.path.join(C, r"Slides\M13-Shader-Compilation-Testing-and-Shipping.pptx"))))
