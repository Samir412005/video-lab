import os
import subprocess
from PIL import Image, ImageDraw, ImageFont, features

# Arabic shaping (joined letters) needs libraqm in Pillow; fail loudly
# instead of producing disconnected letters.
assert features.check("raqm"), "Pillow was built without libraqm; Arabic shaping unavailable"

# Find an Arabic font (prefer Noto Kufi Arabic Bold).
fonts = subprocess.run(
    ["fc-list", ":lang=ar", "file"], capture_output=True, text=True
).stdout.splitlines()
fonts = [line.split(":")[0] for line in fonts if line.strip()]

def pick(*names):
    for name in names:
        for font in fonts:
            if name.lower() in font.lower():
                return font
    return fonts[0] if fonts else None

font_path = pick("NotoKufiArabic-Bold", "NotoKufiArabic",
                 "NotoNaskhArabic-Bold", "NotoSansArabic-Bold")
assert font_path, "No Arabic font found (fc-list :lang=ar empty)"
print("Arabic font:", font_path)

os.makedirs("scripts/titles", exist_ok=True)
titles = [
    ("title1.png", "الوقت يمضي", 110, (255, 215, 0)),
    ("title2.png", "نبني في كل لحظة", 100, (255, 215, 0)),
    ("title3.png", "نتعلم، ننمو، نترك أثرًا", 88, (255, 255, 255)),
    ("title4.png", "الوقت لا يعود... فاجعله يستحق", 78, (255, 215, 0)),
]
for name, text, size, color in titles:
    font = ImageFont.truetype(font_path, size)
    img = Image.new("RGBA", (1400, 260), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font, direction="rtl", language="ar")
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((1400 - w) / 2 - bbox[0], (260 - h) / 2 - bbox[1]),
              text, font=font, fill=color + (255,), direction="rtl", language="ar")
    img.save(f"scripts/titles/{name}")
    print("wrote", name)
