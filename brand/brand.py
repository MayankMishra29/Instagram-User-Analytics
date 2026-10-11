"""Shared ThriveXLabs / Mayank Mishra brand: fonts, tokens, headshot and book-cover markup.

Used by both book builds and the marketing image renderer so every surface matches.
"""
import re
from pathlib import Path

import qrcode
import qrcode.image.svg

BRAND = Path(__file__).resolve().parent
FONTS = BRAND / "fonts"
STORE_URL = "https://revops.eden.so/"

INK, CREAM, PAPER, RED, MUTE, RULE = "#0E0D0C", "#EFE8DC", "#F7F3EC", "#D7261E", "#6E675E", "#D9D0C2"


def fonts_css() -> str:
    """@font-face rules pointing at the local woff2 files with absolute file URIs."""
    css = (FONTS / "fonts.css").read_text()
    return re.sub(r"url\('([^']+)'\)", lambda m: f"url('{(FONTS / m.group(1)).as_uri()}')", css)


def qr_svg(url: str = STORE_URL, cls: str = "qr") -> str:
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2)
    svg = re.sub(r"<\?xml[^>]*\?>", "", img.to_string(encoding="unicode"))
    return svg.replace("<svg ", f'<svg class="{cls}" ', 1)


def headshot(size: int, ring: str = RED) -> str:
    """Circular headshot with a ring; falls back to an MM monogram when brand/headshot.jpg is absent."""
    photo = BRAND / "headshot.jpg"
    style = f"width:{size}px;height:{size}px;border-radius:50%;box-shadow:0 0 0 3px {ring};flex:none;"
    if photo.exists():
        return f'<img src="{photo.as_uri()}" style="{style}object-fit:cover;">'
    return (f'<div style="{style}background:{CREAM};color:{INK};display:flex;align-items:center;justify-content:center;'
            f"font-family:'Bebas Neue';font-size:{int(size * .46)}px;letter-spacing:.02em;\">MM</div>")


# Cover specs shared by the PDFs and the cover images.
COVERS = {
    "nsdm": {"bg": INK, "fg": CREAM, "vol": "VOL. 01", "title": ["THE", "NON-SALESY", "DM"],
             "accent": "Without pressure, chasing or scripts.",
             "sub": "A Trust-Led System for Turning LinkedIn Conversations Into Clients"},
    "lle": {"bg": CREAM, "fg": INK, "vol": "VOL. 02", "title": ["THE", "LINKEDIN", "LEAD ENGINE"],
            "accent": "Clients, not just likes.",
            "sub": "How to Write LinkedIn Posts That Attract Clients, Not Just Likes"},
}


def cover_inner(key: str, kicker: str, title=None, accent=None, sub=None, bg=None, fg=None, vol=None, w=816, h=1056) -> str:
    """Book cover markup sized w x h px (default = US Letter at 96 dpi)."""
    c = dict(COVERS[key])
    title = title or c["title"]
    accent = c["accent"] if accent is None else accent
    sub = c["sub"] if sub is None else sub
    bg, fg = bg or c["bg"], fg or c["fg"]
    vol = vol or c["vol"]
    k = w / 816
    soft = "rgba(239,232,220,.72)" if fg == CREAM else "rgba(14,13,12,.68)"
    rule = "rgba(239,232,220,.22)" if fg == CREAM else "rgba(14,13,12,.18)"
    qr_bg = CREAM if bg == INK else PAPER
    lines = "".join(f"<div>{t}</div>" for t in title)
    size = 150 if max(len(t) for t in title) <= 10 else 128
    return f"""
<div class="bk" style="width:{w}px;height:{h}px;background:{bg};color:{fg};position:relative;overflow:hidden;
  font-family:'DM Sans';box-sizing:border-box;padding:{64*k}px {68*k}px;display:flex;flex-direction:column;justify-content:space-between;">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;font-family:'JetBrains Mono';font-size:{15*k}px;letter-spacing:.14em;text-transform:uppercase;color:{soft};line-height:1.6;">
    <div>ThriveXLabs<br><span style="color:{fg}">{kicker}</span></div><div style="text-align:right;white-space:nowrap">LinkedIn Client System<br>{vol}</div>
  </div>
  <div>
    <div style="height:{2*k}px;background:{rule};margin-bottom:{34*k}px"></div>
    <div style="font-family:'Bebas Neue';font-size:{size*k}px;line-height:.88;letter-spacing:.005em;">{lines}</div>
    <div style="font-family:'DM Serif Display';font-style:italic;color:{RED};font-size:{50*k}px;line-height:1.1;margin-top:{26*k}px;">{accent}</div>
    <div style="font-size:{21*k}px;line-height:1.45;color:{soft};margin-top:{22*k}px;max-width:{560*k}px;">{sub}</div>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;">
    <div style="display:flex;align-items:center;gap:{18*k}px;">
      {headshot(int(64*k), ring=fg)}
      <div><div style="font-family:'Bebas Neue';font-size:{38*k}px;line-height:1;letter-spacing:.02em;">MAYANK MISHRA</div>
      <div style="font-size:{16*k}px;color:{soft};margin-top:{4*k}px;">Founder, ThriveXLabs</div></div>
    </div>
    <div style="text-align:center;font-family:'JetBrains Mono';font-size:{12*k}px;letter-spacing:.08em;color:{soft};">
      <div style="background:{qr_bg};padding:{6*k}px;width:{104*k}px;height:{104*k}px;margin-bottom:{6*k}px;box-sizing:border-box;">{qr_svg()}</div>
      REVOPS.EDEN.SO</div>
  </div>
</div>"""


def page(body: str, w: int, h: int, bg: str = PAPER, extra_css: str = "") -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{fonts_css()}
html,body{{margin:0;padding:0;width:{w}px;height:{h}px;background:{bg};-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
.qr{{width:100%;height:100%;display:block}} *{{box-sizing:border-box}} {extra_css}</style></head><body>{body}</body></html>"""
