"""Render book covers, Eden hero images, LinkedIn single-image posts and carousels.

Usage: python marketing/build_images.py
Outputs PNGs to marketing/images/ and carousel PDFs (LinkedIn document posts) to marketing/carousels/.
"""
import io
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "brand"))
import brand  # noqa: E402
from brand import CREAM, INK, MUTE, PAPER, RED, RULE  # noqa: E402

OUT = ROOT / "marketing" / "images"
CAR = ROOT / "marketing" / "carousels"
CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
HANDLE = "@mayankmishra29"
W, H = 1080, 1350

# ---------- building blocks ----------

def lockup(dark=True):
    fg = CREAM if dark else INK
    return f"""<div style="position:absolute;top:70px;left:70px;display:flex;align-items:center;gap:22px;">
  {brand.headshot(96, ring=RED)}
  <div><div style="font-family:'Bebas Neue';font-size:48px;line-height:1;color:{fg};letter-spacing:.01em;">MAYANK MISHRA</div>
  <div style="font-family:'DM Sans';font-size:30px;color:{fg};opacity:.6;margin-top:4px;">{HANDLE}</div></div></div>"""


def pnum(n, total, dark):
    if not n:
        return ""
    c = CREAM if dark else INK
    return f"""<div style="position:absolute;right:70px;bottom:62px;font-family:'JetBrains Mono';font-size:24px;color:{c};opacity:.55;">{n} / {total}</div>"""


def grain():
    return f"background-color:{CREAM};background-image:radial-gradient(rgba(14,13,12,.05) 1px, transparent 1px);background-size:43px 43px;"


def frame(inner, bg, extra_style=""):
    return f'<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{bg};{extra_style}">{inner}</div>'


def mode_a(lines, accent=None, kicker=None, n=None, total=9, size=160, accent_red=True, extra=""):
    ac = ""
    if accent:
        col = RED if accent_red else CREAM
        ac = f"""<div style="font-family:'DM Serif Display';font-style:italic;color:{col};font-size:{int(size*.66)}px;line-height:1.05;margin-top:14px;">{accent}</div>"""
    kick = f"""<div style="font-family:'JetBrains Mono';font-size:32px;letter-spacing:.14em;color:{'rgba(239,232,220,.6)' if (accent and accent_red) else RED};text-transform:uppercase;margin-bottom:28px;">{kicker}</div>""" if kicker else ""
    body = "".join(f"<div>{l}</div>" for l in lines)
    inner = f"""{lockup(True)}
<div style="position:absolute;left:70px;right:90px;top:50%;transform:translateY(-44%);">{kick}
<div style="font-family:'Bebas Neue';font-size:{size}px;line-height:.9;color:{CREAM};">{body}</div>{ac}</div>{extra}{pnum(n, total, True)}"""
    return frame(inner, INK)


def underline(text):
    return (f'<span style="position:relative;white-space:nowrap;">{text}<svg viewBox="0 0 300 20" preserveAspectRatio="none" '
            f'style="position:absolute;left:-4px;right:-4px;bottom:-14px;width:calc(100% + 8px);height:20px;overflow:visible">'
            f'<path d="M2 12 C 40 4, 70 18, 110 10 S 180 4, 220 12 S 280 16, 298 8" fill="none" stroke="{RED}" stroke-width="4" stroke-linecap="round"/></svg></span>')


def mode_b(num, headline, body, mark, n, total=9):
    body_html = body.replace(mark, underline(mark), 1)
    inner = f"""<div style="position:absolute;left:86px;right:86px;top:170px;">
<div style="font-family:'Bebas Neue';font-size:96px;color:{RED};line-height:1;">{num}</div>
<div style="font-family:'DM Serif Display';font-size:86px;line-height:1.02;color:{INK};margin-top:24px;">{headline}</div>
<div style="font-family:'DM Sans';font-size:44px;line-height:1.42;color:{INK};margin-top:48px;">{body_html}</div></div>{pnum(n, total, False)}"""
    return frame(inner, CREAM, grain())


def mode_c(first, lines, n, total=9, label=""):
    ls = "".join(f'<div style="margin-top:30px;">{l}</div>' for l in lines)
    lab = f"""<div style="font-family:'JetBrains Mono';font-size:28px;letter-spacing:.14em;text-transform:uppercase;color:{MUTE};margin:0 0 34px 6px;">{label}</div>""" if label else ""
    inner = f"""<div style="position:absolute;left:76px;right:76px;top:50%;transform:translateY(-50%);">{lab}
<div style="background:#fff;border:1px solid {RULE};border-radius:32px;padding:64px;">
<div style="display:flex;align-items:center;gap:22px;">{brand.headshot(88, ring=RULE)}
<div><div style="font-family:'DM Sans';font-weight:700;font-size:36px;color:{INK};">Mayank Mishra</div>
<div style="font-family:'DM Sans';font-size:28px;color:{MUTE};">{HANDLE}</div></div></div>
<div style="font-family:'DM Sans';font-size:46px;line-height:1.38;color:{INK};margin-top:64px;">
<div style="font-weight:700;">{first}</div>{ls}</div></div></div>{pnum(n, total, False)}"""
    return frame(inner, PAPER)


def mode_d(title, subtitle, diagram, n=None, total=9, standalone=False, footer=""):
    top = 250 if standalone else 120
    head = lockup(False) if standalone else ""
    inner = f"""{head}<div style="position:absolute;left:80px;right:80px;top:{top}px;">
<div style="font-family:'Bebas Neue';font-size:86px;line-height:.95;color:{INK};">{title}</div>
<div style="font-family:'DM Sans';font-size:34px;line-height:1.35;color:{MUTE};margin-top:16px;">{subtitle}</div>
<div style="margin-top:46px;">{diagram}</div></div>{footer}{pnum(n, total, False)}"""
    return frame(inner, PAPER)


def mode_e(sentence, red_tail, n, total=9):
    s = sentence.replace(red_tail, f'<span style="color:{RED}">{red_tail}</span>')
    inner = f"""<div style="position:absolute;left:110px;right:110px;top:50%;transform:translateY(-60%);text-align:center;
font-family:'DM Serif Display';font-size:80px;line-height:1.16;color:{INK};">{s}</div>
<div style="position:absolute;left:0;right:0;bottom:300px;display:flex;justify-content:center;align-items:center;gap:26px;">
<div style="width:120px;height:2px;background:{INK};opacity:.5"></div><div style="width:18px;height:18px;background:{RED};transform:rotate(45deg)"></div>
<div style="width:120px;height:2px;background:{INK};opacity:.5"></div></div>{pnum(n, total, False)}"""
    return frame(inner, PAPER)


def mode_f(headline, gets, keyword, n=None, total=9):
    inner = f"""{lockup(True)}<div style="position:absolute;left:70px;right:70px;top:50%;transform:translateY(-42%);">
<div style="font-family:'Bebas Neue';font-size:135px;line-height:.92;color:{CREAM};">{headline}</div>
<div style="font-family:'DM Sans';font-size:42px;line-height:1.35;color:{CREAM};opacity:.8;margin-top:36px;">{gets}</div>
<div style="display:inline-block;margin-top:56px;background:{RED};color:#fff;font-family:'Bebas Neue';font-size:64px;letter-spacing:.03em;padding:18px 44px 12px;border-radius:999px;">COMMENT "{keyword}"</div>
</div>{pnum(n, total, True)}"""
    return frame(inner, INK)


def book(key, w, **kw):
    """A flat book: cover plus a page-edge strip (no shadows)."""
    h = int(w * 1056 / 816)
    edge = "".join(f'<div style="height:{h}px;width:2px;background:{c};"></div>' for c in ("#FFFDF8", RULE, "#FFFDF8", RULE, "#FFFDF8"))
    return (f'<div style="display:flex;align-items:stretch;">{brand.cover_inner(key, w=w, h=h, **kw)}'
            f'<div style="display:flex;margin-top:6px;margin-bottom:6px;">{edge}</div></div>')


# ---------- diagrams ----------

def gates_diagram():
    gates = [("G1", "REALITY", "Is this person real?"), ("G2", "RELEVANCE", "Is this relevant to me?"),
             ("G3", "FIT", "Do they understand me?"), ("G4", "SAFETY", "Is it safe to explore?"),
             ("G5", "VALUE", "Is it worth it?"), ("G6", "IDENTITY", "Is this right for us?")]
    rows = ""
    for i, (g, name, q) in enumerate(gates):
        last = i == 5
        bg, fg = (INK, CREAM) if last else ("#fff", INK)
        rows += f"""<div style="display:flex;align-items:center;gap:26px;margin-left:{i*44}px;margin-bottom:14px;background:{bg};color:{fg};
border:1px solid {INK if last else RULE};border-radius:14px;padding:18px 28px;">
<div style="font-family:'JetBrains Mono';font-size:26px;opacity:.7;width:56px;">{g}</div>
<div style="font-family:'Bebas Neue';font-size:52px;width:250px;line-height:1;">{name}</div>
<div style="font-family:'DM Sans';font-size:30px;">{q}</div></div>"""
    note = f"""<div style="font-family:'DM Serif Display';font-style:italic;font-size:38px;color:{RED};margin-top:26px;">Salesy = answering a gate they haven't reached.</div>"""
    return rows + note


def ladder_diagram(items, top_red_label):
    out = ""
    n = len(items)
    for i, (rung, quote) in enumerate(items):
        top = i == 0
        bg, fg = (INK, CREAM) if top else ("#fff", INK)
        label = f'<span style="color:{RED}">{rung}</span>' if top else rung
        out += f"""<div style="display:flex;align-items:center;justify-content:space-between;gap:24px;margin-left:{(i)*30}px;margin-bottom:12px;
background:{bg};color:{fg};border:1px solid {INK if top else RULE};border-radius:12px;padding:16px 26px;">
<div style="font-family:'Bebas Neue';font-size:50px;line-height:1;white-space:nowrap;">{label}</div>
<div style="font-family:'DM Sans';font-style:normal;font-size:28px;text-align:right;opacity:.85;">{quote}</div></div>"""
    return out


def matrix(xlab, ylab, q):
    """q = dict(tl, tr, bl, br) -> (title, sub); 'tr' is the winning quadrant."""
    def cell(key, win=False):
        t, s = q[key]
        bg, fg = (INK, CREAM) if win else ("#fff", INK)
        tcol = RED if win else INK
        return f"""<div style="background:{bg};color:{fg};border:1px solid {INK if win else RULE};padding:30px;display:flex;flex-direction:column;justify-content:flex-end;">
<div style="font-family:'Bebas Neue';font-size:58px;line-height:.95;color:{tcol};">{t}</div>
<div style="font-family:'DM Sans';font-size:27px;line-height:1.3;margin-top:10px;opacity:.85;">{s}</div></div>"""
    return f"""<div style="display:flex;gap:18px;">
<div style="writing-mode:vertical-rl;transform:rotate(180deg);font-family:'JetBrains Mono';font-size:24px;letter-spacing:.12em;color:{MUTE};text-align:center;">{ylab} →</div>
<div style="flex:1;"><div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:330px 330px;gap:14px;">
{cell('tl')}{cell('tr', True)}{cell('bl')}{cell('br')}</div>
<div style="font-family:'JetBrains Mono';font-size:24px;letter-spacing:.12em;color:{MUTE};text-align:center;margin-top:16px;">{xlab} →</div></div></div>"""


def audit_diagram():
    stages = ["Audience & offer", "Profile & path", "Content mix", "CTAs & lead magnets", "Conversations", "Measurement"]
    rows = ""
    for i, s in enumerate(stages, 1):
        dots = "".join(f'<div style="width:34px;height:34px;border-radius:50%;border:2px solid {INK};"></div>' for _ in range(5))
        rows += f"""<div style="display:flex;align-items:center;justify-content:space-between;background:#fff;border:1px solid {RULE};border-radius:12px;padding:20px 28px;margin-bottom:12px;">
<div style="display:flex;align-items:center;gap:22px;"><div style="font-family:'JetBrains Mono';font-size:26px;color:{MUTE};">0{i}</div>
<div style="font-family:'Bebas Neue';font-size:50px;line-height:1;color:{INK};">{s}</div></div><div style="display:flex;gap:10px;">{dots}</div></div>"""
    total = f"""<div style="display:flex;align-items:center;justify-content:space-between;background:{INK};border-radius:12px;padding:22px 28px;">
<div style="font-family:'Bebas Neue';font-size:54px;color:{CREAM};">Your score</div><div style="font-family:'Bebas Neue';font-size:54px;color:{RED};">___ / 60</div></div>"""
    return rows + total


def iceberg():
    return f"""<div style="position:relative;">
<div style="background:{INK};border-radius:16px 16px 0 0;padding:28px 34px;">
<div style="font-family:'Bebas Neue';font-size:56px;color:{CREAM};line-height:1;">HOOK</div>
<div style="font-family:'DM Sans';font-size:28px;color:{CREAM};opacity:.8;">Earns a glance</div>
<div style="font-family:'Bebas Neue';font-size:56px;color:{RED};line-height:1;margin-top:18px;">REHOOK</div>
<div style="font-family:'DM Sans';font-size:28px;color:{CREAM};opacity:.8;">Earns the read</div></div>
<div style="display:flex;align-items:center;gap:16px;margin:14px 0;"><div style="flex:1;height:2px;background:{INK};"></div>
<div style="font-family:'JetBrains Mono';font-size:26px;color:{MUTE};">…see more</div><div style="flex:1;height:2px;background:{INK};"></div></div>
<div style="background:#fff;border:1px solid {RULE};border-radius:0 0 16px 16px;padding:26px 34px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;">
<div><div style="font-family:'Bebas Neue';font-size:50px;color:{INK};">BODY</div><div style="font-family:'DM Sans';font-size:26px;color:{MUTE};">Delivers the value</div></div>
<div><div style="font-family:'Bebas Neue';font-size:50px;color:{INK};">PAYOFF</div><div style="font-family:'DM Sans';font-size:26px;color:{MUTE};">Keeps the promise</div></div>
<div><div style="font-family:'Bebas Neue';font-size:50px;color:{INK};">CTA</div><div style="font-family:'DM Sans';font-size:26px;color:{MUTE};">The next step</div></div></div></div>"""


# ---------- assets ----------

def covers():
    specs = {
        "cover-non-salesy-dm": dict(key="nsdm", kicker="Complete Edition + Implementation System"),
        "cover-non-salesy-dm-field-guide": dict(key="nsdm", kicker="Free Field Guide",
                                               sub="The Field Guide: How to Read a LinkedIn Conversation Before You Send the Next Message"),
        "cover-reply-rates-lie": dict(key="nsdm", kicker="Field Report", title=["REPLY", "RATES", "LIE"], accent="And what to measure instead.",
                                     sub="A Field Report on Trust-Led Outbound for B2B Teams", bg=PAPER, fg=INK, vol="B2B FIELD REPORT"),
        "cover-linkedin-lead-engine": dict(key="lle", kicker="Complete Edition + Implementation System"),
        "cover-linkedin-lead-engine-field-guide": dict(key="lle", kicker="Free Field Guide",
                                                      sub="The Field Guide: Write Posts That Reach the Right People and Start the Right Conversations"),
        "cover-b2b-linkedin-pipeline-audit": dict(key="lle", kicker="Scorecard", title=["THE B2B", "LINKEDIN", "PIPELINE AUDIT"],
                                                 accent="Pipeline, or just posts?", sub="A 30-Point Scorecard for Founders and Revenue Leaders",
                                                 bg=PAPER, fg=INK, vol="B2B SCORECARD"),
    }
    return {name: (brand.cover_inner(**s), 816, 1056, 2) for name, s in specs.items()}, specs


def heroes(specs):
    out = {}
    for name, s in specs.items():
        key, title_parts = s["key"], s.get("title") or brand.COVERS[s["key"]]["title"]
        dark = s.get("bg", brand.COVERS[key]["bg"]) != INK
        bg = INK if dark else PAPER
        fg = CREAM if dark else INK
        label = s["kicker"]
        inner = f"""<div style="width:1200px;height:630px;background:{bg};display:flex;align-items:center;gap:70px;padding:0 80px;">
{book(key, 330, **{k: v for k, v in s.items() if k != 'key'})}
<div style="color:{fg};"><div style="font-family:'JetBrains Mono';font-size:20px;letter-spacing:.14em;text-transform:uppercase;opacity:.7;">{label}</div>
<div style="font-family:'Bebas Neue';font-size:96px;line-height:.9;margin-top:16px;">{' '.join(title_parts)}</div>
<div style="font-family:'DM Sans';font-size:26px;line-height:1.4;opacity:.75;margin-top:18px;max-width:560px;">Mayank Mishra · ThriveXLabs</div></div></div>"""
        out["hero-" + name.replace("cover-", "")] = (inner, 1200, 630, 1)
    # bundle
    inner = f"""<div style="width:1200px;height:630px;background:{INK};display:flex;align-items:center;gap:56px;padding:0 70px;">
<div style="display:flex;gap:26px;">{book('lle', 270, kicker='Complete Edition')}{book('nsdm', 270, kicker='Complete Edition')}</div>
<div style="color:{CREAM};"><div style="font-family:'JetBrains Mono';font-size:20px;letter-spacing:.14em;opacity:.7;">THE BUNDLE · VOL. 01 + 02</div>
<div style="font-family:'Bebas Neue';font-size:92px;line-height:.9;margin-top:16px;">THE LINKEDIN<br>CLIENT SYSTEM</div>
<div style="font-family:'DM Serif Display';font-style:italic;font-size:34px;margin-top:16px;opacity:.9;">Content starts it. Trust closes it.</div></div></div>"""
    out["hero-linkedin-client-system-bundle"] = (inner, 1200, 630, 1)
    return out


def single_posts():
    p = {}
    p["post-01-nsdm-launch"] = frame(f"""{lockup(True)}
<div style="position:absolute;left:70px;top:270px;width:560px;">
<div style="font-family:'JetBrains Mono';font-size:28px;letter-spacing:.14em;color:{CREAM};opacity:.7;">11,466 COLD DMS</div>
<div style="font-family:'Bebas Neue';font-size:138px;line-height:.9;color:{CREAM};margin-top:20px;">46% REPLIED.<br>THE BOOKINGS<br>DIDN'T FOLLOW.</div>
<div style="font-family:'DM Serif Display';font-style:italic;font-size:46px;line-height:1.15;color:{CREAM};margin-top:28px;opacity:.9;">So I wrote down what I learned from reading the threads.</div></div>
<div style="position:absolute;right:70px;bottom:120px;">{book('nsdm', 360, kicker='Complete Edition')}</div>""", INK)
    p["post-02-six-trust-gates"] = mode_d("THE SIX TRUST GATES", "Every buyer in your DMs is silently answering one of these.", gates_diagram(), standalone=True)
    p["post-03-interest-is-not-readiness"] = mode_d("INTEREST IS NOT READINESS", "Replies are interest. Bookings need readiness. Match the rung.",
        ladder_diagram([("Readiness", "“We have approval. What's needed to start?”"), ("Intent", "“Send scope and pricing.”"),
                        ("Exploration", "“What would you recommend for us?”"), ("Interest", "“How would that work?”"),
                        ("Curiosity", "“Interesting.”"), ("Attention", "A like, a view, a follow")], True), standalone=True)
    p["post-04-reply-rates-lie"] = mode_a(["REPLIES WERE", "NEVER THE", "PROBLEM."], accent="What came after them was.",
                                          kicker="11,466 DMs · 46% replied", size=170)
    p["post-05-lle-launch"] = frame(f"""{lockup(True)}
<div style="position:absolute;left:70px;top:280px;width:600px;">
<div style="font-family:'Bebas Neue';font-size:142px;line-height:.9;color:{CREAM};">I'M NOT A<br>LINKEDIN<br>INFLUENCER.</div>
<div style="font-family:'DM Serif Display';font-style:italic;font-size:62px;color:{CREAM};margin-top:22px;">That's the point.</div>
<div style="font-family:'DM Sans';font-size:34px;line-height:1.4;color:{CREAM};opacity:.7;margin-top:30px;">12.5k users in 3 months came from relevance, not reach.</div></div>
<div style="position:absolute;right:70px;bottom:120px;">{book('lle', 330, kicker='Complete Edition')}</div>""", INK)
    p["post-06-viral-vs-valuable"] = mode_d("VIRAL ≠ VALUABLE", "Optimize for qualified attention, not maximum attention.",
        matrix("REACH", "RELEVANCE", {"tl": ("QUIET PIPELINE", "Small reach, right people. Underrated."),
                                      "tr": ("QUALIFIED ATTENTION", "The right people, at scale. The goal."),
                                      "bl": ("NOISE", "Few people, wrong people."),
                                      "br": ("VANITY VIRAL", "Huge reach, nobody who buys.")}), standalone=True)
    p["post-07-cta-ladder"] = mode_d("THE CTA LADDER", "Ask for the smallest next step the post has earned.",
        ladder_diagram([("Commercial", "“Solving this this quarter? Message me.”"), ("Conversation", "“Tell me where it stalls.”"),
                        ("Resource", "“The checklist is linked below.”"), ("Experience", "“What's your biggest bottleneck?”"),
                        ("Application", "“Check one stalled deal today.”")], True), standalone=True)
    p["post-08-pipeline-audit"] = mode_d("PIPELINE OR JUST POSTS?", "Score your LinkedIn across six stages. Fix the lowest one first.", audit_diagram(), standalone=True)
    p["post-09-bundle-launch"] = frame(f"""{lockup(True)}
<div style="position:absolute;left:70px;top:250px;right:70px;">
<div style="font-family:'Bebas Neue';font-size:128px;line-height:.9;color:{CREAM};">CONTENT STARTS IT.<br>TRUST CLOSES IT.</div>
<div style="font-family:'DM Sans';font-size:36px;color:{CREAM};opacity:.7;margin-top:22px;">The LinkedIn Client System: both books, both AI tools.</div></div>
<div style="position:absolute;left:70px;right:70px;bottom:110px;display:flex;gap:40px;justify-content:center;">
{book('lle', 400, kicker='Vol. 02')}{book('nsdm', 400, kicker='Vol. 01')}</div>""", INK)
    return p


def carousel_hooks():
    return [
        mode_a(["MOST PEOPLE", "OBSESS OVER", "LINE ONE."], accent="Experts write lines one to three.", kicker="LinkedIn writing", n=1),
        mode_a(["A HOOK EARNS", "A GLANCE."], accent="The rehook earns the read.", n=2),
        mode_b("01", "Narrow the reader", "Tell the right person it's for them: “This matters most when the founder still approves every proposal.”", "the right person", 3),
        mode_b("02", "Complicate the diagnosis", "Add a twist that improves the explanation: “The team follows the process exactly. The process is missing the decision.”", "improves the explanation", 4),
        mode_c("I almost quit my business.", ["Not because it was failing.", "Because it was succeeding in the wrong way."], 5, label="Example: hook + rehook"),
        mode_d("WHAT SHOWS BEFORE “SEE MORE”", "The rehook decides whether the rest gets read.", iceberg(), n=6),
        mode_b("03", "Preview the payoff", "Set an honest expectation: “Here are three places to check before you change your price.”", "honest expectation", 7),
        mode_e("If your rehook could sit under twenty different hooks, it isn't doing its job.", "it isn't doing its job.", 8),
        mode_f("WANT 10 HOOKS +<br>3 REHOOK MOVES?", "The free LinkedIn Lead Engine Field Guide.", "HOOKS", n=9),
    ]


def carousel_salesy():
    return [
        mode_a(["YOUR DMS AREN'T", "TOO SALESY."], accent="They're too early.", kicker="LinkedIn DMs", n=1),
        mode_a(["46% REPLIED.", "BOOKINGS", "DIDN'T FOLLOW."], kicker="11,466 cold DMs", n=2, size=150),
        mode_b("01", "They asked one question", "“Interesting, what do you do?” got an offer, a proof point, a link and a call request. Answers to questions nobody asked.", "nobody asked", 3),
        mode_b("02", "Buyers move through gates", "Reality, relevance, fit, safety, value, identity. A DM feels salesy when it answers a gate they haven't reached.", "haven't reached", 4),
        mode_c("Hey Jon, saw you're a founder.", ["We help founders get 10–20 qualified leads a month.", "Open to a quick call this week?"], 5, label="The DM everyone ignores"),
        mode_d("PUSHY, HIDING OR TRUST-LED?", "Two questions decide how your DMs land.",
               matrix("MOVES AT THE BUYER'S PACE", "COMMERCIAL CLARITY",
                      {"tl": ("PUSHY", "Clear offer, way too early."), "tr": ("TRUST-LED", "Clear and well timed. The goal."),
                       "bl": ("SPAM", "Vague and early."), "br": ("HIDING", "Patient, but never makes the offer.")}), n=6),
        mode_b("03", "Read before you move", "Ask what state they're in, which gate they're at and what risk they're protecting. Then make the smallest move.", "smallest move", 7),
        mode_e("Your next message should solve the buyer's uncertainty, not your anxiety.", "not your anxiety.", 8),
        mode_f("WANT THE SIX<br>TRUST GATES?", "The free Non-Salesy DM Field Guide.", "TRUST", n=9),
    ]


# ---------- render ----------

def render():
    OUT.mkdir(parents=True, exist_ok=True)
    CAR.mkdir(parents=True, exist_ok=True)
    cov, specs = covers()
    jobs = dict(cov)
    jobs.update(heroes(specs))
    jobs.update({k: (v, W, H, 1) for k, v in single_posts().items()})
    carousels = {"carousel-lle-hook-rehook": carousel_hooks(), "carousel-nsdm-salesy-dms": carousel_salesy()}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM)
        for name, (inner, w, h, scale) in jobs.items():
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
            tmp = OUT / f".{name}.html"
            tmp.write_text(brand.page(inner, w, h))
            page.goto(tmp.as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            page.screenshot(path=str(OUT / f"{name}.png"))
            page.close()
            tmp.unlink()
            print("png", name)
        for name, slides in carousels.items():
            d = CAR / name
            d.mkdir(exist_ok=True)
            writer = PdfWriter()
            for i, s in enumerate(slides, 1):
                page = browser.new_page(viewport={"width": W, "height": H})
                tmp = d / f".slide-{i:02d}.html"
                tmp.write_text(brand.page(s, W, H))
                page.goto(tmp.as_uri(), wait_until="load")
                page.evaluate("document.fonts.ready")
                page.screenshot(path=str(d / f"slide-{i:02d}.png"))
                pdf = page.pdf(width=f"{W}px", height=f"{H}px", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
                writer.add_page(PdfReader(io.BytesIO(pdf)).pages[0])
                page.close()
                tmp.unlink()
            with open(CAR / f"{name}.pdf", "wb") as fh:
                writer.write(fh)
            print("carousel", name, len(slides))
        browser.close()


if __name__ == "__main__":
    render()
