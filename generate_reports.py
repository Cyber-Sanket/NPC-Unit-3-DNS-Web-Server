# -*- coding: utf-8 -*-
"""
generate_reports.py
Master report compiler for NPC Unit 3 practical assignment.
Executes both PDF (ReportLab) and DOCX (python-docx) report generators for Sanket Aher.
"""

import sys
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    print("=" * 70)
    print("NPC UNIT 3: MASTER REPORT COMPILER")
    print("Candidate: Sanket Aher (PRN: 2125UCSM1080) | Sanjivani University")
    print("=" * 70)

    # 1. Check placeholders / screenshots
    print("\n[1/3] Checking screenshot assets in 'screenshots/'...")
    screenshots_dir = os.path.join(HERE, "screenshots")
    if os.path.exists(screenshots_dir):
        files = [f for f in os.listdir(screenshots_dir) if f.endswith(".png")]
        print(f"Found {len(files)} screenshot image(s) in {screenshots_dir}.")
    else:
        print("Warning: screenshots directory not found.")

    # 2. Build PDF Report
    print("\n[2/3] Compiling 19-Page Academic PDF Report via ReportLab...")
    try:
        from build_pdf import generate_pdf_report
        generate_pdf_report()
        print("-> SUCCESS: NPC_Unit_3_Sanket_Aher.pdf compiled successfully.")
    except Exception as e:
        print(f"-> ERROR in PDF generation: {e}")
        return 1

    # 3. Build DOCX Report
    print("\n[3/3] Compiling Matching Academic Word (.docx) Report via python-docx...")
    try:
        from build_docx import build_docx_report
        build_docx_report()
        print("-> SUCCESS: NPC_Unit_3_Sanket_Aher.docx compiled successfully.")
    except Exception as e:
        print(f"-> ERROR in DOCX generation: {e}")
        return 1

    print("\n" + "=" * 70)
    print("ALL DELIVERABLES COMPILED SUCCESSFULLY!")
    print("- PDF Report:  NPC_Unit_3_Sanket_Aher.pdf")
    print("- Word Report: NPC_Unit_3_Sanket_Aher.docx")
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
