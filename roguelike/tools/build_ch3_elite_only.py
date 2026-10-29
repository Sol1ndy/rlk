#!/usr/bin/env python3
"""TEMPORARY runner for the chapter-3 elites (part B) until build_ch3_mobs.py (part A) is merged; the lead deletes it then.

    python3 tools/build_ch3_elite_only.py [--datapack <roguelike dir>] [--hooks <data/rlk/function of a test copy>]

Writes cm/{cs,rv,pc}/** and cm/spawn/{cs,rv,pc} through tools/ch3mob/elite.py (stale files there are removed). It never
touches shared files: --hooks installs elite_lib.HOOKS into the given function tree only (a test copy). Rigs / skins:
node tools/build_ch3_elite_rigs.mjs --resourcepack <rp> (writes tools/ch3_elite_poses.json, read here). Running it twice
gives identical output.
"""
import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ch3mob import elite, elite_lib  # noqa: E402

IDS = elite_lib.IDS


class Writer:
    def __init__(self, dp):
        self.fn = Path(dp) / 'data' / 'rlk' / 'function'
        self.files = {}

    def __call__(self, path, text):
        if not re.fullmatch(r'[a-z0-9_./-]+', path):
            raise ValueError('bad function path ' + path)
        if not (path.startswith(tuple(f'cm/{m}/' for m in IDS)) or path in {f'cm/spawn/{m}' for m in IDS}):
            raise ValueError('outside part B: ' + path)
        if path in self.files:
            raise ValueError('written twice: ' + path)
        self.files[path] = '\n'.join(x.rstrip() for x in text.strip('\n').split('\n')) + '\n'

    def has(self, path):
        return path in self.files or (self.fn / (path + '.mcfunction')).exists()

    def flush(self):
        old = set()
        for m in IDS:
            d = self.fn / 'cm' / m
            if d.is_dir():
                old |= {str(f.relative_to(self.fn))[:-len('.mcfunction')] for f in d.rglob('*.mcfunction')}
            if (self.fn / 'cm' / 'spawn' / f'{m}.mcfunction').exists():
                old.add(f'cm/spawn/{m}')
        changed = 0
        for path, text in sorted(self.files.items()):
            p = self.fn / (path + '.mcfunction')
            if p.exists() and p.read_text(encoding='utf-8') == text:
                continue
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding='utf-8')
            changed += 1
        stale = sorted(old - set(self.files))
        for path in stale:
            (self.fn / (path + '.mcfunction')).unlink()
        for m in IDS:                                   # empty folders left by removed functions
            d = self.fn / 'cm' / m
            if d.is_dir():
                for sub in sorted((x for x in d.rglob('*') if x.is_dir()), key=lambda x: -len(x.parts)):
                    if not any(sub.iterdir()):
                        sub.rmdir()
        return changed, len(stale)


def lint(w):
    bad = []
    for path, text in w.files.items():
        for n, line in enumerate(text.split('\n'), 1):
            if re.search(r'scoreboard players (add|remove) \S+ \S+ -\d', line):
                bad.append(f'{path}:{n}: negative add/remove literal')
            if re.search(r'playsound (?!minecraft:)', line):
                bad.append(f'{path}:{n}: non-vanilla sound')
            if line.startswith('#'):
                continue
            for ref in re.findall(r'function rlk:([a-z0-9_/.-]+)', line.lstrip('$')):
                if '$(' in ref or ref.endswith('/'):
                    continue
                if not w.has(ref):
                    bad.append(f'{path}:{n}: unknown function rlk:{ref}')
            for rid in re.findall(r'"minecraft:item_model":"([^"]+)"', line):
                if rid != rid.lower():
                    bad.append(f'{path}:{n}: resource id not lowercase {rid}')
    if bad:
        raise SystemExit('ch3 elite lint failed:\n  ' + '\n  '.join(bad[:40]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--datapack', default=str(HERE.parent))
    ap.add_argument('--hooks', default=None, help='install elite_lib.HOOKS into this data/rlk/function tree (a test copy)')
    a = ap.parse_args()
    w = Writer(Path(a.datapack).resolve())
    elite.build(w)
    lint(w)
    changed, removed = w.flush()
    hooked = elite_lib.install_hooks(a.hooks) if a.hooks else 0
    print(f'ch3 elites: {len(w.files)} functions ({changed} written, {removed} stale removed), {hooked} hook lines added'
          + (f' to {a.hooks}' if a.hooks else ' (shared files untouched)'))


if __name__ == '__main__':
    main()
