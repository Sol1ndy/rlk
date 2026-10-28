#!/usr/bin/env python3
"""TEMPORARY runner for part B (the lead deletes it at merge; A's tools/build_ch2_mobs.py then imports ch2mob/elite.py).

    python3 tools/build_ch2_elite_only.py            # writes cm/{kr,nj,cc,ci}/** and cm/spawn/{kr,nj,cc,ci}
    python3 tools/build_ch2_elite_only.py --hooks    # + installs elite_lib.HOOKS into the shared cm files (local tests only)

Run tools/build_ch2_elite_rigs.mjs first when the rigs change (it writes tools/ch2_elite_poses.json).
Stale files under the four id folders (and the four spawn files) that this run did not write are deleted.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS / 'ch2mob'))
import elite  # noqa: E402
import elite_lib  # noqa: E402

FN = TOOLS.parent / 'data/rlk/function'
OWN_DIRS = [FN / 'cm' / m for m in elite_lib.IDS]
OWN_SPAWN = [FN / 'cm/spawn' / f'{m}.mcfunction' for m in elite_lib.IDS]
written = {}


def w(path, text):
    p = FN / (path + '.mcfunction')
    rel = p.relative_to(FN).as_posix()
    if not (any(d in p.parents for d in OWN_DIRS) or p in OWN_SPAWN):
        raise SystemExit(f'elite generator may not write {rel}')
    if rel in written:
        raise SystemExit(f'written twice: {rel}')
    text = text.rstrip('\n') + '\n'
    written[rel] = text
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists() or p.read_text(encoding='utf-8') != text:
        p.write_text(text, encoding='utf-8')


elite.build(w)
stale = 0
for d in OWN_DIRS:
    for p in sorted(d.rglob('*.mcfunction')) if d.exists() else []:
        if p.relative_to(FN).as_posix() not in written:
            p.unlink()
            stale += 1
for p in OWN_SPAWN:
    if p.exists() and p.relative_to(FN).as_posix() not in written:
        p.unlink()
        stale += 1
hooks = elite_lib.install_hooks(FN) if '--hooks' in sys.argv else 0
print(f'ch2 elite: {len(written)} functions, {stale} stale removed, {hooks} hook lines installed')
