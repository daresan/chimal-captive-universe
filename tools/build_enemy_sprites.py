"""Turn the generated enemy concept atlas into five transparent runtime sheets."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "enemies_chromakey.png"
OUT = ROOT / "assets" / "enemies"
SPECS = [
    ("snake", 6, 96, 64), ("bat", 6, 96, 64),
    ("cougar", 5, 128, 64), ("priest", 5, 96, 96),
    ("boss", 5, 160, 112),
]


def remove_key(im):
    im = im.convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, _ = px[x, y]
            if r > 155 and b > 125 and g < 130 and r + b - 2 * g > 130:
                px[x, y] = (r, g, b, 0)
    return im


def fit(cell, w, h, scale):
    box = cell.getchannel("A").getbbox()
    if not box:
        return Image.new("RGBA", (w, h))
    cell = cell.crop(box)
    cell = cell.resize((round(cell.width * scale), round(cell.height * scale)), Image.Resampling.NEAREST)
    out = Image.new("RGBA", (w, h))
    out.alpha_composite(cell, ((w - cell.width) // 2, h - cell.height - 2))
    return out


def frame_spans(strip, expected):
    """Find visual frame groups; Imagegen spacing is intentionally not assumed."""
    alpha = strip.getchannel("A")
    active = [sum(alpha.getpixel((x, y)) > 0 for y in range(strip.height)) >= 3
              for x in range(strip.width)]
    runs, start = [], None
    for x, on in enumerate(active + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            runs.append([start, x])
            start = None
    # Motion accents can be disconnected. Merge the closest neighbours until
    # exactly the expected number of animation groups remains.
    while len(runs) > expected:
        i = min(range(len(runs) - 1), key=lambda n: runs[n + 1][0] - runs[n][1])
        runs[i:i + 2] = [[runs[i][0], runs[i + 1][1]]]
    return [(max(0, a - 4), min(strip.width, b + 4)) for a, b in runs]


def main():
    src = remove_key(Image.open(SRC))
    OUT.mkdir(parents=True, exist_ok=True)
    for row, (name, count, fw, fh) in enumerate(SPECS):
        if name == "boss":
            # Boss has a dedicated 6x2 FLY/ATTACK + IDLE_FLOAT source/build.
            continue
        y0, y1 = round(row * src.height / 5), round((row + 1) * src.height / 5)
        strip = src.crop((0, y0, src.width, y1))
        spans = frame_spans(strip, count)
        raw = []
        for x0, x1 in spans:
            cell = strip.crop((x0, 0, x1, strip.height))
            box = cell.getchannel("A").getbbox()
            raw.append(cell.crop(box) if box else cell)
        common_scale = min((fw - 4) / max(c.width for c in raw), (fh - 4) / max(c.height for c in raw))
        frames = [fit(cell, fw, fh, common_scale) for cell in raw]
        if not frames:
            frames = [Image.new("RGBA", (fw, fh))]
        while len(frames) < 6:
            frames.append(frames[-1].copy())
        sheet = Image.new("RGBA", (fw * 6, fh))
        for col, frame in enumerate(frames):
            sheet.alpha_composite(frame, (col * fw, 0))
        path = OUT / f"{name}.png"
        sheet.save(path, optimize=True)
        print(f"{name}: {sheet.size} -> {path}")


if __name__ == "__main__":
    main()
