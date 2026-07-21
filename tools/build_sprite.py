"""Build the exact 6x14, 48x64 runtime sheet from the generated concept sheet."""
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "maya_boy_chromakey.png"
OUTPUT = ROOT / "assets" / "mempalace_boy_spritesheet.png"

ROWS, SOURCE_ROWS, SOURCE_COLS = 14, 13, 5
SOURCE_X0, SOURCE_STEP = 24, 137
ROW_MAP = [0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12]
CELL_W, CELL_H = 48, 64


def bbox_for_cell(source: Image.Image, col: int, row: int):
    w, h = source.size
    # Imagegen placed five poses on a regular 137 px cadence and left a wide
    # right margin, so using the full canvas width as a grid would split poses.
    x0, x1 = SOURCE_X0 + col * SOURCE_STEP, SOURCE_X0 + (col + 1) * SOURCE_STEP
    row = ROW_MAP[row]
    y0, y1 = round(row * h / SOURCE_ROWS), round((row + 1) * h / SOURCE_ROWS)
    cell = source.crop((x0, y0, x1, y1)).convert("RGBA")
    px = cell.load()
    for y in range(cell.height):
        for x in range(cell.width):
            r, g, b, _ = px[x, y]
            # Remove the generated magenta key with a compact, pixel-friendly matte.
            # The source key is hot magenta (high red + blue, low green).
            # Accept its small compression/antialiasing variance as well.
            if r > 135 and b > 105 and g < 155 and (r + b - 2 * g) > 95:
                px[x, y] = (r, g, b, 0)
    alpha = cell.getchannel("A")
    # Ignore isolated compression specks when determining the content bounds.
    cols = [sum(1 for y in range(cell.height) if alpha.getpixel((x, y)) > 0)
            for x in range(cell.width)]
    rows = [sum(1 for x in range(cell.width) if alpha.getpixel((x, y)) > 0)
            for y in range(cell.height)]
    xs = [x for x, count in enumerate(cols) if count >= 4]
    ys = [y for y, count in enumerate(rows) if count >= 4]
    box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1) if xs and ys else alpha.getbbox()
    return cell.crop(box) if box else cell


def fit(cell: Image.Image) -> Image.Image:
    target = Image.new("RGBA", (CELL_W, CELL_H))
    max_w, max_h = 46, 62
    scale = min(max_w / cell.width, max_h / cell.height)
    size = (max(1, round(cell.width * scale)), max(1, round(cell.height * scale)))
    cell = cell.resize(size, Image.Resampling.NEAREST)
    target.alpha_composite(cell, ((CELL_W - size[0]) // 2, CELL_H - size[1]))
    return target


def main():
    source = Image.open(SOURCE)
    out = Image.new("RGBA", (CELL_W * 6, CELL_H * ROWS))
    for row in range(ROWS):
        frames = [fit(bbox_for_cell(source, col, row)) for col in range(SOURCE_COLS)]
        frames.append(frames[0].copy() if row in (0, 6, 7, 12) else frames[-1].copy())
        for col, frame in enumerate(frames):
            out.alpha_composite(frame, (col * CELL_W, row * CELL_H))
    OUTPUT.parent.mkdir(exist_ok=True)
    out.save(OUTPUT, optimize=True)
    assert out.size == (288, 896)
    assert out.mode == "RGBA" and out.getpixel((0, 0))[3] == 0
    print(f"Wrote {OUTPUT} ({out.width}x{out.height}, RGBA)")


if __name__ == "__main__":
    main()
