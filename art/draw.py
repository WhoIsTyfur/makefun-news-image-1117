"""Draw the front page for Tuesday 17 November 2026 into entry.png (1024x1024).

Run from the repo root:  python art/draw.py
Needs Pillow and the Windows fonts (Georgia, Arial). The output PNG is committed;
main.py only copies it, so the graded run needs neither.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SCALE = 2  # draw at 2x, downsample for clean edges
FONT_DIR = r"C:\Windows\Fonts"

BG = (247, 243, 234)
INK = (24, 24, 28)
GREY = (90, 90, 96)
RED = (178, 34, 34)
NAVY = (24, 46, 82)
LAND = (214, 205, 186)
SEA = (226, 233, 238)
GOLD = (196, 140, 30)

REGION_COLOURS = {
    "Middle East": (178, 34, 34),
    "Europe": (36, 84, 160),
    "Asia-Pacific": (190, 110, 20),
    "Africa": (60, 130, 60),
    "Americas": (120, 60, 140),
    "Tech, science, health, climate": (20, 120, 130),
    "Sport": (90, 90, 96),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size * SCALE)


img = Image.new("RGB", (W * SCALE, H * SCALE), BG)
d = ImageDraw.Draw(img)


def S(v):
    return int(round(v * SCALE))


def text(x, y, s, f, fill=INK, anchor="la"):
    d.text((S(x), S(y)), s, font=f, fill=fill, anchor=anchor)


def width(s, f):
    return d.textlength(s, font=f) / SCALE


def rect(x0, y0, x1, y1, fill=None, outline=None, w=1):
    d.rectangle([S(x0), S(y0), S(x1), S(y1)], fill=fill, outline=outline, width=S(w) if outline else 0)


def line(pts, fill=INK, w=1):
    d.line([(S(x), S(y)) for x, y in pts], fill=fill, width=max(1, S(w)))


def poly(pts, fill=None, outline=None):
    d.polygon([(S(x), S(y)) for x, y in pts], fill=fill, outline=outline)


def circle(cx, cy, r, fill=None, outline=None, w=1):
    d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill=fill, outline=outline,
              width=S(w) if outline else 0)


def wrap_rich(segments, max_w):
    """segments: list of (text, font, colour). Returns lines of [(word, font, colour)]."""
    words = []
    for s, f, c in segments:
        for i, wd in enumerate(s.split(" ")):
            if wd:
                words.append((wd, f, c))
    lines, cur, cur_w = [], [], 0.0
    for wd, f, c in words:
        sp = width(" ", f) if cur else 0
        ww = width(wd, f)
        if cur and cur_w + sp + ww > max_w:
            lines.append(cur)
            cur, cur_w = [], 0.0
            sp = 0
        cur.append((wd, f, c))
        cur_w += sp + ww
    if cur:
        lines.append(cur)
    return lines


def draw_rich(x, y, segments, max_w, lh):
    lines = wrap_rich(segments, max_w)
    for i, ln in enumerate(lines):
        cx = x
        for j, (wd, f, c) in enumerate(ln):
            if j:
                cx += width(" ", f)
            text(cx, y + i * lh, wd, f, c)
            cx += width(wd, f)
    return len(lines) * lh


# ---------------------------------------------------------------- masthead
F_KICK = font("arialbd.ttf", 12)
F_DATE = font("georgiab.ttf", 56)
F_SUB = font("arial.ttf", 14)
F_SUBB = font("arialbd.ttf", 14)

rect(0, 0, W, 24, fill=NAVY)
text(12, 5, "THE WORLD IN ONE PAGE", F_KICK, (255, 255, 255))
text(W - 12, 5, "EVENTS OF ONE DAY, ANY TIME ZONE", F_KICK, (255, 255, 255), anchor="ra")
text(W / 2, 30, "TUESDAY 17 NOVEMBER 2026", F_DATE, INK, anchor="ma")
line([(12, 96), (W - 12, 96)], INK, 2)
sub = "52 stories  \u00b7  6 continents  \u00b7  numbered on the map  \u00b7  as reported by AP, Reuters, AFP, BBC, Al Jazeera"
text(W / 2, 101, sub, F_SUB, GREY, anchor="ma")
line([(12, 121), (W - 12, 121)], INK, 1)

# ---------------------------------------------------------------- lead row
F_LEAD = font("arialbd.ttf", 15)
F_LEADN = font("arialbd.ttf", 16)
F_DET = font("arial.ttf", 12)
F_ILL = font("arialbd.ttf", 11)

PX0, PY0, PW, PIH = 12, 128, 244, 112
GAP = (W - 24 - 4 * PW) / 3


def ill_bahrain(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(28, 36, 60))
    for i in range(18):  # stars
        sx = x + (i * 53) % w
        sy = y + (i * 29) % (h - 50) + 4
        circle(sx, sy, 0.8, fill=(220, 220, 240))
    poly([(x, y + h - 22), (x + w, y + h - 22), (x + w, y + h), (x, y + h)], fill=(196, 170, 120))
    # radar dish
    bx, by = x + 60, y + h - 22
    line([(bx, by), (bx, by - 22)], (230, 230, 230), 3)
    d.chord([S(bx - 20), S(by - 44), S(bx + 20), S(by - 8)], 200, 340, fill=(235, 235, 235))
    # drones with trails, intercept bursts
    for k, (dx, dy) in enumerate([(w - 40, 22), (w - 80, 40), (w - 120, 18)]):
        ox, oy = x + dx, y + dy
        line([(ox, oy), (ox + 40, oy - 10)], (240, 120, 60), 2)
        poly([(ox - 9, oy + 2), (ox + 3, oy - 5), (ox + 1, oy + 5)], fill=(230, 230, 230))
    for ex, ey in [(x + 110, y + 34), (x + 150, y + 52)]:
        for a in range(0, 360, 30):
            r1, r2 = 4, 11
            line([(ex + r1 * math.cos(math.radians(a)), ey + r1 * math.sin(math.radians(a))),
                  (ex + r2 * math.cos(math.radians(a)), ey + r2 * math.sin(math.radians(a)))], (255, 210, 80), 2)
    text(x + 6, y + h - 17, "BAHRAIN \u00b7 SHEIKH ISA AIR BASE", F_ILL, (40, 30, 10))


def ill_bridge(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(200, 214, 226))
    rect(x, y + h - 34, x + w, y + h, fill=(70, 110, 150))
    deck = y + h - 50
    # left and right deck, broken in the middle
    rect(x, deck, x + w * 0.42, deck + 6, fill=(60, 60, 64))
    rect(x + w * 0.58, deck, x + w, deck + 6, fill=(60, 60, 64))
    poly([(x + w * 0.42, deck), (x + w * 0.42, deck + 6), (x + w * 0.5, deck + 30), (x + w * 0.47, deck + 32)],
         fill=(60, 60, 64))
    for px in [0.1, 0.25, 0.75, 0.9]:
        rect(x + w * px - 3, deck + 6, x + w * px + 3, y + h - 34, fill=(80, 80, 84))
    # arch
    d.arc([S(x + w * 0.6), S(deck - 30), S(x + w * 0.98), S(deck + 30)], 180, 360, fill=(90, 90, 96), width=S(3))
    # smoke
    for i, (sx, sy, r) in enumerate([(0.5, -8, 14), (0.47, -24, 16), (0.53, -40, 18), (0.49, -58, 15)]):
        g = 90 + i * 25
        circle(x + w * sx, deck + sy, r, fill=(g, g, g))
    circle(x + w * 0.5, deck + 2, 8, fill=(240, 140, 40))
    text(x + 6, y + 5, "KERCH STRAIT \u00b7 CRIMEA", F_ILL, (30, 40, 60))


def flag(x, y, w, h, kind):
    if kind == "US":
        for i in range(7):
            rect(x, y + i * h / 7, x + w, y + (i + 0.5) * h / 7, fill=(190, 30, 45))
            rect(x, y + (i + 0.5) * h / 7, x + w, y + (i + 1) * h / 7, fill=(255, 255, 255))
        rect(x, y, x + w * 0.42, y + h * 0.54, fill=(30, 50, 110))
    elif kind == "IN":
        rect(x, y, x + w, y + h / 3, fill=(255, 153, 51))
        rect(x, y + h / 3, x + w, y + 2 * h / 3, fill=(255, 255, 255))
        rect(x, y + 2 * h / 3, x + w, y + h, fill=(19, 136, 8))
        circle(x + w / 2, y + h / 2, h / 8, outline=(0, 0, 128), w=1.5)
    elif kind == "JP":
        rect(x, y, x + w, y + h, fill=(255, 255, 255))
        circle(x + w / 2, y + h / 2, h * 0.3, fill=(188, 0, 45))
    elif kind == "AU":
        rect(x, y, x + w, y + h, fill=(0, 40, 120))
        line([(x, y), (x + w / 2, y + h / 2)], (255, 255, 255), 3)
        line([(x + w / 2, y), (x, y + h / 2)], (255, 255, 255), 3)
        line([(x + w / 4, y), (x + w / 4, y + h / 2)], (200, 16, 46), 3)
        line([(x, y + h / 4), (x + w / 2, y + h / 4)], (200, 16, 46), 3)
        for sx, sy in [(0.75, 0.3), (0.85, 0.55), (0.7, 0.75), (0.25, 0.78)]:
            circle(x + w * sx, y + h * sy, 2, fill=(255, 255, 255))
    rect(x, y, x + w, y + h, outline=(60, 60, 60), w=0.6)


def ill_quad(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(232, 226, 210))
    fw, fh = 46, 30
    for i, k in enumerate(["US", "IN", "JP", "AU"]):
        fx = x + 12 + i * (fw + 12)
        line([(fx, y + 14), (fx, y + 62)], (110, 90, 60), 2)
        flag(fx + 1, y + 14, fw, fh, k)
    # table and mineral rocks
    rect(x + 8, y + h - 40, x + w - 8, y + h - 30, fill=(120, 80, 40))
    for i, (rx, c) in enumerate([(0.3, (120, 120, 130)), (0.45, (170, 120, 70)), (0.6, (90, 110, 120)),
                                 (0.75, (150, 150, 160))]):
        poly([(x + w * rx - 12, y + h - 40), (x + w * rx - 6, y + h - 54), (x + w * rx + 6, y + h - 56),
              (x + w * rx + 12, y + h - 40)], fill=c)
    text(x + 6, y + h - 22, "MANILA \u00b7 QUAD SUMMIT", F_ILL, (60, 40, 20))


def ill_markets(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(18, 22, 30))
    for gy in range(1, 5):
        line([(x, y + gy * h / 5), (x + w, y + gy * h / 5)], (45, 55, 70), 1)
    pts = []
    vals = [0.25, 0.2, 0.3, 0.26, 0.35, 0.33, 0.45, 0.5, 0.48, 0.62, 0.7, 0.78, 0.74, 0.86]
    for i, v in enumerate(vals):
        pts.append((x + 8 + i * (w - 70) / (len(vals) - 1), y + 12 + v * (h - 30)))
    line(pts, (235, 70, 60), 3)
    ax, ay = pts[-1]
    poly([(ax - 7, ay - 4), (ax + 7, ay - 4), (ax, ay + 8)], fill=(235, 70, 60))
    F_BIG = font("arialbd.ttf", 22)
    text(x + w - 8, y + 10, "DOW", F_ILL, (200, 200, 210), anchor="ra")
    text(x + w - 8, y + 24, "\u2212849", F_BIG, (235, 70, 60), anchor="ra")
    text(x + w - 8, y + 50, "\u22121.6%", F_ILL, (235, 70, 60), anchor="ra")
    text(x + 6, y + h - 16, "WALL STREET \u00b7 NEW YORK", F_ILL, (200, 200, 210))


LEADS = [
    (ill_bahrain, "1", "Iran fires drones at US base in Bahrain; US strikes Qeshm Island",
     "Bahrain intercepts them: third attempt in five days"),
    (ill_bridge, "2", "Ukraine hits Crimea's Kerch bridge a second day; 2 killed",
     "Traffic halted; Kremlin vows to rebuild"),
    (ill_quad, "3", "Trump in Manila: Quad leaders back critical-minerals deals",
     "US, India, Japan, Australia meet before APEC"),
    (ill_markets, "4", "Wall Street slides: Dow \u2212849 to 50,759; S&P at July low",
     "AI and chip stocks lead a broad sell-off"),
]

for i, (ill, n, head, det) in enumerate(LEADS):
    x = PX0 + i * (PW + GAP)
    ill(x, PY0, PW, PIH)
    rect(x, PY0, x + PW, PY0 + PIH, outline=INK, w=1)
    circle(x + 14, PY0 + PIH + 14, 10, fill=RED)
    text(x + 14, PY0 + PIH + 14, n, F_LEADN, (255, 255, 255), anchor="mm")
    hgt = draw_rich(x + 30, PY0 + PIH + 5, [(head, F_LEAD, INK)], PW - 30, 18)
    draw_rich(x + 30, PY0 + PIH + 7 + hgt, [(det, F_DET, GREY)], PW - 30, 14)

LEAD_BOTTOM = PY0 + PIH + 84
line([(12, LEAD_BOTTOM), (W - 12, LEAD_BOTTOM)], INK, 1)

# ---------------------------------------------------------------- world map
MX0, MY0, MW = 12, LEAD_BOTTOM + 8, 500
LON0, LON1, LAT0, LAT1 = -170.0, 180.0, -56.0, 78.0
MH = MW * (LAT1 - LAT0) / (LON1 - LON0)


def proj(lon, lat):
    return MX0 + (lon - LON0) / (LON1 - LON0) * MW, MY0 + (LAT1 - lat) / (LAT1 - LAT0) * MH


CONTINENTS = [
    [(-168, 66), (-162, 70), (-140, 70), (-120, 72), (-95, 74), (-80, 73), (-62, 60), (-56, 52), (-66, 45),
     (-70, 42), (-76, 35), (-81, 31), (-80, 25), (-82, 28), (-84, 30), (-90, 29), (-97, 27), (-97, 22),
     (-92, 18), (-88, 21), (-87, 15), (-83, 10), (-79, 9), (-80, 7), (-85, 10), (-92, 14), (-105, 20),
     (-110, 24), (-112, 30), (-117, 33), (-124, 40), (-124, 48), (-132, 55), (-140, 60), (-150, 60),
     (-158, 57), (-165, 60)],
    [(-55, 60), (-44, 60), (-20, 70), (-20, 78), (-40, 78), (-60, 78), (-72, 77), (-60, 70)],
    [(-80, 9), (-75, 11), (-62, 11), (-52, 5), (-35, -5), (-35, -9), (-39, -15), (-41, -22), (-48, -26),
     (-53, -34), (-58, -38), (-63, -41), (-65, -47), (-69, -52), (-75, -50), (-73, -40), (-71, -30),
     (-70, -18), (-76, -14), (-81, -5), (-80, 0), (-77, 4)],
    [(-10, 36), (-9, 43), (-2, 44), (-4, 48), (2, 51), (8, 54), (10, 57), (5, 62), (15, 69), (28, 71),
     (40, 67), (60, 69), (70, 73), (80, 73), (100, 77), (115, 73), (130, 71), (140, 72), (160, 70),
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
    poly([proj(lo, la) for lo, la in c], fill=LAND, outline=(170, 160, 140))
rect(MX0, MY0, MX0 + MW, MY0 + MH, outline=INK, w=1)

# pins: (story number, lon, lat, label dx, dy)
PINS = [
    ("1", 50.6, 26.1, 10, 8), ("2", 36.5, 45.3, 10, -10), ("3", 121.0, 14.6, 10, 6), ("4", -74.0, 40.7, 10, -8),
    ("5", -100, 38, -26, 8), ("6", 106.9, 47.9, 0, -14), ("7", 25.0, -2.0, 10, 4), ("8", -150, 62, 10, 6),
    ("9", 114.1, 22.5, 10, 10), ("10", 116.4, 39.9, 10, -6),
]
F_PIN = font("arialbd.ttf", 10)


def draw_pin(n, lo, la, dx, dy):
    px, py = proj(lo, la)
    circle(px, py, 3.2, fill=RED, outline=(255, 255, 255), w=0.8)
    lx, ly = px + dx, py + dy
    tw = width(n, F_PIN)
    rect(lx - tw / 2 - 2, ly - 6, lx + tw / 2 + 2, ly + 6, fill=(255, 255, 255), outline=RED, w=0.6)
    text(lx, ly, n, F_PIN, RED, anchor="mm")


for _p in PINS:
    draw_pin(*_p)

F_MAPCAP = font("arial.ttf", 11)
text(MX0 + 4, MY0 + MH + 3, "Numbers match the stories on this page", F_MAPCAP, GREY)
MAP_BOTTOM = MY0 + MH + 16

# ---------------------------------------------------------------- second-tier tiles with icons
TX0 = MX0 + MW + 12
TW = (W - 12 - TX0 - 8) / 2
TH = (MAP_BOTTOM - MY0 - 8) / 3
F_TILE = font("arialbd.ttf", 13)


def icon_virus(cx, cy, col):
    for a in range(0, 360, 40):
        line([(cx, cy), (cx + 15 * math.cos(math.radians(a)), cy + 15 * math.sin(math.radians(a)))], col, 2)
        circle(cx + 15 * math.cos(math.radians(a)), cy + 15 * math.sin(math.radians(a)), 2.5, fill=col)
    circle(cx, cy, 10, fill=col)
    circle(cx - 3, cy - 3, 2.5, fill=(255, 255, 255))


def icon_ebola(cx, cy, col):
    pts = [(cx - 16 + i * 2, cy + 8 * math.sin(i * 0.45)) for i in range(15)]
    line(pts, col, 4)
    d.arc([S(cx + 8), S(cy - 14), S(cx + 20), S(cy - 2)], 90, 360, fill=col, width=S(4))


def icon_resign(cx, cy, col):
    rect(cx - 13, cy - 16, cx + 11, cy + 14, fill=(255, 255, 255), outline=col, w=1.5)
    for i in range(4):
        line([(cx - 9, cy - 9 + i * 6), (cx + 7, cy - 9 + i * 6)], col, 1.2)
    line([(cx - 2, cy + 18), (cx + 16, cy - 2)], (40, 40, 40), 2.5)


def icon_ballot(cx, cy, col):
    rect(cx - 16, cy - 2, cx + 16, cy + 16, fill=col)
    rect(cx - 8, cy - 2, cx + 8, cy + 1, fill=(255, 255, 255))
    rect(cx - 7, cy - 18, cx + 7, cy, fill=(255, 255, 255), outline=col, w=1.2)
    line([(cx - 3, cy - 10), (cx, cy - 6), (cx + 5, cy - 14)], col, 2)


def icon_trade(cx, cy, col):
    rect(cx - 16, cy - 6, cx + 4, cy + 12, fill=(176, 130, 80), outline=(110, 80, 40), w=1)
    line([(cx - 16, cy + 3), (cx + 4, cy + 3)], (110, 80, 40), 1)
    line([(cx - 4, cy - 14), (cx + 16, cy - 14)], col, 2.5)
    poly([(cx + 16, cy - 19), (cx + 22, cy - 14), (cx + 16, cy - 9)], fill=col)
    line([(cx + 20, cy + 4), (cx + 8, cy + 4)], col, 2.5)
    poly([(cx + 8, cy - 1), (cx + 2, cy + 4), (cx + 8, cy + 9)], fill=col)


def icon_summit(cx, cy, col):
    for i, dx in enumerate([-12, 0, 12]):
        circle(cx + dx, cy - 6, 5, fill=col)
        d.chord([S(cx + dx - 8), S(cy), S(cx + dx + 8), S(cy + 18)], 180, 360, fill=col)
    rect(cx - 20, cy + 9, cx + 20, cy + 13, fill=(110, 80, 40))


TILES = [
    (icon_virus, "5", "US, Mexico and Bolivia lose measles-free status, PAHO says"),
    (icon_resign, "6", "Mongolia's president says he will resign over graft claims"),
    (icon_ebola, "7", "DR Congo Ebola: 11,254 cases, 5,505 deaths, Reuters tally"),
    (icon_ballot, "8", "Alaska: Democrat Peltola projected to unseat Sen. Sullivan"),
    (icon_trade, "9", "Canada and China agree new tariff cuts at Carney\u2013Xi talks"),
    (icon_summit, "10", "Kremlin: first Putin\u2013Trump\u2013Xi summit set for Shenzhen"),
]
for i, (ic, n, s) in enumerate(TILES):
    cx = TX0 + (i % 2) * (TW + 8)
    cy = MY0 + (i // 2) * (TH + 4)
    rect(cx, cy, cx + TW, cy + TH, fill=(255, 252, 245), outline=(180, 170, 150), w=1)
    ic(cx + 28, cy + TH / 2, NAVY)
    circle(cx + 10, cy + 10, 8, fill=RED)
    text(cx + 10, cy + 10, n, F_PIN, (255, 255, 255), anchor="mm")
    lines = wrap_rich([(s, F_TILE, INK)], TW - 64)
    lh = 16
    ty = cy + (TH - len(lines) * lh) / 2
    draw_rich(cx + 56, ty, [(s, F_TILE, INK)], TW - 64, lh)

SEC_TOP = max(MAP_BOTTOM, MY0 + 3 * TH + 8) + 6
line([(12, SEC_TOP), (W - 12, SEC_TOP)], INK, 2)

# ---------------------------------------------------------------- region columns
SECTIONS = [
    ("Middle East", [
        ("11", "West Bank:", "settlers kill woman, 72, near Jericho"),
        ("12", "UK", "sanctions 8 Israeli settlement builders"),
        ("13", "Gaza:", "Israeli strikes kill 5 despite truce"),
        ("14", "Israel:", "Knesset elects Kahana speaker, ousting Likud's Ohana"),
        ("15", "Iraq:", "troops surround Kataib Hezbollah base"),
        ("16", "Yemen:", "Houthis say Saudi strike kills 7 in Hudaydah"),
        ("17", "Oman:", "gas tanker hit offshore; 24 crew evacuated"),
        ("18", "Jordan and Iraq", "block Telegram"),
    ]),
    ("Africa", [
        ("34", "Mozambique:", "opposition leader Mondlane's trial opens"),
        ("35", "Guinea:", "224 sentenced over illegal gold mining"),
        ("36", "South Africa:", "two mass shootings kill 17"),
    ]),
    ("Europe", [
        ("19", "Serbia:", "new parliament sits after student movement's win"),
        ("20", "Prague:", "train collision injures 46"),
        ("21", "Turkey", "seizes opposition channel S\u00f6zc\u00fc TV"),
        ("22", "Moldova:", "Sandu says Russian drone flew over Chi\u0219in\u0103u"),
        ("23", "Kyiv:", "Russian strikes damage two Dnipro bridges"),
        ("24", "N. Macedonia", "arrests 5 in alleged Iran-linked murder plot"),
        ("25", "Five EU states", "and Rwanda plan asylum 'return hub'"),
        ("26", "Kosovo:", "Tha\u00e7i gets 17 more months for obstruction"),
        ("27", "IMF:", "Ukraine could get $1.6bn more"),
        ("0", "Bosnia:", "new three-member presidency takes office"),
    ]),
    ("Asia-Pacific", [
        ("28", "Bangladesh:", "police clash with garment workers; 37 factories shut"),
        ("29", "Bangladesh:", "Awami League activists burn police station"),
        ("30", "France and Malaysia", "sign rare-earths partnership"),
        ("31", "Mexico's Sheinbaum", "meets Xi in China"),
        ("32", "Geneva:", "128 states weigh ban on killer robots"),
    ]),
    ("Americas", [
        ("37", "Costa Rica:", "journalist shot dead, first in 25 years"),
        ("38", "Mexico:", "journalist found dead in Acapulco"),
        ("39", "Haiti:", "marches back Salvadoran troops fighting gangs"),
        ("40", "Pentagon", "fails its audit for a 9th year"),
        ("41", "Ecuadorian fishermen", "sue US over boat strike"),
        ("42", "New York:", "Mayor Mamdani disbands NYPD protest unit"),
    ]),
    ("Tech, science, health, climate", [
        ("43", "California", "sues OpenAI over AI safeguards"),
        ("44", "US", "curbs overseas data centres serving China"),
        ("45", "Study:", "big US data centres emit as much as Denmark"),
        ("46", "Apple", "outage hits Apple Pay and iCloud"),
        ("47", "COP31", "climate talks in Antalya near the end"),
        ("48", "WHO:", "superbugs could kill 39m by 2050"),
    ]),
    ("Sport", [
        ("49", "Football:", "Brazil 7\u20130 Singapore; Vin\u00edcius hat-trick"),
        ("50", "USA", "reach Concacaf Nations League semis"),
        ("51", "FIFA:", "UEFA backs Diallo to challenge Infantino"),
        ("52", "Crystal Palace", "appoint Thomas Frank"),
    ]),
]

# number every listed story in reading order, after the ten top stories
_num = 11
NUMBER_OF = {}
for _name, _items in SECTIONS:
    for _k, (_n, _b, _r) in enumerate(_items):
        _items[_k] = (str(_num), _b, _r)
        NUMBER_OF[_b] = str(_num)
        _num += 1
TOTAL_STORIES = _num - 1

# pins for listed stories, keyed by their bold lead (drawn here, after numbering)
REGION_PINS = [
    ("West Bank:", 35.4, 31.9, -14, 10), ("Iraq:", 44.3, 32.6, 10, -14), ("Serbia:", 20.5, 44.8, -14, -10),
    ("Prague:", 14.4, 50.1, -16, -8), ("Bangladesh:", 90.4, 23.8, 0, 14), ("Mozambique:", 32.6, -25.9, 10, 4),
    ("Guinea:", -13.7, 9.5, -14, 8), ("Costa Rica:", -84.1, 9.9, -16, 6), ("Haiti:", -72.3, 18.5, 10, 2),
    ("COP31", 30.7, 36.9, 0, -14), ("Football:", 103.8, 1.3, 0, 14), ("South Africa:", 28.0, -26.2, -16, 6),
]
for b, lo, la, dx, dy in REGION_PINS:
    draw_pin(NUMBER_OF[b], lo, la, dx, dy)

F_SEC = font("arialbd.ttf", 12)
F_ITB = font("arialbd.ttf", 13)
F_IT = font("arial.ttf", 13)
F_NUM = font("arialbd.ttf", 11)
NCOL = 4
COL_GAP = 12
CW = (W - 24 - (NCOL - 1) * COL_GAP) / NCOL
FOOT_TOP = H - 26
LH = 15


def section_height(items):
    h = 20
    for n, b, r in items:
        h += len(wrap_rich([(b, F_ITB, INK), (r, F_IT, INK)], CW - 22)) * LH + 4
    return h + 4


# assign sections to columns in order, greedy fill
cols = [[] for _ in range(NCOL)]
col_h = [0.0] * NCOL
avail = FOOT_TOP - SEC_TOP - 10
ci = 0
for name, items in SECTIONS:
    hgt = section_height(items)
    if col_h[ci] + hgt > avail and ci < NCOL - 1:
        ci += 1
    cols[ci].append((name, items))
    col_h[ci] += hgt
if max(col_h) > avail:
    print("WARNING: column overflow", col_h, avail, file=sys.stderr)

for c in range(NCOL):
    x = 12 + c * (CW + COL_GAP)
    y = SEC_TOP + 8
    if c:
        line([(x - COL_GAP / 2, SEC_TOP + 6), (x - COL_GAP / 2, FOOT_TOP - 6)], (180, 170, 150), 1)
    for name, items in cols[c]:
        col = REGION_COLOURS[name]
        rect(x, y, x + CW, y + 16, fill=col)
        text(x + 5, y + 2, name.upper(), F_SEC, (255, 255, 255))
        y += 20
        for n, b, r in items:
            text(x + 9, y + 1, n, F_NUM, col, anchor="ma")
            y += draw_rich(x + 22, y, [(b, F_ITB, INK), (r, F_IT, INK)], CW - 22, LH) + 4
        y += 4

# ---------------------------------------------------------------- footer
rect(0, FOOT_TOP, W, H, fill=NAVY)
F_FOOT = font("arial.ttf", 12)
text(W / 2, FOOT_TOP + 6,
     f"All {TOTAL_STORIES} items are events of Tuesday 17 November 2026, or that day's development in a longer story, as reported by news agencies",
     F_FOOT, (235, 235, 240), anchor="ma")

out = img.resize((W, H), Image.LANCZOS)
pal = out.quantize(colors=96, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
pal.save(dest, optimize=True)
print("wrote", os.path.normpath(dest), os.path.getsize(dest), "bytes")
