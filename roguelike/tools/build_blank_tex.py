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
      rigs. (The one visible husk is the developer fallback `#mobTmp room 1` of room/mob_summon: it loses its look.)
  assets/rlk/textures/skin/blank.png
      the skin of a mannequin that must not be seen: the avatar while the cutscene actor stands in for it
      (char/cine/blank: profile.texture "rlk:skin/blank"), the mob lure (cm/lure_new).
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


if __name__ == '__main__':
    main()
