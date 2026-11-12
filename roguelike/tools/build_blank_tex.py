#!/usr/bin/env python3
"""Blank textures for entities that are never meant to be seen (round V, lane VC; v_brief.md §3 "VC" 7).

    python3 tools/build_blank_tex.py --resourcepack <resource pack root>

Why: the player watches a cutscene as a spectator (FN-cam), and the 26.3 client draws every INVISIBLE living entity for a
spectator as a 15 % ghost with the entity's own texture (LivingEntityRenderer: isInvisibleTo(player) is false for a
spectator, the model is submitted with the translucent render type in colour 0x26FFFFFF). No entity flag turns that off. A
texture whose every pixel has alpha 0 leaves nothing to draw (entity.fsh discards on the texture's alpha).

What it writes (deterministic, 64 x 64, all transparent):
  assets/minecraft/textures/entity/zombie/husk.png, husk_baby.png
      the husk: in this pack a husk is only ever an invisible hit-box carrier - the body of every boss of the framework
      (mboss: rlk_mb_body), of every custom mob (cm/spawn/*) and the proxies of the chapter bosses; their looks are display
      rigs. (The one visible husk was the developer fallback `#mobTmp room 1` of room/mob_summon: a zombie since the
      round V integration.)
  assets/rlk/textures/skin/blank.png
      the skin of a mannequin that must not be seen: the avatar while the cutscene actor stands in for it
      (char/cine/blank: profile.texture "rlk:skin/blank"), the mob lure (cm/lure_new).
Round W (lane WC): the two halves of the petal 홍련 cuts in CS1 (tools/mboss_scarlet/seq.py half_summon). No new texture:
two item models that show the upper / the lower half of the kit's whole petal (rlk:mboss/hr_kit/petal_big_0, already a
sprite of the items atlas) on a half card, the centre of the whole card as their origin:
  assets/rlk/items/hr_cine/petal_half_a.json, petal_half_b.json; assets/rlk/models/item/hr_cine/petal_half_a.json, _b.json
Armour stands are NOT blanked (the lobby's doll is a visible one): the F5 seat is removed for the length of a lock instead
(mboss/cam/hold_in) and the cameras are empty item_displays.
"""
import argparse
import struct
import sys
import zlib
from pathlib import Path

FILES = ('assets/minecraft/textures/entity/zombie/husk.png', 'assets/minecraft/textures/entity/zombie/husk_baby.png',
         'assets/rlk/textures/skin/blank.png')
SIZE = 64
PETAL_TEX = 'rlk:mboss/hr_kit/petal_big_0'          # the kit's whole petal (tools/build_mboss_hr_fx.py; 64 x 64, a face card)
# (name, the card's y span in model units, the texture's v span): a = the upper half, b = the lower
PETAL_HALVES = (('a', (8.0, 16.0), (0, 8)), ('b', (0.0, 8.0), (8, 16)))


def petal_half_files():
    """{relative path: text} of the half-petal item definitions and models (the kit's card: a plane at z 8, both faces)."""
    import json
    out = {}
    for name, (y0, y1), (v0, v1) in PETAL_HALVES:
        mid = f'rlk:item/hr_cine/petal_half_{name}'
        out[f'assets/rlk/items/hr_cine/petal_half_{name}.json'] = json.dumps({'model': {'type': 'minecraft:model', 'model': mid}}, separators=(',', ':')) + '\n'
        model = {'ambientocclusion': False, 'textures': {'0': PETAL_TEX, 'particle': PETAL_TEX},
                 'elements': [{'from': [0.0, y0, 8], 'to': [16.0, y1, 8], 'shade': False,
                               'faces': {'south': {'uv': [0, v0, 16, v1], 'texture': '#0'}, 'north': {'uv': [16, v0, 0, v1], 'texture': '#0'}}}]}
        out[f'assets/rlk/models/item/hr_cine/petal_half_{name}.json'] = json.dumps(model, separators=(',', ':')) + '\n'
    return out


def blank_png(w=SIZE, h=SIZE):
    """An RGBA PNG of w x h fully transparent pixels (fixed bytes: no time stamp, one IDAT, compression level 9)."""
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)
    raw = b''.join(b'\x00' + b'\x00\x00\x00\x00' * w for _ in range(h))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--resourcepack', required=True)
    a = ap.parse_args()
    rp = Path(a.resourcepack)
    if not (rp / 'assets').is_dir():
        sys.exit(f'{rp}: not a resource pack root (no assets/)')
    data = blank_png()
    n = 0
    for rel in FILES:
        p = rp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists() or p.read_bytes() != data:
            p.write_bytes(data)
            n += 1
    print(f'blank textures: {len(FILES)} files of {SIZE} x {SIZE} transparent pixels ({n} written, {len(FILES) - n} unchanged).')
    if not (rp / 'assets/rlk/textures/mboss/hr_kit/petal_big_0.png').exists():
        sys.exit(f'{rp}: the kit\'s petal texture is missing (run tools/build_mboss_hr_fx.py --resourcepack first)')
    m = 0
    halves = petal_half_files()
    for rel, text in halves.items():
        p = rp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists() or p.read_text(encoding='utf-8') != text:
            p.write_text(text, encoding='utf-8')
            m += 1
    print(f'petal halves: {len(halves)} files ({m} written, {len(halves) - m} unchanged).')


if __name__ == '__main__':
    main()
