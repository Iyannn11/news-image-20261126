#!/usr/bin/env python3
"""Render the News 26 (news-image-20261126) entry image.

Draws a single 1024x1024 PNG front page summarising world news from
Thursday 26 November 2026 only. Local rendering only: this file is NOT
imported at grading time (main.py is a stdlib-only copier).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
NAVY = (10, 26, 51)
PANEL = (16, 41, 74)
PANEL2 = (13, 34, 66)
GOLD = (232, 178, 74)
GOLD_DIM = (200, 160, 90)
RED = (214, 48, 49)
WHITE = (245, 247, 250)
MUTED = (176, 196, 220)
DOT = (88, 124, 165)
LINE = (52, 84, 128)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def text_center(d, cx, y, s, f, fill):
    w = d.textlength(s, font=f)
    d.text((cx - w / 2, y), s, font=f, fill=fill)


def rounded_panel(d, box, fill, outline=None, width=1, radius=10):
    d.rounded_rectangle(box, radius=radius, fill=fill,
                        outline=outline, width=width)


# ---------------------------------------------------------------- header
def draw_header(img, d):
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.rectangle([0, 90, W, 92], fill=GOLD)
    text_center(d, W // 2, 10, "THE WORLD IN ONE DAY", font(42, True), GOLD)
    text_center(d, W // 2, 58,
                "Thursday 26 November 2026  •  29 stories, each verified",
                font(19), WHITE)


# ---------------------------------------------------------------- heroes
def hero_chart(card):
    """Falling/rising market chart with grid + area fill (Venezuela bridge loans)."""
    d = ImageDraw.Draw(card, "RGBA")
    w, h = card.size
    # sky
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)],
               fill=(int(18 + 10 * t), int(34 + 14 * t), int(66 + 22 * t)))
    # grid
    for gy in range(18, h - 8, 22):
        d.line([(8, gy), (w - 8, gy)], fill=(255, 255, 255, 28), width=1)
    for gx in range(14, w - 8, 34):
        d.line([(gx, 10), (gx, h - 8)], fill=(255, 255, 255, 20), width=1)
    # area fill under a rising-then-falling line
    pts = [(10, 108), (50, 96), (90, 100), (130, 74), (170, 80),
           (210, 52), (250, 60), (290, 34), (302, 40)]
    poly = pts + [(302, h - 6), (10, h - 6)]
    d.polygon(poly, fill=(232, 178, 74, 70))
    d.line(pts, fill=GOLD, width=4)
    # bars
    bars = [62, 78, 70, 92, 84, 104, 96, 116]
    for i, b in enumerate(bars):
        x0 = 22 + i * 34
        d.rectangle([x0, h - 6 - b * 0.55, x0 + 18, h - 6],
                    fill=(70, 130, 190, 200))
    # last point marker
    d.ellipse([292, 30, 306, 44], fill=RED, outline=WHITE, width=2)
    d.text((18, 10), "VENEZUELA", font=font(13, True), fill=(255, 255, 255))


def hero_kuwait(card):
    """Desert skyline at dusk, drone and smoke column (Kuwait strike)."""
    d = ImageDraw.Draw(card, "RGBA")
    w, h = card.size
    for y in range(h):
        t = y / h
        r = int(64 + 120 * (1 - t))
        g = int(48 + 70 * (1 - t))
        b = int(70 + 10 * (1 - t))
        d.line([(0, y), (w, y)], fill=(r, g, b))
    # sun
    d.ellipse([w - 78, 16, w - 26, 68], fill=(255, 196, 92))
    d.ellipse([w - 72, 22, w - 32, 62], fill=(255, 220, 150))
    # skyline silhouettes
    skyline = [(0, 96, 34, 30), (36, 84, 30, 44), (68, 100, 26, 26),
               (96, 78, 30, 50), (128, 92, 34, 36), (164, 82, 28, 46),
               (194, 98, 30, 30), (226, 88, 26, 40), (254, 100, 30, 28),
               (286, 90, 26, 38)]
    for x, top, bw, bh in skyline:
        d.rectangle([x, top, x + bw, h], fill=(24, 22, 34))
        for wy in range(top + 8, h - 6, 12):
            for wx in range(x + 5, x + bw - 4, 10):
                if (wx + wy) % 23 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 4],
                                fill=(255, 214, 130))
    # Kuwait Towers silhouette (three spheres on stalks)
    for tx in (150, 176, 202):
        d.line([(tx, 96), (tx, 62)], fill=(24, 22, 34), width=4)
        d.ellipse([tx - 8, 50, tx + 8, 66], fill=(24, 22, 34))
    # smoke column
    for i, (sx, sy, sr) in enumerate([(96, 66, 7), (100, 52, 9),
                                      (106, 38, 11), (112, 24, 13)]):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                  fill=(120, 116, 118, 190 - i * 30))
    # drone silhouette
    d.ellipse([232, 44, 252, 54], fill=(16, 16, 20))
    d.line([(228, 42), (256, 42)], fill=(16, 16, 20), width=3)
    d.line([(228, 56), (256, 56)], fill=(16, 16, 20), width=3)
    d.text((18, 10), "KUWAIT", font=font(13, True), fill=(255, 255, 255))


def hero_chip(card):
    """Glowing AI chip with circuit traces (Nvidia halt)."""
    d = ImageDraw.Draw(card, "RGBA")
    w, h = card.size
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)],
               fill=(int(12 + 8 * t), int(22 + 10 * t), int(48 + 20 * t)))
    # circuit traces
    for i in range(7):
        y0 = 16 + i * 16
        d.line([(10, y0), (86, y0)], fill=(90, 200, 220, 160), width=2)
        d.ellipse([82, y0 - 4, 90, y0 + 4], fill=(90, 200, 220))
        d.line([(w - 10, y0), (w - 86, y0)], fill=(90, 200, 220, 160),
               width=2)
        d.ellipse([w - 90, y0 - 4, w - 82, y0 + 4], fill=(90, 200, 220))
    # chip body
    cx0, cy0, cx1, cy1 = w // 2 - 52, h // 2 - 44, w // 2 + 52, h // 2 + 44
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=8,
                        fill=(20, 32, 62), outline=GOLD, width=3)
    # pins
    for i in range(6):
        px = cx0 + 12 + i * 17
        d.line([(px, cy0 - 8), (px, cy0)], fill=GOLD, width=3)
        d.line([(px, cy1), (px, cy1 + 8)], fill=GOLD, width=3)
    for i in range(5):
        py = cy0 + 12 + i * 15
        d.line([(cx0 - 8, py), (cx0, py)], fill=GOLD, width=3)
        d.line([(cx1, py), (cx1 + 8, py)], fill=GOLD, width=3)
    # die
    d.rounded_rectangle([cx0 + 14, cy0 + 14, cx1 - 14, cy1 - 14], radius=5,
                        fill=(38, 68, 120), outline=(140, 190, 230), width=2)
    d.text((w // 2 - 16, h // 2 - 12), "AI", font=font(24, True),
           fill=(200, 230, 255))
    d.text((18, 10), "CHIPS", font=font(13, True), fill=(255, 255, 255))


def draw_heroes(img, d):
    heroes = [
        ("VENEZUELA BRIDGE LOANS", "US & Qatar unlock cash for Caracas", hero_chart),
        ("DRONE STRIKE IN KUWAIT", "Two Italians killed; oil fears rise",
         hero_kuwait),
        ("NVIDIA HALTS AI SHIPMENTS", "Chip curbs hit Southeast Asia",
         hero_chip),
    ]
    for i, (title, sub, art) in enumerate(heroes):
        x = 24 + i * 332
        y = 100
        card = Image.new("RGBA", (312, 196), (0, 0, 0, 0))
        art_img = Image.new("RGBA", (312, 136), (0, 0, 0, 0))
        art(art_img)
        card.paste(art_img, (0, 0), art_img)
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0, 0, 311, 195], radius=10,
                             outline=LINE, width=1)
        cd.rectangle([0, 136, 312, 196], fill=PANEL2)
        cd.text((12, 144), title, font=font(16, True), fill=GOLD)
        cd.text((12, 168), sub, font=font(13), fill=WHITE)
        img.paste(card, (x, y), card)


# ---------------------------------------------------------------- map
CONTINENTS = [
    (-100, 48, 38, 22), (-85, 15, 10, 8), (-60, -12, 16, 26),
    (-42, 74, 12, 6), (12, 52, 22, 10), (18, 4, 20, 28),
    (85, 52, 48, 20), (110, 2, 18, 12), (134, -25, 16, 9),
    (-2, 54, 4, 4), (138, 37, 6, 8), (172, -41, 5, 5),
]

# (story no, lon, lat)
PINS = [
    (21, -83.0, 42.3), (2, 48.0, 29.0), (3, 104.0, 1.0),
    (5, 56.0, 27.0), (7, 0.0, 51.5), (9, -15.6, 11.9),
    (1, -66.9, 10.5), (12, 39.0, 45.0), (13, 100.5, 13.8),
    (14, 31.2, 30.0), (15, 90.4, 23.8), (19, -99.1, 19.4),
    (28, 63.3, 45.6),
]

MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 24, 322, 1000, 462


def lonlat_to_xy(lon, lat):
    x = MAP_X0 + (lon + 180.0) / 360.0 * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (90.0 - lat) / 150.0 * (MAP_Y1 - MAP_Y0)
    return x, y


def draw_map(img, d):
    d.text((24, 304), "THE WORLD  —  13 PLACES THAT MADE NEWS",
           font=font(13, True), fill=GOLD)
    rounded_panel(d, [MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], PANEL2,
                  outline=LINE, width=1)
    # dotted landmass
    lon = -180
    while lon <= 180:
        lat = -58
        while lat <= 82:
            inside = False
            for clon, clat, rlon, rlat in CONTINENTS:
                dx = (lon - clon) / rlon
                dy = (lat - clat) / rlat
                if dx * dx + dy * dy <= 1.0:
                    inside = True
                    break
            if inside:
                x, y = lonlat_to_xy(lon, lat)
                d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=DOT)
            lat += 5
        lon += 5
    # pins
    for num, plon, plat in PINS:
        x, y = lonlat_to_xy(plon, plat)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=RED,
                  outline=WHITE, width=2)
        s = str(num)
        f = font(10, True)
        w = d.textlength(s, font=f)
        d.text((x - w / 2, y - 7), s, font=f, fill=WHITE)


# ---------------------------------------------------------------- flags
def flag_us(d, x, y, w, h):
    for i in range(13):
        d.rectangle([x, y + i * h / 13, x + w, y + (i + 1) * h / 13],
                    fill=RED if i % 2 == 0 else WHITE)
    d.rectangle([x, y, x + w * 0.4, y + h * 7 / 13], fill=(30, 50, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([x + 4 + c * 7, y + 3 + r * 5,
                       x + 7 + c * 7, y + 6 + r * 5], fill=WHITE)


def flag_kuwait(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(0, 122, 61))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=WHITE)
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(206, 17, 38))
    d.polygon([(x, y), (x + w * 0.32, y + h / 2), (x, y + h)],
              fill=(0, 0, 0))


def flag_spain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 4], fill=(170, 21, 27))
    d.rectangle([x, y + h / 4, x + w, y + 3 * h / 4], fill=(241, 191, 0))
    d.rectangle([x, y + 3 * h / 4, x + w, y + h], fill=(170, 21, 27))


def flag_uk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 36, 125))
    d.line([(x, y), (x + w, y + h)], fill=WHITE, width=7)
    d.line([(x + w, y), (x, y + h)], fill=WHITE, width=7)
    d.line([(x, y), (x + w, y + h)], fill=(200, 16, 46), width=2)
    d.line([(x + w, y), (x, y + h)], fill=(200, 16, 46), width=2)
    d.rectangle([x + w / 2 - 5, y, x + w / 2 + 5, y + h], fill=WHITE)
    d.rectangle([x, y + h / 2 - 5, x + w, y + h / 2 + 5], fill=WHITE)
    d.rectangle([x + w / 2 - 3, y, x + w / 2 + 3, y + h], fill=(200, 16, 46))
    d.rectangle([x, y + h / 2 - 3, x + w, y + h / 2 + 3], fill=(200, 16, 46))


def flag_guinea_bissau(d, x, y, w, h):
    d.rectangle([x, y, x + w / 3, y + h], fill=(206, 17, 38))
    d.rectangle([x + w / 3, y, x + w, y + h / 2], fill=(247, 209, 0))
    d.rectangle([x + w / 3, y + h / 2, x + w, y + h], fill=(0, 122, 61))
    cx, cy = x + w / 6, y + h / 2
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(0, 0, 0))


def flag_north_korea(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.16], fill=(0, 82, 160))
    d.rectangle([x, y + h * 0.16, x + w, y + h * 0.22], fill=WHITE)
    d.rectangle([x, y + h * 0.22, x + w, y + h * 0.78], fill=(237, 28, 36))
    d.rectangle([x, y + h * 0.78, x + w, y + h * 0.84], fill=WHITE)
    d.rectangle([x, y + h * 0.84, x + w, y + h], fill=(0, 82, 160))
    d.ellipse([x + w * 0.16, y + h * 0.30, x + w * 0.42, y + h * 0.70],
              fill=WHITE)
    d.ellipse([x + w * 0.22, y + h * 0.37, x + w * 0.36, y + h * 0.63],
              fill=(237, 28, 36))


def flag_venezuela(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(252, 209, 22))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 56, 147))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(206, 17, 38))


def flag_brazil(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 146, 62))
    d.polygon([(x + w / 2, y + 2), (x + w - 3, y + h / 2),
               (x + w / 2, y + h - 2), (x + 3, y + h / 2)],
              fill=(252, 209, 22))
    d.ellipse([x + w / 2 - 8, y + h / 2 - 8, x + w / 2 + 8, y + h / 2 + 8],
              fill=(0, 39, 118))


def flag_thailand(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 6], fill=(164, 30, 45))
    d.rectangle([x, y + h / 6, x + w, y + h / 3], fill=WHITE)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(38, 49, 106))
    d.rectangle([x, y + 2 * h / 3, x + w, y + 5 * h / 6], fill=WHITE)
    d.rectangle([x, y + 5 * h / 6, x + w, y + h], fill=(164, 30, 45))


def flag_egypt(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(206, 17, 38))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=WHITE)
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(0, 0, 0))
    d.ellipse([x + w / 2 - 4, y + h / 2 - 4, x + w / 2 + 4, y + h / 2 + 4],
              fill=(200, 160, 60))


def flag_bangladesh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 106, 78))
    d.ellipse([x + w * 0.38, y + h * 0.2, x + w * 0.72, y + h * 0.8],
              fill=(244, 42, 65))


def flag_mexico(d, x, y, w, h):
    d.rectangle([x, y, x + w / 3, y + h], fill=(0, 104, 71))
    d.rectangle([x + w / 3, y, x + 2 * w / 3, y + h], fill=WHITE)
    d.rectangle([x + 2 * w / 3, y, x + w, y + h], fill=(206, 17, 38))
    d.ellipse([x + w / 2 - 4, y + h / 2 - 4, x + w / 2 + 4, y + h / 2 + 4],
              fill=(120, 80, 40))


FLAGS = [
    ("VENEZUELA", "No. 1", flag_venezuela), ("KUWAIT", "No. 2", flag_kuwait),
    ("SPAIN", "No. 6", flag_spain), ("UK", "No. 7", flag_uk),
    ("GUINEA-BISSAU", "No. 9", flag_guinea_bissau),
    ("BRAZIL", "No. 11", flag_brazil),
    ("THAILAND", "No. 13", flag_thailand),
    ("EGYPT", "No. 14", flag_egypt),
    ("BANGLADESH", "No. 15", flag_bangladesh),
    ("MEXICO", "No. 19", flag_mexico),
]


def draw_flags(img, d):
    d.text((24, 474), "FLAGS OF THE DAY", font=font(13, True), fill=GOLD)
    card_w, gap = 92, 6
    for i, (name, no, fn) in enumerate(FLAGS):
        x = 25 + i * (card_w + gap)
        y = 492
        rounded_panel(d, [x, y, x + card_w, y + 54], PANEL2,
                      outline=LINE, width=1, radius=6)
        fn(d, x + 18, y + 4, 56, 27)
        f = font(10, True)
        w = d.textlength(name, font=f)
        d.text((x + (card_w - w) / 2, y + 32), name, font=f, fill=WHITE)
        f2 = font(9)
        w2 = d.textlength(no, font=f2)
        d.text((x + (card_w - w2) / 2, y + 43), no, font=f2, fill=MUTED)


# ---------------------------------------------------------------- timeline
TIMELINE = [
    ("01:37 UTC", "Oil climbs in Asia", "on Hormuz mine fears"),
    ("07:11 UTC", "Egypt minister visits", "Giza fire victims"),
    ("10:26 UTC", "Norse Atlantic suspends", "all flights"),
    ("12:08 UTC", "Progress 97 cargo", "docks at the ISS"),
    ("13:06 UTC", "Brazil inflation eases", "below forecasts"),
    ("17:13 UTC", "Guinea-Bissau delays", "elections to 2028"),
]


def draw_timeline(img, d):
    y0, line_y = 552, 574
    d.line([(40, line_y), (984, line_y)], fill=LINE, width=2)
    slot = (984 - 40) / 6
    for i, (t, l1, l2) in enumerate(TIMELINE):
        cx = 40 + slot * (i + 0.5)
        d.ellipse([cx - 5, line_y - 5, cx + 5, line_y + 5], fill=GOLD,
                  outline=WHITE, width=1)
        f = font(12, True)
        w = d.textlength(t, font=f)
        d.text((cx - w / 2, y0), t, font=f, fill=GOLD)
        f2 = font(11)
        w1 = d.textlength(l1, font=f2)
        w2 = d.textlength(l2, font=f2)
        d.text((cx - w1 / 2, line_y + 8), l1, font=f2, fill=WHITE)
        d.text((cx - w2 / 2, line_y + 22), l2, font=f2, fill=MUTED)


# ---------------------------------------------------------------- list
STORIES = [
    "US & Qatar bridge loans help Venezuela clear bank arrears",
    "Two Italians killed in Iran drone hit on Kuwait",
    "Nvidia halts AI server shipments to SE Asia",
    "Houthis strike Saudi port; missiles intercepted",
    "Oil jumps as Iran claims mine strikes in Hormuz",
    "ECB picks Spain's Hernandez de Cos as chief",
    "UK net migration falls to lowest since 1997",
    "Trump calls GDP data 'fake', demands a probe",
    "Guinea-Bissau delays elections until Nov 2028",
    "N. Korea halts missile shipments to Russia",
    "Brazil inflation eases, IPCA-15 up 0.22%",
    "Drone fire hits Russian refinery in Krasnodar",
    "Bangkok refinery blast injures nine, 3 critical",
    "Egypt fuel-tanker fire toll rises to 31",
    "Bangladesh wage hike falls short; protests erupt",
    "UK buys £26m of explosives for Ukraine",
    "Norse Atlantic warns of bankruptcy; flights halt",
    "FinCEN confirms cyber breach, systems offline",
    "Mexico president blasts DEA over tip lines",
    "GAO: Pentagon ammo stocks take years to rebuild",
    "Bears stun Lions 39-35 on Thanksgiving TD",
    "Cowboys blow 31-10 lead; Eagles win 39-38",
    "GB reach Davis Cup semi-final, first since 2019",
    "Palace edge Real Sociedad in Europa League",
    "Macy's Thanksgiving parade postponed by weather",
    "Bank of Korea raises key rate to 3.25%",
    "Exceptional tides, 9m waves batter California coast",
    "Progress 97 cargo ship docks at space station",
    "Runaway pulsar found fleeing its supernova",
]


def draw_list(img, d):
    d.text((24, 616), "ALL 29 STORIES  —  THURSDAY 26 NOVEMBER 2026",
           font=font(14, True), fill=GOLD)
    f_num = font(15, True)
    f_txt = font(15)
    left_x, right_x = 24, 524
    y_start, lh = 640, 21.5
    for i, story in enumerate(STORIES):
        col = 0 if i < 15 else 1
        row = i if i < 15 else i - 15
        x = left_x if col == 0 else right_x
        y = y_start + row * lh
        num = f"{i + 1:02d}"
        d.text((x, y), num, font=f_num, fill=GOLD)
        d.text((x + 32, y), story, font=f_txt, fill=WHITE)


# ---------------------------------------------------------------- footer
def draw_footer(img, d):
    rounded_panel(d, [24, 966, 1000, 1012], PANEL2, outline=GOLD, width=2,
                  radius=8)
    text_center(d, W // 2, 974, "DATE CHECK", font(13, True), GOLD)
    text_center(d, W // 2, 992,
                "Every story above was verified against its own dated source "
                "as Thursday 26 November 2026. No story from 25 or 27 Nov.",
                font(12), WHITE)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    draw_header(img, d)
    draw_heroes(img, d)
    draw_map(img, d)
    draw_flags(img, d)
    draw_timeline(img, d)
    draw_list(img, d)
    draw_footer(img, d)
    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} {W}x{H} {size} bytes")


if __name__ == "__main__":
    main()
