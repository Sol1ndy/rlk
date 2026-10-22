"""Shared RGBA materials for Narukami's native 26.3 item-display effects.

These are numeric color/opacity swatches, not copied game imagery. The 26.3
client BakedQuad.MaterialInfo.of routes partially transparent sprite quads to
Sheets.translucentItemSheet; no modded render_type or shader override is used.
The narrow opaque cores and separate transparent shells retain depth and
contrast without concrete-texture noise. Register every swatch in items atlas.
"""
from pathlib import Path
import argparse
import json
import struct
import zlib


PALETTE = {
    "void": (29, 13, 65, 191),
    "violet": (132, 63, 238, 89),
    "lavender": (212, 183, 255, 51),
    "white": (250, 244, 255, 255),
    "cyan": (161, 229, 255, 180),
    "shadow": (15, 9, 30, 210),
    "violet_dense": (153, 80, 250, 184),
    "glow": (181, 118, 255, 30),
    "afterglow": (144, 96, 230, 64),
    "pearl": (235, 213, 255, 224),
    # opaque armour / katana swatches of the 만겁 arm (build_raiden_judgment_rig.mjs)
    "arm_lilac": (201, 182, 236, 255),
    "arm_shade": (154, 130, 207, 255),
    "arm_deep": (75, 45, 122, 255),
    "arm_tomoe": (58, 37, 96, 255),
    "gold_dull": (184, 154, 94, 255),
    "blade_pale": (215, 198, 247, 255),
    "blade_edge": (245, 240, 255, 255),
    "blade_core": (156, 120, 224, 255),
    "grip_dark": (44, 30, 66, 255),
    "nail_glow": (199, 125, 255, 255),
    # the blink scatter silhouette's blue slices (build_raiden_movement.py; restored with the release's blink art)
    "blue": (61, 64, 199, 148),
}


def png(path, rgba):
    # Constant 16x16 RGBA textures avoid atlas mipmap surprises of 1px sprites.
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    rows = b"".join(b"\0" + bytes(rgba) * 16 for _ in range(16))
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 16, 8, 6, 0, 0, 0)) +
                     chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))


# Swatches of the release's dome / puppet-arm models; nothing uses them since S3, so they are pruned (the judgment rig's
# armour swatches came back with the 만겁 arm, 10-22a; "blue" came back with the release blink art).
RETIRED = ("floor", "shield_glass", "shield_mist", "hand_dull", "hand_dull_dark")


def build_materials(resourcepack):
    rp = Path(resourcepack)
    out = rp / "assets/rlk/textures/raiden/fx"
    out.mkdir(parents=True, exist_ok=True)
    for name, rgba in PALETTE.items():
        png(out / (name + ".png"), rgba)
    for name in RETIRED:
        (out / (name + ".png")).unlink(missing_ok=True)
    atlaspath = rp / "assets/minecraft/atlases/items.json"
    atlas = json.loads(atlaspath.read_text(encoding="utf-8")) if atlaspath.exists() else {"sources": []}
    atlas["sources"] = [s for s in atlas["sources"] if s.get("resource") not in {"rlk:raiden/fx/" + n for n in RETIRED}]
    known = {s.get("sprite", s.get("resource")) for s in atlas["sources"]}
    for name in PALETTE:
        texture = "rlk:raiden/fx/" + name
        if texture not in known:
            atlas["sources"].append({"type": "minecraft:single", "resource": texture})
    atlaspath.parent.mkdir(parents=True, exist_ok=True)
    atlaspath.write_text(json.dumps(atlas, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(PALETTE)} native RGBA effect materials; opacity range {min(c[3] for c in PALETTE.values())}..255.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resourcepack", type=Path, default=Path(__file__).resolve().parents[2] / "resourcepack")
    build_materials(parser.parse_args().resourcepack)
