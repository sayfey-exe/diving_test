import math
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "static/img/pascal.png")
OUT = os.path.join(ROOT, "static/img/") 
S = 240  # taille du GIF (carré)

# Crop carré centré sur le mérou, puis resize
full = Image.open(SRC).convert("RGB")
W, H = full.size
side = min(W, H)
left = (W - side) // 2
base = full.crop((left, 0, left + side, side)).resize((S, S), Image.LANCZOS)
BG_FILL = base.getpixel((4, 4))  # bleu du haut pour combler les rotations


def transform(angle=0.0, scale=1.0, dy=0):
    """Retourne une frame S×S : zoom (>=1), rotation, décalage vertical."""
    sc = max(scale, 1.0)
    big = base.resize((int(S * sc * 1.12), int(S * sc * 1.12)), Image.LANCZOS)
    if angle:
        big = big.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=BG_FILL)
    bw, bh = big.size
    cx, cy = bw // 2, bh // 2 + dy
    box = (cx - S // 2, cy - S // 2, cx + S // 2, cy + S // 2)
    return big.crop(box).convert("RGBA")


def lightbulb(d, cx, cy, r, a=255):
    # rayons
    for ang in range(0, 360, 45):
        x1 = cx + math.cos(math.radians(ang)) * r * 1.25
        y1 = cy + math.sin(math.radians(ang)) * r * 1.25
        x2 = cx + math.cos(math.radians(ang)) * r * 1.7
        y2 = cy + math.sin(math.radians(ang)) * r * 1.7
        d.line((x1, y1, x2, y2), fill=(255, 214, 64, a), width=max(2, r // 6))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 224, 92, a))
    d.ellipse((cx - r*0.45, cy - r*0.55, cx + r*0.1, cy), fill=(255, 248, 200, a))
    d.rectangle((cx - r*0.45, cy + r*0.7, cx + r*0.45, cy + r*1.25), fill=(120, 120, 120, a))


def sparkle(d, cx, cy, r, col=(255, 255, 255, 255)):
    pts = [(cx, cy-r), (cx+r*0.22, cy-r*0.22), (cx+r, cy), (cx+r*0.22, cy+r*0.22),
           (cx, cy+r), (cx-r*0.22, cy+r*0.22), (cx-r, cy), (cx-r*0.22, cy-r*0.22)]
    d.polygon(pts, fill=col)


def teardrop(d, cx, cy, s, a=235):
    d.polygon([(cx, cy - s*1.4), (cx - s*0.8, cy), (cx + s*0.8, cy)], fill=(90, 190, 255, a))
    d.ellipse((cx - s*0.8, cy - s*0.4, cx + s*0.8, cy + s), fill=(90, 190, 255, a))
    d.ellipse((cx - s*0.4, cy - s*0.1, cx - s*0.05, cy + s*0.35), fill=(220, 245, 255, a))


def badge(frame, kind):
    # pastille coin haut-droit : check vert / croix rouge
    ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    r = S // 7
    cx, cy = S - r - 6, r + 6
    col = (31, 169, 113, 255) if kind == "ok" else (226, 59, 84, 255)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col, outline=(255, 255, 255, 255), width=4)
    if kind == "ok":
        d.line((cx - r*0.45, cy + r*0.05, cx - r*0.05, cy + r*0.45), fill="white", width=6)
        d.line((cx - r*0.05, cy + r*0.45, cx + r*0.5, cy - r*0.4), fill="white", width=6)
    else:
        d.line((cx - r*0.4, cy - r*0.4, cx + r*0.4, cy + r*0.4), fill="white", width=6)
        d.line((cx - r*0.4, cy + r*0.4, cx + r*0.4, cy - r*0.4), fill="white", width=6)
    return Image.alpha_composite(frame, ov)


def overlay(frame, drawer):
    ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    drawer(ImageDraw.Draw(ov))
    return Image.alpha_composite(frame, ov)


def save_gif(name, frames, dur):
    flat = [f.convert("RGB").quantize(colors=128, method=Image.MEDIANCUT) for f in frames]
    flat[0].save(OUT + name, save_all=True, append_images=flat[1:], loop=0,
                 duration=dur, disposal=2, optimize=True)
    print("écrit", name, len(frames), "frames")


# ---------- 1) CONSEIL : léger balancement + ampoule qui pulse ----------
N = 16
frames = []
for i in range(N):
    t = i / N
    ang = 4 * math.sin(2 * math.pi * t)            # balancement ±4°
    fr = transform(angle=ang, scale=1.03)
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * t)  # ampoule qui respire
    a = int(150 + 105 * pulse)
    r = int(S * (0.085 + 0.02 * pulse))
    fr = overlay(fr, lambda d, a=a, r=r: lightbulb(d, int(S*0.2), int(S*0.2), r, a))
    frames.append(fr)
save_gif("pascal-conseil.gif", frames, 80)


# ---------- 2) CONTENT : rebond + étincelles + éclat + badge ✓ ----------
N = 16
frames = []
base_bright = ImageEnhance.Color(ImageEnhance.Brightness(base).enhance(1.06)).enhance(1.18)
base = base_bright  # un peu plus vif
for i in range(N):
    t = i / N
    bounce = abs(math.sin(math.pi * t))            # rebond 0..1..0
    sc = 1.0 + 0.07 * bounce
    dy = int(-10 * bounce)
    fr = transform(scale=sc, dy=dy)
    def draw_sp(d, t=t):
        spots = [(0.18, 0.2, 0.05), (0.84, 0.28, 0.06), (0.8, 0.78, 0.045), (0.2, 0.8, 0.05)]
        for j, (px, py, pr) in enumerate(spots):
            ph = (t + j / len(spots)) % 1.0
            tw = abs(math.sin(math.pi * ph))
            if tw > 0.15:
                sparkle(d, int(S*px), int(S*py), int(S*pr*tw*1.6),
                        (255, 246, 150, int(255*tw)))
    fr = overlay(fr, draw_sp)
    fr = badge(fr, "ok")
    frames.append(fr)
save_gif("pascal-content.gif", frames, 70)
base = base_bright  # reset reference not needed further


# ---------- 3) PAS CONTENT : désaturé, secoue, larme + badge ✗ ----------
# repartir de l'image d'origine (non éclaircie)
full2 = Image.open(SRC).convert("RGB")
base = full2.crop((left, 0, left + side, side)).resize((S, S), Image.LANCZOS)
base = ImageEnhance.Brightness(ImageEnhance.Color(base).enhance(0.35)).enhance(0.82)
overlay_blue = Image.new("RGB", (S, S), (40, 70, 120))
base = Image.blend(base, overlay_blue, 0.18)
BG_FILL = base.getpixel((4, 4))
N = 16
frames = []
for i in range(N):
    t = i / N
    shake = 5 * math.sin(2 * math.pi * t * 2)      # tremblement
    droop = 4                                       # penché vers le bas
    fr = transform(angle=shake, scale=1.04, dy=droop)
    ty = int(S*0.5 + (t * S*0.32))                 # larme qui glisse
    fr = overlay(fr, lambda d, ty=ty: teardrop(d, int(S*0.34), ty, S*0.05))
    fr = badge(fr, "ko")
    frames.append(fr)
save_gif("pascal-pas-content.gif", frames, 70)

print("Terminé.")
