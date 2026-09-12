#!/usr/bin/env python3
"""Emit the review artifact and the real site from one template.

    python3 build_site.py            # writes site-draft.html (artifact) and site-out/ (the repo files)
"""
import base64, math, os, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
TMPL = open(os.path.join(HERE, "site.tmpl.html"), encoding="utf-8").read()
STORE = "https://apps.apple.com/gb/app/sealed/id6807351225"
APPLE = ("M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 "
         "1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 "
         "3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559"
         "-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052"
         "-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701")
IMAGES = {"wrist": "shots/04-wrist-wide.jpg", "base": "shots/06-base-phone.jpg", "progress": "shots/08-progress-phone.jpg", "pact": "shots/07-pact-phone.jpg"}
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;800&family=JetBrains+Mono:wght@400;600&display=swap">'
FAVICON = ("data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Ccircle cx='32' cy='32' r='30' fill='%230c0d0f'/%3E%3Ccircle cx='32' cy='32' r='22' fill='%237a2430' stroke='%23e0b64a' stroke-width='3'/%3E"
           "%3Ctext x='32' y='42' text-anchor='middle' font-family='Georgia,serif' font-weight='900' font-size='30' fill='%23e0b64a'%3ES%3C/text%3E%3C/svg%3E")

DESCRIPTION = "Sealed is the workout habit tracker with one honest ritual: press a wax seal on your day, and the impression only forms as complete as you earned. Train, fuel and base. iPhone and Apple Watch."

SITE_HEAD = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sealed — Workout habit tracker. Earn the close.</title>
<meta name="description" content="{DESCRIPTION}">
<link rel="canonical" href="https://sealedapp.co.uk/">
<meta name="theme-color" content="#0c0d0f">
<meta name="apple-itunes-app" content="app-id=6807351225">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sealed">
<meta property="og:title" content="Sealed — Earn the close">
<meta property="og:description" content="One wax seal a night. The impression only forms as complete as you earned. Workout habit tracker for iPhone and Apple Watch.">
<meta property="og:url" content="https://sealedapp.co.uk/">
<meta property="og:image" content="https://sealedapp.co.uk/assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Sealed — Earn the close">
<meta name="twitter:description" content="One wax seal a night. The impression only forms as complete as you earned.">
<meta name="twitter:image" content="https://sealedapp.co.uk/assets/og.jpg">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{FONTS}
</head>
<body>'''
SITE_FOOT = "\n</body>\n</html>\n"

def fill(head, img):
    s = TMPL.replace("{{HEAD}}", head).replace("{{STORE}}", STORE).replace("{{APPLE}}", APPLE)
    for name, path in IMAGES.items():
        s = s.replace("{{IMG:%s}}" % name, img(name, path))
    assert "{{" not in s, "unfilled placeholder"
    return s

# 1. The artifact: fonts link + title, images inline.
def data_uri(name, path):
    return "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(HERE, path), "rb").read()).decode()
open(os.path.join(HERE, "site-draft.html"), "w", encoding="utf-8").write(fill("<title>Earn the Close</title>\n" + FONTS, data_uri))

# 2. The site: full head, images as files under assets/.
out = os.path.join(HERE, "site-out"); shutil.rmtree(out, ignore_errors=True); os.makedirs(os.path.join(out, "assets"))
for name, path in IMAGES.items():
    shutil.copy(os.path.join(HERE, path), os.path.join(out, "assets", name + ".jpg"))
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(fill(SITE_HEAD, lambda n, p: "/assets/%s.jpg" % n) + SITE_FOOT)

# 3. The share image: the seal on the dark field, the name beside it.
W, H = 1200, 630
im = Image.new("RGB", (W, H), (12, 13, 15))
d = ImageDraw.Draw(im)
# a warm glow behind the wax
glow = Image.new("RGB", (W, H), (12, 13, 15)); gd = ImageDraw.Draw(glow)
cx, cy = 880, 315
for r in range(300, 0, -4):
    a = (1 - r / 300) ** 2
    gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(int(12 + 60 * a), int(13 + 14 * a), int(15 + 18 * a)))
im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(30)), 0.9); d = ImageDraw.Draw(im)
# the arcs
ring, gap = 232, 9
for i in range(3):
    a0 = -90 + gap / 2 + i * 120; a1 = a0 + 120 - gap
    d.arc((cx - ring, cy - ring, cx + ring, cy + ring), a0, a1, fill=(28, 30, 35), width=22)
    d.arc((cx - ring, cy - ring, cx + ring, cy + ring), a0, a0 + (120 - gap) * [1, 1, .92][i], fill=(142, 42, 51), width=22)
# the wax, sealed: deep red, gold surround, gold crest
R = 150
for r in range(R, 0, -1):
    t = r / R
    col = (int(122 - 60 * t), int(36 - 20 * t), int(48 - 26 * t))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
d.ellipse((cx - R - 8, cy - R - 8, cx + R + 8, cy + R + 8), outline=(224, 182, 74), width=9)
georgia = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 190)
d.text((cx + 4, cy + 10), "S", font=georgia, fill=(0, 0, 0), anchor="mm")
d.text((cx, cy + 2), "S", font=georgia, fill=(224, 182, 74), anchor="mm")
# the words
archivo = ImageFont.truetype(os.path.join(HERE, "archivo-800.ttf"), 150)
small = ImageFont.truetype(os.path.join(HERE, "archivo-800.ttf"), 44)
mono = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", 22) if os.path.exists("/System/Library/Fonts/Supplemental/Courier New Bold.ttf") else small
d.text((80, 190), "SEALED", font=archivo, fill=(232, 233, 235), anchor="ls")
d.text((84, 262), "EARN THE CLOSE.", font=small, fill=(200, 240, 74), anchor="ls")
d.text((86, 330), "One wax seal a night. The impression", font=mono, fill=(139, 143, 152), anchor="ls")
d.text((86, 364), "only forms as complete as you earned.", font=mono, fill=(139, 143, 152), anchor="ls")
d.text((86, 440), "WORKOUT HABIT TRACKER  ·  IPHONE + APPLE WATCH", font=mono, fill=(139, 143, 152), anchor="ls")
im.save(os.path.join(out, "assets", "og.jpg"), quality=88)
print("artifact:", os.path.getsize(os.path.join(HERE, "site-draft.html")) // 1024, "KB; site:", sorted(os.listdir(os.path.join(out, "assets"))))
