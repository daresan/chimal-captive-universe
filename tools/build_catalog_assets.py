"""Build the revised Cougar sheet and expandable scenery catalog."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def remove_key(im):
    im = im.convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, _ = px[x, y]
            # The generated key contains antialiased dark-purple edge pixels too.
            # Maya turquoise and warm character colours remain outside this hue range.
            is_magenta = r > 55 and b > 55 and g < min(r, b) * 0.72 and abs(r - b) < 145
            if is_magenta:
                px[x, y] = (r, g, b, 0)
    return im


def fitted(cell, width, height, common_scale=None):
    box = cell.getchannel("A").getbbox()
    cell = cell.crop(box) if box else cell
    scale = common_scale or min((width - 4) / cell.width, (height - 4) / cell.height)
    cell = cell.resize((max(1, round(cell.width * scale)), max(1, round(cell.height * scale))), Image.Resampling.NEAREST)
    out = Image.new("RGBA", (width, height))
    out.alpha_composite(cell, ((width - cell.width) // 2, height - cell.height - 2))
    return out


def build_cougar():
    src = remove_key(Image.open(ASSETS / "cougar_run_chromakey.png"))
    raw = []
    for col in range(6):
        x0, x1 = round(col * src.width / 6), round((col + 1) * src.width / 6)
        cell = src.crop((x0, 0, x1, src.height))
        box = cell.getchannel("A").getbbox()
        raw.append(cell.crop(box) if box else cell)
    scale = min(124 / max(c.width for c in raw), 60 / max(c.height for c in raw))
    out = Image.new("RGBA", (128 * 6, 64))
    for i, cell in enumerate(raw):
        out.alpha_composite(fitted(cell, 128, 64, scale), (i * 128, 0))
    out.save(ASSETS / "enemies" / "cougar.png", optimize=True)


def build_scenery():
    names = ["village_hut", "village_totem", "ceiba_tree", "village_terrace",
             "jungle_cluster", "vine_arch", "mountain_peak", "rock_outcrop",
             "temple_facade", "temple_column", "crystal_cluster", "dungeon_arch"]
    src = remove_key(Image.open(ASSETS / "scenery_catalog_chromakey.png"))
    out_dir = ASSETS / "scenery"
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(names):
        row, col = divmod(i, 4)
        box = (round(col * src.width / 4), round(row * src.height / 3),
               round((col + 1) * src.width / 4), round((row + 1) * src.height / 3))
        fitted(src.crop(box), 320, 240).save(out_dir / f"{name}.png", optimize=True)
    print(f"Built {len(names)} scenery catalog sprites")


if __name__ == "__main__":
    build_cougar()
    build_scenery()
