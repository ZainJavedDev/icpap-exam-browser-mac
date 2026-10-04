"""Regenerates every ICPAP-branded image from Branding/icpap-logo.png.

Run from the repository root: python3 Branding/make-branding.py
Needs Pillow and one of the font pairs listed in FONTS (Noto on Linux, Georgia/Segoe UI on Windows,
Georgia/Helvetica on macOS).
"""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
GREEN = (12, 115, 71, 255)
DARK = (40, 52, 46, 255)
FONTS = [
    ('/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf', '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'),
    ('C:/Windows/Fonts/georgiab.ttf', 'C:/Windows/Fonts/segoeui.ttf'),
    ('/System/Library/Fonts/Supplemental/Georgia Bold.ttf', '/System/Library/Fonts/Helvetica.ttc'),
]

seal = Image.open(ROOT / 'Branding/icpap-logo.png').convert('RGBA')
seal = seal.crop(seal.getchannel('A').getbbox())
serif, sans = next((s, n) for s, n in FONTS if Path(s).exists() and Path(n).exists())


def fit(height: int) -> Image.Image:
    return seal.resize((round(seal.width * height / seal.height), height), Image.LANCZOS)


# App icon: the seal on a white rounded square, in the proportions of Apple's macOS icon grid
# (824 of 1024 pixels with a 185 pixel corner radius).
icon = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
ImageDraw.Draw(icon).rounded_rectangle((100, 100, 923, 923), radius=185, fill=(255, 255, 255, 255))
mark = fit(680)
icon.alpha_composite(mark, ((1024 - mark.width) // 2, (1024 - mark.height) // 2))

iconset = ROOT / 'Safe Exam Browser/Images.xcassets/AppIcon.appiconset'
for entry in json.loads((iconset / 'Contents.json').read_text())['images']:
    points = int(entry['size'].split('x')[0])
    pixels = points * int(entry['scale'].rstrip('x'))
    icon.resize((pixels, pixels), Image.LANCZOS).save(iconset / entry['filename'])

# About window. SEB draws the version and copyright text over the lower right,
# so the name stays above y=120 and right of x=310 (in points).
for scale, suffix in [(1, ''), (2, '@2x')]:
    about = Image.new('RGBA', (550 * scale, 300 * scale), (255, 255, 255, 255))
    mark = fit(270 * scale)
    about.alpha_composite(mark, ((310 * scale - mark.width) // 2, 15 * scale))
    draw = ImageDraw.Draw(about)
    draw.text((318 * scale, 14 * scale), 'ICPAP', font=ImageFont.truetype(serif, 62 * scale), fill=GREEN)
    draw.text((320 * scale, 88 * scale), 'Exam Browser', font=ImageFont.truetype(sans, 27 * scale), fill=DARK)
    about.save(ROOT / f'Resources/Images/AboutSEB{suffix}.png')

print('Branding images written.')
