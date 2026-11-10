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
  lane R        the combat overhaul's removals (11-10, wip/combat-rm): 요이미야 / the bow (char/yoimiya/**, char/bow/**,
                the migration char/migrate_yoi*, the hand files that called them, mboss/px/db), the first-person mode and the
                shoulder view (view/**, lobby/** settings and tutorial texts, char/{ronova,nefer}/def texts), the pick subtitle
                (lvup/pick_sub)
  lane C        the combat overhaul's parry / dodge (11-10, wip/combat-core): player/def/**, the dash files (its charges, gauge
                and i-frame files gone), cm hit context, the boss framework's no-parry / near re-test / glint lines, Raiden's
                hazard land, 홍련's pips and yellow-flag marks, the item / engraving / character texts, the guard clips
  combat P      the late-game lag fixes (11-10): F:player/{tick,hotbar/place,hotbar/wrap,inv/sync,inv/manage,
                inv/order_count2}, F:items/{equip_scan,scan_*,scan_s/*}, F:engravings/info_{build,bucket*,pass*}
  combat B      the balance gauge / groggy (11-10, wip/combat-bal): F:bal/**, the bosses' bal_{ok,on,tick,off} hooks and their
                own groggies' refill lines, the mob / cm / combat / burst hook lines, the cm rig ticks, Raiden's balance stun
  lane H2       the 홍련 rebuild's cinematic lock FN-cam (11-11, wip/combat-hr2): F:mboss/cam/**, the request lines of
                F:mboss/{main,cleanup_fight,init,uninstall}, F:tick, F:view/tick, F:lvup/tick

Prints every allow-listed file that changed (grouped) and fails on anything else (FAIL lines name the files). A gone
file passes only in a group named in ALLOW_GONE.
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
    # finished inside player/tick, the F-swap event, the inventory sync / equipment scan / engraving sort fast paths;
    # order_count2's temporaries no longer overwrite load's constant #c2 tmp
    # (items/enh_add, load, uninstall are already on the SR list)
    'combat P late-game lag (11-10)': [F + f'player/{n}.mcfunction' for n in ('tick', 'hotbar/place', 'hotbar/wrap', 'inv/sync',
                                                                               'inv/manage', 'inv/order_count2')]
    + [F + 'items/equip_scan.mcfunction', F + r'items/scan_[a-z_]+\.mcfunction', F + r'items/scan_s/[a-z_]+\.mcfunction']
    + [F + r'engravings/info_(build|bucket|bucket_loop|bucket_put|pass|pass_one)\.mcfunction'],
}
# 11-10 combat overhaul, lane R (wip/combat-rm; tools/dev/plan/combat/r_progress.md): the files it changes, adds and removes
# on purpose (요이미야 and the bow, the first-person mode and the shoulder view, the pick subtitle in combat). Its removals
# are the only allowed `gone` files.
LANE_R = 'combat overhaul R (11-10): 요이미야 / bow, first person / shoulder view, pick subtitle'
VIEW_GONE = 'mode|mode_do|mode_help|on|off|ride|rot|rot_lead|cam_go|cam_step|cam_put|cam_y|cam_calc|dur_set|dur_set2|set|tune|tune_apply'
ALLOW[LANE_R] = (
    [F + r'char/yoimiya/.+', F + r'char/bow/[a-z_0-9]+\.mcfunction', F + r'char/migrate_yoi(?:_[a-z]+)?\.mcfunction',
     F + 'char/weapon_item_bow.mcfunction', F + r'char/(?:ronova|nefer)/def\.mcfunction', F + 'mboss/px/db.mcfunction',
     F + 'mboss/px/db/aurend.mcfunction', F + r'lobby/set/s2[0245]\.mcfunction', F + rf'view/(?:{VIEW_GONE})\.mcfunction']
    + [F + f'char/{n}.mcfunction' for n in ('burst_go', 'burst_wind', 'cast_skill', 'load_cur', 'player_init', 'reg_items',
                                             'setup', 'tick')]
    + [F + f'combat/{n}.mcfunction' for n in ('apply', 'apply_mods', 'on_attack', 'rclick_do')]
    + [F + f'lobby/{n}.mcfunction' for n in ('act', 'build', 'set/cam', 'set/labels', 'tick', 'tut/s1', 'tut/s11')]
    + [F + f'player/{n}.mcfunction' for n in ('f_key', 'hotbar/fix_attack', 'level/up', 'swing/jump', 'swing/tick', 'tick')]
    + [F + f'view/{n}.mcfunction' for n in ('av_unwrap', 'burst_camera_apply', 'burst_camera_tick', 'hand_wrap', 'hold', 'move',
                                             'rays', 'slow', 'spawn', 'sync', 'ttl_blank')]
    + [F + n for n in ('items/q/run.mcfunction', 'lvup/pick_sub.mcfunction', 'mob/tick.mcfunction', 'room/fall/mob_reward.mcfunction',
                       'room/fall/player.mcfunction', 'tick.mcfunction')])
# 11-10 combat overhaul, lane C (wip/combat-core; tools/dev/plan/combat/c_progress.md): the parry on F, the dodge replacing the
# dash (its charge / gauge / i-frame files are removed on purpose), the damage context and judge (player/def/**), the boss
# framework's no-parry / near re-test / glint, Raiden's hazard land, 홍련's pips and yellow-flag marks, the readers, lores
LANE_C = 'combat overhaul C (11-10): parry, dodge, damage context, unparriable attacks'
_LANE_C_FN = (
    'boss/apep/org/pj_end', 'boss/raiden/hazard/land', 'boss/raiden/hazard/land_nd',
    'boss/raiden/hazard/new', 'boss/raiden/hazard/try', 'boss/raiden/hazard/try_near', 'boss/scarlet/core/setup',
    'boss/scarlet/fx/hud/warn', 'boss/scarlet/g/disc/throw', 'boss/scarlet/p/a10/k/21', 'boss/scarlet/p/a9/k/27',
    'boss/scarlet/shield/pip', 'char/arlecchino/def', 'char/cd_cut', 'char/clorinde/auto_tick', 'char/clorinde/def',
    'char/lumine/def', 'char/motion/guard', 'char/navia/def', 'char/nefer/def', 'char/ronova/def', 'char/skirk/def',
    'cm/hit_pl', 'cm/hit_pl2', 'cm/pj/cb_boom', 'cm/pj/ic_boom', 'cm/sh/rcontact', 'combat/atkblock_manage',
    'combat/rclick_do', 'element/on_player_hurt', 'engravings/dash/regen', 'engravings/register', 'engravings/scan',
    'engravings/scan_more', 'items/epic/crane_feather/def', 'items/epic/lifeline/def', 'items/hook/on_basic_attack',
    'items/hook/on_dash', 'items/hook/on_dash_move', 'items/hook/on_parry', 'items/hook/on_parry_press',
    'items/hook/on_pdodge', 'items/hook/tick_player', 'items/legendary/pain_despair/def',
    'items/legendary/sword_kirion/def', 'items/mythic/sword_hwamu/def', 'items/proc/hw_ctr', 'items/proc/hw_ctr_q',
    'items/proc/hw_dash', 'items/proc/hw_due', 'items/proc/hw_reset', 'items/proc/kslash_burst',
    'items/proc/lifeline_fire', 'items/rare/kinetic_scale/def', 'items/tune/b10', 'items/tune/b7', 'load',
    'lobby/tut/s1', 'mboss/cproto/test/help', 'mboss/fight_vars', 'mboss/hurt', 'mboss/hurt_bol', 'mboss/hurt_ctx',
    'mboss/hurt_dodge', 'mboss/hurt_nd', 'mboss/hz/disc', 'mboss/hz/full', 'mboss/hz/hurt', 'mboss/hz/hurt_pm',
    'mboss/hz/init', 'mboss/hz/line', 'mboss/hz/near', 'mboss/hz/np_def', 'mboss/hz/ring', 'mboss/hz/sector',
    'mboss/init', 'mboss/near_all', 'mboss/np_glint', 'mboss/opts_reset', 'mboss/pj/hit', 'mboss/pj/launch',
    'mboss/pj/near', 'mboss/pl_dot', 'mboss/uninstall', 'player/dash', 'player/dash_fail', 'player/dash_go',
    'player/dash_iframe', 'player/dash_move_tick', 'player/dash_refill', 'player/dash_regen', 'player/dash_sub',
    'player/dash_up_x', 'player/f_key', 'player/hotbar/fix_attack', 'player/hotbar/tick', 'player/hud/build',
    'player/hud/build_slot', 'player/hud/part', 'player/hud/setup', 'player/hud/tick', 'player/init',
    'player/knockback/start', 'player/nudge', 'player/step_move_tick', 'player/swing/tick', 'player/take_damage',
    'player/tick', 'tick', 'uninstall', 'view/av_tick', 'view/dash_dir', 'view/move', 'view/ride_tick')
ALLOW[LANE_C] = ([F + f'{n}.mcfunction' for n in _LANE_C_FN]
                 + [F + r'player/def/.+\.mcfunction', F + r'char/motion/clips/(?:arle|skirk|navia)/guard/.+\.mcfunction',
                    F + r'char/motion/(?:arle_fx|skirk_fx|navia_fx|events/arle|events/skirk|events/navia)/guard\.mcfunction',
                    'items.md'])
# 11-10 combat overhaul, lane B (wip/combat-bal; tools/dev/plan/combat/b_progress.md): the balance gauge and groggy —
# the generated rlk:bal/** (tools/build_balance.py), the boss modules' balance hooks (mboss_lib.BAL_HOOKS) and the lines that
# call / refill it (their own groggies), the mob / cm / combat hook lines, the cm rig ticks' groggy branch, Raiden's
# balance stun, the boss bars' pip row. It removes nothing.
LANE_B = 'combat overhaul B (11-10): balance gauge / groggy'
ALLOW[LANE_B] = (
    [F + r'bal/.+', F + r'(?:mboss|boss)/[a-z]+/bal_(?:ok|on|tick|off)\.mcfunction', F + r'cm/[a-z]{2}/rig/tick\.mcfunction']
    + [F + f'{n}.mcfunction' for n in (
        'mob/setup', 'mob/tick', 'mob/hb_cleanup', 'cm/tick', 'cm/sb/tick', 'combat/apply', 'combat/apply_mods',
        'combat/clear_atkflags', 'char/after_hit', 'char/lumine/jav_spawn', 'char/lumine/jav_hit', 'items/hook/burst_dmg',
        'element/frz_end', 'mboss/bars', 'mboss/guardian/groggy/begin', 'mboss/butterfly/groggy/begin',
        'mboss/fieldgen/groggy/begin', 'boss/arlecchino/core/stun_start', 'boss/arlecchino/hud/bar_stun',
        'boss/tachy/el/backfire', 'boss/tachy/mantle/break', 'boss/raiden/bars', 'boss/raiden/tick',
        'boss/raiden/exhausted_start', 'boss/raiden/sg/stun_begin', 'boss/raiden/sg/stun_tick')])
# 11-11 홍련 rebuild, lane H2 (wip/combat-hr2; tools/dev/plan/combat/hr2_progress.md): the cinematic lock FN-cam — the generated
# F:mboss/cam/** and its request lines in the framework's shared files (tools/build_mboss_core.py), rlk:tick's hold / release
# lines, view/tick's guard, lvup/tick's held-sneak line; the RIGLIB look target changes only her own rig (F:boss/scarlet/**)
LANE_H2 = '홍련 rebuild H2 (11-11): the cinematic lock FN-cam'
ALLOW[LANE_H2] = ([F + r'mboss/cam/.+\.mcfunction']
                  + [F + f'{n}.mcfunction' for n in ('mboss/main', 'mboss/cleanup_fight', 'mboss/init', 'mboss/uninstall', 'tick',
                                                     'view/tick', 'lvup/tick')])
# 11-11 홍련 rebuild, lane H3 (wip/combat-hr3; tools/dev/plan/combat/h3_progress.md): the cutscene actor — the generated
# rlk:char/cine/** and its manifest (tools/build_player_cine.mjs, run by build_player_rig.mjs). It changes and removes nothing.
LANE_H3 = 'scarlet rebuild H3 (11-11): the cutscene actor'
ALLOW[LANE_H3] = [F + r'char/cine/.+', r'tools/player_motion/cine/manifest\.json']
# groups whose files may also be gone (removed on purpose; every other gone file fails)
ALLOW_GONE = {LANE_R,                               # lane R's removals
              LANE_C,                               # lane C: the dash charges / gauge / i-frames, hurt_nd, hw_dash
              'combat P late-game lag (11-10)'}     # engravings/info_pass(_one), items/scan_add: replaced by B3 / B4
PATS = [(grp, re.compile(p)) for grp, ps in ALLOW.items() for p in ps]


def in_scope(rel):
    return (rel.startswith('data/') or rel in ('items.md', 'pack.mcmeta') or rel == 'tools/player_motion/compiled_audio.json'
            or (rel.startswith('tools/') and not rel.startswith('tools/dev/') and 'manifest' in rel.rsplit('/', 1)[-1]
                and rel.endswith('.json')))


def allowed(rel, gone=False):
    """The first group that allows rel; for a gone file the first such group in ALLOW_GONE (a path several groups own, e.g.
    player/dash_iframe of SR and lane C, passes as gone when one of them may remove it)."""
    if gone:
        g = next((grp for grp, p in PATS if grp in ALLOW_GONE and p.fullmatch(rel)), None)
        if g:
            return g
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
            g = allowed(rel, gone=kind == 'gone')
            if g and (kind != 'gone' or g in ALLOW_GONE):
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
