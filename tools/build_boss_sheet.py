"""Build the normalized 6x2 Cursed Vulture sheet (FLY/ATTACK + IDLE_FLOAT)."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "boss_idle_chromakey.png"
OUT = ROOT / "assets" / "enemies" / "boss.png"
COLS, ROWS, FW, FH = 6, 2, 160, 112


def main():
    src = Image.open(SRC).convert("RGBA")
    px = src.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, _ = px[x, y]
            if r > 155 and b > 125 and g < 130 and r + b - 2 * g > 130:
                px[x, y] = (r, g, b, 0)
    raw = []
    for row in range(ROWS):
        for col in range(COLS):
            box = (round(col * src.width / COLS), round(row * src.height / ROWS),
                   round((col + 1) * src.width / COLS), round((row + 1) * src.height / ROWS))
            cell = src.crop(box)
            bounds = cell.getchannel("A").getbbox()
            raw.append(cell.crop(bounds) if bounds else cell)
    # One common scale and one fixed frame canvas eliminate perceived size jumps.
    scale = min((FW - 6) / max(c.width for c in raw), (FH - 6) / max(c.height for c in raw))
    out = Image.new("RGBA", (FW * COLS, FH * ROWS))
    for i, cell in enumerate(raw):
        cell = cell.resize((round(cell.width * scale), round(cell.height * scale)), Image.Resampling.NEAREST)
        frame = Image.new("RGBA", (FW, FH))
        frame.alpha_composite(cell, ((FW - cell.width) // 2, (FH - cell.height) // 2))
        out.alpha_composite(frame, ((i % COLS) * FW, (i // COLS) * FH))
    out.save(OUT, optimize=True)
    print(f"Wrote {OUT} {out.size} RGBA")


if __name__ == "__main__":
    main()
