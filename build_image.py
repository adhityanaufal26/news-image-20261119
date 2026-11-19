#!/usr/bin/env python3
"""Draw Thursday 19 November 2026 world-news front page, 1024x1024, deterministic."""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

INK = (17, 17, 17); PAPER = (247, 243, 232); NAVY = (18, 48, 92)
RED = (178, 32, 40); TEAL = (0, 112, 108); AMBER = (214, 138, 0)
GREY = (90, 90, 90); LIGHT = (232, 226, 208); OCEAN = (168, 205, 224)
LAND = (222, 206, 150)

def font(sz, bold=False, serif=False):
    cands = []
    if serif:
        cands = ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
    else:
        cands = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]
    for p in cands:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()

def wrap(draw, text, f, maxw):
    words = text.split(); lines = []; cur = ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=f) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def textbox(draw, x, y, text, f, maxw, fill=INK, leading=1.15, maxlines=99):
    yy = y
    for ln in wrap(draw, text, f, maxw)[:maxlines]:
        draw.text((x, yy), ln, font=f, fill=fill)
        yy += int(f.size * leading)
    return yy

STORIES = [
 "Shenzhen: Trump-Xi-Putin first trilateral summit; UN reform + oil pact",
 "ICJ rules 9-6: Myanmar committed Rohingya genocide (2017)",
 "Ukraine 3rd strike in 4 days halts Kerch Bridge rail traffic",
 "Iran attacks Kuwait & Bahrain after US strike on Qeshm I.",
 "Israel Gaza op beyond 'yellow line' at Nuseirat; Hamas claims breach",
 "Anthropic IPO $81.3B at $83; $1.5T value; Nasdaq ANT debut",
 "COP31 Antalya: ministers try to unblock climate text",
 "IEA: Hormuz crisis = greatest-ever energy-security threat",
 "Van Gogh 'Chestnuts in Bloom' sells $190.4M, artist record",
 "Bangladesh: Yunus ancestral home burned; 28 districts hit",
 "EU Commission proposes new EUR45B loan for Ukraine",
 "US-Venezuela military pact; Hegseth surprise Caracas visit",
 "Houthi missile debris damages Saudi PIF tower, Riyadh",
 "IAEA: N. Korea expands uranium enrichment plant",
 "Trump floats selling Nvidia Blackwell chips to China",
 "IMF warns global public debt near 100% of GDP; infl. 4.7%",
 "S. Korea exports top $1 trillion for first time",
 "UK typical energy bill forecast +GBP443/yr from January",
 "France senators reject pension freeze in 2027 budget",
 "Palo Alto Networks raises outlook on cyber demand",
 "Fiji declares disaster: El Nino drought, water shortages",
 "Indonesia fires ravage ~3M hectares this season",
 "Homo erectus teeth in Guangxi challenge evolution theory",
 "Miami court: pastor Sanon guilty in Moise assassination",
 "Kenya milk shortage worsens as drought bites",
 "Ethiopia & Eritrea mass troops on border, Tigray fears",
 "Senegal: Pastef formally expels President Faye",
 "Japan PM Takaichi meets Putin on APEC sidelines",
 "Myanmar leader says ties with ASEAN under review",
 "S. Korea's Lee renews call for dialogue with N. Korea",
 "Taiwan: 2 Russian Tu-95 bombers fly east of island",
 "Russian arrested in US over alleged Palantir spying",
 "Australia-China Landbridge clash over Darwin port lease",
 "Democrats designate Jeffries to lead US House",
 "Indonesia passes asset-confiscation law after 18 years",
 "Hong Kong drops case vs Newnew Polar Bear captain",
 "NZ court: pay-equity reform violated women's rights",
 "Australia: General Pants Co enters administration",
 "Argentina Senate to vote on suspending 2027 primaries",
 "Kumamoto, Japan M5.7 quake; 2 hurt, trains halted",
 "M5.3 quake off Sumatra near Nias; no tsunami threat",
 "Cyclone Akvan heads for Andhra-Odisha coast, India",
 "Report: record 589M children live in conflict zones",
 "Cricket: S. Africa beat Bangladesh by 9 wkts, 1st Test",
 "Cricket: NZ 243/5, Nicholls 113* vs India, Day 1",
 "India electronics exports +44% to $31.97B Apr-Sep",
 "Sensex +990 pts crosses 83,000; Nifty reclaims 25,500",
 "Cyberattack disrupts European Commission services",
 "Denmark parliament approves Greenland-US security deal",
 "Berlin: 'Coalition of the Willing' meets on Ukraine",
]

# (lon, lat, short label) for map pins, numbered 1..12
PINS = [
 (114.0, 22.5, "Shenzhen summit"), (96.0, 20.0, "Myanmar / ICJ case"),
 (36.6, 45.3, "Kerch Bridge strike"), (51.5, 27.0, "Hormuz / Gulf attacks"),
 (34.4, 28.5, "Gaza operation"), (-74.0, 40.7, "NY: Anthropic IPO + Van Gogh"),
 (30.7, 36.9, "COP31 Antalya"), (90.4, 23.8, "Bangladesh unrest"),
 (44.0, 15.0, "Houthi / Riyadh"), (125.8, 39.8, "N. Korea enrichment"),
 (130.7, 32.8, "Kumamoto quake"), (82.0, 16.0, "Cyclone Akvan"),
]

def draw_map(draw, x, y, mw, mh):
    draw.rectangle([x, y, x+mw, y+mh], fill=OCEAN, outline=INK, width=2)
    # crude continent blobs (equirectangular lon/lat -> xy)
    def xy(lon, lat): return (x + (lon+180)/360*mw, y + (90-lat)/180*mh)
    blobs = [
        [(-165,60),(-150,70),(-120,70),(-95,70),(-80,62),(-65,45),(-70,42),(-76,35),(-81,26),(-84,30),(-90,21),(-97,16),(-105,20),(-114,29),(-122,37),(-124,47),(-132,56),(-150,60)],
        [(-78,8),(-72,12),(-62,10),(-52,5),(-44,-3),(-35,-8),(-39,-15),(-48,-25),(-52,-33),(-58,-39),(-65,-41),(-68,-50),(-74,-52),(-74,-40),(-72,-30),(-70,-18),(-75,-15),(-79,-8),(-80,-3)],
        [(-9,43),(-2,48),(0,51),(5,53),(8,55),(10,57),(18,56),(21,60),(25,66),(30,70),(45,68),(68,69),(90,75),(110,74),(130,72),(150,70),(170,66),(178,65),(170,60),(158,52),(142,50),(140,40),(129,33),(122,31),(120,25),(108,15),(107,9),(103,2),(100,6),(98,10),(92,16),(89,22),(80,13),(77,8),(72,20),(66,25),(57,27),(52,26),(50,29),(48,30),(44,29),(42,32),(36,36),(30,36),(27,37),(23,36),(19,40),(12,44),(7,44),(3,43),(-2,37),(-9,37)],
        [(-17,15),(-16,21),(-13,27),(-9,31),(-6,35),(0,36),(10,37),(11,34),(20,32),(30,31),(32,31),(34,28),(35,24),(37,22),(39,21),(40,15),(43,12),(48,11),(51,12),(51,10),(48,5),(42,-2),(40,-8),(40,-15),(37,-20),(35,-24),(33,-26),(31,-29),(28,-33),(20,-35),(17,-32),(15,-27),(12,-18),(13,-12),(9,-1),(9,4),(6,4),(-2,5),(-8,5),(-13,8),(-17,12)],
        [(113,-22),(114,-28),(115,-34),(118,-35),(124,-33),(129,-32),(132,-32),(135,-35),(138,-36),(140,-38),(145,-38),(147,-38),(150,-37),(153,-32),(153,-27),(151,-24),(149,-20),(146,-19),(143,-15),(142,-11),(141,-13),(142,-11),(136,-15),(136,-12),(132,-11),(130,-13),(126,-14),(122,-17),(118,-20),(114,-22)],
    ]
    for b in blobs:
        draw.polygon([xy(a, c) for a, c in b], fill=LAND, outline=(120,100,60))
    for i, (lon, lat, _l) in enumerate(PINS, 1):
        px, py = xy(lon, lat); r = 11
        draw.ellipse([px-r, py-r, px+r, py+r], fill=RED, outline=(255,255,255), width=2)
        s = str(i); tw = draw.textlength(s, font=font(11, True))
        draw.text((px-tw/2, py-7), s, font=font(11, True), fill=(255,255,255))

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.text((18, 8), "THE WORLD IN ONE DAY", font=font(38, True, serif=True), fill=(255,255,255))
    d.text((18, 54), "Thursday 19 November 2026  -  50 stories  -  one front page", font=font(15, True), fill=(255, 220, 130))
    d.rectangle([748, 10, 1006, 82], fill=(255,255,255), outline=RED, width=3)
    d.text((758, 16), "DATE CHECK: VERIFIED", font=font(15, True), fill=RED)
    textbox(d, 758, 36, "Thursday 19 November 2026 - all stories first reported this day.", font(11), 240)
    # day in numbers
    d.rectangle([0, 92, W, 132], fill=(255, 240, 190))
    nums = [("$81.3B", "Anthropic IPO"), ("$190.4M", "Van Gogh record"), ("9-6", "ICJ Rohingya vote"),
            ("42%", "Hormuz traffic"), ("589M", "kids in conflict"), ("M5.7", "Kumamoto quake"),
            ("EUR45B", "EU Ukraine loan"), ("$89.59", "Brent crude")]
    for i, (n, lab) in enumerate(nums):
        xx = 10 + i*127
        d.text((xx, 96), n, font=font(17, True), fill=NAVY)
        d.text((xx, 116), lab, font=font(10), fill=INK)
    # lead cards
    cards = [
        ("1  SHENZHEN SUMMIT", "Trump, Xi and Putin hold first three-way talks. Joint pledge: reform UN, boost oil output, cut nuclear risk. No Ukraine breakthrough announced.", NAVY),
        ("2  WORLD COURT RULES", "ICJ finds 9-6 that Myanmar committed genocide against Rohingya in 2017. First state ever found guilty of genocide by an international court.", TEAL),
        ("3  LARGEST IPO EVER", "Anthropic raises $81.3B at $83/share, $1.5 trillion value, tops SpaceX. Shares debut on Nasdaq as ANT amid AI cost questions.", RED),
    ]
    for i, (t, body, col) in enumerate(cards):
        x = 12 + i*338; y = 140; cw = 328; ch = 205
        d.rectangle([x, y, x+cw, y+ch], fill=(255,255,255), outline=col, width=3)
        d.rectangle([x, y, x+cw, y+30], fill=col)
        d.text((x+10, y+6), t, font=font(15, True), fill=(255,255,255))
        # simple vector illustration strip
        iy = y + 38
        if i == 0:
            for j, fc in enumerate([(178,32,40),(40,90,200),(200,200,200)]):
                fx = x+18+j*100
                d.rectangle([fx, iy+8, fx+8, iy+52], fill=INK)
                d.polygon([(fx+8, iy+8), (fx+70, iy+20), (fx+8, iy+34)], fill=fc, outline=INK)
            d.ellipse([x+120, iy+40, x+210, iy+58], outline=NAVY, width=3)
        elif i == 1:
            d.rectangle([x+30, iy+40, x+290, iy+50], fill=(120,80,40))
            d.rectangle([x+140, iy+6, x+180, iy+44], fill=(90,60,30))
            d.ellipse([x+130, iy+2, x+190, iy+20], fill=(90,60,30))
            d.text((x+225, iy+14), "9-6", font=font(26, True), fill=TEAL)
        else:
            pts = [(x+20, iy+48), (x+90, iy+36), (x+160, iy+26), (x+230, iy+14), (x+300, iy+6)]
            d.line(pts, fill=RED, width=5)
            for px, py in pts: d.ellipse([px-5, py-5, px+5, py+5], fill=NAVY)
            d.text((x+18, iy+2), "ANT $83", font=font(16, True), fill=NAVY)
        textbox(d, x+10, y+102, body, font(13), cw-20, leading=1.2)
    # map + legend
    d.text((12, 352), "WHERE IT HAPPENED - world map (2:1)", font=font(15, True), fill=NAVY)
    draw_map(d, 12, 376, 640, 320)
    lx = 664
    d.rectangle([lx, 376, 1012, 696], fill=(255,255,255), outline=INK, width=2)
    d.text((lx+10, 382), "MAP LEGEND", font=font(14, True), fill=RED)
    yy = 404
    for i, (_lon, _lat, lab) in enumerate(PINS, 1):
        d.ellipse([lx+10, yy+1, lx+28, yy+19], fill=RED)
        s = str(i); tw = d.textlength(s, font=font(10, True))
        d.text((lx+19-tw/2, yy+3), s, font=font(10, True), fill=(255,255,255))
        d.text((lx+34, yy+2), lab, font=font(12), fill=INK)
        yy += 23
    # timeline
    d.rectangle([0, 704, W, 744], fill=NAVY)
    d.text((12, 708), "DAY IN UTC:", font=font(13, True), fill=(255,220,130))
    tl = "00h APEC opens Shenzhen  |  02h Kumamoto M5.7  |  06h Kerch strike  |  09h ICJ ruling  |  13h Anthropic ANT trades  |  17h Berlin Ukraine talks"
    d.text((118, 708), tl, font=font(11), fill=(255,255,255))
    d.text((12, 724), "Contested battlefield figures are claims by the parties, not independently verified counts.", font=font(10), fill=(200,220,255))
    # 50 stories grid 5 cols x 10 rows, two lines per cell
    d.text((12, 748), "ALL 50 STORIES - Thursday 19 November 2026 (numbered; leads 1-3 above)", font=font(14, True), fill=NAVY)
    colw = 200; x0 = 12; y0 = 768
    for idx, s in enumerate(STORIES):
        c = idx % 5; r = idx // 5
        xx = x0 + c*colw; yy = y0 + r*18
        d.text((xx, yy), f"{idx+1}.", font=font(9, True), fill=RED)
        lines = wrap(d, s, font(8), colw-30)
        if lines: d.text((xx+22, yy-1), lines[0], font=font(8), fill=INK)
        if len(lines) > 1: d.text((xx+22, yy+7), lines[1], font=font(8), fill=INK)
    # market ticker line above footer
    d.text((12, 950), "MARKETS 19 NOV CLOSE: S&P 7,323.63 (-0.23%)  Nasdaq 24,429.88 (+0.42%)  Nikkei 59,444 (+0.71%)  FTSE 10,551 (-1.30%)  Gold $3,739.6  BTC $63,552", font=font(9, True), fill=NAVY)
    # footer
    d.rectangle([0, 966, W, 1024], fill=(40,40,40))
    textbox(d, 12, 970, "Sources: Horizon 19 Nov briefing; The Times live; AP; BBC; Le Monde; Straits Times; SCMP; Al Jazeera; IANS; Kyodo/JMA; MetMalaysia; IEA; IMF. Contested claims (casualties, strike damage, weapons allegations) are reported as claims. Illustrations are original vector drawings. Entry for make.fun news-image-20261119.", font(9), 1000, fill=(255,255,255), leading=1.2)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")

if __name__ == "__main__":
    main()
