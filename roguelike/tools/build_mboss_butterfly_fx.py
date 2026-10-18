#!/usr/bin/env python3
"""Resource-pack side of the butterfly module's tinted FX cards (tools/mboss_butterfly/cards.py):

    python3 tools/build_mboss_butterfly_fx.py --resourcepack <unpacked RP>

Writes assets/rlk/{textures,models/item,items}/mboss/bf_fx/<kind> (greyscale sprites, tinted card models, item
definitions with the custom_model_data colour tint) and adds them to assets/minecraft/atlases/items.json. The
datapack engine (F:mboss/butterfly/tc/**) is written by tools/build_mboss_butterfly.py.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mboss_butterfly import cards  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('--resourcepack', required=True)
args = ap.parse_args()
n, px = cards.build_resourcepack(args.resourcepack)
print(f'butterfly fx cards: {n} tinted kinds, {px} px of sprites -> {args.resourcepack}')
