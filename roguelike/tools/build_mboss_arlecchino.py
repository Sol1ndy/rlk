#!/usr/bin/env python3
"""아를레키노 (Arlecchino, "The Knave") chapter-4 boss module generator (plan S:ar/PLAN.md, contract S:ar/contract.md;
OWNER: S3).

    python3 tools/build_mboss_arlecchino.py

Registry entry: tools/mboss_registry.json id "arlecchino", n 12, kind chapter, fn boss/arlecchino, arena fl_ruins. Writes
F:boss/arlecchino/** through three api.Writer owners (stale files are deleted only inside each owner's prefixes):
  S3      api.OWN['S3']: the 17 hooks, prep, init, core/ ai/ bond/ hud/ test/ rig_stub/ gate/, p/<P1 key>/
          (tools/mboss_arlecchino/{core,ai,bond,p1,s3lib}.py)
  S4      api.OWN['S4']: p/<P2 key>/ from tools/mboss_arlecchino/p2.py PATTERNS
  S2seq   api.OWN['S2seq']: seq/ from tools/mboss_arlecchino/seq.py SERVICES
Never touched: rig/** (tools/build_arlecchino_rig.mjs, S2) and the kit's fx/** (tools/build_mboss_kn_fx.py, S1K). Missing
stages degrade gracefully: no S2 manifest -> rig_stub/** (api.rig points there); no kit manifest -> api.K lines are empty
(vanilla stand-in particles / sounds); an absent S4 pattern is never picked; an absent S2 sequence runs the core stand-in;
no FN-1 in mboss_lib -> the #bolw stand-in (s3lib).

Generator order: build_mboss_core.py -> build_mboss_arena.py -> build_cboss_rooms.py -> (rig, kit) -> this ->
check_mboss_pack.py. Running it twice gives the same bytes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mboss_arlecchino import api, core, ai, bond, p1, p2, seq  # noqa: E402
from mboss_arlecchino import s3lib as S  # noqa: E402

W3 = api.Writer('S3', api.OWN['S3'])
W4 = api.Writer('S4', api.OWN['S4'])
W2 = api.Writer('S2seq', api.OWN['S2seq'])


def has(Wr, rel):
    return (api.L.FN / f'{api.ROOT}/{rel}.mcfunction').resolve() in Wr.out.written


def main():
    api.rig_manifest()                                   # S2's manifest (or the D0 stub) must match the contract
    pats = []
    for mod, Wr, keys in ((p1, W3, api.P1), (p2, W4, api.P2)):
        for p in mod.PATTERNS:
            assert p.key in keys, f'{mod.__name__}: pattern {p.key} is not one of {keys}'
            assert p.tid == S.TID[p.key], f'{p.key}: tid {p.tid} != the test id {S.TID[p.key]}'
            p.build(Wr)
            for f in ('start', 'tick', 'cancel'):
                assert has(Wr, f'p/{p.key}/{f}'), f'{mod.__name__}: pattern {p.key} wrote no p/{p.key}/{f}'
            pats.append(p)
    keys = [p.key for p in pats]
    assert len(keys) == len(set(keys)), keys
    for s in seq.SERVICES:
        assert s.name in api.SEQS and s.clip in api.CLIPS, (s.name, s.clip)
        s.build(W2)
        for f in ('start', 'tick', 'cancel'):
            assert has(W2, f'seq/{s.name}/{f}'), f'seq.py: service {s.name} wrote no seq/{s.name}/{f}'
    ctx = core.Ctx(pats, W4, seq.SERVICES)
    ai.build(W3, ctx)
    bond.build(W3, ctx)
    core.build(W3, ctx)
    for h in api.L.HOOKS + api.L.HELP_HOOKS + api.L.CHAPTER_HOOKS + ['init']:
        assert has(W3, h), f'hook {h} missing'
    removed = W3.clean() + W4.clean() + W2.clean()
    n3, n4, n2 = len(W3.out.written), len(W4.out.written), len(W2.out.written)
    miss = [k for k in api.P1 + api.P2 if k not in keys]
    print(f'mboss arlecchino: {n3 + n4 + n2} functions (S3 {n3}, S4 {n4}, seq {n2}); patterns {", ".join(keys)}; '
          f'{removed} stale removed.')
    notes = []
    if miss:
        notes.append('patterns not present yet (never picked): ' + ', '.join(miss))
    stand = [n for n in api.SEQS if n not in {s.name for s in seq.SERVICES}]
    if stand:
        notes.append('stand-in sequences (core/sq): ' + ', '.join(stand))
    if not api.rig_real():
        notes.append('rig: stand-in rig_stub/** (tools/arlecchino_rig_manifest.json missing)')
    if not api.K._on():
        notes.append('kit: missing (tools/mboss_kn_fx_manifest.json): vanilla stand-in particles / sounds')
    if not api.arena_ready():
        notes.append('arena fl_ruins: not in the registry yet (no look job calls)')
    if not api.fn1_ready():
        notes.append('FN-1 (mboss_lib bol option) missing: Bond-of-Life hits use the #bolw stand-in (s3lib)')
    for n in notes:
        print('  note: ' + n)


main()
