"""Generate the Proddyt Studio app icons (icons/<bin>.ico + .png) and the suite mark (icons/studio.ico).

Usage: python gen-icons.py <IBMPlexMono-Bold.ttf>   (writes into ../icons, idempotent)
Spec: ORGANIZATIONS/PRODDYT/MARCA.md in the Second Brain — pastel fill, 2-letter code in IBM Plex Mono Bold #17161A.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

APPS = {
    "printcraft": ("Pr", "#FF9A85"), "photocraft": ("Ph", "#8EC5FF"), "vectorcraft": ("Vc", "#FFCB66"),
    "lightcraft": ("Lt", "#B5E3FF"), "filmcraft": ("Fm", "#C9B2FF"), "effectcraft": ("Fx", "#E2B0FF"),
    "designcraft": ("Ds", "#FFB3D4"), "soundcraft": ("Sd", "#9BEEDC"), "wordcraft": ("Wd", "#A9C2FF"),
    "gridcraft": ("Gd", "#A6EBC0"), "deckcraft": ("Dk", "#FFBD94"), "cadcraft": ("Cd", "#E9F08A"),
}
SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
N = 1024  # draw big, downsample


def tile(fill):
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, N - 1, N - 1), radius=int(N * 20 / 84), fill=fill)
    return img


def app_icon(code, fill, font_path):
    img = tile(fill)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, int(N * 0.42))
    d.text((N / 2, N / 2), code, font=font, fill="#17161A", anchor="mm")
    return img


def studio_mark():
    img = tile("#E8462A")
    d = ImageDraw.Draw(img)
    k = N / 64
    w = int(5 * k)
    for x1, y1, x2, y2 in ((13, 46, 23, 18), (41, 46, 51, 18)):
        d.line((x1 * k, y1 * k, x2 * k, y2 * k), fill="#FFFFFF", width=w)
        for x, y in ((x1, y1), (x2, y2)):
            d.ellipse((x * k - w / 2, y * k - w / 2, x * k + w / 2, y * k + w / 2), fill="#FFFFFF")
    r = 3.6 * k
    d.ellipse((32 * k - r, 32 * k - r, 32 * k + r, 32 * k + r), fill="#FFFFFF")
    return img


def save(img, out, name):
    img.resize((256, 256), Image.LANCZOS).save(os.path.join(out, name + ".png"))
    img.save(os.path.join(out, name + ".ico"), sizes=SIZES)


font_path = sys.argv[1]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "icons")
os.makedirs(out, exist_ok=True)
for bin_name, (code, fill) in APPS.items():
    save(app_icon(code, fill, font_path), out, bin_name)
save(studio_mark(), out, "studio")
print("ok", len(APPS) + 1, "icons in", os.path.normpath(out))
