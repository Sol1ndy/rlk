#!/usr/bin/env python3
"""Resource-pack lint for client-only failures the server load check cannot see.

usage: python3 -I rplint.py <unpacked resource pack>
Fails (exit 1) on: asset paths with characters outside [a-z0-9_.-/] (one bad id makes the client reject a whole
atlas or model set), invalid or missing atlas sources, JSON that does not parse.
"""
import glob
import json
import os
import re
import sys

rp = sys.argv[1]
ok_path = re.compile(r'[a-z0-9_.\-/]+')
ok_id = re.compile(r'[a-z0-9_.\-]+:[a-z0-9_.\-/]+')
problems = []
for f in glob.glob(os.path.join(rp, 'assets', '**', '*'), recursive=True):
    if os.path.isdir(f):
        continue
    rel = os.path.relpath(f, os.path.join(rp, 'assets'))
    if not ok_path.fullmatch(rel):
        problems.append(f'bad path: {rel}')
    if f.endswith(('.json', '.mcmeta')):
        try:
            json.load(open(f, encoding='utf-8'))
        except Exception as e:  # noqa: BLE001
            problems.append(f'bad json: {rel}: {e}')
for atlas in glob.glob(os.path.join(rp, 'assets', '*', 'atlases', '*.json')):
    try:
        srcs = json.load(open(atlas, encoding='utf-8')).get('sources', [])
    except Exception:  # noqa: BLE001
        continue
    for s in srcs:
        rid = s.get('resource')
        if rid is None:
            continue
        if not ok_id.fullmatch(rid):
            problems.append(f'bad atlas id in {os.path.basename(atlas)}: {rid}')
            continue
        ns, p = rid.split(':', 1)
        if ns != 'minecraft' and not os.path.exists(os.path.join(rp, 'assets', ns, 'textures', p + '.png')):
            problems.append(f'missing atlas texture in {os.path.basename(atlas)}: {rid}')
print(f'rplint: {len(problems)} problem(s)')
for p in problems[:40]:
    print('  ' + p)
sys.exit(1 if problems else 0)
