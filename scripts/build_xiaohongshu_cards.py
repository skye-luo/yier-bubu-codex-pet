#!/usr/bin/env python3
"""Build Xiaohongshu cards from the exact packaged pet sprites."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1080
HEIGHT = 1440
CELL = (192, 208)
ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "social" / "xiaohongshu"
FONT_PATHS = (
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
)


def font(size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    for path in FONT_PATHS:
        if path.exists():
            return ImageFont.truetype(str(path), size=size, index=index)
    return ImageFont.load_default(size=size)


F_TITLE = font(82)
F_SUBTITLE = font(39)
F_HEADING = font(51)
F_BODY = font(34)
F_SMALL = font(27)
F_LABEL = font(31)
F_CODE = font(25)


def gradient(top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    canvas = Image.new("RGB", (WIDTH, HEIGHT), top)
    pixels = canvas.load()
    for y in range(HEIGHT):
        ratio = y / (HEIGHT - 1)
        color = tuple(round(a + (b - a) * ratio) for a, b in zip(top, bottom))
        for x in range(WIDTH):
            pixels[x, y] = color
    return canvas.convert("RGBA")


def sprite(pet_id: str, sleeping: bool = False) -> Image.Image:
    filename = "spritesheet-night.webp" if sleeping else "spritesheet.webp"
    atlas = Image.open(ROOT / "pets" / pet_id / filename).convert("RGBA")
    return atlas.crop((0, 0, CELL[0], CELL[1]))


def fit_sprite(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
    box = image.getbbox()
    if box:
        image = image.crop(box)
    ratio = min(max_width / image.width, max_height / image.height)
    return image.resize(
        (round(image.width * ratio), round(image.height * ratio)),
        Image.Resampling.LANCZOS,
    )


def text_center(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, fnt, fill):
    box = draw.textbbox((0, 0), value, font=fnt)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1]), value, font=fnt, fill=fill)


def badge(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, fill, text_fill):
    x, y = xy
    box = draw.textbbox((0, 0), value, font=F_SMALL)
    w = box[2] - box[0] + 46
    h = 58
    draw.rounded_rectangle((x, y, x + w, y + h), radius=29, fill=fill)
    draw.text((x + 23, y + 11), value, font=F_SMALL, fill=text_fill)
    return w


def footer(draw: ImageDraw.ImageDraw, dark: bool = False):
    color = (255, 255, 255, 160) if dark else (82, 71, 70, 155)
    text_center(draw, (WIDTH // 2, 1372), "非官方 · 非商业粉丝体验版", F_SMALL, color)


def build_cover() -> None:
    canvas = gradient((255, 247, 241), (246, 224, 221))
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((760, -90, 1140, 290), fill=(255, 214, 196, 110))
    draw.ellipse((-140, 1010, 360, 1510), fill=(238, 202, 212, 105))
    badge(draw, (72, 72), "Codex Desktop 宠物", (255, 255, 255, 215), (93, 68, 64, 255))
    draw.text((72, 190), "我把一二和布布", font=F_TITLE, fill=(72, 53, 51, 255))
    draw.text((72, 302), "搬进 Codex 啦！", font=F_TITLE, fill=(72, 53, 51, 255))
    draw.text((76, 432), "会工作，也会按时睡觉", font=F_SUBTITLE, fill=(135, 94, 88, 255))

    draw.rounded_rectangle((80, 590, 1000, 1245), radius=76, fill=(255, 255, 255, 205))
    yier = fit_sprite(sprite("yier"), 390, 430)
    bubu = fit_sprite(sprite("bubu"), 390, 430)
    canvas.alpha_composite(yier, (265 - yier.width // 2, 730))
    canvas.alpha_composite(bubu, (785 - bubu.width // 2, 730))
    text_center(draw, (265, 1180), "一二", F_LABEL, (77, 58, 55, 255))
    text_center(draw, (785, 1180), "布布", F_LABEL, (77, 58, 55, 255))
    badge(draw, (348, 1257), "GitHub 已开源", (87, 71, 68, 230), (255, 255, 255, 255))
    footer(draw)
    canvas.convert("RGB").save(OUTPUT / "01-cover.png", quality=95)


def build_sleep() -> None:
    canvas = gradient((242, 244, 255), (221, 225, 248))
    draw = ImageDraw.Draw(canvas)
    badge(draw, (72, 72), "自动日夜待机", (255, 255, 255, 215), (59, 65, 102, 255))
    draw.text((72, 180), "一个角色", font=F_TITLE, fill=(44, 49, 77, 255))
    draw.text((72, 292), "两种待机状态", font=F_TITLE, fill=(44, 49, 77, 255))

    panels = [
        ((65, 480, 1015, 820), "白天 / 有空时", False, (255, 255, 255, 215)),
        ((65, 855, 1015, 1215), "22:00–08:00", True, (44, 48, 76, 225)),
    ]
    for rect, label, sleeping, fill in panels:
        draw.rounded_rectangle(rect, radius=54, fill=fill)
        label_color = (70, 68, 78, 255) if not sleeping else (235, 239, 255, 255)
        draw.text((105, rect[1] + 38), label, font=F_HEADING, fill=label_color)
        for pet_id, center_x in (("yier", 600), ("bubu", 830)):
            pet = fit_sprite(sprite(pet_id, sleeping), 210, 210)
            canvas.alpha_composite(pet, (center_x - pet.width // 2, rect[1] + 95))

    draw.text((80, 1263), "只替换待机行 · 工作动画保持原样", font=F_BODY, fill=(67, 73, 111, 255))
    footer(draw)
    canvas.convert("RGB").save(OUTPUT / "02-day-night.png", quality=95)


def build_install() -> None:
    canvas = gradient((246, 242, 236), (234, 225, 213))
    draw = ImageDraw.Draw(canvas)
    badge(draw, (72, 72), "macOS 安装", (255, 255, 255, 220), (81, 66, 57, 255))
    draw.text((72, 184), "复制这一条", font=F_TITLE, fill=(65, 52, 46, 255))
    draw.text((72, 296), "就能养进 Codex", font=F_TITLE, fill=(65, 52, 46, 255))
    draw.rounded_rectangle((65, 475, 1015, 1035), radius=45, fill=(44, 40, 40, 245))
    badge(draw, (100, 535), "一条命令", (229, 177, 159, 255), (51, 42, 39, 255))
    command_lines = [
        "curl -fsSL https://raw.githubusercontent.com/",
        "skye-luo/yier-bubu-codex-pet/v1.0.1/",
        "quick-install.sh | bash",
    ]
    for index, command in enumerate(command_lines):
        draw.text((100, 665 + index * 72), command, font=F_CODE, fill=(245, 241, 237, 255))
    draw.text((100, 915), "同一条命令 · 终端整行复制", font=F_SMALL, fill=(205, 190, 185, 255))
    draw.rounded_rectangle((65, 1085, 1015, 1290), radius=42, fill=(255, 255, 255, 205))
    draw.text((110, 1128), "自动安装 + 自动睡眠", font=F_HEADING, fill=(73, 59, 53, 255))
    draw.text((110, 1206), "重启 Codex → Pets → 选择角色", font=F_BODY, fill=(116, 89, 79, 255))
    footer(draw)
    canvas.convert("RGB").save(OUTPUT / "03-install.png", quality=95)


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    build_cover()
    build_sleep()
    build_install()
    print(f"已生成 3 张小红书图片：{OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
