"""
Generate the demo site's images and PDFs with Pillow.

    python seed/make_assets.py

Writes to seed/assets/images/ and seed/assets/documents/. The output is
committed so seeding is repeatable; rerun this only to change the artwork.
Everything is drawn from shapes and text: no downloads, no photos of people.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from core import seed_data  # noqa: E402

IMAGES = os.path.join(HERE, 'assets', 'images')
DOCUMENTS = os.path.join(HERE, 'assets', 'documents')

NAVY = (20, 40, 75)
NAVY_DARK = (12, 26, 51)
NAVY_LIGHT = (42, 69, 116)
GOLD = (201, 162, 39)
GOLD_LIGHT = (232, 207, 122)
CREAM = (247, 245, 239)
GUM = (74, 110, 82)
GUM_DARK = (46, 76, 58)
SS = 2  # supersampling factor

FONT_DIR = os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts')


def font(name, size):
    candidates = {
        'serif-bold': ['georgiab.ttf', 'DejaVuSerif-Bold.ttf'],
        'serif': ['georgia.ttf', 'DejaVuSerif.ttf'],
        'sans': ['segoeui.ttf', 'arial.ttf', 'DejaVuSans.ttf'],
        'sans-bold': ['segoeuib.ttf', 'arialbd.ttf', 'DejaVuSans-Bold.ttf'],
    }[name]
    for filename in candidates:
        for folder in (FONT_DIR, '/usr/share/fonts/truetype/dejavu'):
            path = os.path.join(folder, filename)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(size, top, bottom):
    w, h = size
    img = Image.new('RGB', size, top)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        draw.line([(0, y), (w, y)], fill=lerp(top, bottom, y / max(h - 1, 1)))
    return img


def canvas(w, h, top, bottom):
    img = gradient((w * SS, h * SS), top, bottom)
    return img, ImageDraw.Draw(img)


def finish(img, w, h, path, quality=86):
    img = img.resize((w, h), Image.LANCZOS)
    img.save(path, 'JPEG', quality=quality, optimize=True, progressive=True)
    print('wrote', os.path.relpath(path, ROOT))


def hills(draw, w, h, base, amp, colour, seed, freq=2.0):
    rng = random.Random(seed)
    phase = rng.uniform(0, math.pi * 2)
    pts = []
    for x in range(0, w + 1, 8 * SS):
        y = base + amp * math.sin(phase + freq * math.pi * x / w) + amp * 0.35 * math.sin(phase * 2 + 5 * math.pi * x / w)
        pts.append((x, y))
    pts += [(w, h), (0, h)]
    draw.polygon(pts, fill=colour)


def tree(draw, x, ground, scale, colour, trunk=(92, 70, 52)):
    s = scale * SS
    draw.rectangle([x - 5 * s, ground - 60 * s, x + 5 * s, ground], fill=trunk)
    for dx, dy, r in [(0, -95, 42), (-30, -70, 32), (30, -72, 34), (-12, -120, 30), (18, -112, 28)]:
        draw.ellipse([x + dx * s - r * s, ground + dy * s - r * s, x + dx * s + r * s, ground + dy * s + r * s], fill=colour)


def building(draw, x, ground, width, height, colour, window, roof=None, seed=0):
    rng = random.Random(seed)
    draw.rectangle([x, ground - height, x + width, ground], fill=colour)
    if roof:
        draw.polygon([(x - 12 * SS, ground - height), (x + width / 2, ground - height - roof), (x + width + 12 * SS, ground - height)], fill=NAVY_DARK)
    cols = max(int(width / (46 * SS)), 1)
    rows = max(int((height - 30 * SS) / (58 * SS)), 1)
    ww = width / cols
    for c in range(cols):
        for r in range(rows):
            lit = rng.random() < 0.72
            wx = x + c * ww + ww * 0.28
            wy = ground - height + 26 * SS + r * 58 * SS
            draw.rectangle([wx, wy, wx + ww * 0.44, wy + 30 * SS], fill=window if lit else lerp(colour, NAVY_DARK, .5))


def banner_campus(w, h, path):
    img, d = canvas(w, h, (28, 52, 96), (214, 150, 92))
    W, H = w * SS, h * SS
    d.ellipse([W * .70, H * .18, W * .80, H * .18 + W * .10], fill=GOLD_LIGHT)
    hills(d, W, H, H * .62, H * .05, (58, 72, 104), 3)
    ground = H * .80
    building(d, W * .22, ground, W * .30, H * .30, (60, 58, 84), GOLD_LIGHT, roof=H * .08, seed=1)
    d.rectangle([W * .355, ground - H * .47, W * .385, ground - H * .30], fill=(60, 58, 84))  # clock tower
    d.polygon([(W * .345, ground - H * .47), (W * .37, ground - H * .54), (W * .395, ground - H * .47)], fill=NAVY_DARK)
    d.ellipse([W * .362, ground - H * .45, W * .378, ground - H * .45 + W * .016], fill=CREAM)
    building(d, W * .54, ground, W * .20, H * .20, (72, 70, 96), GOLD_LIGHT, seed=2)
    building(d, W * .05, ground, W * .14, H * .16, (72, 70, 96), GOLD_LIGHT, seed=3)
    hills(d, W, H, H * .83, H * .02, GUM_DARK, 5, freq=1)
    for x, sc in [(.80, 1.5), (.90, 1.9), (.02, 1.4), (.97, 1.2)]:
        tree(d, W * x, H * .86, sc, GUM_DARK)
    finish(img, w, h, path)


def banner_grounds(w, h, path):
    img, d = canvas(w, h, (170, 205, 225), (244, 230, 190))
    W, H = w * SS, h * SS
    hills(d, W, H, H * .55, H * .06, (122, 150, 128), 11)
    hills(d, W, H, H * .66, H * .05, (96, 130, 100), 12)
    hills(d, W, H, H * .78, H * .03, (80, 116, 84), 13, freq=1.2)
    # path
    d.polygon([(W * .44, H), (W * .56, H), (W * .515, H * .70), (W * .495, H * .70)], fill=(214, 196, 150))
    rng = random.Random(7)
    for i in range(14):
        side = -1 if i % 2 else 1
        x = W * .5 + side * W * (.07 + (i // 2) * .065) + rng.uniform(-20, 20) * SS
        tree(d, x, H * (.93 - (i // 2) * .025), 2.3 - (i // 2) * .18, lerp(GUM, GUM_DARK, rng.random()))
    finish(img, w, h, path)


def banner_library(w, h, path):
    img, d = canvas(w, h, (58, 44, 36), (30, 22, 20))
    W, H = w * SS, h * SS
    rng = random.Random(21)
    spines = [NAVY, NAVY_LIGHT, GOLD, (122, 46, 60), (46, 90, 70), (150, 110, 60), CREAM, (90, 60, 110)]
    shelf_h = H / 4
    for s in range(4):
        y1 = s * shelf_h + shelf_h * .12
        y2 = (s + 1) * shelf_h - 14 * SS
        x = 30 * SS
        while x < W - 30 * SS:
            bw = rng.randint(22, 58) * SS
            bh = (y2 - y1) * rng.uniform(.72, .98)
            col = rng.choice(spines)
            if rng.random() < .08:  # a leaning book
                d.polygon([(x, y2), (x + bw, y2), (x + bw + bh * .25, y2 - bh), (x + bh * .25, y2 - bh)], fill=col)
                x += bw + bh * .25 + 6 * SS
                continue
            d.rectangle([x, y2 - bh, x + bw, y2], fill=col)
            band = lerp(col, GOLD_LIGHT, .55)
            d.rectangle([x, y2 - bh * .82, x + bw, y2 - bh * .78], fill=band)
            d.rectangle([x, y2 - bh * .22, x + bw, y2 - bh * .18], fill=band)
            x += bw + 3 * SS
        d.rectangle([0, y2, W, y2 + 18 * SS], fill=(110, 78, 50))
    glow = Image.new('RGB', img.size, GOLD_LIGHT)
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).ellipse([W * .55, -H * .3, W * 1.2, H * .6], fill=70)
    mask = mask.filter(ImageFilter.GaussianBlur(120 * SS))
    img = Image.composite(glow, img, mask)
    finish(img, w, h, path)


def banner_pattern(w, h, path):
    img, d = canvas(w, h, NAVY, NAVY_DARK)
    W, H = w * SS, h * SS
    size = 120 * SS
    rng = random.Random(4)
    for row in range(int(H / size) + 2):
        for col in range(int(W / size) + 2):
            x, y = col * size, row * size
            pick = rng.random()
            if pick < .18:
                colour = GOLD
            elif pick < .45:
                colour = NAVY_LIGHT
            else:
                continue
            if (row + col) % 2:
                d.polygon([(x, y), (x + size, y), (x, y + size)], fill=colour)
            else:
                d.polygon([(x + size, y), (x + size, y + size), (x, y + size)], fill=colour)
    for i in range(6):
        cx, cy = rng.uniform(0, W), rng.uniform(0, H)
        r = rng.uniform(60, 160) * SS
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD_LIGHT, width=6 * SS)
    finish(img, w, h, path)


def banner_sport(w, h, path):
    img, d = canvas(w, h, (150, 196, 222), (220, 236, 240))
    W, H = w * SS, h * SS
    hills(d, W, H, H * .42, H * .03, (110, 150, 120), 31)
    d.rectangle([0, H * .48, W, H], fill=(70, 140, 80))
    # running track in perspective
    lanes = 6
    for i in range(lanes + 1):
        t = i / lanes
        d.line([(W * (.30 - .30 * t), H), (W * (.47 - .06 * t), H * .52)], fill=CREAM, width=5 * SS)
        d.line([(W * (.70 + .30 * t), H), (W * (.53 + .06 * t), H * .52)], fill=CREAM, width=5 * SS)
    d.polygon([(W * .30, H), (W * .47, H * .52), (W * .53, H * .52), (W * .70, H)], fill=(186, 84, 60))
    for i in range(1, 4):
        t = i / 4
        d.line([(W * (.30 + .10 * t), H), (W * (.47 + .01 * t), H * .52)], fill=CREAM, width=4 * SS)
        d.line([(W * (.70 - .10 * t), H), (W * (.53 - .01 * t), H * .52)], fill=CREAM, width=4 * SS)
    d.rectangle([W * .30, H * .86, W * .70, H * .875], fill=CREAM)
    for x in (.12, .88):
        d.rectangle([W * x - 4 * SS, H * .30, W * x + 4 * SS, H * .50], fill=(230, 230, 230))
        d.polygon([(W * x + 4 * SS, H * .30), (W * x + 70 * SS, H * .33), (W * x + 4 * SS, H * .36)], fill=GOLD)
    finish(img, w, h, path)


def banner_stage(w, h, path):
    img, d = canvas(w, h, (26, 16, 34), (12, 8, 18))
    W, H = w * SS, h * SS
    beams = Image.new('L', img.size, 0)
    bd = ImageDraw.Draw(beams)
    for x in (.2, .5, .8):
        bd.polygon([(W * x - 20 * SS, 0), (W * x + 20 * SS, 0), (W * x + W * .14, H * .82), (W * x - W * .14, H * .82)], fill=90)
    beams = beams.filter(ImageFilter.GaussianBlur(30 * SS))
    img = Image.composite(Image.new('RGB', img.size, GOLD_LIGHT), img, beams)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H * .82, W, H], fill=(70, 44, 30))
    for side in (0, 1):
        x0 = 0 if side == 0 else W * .86
        d.rectangle([x0, 0, x0 + W * .14, H * .82], fill=(122, 26, 40))
        for i in range(6):
            fx = x0 + i * W * .14 / 6
            d.line([(fx, 0), (fx, H * .82)], fill=(90, 18, 30), width=6 * SS)
    d.rectangle([0, 0, W, H * .08], fill=(122, 26, 40))
    for i in range(5):  # music stands
        x = W * (.3 + i * .1)
        d.line([(x, H * .82), (x, H * .70)], fill=NAVY_DARK, width=5 * SS)
        d.polygon([(x - 26 * SS, H * .66), (x + 26 * SS, H * .66), (x + 20 * SS, H * .70), (x - 20 * SS, H * .70)], fill=NAVY_DARK)
    finish(img, w, h, path)


def category_image(slug, colour_hex, w, h, path):
    colour = tuple(int(colour_hex[i:i + 2], 16) for i in (1, 3, 5))
    img, d = canvas(w, h, lerp(colour, (255, 255, 255), .25), lerp(colour, NAVY_DARK, .45))
    W, H = w * SS, h * SS
    rng = random.Random(slug)
    for i in range(18):  # soft background circles
        cx, cy, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(30, 140) * SS
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=lerp(colour, (255, 255, 255), rng.uniform(.1, .3)))
    cx, cy = W / 2, H / 2
    if slug == 'academic':
        for i, c in enumerate([NAVY, GOLD, CREAM, NAVY_LIGHT]):
            d.rectangle([cx - 230 * SS, cy + 120 * SS - i * 62 * SS, cx + 230 * SS - i * 30 * SS, cy + 176 * SS - i * 62 * SS], fill=c)
        for angle in (0, 60, 120):  # atom
            a = math.radians(angle)
            box = Image.new('L', img.size, 0)
            ImageDraw.Draw(box).ellipse([cx - 180 * SS, cy - 250 * SS, cx + 180 * SS, cy - 130 * SS], outline=255, width=7 * SS)
            box = box.rotate(angle, center=(cx, cy - 190 * SS))
            img.paste(GOLD_LIGHT, (0, 0), box)
        d = ImageDraw.Draw(img)
        d.ellipse([cx - 22 * SS, cy - 212 * SS, cx + 22 * SS, cy - 168 * SS], fill=CREAM)
    elif slug == 'sport':
        d.ellipse([cx - 190 * SS, cy - 190 * SS, cx + 190 * SS, cy + 190 * SS], fill=CREAM)
        d.arc([cx - 190 * SS, cy - 190 * SS, cx + 190 * SS, cy + 190 * SS], 0, 360, fill=NAVY, width=8 * SS)
        d.arc([cx - 300 * SS, cy - 120 * SS, cx - 20 * SS, cy + 160 * SS], -60, 60, fill=(186, 60, 50), width=8 * SS)
        d.arc([cx + 20 * SS, cy - 160 * SS, cx + 300 * SS, cy + 120 * SS], 120, 240, fill=(186, 60, 50), width=8 * SS)
    elif slug == 'arts':
        d.ellipse([cx - 260 * SS, cy - 190 * SS, cx + 260 * SS, cy + 190 * SS], fill=CREAM)
        d.ellipse([cx + 120 * SS, cy + 40 * SS, cx + 200 * SS, cy + 120 * SS], fill=lerp(colour, NAVY_DARK, .45))
        for (dx, dy), c in zip([(-150, -60), (-60, -120), (50, -110), (150, -40), (-130, 70)],
                               [GOLD, (186, 60, 50), NAVY_LIGHT, (46, 107, 48), (122, 46, 107)]):
            d.ellipse([cx + (dx - 42) * SS, cy + (dy - 42) * SS, cx + (dx + 42) * SS, cy + (dy + 42) * SS], fill=c)
    elif slug == 'community':
        ground = cy + 200 * SS
        d.rectangle([0, ground, W, H], fill=lerp(GUM, NAVY_DARK, .3))
        for x, sc in [(-260, 2.4), (0, 3.2), (250, 2.6)]:
            tree(d, cx + x * SS, ground, sc, lerp(GUM, GOLD, .15))
        d.ellipse([cx - 60 * SS, cy - 300 * SS, cx + 60 * SS, cy - 180 * SS], fill=GOLD_LIGHT)
    elif slug == 'open-day':
        ground = cy + 220 * SS
        d.rectangle([0, ground, W, H], fill=lerp(GUM, NAVY_DARK, .3))
        building(d, cx - 260 * SS, ground, 520 * SS, 300 * SS, CREAM, NAVY_LIGHT, roof=110 * SS, seed=9)
        d.rectangle([cx - 45 * SS, ground - 120 * SS, cx + 45 * SS, ground], fill=NAVY)
        for x in (-320, 320):
            d.line([(cx + x * SS, ground), (cx + x * SS, ground - 420 * SS)], fill=CREAM, width=6 * SS)
            d.polygon([(cx + x * SS, ground - 420 * SS), (cx + (x + 110) * SS, ground - 385 * SS), (cx + x * SS, ground - 350 * SS)], fill=GOLD)
    finish(img, w, h, path)


def avatar(initials, colour_hex, path, size=800):
    colour = tuple(int(colour_hex[i:i + 2], 16) for i in (1, 3, 5))
    S = size * SS
    img = gradient((S, S), lerp(colour, (255, 255, 255), .12), lerp(colour, NAVY_DARK, .35))
    d = ImageDraw.Draw(img)
    d.ellipse([S * .08, S * .08, S * .92, S * .92], outline=GOLD, width=10 * SS)
    f = font('serif-bold', int(300 * SS))
    tw, th = d.textsize(initials, font=f)
    offset_y = f.getoffset(initials)[1]
    d.text(((S - tw) / 2, (S - th - offset_y) / 2), initials, font=f, fill=CREAM)
    finish(img, size, size, path, quality=90)


# ---------------------------------------------------------------------------
# PDFs — A4 pages at 150 dpi, drawn with Pillow and saved as multi-page PDF
# ---------------------------------------------------------------------------

A4 = (1240, 1754)


class PdfWriter(object):
    def __init__(self, title):
        self.title = title
        self.pages = []
        self.new_page()

    def new_page(self):
        self.page = Image.new('RGB', A4, (255, 255, 255))
        self.draw = ImageDraw.Draw(self.page)
        self.pages.append(self.page)
        self.draw.rectangle([0, 0, A4[0], 150], fill=NAVY)
        self.draw.rectangle([0, 150, A4[0], 162], fill=GOLD)
        self.draw.text((90, 38), 'Kestrel Ridge College', font=font('serif-bold', 44), fill=(255, 255, 255))
        self.draw.text((90, 96), self.title, font=font('sans', 30), fill=GOLD_LIGHT)
        self.draw.text((90, A4[1] - 70), 'Kestrel Ridge College is a fictional school created for a software demonstration.',
                       font=font('sans', 20), fill=(120, 120, 120))
        self.y = 230

    def ensure(self, height):
        if self.y + height > A4[1] - 120:
            self.new_page()

    def heading(self, text):
        self.ensure(90)
        self.y += 20
        self.draw.text((90, self.y), text, font=font('serif-bold', 36), fill=NAVY)
        self.y += 64

    def para(self, text, size=26):
        f = font('sans', size)
        words, line = text.split(), ''
        for word in words:
            trial = (line + ' ' + word).strip()
            if self.draw.textsize(trial, font=f)[0] > A4[0] - 180:
                self.ensure(size + 14)
                self.draw.text((90, self.y), line, font=f, fill=(29, 36, 51))
                self.y += size + 14
                line = word
            else:
                line = trial
        if line:
            self.ensure(size + 14)
            self.draw.text((90, self.y), line, font=f, fill=(29, 36, 51))
            self.y += size + 14
        self.y += 16

    def table(self, rows, widths):
        f, fb = font('sans', 24), font('sans-bold', 24)
        for i, row in enumerate(rows):
            self.ensure(52)
            if i == 0:
                self.draw.rectangle([90, self.y - 8, A4[0] - 90, self.y + 40], fill=NAVY)
            elif i % 2 == 0:
                self.draw.rectangle([90, self.y - 8, A4[0] - 90, self.y + 40], fill=CREAM)
            x = 100
            for cell, width in zip(row, widths):
                self.draw.text((x, self.y), cell, font=fb if i == 0 else f, fill=(255, 255, 255) if i == 0 else (29, 36, 51))
                x += width
            self.y += 50
        self.y += 20

    def save(self, path):
        first, rest = self.pages[0], self.pages[1:]
        first.save(path, 'PDF', resolution=150.0, save_all=True, append_images=rest,
                   title=self.title, author='Kestrel Ridge College')
        print('wrote', os.path.relpath(path, ROOT))


def uniform_pdf(path):
    pdf = PdfWriter('Uniform Price List')
    pdf.para('All prices include GST and are fictional. Uniforms are sold at the College Uniform Shop, '
             'open Tuesday and Thursday 8:00 am to 10:00 am and during Open Days.')
    pdf.heading('Junior School (K-6)')
    pdf.table([
        ('Item', 'Sizes', 'Price'),
        ('Summer dress, navy check', '4-16', '$58.00'),
        ('Polo shirt, gold with crest', '4-16', '$32.00'),
        ('Shorts, navy', '4-16', '$29.00'),
        ('Winter pinafore', '4-16', '$74.00'),
        ('Jumper, navy wool blend', '4-16', '$68.00'),
        ('Bucket hat', 'S-L', '$18.00'),
        ('Library bag', 'One size', '$14.00'),
    ], [560, 240, 200])
    pdf.heading('Senior School (7-12)')
    pdf.table([
        ('Item', 'Sizes', 'Price'),
        ('Blazer, navy with gold piping', '8-XXL', '$189.00'),
        ('Shirt, white, long sleeve', '8-XXL', '$39.00'),
        ('Skirt or trousers, navy', '6-24', '$64.00'),
        ('College tie', 'One size', '$24.00'),
        ('Sport polo, house colour', 'XS-XXL', '$36.00'),
        ('Tracksuit jacket', 'XS-XXL', '$82.00'),
        ('Backpack with crest', 'One size', '$75.00'),
    ], [560, 240, 200])
    pdf.para('Second-hand uniforms in good condition are sold by the Parents and Friends Association on the '
             'first Friday of each month.')
    pdf.save(path)


def term_dates_pdf(path):
    pdf = PdfWriter('Term Dates')
    pdf.para('Dates are for the current school year. Staff development days are pupil-free.')
    pdf.table([
        ('Term', 'Students start', 'Students finish'),
        ('Term 1', 'Wednesday, week 1', 'Thursday, week 11'),
        ('Term 2', 'Tuesday, week 1', 'Friday, week 10'),
        ('Term 3', 'Tuesday, week 1', 'Friday, week 10'),
        ('Term 4', 'Tuesday, week 1', 'Wednesday, week 9'),
    ], [300, 360, 360])
    pdf.heading('Pupil-free days')
    pdf.para('The first Monday of each term is a staff development day. Before and after school care runs '
             'as normal on these days for Junior School families who have booked.')
    pdf.heading('Key dates')
    pdf.para('Open Mornings are held in Terms 1 and 3. Parent-teacher interviews run in weeks 8 and 9 of '
             'Terms 1 and 3. The Year 12 Valedictory Assembly is held in Term 4.')
    pdf.save(path)


def enrolment_pdf(path):
    pdf = PdfWriter('Enrolment Information Pack')
    pdf.heading('Welcome')
    pdf.para('Thank you for your interest in Kestrel Ridge College. This pack explains how to apply for a '
             'place, what happens after you apply, and what our fees cover.')
    pdf.heading('How to apply')
    for i, step in enumerate([
        'Submit an enrolment enquiry online or call the Registrar.',
        'Attend an Open Morning or book a personal tour.',
        'Complete the application form and pay the $150 application fee.',
        'Your child is invited to a friendly interview with the Head of School.',
        'Offers are made in writing. Accept by paying the enrolment deposit.',
    ], 1):
        pdf.para('{}. {}'.format(i, step))
    pdf.heading('Tuition fees (fictional)')
    pdf.table([
        ('Year level', 'Annual tuition', 'Per term'),
        ('Kindergarten - Year 2', '$11,480', '$2,870'),
        ('Year 3 - Year 6', '$13,960', '$3,490'),
        ('Year 7 - Year 10', '$19,720', '$4,930'),
        ('Year 11 - Year 12', '$22,160', '$5,540'),
    ], [420, 320, 280])
    pdf.para('A sibling discount of 10% applies to the second child and 20% to the third and subsequent '
             'children enrolled at the same time.')
    pdf.heading('Scholarships')
    pdf.para('Academic, music and all-rounder scholarships are offered for entry to Years 7 and 10. '
             'Means-tested bursaries are available at every year level.')
    pdf.save(path)


def main():
    os.makedirs(IMAGES, exist_ok=True)
    os.makedirs(DOCUMENTS, exist_ok=True)

    makers = {
        'campus': banner_campus, 'grounds': banner_grounds, 'library': banner_library,
        'pattern': banner_pattern, 'sport': banner_sport, 'stage': banner_stage,
    }
    for key, filename, _title in seed_data.BANNERS:
        makers[key](1920, 1080, os.path.join(IMAGES, filename))

    for _name, slug, colour, filename in seed_data.CATEGORIES:
        category_image(slug, colour, 1200, 800, os.path.join(IMAGES, filename))

    for i, member in enumerate(seed_data.STAFF):
        initials = member['first_name'][0] + member['last_name'][0]
        colour = seed_data.AVATAR_COLOURS[i % len(seed_data.AVATAR_COLOURS)]
        avatar(initials, colour, os.path.join(IMAGES, seed_data.staff_photo_filename(member)))

    uniform_pdf(os.path.join(DOCUMENTS, 'uniform-price-list.pdf'))
    term_dates_pdf(os.path.join(DOCUMENTS, 'term-dates.pdf'))
    enrolment_pdf(os.path.join(DOCUMENTS, 'enrolment-information-pack.pdf'))


if __name__ == '__main__':
    main()
