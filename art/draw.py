"""Draw the front page for Tuesday 17 November 2026 into entry.png (1024x1024), layout v2.

Run from the repo root:  python art/draw.py [out.png]
Needs Pillow and the Windows fonts (Georgia, Arial). The output PNG is committed;
main.py only copies it, so the graded run needs neither.

Every story is sourced in research/sources-2026-11-17.md.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SCALE = 2  # draw at 2x, downsample for clean edges
FONT_DIR = r"C:\Windows\Fonts"

BG = (248, 245, 237)
INK = (22, 22, 26)
GREY = (88, 88, 94)
RULE = (190, 180, 160)
RED = (180, 30, 36)
NAVY = (22, 44, 80)
LAND = (222, 212, 188)
SEA = (214, 228, 238)
WHITE = (255, 255, 255)

REG = {  # region tag colours
    "EUROPE": (36, 84, 160),
    "MIDDLE EAST": (178, 34, 34),
    "ASIA": (176, 96, 10),
    "AFRICA": (40, 120, 60),
    "AMERICAS": (118, 56, 140),
    "GLOBAL": (20, 116, 128),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), int(size * SCALE))


img = Image.new("RGB", (W * SCALE, H * SCALE), BG)
d = ImageDraw.Draw(img)


def S(v):
    return int(round(v * SCALE))


def text(x, y, s, f, fill=INK, anchor="la"):
    d.text((S(x), S(y)), s, font=f, fill=fill, anchor=anchor)


def width(s, f):
    return d.textlength(s, font=f) / SCALE


def rect(x0, y0, x1, y1, fill=None, outline=None, w=1.0):
    d.rectangle([S(x0), S(y0), S(x1), S(y1)], fill=fill, outline=outline, width=max(1, S(w)) if outline else 0)


def line(pts, fill=INK, w=1.0):
    d.line([(S(x), S(y)) for x, y in pts], fill=fill, width=max(1, S(w)))


def poly(pts, fill=None, outline=None):
    d.polygon([(S(x), S(y)) for x, y in pts], fill=fill, outline=outline)


def circle(cx, cy, r, fill=None, outline=None, w=1.0):
    d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill=fill, outline=outline,
              width=max(1, S(w)) if outline else 0)


def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    poly(pts, fill=fill)


def wrap(segments, max_w):
    words = []
    for s, f, c in segments:
        for wd in s.split(" "):
            if wd:
                words.append((wd, f, c))
    lines, cur, cur_w = [], [], 0.0
    for wd, f, c in words:
        sp = width(" ", f) if cur else 0
        ww = width(wd, f)
        if cur and cur_w + sp + ww > max_w:
            lines.append(cur)
            cur, cur_w, sp = [], 0.0, 0
        cur.append((wd, f, c))
        cur_w += sp + ww
    if cur:
        lines.append(cur)
    return lines


def draw_lines(x, y, lines, lh):
    for i, ln in enumerate(lines):
        cx = x
        for j, (wd, f, c) in enumerate(ln):
            if j:
                cx += width(" ", f)
            text(cx, y + i * lh, wd, f, c)
            cx += width(wd, f)
    return len(lines) * lh


def para(x, y, segments, max_w, lh, max_lines=None):
    lines = wrap(segments, max_w)
    if max_lines and len(lines) > max_lines:
        print("WARNING: text too long:", " ".join(s for s, _, _ in segments), file=sys.stderr)
        lines = lines[:max_lines]
    return draw_lines(x, y, lines, lh)


# ------------------------------------------------------------------ fonts
F_KICK = font("arialbd.ttf", 11)
F_DATE = font("georgiab.ttf", 80)
F_STRAP = font("georgiai.ttf", 15)
F_BADGE = font("arialbd.ttf", 12)
F_FIG = font("georgiab.ttf", 19)
F_FIGL = font("arial.ttf", 10.5)
F_LBAR = font("arialbd.ttf", 9.5)
F_TAG = font("arialbd.ttf", 10)
F_LHEAD = font("georgiab.ttf", 19)
F_LDET = font("arial.ttf", 13)
F_THEAD = font("georgiab.ttf", 14)
F_TDET = font("arial.ttf", 11.5)
F_NUM = font("arialbd.ttf", 10)
F_SEC = font("arialbd.ttf", 11)
F_LIB = font("arialbd.ttf", 12.5)
F_LIR = font("arial.ttf", 12.5)
F_FOOT = font("arial.ttf", 10.5)
F_ILL = font("arialbd.ttf", 9)

# ------------------------------------------------------------------ flags
def flag(x, y, w, h, k):
    def hbands(cols):
        n = len(cols)
        for i, c in enumerate(cols):
            rect(x, y + i * h / n, x + w, y + (i + 1) * h / n, fill=c)

    def vbands(cols, weights=None):
        weights = weights or [1] * len(cols)
        tot, acc = sum(weights), 0
        for c, wt in zip(cols, weights):
            rect(x + acc * w / tot, y, x + (acc + wt) * w / tot, y + h, fill=c)
            acc += wt

    if k == "US":
        for i in range(7):
            rect(x, y + i * h / 7, x + w, y + (i + 0.5) * h / 7, fill=(190, 30, 45))
            rect(x, y + (i + 0.5) * h / 7, x + w, y + (i + 1) * h / 7, fill=WHITE)
        rect(x, y, x + w * 0.42, y + h * 0.54, fill=(30, 50, 110))
    elif k == "IN":
        hbands([(255, 153, 51), WHITE, (19, 136, 8)])
        circle(x + w / 2, y + h / 2, h / 9, outline=(0, 0, 128), w=1)
    elif k == "JP":
        rect(x, y, x + w, y + h, fill=WHITE)
        circle(x + w / 2, y + h / 2, h * 0.3, fill=(188, 0, 45))
    elif k == "AU":
        rect(x, y, x + w, y + h, fill=(0, 40, 120))
        line([(x, y), (x + w / 2, y + h / 2)], WHITE, 2.5)
        line([(x + w / 2, y), (x, y + h / 2)], WHITE, 2.5)
        rect(x + w / 4 - 1.2, y, x + w / 4 + 1.2, y + h / 2, fill=(200, 16, 46))
        rect(x, y + h / 4 - 1.2, x + w / 2, y + h / 4 + 1.2, fill=(200, 16, 46))
        for sx, sy in [(0.75, 0.3), (0.86, 0.55), (0.72, 0.78), (0.25, 0.78)]:
            star(x + w * sx, y + h * sy, h * 0.08, WHITE)
    elif k == "MX":
        vbands([(0, 104, 71), WHITE, (206, 17, 38)])
        circle(x + w / 2, y + h / 2, h * 0.12, fill=(140, 90, 40))
    elif k == "BO":
        hbands([(213, 43, 30), (249, 228, 0), (0, 122, 51)])
    elif k == "MN":
        vbands([(200, 16, 46), (0, 102, 179), (200, 16, 46)])
        circle(x + w / 6, y + h * 0.3, h * 0.07, fill=(255, 210, 0))
        rect(x + w / 6 - h * 0.06, y + h * 0.42, x + w / 6 + h * 0.06, y + h * 0.75, fill=(255, 210, 0))
    elif k == "CA":
        vbands([(216, 6, 33), WHITE, (216, 6, 33)], [1, 2, 1])
        cx, cy, r = x + w / 2, y + h / 2, h * 0.3
        poly([(cx, cy - r), (cx + r * 0.35, cy - r * 0.35), (cx + r, cy - r * 0.2), (cx + r * 0.5, cy + r * 0.4),
              (cx + r * 0.1, cy + r * 0.45), (cx, cy + r), (cx - r * 0.1, cy + r * 0.45), (cx - r * 0.5, cy + r * 0.4),
              (cx - r, cy - r * 0.2), (cx - r * 0.35, cy - r * 0.35)], fill=(216, 6, 33))
    elif k == "CN":
        rect(x, y, x + w, y + h, fill=(222, 41, 16))
        star(x + w * 0.17, y + h * 0.3, h * 0.17, (255, 222, 0))
        for sx, sy in [(0.33, 0.12), (0.4, 0.25), (0.4, 0.42), (0.33, 0.55)]:
            star(x + w * sx, y + h * sy, h * 0.06, (255, 222, 0))
    elif k == "RU":
        hbands([WHITE, (0, 57, 166), (213, 43, 30)])
    elif k == "RS":
        hbands([(198, 54, 60), (12, 64, 118), WHITE])
    elif k == "MZ":
        hbands([(0, 150, 57), (0, 0, 0), (252, 225, 0)])
        line([(x, y + h / 3), (x + w, y + h / 3)], WHITE, 1)
        line([(x, y + 2 * h / 3), (x + w, y + 2 * h / 3)], WHITE, 1)
        poly([(x, y), (x + w * 0.42, y + h / 2), (x, y + h)], fill=(210, 16, 52))
        star(x + w * 0.13, y + h / 2, h * 0.12, (252, 225, 0))
    elif k == "GB":
        rect(x, y, x + w, y + h, fill=(1, 33, 105))
        line([(x, y), (x + w, y + h)], WHITE, 3)
        line([(x + w, y), (x, y + h)], WHITE, 3)
        line([(x, y), (x + w, y + h)], (200, 16, 46), 1)
        line([(x + w, y), (x, y + h)], (200, 16, 46), 1)
        rect(x + w / 2 - 3, y, x + w / 2 + 3, y + h, fill=WHITE)
        rect(x, y + h / 2 - 3, x + w, y + h / 2 + 3, fill=WHITE)
        rect(x + w / 2 - 1.6, y, x + w / 2 + 1.6, y + h, fill=(200, 16, 46))
        rect(x, y + h / 2 - 1.6, x + w, y + h / 2 + 1.6, fill=(200, 16, 46))
    rect(x, y, x + w, y + h, outline=(70, 70, 70), w=0.5)


def badge(x, y, s, fill, anchor="l"):
    """Small filled label sized to its text; anchor l/m/r is where x sits."""
    tw = width(s, F_ILL) + 10
    x0 = x if anchor == "l" else (x - tw / 2 if anchor == "m" else x - tw)
    rect(x0, y, x0 + tw, y + 13, fill=fill)
    text(x0 + tw / 2, y + 6.5, s, F_ILL, WHITE, anchor="mm")


def label_bar(x, y, w, h, s, fill=(20, 24, 34)):
    rect(x, y + h - 13, x + w, y + h, fill=fill)
    text(x + w / 2, y + h - 6.5, s, F_LBAR, WHITE, anchor="mm")


# ------------------------------------------------------------------ lead illustrations (328 x 124)
def ill_iran(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(206, 222, 234))  # sea (Gulf)
    # Iran coast top, Arabian side bottom-left with Bahrain island
    poly([(x, y), (x + w, y), (x + w, y + 30), (x + w * 0.7, y + 40), (x + w * 0.45, y + 28), (x + w * 0.2, y + 22),
          (x, y + 18)], fill=(226, 210, 176))
    poly([(x, y + h - 13), (x, y + 70), (x + 40, y + 76), (x + 70, y + 96), (x + 120, y + h - 13)], fill=(226, 210, 176))
    poly([(x + 58, y + 62), (x + 70, y + 60), (x + 74, y + 74), (x + 62, y + 78)], fill=(226, 210, 176),
         outline=(150, 130, 100))
    text(x + 60, y + 4, "IRAN", F_ILL, (90, 70, 40))
    text(x + 30, y + 82, "BAHRAIN", F_ILL, (90, 70, 40))
    # Qeshm island
    poly([(x + w * 0.72, y + 44), (x + w * 0.86, y + 40), (x + w * 0.9, y + 46), (x + w * 0.76, y + 50)],
         fill=(226, 210, 176), outline=(150, 130, 100))
    text(x + w * 0.79, y + 31, "QESHM", F_ILL, (90, 70, 40), anchor="ma")
    # drone track Iran -> Bahrain, intercepted
    pts = [(x + w * 0.55, y + 30), (x + w * 0.4, y + 48), (x + w * 0.27, y + 62)]
    for i in range(len(pts) - 1):
        line([pts[i], pts[i + 1]], (200, 40, 40), 2)
    cx, cy = x + w * 0.25, y + 64
    line([(cx - 6, cy - 6), (cx + 6, cy + 6)], (200, 40, 40), 3)
    line([(cx - 6, cy + 6), (cx + 6, cy - 6)], (200, 40, 40), 3)
    badge(x + 6, y + 38, "DRONES INTERCEPTED", (200, 40, 40))
    # US strike track -> Qeshm
    for i in range(10):
        sx = x + w * 0.42 + i * 12
        line([(sx, y + 88 - i * 3.6), (sx + 6, y + 88 - (i + 0.5) * 3.6)], (30, 60, 140), 2)
    poly([(x + w * 0.76, y + 52), (x + w * 0.76 - 9, y + 54), (x + w * 0.76 - 5, y + 60)], fill=(30, 60, 140))
    badge(x + w * 0.44, y + h - 30, "US STRIKES QESHM", (30, 60, 140))
    label_bar(x, y, w, h, "BAHRAIN \u00b7 SHEIKH ISA AIR BASE \u00b7 STRAIT OF HORMUZ")


def ill_bridge(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(196, 212, 226))
    rect(x, y + h - 44, x + w, y + h - 13, fill=(66, 104, 146))
    for i in range(6):
        line([(x + 10 + i * 55, y + h - 30), (x + 30 + i * 55, y + h - 30)], (110, 150, 190), 1)
    deck = y + h - 62
    rect(x, deck, x + w * 0.44, deck + 6, fill=(58, 58, 62))
    rect(x + w * 0.58, deck, x + w, deck + 6, fill=(58, 58, 62))
    poly([(x + w * 0.44, deck), (x + w * 0.44, deck + 6), (x + w * 0.52, deck + 30), (x + w * 0.5, deck + 33)],
         fill=(58, 58, 62))
    for px in [0.06, 0.18, 0.3, 0.42, 0.62, 0.74, 0.86, 0.97]:
        rect(x + w * px - 2.5, deck + 6, x + w * px + 2.5, y + h - 44, fill=(80, 80, 84))
    d.arc([S(x + w * 0.6), S(deck - 26), S(x + w * 0.96), S(deck + 26)], 180, 360, fill=(96, 96, 102), width=S(3))
    for i, (sx, sy, r) in enumerate([(0.5, -6, 13), (0.47, -22, 15), (0.53, -38, 16), (0.49, -54, 13)]):
        g = 80 + i * 28
        circle(x + w * sx, deck + sy, r, fill=(g, g, g))
    circle(x + w * 0.5, deck + 2, 7, fill=(240, 140, 40))
    text(x + 8, y + 6, "CRIMEA", F_ILL, (40, 50, 70))
    text(x + w - 8, y + 6, "RUSSIA", F_ILL, (40, 50, 70), anchor="ra")
    badge(x + w * 0.62, y + 24, "STRUCK FOR A 2ND DAY", (200, 40, 40))
    label_bar(x, y, w, h, "KERCH STRAIT \u00b7 CRIMEAN BRIDGE")


def ill_quad(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(236, 230, 214))
    rect(x + 50, y + 8, x + w - 50, y + 26, fill=(70, 50, 120))
    text(x + w / 2, y + 17, "QUAD LEADERS' SUMMIT \u00b7 MANILA", F_ILL, WHITE, anchor="mm")
    fw, fh = 50, 32
    gap = (w - 4 * fw) / 5
    for i, k in enumerate(["US", "IN", "JP", "AU"]):
        fx = x + gap + i * (fw + gap)
        flag(fx, y + 31, fw, fh, k)
        name = {"US": "US", "IN": "INDIA", "JP": "JAPAN", "AU": "AUSTRALIA"}[k]
        text(fx + fw / 2, y + 66, name, F_ILL, (60, 50, 40), anchor="ma")
    rect(x + 10, y + h - 21, x + w - 10, y + h - 15, fill=(120, 80, 40))
    for rx, c in [(0.3, (120, 120, 132)), (0.44, (172, 120, 70)), (0.58, (90, 112, 124)), (0.72, (150, 150, 162))]:
        poly([(x + w * rx - 9, y + h - 21), (x + w * rx - 4, y + h - 29), (x + w * rx + 5, y + h - 30),
              (x + w * rx + 9, y + h - 21)], fill=c)
    label_bar(x, y, w, h, "CRITICAL-MINERALS DEALS", fill=(70, 50, 120))


# ------------------------------------------------------------------ tile illustrations (about 158 x 66)
def t_nvidia(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(18, 22, 30))
    cx, cy = x + 26, y + 26
    rect(cx - 13, cy - 13, cx + 13, cy + 13, fill=(60, 64, 72), outline=(118, 185, 0), w=1.2)
    for i in range(4):
        line([(cx - 17, cy - 9 + i * 6), (cx - 13, cy - 9 + i * 6)], (180, 180, 180), 1)
        line([(cx + 13, cy - 9 + i * 6), (cx + 17, cy - 9 + i * 6)], (180, 180, 180), 1)
    text(cx, cy, "AI", F_ILL, (118, 185, 0), anchor="mm")
    for i, v in enumerate([10, 16, 22, 30, 40]):
        rect(x + 52 + i * 9, y + 48 - v, x + 58 + i * 9, y + 48, fill=(118, 185, 0))
    text(x + w - 6, y + 6, "$115.8BN", F_BADGE, (118, 185, 0), anchor="ra")
    text(x + w - 6, y + 24, "DOW \u2212849", F_ILL, (235, 80, 70), anchor="ra")
    label_bar(x, y, w, h, "NVIDIA \u00b7 WALL STREET")


def t_ebola(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(232, 220, 196))
    poly([(x + 20, y + 48), (x + 46, y + 20), (x + 72, y + 48)], fill=WHITE, outline=(150, 140, 120))
    rect(x + 42, y + 30, x + 50, y + 33, fill=(200, 30, 30))
    rect(x + 44.5, y + 27, x + 47.5, y + 36, fill=(200, 30, 30))
    circle(x + 88, y + 24, 5, fill=(230, 230, 230), outline=(120, 120, 120), w=0.6)
    rect(x + 82, y + 29, x + 94, y + 48, fill=(230, 230, 230), outline=(120, 120, 120), w=0.6)
    rect(x + w - 58, y + 8, x + w - 6, y + 22, fill=(200, 30, 30))
    text(x + w - 32, y + 15, "11,254", F_ILL, WHITE, anchor="mm")
    text(x + w - 32, y + 26, "CASES", F_ILL, (120, 30, 30), anchor="ma")
    label_bar(x, y, w, h, "DR CONGO \u00b7 EBOLA")


def virus(cx, cy, r, col):
    for a in range(0, 360, 45):
        ex, ey = cx + r * 1.5 * math.cos(math.radians(a)), cy + r * 1.5 * math.sin(math.radians(a))
        line([(cx, cy), (ex, ey)], col, 1)
        circle(ex, ey, r * 0.25, fill=col)
    circle(cx, cy, r, fill=col)


def t_measles(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(246, 230, 230))
    for i, k in enumerate(["US", "MX", "BO"]):
        fx = x + 14 + i * 46
        flag(fx, y + 10, 36, 23, k)
        text(fx + 18, y + 36, {"US": "US", "MX": "MEXICO", "BO": "BOLIVIA"}[k], F_ILL, (90, 40, 40), anchor="ma")
    virus(x + w - 12, y + 10, 4, (190, 40, 40))
    label_bar(x, y, w, h, "PAHO \u00b7 MEASLES", fill=(140, 30, 30))


def t_mongolia(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(228, 234, 242))
    flag(x + 14, y + 10, 52, 32, "MN")
    rect(x + 86, y + 6, x + 140, y + 48, fill=WHITE, outline=(120, 120, 130), w=0.8)
    text(x + 113, y + 10, "RESIGNATION", font("arialbd.ttf", 6.5), INK, anchor="ma")
    for i in range(4):
        line([(x + 92, y + 22 + i * 6), (x + 134, y + 22 + i * 6)], (150, 150, 160), 1)
    label_bar(x, y, w, h, "ULAANBAATAR")


def t_alaska(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(226, 236, 246))
    cx, cy = x + 44, y + 30
    rect(cx - 22, cy, cx + 22, cy + 22, fill=(40, 70, 140))
    rect(cx - 10, cy, cx + 10, cy + 3, fill=WHITE)
    rect(cx - 9, cy - 20, cx + 9, cy + 1, fill=WHITE, outline=(40, 70, 140), w=1)
    line([(cx - 4, cy - 10), (cx - 1, cy - 6), (cx + 5, cy - 15)], (40, 70, 140), 2)
    rect(x + 82, y + 12, x + w - 8, y + 26, fill=(40, 70, 140))
    text(x + (82 + w - 8) / 2, y + 19, "PELTOLA (D)", F_ILL, WHITE, anchor="mm")
    rect(x + 82, y + 30, x + w - 8, y + 44, fill=(200, 200, 205))
    text(x + (82 + w - 8) / 2, y + 37, "SULLIVAN (R)", F_ILL, (60, 60, 60), anchor="mm")
    label_bar(x, y, w, h, "ALASKA \u00b7 US SENATE")


def t_summit(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(236, 232, 222))
    for i, k in enumerate(["US", "CN", "RU"]):
        fx = x + 10 + i * 40
        line([(fx, y + 8), (fx, y + 46)], (110, 90, 60), 1.5)
        flag(fx + 1, y + 8, 32, 21, k)
    rect(x + w - 40, y + 8, x + w - 8, y + 46, fill=WHITE, outline=(120, 120, 120), w=0.8)
    rect(x + w - 40, y + 8, x + w - 8, y + 18, fill=(200, 40, 40))
    text(x + w - 24, y + 13, "THU", F_ILL, WHITE, anchor="mm")
    text(x + w - 24, y + 32, "19", F_BADGE, INK, anchor="mm")
    label_bar(x, y, w, h, "SHENZHEN \u00b7 SET FOR THURSDAY")


def t_trade(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(232, 236, 228))
    flag(x + 10, y + 12, 40, 25, "CA")
    flag(x + w - 50, y + 12, 40, 25, "CN")
    line([(x + 58, y + 18), (x + w - 60, y + 18)], (60, 60, 60), 2)
    poly([(x + w - 60, y + 14), (x + w - 54, y + 18), (x + w - 60, y + 22)], fill=(60, 60, 60))
    line([(x + 64, y + 32), (x + w - 56, y + 32)], (60, 60, 60), 2)
    poly([(x + 64, y + 28), (x + 58, y + 32), (x + 64, y + 36)], fill=(60, 60, 60))
    text(x + w / 2, y + 36, "TARIFFS CUT", F_ILL, (60, 60, 60), anchor="ma")
    label_bar(x, y, w, h, "CARNEY \u2013 XI TALKS")


def t_bangladesh(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(232, 228, 220))
    poly([(x + 8, y + 52), (x + 8, y + 26), (x + 24, y + 18), (x + 24, y + 26), (x + 40, y + 18), (x + 40, y + 26),
          (x + 56, y + 18), (x + 56, y + 52)], fill=(120, 120, 128))
    rect(x + 44, y + 6, x + 50, y + 20, fill=(100, 100, 108))
    for i in range(14):
        cx = x + 66 + (i % 7) * 12
        cy = y + 40 + (i // 7) * 8
        circle(cx, cy - 4, 2.6, fill=(60, 40, 30))
        rect(cx - 3, cy - 1, cx + 3, cy + 5, fill=(170, 60, 60) if i % 3 else (60, 90, 150))
    rect(x + 70, y + 8, x + w - 6, y + 24, fill=WHITE, outline=(40, 120, 60), w=1)
    text(x + (70 + w - 6) / 2, y + 16, "TK 30,000 WAGE", F_ILL, (40, 120, 60), anchor="mm")
    label_bar(x, y, w, h, "DHAKA \u00b7 GARMENT BELT")


def t_westbank(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(236, 232, 224))
    flag(x + 10, y + 10, 46, 28, "GB")
    rect(x + 70, y + 6, x + 118, y + 50, fill=WHITE, outline=(120, 120, 120), w=0.8)
    for i in range(5):
        line([(x + 75, y + 13 + i * 6), (x + 113, y + 13 + i * 6)], (160, 160, 160), 1)
    d.rounded_rectangle([S(x + 84), S(y + 30), S(x + 150), S(y + 44)], radius=S(2), outline=(190, 30, 30), width=S(1.5))
    text(x + 117, y + 37, "SANCTIONS", F_ILL, (190, 30, 30), anchor="mm")
    label_bar(x, y, w, h, "WEST BANK SETTLEMENTS")


def t_serbia(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(232, 234, 240))
    cx, cy = x + w / 2 + 14, y + 48
    k = 0
    for ring, n in [(14, 9), (22, 13), (30, 17), (38, 21)]:
        for i in range(n):
            a = math.pi + i * math.pi / (n - 1)
            col = (40, 110, 200) if k % 9 < 5 else (200, 60, 60)
            circle(cx + ring * math.cos(a), cy + ring * math.sin(a), 2.2, fill=col)
            k += 1
    flag(x + 8, y + 8, 34, 22, "RS")
    label_bar(x, y, w, h, "BELGRADE \u00b7 NEW PARLIAMENT")


def t_robots(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(222, 234, 244))
    cx, cy = x + w / 2, y + 28
    rect(cx - 9, cy - 20, cx + 9, cy - 6, fill=(110, 116, 128))
    circle(cx - 4, cy - 13, 2, fill=(255, 80, 60))
    circle(cx + 4, cy - 13, 2, fill=(255, 80, 60))
    rect(cx - 12, cy - 4, cx + 12, cy + 16, fill=(110, 116, 128))
    rect(cx - 18, cy - 2, cx - 14, cy + 12, fill=(110, 116, 128))
    rect(cx + 14, cy - 2, cx + 18, cy + 12, fill=(110, 116, 128))
    circle(cx, cy - 2, 25, outline=(200, 30, 30), w=3)
    line([(cx - 18, cy + 16), (cx + 18, cy - 20)], (200, 30, 30), 3)
    text(x + 8, y + 6, "128", F_BADGE, (20, 60, 120))
    text(x + 8, y + 22, "STATES", F_ILL, (20, 60, 120))
    label_bar(x, y, w, h, "GENEVA \u00b7 TREATY TALKS")


def t_mozambique(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(234, 230, 220))
    flag(x + 12, y + 10, 50, 32, "MZ")
    # gavel
    gx, gy = x + 110, y + 26
    poly([(gx - 20, gy - 6), (gx + 4, gy - 22), (gx + 12, gy - 12), (gx - 12, gy + 4)], fill=(120, 70, 30))
    line([(gx - 2, gy - 4), (gx + 22, gy + 18)], (90, 50, 20), 4)
    rect(x + 90, y + 44, x + 140, y + 50, fill=(90, 50, 20))
    label_bar(x, y, w, h, "MAPUTO \u00b7 SUPREME COURT")


# ------------------------------------------------------------------ content
LEADS = [
    (ill_iran, "MIDDLE EAST", "IRAN WAR", "Bahrain says it downed Iranian drones; US hits Qeshm",
     "Third attempt in five days, Bahrain says; US jets struck a missile site on Iran's Qeshm Island."),
    (ill_bridge, "EUROPE", "UKRAINE WAR", "Crimean Bridge hit a second day; Russia says 2 dead",
     "Ukrainian drones struck the road link to Crimea; the Kremlin says it will be rebuilt."),
    (ill_quad, "ASIA", "DIPLOMACY", "Trump lands in Manila; Quad leaders back minerals deals",
     "US, India, Japan and Australia meet at ASEAN before talks with Xi and Putin in China."),
]

TILES = [
    (t_nvidia, "AMERICAS", "MARKETS", "Dow falls 849; Nvidia sales $115.8bn",
     "Nvidia reported after the close"),
    (t_ebola, "AFRICA", "HEALTH", "Ebola in DR Congo passes 11,000 cases",
     "5,505 deaths, Reuters tally"),
    (t_measles, "AMERICAS", "HEALTH", "US loses measles-free status, PAHO says",
     "Mexico and Bolivia too"),
    (t_mongolia, "ASIA", "POLITICS", "Mongolia's president says he will resign",
     "He denies graft claims"),
    (t_alaska, "AMERICAS", "ELECTIONS", "Peltola projected to unseat Sen. Sullivan",
     "Democrats gain Alaska seat"),
    (t_summit, "ASIA", "DIPLOMACY", "Trump, Xi and Putin to meet in Shenzhen",
     "Summit set for Thursday"),
    (t_trade, "AMERICAS", "TRADE", "Canada and China agree new tariff cuts",
     "After Carney\u2013Xi talks"),
    (t_bangladesh, "ASIA", "LABOUR", "Garment workers tear-gassed in Bangladesh",
     "37 factories shut"),
    (t_westbank, "MIDDLE EAST", "WEST BANK", "UK sanctions Israeli settlement firms",
     "8 firms; settlers kill woman, 72"),
    (t_serbia, "EUROPE", "POLITICS", "New Serbian parliament meets",
     "After student-led win"),
    (t_robots, "GLOBAL", "SECURITY", "128 states weigh a ban on killer robots",
     "US and Russia object"),
    (t_mozambique, "AFRICA", "JUSTICE", "Mozambique: Mondlane trial opens",
     "Opposition leader in court"),
]

# story number, (lon, lat) for map pins: leads then tiles
PIN_LL = [
    (50.6, 26.1), (35.5, 45.3), (121.0, 14.6),
    (-74.0, 40.7), (25.3, 0.5), (-98.0, 37.0), (106.9, 47.9), (-150.0, 63.0), (114.1, 22.5),
    (-90.0, 56.0), (90.4, 23.8), (35.4, 31.9), (20.5, 44.8), (6.1, 46.2), (32.6, -25.9),
]

# also-on-the-day list: region, bold lead, rest, (lon, lat)
ALSO = [
    ("MIDDLE EAST", "Gaza:", "Israeli strikes kill 5 despite ceasefire", (34.4, 31.4)),
    ("MIDDLE EAST", "Israel:", "Kahana elected Knesset speaker", (35.2, 31.8)),
    ("MIDDLE EAST", "Iraq:", "troops ring Kataib Hezbollah's Jurf al-Sakhar", (44.1, 32.8)),
    ("MIDDLE EAST", "Yemen:", "Houthis say Saudi strike kills 7 in Hudaydah", (42.9, 14.8)),
    ("MIDDLE EAST", "Oman:", "gas tanker hit offshore; 24 crew evacuated", (57.5, 23.0)),
    ("MIDDLE EAST", "Jordan and Iraq", "block Telegram", (36.0, 31.9)),
    ("EUROPE", "Prague:", "two trains collide; 46 injured", (14.4, 50.1)),
    ("EUROPE", "Turkey", "seizes opposition broadcaster S\u00f6zc\u00fc TV", (29.0, 41.0)),
    ("EUROPE", "Moldova:", "Russian drone over capital, Sandu says", (28.8, 47.0)),
    ("EUROPE", "Kyiv:", "Russian strikes damage two Dnipro bridges", (30.5, 50.4)),
    ("EUROPE", "France:", "public-sector unions strike over pay", (2.35, 48.85)),
    ("EUROPE", "N. Macedonia:", "5 held over Iran-linked plot", (21.4, 42.0)),
    ("EUROPE", "EU states and Rwanda", "plan an asylum 'return hub'", (30.1, -1.9)),
    ("EUROPE", "Kosovo:", "17 months added to Tha\u00e7i's sentence", (21.2, 42.7)),
    ("ASIA", "Russia:", "An-12 military plane crash kills 19", (86.1, 55.4)),
    ("ASIA", "Bangladesh:", "activists burn police station", (89.9, 22.9)),
    ("ASIA", "France and Malaysia", "sign rare-earths partnership", (101.7, 3.1)),
    ("ASIA", "Sheinbaum", "meets Xi in China ahead of APEC", (114.1, 22.6)),
    ("AFRICA", "Guinea:", "224 sentenced over illegal gold mining", (-9.2, 11.4)),
    ("AFRICA", "South Africa:", "two mass shootings kill 17", (28.2, -25.7)),
    ("AFRICA", "DR Congo:", "WFP says 2.3m in crisis hunger in east", (29.2, -1.7)),
    ("ASIA", "Japan", "protests Russian aircraft airspace breach", (130.4, 33.6)),
    ("AMERICAS", "Costa Rica:", "journalist shot dead, first in 25 years", (-84.1, 9.9)),
    ("AMERICAS", "Mexico:", "journalist found dead in Acapulco", (-99.9, 16.9)),
    ("AMERICAS", "Haiti:", "marches back Salvadoran troops", (-72.3, 18.5)),
    ("AMERICAS", "Pentagon", "fails its audit for a ninth year", (-77.1, 38.9)),
    ("AMERICAS", "Ecuadorian fishermen", "sue US over a boat strike", (-79.9, -2.2)),
    ("AMERICAS", "New York:", "Mamdani disbands NYPD protest unit", (-74.0, 40.7)),
    ("GLOBAL", "California", "sues OpenAI over AI safeguards", (-121.5, 38.6)),
    ("GLOBAL", "Apple:", "Pay and iCloud outage; firm rules out attack", (-122.0, 37.3)),
    ("GLOBAL", "WHO:", "superbugs could kill 39m by 2050", (6.1, 46.2)),
    ("GLOBAL", "COP31:", "EU lobbies China on IPCC timetable", (30.7, 36.9)),
    ("GLOBAL", "Football:", "Brazil 7\u20130 Singapore; Vin\u00edcius hat-trick", (103.8, 1.3)),
    ("GLOBAL", "Football:", "USA into Nations League semis", (-95.0, 30.0)),
    ("GLOBAL", "FIFA:", "UEFA backs Diallo to challenge Infantino", (8.5, 47.4)),
]

N_TOTAL = len(LEADS) + len(TILES) + len(ALSO)

# ------------------------------------------------------------------ masthead
rect(0, 0, W, 20, fill=NAVY)
text(12, 4.5, "THE WORLD'S NEWS IN ONE PAGE", F_KICK, WHITE)
text(W - 12, 4.5, f"{N_TOTAL} STORIES \u00b7 SIX CONTINENTS \u00b7 ONE DAY", F_KICK, WHITE, anchor="ra")
_size = 80
while width("Tuesday 17 November 2026", font("georgiab.ttf", _size)) > W - 36:
    _size -= 1
F_DATE = font("georgiab.ttf", _size)
text(W / 2, 92, "Tuesday 17 November 2026", F_DATE, INK, anchor="ms")
line([(12, 106), (W - 12, 106)], INK, 2.2)
line([(12, 109), (W - 12, 109)], INK, 0.8)
text(14, 114, "Every story here happened, or was first reported, on this day. Claims are attributed.", F_STRAP, (60, 60, 64))
bw = width(f"{N_TOTAL} STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY", F_BADGE) + 16
rect(W - 12 - bw, 113, W - 12, 130, fill=RED)
text(W - 12 - bw / 2, 121.5, f"{N_TOTAL} STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY", F_BADGE, WHITE, anchor="mm")

# ------------------------------------------------------------------ figures strip
FIGS = [
    ("\u2212849", "Dow points, to 50,759"),
    ("$115.8bn", "Nvidia quarterly sales"),
    ("11,254", "Ebola cases, DR Congo"),
    ("2nd day", "Crimean Bridge struck"),
    ("3rd", "Iran drone attempt in 5 days"),
    ("128", "states at robot-weapons talks"),
]
FY0, FY1 = 135, 173
rect(12, FY0, W - 12, FY1, fill=(238, 232, 218))
fw = (W - 24) / len(FIGS)
for i, (big, small) in enumerate(FIGS):
    cx = 12 + fw * (i + 0.5)
    text(cx, FY0 + 3, big, F_FIG, RED if i in (0, 3, 4) else NAVY, anchor="ma")
    text(cx, FY0 + 25, small, F_FIGL, GREY, anchor="ma")
    if i:
        line([(12 + fw * i, FY0 + 6), (12 + fw * i, FY1 - 6)], RULE, 1)

# ------------------------------------------------------------------ leads
LY = 180
LW = (W - 24 - 2 * 14) / 3
LIH = 112
lead_bottom = 0
for i, (ill, reg, beat, head, det) in enumerate(LEADS):
    x = 12 + i * (LW + 14)
    ill(x, LY, LW, LIH)
    rect(x, LY, x + LW, LIH + LY, outline=(60, 60, 60), w=0.6)
    ty = LY + LIH + 6
    circle(x + 7, ty + 6, 7, fill=RED)
    text(x + 7, ty + 6, str(i + 1), F_NUM, WHITE, anchor="mm")
    text(x + 19, ty + 1.5, f"{reg} \u00b7 {beat}", F_TAG, REG[reg])
    hy = ty + 16
    hh = para(x, hy, [(head, F_LHEAD, INK)], LW, 22, max_lines=2)
    dh = para(x, hy + hh + 2, [(det, F_LDET, (60, 60, 64))], LW, 14.5, max_lines=2)
    lead_bottom = max(lead_bottom, hy + hh + 2 + dh)

line([(12, lead_bottom + 6), (W - 12, lead_bottom + 6)], INK, 1)

# ------------------------------------------------------------------ tiles (2 rows of 6)
TY = lead_bottom + 13
TCOLS = 6
TG = 10
TW = (W - 24 - (TCOLS - 1) * TG) / TCOLS
TIH = 58
row_bottom = TY
for r in range(2):
    ry = row_bottom if r == 0 else row_bottom + 8
    bottom = ry
    for c in range(TCOLS):
        k = r * TCOLS + c
        ill, reg, beat, head, det = TILES[k]
        x = 12 + c * (TW + TG)
        ill(x, ry, TW, TIH)
        rect(x, ry, x + TW, ry + TIH, outline=(60, 60, 60), w=0.6)
        ty = ry + TIH + 4
        circle(x + 7, ty + 6, 7, fill=NAVY)
        text(x + 7, ty + 6, str(4 + k), F_NUM, WHITE, anchor="mm")
        text(x + 18, ty + 1.5, f"{reg} \u00b7 {beat}", F_TAG, REG[reg])
        hy = ty + 15
        hh = para(x, hy, [(head, F_THEAD, INK)], TW, 15, max_lines=3)
        dh = para(x, hy + hh + 1, [(det, F_TDET, (70, 70, 74))], TW, 12.5, max_lines=1)
        bottom = max(bottom, hy + hh + 1 + dh)
    row_bottom = bottom
    if r == 0:
        line([(12, row_bottom + 4), (W - 12, row_bottom + 4)], RULE, 1)

SEC_Y = row_bottom + 8
line([(12, SEC_Y), (W - 12, SEC_Y)], INK, 1.6)

# ------------------------------------------------------------------ map
FOOT_Y = H - 20
MX0, MY0 = 12, SEC_Y + 22
MW = 318
LON0, LON1, LAT0, LAT1 = -170.0, 180.0, -50.0, 74.0
MH = min(176, FOOT_Y - 34 - MY0)
text(MX0, SEC_Y + 6, "WHERE IT HAPPENED", F_SEC, RED)


def proj(lon, lat):
    return MX0 + (lon - LON0) / (LON1 - LON0) * MW, MY0 + (LAT1 - lat) / (LAT1 - LAT0) * MH


CONTINENTS = [
    [(-168, 66), (-162, 70), (-140, 70), (-120, 72), (-95, 74), (-80, 73), (-62, 60), (-56, 52), (-66, 45),
     (-70, 42), (-76, 35), (-81, 31), (-80, 25), (-82, 28), (-84, 30), (-90, 29), (-97, 27), (-97, 22),
     (-92, 18), (-88, 21), (-87, 15), (-83, 10), (-79, 9), (-80, 7), (-85, 10), (-92, 14), (-105, 20),
     (-110, 24), (-112, 30), (-117, 33), (-124, 40), (-124, 48), (-132, 55), (-140, 60), (-150, 60),
     (-158, 57), (-165, 60)],
    [(-55, 60), (-44, 60), (-20, 70), (-20, 74), (-72, 74), (-72, 77), (-60, 70)],
    [(-80, 9), (-75, 11), (-62, 11), (-52, 5), (-35, -5), (-35, -9), (-39, -15), (-41, -22), (-48, -26),
     (-53, -34), (-58, -38), (-63, -41), (-65, -47), (-69, -50), (-75, -50), (-73, -40), (-71, -30),
     (-70, -18), (-76, -14), (-81, -5), (-80, 0), (-77, 4)],
    [(-10, 36), (-9, 43), (-2, 44), (-4, 48), (2, 51), (8, 54), (10, 57), (5, 62), (15, 69), (28, 71),
     (40, 67), (60, 69), (70, 73), (80, 73), (100, 74), (115, 73), (130, 71), (140, 72), (160, 70),
     (180, 68), (180, 65), (170, 60), (162, 58), (156, 51), (142, 59), (135, 55), (140, 48), (130, 42),
     (127, 39), (126, 35), (120, 40), (122, 32), (119, 25), (110, 21), (108, 16), (109, 12), (105, 9),
     (101, 13), (100, 7), (104, 1), (98, 8), (97, 17), (92, 22), (88, 22), (80, 15), (78, 8), (73, 18),
     (67, 25), (57, 25), (52, 28), (48, 30), (50, 26), (51, 24), (56, 25), (59, 22), (52, 16), (44, 12),
     (42, 16), (39, 22), (35, 28), (34, 31), (36, 36), (30, 36), (27, 40), (23, 40), (22, 37), (20, 40),
     (19, 42), (13, 45), (17, 40), (16, 38), (12, 42), (8, 44), (3, 43), (0, 39), (-5, 36)],
    [(-17, 21), (-17, 15), (-12, 8), (-8, 4), (5, 5), (9, 4), (9, -1), (13, -6), (12, -17), (15, -27),
     (18, -34), (25, -34), (32, -28), (35, -24), (41, -15), (40, -10), (39, -5), (44, 2), (51, 11), (43, 12),
     (38, 18), (33, 28), (32, 31), (20, 32), (10, 37), (0, 36), (-6, 36), (-10, 30), (-15, 27)],
    [(114, -22), (122, -18), (130, -12), (137, -12), (142, -11), (146, -19), (153, -27), (150, -37),
     (141, -38), (135, -35), (130, -32), (115, -34), (113, -26)],
    [(-5, 50), (1, 51), (2, 53), (-2, 56), (-4, 58.5), (-6, 57), (-5, 54), (-3, 54), (-5, 52)],
    [(-10, 52), (-6, 52), (-6, 55), (-8, 55), (-10, 54)],
    [(130, 31), (132, 34), (136, 34), (140, 35), (141, 40), (142, 43), (145, 44), (141, 45), (140, 42),
     (139, 38), (136, 36), (131, 34)],
    [(95, 5), (98, 4), (104, -2), (106, -6), (102, -4), (97, 1)],
    [(109, 2), (112, 3), (117, 7), (119, 5), (117, 1), (116, -4), (111, -3), (109, -1)],
    [(131, -1), (138, -2), (145, -5), (151, -10), (143, -9), (138, -8), (132, -4)],
    [(105, -6), (115, -8), (110, -8)],
    [(120, 18), (122, 18), (124, 13), (126, 7), (122, 7), (121, 13)],
    [(44, -25), (47, -25), (50, -15), (49, -12), (44, -17)],
    [(172, -34), (178, -38), (174, -41), (167, -46), (171, -44)],
    [(-24, 64), (-14, 64), (-14, 66), (-22, 66.5)],
]

rect(MX0, MY0, MX0 + MW, MY0 + MH, fill=SEA)
for c in CONTINENTS:
    poly([proj(lo, la) for lo, la in c], fill=LAND, outline=(176, 164, 140))
for _, _, _, (lo, la) in ALSO:
    px, py = proj(lo, la)
    circle(px, py, 2.3, fill=(110, 110, 116), outline=WHITE, w=0.5)
for i, (lo, la) in enumerate(PIN_LL):
    px, py = proj(lo, la)
    col = RED if i < 3 else NAVY
    r = 6.5 if i < 3 else 6
    circle(px, py, r, fill=col, outline=WHITE, w=0.8)
    text(px, py, str(i + 1), font("arialbd.ttf", 8.5 if i >= 9 else 9.5), WHITE, anchor="mm")
rect(MX0, MY0, MX0 + MW, MY0 + MH, outline=(80, 80, 80), w=0.8)
ly = MY0 + MH + 6
circle(MX0 + 6, ly + 5, 5, fill=RED)
text(MX0 + 14, ly, "Lead stories 1\u20133", F_TDET, GREY)
circle(MX0 + 112, ly + 5, 5, fill=NAVY)
text(MX0 + 120, ly, "Stories 4\u201315", F_TDET, GREY)
circle(MX0 + 204, ly + 5, 2.5, fill=(110, 110, 116))
text(MX0 + 210, ly, "Also on Tuesday", F_TDET, GREY)

# ------------------------------------------------------------------ also list (two columns)
AX0 = MX0 + MW + 16
text(AX0, SEC_Y + 6, "ALSO ON TUESDAY 17 NOVEMBER", F_SEC, RED)
ACOLS = 2
AGAP = 14
AW = (W - 12 - AX0 - AGAP) / ACOLS
ALH = 15.2
AY0 = SEC_Y + 22
AMAX = FOOT_Y - 6
# list columns: two to the right of the map, then one under the map
UNDER_Y = ly + 18
line([(MX0, UNDER_Y - 5), (MX0 + MW, UNDER_Y - 5)], RULE, 1)
LCOLS = [(AX0, AY0, AW), (AX0 + AW + AGAP, AY0, AW), (MX0, UNDER_Y, MW)]
col, y = 0, AY0
for idx, (reg, b, r, _) in enumerate(ALSO):
    n = len(LEADS) + len(TILES) + idx + 1
    lines = wrap([(b, F_LIB, INK), (r, F_LIR, INK)], LCOLS[col][2] - 26)
    hgt = len(lines) * ALH + 3
    if y + hgt > AMAX:
        col += 1
        if col >= len(LCOLS):
            print("WARNING: also list overflow at", idx, file=sys.stderr)
            break
        y = LCOLS[col][1]
        lines = wrap([(b, F_LIB, INK), (r, F_LIR, INK)], LCOLS[col][2] - 26)
    x = LCOLS[col][0]
    rect(x, y + 0.5, x + 20, y + 12.5, fill=REG[reg])
    text(x + 10, y + 6.5, str(n), font("arialbd.ttf", 9), WHITE, anchor="mm")
    draw_lines(x + 26, y, lines, ALH)
    y += hgt
line([(AX0 + AW + AGAP / 2, AY0), (AX0 + AW + AGAP / 2, AMAX)], RULE, 1)
line([(AX0 - 8, SEC_Y + 6), (AX0 - 8, AMAX)], RULE, 1)

# region key under the list
# ------------------------------------------------------------------ footer
rect(0, FOOT_Y, W, H, fill=NAVY)
text(12, FOOT_Y + 5, "Sources: Reuters, AP, AFP, BBC, Al Jazeera, Anadolu, NYT, PAHO. Claims attributed. Original drawings.", F_FOOT, (230, 232, 238))
kx = W - 12
for name in reversed(list(REG)):
    tw = width(name, F_TAG)
    kx -= tw + 14
    rect(kx, FOOT_Y + 5, kx + 8, FOOT_Y + 13, fill=REG[name])
    text(kx + 11, FOOT_Y + 5, name, F_TAG, (230, 232, 238))

# ------------------------------------------------------------------ save
out = img.resize((W, H), Image.LANCZOS)
pal = out.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
pal.save(dest, optimize=True)
print("wrote", os.path.normpath(dest), os.path.getsize(dest), "bytes;", N_TOTAL, "stories")
