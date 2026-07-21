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


def largest_component_box(cell: Image.Image):
    alpha = cell.getchannel("A")
    visible = {(x, y) for y in range(cell.height) for x in range(cell.width)
               if alpha.getpixel((x, y)) > 0}
    best = None
    while visible:
        todo = [visible.pop()]
        component = []
        while todo:
            x, y = todo.pop()
            component.append((x, y))
            for n in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if n in visible:
                    visible.remove(n)
                    todo.append(n)
        if best is None or len(component) > len(best):
            best = component
    if not best:
        return (0, 0, cell.width, cell.height)
    xs, ys = zip(*best)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def fit(cell: Image.Image, row: int) -> Image.Image:
    target = Image.new("RGBA", (CELL_W, CELL_H))
    bx0, by0, bx1, by1 = largest_component_box(cell)
    body_w, body_h = bx1 - bx0, by1 - by0
    # Detached weapons, projectiles and power-up rays do not influence body size.
    scale = 45 / body_w if row == 13 else min(56 / body_h, 44 / body_w)
    size = (max(1, round(cell.width * scale)), max(1, round(cell.height * scale)))
    cell = cell.resize(size, Image.Resampling.NEAREST)
    body_cx = (bx0 + bx1) / 2 * scale
    body_bottom = by1 * scale
    target.alpha_composite(cell, (round(CELL_W / 2 - body_cx), round(CELL_H - 2 - body_bottom)))
    return target


def main():
    source = Image.open(SOURCE)
    out = Image.new("RGBA", (CELL_W * 6, CELL_H * ROWS))
    for row in range(ROWS):
        raw = [bbox_for_cell(source, col, row) for col in range(SOURCE_COLS)]
        # Some generated throw rows end with the projectile alone. A projectile
        # is not a valid character frame; hold the last complete pose instead.
        for col, cell in enumerate(raw):
            skin = sum(1 for r, g, b, a in cell.getdata()
                       if a and r > 110 and g > 40 and b < 100)
            if skin < 1000 and col:
                raw[col] = raw[col - 1].copy()
        frames = [fit(cell, row) for cell in raw]
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
