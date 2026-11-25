#!/usr/bin/env python3
"""Draw entry.png for news-image-20261125 — "The World Today".

One image summing up Wednesday 25 November 2026: 47 real stories from
7 regions, laid out as a newspaper front page. All text and geometry are
fixed — no network, no randomness, no clock — so running this script
twice writes byte-identical PNG bytes.

Python 3 + Pillow, DejaVu fonts from the system. Usage: python3 render.py
"""
from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAPER = (253, 253, 247)
INK = (18, 18, 18)
GREY = (96, 96, 96)
RULE = (178, 178, 168)
CARD = (255, 255, 255)
CARD_EDGE = (202, 202, 192)
LEAD_FILL = (235, 240, 247)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def shrink_to_fit(draw, text, path, size, max_width, floor=10):
    """Biggest size at or under `size` that fits, else truncate with …."""
    s = size
    while s > floor:
        f = load_font(path, s)
        if draw.textlength(text, font=f) <= max_width:
            return f, text
        s -= 1
    f = load_font(path, floor)
    while text and draw.textlength(text + "…", font=f) > max_width:
        text = text[:-1]
    return f, text + "…"


def wrap_text(draw, text, f, max_width):
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ------------------------------------------------------------------ content
LEAD_KICKER = "LEAD  —  MINES IN THE STRAIT OF HORMUZ"
LEAD_HEADLINE = "Tankers hit mines in Hormuz as US weighs strikes on Iran"
LEAD_DECK = ("The IRGC says two tankers struck naval mines and Iran "
             "downed a US MQ-9 drone; Washington weighs targeting "
             "Iranian leaders. (Reuters · AP)")

BIG_STORIES = [
    ("RIYADH", (190, 0, 0),
     "Houthi drone hits Riyadh tower, 11 hurt",
     "A drone strikes the PIF tower, injuring 11 incl. 2 Indians; "
     "the coalition hits Hodeidah port in response. (Reuters)"),
    ("UKRAINE", (10, 80, 145),
     "Ukrainian drones hit two refineries in Samara",
     "Syzran and Kuibyshev hit overnight; Putin vows retaliation; "
     "NATO-style guarantees now on the table. (Reuters)"),
    ("SPACE", (0, 128, 140),
     "Pakistan’s first astronaut reaches Tiangong",
     "Shenzhou-24 docks with the station; Muhammad Zeeshan Ali is "
     "China’s first foreign visitor in orbit. (Reuters)"),
    ("HUAWEI", (110, 45, 155),
     "Huawei convicted on 10 of 12 counts in Brooklyn",
     "Fraud, sanctions breaches, trade-secret theft; sentencing in "
     "September 2027. (Reuters · DOJ)"),
    ("PACIFIC", (45, 120, 48),
     "Australia–Solomons treaty bars foreign bases",
     "Canberra becomes the principal security partner; the 2022 China "
     "pact is not renewed. (AP)"),
    ("ASTEROID", (195, 85, 15),
     "Hera unveils first close-ups of Dimorphos",
     "ESA shows the asteroid four years after NASA’s DART impact "
     "moved it. (ESA)"),
]

REGIONS = [
    ("NORTH AMERICA", (10, 80, 145), [
        "Nvidia shares fall ~7% as lawmakers question Trump’s role in Huang’s return",
        "US set to unveil new tariffs after Section 301 probe on 16 partners",
        "US consumer confidence jumps to its highest in nearly two years",
        "Cyber intrusions hit CIA and ODNI systems; no classified data reported lost",
        "Microsoft declares “Code Red” after a historic outage, memos show",
        "Small plane crashes off the Mississippi coast; 6 killed, incl. 2 children",
        "Thanksgiving travel hit by ground stops at Chicago O’Hare, twice in two days",
    ]),
    ("LATIN AMERICA", (195, 85, 15), [
        "Colombia: all ~30 hostages freed as forces storm a Cartagena supermarket",
        "Venezuela discloses $237.5bn public debt; wage protests go on",
        "Argentina enters technical recession",
        "Chile: teachers strike nationwide over education spending cuts",
        "Cuba: life expectancy fell for the first time since 1950, WHO says",
    ]),
    ("EUROPE", (110, 45, 155), [
        "Russia: leaked data points to at least 490,000 Russian war deaths",
        "Poland: Russian drone enters Polish airspace days after missiles fell",
        "Germany to set up a dedicated drone regiment",
        "Norway plans more Ukraine aid in 2027, focused on air defence",
        "Poland and the US conclude a defence research agreement",
        "Spain: election campaign turns on housing affordability",
    ]),
    ("AFRICA", (190, 0, 0), [
        "Senegal reinstated as Africa Cup champions by CAS; 1-0 win confirmed",
        "Sudan: drone attacks on Khartoum; abductions reported in Blue Nile",
        "DR Congo: military aircraft missing; rebels claim they shot it down",
        "Zambia: opposition leader indicted on treason charges",
    ]),
    ("MIDDLE EAST", (45, 120, 48), [
        "Gaza: Israeli strike kills Hamas security chief Naeem Abu Nahel",
        "Israel: Eisenkot secures first coalition pact, with Lieberman",
        "Iran: singer flogged 74 times over an unveiled concert",
        "Iraq stresses independence of its decisions amid US deployment reports",
        "Lebanon: Aoun keeps pressing diplomacy; defends sovereignty",
        "Libya: Haftar visits Türkiye as Ankara courts eastern Libya",
        "Gaza: meningitis cases rise among infants; hospitals hit by power failures",
    ]),
    ("ASIA", (185, 140, 0), [
        "China: Politburo member Chen Jining investigated in graft crackdown",
        "China: reported order for 50 Boeing jets worth ~$7.4bn",
        "North Korea orders Switzerland’s reopened office closed",
        "Japan: Nikkei falls 2.8% in the Asian AI sell-off",
        "Bangladesh: garment minimum wage up 36%, to 17,000 taka a month",
        "Bangladesh: ex-PM Hasina says she will return on 16 December",
        "Indonesia: rescuers search for workers trapped in a flooded gold mine",
        "Hong Kong: a year since the deadly Tai Po fire; survivors return home",
    ]),
    ("OCEANIA & PACIFIC", (0, 128, 140), [
        "Australia: inflation rises to 4.9%",
        "Australia: sweeping online-safety bill approved; US criticises it",
        "El Niño raises drought risk for Guam and the N. Mariana Islands",
    ]),
]


# ------------------------------------------------------------------ drawing
def draw_masthead(d):
    mx = 28
    d.text((CANVAS_W / 2, 20), "THE WORLD TODAY",
           font=load_font(SERIF_BOLD, 54), fill=INK, anchor="ma")
    d.text((CANVAS_W / 2, 82),
           "WEDNESDAY 25 NOVEMBER 2026   ·   47 STORIES FROM 7 REGIONS",
           font=load_font(SANS, 19), fill=INK, anchor="ma")
    d.line([(mx, 114), (CANVAS_W - mx, 114)], fill=INK, width=3)
    d.line([(mx, 119), (CANVAS_W - mx, 119)], fill=INK, width=1)


def draw_lead(d):
    mx, cw = 28, CANVAS_W - 56
    top, height = 130, 96
    d.rectangle([mx, top, CANVAS_W - mx, top + height],
                fill=LEAD_FILL, outline=CARD_EDGE)
    d.rectangle([mx, top, mx + 7, top + height], fill=(190, 0, 0))
    d.text((mx + 18, top + 8), LEAD_KICKER,
           font=load_font(SANS_BOLD, 12), fill=(190, 0, 0))
    head_font, head_text = shrink_to_fit(
        d, LEAD_HEADLINE, SANS_BOLD, 24, cw - 36)
    d.text((mx + 18, top + 26), head_text, font=head_font, fill=INK)
    body_font = load_font(SANS, 14)
    y = top + 58
    for line in wrap_text(d, LEAD_DECK, body_font, cw - 36)[:2]:
        d.text((mx + 18, y), line, font=body_font, fill=GREY)
        y += 17


def draw_big_stories(d):
    mx, cw = 28, CANVAS_W - 56
    y0 = 240
    d.text((mx, y0), "THE DAY’S BIG STORIES",
           font=load_font(SANS_BOLD, 15), fill=INK)
    d.line([(mx + 218, y0 + 8), (CANVAS_W - mx, y0 + 8)], fill=RULE, width=1)
    card_w, card_h, gap = (cw - 12) // 2, 74, 12
    for i, (tag, color, headline, deck) in enumerate(BIG_STORIES):
        x = mx + (i % 2) * (card_w + gap)
        y = y0 + 26 + (i // 2) * (card_h + gap)
        d.rectangle([x, y, x + card_w, y + card_h],
                    fill=CARD, outline=CARD_EDGE)
        d.rectangle([x, y, x + 6, y + card_h], fill=color)
        d.text((x + 14, y + 6), tag, font=load_font(SANS_BOLD, 11), fill=color)
        head_font, head_text = shrink_to_fit(
            d, headline, SANS_BOLD, 16, card_w - 24)
        d.text((x + 14, y + 21), head_text, font=head_font, fill=INK)
        body_font = load_font(SANS, 12)
        y2 = y + 41
        for line in wrap_text(d, deck, body_font, card_w - 24)[:2]:
            d.text((x + 14, y2), line, font=body_font, fill=GREY)
            y2 += 14


def draw_region_column(d, regions, x, y, col_w):
    for name, color, stories in regions:
        d.rectangle([x, y + 3, x + 10, y + 13], fill=color)
        d.text((x + 16, y), "%s (%d)" % (name, len(stories)),
               font=load_font(SANS_BOLD, 13), fill=color)
        y += 19
        for story in stories:
            f, text = shrink_to_fit(d, story, SANS, 12, col_w - 20)
            d.text((x + 16, y), "•  " + text, font=f, fill=INK)
            y += 15
        y += 5
    return y


def draw_briefs(d):
    mx, cw = 28, CANVAS_W - 56
    y0 = 524
    d.text((mx, y0), "THE WORLD IN BRIEF",
           font=load_font(SANS_BOLD, 15), fill=INK)
    d.line([(mx + 196, y0 + 8), (CANVAS_W - mx, y0 + 8)], fill=RULE, width=1)
    top = y0 + 26
    col_w = (cw - 12) // 2
    left_end = draw_region_column(d, REGIONS[:4], mx, top, col_w)
    right_end = draw_region_column(d, REGIONS[4:], mx + col_w + 12, top, col_w)
    # Explainer box under the shorter (right) column.
    box_x = mx + col_w + 12
    box_y = right_end + 6
    box_h = 76
    d.rectangle([box_x, box_y, CANVAS_W - mx, box_y + box_h],
                fill=CARD, outline=CARD_EDGE)
    d.text((box_x + 14, box_y + 8), "HOW TO READ THIS PAGE",
           font=load_font(SANS_BOLD, 12), fill=INK)
    note_font = load_font(SANS, 12)
    note = ("One day, seven regions: every story on this page was "
            "reported on 24–25 November 2026.")
    y = box_y + 28
    for line in wrap_text(d, note, note_font, col_w - 28):
        d.text((box_x + 14, y), line, font=note_font, fill=GREY)
        y += 15
    d.text((box_x + 14, y),
           "Lead + 6 big stories + 40 in brief = 47 stories.",
           font=note_font, fill=GREY)
    return left_end


def draw_footer(d):
    mx = 28
    fy = CANVAS_H - 30
    d.line([(mx, fy), (CANVAS_W - mx, fy)], fill=RULE, width=1)
    d.text((CANVAS_W / 2, fy + 6),
           "THE WORLD TODAY — 25 November 2026  ·  All stories as reported 24–25 Nov 2026",
           font=load_font(SANS, 11), fill=GREY, anchor="ma")


def render():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d)
    draw_big_stories(d)
    draw_briefs(d)
    draw_footer(d)
    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    render()
