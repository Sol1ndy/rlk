#!/usr/bin/env python3
"""ident_hr.py: identity of the merged 홍련 (Scarlet) tree against the 11-03 handover tree 35b82e5 (I1; scratchpad
hr/i1_brief.md I1a step 7, hr/contract.md §5 "the I1 ident.py allow-list").

    python3 ident_hr.py <datapack root> [--base 35b82e5] [-v]

Read only: the tree's files are hashed as git blobs and compared with `git ls-tree -r <base>` of the tree's own
repository (the worktree; the objects live in /home/user/rlk). Scope = every file under data/ (F: and the rest of the
datapack), every generated manifest of tools/ (tools/**/*manifest*.json, tools/player_motion/compiled_audio.json),
items.md and pack.mcmeta. A file of the scope that is new, changed or gone must be on the allow-list:

  contract §5   D0's arena lines: F:mboss/ar/{box_absorb,clamp,clamp_step,clampw,clampw_step,ensure,fl_off,fl_on,full_rim,
                leash,loaded,marker,ok,oob,sweep,test,tp_in}, F:mboss/arena/clear_all, F:mboss/cb/remove, F:mboss/cleanup,
                F:mboss/fight_vars, F:mboss/uninstall; the new trees F:mboss/ar/hr_field/**, F:mboss/arena/hr_field/**;
                the FN outputs (S1): F:mboss/{sp/reward,test/swon,test/swon_msg_w,death_finish,register,world,fight_vars,
                cleanup_fight,bars_off,bars_on}; what enabling her adds (n 21 / hr_field lines): F:mboss/d/*,
                F:mboss/{register,sp/gate,sp/prep,sp/pp/scarlet,sp/g/scarlet,cb/inc/scarlet}, F:mboss/test/{help_special,
                help_pattern,help_rift_id,help_special_ch}, the arena dispatchers F:mboss/arena/{job_tick,abort} (S1K's
                theme lines, I1b); the module tree F:boss/scarlet/**
  contract §1   SR's hand files: F:items/{register,build_rarbuckets,enh_add}, F:items/tune/b10,
                F:items/hook/{on_hit,stat_buffs,tick_player,on_cast_burst}, F:items/mythic/sword_hwamu/**, F:items/proc/hw_*,
                F:player/{take_damage,dash_iframe,reset_one,update_item,update_item_macro}, F:player/hr_moon/apply,
                F:codex/labels, F:snd/f422..f429, F:load, F:uninstall, items.md
  this boss     its own generated manifests: tools/scarlet_rig_manifest.json (S2a / S2b), tools/mboss_hr_fx_manifest.json
                (S1K, I1b), tools/mboss_scarlet/stub_rig_manifest.json (D0, api.py --write-stub)
  F3 (review)   the pack-wide lines of the lead's decisions: F:view/{tick,ride_tick,sel_xhair} (HR-08: vBig counted down in
                every view), F:lvup/tick (HR-34: no F5 sneak-tap during a boss intro), F:items/hook/on_dash (HR-09: the
                sword's dash window)
  release       pack.mcmeta: the build stamp at the end of its description (README 0-5 step 3; V-I, 11-06)
  combat P      the late-game lag fixes (11-10): F:player/{tick,hotbar/place,hotbar/wrap,inv/sync,inv/manage,
                inv/collect_none}, F:items/{equip_scan,scan_*,scan_s/*}, F:engravings/info_{build,bucket*,pass*}

Prints every allow-listed file that changed (grouped) and fails on anything else (FAIL lines name the files).
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ARGS = [a for a in sys.argv[1:] if a != '-v']
VERBOSE = '-v' in sys.argv[1:]
BASE = '35b82e5'
if '--base' in ARGS:
    i = ARGS.index('--base')
    BASE = ARGS[i + 1]
    del ARGS[i:i + 2]
DP = Path(ARGS[0]).resolve()
REPO = DP.parent
F = 'data/rlk/function/'

AR_DISP = ('box_absorb', 'clamp', 'clamp_step', 'clampw', 'clampw_step', 'ensure', 'fl_off', 'fl_on', 'full_rim', 'leash',
           'loaded', 'marker', 'ok', 'oob', 'sweep', 'test', 'tp_in')
ALLOW = {
    'contract §5 D0 arena lines': [F + f'mboss/ar/{n}.mcfunction' for n in AR_DISP]
    + [F + 'mboss/arena/clear_all.mcfunction', F + 'mboss/cb/remove.mcfunction', F + 'mboss/cleanup.mcfunction',
       F + 'mboss/fight_vars.mcfunction', F + 'mboss/uninstall.mcfunction', F + r'mboss/ar/hr_field/.+',
       F + r'mboss/arena/hr_field/.+'],
    'contract §5 FN outputs (S1)': [F + f'mboss/{n}.mcfunction' for n in (
        'sp/reward', 'test/swon', 'test/swon_msg_w', 'death_finish', 'register', 'world', 'fight_vars', 'cleanup_fight',
        'bars_off', 'bars_on')],
    'contract §5 enabling her (n 21 / hr_field lines)': [F + r'mboss/d/[^/]+\.mcfunction']
    + [F + f'mboss/{n}.mcfunction' for n in ('register', 'sp/gate', 'sp/prep', 'sp/pp/scarlet', 'sp/g/scarlet',
                                              'cb/inc/scarlet', 'test/help_special', 'test/help_pattern', 'test/help_rift_id',
                                              'test/help_special_ch', 'arena/job_tick', 'arena/abort')],
    'contract §5 the module tree F:boss/scarlet/**': [F + r'boss/scarlet/.+'],
    'contract §1 SR hand files': [F + f'items/{n}.mcfunction' for n in ('register', 'build_rarbuckets', 'enh_add', 'tune/b10')]
    + [F + f'items/hook/{n}.mcfunction' for n in ('on_hit', 'stat_buffs', 'tick_player', 'on_cast_burst')]
    + [F + r'items/mythic/sword_hwamu/.+', F + r'items/proc/hw_[a-z_]+\.mcfunction']
    + [F + f'player/{n}.mcfunction' for n in ('take_damage', 'dash_iframe', 'reset_one', 'update_item', 'update_item_macro',
                                               'hr_moon/apply')]
    + [F + 'codex/labels.mcfunction', F + r'snd/f42[2-9]\.mcfunction', F + 'load.mcfunction', F + 'uninstall.mcfunction',
       'items.md'],
    'this boss\'s generated manifests': ['tools/scarlet_rig_manifest.json', 'tools/mboss_hr_fx_manifest.json',
                                         'tools/mboss_scarlet/stub_rig_manifest.json'],
    'F3 review fixes (pack-wide lines)': [F + f'view/{n}.mcfunction' for n in ('tick', 'ride_tick', 'sel_xhair')]
    + [F + 'lvup/tick.mcfunction', F + 'items/hook/on_dash.mcfunction'],
    # F-I (f2-8, V2R-02): start_go shows the bars only while the spawn hook left them on (#mbBarOff; build_mboss_core.py)
    'F-I review fixes (pack-wide lines)': [F + 'mboss/start_go.mcfunction'],
    # V-I (11-06): every release re-stamps the datapack's pack.mcmeta description (README 0-5 step 3)
    'release build stamp (README 0-5 step 3)': ['pack.mcmeta'],
    # combat lane P (11-10, wip/combat-perf; plan/combat/research_misc.md §4): the late-game lag fixes — rebuilt hotbar items
    # finished inside player/tick, the F-swap event, the inventory sync / equipment scan / engraving sort fast paths
    # (items/enh_add, load, uninstall are already on the SR list)
    'combat P late-game lag (11-10)': [F + f'player/{n}.mcfunction' for n in ('tick', 'hotbar/place', 'hotbar/wrap', 'inv/sync',
                                                                               'inv/manage', 'inv/collect_none')]
    + [F + 'items/equip_scan.mcfunction', F + r'items/scan_[a-z_]+\.mcfunction', F + r'items/scan_s/[a-z_]+\.mcfunction']
    + [F + r'engravings/info_(build|bucket|bucket_loop|bucket_put|pass|pass_one)\.mcfunction'],
}
PATS = [(grp, re.compile(p)) for grp, ps in ALLOW.items() for p in ps]


def in_scope(rel):
    return (rel.startswith('data/') or rel in ('items.md', 'pack.mcmeta') or rel == 'tools/player_motion/compiled_audio.json'
            or (rel.startswith('tools/') and not rel.startswith('tools/dev/') and 'manifest' in rel.rsplit('/', 1)[-1]
                and rel.endswith('.json')))


def allowed(rel):
    return next((grp for grp, p in PATS if p.fullmatch(rel)), None)


def blob(p):
    b = p.read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


def main():
    out = subprocess.run(['git', '-C', str(REPO), 'ls-tree', '-r', '--full-tree', BASE, '--', 'roguelike'],
                         capture_output=True, text=True, check=True).stdout
    base = {}
    for ln in out.splitlines():
        meta, path = ln.split('\t', 1)
        rel = path[len('roguelike/'):]
        if in_scope(rel):
            base[rel] = meta.split()[2]
    cur = {}
    for p in DP.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:
            rel = p.relative_to(DP).as_posix()
            if in_scope(rel):
                cur[rel] = blob(p)
    new = sorted(set(cur) - set(base))
    gone = sorted(set(base) - set(cur))
    changed = sorted(k for k in set(cur) & set(base) if cur[k] != base[k])
    print(f'ident_hr: {len(cur)} files in scope on the tree, {len(base)} at {BASE}; changed {len(changed)}, new {len(new)}, '
          f'gone {len(gone)}')
    groups, bad = {}, []
    for kind, lst in (('changed', changed), ('new', new), ('gone', gone)):
        for rel in lst:
            g = allowed(rel)
            if g and kind != 'gone':
                groups.setdefault(g, {}).setdefault(kind, []).append(rel)
            else:
                bad.append((kind, rel))
    for g in ALLOW:
        if g in groups:
            parts = ', '.join(f'{k} {len(v)}' for k, v in groups[g].items())
            print(f'  allowed  {g}: {parts}')
            for k, v in groups[g].items():
                shown = v if (VERBOSE or len(v) <= 40) else v[:12] + [f'... (+{len(v) - 12})']
                for rel in shown:
                    print(f'           {k:7s} {rel}')
    for kind, rel in bad:
        print(f'FAIL {kind} outside the allow-list: {rel}')
    if bad:
        print(f'{len(bad)} IDENT_HR CHECK(S) FAILED')
        return 1
    print(f'ident_hr: every in-scope file outside the allow-list is byte-identical to {BASE}; ALL IDENT_HR CHECKS PASSED')
    return 0


if __name__ == '__main__':
    sys.exit(main())
