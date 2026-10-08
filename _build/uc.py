"""
University of Claude — document engine.

Shared theme + builders for course slide decks (PPTX) and lecture notes (PDF).
All content authored originally for this program. No third-party course
material is reproduced; external courses are referenced by link only.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, KeepTogether, ListFlowable, ListItem, HRFlowable, PageBreak,
)

# ----------------------------------------------------------------------------
# Theme
# ----------------------------------------------------------------------------

INK      = RGBColor(0x14, 0x19, 0x24)   # near-black navy, title/section fields
INK_SOFT = RGBColor(0x24, 0x2C, 0x3B)
PAPER    = RGBColor(0xF8, 0xF6, 0xF2)   # warm off-white body background
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
CRIMSON  = RGBColor(0xB0, 0x3F, 0x2B)   # primary accent
TEAL     = RGBColor(0x1F, 0x6B, 0x68)   # secondary accent
GOLD     = RGBColor(0xC2, 0x9B, 0x3F)   # tertiary accent / wordmark
SLATE    = RGBColor(0x3C, 0x45, 0x55)   # body text on paper
MUTED    = RGBColor(0x79, 0x82, 0x90)   # captions, metadata
CODE_BG  = RGBColor(0x1B, 0x21, 0x2D)
CODE_FG  = RGBColor(0xE4, 0xE8, 0xEF)

HEAD_FONT = "Georgia"
BODY_FONT = "Calibri"
CODE_FONT = "Consolas"

LF_CODE = 1.32   # calibrated: line_spacing 1.05 x ~1.2 PPT factor
LF_BODY = 1.48   # calibrated: line_spacing 1.22 x ~1.2 PPT factor
SLIDE_W = 13.333
SLIDE_H = 7.5

# reportlab equivalents
R_INK     = colors.HexColor("#141924")
R_CRIMSON = colors.HexColor("#B03F2B")
R_TEAL    = colors.HexColor("#1F6B68")
R_GOLD    = colors.HexColor("#C29B3F")
R_SLATE   = colors.HexColor("#3C4555")
R_MUTED   = colors.HexColor("#798290")
R_RULE    = colors.HexColor("#D8D3C9")
R_PANEL   = colors.HexColor("#F2EFE8")
R_CODEBG  = colors.HexColor("#1B212D")

WORDMARK = "UNIVERSITY OF CLAUDE"

# ----------------------------------------------------------------------------
# Inline markup: slide text is authored with the same <b>/<i> markup as the
# PDF notes, so it must be parsed rather than printed literally.
# ----------------------------------------------------------------------------

import re as _re

# Slides take raw Unicode and notes take HTML entities, but authored text mixes
# them. Rather than police every call site, decode the full set the notes use:
# named below, numeric via _NUMENT_ANY in _inline. &amp; resolves LAST so that
# "&amp;times;" stays literal "&times;" instead of decoding twice.
_NAMED = {
    "lt": "<", "gt": ">", "nbsp": " ", "quot": '"', "apos": "'",
    "mdash": "—", "ndash": "–", "middot": "·",
    "hellip": "…", "bull": "•", "prime": "′",
    "Prime": "″", "deg": "°", "sect": "§",
    "copy": "©", "reg": "®", "trade": "™",
    "ldquo": "“", "rdquo": "”", "lsquo": "‘",
    "rsquo": "’",
    "rarr": "→", "larr": "←", "uarr": "↑",
    "darr": "↓", "harr": "↔", "rArr": "⇒",
    "lArr": "⇐", "hArr": "⇔",
    "minus": "−", "times": "×", "divide": "÷",
    "plusmn": "±", "le": "≤", "ge": "≥", "ne": "≠",
    "asymp": "≈", "equiv": "≡", "prop": "∝",
    "infin": "∞", "radic": "√", "part": "∂",
    "nabla": "∇", "sum": "∑", "prod": "∏",
    "int": "∫", "sdot": "⋅", "cup": "∪", "cap": "∩",
    "isin": "∈", "notin": "∉", "forall": "∀",
    "exist": "∃", "empty": "∅", "ang": "∠",
    "perp": "⊥", "sim": "∼", "cong": "≅",
    "frac12": "½", "frac14": "¼", "frac34": "¾",
    "sup1": "¹", "sup2": "²", "sup3": "³",
    "alpha": "α", "beta": "β", "gamma": "γ",
    "delta": "δ", "epsilon": "ε", "zeta": "ζ",
    "eta": "η", "theta": "θ", "iota": "ι",
    "kappa": "κ", "lambda": "λ", "mu": "μ",
    "nu": "ν", "xi": "ξ", "omicron": "ο",
    "pi": "π", "rho": "ρ", "sigmaf": "ς",
    "sigma": "σ", "tau": "τ", "upsilon": "υ",
    "phi": "φ", "chi": "χ", "psi": "ψ",
    "omega": "ω",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ",
    "Lambda": "Λ", "Xi": "Ξ", "Pi": "Π",
    "Sigma": "Σ", "Upsilon": "Υ", "Phi": "Φ",
    "Psi": "Ψ", "Omega": "Ω",
    "eacute": "é", "egrave": "è", "agrave": "à",
    "auml": "ä", "ouml": "ö", "uuml": "ü",
    "ccedil": "ç", "ntilde": "ñ", "oslash": "ø",
    "aring": "å", "szlig": "ß",
}
# Longest name first, so "&sup2;" is not shadowed by a shorter prefix.
_ENTITIES = [("&%s;" % k, v)
             for k, v in sorted(_NAMED.items(), key=lambda kv: -len(kv[0]))]
_ENTITIES.append(("&amp;", "&"))

_NUMENT_ANY = _re.compile(r"&#(\d{2,5});")
_TAG = _re.compile(r"</?(b|i|em|strong|code|tt|sub|super|sup)>", _re.I)


def _inline(text):
    """Split authored text into (segment, bold, italic, mono, baseline)."""
    out, bold, ital, mono, base, pos = [], 0, 0, 0, 0, 0
    for m in _TAG.finditer(text):
        seg = text[pos:m.start()]
        if seg:
            out.append((seg, bold > 0, ital > 0, mono > 0, base))
        tag = m.group(1).lower()
        close = m.group(0).startswith("</")
        d = -1 if close else 1
        if tag in ("b", "strong"):
            bold = max(0, bold + d)
        elif tag in ("i", "em"):
            ital = max(0, ital + d)
        elif tag == "sub":
            base += -1 * d
        elif tag in ("super", "sup"):
            base += 1 * d
        else:
            mono = max(0, mono + d)
        pos = m.end()
    if text[pos:]:
        out.append((text[pos:], bold > 0, ital > 0, mono > 0, base))
    res = []
    for seg, b, i, c, bl in out:
        seg = _NUMENT_ANY.sub(lambda m: chr(int(m.group(1))), seg)
        for ent, ch in _ENTITIES:
            seg = seg.replace(ent, ch)
        res.append((seg, b, i, c, bl))
    return res or [("", False, False, False, 0)]


def _plain(text):
    return "".join(s for s, _, _, _, _ in _inline(text))


# Uppercasing a label must not touch entity references or markup tags:
# HTML entity names are case-sensitive, so "&times;".upper() yields
# "&TIMES;", which no parser will decode and which then prints literally.
_KEEP_CASE_RE = _re.compile(r"<[^>]+>|&[#A-Za-z0-9]+;")


def _upper(text):
    out, last = [], 0
    for m in _KEEP_CASE_RE.finditer(text):
        out.append(text[last:m.start()].upper())
        out.append(m.group(0))
        last = m.end()
    out.append(text[last:].upper())
    return "".join(out)


# ----------------------------------------------------------------------------
# Sub/superscript normalisation for PDF.
#
# reportlab's built-in Type1 fonts (Times, Courier, Helvetica) have no glyphs
# for Unicode sub/superscript characters, and render them as black boxes.
# PPTX is unaffected (Calibri and Consolas have them), so this applies only
# to the PDF path. Runs of adjacent marks are grouped into one tag.
# ----------------------------------------------------------------------------

_SUB = {
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
    "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9",
    "₊": "+", "₋": "-", "₌": "=", "₍": "(", "₎": ")",
    "ₐ": "a", "ₑ": "e", "ₒ": "o", "ₓ": "x", "ₕ": "h",
    "ₖ": "k", "ₗ": "l", "ₘ": "m", "ₙ": "n", "ₚ": "p",
    "ₛ": "s", "ₜ": "t",
    "ᵢ": "i", "ᵣ": "r", "ᵤ": "u", "ᵥ": "v",
    "ᵦ": "&beta;", "ᵨ": "&rho;",
    "ᵩ": "&phi;", "ᵪ": "&chi;", "ᶻ": "z",
}
_SUP = {
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
    "⁺": "+", "⁻": "-", "⁼": "=", "⁽": "(", "⁾": ")",
    "ⁿ": "n", "ᶜ": "c", "ᵀ": "T", "ᵗ": "t",
}
_SUB_RE = _re.compile("[" + "".join(_SUB) + "]+")
_SUP_RE = _re.compile("[" + "".join(_SUP) + "]+")


_NUMENT_RE = _re.compile(r"&#(\d{2,5});")


def _subsup(text):
    # Source text writes these as numeric entities (&#8320;), so decode the
    # ones we know are sub/superscript marks before matching. Structural
    # entities (&amp;, &lt;, &gt;) and all others are left untouched.
    def _dec(m):
        ch = chr(int(m.group(1)))
        return ch if (ch in _SUB or ch in _SUP) else m.group(0)
    text = _NUMENT_RE.sub(_dec, text)

    text = _SUB_RE.sub(
        lambda m: "<sub>" + "".join(_SUB[c] for c in m.group(0)) + "</sub>",
        text)
    return _SUP_RE.sub(
        lambda m: "<super>" + "".join(_SUP[c] for c in m.group(0)) + "</super>",
        text)


# ----------------------------------------------------------------------------
# PPTX deck builder
# ----------------------------------------------------------------------------

class Deck:
    def __init__(self, course, course_title, module=None, module_title=None):
        self.course = course
        self.course_title = course_title
        self.module = module or ""
        self.module_title = module_title or ""
        self.prs = Presentation()
        self.prs.slide_width = Inches(SLIDE_W)
        self.prs.slide_height = Inches(SLIDE_H)
        self._blank = self.prs.slide_layouts[6]
        self.n = 0

    # -- primitives ---------------------------------------------------------

    def _slide(self):
        return self.prs.slides.add_slide(self._blank)

    def _rect(self, s, x, y, w, h, fill, line=None):
        shp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                 Inches(w), Inches(h))
        shp.shadow.inherit = False
        if fill is None:
            shp.fill.background()
        else:
            shp.fill.solid()
            shp.fill.fore_color.rgb = fill
        if line is None:
            shp.line.fill.background()
        else:
            shp.line.color.rgb = line
            shp.line.width = Pt(1)
        return shp

    def _text(self, s, x, y, w, h, runs, align=PP_ALIGN.LEFT,
              anchor=MSO_ANCHOR.TOP, line_spacing=1.0):
        """runs = list of dicts: text, size, bold, italic, color, font,
        space_before, space_after, bullet_level, align.

        `text` may contain inline <b>/<i>/<code> markup and HTML entities;
        these become separate runs rather than literal characters."""
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = 0
        tf.margin_top = tf.margin_bottom = 0
        first = True
        for r in runs:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.alignment = r.get("align", align)
            p.line_spacing = r.get("line_spacing", line_spacing)
            if r.get("space_before"):
                p.space_before = Pt(r["space_before"])
            if r.get("space_after"):
                p.space_after = Pt(r["space_after"])
            if r.get("level"):
                p.level = r["level"]
            for seg, bold, ital, mono, base in _inline(r["text"]):
                if not seg:
                    continue
                run = p.add_run()
                run.text = seg
                f = run.font
                f.name = CODE_FONT if mono else r.get("font", BODY_FONT)
                shrink = 0.92 if mono else 1.0
                if base:
                    shrink *= 0.72
                    run._r.get_or_add_rPr().set(
                        "baseline", "-25000" if base < 0 else "30000")
                f.size = Pt(r.get("size", 18) * shrink)
                f.bold = bool(r.get("bold", False) or bold)
                f.italic = bool(r.get("italic", False) or ital)
                f.color.rgb = r.get("color", SLATE)
        return tb

    def _footer(self, s, dark=False):
        c = MUTED if not dark else RGBColor(0x6E, 0x78, 0x8A)
        self.n += 1
        self._text(s, 0.62, SLIDE_H - 0.48, 9.0, 0.3, [{
            "text": f"{self.course} · {self.course_title}"
                    + (f"  —  {self.module}" if self.module else ""),
            "size": 9, "color": c}])
        self._text(s, SLIDE_W - 1.6, SLIDE_H - 0.48, 1.0, 0.3,
                   [{"text": str(self.n), "size": 9, "color": c}],
                   align=PP_ALIGN.RIGHT)

    # -- slide types --------------------------------------------------------

    def title_slide(self, subtitle=None, meta=None):
        s = self._slide()
        self._rect(s, 0, 0, SLIDE_W, SLIDE_H, INK)
        self._rect(s, 0, 0, 0.22, SLIDE_H, CRIMSON)
        self._text(s, 1.1, 0.95, 10.5, 0.4, [{
            "text": WORDMARK, "size": 13, "bold": True, "color": GOLD,
            "font": BODY_FONT}])
        self._text(s, 1.1, 1.55, 10.5, 0.5, [{
            "text": f"{self.course} — {self.course_title}",
            "size": 17, "color": RGBColor(0xA9, 0xB4, 0xC4),
            "font": BODY_FONT}])
        if self.module:
            self._text(s, 1.1, 2.35, 11.0, 0.45, [{
                "text": _upper(self.module), "size": 13, "bold": True,
                "color": TEAL, "font": BODY_FONT}])
        self._text(s, 1.1, 2.85, 11.2, 1.9, [{
            "text": self.module_title or self.course_title,
            "size": 44, "bold": True, "color": WHITE, "font": HEAD_FONT,
            "line_spacing": 1.05}])
        if subtitle:
            self._rect(s, 1.1, 4.95, 2.6, 0.045, CRIMSON)
            self._text(s, 1.1, 5.25, 10.4, 1.1, [{
                "text": subtitle, "size": 16, "italic": True,
                "color": RGBColor(0x9A, 0xA5, 0xB5), "line_spacing": 1.25}])
        self._text(s, 1.1, SLIDE_H - 0.85, 11.0, 0.35, [{
            "text": meta or "Original course material · free to copy, adapt, and share",
            "size": 10, "color": RGBColor(0x5E, 0x69, 0x7A)}])
        return s

    def section(self, label, title, blurb=None):
        s = self._slide()
        self._rect(s, 0, 0, SLIDE_W, SLIDE_H, INK_SOFT)
        self._rect(s, 0, 0, SLIDE_W, 0.16, GOLD)
        self._text(s, 1.1, 2.45, 11.0, 0.4, [{
            "text": _upper(label), "size": 13, "bold": True, "color": GOLD}])
        self._text(s, 1.1, 2.95, 11.0, 1.4, [{
            "text": title, "size": 36, "bold": True, "color": WHITE,
            "font": HEAD_FONT, "line_spacing": 1.1}])
        if blurb:
            self._text(s, 1.1, 4.35, 10.2, 1.2, [{
                "text": blurb, "size": 15, "color": RGBColor(0x9A, 0xA5, 0xB5),
                "line_spacing": 1.3}])
        self._footer(s, dark=True)
        return s

    def _head(self, s, title, kicker=None):
        self._rect(s, 0, 0, SLIDE_W, SLIDE_H, PAPER)
        y = 0.52
        if kicker:
            self._text(s, 0.62, y, 11.8, 0.3,
                       [{"text": _upper(kicker), "size": 10.5, "bold": True,
                         "color": CRIMSON}])
            y += 0.34
        self._text(s, 0.62, y, 12.1, 0.85,
                   [{"text": title, "size": 27, "bold": True, "color": INK,
                     "font": HEAD_FONT, "line_spacing": 1.08}])
        self._rect(s, 0.62, y + 0.92, 1.5, 0.035, CRIMSON)
        return y + 1.22

    def bullets(self, title, items, kicker=None, note=None, footnote=None):
        """items: list of (text, level) or plain strings."""
        s = self._slide()
        top = self._head(s, title, kicker)
        norm = [(i, 0) if isinstance(i, str) else i for i in items]
        avail = SLIDE_H - top - (1.05 if footnote else 0.7)
        size = 18.0
        while size > 11.0:
            # estimate wrapped height: chars-per-line scales with 1/size
            used = 0.0
            for txt, lv in norm:
                if txt == "":
                    used += 0.11
                    continue
                sz = size if lv == 0 else size - 2
                cpl = max(20, int((11.6 - 0.35 * lv) * 72.0 / (sz * 0.50)))
                rows = max(1, -(-len(_plain(txt)) // cpl))
                used += rows * sz * LF_BODY / 72.0 + (9 if lv == 0 else 5) / 72.0
            if used <= avail:
                break
            size -= 0.5
        else:
            print(f"  [OVERFLOW RISK] bullets: {title[:50]!r} "
                  f"needs {used:.2f}in, has {avail:.2f}in")
        runs = []
        for txt, lv in norm:
            if txt == "":
                runs.append({"text": " ", "size": 6})
                continue
            runs.append({
                "text": ("▪  " if lv == 0 else "–  ") + txt,
                "size": size if lv == 0 else size - 2,
                "bold": False,
                "color": SLATE if lv == 0 else MUTED,
                "level": lv,
                "space_after": 9 if lv == 0 else 5,
                "line_spacing": 1.22,
            })
        self._text(s, 0.78, top, 11.8, SLIDE_H - top - 1.0, runs)
        if footnote:
            self._text(s, 0.62, SLIDE_H - 0.95, 11.8, 0.4, [{
                "text": footnote, "size": 10.5, "italic": True,
                "color": MUTED}])
        self._footer(s)
        if note:
            s.notes_slide.notes_text_frame.text = note
        return s

    def two_col(self, title, lhead, litems, rhead, ritems, kicker=None,
                note=None):
        s = self._slide()
        top = self._head(s, title, kicker)
        h = SLIDE_H - top - 1.0
        for x, head, items, accent in ((0.62, lhead, litems, CRIMSON),
                                       (6.95, rhead, ritems, TEAL)):
            self._rect(s, x, top, 5.76, h, WHITE, line=RGBColor(0xE2, 0xDE, 0xD5))
            self._rect(s, x, top, 5.76, 0.05, accent)
            self._text(s, x + 0.3, top + 0.28, 5.2, 0.45,
                       [{"text": head, "size": 15, "bold": True, "color": INK,
                         "font": BODY_FONT}])
            norm = [(i, 0) if isinstance(i, str) else i for i in items]
            size = 14 if len(norm) <= 7 else 12.5
            runs = [{
                "text": ("▪  " if lv == 0 else "–  ") + t,
                "size": size if lv == 0 else size - 1.5,
                "color": SLATE if lv == 0 else MUTED,
                "level": lv, "space_after": 7, "line_spacing": 1.2,
            } for t, lv in norm]
            self._text(s, x + 0.3, top + 0.85, 5.2, h - 1.1, runs)
        self._footer(s)
        if note:
            s.notes_slide.notes_text_frame.text = note
        return s

    def code(self, title, code, lang=None, caption=None, kicker=None,
             note=None):
        s = self._slide()
        top = self._head(s, title, kicker)
        lines = code.strip("\n").split("\n")
        avail = SLIDE_H - top - (1.15 if caption else 0.75)
        # fit to the available height, and to the 11.5in text column width
        by_h = (avail - 0.34) * 72.0 / (len(lines) * LF_CODE)
        by_w = 11.5 * 72.0 / (max(len(l) for l in lines) * 0.553 or 1)
        size = max(7.5, min(14.0, by_h, by_w))
        if min(by_h, by_w) < 7.5:
            print(f"  [OVERFLOW RISK] code: {title[:50]!r} "
                  f"{len(lines)} lines, longest {max(len(l) for l in lines)} chars")
        h = min(avail, 0.34 + len(lines) * (size * LF_CODE / 72))
        self._rect(s, 0.62, top, 12.1, h, CODE_BG)
        if lang:
            self._text(s, 11.5, top + 0.12, 1.1, 0.3,
                       [{"text": lang, "size": 10, "color": GOLD,
                         "font": CODE_FONT}], align=PP_ALIGN.RIGHT)
        runs = [{"text": ln if ln else " ", "size": size, "font": CODE_FONT,
                 "color": CODE_FG, "line_spacing": 1.05} for ln in lines]
        self._text(s, 0.95, top + 0.2, 11.5, h - 0.3, runs)
        if caption:
            self._text(s, 0.62, min(top + h + 0.18, SLIDE_H - 0.95), 11.8, 0.5,
                       [{"text": caption, "size": 12.5, "italic": True,
                         "color": MUTED, "line_spacing": 1.2}])
        self._footer(s)
        if note:
            s.notes_slide.notes_text_frame.text = note
        return s

    def equations(self, title, eqs, caption=None, kicker=None, note=None):
        """eqs: list of (expr, gloss) — gloss may be None."""
        s = self._slide()
        top = self._head(s, title, kicker)
        y = top
        for expr, gloss in eqs:
            self._rect(s, 0.62, y, 12.1, 0.72, WHITE,
                       line=RGBColor(0xE2, 0xDE, 0xD5))
            self._rect(s, 0.62, y, 0.05, 0.72, TEAL)
            self._text(s, 0.95, y + 0.1, 11.5, 0.5,
                       [{"text": expr, "size": 17, "font": CODE_FONT,
                         "color": INK}], anchor=MSO_ANCHOR.MIDDLE)
            y += 0.78
            if gloss:
                self._text(s, 1.0, y - 0.04, 11.4, 0.42,
                           [{"text": gloss, "size": 12.5, "italic": True,
                             "color": MUTED, "line_spacing": 1.15}])
                y += 0.46
            y += 0.1
        if caption:
            self._text(s, 0.62, min(y + 0.1, SLIDE_H - 0.95), 11.8, 0.5,
                       [{"text": caption, "size": 12.5, "italic": True,
                         "color": MUTED, "line_spacing": 1.2}])
        self._footer(s)
        if note:
            s.notes_slide.notes_text_frame.text = note
        return s

    def table(self, title, header, rows, kicker=None, note=None, widths=None):
        s = self._slide()
        top = self._head(s, title, kicker)
        ncol = len(header)
        widths = widths or [12.1 / ncol] * ncol
        rowh = min(0.52, (SLIDE_H - top - 1.1) / (len(rows) + 1))
        x = 0.62
        for j, (hd, w) in enumerate(zip(header, widths)):
            self._rect(s, x, top, w, rowh, INK)
            self._text(s, x + 0.12, top + 0.06, w - 0.24, rowh,
                       [{"text": hd, "size": 12.5, "bold": True,
                         "color": WHITE}], anchor=MSO_ANCHOR.MIDDLE)
            x += w
        y = top + rowh
        for i, row in enumerate(rows):
            x = 0.62
            bg = WHITE if i % 2 == 0 else RGBColor(0xF1, 0xEE, 0xE8)
            for cell, w in zip(row, widths):
                self._rect(s, x, y, w, rowh, bg,
                           line=RGBColor(0xE2, 0xDE, 0xD5))
                self._text(s, x + 0.12, y + 0.04, w - 0.24, rowh,
                           [{"text": str(cell), "size": 11.5,
                             "color": SLATE, "line_spacing": 1.1}],
                           anchor=MSO_ANCHOR.MIDDLE)
                x += w
            y += rowh
        self._footer(s)
        if note:
            s.notes_slide.notes_text_frame.text = note
        return s

    def callout(self, title, body, kind="Key idea", kicker=None, note=None):
        s = self._slide()
        top = self._head(s, title, kicker)
        h = SLIDE_H - top - 1.1
        self._rect(s, 0.62, top, 12.1, h, WHITE,
                   line=RGBColor(0xE2, 0xDE, 0xD5))
        self._rect(s, 0.62, top, 0.07, h, GOLD)
        self._text(s, 1.1, top + 0.35, 11.2, 0.35,
                   [{"text": _upper(kind), "size": 11, "bold": True,
                     "color": GOLD}])
        lines = body if isinstance(body, list) else [body]
        runs = [{"text": t, "size": 19 if len(lines) <= 3 else 16,
                 "color": INK, "font": HEAD_FONT, "line_spacing": 1.35,
                 "space_after": 12} for t in lines]
        self._text(s, 1.1, top + 0.85, 11.0, h - 1.2, runs)
        self._footer(s)
        if note:
            s.notes_slide.notes_text_frame.text = note
        return s

    def takeaways(self, items, title="What to carry forward"):
        s = self._slide()
        self._rect(s, 0, 0, SLIDE_W, SLIDE_H, INK)
        self._rect(s, 0, 0, SLIDE_W, 0.16, CRIMSON)
        self._text(s, 0.9, 0.75, 11.5, 0.75,
                   [{"text": title, "size": 29, "bold": True, "color": WHITE,
                     "font": HEAD_FONT}])
        self._rect(s, 0.9, 1.62, 1.5, 0.035, GOLD)
        runs = []
        for i, t in enumerate(items, 1):
            runs.append({"text": f"{i}.  {t}",
                         "size": 17 if len(items) <= 6 else 15,
                         "color": RGBColor(0xD6, 0xDC, 0xE6),
                         "space_after": 13, "line_spacing": 1.25})
        self._text(s, 0.95, 2.0, 11.4, SLIDE_H - 2.9, runs)
        self._footer(s, dark=True)
        return s

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.prs.save(path)
        return path


# ----------------------------------------------------------------------------
# PDF document builder
# ----------------------------------------------------------------------------

class Doc:
    def __init__(self, title, subtitle=None, course=None, kicker=None,
                 landscape=False):
        self.title = title
        self.subtitle = subtitle
        self.course = course or ""
        self.kicker = kicker
        self.pagesize = (LETTER[1], LETTER[0]) if landscape else LETTER
        self.flow = []
        self._styles()

    def _styles(self):
        self.S = {
            "title": ParagraphStyle("title", fontName="Times-Bold", fontSize=26,
                                    leading=31, textColor=R_INK,
                                    spaceAfter=6),
            "subtitle": ParagraphStyle("subtitle", fontName="Times-Italic",
                                       fontSize=13.5, leading=18,
                                       textColor=R_MUTED, spaceAfter=4),
            "kicker": ParagraphStyle("kicker", fontName="Helvetica-Bold",
                                     fontSize=9, leading=12,
                                     textColor=R_CRIMSON, spaceAfter=10),
            "h1": ParagraphStyle("h1", fontName="Times-Bold", fontSize=17,
                                 leading=21, textColor=R_INK, spaceBefore=18,
                                 spaceAfter=7),
            "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12,
                                 leading=15.5, textColor=R_CRIMSON,
                                 spaceBefore=13, spaceAfter=5),
            "h3": ParagraphStyle("h3", fontName="Helvetica-BoldOblique",
                                 fontSize=10.5, leading=14, textColor=R_TEAL,
                                 spaceBefore=10, spaceAfter=3),
            "p": ParagraphStyle("p", fontName="Times-Roman", fontSize=10.8,
                                leading=15.4, textColor=R_SLATE,
                                alignment=TA_JUSTIFY, spaceAfter=7),
            "li": ParagraphStyle("li", fontName="Times-Roman", fontSize=10.5,
                                 leading=14.6, textColor=R_SLATE,
                                 spaceAfter=4),
            "code": ParagraphStyle("code", fontName="Courier", fontSize=8.6,
                                   leading=11.4,
                                   textColor=colors.HexColor("#E4E8EF")),
            "cap": ParagraphStyle("cap", fontName="Times-Italic", fontSize=9.4,
                                  leading=12.6, textColor=R_MUTED,
                                  spaceAfter=9),
            "eq": ParagraphStyle("eq", fontName="Courier-Bold", fontSize=10.4,
                                 leading=14, textColor=R_INK,
                                 alignment=TA_CENTER, spaceBefore=5,
                                 spaceAfter=5),
            "cell": ParagraphStyle("cell", fontName="Times-Roman", fontSize=9.2,
                                   leading=12.2, textColor=R_SLATE),
            "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold",
                                    fontSize=9.2, leading=12.2,
                                    textColor=colors.white),
        }

    # -- flow helpers -------------------------------------------------------

    def h1(self, t):
        self.flow.append(Paragraph(_subsup(t), self.S["h1"]))
        self.flow.append(HRFlowable(width="100%", thickness=0.9,
                                    color=R_RULE, spaceAfter=7,
                                    spaceBefore=1))
        return self

    def h2(self, t):
        self.flow.append(Paragraph(_subsup(t), self.S["h2"]))
        return self

    def h3(self, t):
        self.flow.append(Paragraph(_subsup(t), self.S["h3"]))
        return self

    def p(self, t):
        self.flow.append(Paragraph(_subsup(t), self.S["p"]))
        return self

    def cap(self, t):
        self.flow.append(Paragraph(_subsup(t), self.S["cap"]))
        return self

    def eq(self, t):
        self.flow.append(Paragraph(_subsup(t), self.S["eq"]))
        return self

    def bullets(self, items, numbered=False):
        lis = []
        for it in items:
            if isinstance(it, (list, tuple)):
                sub = ListFlowable(
                    [ListItem(Paragraph(_subsup(x), self.S["li"]), leftIndent=12)
                     for x in it],
                    bulletType="bullet", start="circle", leftIndent=16,
                    bulletFontSize=6)
                lis.append(sub)
            else:
                lis.append(ListItem(Paragraph(_subsup(it), self.S["li"]),
                                    leftIndent=12))
        self.flow.append(ListFlowable(
            lis, bulletType="1" if numbered else "bullet",
            start="1" if numbered else "square", leftIndent=16,
            bulletFontSize=7 if not numbered else 10,
            bulletColor=R_CRIMSON))
        self.flow.append(Spacer(1, 7))
        return self

    def code(self, src, caption=None):
        lines = src.strip("\n").split("\n")
        body = "<br/>".join(
            ln.replace("&", "&amp;").replace("<", "&lt;")
              .replace(">", "&gt;").replace(" ", "&nbsp;") or "&nbsp;"
            for ln in lines)
        t = Table([[Paragraph(body, self.S["code"])]],
                  colWidths=[self._cw()])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), R_CODEBG),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ]))
        self.flow.append(t)
        self.flow.append(Spacer(1, 5))
        if caption:
            self.cap(caption)
        return self

    def callout(self, label, body, color=None):
        color = color or R_GOLD
        inner = [Paragraph(_subsup(_upper(label)),
                           ParagraphStyle("cl", fontName="Helvetica-Bold",
                                          fontSize=8.4, leading=11,
                                          textColor=color, spaceAfter=4))]
        for b in (body if isinstance(body, list) else [body]):
            inner.append(Paragraph(_subsup(b), self.S["li"]))
        t = Table([[inner]], colWidths=[self._cw()])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), R_PANEL),
            ("LINEBEFORE", (0, 0), (0, -1), 2.5, color),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ]))
        self.flow.append(KeepTogether(t))
        self.flow.append(Spacer(1, 10))
        return self

    def table(self, header, rows, widths=None, caption=None):
        cw = self._cw()
        widths = ([w * cw for w in widths] if widths
                  else [cw / len(header)] * len(header))
        data = [[Paragraph(_subsup(h), self.S["cellh"]) for h in header]]
        for r in rows:
            data.append([Paragraph(_subsup(str(c)), self.S["cell"]) for c in r])
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), R_INK),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, R_PANEL]),
            ("GRID", (0, 0), (-1, -1), 0.5, R_RULE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        self.flow.append(t)
        self.flow.append(Spacer(1, 6))
        if caption:
            self.cap(caption)
        return self

    def spacer(self, h=10):
        self.flow.append(Spacer(1, h))
        return self

    def pagebreak(self):
        self.flow.append(PageBreak())
        return self

    def _cw(self):
        return self.pagesize[0] - 2 * 0.95 * inch

    # -- render -------------------------------------------------------------

    def _decorate(self, canvas, doc):
        canvas.saveState()
        w, h = self.pagesize
        if canvas.getPageNumber() == 1:
            canvas.setFillColor(R_INK)
            canvas.rect(0, h - 0.42 * inch, w, 0.42 * inch, stroke=0, fill=1)
            canvas.setFillColor(R_GOLD)
            canvas.setFont("Helvetica-Bold", 8.5)
            canvas.drawString(0.95 * inch, h - 0.27 * inch, WORDMARK)
            canvas.setFillColor(colors.HexColor("#8A95A6"))
            canvas.drawRightString(w - 0.95 * inch, h - 0.27 * inch,
                                   self.course)
        else:
            canvas.setFillColor(R_MUTED)
            canvas.setFont("Helvetica", 7.8)
            canvas.drawString(0.95 * inch, h - 0.55 * inch,
                              f"{WORDMARK}  ·  {self.course}")
            canvas.setStrokeColor(R_RULE)
            canvas.setLineWidth(0.6)
            canvas.line(0.95 * inch, h - 0.63 * inch, w - 0.95 * inch,
                        h - 0.63 * inch)
        canvas.setFillColor(R_MUTED)
        canvas.setFont("Helvetica", 7.8)
        canvas.drawCentredString(w / 2, 0.52 * inch,
                                 str(canvas.getPageNumber()))
        canvas.drawRightString(w - 0.95 * inch, 0.52 * inch,
                               "Original material · share freely")
        canvas.restoreState()

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        doc = BaseDocTemplate(
            path, pagesize=self.pagesize, title=self.title,
            author="University of Claude",
            leftMargin=0.95 * inch, rightMargin=0.95 * inch,
            topMargin=0.95 * inch, bottomMargin=0.85 * inch)
        first = Frame(0.95 * inch, 0.85 * inch, self._cw(),
                      self.pagesize[1] - 1.8 * inch, id="first")
        rest = Frame(0.95 * inch, 0.85 * inch, self._cw(),
                     self.pagesize[1] - 1.75 * inch, id="rest")
        doc.addPageTemplates([
            PageTemplate(id="first", frames=[first],
                         onPage=self._decorate),
            PageTemplate(id="rest", frames=[rest], onPage=self._decorate),
        ])
        head = []
        if self.kicker:
            head.append(Paragraph(_subsup(self.kicker), self.S["kicker"]))
        head.append(Paragraph(_subsup(self.title), self.S["title"]))
        if self.subtitle:
            head.append(Paragraph(_subsup(self.subtitle), self.S["subtitle"]))
        head.append(HRFlowable(width="100%", thickness=2, color=R_CRIMSON,
                               spaceBefore=8, spaceAfter=14))
        doc.build(head + self.flow)
        return path


def link(url, label=None):
    return f'<a href="{url}" color="#1F6B68">{label or url}</a>'
