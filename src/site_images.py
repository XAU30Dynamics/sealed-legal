"""Site + press images from the raws, the frames and the sim shots in src/sim/ - then run build_site.py and copy site-out up."""
from pathlib import Path
from PIL import Image
S = Path.home() / "Desktop/Fitness_app/Sealed App Store screenshots"
RAW, FRAMES = S / "raw-1.3", S / "1.3/iphone-6.9"
SITE = Path.home() / "Desktop/Fitness_app/sealed-legal"
SHOTS, PRESS = SITE / "src/shots", SITE / "press/assets"
SCR = Path(__file__).parent / "sim"  # the sim shots: wall, readiness, and any raw iCloud left as a stub

def rgb(p):
    p = Path(p)
    alt = SCR / p.name  # four raws are iCloud stubs today; the sim re-captures sit beside this script
    try: return Image.open(p).convert("RGB")
    except Exception: return Image.open(alt).convert("RGB")
def save(im, p, q=88): p.parent.mkdir(parents=True, exist_ok=True); im.save(p, quality=q, optimize=True); print(p.relative_to(SITE), im.size)

# 1. Home-page phone shots: the screen below the status bar, 427x900.
for name, src in {"05-fuel": "fuel", "06-base": "base", "07-pact": "pact", "08-progress": "progress", "09-train": "train"}.items():
    im = rgb(RAW / f"{src}.png").crop((25, 190, 1295, 2868)).resize((427, 900), Image.LANCZOS)
    save(im, SHOTS / f"{name}-phone.jpg")
# TRAIN wide: from the cardio card down, 608x1000.
save(rgb(RAW / "train.png").crop((0, 640, 1320, 640 + 2171)).resize((608, 1000), Image.LANCZOS), SHOTS / "04-wrist-wide.jpg")

# 2. Press stills: the raws at 644x1400 (wall + readiness from today's sim).
stills = {"01-home-open": RAW / "home.png", "02-home-sealed": RAW / "sealed.png", "03-train": RAW / "train.png",
          "04-fuel": RAW / "fuel.png", "05-base": RAW / "base.png", "06-progress": RAW / "progress.png",
          "07-wall": SCR / "wall.png", "08-readiness": SCR / "readiness.png"}
for name, src in stills.items():
    save(rgb(src).resize((644, 1400), Image.LANCZOS), PRESS / f"still-{name}.jpg")
# 3. Press store frames: the nine 1.3 frames at 644x1400.
for f in sorted(FRAMES.glob("*.png")):
    save(rgb(f).resize((644, 1400), Image.LANCZOS), PRESS / f"store-{f.stem}.jpg")
