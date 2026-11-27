"""News 26 R3 renderer: builds entry.png (1024x1024) from the 30 verified
stories of Wednesday 26 November 2026. Bright paper design: navy header,
two hero panels, a 4x7 story grid, and a slim timeline strip.
Run: python3 render.py  -> writes entry.png next to this file.
"""

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
F_REG = f"{FONT_DIR}/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# Palette
PAPER = (248, 246, 240)
NAVY = (11, 31, 58)
NAVY_SOFT = (27, 58, 95)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
INK = (18, 28, 43)
GREY = (94, 104, 118)
CARD = (255, 255, 255)
CARD_LINE = (214, 210, 198)
HERO1_BG = (220, 233, 245)
HERO2_BG = (251, 238, 211)
TIMELINE_BG = (11, 31, 58)

CAT_COLORS = {
    "WORLD": (27, 58, 95),
    "CONFLICT": (178, 34, 34),
    "ECONOMY": (31, 122, 77),
    "TECH": (104, 62, 158),
    "SPORT": (198, 102, 16),
    "SCIENCE": (13, 122, 134),
    "MARKETS": (154, 118, 10),
    "CULTURE": (168, 62, 120),
}

HEROES = [
    {
        "cat": "VENEZUELA",
        "color": (27, 58, 95),
        "bg": HERO1_BG,
        "headline": "US & Qatar bridge loans help Venezuela clear bank arrears",
        "dek": "Arrears cleared — Caracas steps back into the fold",
        "art": "bridge",
    },
    {
        "cat": "KRASNODAR",
        "color": (178, 34, 34),
        "bg": HERO2_BG,
        "headline": "Drone strike sets Krasnodar refinery ablaze",
        "dek": "Slavyansk ECO plant burns after overnight attack",
        "art": "refinery",
    },
]

# (category, headline) — 28 grid stories
GRID = [
    ("WORLD", "Two Italians killed in Kuwait drone attack"),
    ("WORLD", "Trump lashes out at foes in Thanksgiving post"),
    ("TECH", "Nvidia halts AI server shipments to SE Asia"),
    ("CONFLICT", "Houthis strike Saudi port of Jizan"),
    ("MARKETS", "Oil rises as Iran claims mine strikes on ships"),
    ("ECONOMY", "De Cos to become new ECB chief"),
    ("WORLD", "UK net migration falls to lowest since 1997"),
    ("WORLD", "Trump demands probe of GDP data"),
    ("WORLD", "Guinea-Bissau delays elections to Nov 2028"),
    ("CONFLICT", "North Korea halts missile shipments to Russia"),
    ("WORLD", "Bangkok refinery blast injures nine"),
    ("WORLD", "Giza fire death toll rises to 31"),
    ("WORLD", "Fresh clashes rock Bangladesh protests"),
    ("ECONOMY", "Norse Atlantic suspends flights"),
    ("TECH", "FinCEN confirms internal cyber breach"),
    ("WORLD", "Mexico president blasts DEA over cartel claims"),
    ("WORLD", "GAO: ammo stockpiles take years to rebuild"),
    ("SPORT", "Bears stun Lions 39–35 in Thanksgiving thriller"),
    ("SPORT", "Eagles rally past Cowboys 39–38"),
    ("SPORT", "GB reach Davis Cup semis, first since 2019"),
    ("SPORT", "Palace edge Real Sociedad 2–1"),
    ("CULTURE", "Macy's parade postponed by storms"),
    ("ECONOMY", "Bank of Korea hikes rates to 3.25%"),
    ("SCIENCE", "Progress 97 cargo ship docks with ISS"),
    ("SCIENCE", "Runaway pulsar spotted racing through space"),
    ("ECONOMY", "Brazil inflation eases, IPCA-15 up 0.22%"),
    ("CONFLICT", "UK buys £26m of explosives for Ukraine"),
    ("WORLD", "California hit by exceptional 9m tides"),
]

TIMELINE = [
    ("01:37", "Oil climbs"),
    ("10:26", "Norse halts flights"),
    ("12:08", "Progress 97 docks"),
    ("13:06", "Brazil inflation eases"),
    ("17:13", "Guinea-Bissau delays"),
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_bridge(d, x0, y0, x1, y1):
    """Flat suspension-bridge motif in navy + gold."""
    deck_y = y1 - 22
    d.line([(x0 + 8, deck_y), (x1 - 8, deck_y)], fill=NAVY, width=4)
    for tx in (x0 + 52, x1 - 52):
        d.line([(tx, y0 + 14), (tx, deck_y)], fill=NAVY, width=4)
        d.line([(tx - 8, y0 + 14), (tx + 8, y0 + 14)], fill=NAVY, width=4)
    for cx in range(x0 + 20, x1 - 16, 34):
        d.line([(x0 + 52, y0 + 18), (cx, deck_y)], fill=(120, 145, 175), width=1)
        d.line([(x1 - 52, y0 + 18), (cx, deck_y)], fill=(120, 145, 175), width=1)
    # rising bars (bridge loans / arrears cleared)
    bars = [14, 24, 34, 46]
    bx = x1 - 118
    for i, bh in enumerate(bars):
        d.rectangle([bx + i * 26, deck_y - 6 - bh, bx + i * 26 + 18, deck_y - 6],
                    fill=GOLD if i == 3 else (27, 58, 95))
    d.ellipse([x0 + 14, y0 + 10, x0 + 42, y0 + 38], fill=(247, 203, 92))


def draw_refinery(d, x0, y0, x1, y1):
    """Flat refinery motif: towers, flame, smoke. All art stays inside
    the (x0, y0, x1, y1) band: nothing may rise above y0."""
    base = y1 - 16
    d.rectangle([x0 + 30, base - 46, x0 + 58, base], fill=(90, 96, 104))
    d.rectangle([x0 + 66, base - 34, x0 + 92, base], fill=(120, 126, 134))
    d.rectangle([x0 + 100, base - 52, x0 + 128, base], fill=(70, 76, 84))
    d.polygon([(x0 + 100, base - 52), (x0 + 114, base - 60), (x0 + 128, base - 52)],
              fill=(70, 76, 84))
    # flame (top at base - 72, i.e. 8px below the band top)
    fx = x0 + 114
    d.polygon([(fx - 12, base - 66), (fx - 4, base - 72), (fx + 2, base - 70),
               (fx + 10, base - 72), (fx + 14, base - 66)], fill=(232, 122, 26))
    d.polygon([(fx - 6, base - 66), (fx, base - 72), (fx + 6, base - 66)],
              fill=(247, 203, 92))
    # smoke puffs
    for cx, cy, r in ((x0 + 44, y0 + 34, 9), (x0 + 62, y0 + 22, 11),
                      (x0 + 84, y0 + 32, 8)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 182, 188))
    d.line([(x0 + 8, base), (x1 - 8, base)], fill=(70, 76, 84), width=4)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header band ----
    d.rectangle([0, 0, W, 84], fill=NAVY)
    d.rectangle([0, 84, W, 88], fill=GOLD)
    f_title = font(F_BOLD, 34)
    d.text((18, 22), "THE WORLD IN ONE DAY", font=f_title, fill=WHITE)
    f_date = font(F_BOLD, 15)
    date_txt = "WEDNESDAY · 26 NOVEMBER 2026"
    dw = d.textlength(date_txt, font=f_date)
    d.text((W - 18 - dw, 20), date_txt, font=f_date, fill=(214, 222, 235))
    f_tag = font(F_BOLD, 13)
    tag = "30 STORIES"
    tw = d.textlength(tag, font=f_tag)
    tx = W - 18 - tw - 12
    d.rounded_rectangle([tx, 46, tx + tw + 24, 70], radius=11, fill=GOLD)
    d.text((tx + 12, 51), tag, font=f_tag, fill=NAVY)

    # ---- hero panels ----
    hero_y, hero_h, hero_w, gap = 100, 246, 496, 16
    for i, hero in enumerate(HEROES):
        x0 = 16 + i * (hero_w + gap)
        x1 = x0 + hero_w
        y0, y1 = hero_y, hero_y + hero_h
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=hero["bg"])
        # art band on top
        if hero["art"] == "bridge":
            draw_bridge(d, x0 + 12, y0 + 8, x1 - 12, y0 + 104)
        else:
            draw_refinery(d, x0 + 12, y0 + 8, x1 - 12, y0 + 104)
        d.line([(x0 + 16, y0 + 110), (x1 - 16, y0 + 110)], fill=(255, 255, 255), width=2)
        # category + headline + dek
        f_cat = font(F_BOLD, 12)
        d.text((x0 + 18, y0 + 122), hero["cat"], font=f_cat, fill=hero["color"])
        f_head = font(F_BOLD, 25)
        lines = wrap(d, hero["headline"], f_head, hero_w - 36)
        ly = y0 + 144
        for ln in lines[:3]:
            d.text((x0 + 18, ly), ln, font=f_head, fill=INK)
            ly += 30
        f_dek = font(F_REG, 14)
        d.text((x0 + 18, y1 - 30), hero["dek"], font=f_dek, fill=GREY)

    # ---- story grid: 4 cols x 7 rows ----
    grid_y0, cell_w, cell_h, cgap, rgap = 362, 240, 82, 10, 5
    f_cat = font(F_BOLD, 10)
    for idx, (cat, headline) in enumerate(GRID):
        row, col = divmod(idx, 4)
        x0 = 16 + col * (cell_w + cgap)
        y0 = grid_y0 + row * (cell_h + rgap)
        x1, y1 = x0 + cell_w, y0 + cell_h
        d.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD,
                            outline=CARD_LINE, width=1)
        d.rectangle([x0, y0 + 6, x0 + 4, y1 - 6], fill=CAT_COLORS[cat])
        d.text((x0 + 12, y0 + 7), cat, font=f_cat, fill=CAT_COLORS[cat])
        # Auto-fit: shrink the headline font until it wraps to at most
        # two lines, so no headline ever loses its final word.
        f_head = font(F_BOLD, 15)
        lines = wrap(d, headline, f_head, cell_w - 22)
        for size in (14, 13):
            if len(lines) <= 2:
                break
            f_head = font(F_BOLD, size)
            lines = wrap(d, headline, f_head, cell_w - 22)
        if len(lines) > 2:
            print(f"WARNING: headline still 3 lines at 13px: {headline!r}")
        ly = y0 + 26
        for ln in lines[:2]:
            d.text((x0 + 12, ly), ln, font=f_head, fill=INK)
            ly += 19

    # ---- timeline strip (flex layout: measure each item, spread the
    # leftover space evenly as gaps, dots centred in the gaps) ----
    tl_y0, tl_y1 = 968, 1020
    d.rectangle([0, tl_y0, W, tl_y1], fill=TIMELINE_BG)
    f_tl_h = font(F_BOLD, 11)
    f_time = font(F_BOLD, 14)
    f_lbl = font(F_REG, 13)
    d.text((18, tl_y0 + 6), "THE DAY IN FIVE MOMENTS", font=f_tl_h, fill=GOLD)
    widths = []
    for t, label in TIMELINE:
        widths.append(d.textlength(t, font=f_time) + 8 +
                      d.textlength(label, font=f_lbl))
    total = sum(widths)
    gaps = 4
    gap_w = max(16, (W - 32 - total) // gaps)
    x = 16 + (W - 32 - total - gap_w * gaps) / 2
    for i, (t, label) in enumerate(TIMELINE):
        tw = d.textlength(t, font=f_time)
        d.text((x, tl_y0 + 26), t, font=f_time, fill=GOLD)
        d.text((x + tw + 8, tl_y0 + 27), label, font=f_lbl, fill=WHITE)
        x += widths[i]
        if i < gaps:
            dot_cx = x + gap_w / 2
            d.ellipse([dot_cx - 2, tl_y0 + 32, dot_cx + 2, tl_y0 + 36],
                      fill=GOLD)
            x += gap_w

    img.save(OUT, "PNG")
    print(f"wrote {OUT} {img.size} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    render()
