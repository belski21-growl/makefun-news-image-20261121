#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261121 (LOCAL BUILD TOOL ONLY).

Draws a dense newspaper front page with PIL + DejaVu fonts. This script is
NOT run by the grader: the shipped main.py only copies the finished
entry.png. Run: python3 generate.py  ->  writes entry.png next to itself.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (176, 30, 36)
RULE = (201, 191, 168)
PANEL = (255, 253, 246)
MUTED = (90, 84, 70)

SECTIONS = {
    "EU": (31, 78, 121),      # Europe - deep blue
    "ME": (122, 62, 0),       # Middle East & Asia - amber brown
    "AF": (30, 107, 58),      # Africa & the Americas - green
    "SC": (107, 45, 122),     # Science, sport & culture - purple
}

FDIR = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FDIR + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

# (section, headline, deck) - 34 grid stories, numbered 3..36.
# Leads 1-2 are drawn separately. Every fact below was verified against
# BBC / Reuters / AP / AFP reporting of 21 Nov 2026 (see build-log.md).
GRID = [
 ("EU", "UK and EU sign food and youth deals",
  "Burnham seals three Brussels deals; both sides call them landmark."),
 ("EU", "COP31 talks run into overtime",
  "Draft deal drops fossil fuels; a third text is due on Saturday."),
 ("EU", "French police sentenced over Zecler beating",
  "Court upholds racism as an aggravating factor."),
 ("EU", "Estonia closes its border with Russia",
  "Tallinn shuts the crossings as Baltic states raise the alarm."),
 ("EU", "Denmark says it foiled a Russian murder plot",
  "Copenhagen says the plot to kill a US-Ukrainian rapper failed."),
 ("EU", "Portugal's public sector walks out",
  "Strike hits schools and services across the country."),
 ("EU", "France and Germany strike ECB deal",
  "Paris and Berlin agree on the central bank's top jobs."),
 ("EU", "Lufthansa to cut 1,000 jobs",
  "Airline blames weak demand; German youths protest cuts."),
 ("ME", "World court: Myanmar committed genocide",
  "ICJ rules against Myanmar over the Rohingya in The Hague."),
 ("ME", "Trump, Xi, Putin summit ends flat",
  "First trilateral meeting in Shenzhen yields few concrete results."),
 ("ME", "Iran war nears its ninth month",
  "Trump says he is in no rush and may not decide until 2027."),
 ("ME", "Saudi jets down Houthi missiles",
  "Three missiles intercepted over Riyadh; coalition hits Hodeidah."),
 ("ME", "Iraq moves against Iran-backed militia",
  "Baghdad launches operations against the armed group."),
 ("ME", "Man jailed 19 years over US murder plot",
  "Indian man sentenced over a plan to kill a Sikh separatist leader."),
 ("ME", "Nepal's new leader faces his India test",
  "PM Balendra Shah navigates ties with the old neighbour."),
 ("ME", "US opens Pacific deep-sea mining auction",
  "Washington auctions ocean-floor licences in the Pacific."),
 ("AF", "ANC fights to hold South Africa's big cities",
  "Ruling party battles to keep control after an election setback."),
 ("AF", "Nearly 600 women killed in South Africa",
  "Femicide figures in three months shock the country."),
 ("AF", "Sudan war hits disabled children's schooling",
  "Conflict leaves disabled children out of class, aid groups warn."),
 ("AF", "Mamdani vows to close Rikers Island by 2032",
  "New York's mayor sets a date to shut the notorious jail."),
 ("AF", "LA jury convicts Palisades Fire arsonist",
  "Jonathan Rinderknecht found guilty of starting the blaze."),
 ("AF", "Texas execution takes more than an hour",
  "Death-row inmate screams as the procedure drags on."),
 ("AF", "Trump: US flight systems 'ancient' but 'safe'",
  "President defends air safety after a nationwide ground stop."),
 ("AF", "US declassifies more UFO footage",
  "Newly released clips were filmed over the Middle East."),
 ("SC", "BepiColombo reaches Mercury after 8 years",
  "ESA-JAXA probe enters orbit; science starts in April 2027."),
 ("SC", "Pill hailed as pancreatic cancer breakthrough",
  "New drug offers hope against one of the deadliest cancers."),
 ("SC", "AI maths claim sparks debate",
  "Researcher says Claude helped prove the Riemann Hypothesis."),
 ("SC", "Kane out for months with ankle injury",
  "Bayern star tears a ligament in the 1-1 draw with Koln."),
 ("SC", "Alcaraz beats Cobolli 6-4, 6-1",
  "Injured star completes a perfect ATP Finals group stage."),
 ("SC", "Price beats Kotaskova to undisputed crown",
  "Boxer unifies the titles in a thriller."),
 ("SC", "F1: Russell, Verstappen touch in Vegas",
  "Rivals make contact in final Las Vegas practice."),
 ("SC", "Kim leads LPGA finale after ace",
  "Hole-in-one puts her clear at the season finale."),
 ("SC", "England target style win over All Blacks",
  "Stacked England side aim to pile on the misery."),
 ("SC", "US police warn GTA 6 fans",
  "Officers say: what happens in GTA 6 stays in GTA 6."),
]

LEADS = [
 ("POLAND  •  NATO ON ALERT",
  "Russian missile hits Poland during NATO exercise",
  "Warsaw calls it a deliberate provocation; NATO condemns a grave "
  "violation of allied airspace."),
 ("MARKETS  •  WALL STREET",
  "Stocks slide into correction as AI shares plunge",
  "S&P 500 falls about 3.7% on Friday; Nvidia down 22.9% in five sessions, "
  "its worst week since 2008."),
]

SECTION_NAMES = {"EU": "EUROPE", "ME": "MIDDLE EAST & ASIA",
                 "AF": "AFRICA & THE AMERICAS", "SC": "SCIENCE, SPORT & CULTURE"}


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, font, max_w, max_lines):
    """Wrap to at most max_lines, truncating the last with an ellipsis."""
    lines = wrap(draw, text, font, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and draw.textlength(lines[-1] + " ...", font=font) > max_w:
        lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else lines[-1][:-1]
    lines[-1] = lines[-1] + " ..."
    return lines


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ------------------------------------------------------
    d.rectangle([18, 10, 1006, 15], fill=INK)
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 24), title, font=tf, fill=INK)
    d.rectangle([18, 96, 1006, 98], fill=RED)
    dl = "SATURDAY, 21 NOVEMBER 2026   —   36 STORIES FROM EVERY CONTINENT"
    df = SANS_B(17)
    dw = d.textlength(dl, font=df)
    d.text(((W - dw) / 2, 106), dl, font=df, fill=INK)
    d.rectangle([18, 132, 1006, 134], fill=INK)

    # ---- Lead row: two big stories ------------------------------------
    ly, lh = 146, 136
    lw = 484
    for i, (kicker, head, deck) in enumerate(LEADS):
        x = 18 + i * (lw + 10)
        d.rectangle([x, ly, x + lw, ly + lh], fill=PANEL, outline=RULE, width=1)
        d.rectangle([x, ly, x + 5, ly + lh], fill=RED)
        kx, ky = x + 18, ly + 10
        d.text((kx, ky), kicker, font=SANS_B(14), fill=RED)
        hf = SERIF_B(24)
        hlines = fit_lines(d, head, hf, lw - 36, 2)
        hy = ky + 24
        for ln in hlines:
            d.text((kx, hy), ln, font=hf, fill=INK)
            hy += 27
        df2 = SANS(14)
        dlines = fit_lines(d, deck, df2, lw - 36, 2)
        dy = ly + 94
        for ln in dlines:
            d.text((kx, dy), ln, font=df2, fill=MUTED)
            dy += 16

    # ---- Section key ----------------------------------------------------
    sy = 290
    parts = []
    x = 18
    kf = SANS_B(12)
    for code in ("EU", "ME", "AF", "SC"):
        label = SECTION_NAMES[code]
        d.rectangle([x, sy, x + 12, sy + 12], fill=SECTIONS[code])
        d.text((x + 17, sy - 1), label, font=kf, fill=INK)
        x += 17 + int(d.textlength(label, font=kf)) + 26
    d.rectangle([18, 308, 1006, 310], fill=INK)

    # ---- Grid: 4 cols x 9 rows, 34 stories + source strip -------------
    gx, gy = 18, 320
    cw, ch, gapx, gapy = 239, 71, 10, 5
    hf = SANS_B(14)
    df3 = SANS(11)
    for idx, (code, head, deck) in enumerate(GRID):
        row, col = divmod(idx, 4)
        x = gx + col * (cw + gapx)
        y = gy + row * (ch + gapy)
        num = str(idx + 3)
        d.rounded_rectangle([x, y + 3, x + 22, y + 25], radius=4, fill=SECTIONS[code])
        nf = SANS_B(12)
        nw = d.textlength(num, font=nf)
        d.text((x + (22 - nw) / 2, y + 6), num, font=nf, fill=(255, 255, 255))
        tx = x + 30
        hlines = fit_lines(d, head, hf, cw - 30, 2)
        hy = y + 2
        for ln in hlines:
            d.text((tx, hy), ln, font=hf, fill=INK)
            hy += 18
        dlines = fit_lines(d, deck, df3, cw - 30, 2)
        dy = hy + 2
        for ln in dlines:
            d.text((tx, dy), ln, font=df3, fill=MUTED)
            dy += 14
        d.line([x, y + ch - 2, x + cw, y + ch - 2], fill=RULE, width=1)

    # Source strip in the last row's spare cells (cols 2-3 of row 8).
    sx = gx + 2 * (cw + gapx)
    sy2 = gy + 8 * (ch + gapy)
    sw = 2 * cw + gapx
    d.rectangle([sx, sy2, sx + sw, sy2 + ch - 2], fill=(233, 226, 208))
    sf = SANS_B(12)
    d.text((sx + 10, sy2 + 8), "SOURCES", font=sf, fill=RED)
    sbody = ("BBC, Reuters, AP, AFP and ESA reporting of Saturday 21 November 2026. "
             "Every story above was first reported on that day.")
    slines = fit_lines(d, sbody, SANS(12), sw - 20, 3)
    yy = sy2 + 26
    for ln in slines:
        d.text((sx + 10, yy), ln, font=SANS(12), fill=INK)
        yy += 14

    # ---- Footer ---------------------------------------------------------
    d.rectangle([18, 1002, 1006, 1004], fill=INK)
    foot = "THE WORLD IN ONE DAY  •  SATURDAY 21 NOVEMBER 2026  •  ONE DAY, EVERY CONTINENT"
    ff = SANS_B(11)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 1010), foot, font=ff, fill=MUTED)

    return img


if __name__ == "__main__":
    import hashlib, os
    img = draw()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    data = open(out, "rb").read()
    print("wrote", out, len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())
    print("size", img.size, "mode", img.mode)
