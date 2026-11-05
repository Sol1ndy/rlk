#!/usr/bin/env python3
"""홍련 (Scarlet) special-boss module generator (plan S:hr/PLAN.md, contract S:hr/contract.md; OWNER: S3).

    python3 tools/build_mboss_scarlet.py

Registry entry: tools/mboss_registry.json id "scarlet", n 21, kind special, fn boss/scarlet, arena hr_field. Writes
F:boss/scarlet/** through three api.Writer owners (stale files are deleted only inside each owner's prefixes):
  S3   api.OWN['S3']: the 17 hooks + test/help, init, reward (FN-b), core/ ai/ shield/ ult/ hud/ ev/ test/ rig_stub/,
       p/<P1 key>/ (tools/mboss_scarlet/{core,ai,shield,p1,s3lib,reward}.py)
  S4   api.OWN['S4']: p/<P2 key>/ and g/ from tools/mboss_scarlet/p_ghost.py PATTERNS
  S2b  api.OWN['S2b']: seq/ from tools/mboss_scarlet/seq.py SERVICES
Never touched: rig/** (tools/build_scarlet_rig.mjs, S2a / S2b) and the kit's fx/** (tools/build_mboss_hr_fx.py, S1K).
Missing stages degrade gracefully: no rig manifest -> rig_stub/** (api.rig points there); no kit manifest -> api.K lines
are empty (vanilla stand-in particles / sounds); an absent P2 pattern is never picked; an absent gauntlet runs the core
stand-in core/gs/<g>/**; an absent sequence the core stand-in core/sq/<name>/**; no arena theme -> no look jobs.

Generator order: build_mboss_core.py -> build_mboss_arena.py -> (rig, kit) -> this -> check_mboss_pack.py. Running it twice
gives the same bytes.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mboss_scarlet import api, core, ai, shield, p1, reward, p_ghost, seq  # noqa: E402
from mboss_scarlet import s3lib as S  # noqa: E402

W3 = api.Writer('S3', api.OWN['S3'])
W4 = api.Writer('S4', api.OWN['S4'])
W2 = api.Writer('S2b', api.OWN['S2b'])


def has(Wr, rel):
    return (api.L.FN / f'{api.ROOT}/{rel}.mcfunction').resolve() in Wr.out.written


def own_names(Wr):
    """Every '#name hr' fake player written by the files of one Writer (the static check of S3's names)."""
    names = set()
    pat = re.compile(r'(#[A-Za-z0-9_]+) ' + api.OBJ + r'(?=[ \]}]|$)')
    for p in Wr.out.written:
        for ln in Path(p).read_text(encoding='utf-8').split('\n'):
            if not ln.lstrip().startswith('#'):
                names.update(pat.findall(ln))
    return names


def main():
    api.rig_manifest()                                   # S2a's manifest (or the D0 stub) must match the contract
    pats = []
    for mod, Wr, keys in ((p1, W3, api.P1), (p_ghost, W4, api.P2)):
        for p in mod.PATTERNS:
            assert p.key in keys, f'{mod.__name__}: pattern {p.key} is not one of {keys}'
            assert p.tid == S.TID[p.key], f'{p.key}: tid {p.tid} != s3lib.TID {S.TID[p.key]}'
            p.build(Wr)
            for f in ('start', 'tick', 'cancel'):
                assert has(Wr, f'p/{p.key}/{f}'), f'{mod.__name__}: pattern {p.key} wrote no p/{p.key}/{f}'
            pats.append(p)
    keys = [p.key for p in pats]
    assert len(keys) == len(set(keys)), keys
    for s in seq.SERVICES:
        assert s.name in api.SEQS and all(c in api.CLIPS for c in s.clip), (s.name, s.clip)
        s.build(W2)
        for f in ('start', 'tick', 'cancel') + (api.SEQ_EXTRA.get(s.name, ())):
            assert has(W2, f'seq/{s.name}/{f}'), f'seq.py: service {s.name} wrote no seq/{s.name}/{f}'
    for s in reward.SERVICES:
        s.build(W3)
    for f in api.EV_CALLS + (api.REWARD_HOOK,):
        assert has(W3, f), f'reward.py wrote no {f}'
    ctx = core.Ctx(pats, W4, seq.SERVICES)
    shield.build(W3)
    ai.build(W3, ctx)
    core.build(W3, ctx)
    for h in api.L.HOOKS + api.L.HELP_HOOKS + ['init', api.REWARD_HOOK]:
        assert has(W3, h), f'hook {h} missing'
    for call in api.SHIELD_CALLS.values():
        assert has(W3, call), f'shield call {call} missing'
    # S3's fake players of objective hr: the registered core names, a P1 pattern's own #<key>_<x>, the event scores
    names = own_names(W3)
    bad = sorted(n for n in names if n not in S.FP and n not in api.EV_FP and n != api.SEQ_SIGNAL
                 and not n.startswith(S.FP_PATTERN_PREFIXES))
    assert not bad, f'unregistered fake players of objective {api.OBJ} (add them to s3lib.FP): {bad}'
    removed = W3.clean() + W4.clean() + W2.clean()
    n3, n4, n2 = len(W3.out.written), len(W4.out.written), len(W2.out.written)
    miss = [k for k in api.P1 + api.P2 if k not in keys]
    print(f'mboss scarlet: {n3 + n4 + n2} functions (S3 {n3}, S4 {n4}, seq {n2}); patterns {", ".join(keys)}; '
          f'{removed} stale removed.')
    notes = []
    if miss:
        notes.append('patterns not present yet (never picked; gauntlets: core/gs stand-in): ' + ', '.join(miss))
    stand = [n for n in api.SEQS if n not in {s.name for s in seq.SERVICES}]
    if stand:
        notes.append('stand-in sequences (core/sq): ' + ', '.join(stand))
    if not api.rig_real():
        notes.append('rig: stand-in rig_stub/** (tools/scarlet_rig_manifest.json missing)')
    if not api.K._on():
        notes.append('kit: missing (tools/mboss_hr_fx_manifest.json): vanilla stand-in particles / sounds')
    if not api.theme_ready():
        notes.append('arena hr_field: no theme yet (tools/mboss_arena_hr_field.py): no look jobs')
    for n in notes:
        print('  note: ' + n)


main()
