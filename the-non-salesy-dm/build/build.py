"""Render The Non-Salesy DM editions from Markdown to print-ready PDF.

Usage: python build/build.py [complete|field-guide|authority|field-kit|all]
"""
import io
import re
import sys
from pathlib import Path

import markdown
import qrcode
import qrcode.image.svg
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "brand"))
import brand  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
STORE_URL = "https://revops.eden.so/"
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

EDITIONS = {
    "complete": {
        "src": "complete-edition",
        "out": "The-Non-Salesy-DM-Complete-Edition.pdf",
        "title": "The Non-Salesy DM",
        "subtitle": "A Trust-Led System for Turning LinkedIn Conversations Into Clients Without Pressure, Chasing or Scripts",
        "badge": "Complete Edition + Implementation System",
        "toc": True,
        "cover": dict(key="nsdm", kicker="Complete Edition + Implementation System"),
    },
    "field-guide": {
        "src": "field-guide",
        "out": "The-Non-Salesy-DM-Field-Guide.pdf",
        "title": "The Non-Salesy DM",
        "subtitle": "The Field Guide: How to Read a LinkedIn Conversation Before You Send the Next Message",
        "badge": "Free Field Guide",
        "toc": True,
        "cover": dict(key="nsdm", kicker="Free Field Guide", sub="The Field Guide: How to Read a LinkedIn Conversation Before You Send the Next Message"),
    },
    "authority": {
        "src": "authority",
        "out": "Trust-Led-Outbound-Field-Report.pdf",
        "title": "Reply Rates Lie",
        "subtitle": "A Field Report on Trust-Led Outbound for B2B Teams, and What to Measure Instead",
        "badge": "ThriveXLabs Field Report",
        "toc": False,
        "cover": dict(key="nsdm", kicker="Field Report", title=["REPLY", "RATES", "LIE"], accent="And what to measure instead.", sub="A Field Report on Trust-Led Outbound for B2B Teams", bg=brand.PAPER, fg=brand.INK, vol="B2B FIELD REPORT"),
    },
    "field-kit": {
        "src": "system/field-kit",
        "out": "The-Non-Salesy-DM-Field-Kit.pdf",
        "title": "The Field Kit",
        "subtitle": "Printable worksheets for The Non-Salesy DM Implementation System",
        "badge": "Implementation System",
        "toc": False,
        "cover": dict(key="nsdm", kicker="Implementation System", title=["THE NON-SALESY DM", "FIELD KIT"], accent="Worksheets beside the inbox.", sub="Printable worksheets for The Non-Salesy DM"),
    },
}


def qr_svg(url: str) -> str:
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2)
    svg = img.to_string(encoding="unicode")
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    return svg.replace("<svg ", '<svg class="qr" ', 1)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def render_body(src_dir: Path):
    md = markdown.Markdown(extensions=["tables", "md_in_html", "attr_list", "sane_lists"])
    parts = []
    section_re = re.compile(r"<section([^>]*)>(.*?)</section>", re.S)
    for f in sorted(src_dir.glob("[0-9]*.md")):
        text = f.read_text()
        sections = section_re.findall(text) or [("", text)]
        for attrs, inner in sections:
            md.reset()
            parts.append(f"<section{attrs}>{md.convert(inner)}</section>")
    html = "\n".join(parts)
    toc = []

    def add_id(m):
        text = re.sub(r"<[^>]+>", "", m.group(1))
        anchor = slug(text)
        toc.append((anchor, text))
        return f'<h1 id="{anchor}">{m.group(1)}</h1>'

    html = re.sub(r"<h1>(.*?)</h1>", add_id, html)
    html = html.replace("{{QR_STORE}}", qr_svg(STORE_URL))
    return html, toc


def build(key: str):
    ed = EDITIONS[key]
    body, toc = render_body(ROOT / ed["src"])
    css = brand.fonts_css() + (ROOT / "build" / "style.css").read_text() + (brand.BRAND / "interior.css").read_text()
    toc_html = ""
    if ed["toc"]:
        items = "".join(
            f'<li><a href="#{a}">{t}</a></li>' for a, t in toc if t not in ("Contents",)
        )
        toc_html = f'<section class="toc"><h2>Contents</h2><ol>{items}</ol></section>'
    cover = brand.cover_inner(**ed["cover"])
    head = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{ed["title"]}</title><style>{css}</style></head>'
    DIST.mkdir(exist_ok=True)
    stem = Path(ed["out"]).stem
    cover_path = DIST / f"{stem}.cover.html"
    cover_path.write_text(brand.page(cover, 816, 1056))
    html_path = DIST / f"{stem}.html"
    html_path.write_text(f"{head}<body>{toc_html}<main>{body}</main></body></html>")
    pdf_path = DIST / ed["out"]
    footer = (
        '<div style="width:100%;font-family:JetBrains Mono,monospace;font-size:7px;letter-spacing:1px;color:#6E675E;'
        'padding:0 0.75in;display:flex;justify-content:space-between;">'
        f'<span>{ed["title"]} · ThriveXLabs</span><span class="pageNumber"></span></div>'
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM)
        page = browser.new_page()
        page.goto(cover_path.as_uri(), wait_until="load")
        cover_pdf = page.pdf(width="8.5in", height="11in", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        page.goto(html_path.as_uri(), wait_until="load")
        body_pdf = page.pdf(
            format="Letter",
            print_background=True,
            display_header_footer=True,
            header_template="<div></div>",
            footer_template=footer,
            margin={"top": "0.7in", "bottom": "0.7in", "left": "0.75in", "right": "0.75in"},
        )
        browser.close()
    writer = PdfWriter()
    for blob in (cover_pdf, body_pdf):
        for pg in PdfReader(io.BytesIO(blob)).pages:
            writer.add_page(pg)
    writer.add_metadata({"/Title": f"{ed['title']}: {ed['subtitle']}", "/Author": "Mayank Mishra"})
    with open(pdf_path, "wb") as fh:
        writer.write(fh)
    cover_path.unlink()
    print(f"built {pdf_path.relative_to(ROOT)}")


if __name__ == "__main__":
    targets = sys.argv[1:] or ["all"]
    if "all" in targets:
        targets = [k for k in EDITIONS if (ROOT / EDITIONS[k]["src"]).exists()]
    for t in targets:
        build(t)
