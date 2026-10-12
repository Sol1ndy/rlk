"""Regenerate every Narukami (Raiden) boss output in dependency order.

Usage (from anywhere):
    python tools/build_raiden_all.py [--resourcepack <unpacked resource pack>] [--skin <raiden skin png>]

The resource pack defaults to the `resourcepack` folder next to the datapack
folder (the same default the hazard and material generators use). The item
atlas is merged, never replaced, so other entries of the pack are kept.
"""
from pathlib import Path
import argparse
import subprocess
import sys

TOOLS = Path(__file__).resolve().parent
DATAPACK = TOOLS.parent

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--resourcepack", type=Path, default=DATAPACK.parent / "resourcepack")
parser.add_argument("--skin", type=Path, help="Raiden skin PNG; only needed when the pack has no rlk:raiden/skin yet")
args = parser.parse_args()
rp = str(args.resourcepack.resolve())
if not args.resourcepack.is_dir():
    sys.exit(f"Resource pack folder not found: {rp}")

node = ["node"]
steps = [
    ["python3", "build_raiden_materials.py", "--resourcepack", rp],
    # painted gradient lightning sprites (rlk:raiden/fxg/*) used by the effect generators below
    ["python3", "build_raiden_fx_textures.py", "--resourcepack", rp],
    ["python3", "build_raiden_encounter.py"],
    ["python3", "build_raiden_arena.py"],
    ["python3", "build_raiden_cinematic.py"],
    ["python3", "build_raiden_hazards.py", "--resourcepack", rp],
    ["python3", "build_raiden_movement.py", "--resourcepack", rp],
    ["python3", "build_raiden_object_vfx.py", "--resourcepack", rp],
    ["python3", "build_raiden_orb.py", "--resourcepack", rp],
    ["python3", "build_raiden_signature_vfx.py", "--resourcepack", rp],
    ["python3", "build_raiden_illusions.py", "--resourcepack", rp],
    node + ["build_raiden_rig.mjs", "--resourcepack", rp] + (["--skin", str(args.skin.resolve())] if args.skin else []),
    node + ["build_raiden_judgment_rig.mjs", "--resourcepack", rp],
]
for step in steps:
    if step[0] == "python3":
        step = [sys.executable] + step[1:]
    print("$", " ".join(step[:2]))
    subprocess.run(step, cwd=TOOLS, check=True)
print("Done. Apply with /reload (datapack) and F3+T (resource pack).")
