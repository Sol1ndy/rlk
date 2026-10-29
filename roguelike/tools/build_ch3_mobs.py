#!/usr/bin/env python3
"""Chapter-3 (Sumeru) regular mobs: writes every ch3 mob datapack file (never hand-edit them) and the hook lines into
the shared cm / combat / room / load files.

    python3 tools/build_ch3_mobs.py [--datapack <roguelike dir>]

Modules (tools/ch3mob/): common.py (framework, routing, shared hook lines), swarm.py (fu · fp · em · sb · cw + the
groups g_fu · g_em · g_sb), poses.py (keyframes) and, when present, part B's elite.py (cs · rv · pc) with
elite_lib.install_hooks for its shared-file lines. Built on tools/ch2mob (imported, not copied). Stale files under the
owned ids' folders, cm/c3/** and the ch3 spawn files are deleted. The resource-pack side is
tools/build_ch3_swarm_rigs.mjs (+ B's tools/build_ch3_elite_rigs.mjs). Running it twice, before or after
build_ch2_mobs.py, gives identical output.
"""
import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'ch2mob'))   # ch2mob/swarm.py imports its siblings (rig, poses) by plain name
sys.path.insert(0, str(HERE))
from ch2mob import common as c2  # noqa: E402
from ch3mob import common  # noqa: E402
from ch3mob import swarm  # noqa: E402

try:
    from ch3mob import elite  # noqa: E402
except ImportError:
    elite = None
try:
    from ch3mob import elite_lib  # noqa: E402
except ImportError:
    elite_lib = None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--datapack', default=str(HERE.parent))
    a = ap.parse_args()
    dp = Path(a.datapack).resolve()
    w = common.Writer(dp)
    common.build(w)
    swarm.build(w)
    owned = list(common.OWN_IDS)
    if elite is not None:
        elite.build(w)
        owned += list(common.B_IDS)
    common.finish(w)
    c2.lint(w, 'ch3')
    changed, removed = w.flush(owned)
    patched = common.patch_shared(w.fn)
    hooked = elite_lib.install_hooks(w.fn) if elite_lib is not None else 0
    print(f'ch3 mobs: {len(w.files)} functions ({changed} written, {removed} stale removed), '
          f'{len(patched)} shared files patched, elite module {"yes" if elite else "no"} ({hooked} elite hook lines added)')


if __name__ == '__main__':
    main()
