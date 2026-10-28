#!/usr/bin/env python3
"""Chapter-2 regular mobs: writes every ch2 mob datapack file (never hand-edit them) and the hook lines into the shared
cm / room / combat / load files.

    python3 tools/build_ch2_mobs.py [--datapack <roguelike dir>]

Modules (tools/ch2mob/): common.py (framework, routing, shared hit feel), swarm.py (ns · sl · ss · sp · dr + groups),
rig.py / poses.py (display rig math and keyframes) and, when present, elite.py (kr · nj · cc · ci). Each module's
build(w) writes functions through w(path, text); stale files under the owned ids' folders are deleted. The resource-pack
side is tools/build_ch2_swarm_rigs.mjs. Running it twice gives identical output.
"""
import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'ch2mob'))
sys.path.insert(0, str(HERE))
import common  # noqa: E402
import swarm  # noqa: E402

try:
    from ch2mob import elite, elite_lib  # noqa: E402
except ImportError:
    elite = elite_lib = None


def lint(w):
    bad = []
    for path, text in w.files.items():
        for n, line in enumerate(text.split('\n'), 1):
            if re.search(r'scoreboard players (add|remove) \S+ \S+ -\d', line):
                bad.append(f'{path}:{n}: negative add/remove literal')
            if line.startswith('$') or line.startswith('#'):
                continue
            for ref in re.findall(r'function rlk:([a-z0-9_/.-]+)', line):
                if not w.has(ref):
                    bad.append(f'{path}:{n}: unknown function rlk:{ref}')
            for rid in re.findall(r'"minecraft:item_model":"([^"]+)"', line):
                if rid != rid.lower():
                    bad.append(f'{path}:{n}: resource id not lowercase {rid}')
    if bad:
        raise SystemExit('ch2 lint failed:\n  ' + '\n  '.join(bad[:40]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--datapack', default=str(HERE.parent))
    a = ap.parse_args()
    dp = Path(a.datapack).resolve()
    w = common.Writer(dp)
    common.build(w)
    swarm.build(w)
    owned = list(common.A_IDS)
    if elite is not None:
        elite.build(w)
        owned += list(common.B_IDS)
    common.finish(w)
    lint(w)
    changed, removed = w.flush(owned)
    patched = common.patch_shared(w.fn)
    hooked = elite_lib.install_hooks(w.fn) if elite_lib is not None else 0
    print(f'ch2 mobs: {len(w.files)} functions ({changed} written, {removed} stale removed), '
          f'{len(patched)} shared files patched, elite module {"yes" if elite else "no"} ({hooked} elite hook lines added)')


if __name__ == '__main__':
    main()
