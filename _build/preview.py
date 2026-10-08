"""Render PPTX (via PowerPoint COM) and PDF (via PyMuPDF) to PNG for review."""
import os
import subprocess
import sys
import glob
import tempfile

TMP = os.path.join(tempfile.gettempdir(), "uc-preview")


def pdf_png(pdf, pages=(0,), zoom=1.5, tag=None):
    import pymupdf
    os.makedirs(TMP, exist_ok=True)
    tag = tag or os.path.splitext(os.path.basename(pdf))[0]
    out = []
    d = pymupdf.open(pdf)
    for i in pages:
        if i >= len(d):
            continue
        p = d[i].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
        f = os.path.join(TMP, f"{tag}_p{i + 1}.png")
        p.save(f)
        out.append(f)
    d.close()
    return out


def pptx_png(pptx, slides=None, tag=None):
    tag = tag or os.path.splitext(os.path.basename(pptx))[0]
    outdir = os.path.join(TMP, tag)
    os.makedirs(outdir, exist_ok=True)
    for f in glob.glob(os.path.join(outdir, "*.png")):
        os.remove(f)
    ps = f'''
$ErrorActionPreference = "Stop"
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open("{pptx}", $true, $false, $false)
$pres.SaveCopyAs("{outdir}\\s.png", 18)
$pres.Close()
$app.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($app) | Out-Null
Write-Output "done"
'''
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive",
                        "-Command", ps], capture_output=True, text=True)
    if "done" not in r.stdout:
        print("PPTX render failed:", r.stdout[-800:], r.stderr[-800:])
        return []
    found = {os.path.normcase(f): f for f in
             glob.glob(os.path.join(outdir, "**", "*.png"), recursive=True)}
    files = sorted(found.values(),
                   key=lambda p: int("".join(c for c in
                                             os.path.basename(p)
                                             if c.isdigit()) or 0))
    if slides:
        files = [files[i] for i in slides if i < len(files)]
    return files


if __name__ == "__main__":
    kind = sys.argv[1]
    path = sys.argv[2]
    idx = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0]
    fs = pptx_png(path, idx) if kind == "pptx" else pdf_png(path, idx)
    for f in fs:
        print(f)
