#!/usr/bin/env python3
"""Render the News 26 R2 image: 20 strongest stories from Wed 26 Nov 2026.

R2 is TIGHTER and BOLDER than R1: 2 large hero panels, a clean 3x6 grid of
18 more stories, one slim timeline strip. All facts from SOURCES.md (verified
26 Nov 2026 only). PIL is used ONLY here, at render time -- main.py never
imports this module or PIL.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent

W = H = 1024
BG = (247, 244, 238)          # warm paper
NAVY = (15, 31, 51)           # header / hero 1
NAVY_HERO = (22, 50, 79)
RED_HERO = (110, 27, 27)      # hero 2
GOLD = (232, 184, 75)
INK = (26, 26, 26)
MUTED = (90, 88, 82)
CARD = (255, 255, 255)
CARD_BORDER = (217, 210, 195)
SUBLINE = (201, 212, 224)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def bold(size):
    return ImageFont.truetype(str(FONT_DIR / "DejaVuSans-Bold.ttf"), size)


def regular(size):
    return ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), size)


def wrap(draw, text, font, max_width):
    """Greedy word wrap by measured pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, max_width, fill, max_lines=3,
                 spacing=4):
    lines = wrap(draw, text, font, max_width)[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + spacing
    return y


# (kicker, kicker colour, headline)
GRID = [
    ("KUWAIT", (176, 58, 46), "Two Italians killed in Iranian drone attack"),
    ("WHITE HOUSE", (31, 97, 141), "Trump's Thanksgiving message lashes out at foes"),
    ("TECH", (108, 52, 131), "Nvidia halts AI server shipments to SE Asia"),
    ("RED SEA", (176, 58, 46), "Houthis strike Saudi port of Jizan"),
    ("OIL", (176, 130, 11), "Oil rises as Iran claims mine strikes on ships"),
    ("BRITAIN", (31, 97, 141), "UK net migration falls to lowest since 1997"),
    ("GUINEA-BISSAU", (44, 62, 80), "Elections delayed two years after coup"),
    ("BRAZIL", (30, 132, 73), "Inflation eases as IPCA-15 rises just 0.22%"),
    ("UKRAINE AID", (31, 97, 141), "UK buys £26m of explosives for Ukraine"),
    ("BANGKOK", (176, 58, 46), "Refinery blast injures 9, three critical"),
    ("EGYPT", (44, 62, 80), "Giza fire death toll rises to 31"),
    ("CYBER", (108, 52, 131), "FinCEN confirms internal cyber breach"),
    ("PENTAGON", (31, 97, 141), "GAO: ammo stockpiles take years to rebuild"),
    ("NFL", (202, 111, 30), "Bears stun Lions 39–35 on Thanksgiving"),
    ("NFL", (202, 111, 30), "Eagles rally past Cowboys 39–38"),
    ("NEW YORK", (44, 62, 80), "Macy's Thanksgiving parade postponed"),
    ("SPACE", (17, 122, 101), "Progress 97 docks at the space station"),
    ("TRAVEL", (44, 62, 80), "Norse Atlantic suspends flights"),
]

TIMELINE = [
    ("01:37", "Oil climbs"),
    ("10:26", "Norse suspends flights"),
    ("12:08", "Progress 97 docks"),
    ("13:06", "Brazil inflation eases"),
    ("17:13", "Guinea-Bissau delays vote"),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header band -------------------------------------------------
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.rectangle([0, 89, W, 92], fill=GOLD)
    d.text((16, 24), "THE WORLD IN ONE DAY", font=bold(44), fill=(255, 255, 255))
    date = "WEDNESDAY · 26 NOVEMBER 2026"
    dw = d.textlength(date, font=bold(20))
    d.text((W - 16 - dw, 36), date, font=bold(20), fill=GOLD)

    # ---- hero panels -------------------------------------------------
    heroes = [
        (16, NAVY_HERO, "VENEZUELA",
         "US & Qatar throw Venezuela a lifeline on bank arrears",
         "Bridge loans clear the way back to development-bank funding."),
        (520, RED_HERO, "KRASNODAR · UKRAINE WAR",
         "Drone strike sets Russian refinery ablaze",
         "Slavyansk ECO plant hit overnight — the latest in a wave "
         "of refinery strikes."),
    ]
    for x, bg, kicker, headline, sub in heroes:
        d.rounded_rectangle([x, 104, x + 488, 384], radius=12, fill=bg)
        d.text((x + 24, 124), kicker, font=bold(16), fill=GOLD)
        d.rectangle([x + 24, 152, x + 24 + 64, 156], fill=GOLD)
        draw_wrapped(d, x + 24, 172, headline, bold(34), 440,
                     (255, 255, 255), max_lines=3, spacing=6)
        draw_wrapped(d, x + 24, 308, sub, regular(17), 440, SUBLINE,
                     max_lines=2, spacing=4)
        d.text((x + 24, 356), "REUTERS · 26 NOV", font=bold(12), fill=(150, 165, 185))

    # ---- grid: 3 cols x 6 rows --------------------------------------
    cell_w, cell_h, gx, gy = 322, 84, 13, 8
    x0, y0 = 16, 396
    for i, (kicker, colour, headline) in enumerate(GRID):
        row, col = divmod(i, 3)
        x = x0 + col * (cell_w + gx)
        y = y0 + row * (cell_h + gy)
        d.rounded_rectangle([x, y, x + cell_w, y + cell_h], radius=6,
                            fill=CARD, outline=CARD_BORDER, width=1)
        d.text((x + 14, y + 9), kicker, font=bold(13), fill=colour)
        draw_wrapped(d, x + 14, y + 30, headline, bold(18), cell_w - 28,
                     INK, max_lines=2, spacing=3)

    # ---- timeline strip ----------------------------------------------
    d.rounded_rectangle([16, 952, 1008, 1008], radius=8, fill=(237, 233, 223))
    d.text((32, 968), "THE DAY IN TIME", font=bold(14), fill=MUTED)
    tx = 210
    seg = (1008 - 16 - 210 - 16) / len(TIMELINE)
    centres = [int(tx + i * seg + seg / 2) for i in range(len(TIMELINE))]
    d.line([centres[0], 984, centres[-1], 984], fill=(200, 192, 175), width=2)
    for cx, (time, label) in zip(centres, TIMELINE):
        tw = d.textlength(time, font=bold(14))
        d.text((cx - tw / 2, 958), time, font=bold(14), fill=NAVY)
        d.ellipse([cx - 4, 980, cx + 4, 988], fill=GOLD, outline=NAVY, width=1)
        lw = d.textlength(label, font=regular(12))
        d.text((cx - lw / 2, 991), label, font=regular(12), fill=MUTED)

    out = HERE / "entry.png"
    img.save(out, "PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
