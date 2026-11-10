#!/usr/bin/env python3
"""test_rm.py: the combat overhaul's lane R (removals) against one datapack root (read only).

    python3 test_rm.py <datapack root> [section ...]        sections: static yoi view picksub (default: all)

  static  요이미야 / the bow are gone (files, calls, objectives, the generated px/db row, the codex label), the projectile
          frame that 로노바 / 클로린드 use is kept and serves only their kinds, plain F (player/f_key) no longer toggles a
          bow aim
  yoi     the saved-world migration in the real pack (lib/psim.py runs rlk:load and rlk:player/tick): a world saved as
          요이미야 loads as 루미네 (current character and start_char), her card leaves the pending picks (rlk:lvpick choices)
          and the drop queue (dropq), and the player who joins after the restart gets 루미네's weapon (the old bow item
          gone), the bow-aim modifier removed, her arrows killed, once; a world saved as another
          character only loses her card from the lists
  view    the F5 view is the only view: the mode switch, the shoulder camera, the lobby 「시점」 button and its set files are
          gone, the lobby rebuilds (built 12), #on view 1 / #vmode view 2 stay as load's constants for the generated readers
          (mboss/guardian/p/pull/scr_end), no hand file branches on them any more; a world saved in first person (#on 0) or
          the shoulder view (#vmode 1) loads into F5 (the old camera storage removed) and its player's next view ticks take
          the avatar path (fresh -> spawn, rlk_body moves off the player, ride_tick); developer mode keeps view/fps_tick
  picksub 「고를 아이템 N개 …」 (lvup/pick_sub, the real file) never shows in combat: room combat (#active room 1 and
          #combat room 1..) or a live boss engine (#mbLive mb 1); the line on screen goes at once (subtitle "", the F5
          crosshair title stays), it comes back within 20 ticks after the fight, a level-up during the fight shows nothing
          until it ends, a stale #combat with #active 0 does not hide it, and the old rules hold (pkMode, dead, ttlT)

Harness: lib/psim.py + lib/mcsim.py = the research harness of the overhaul (tools/dev/plan/combat/perf_harness, mcsim =
ar/tests/lib/mcsim.py with unset source scores read as 0), vendored so later edits there cannot move this suite. Prints
one line per check; exit 1 on any failure. Run it from a copy outside the datapack (tools/dev/sim/README.md 1).
"""
import copy
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
from psim import PSim, Ent, Ctx, pctx, snbt_parse  # noqa: E402

ARGS = [a for a in sys.argv[1:] if not a.startswith('-')]
DP = Path(ARGS[0]).resolve()
ONLY = set(ARGS[1:])
FN = DP / 'data/rlk/function'
FAILS = []
NOK = 0


def ck(name, ok, info=''):
    global NOK
    if ok:
        NOK += 1
        print(f'ok   {name}')
    else:
        FAILS.append(name)
        print(f'FAIL {name}' + (f'  -- {info}' if info != '' else ''))


def rd(rel):
    p = FN / f'{rel}.mcfunction'
    return p.read_text(encoding='utf-8') if p.exists() else None


def code_lines(text):
    return [l for l in (text or '').split('\n') if l.strip() and not l.lstrip().startswith('#')]


def all_fn():
    return {p.relative_to(FN).as_posix()[:-len('.mcfunction')]: p.read_text(encoding='utf-8') for p in FN.rglob('*.mcfunction')}


# ================================================================================================== static
BOW_ONLY = ('na', 'na_shot', 'flurry_fire', 'queue_fire', 'queue_tick', 'rdash', 'release', 'shot_aim', 'shot_full', 'spawn',
            'stage1', 'start', 'tick', 'toggle', 'charge_tick', 'av_pull', 'hand_pull', 'cancel', 'arrow_trail')
KEPT = ('arrow_tick', 'arrow_step', 'arrow_hit', 'arrow_end', 'arrow_home', 'assist', 'calc')
GONE_OBJ = ('bowT', 'bowGap', 'bowSeen', 'bowUse', 'bowRc', 'bowCd', 'bowQ', 'bowQc', 'bowQo', 'bowF', 'bowK', 'bowSt', 'bowPm',
            'yoiSk', 'yoiPcCd', 'yoiPcN', 'yoiP', 'yoiPT', 'aurEnd')


def t_static():
    fns = all_fn()
    ck('static: char/yoimiya/** is gone', not any(k.startswith('char/yoimiya/') for k in fns))
    ck('static: the bow-only files of char/bow/ are gone (19, arrow_trail included)', not [n for n in BOW_ONLY if f'char/bow/{n}' in fns],
       [n for n in BOW_ONLY if f'char/bow/{n}' in fns])
    ck('static: the projectile frame for 로노바 / 클로린드 is kept (char/bow/arrow_* · assist · calc)', all(f'char/bow/{n}' in fns for n in KEPT))
    ck('static: the bow weapon item (char/weapon_item_bow) is gone', 'char/weapon_item_bow' not in fns)
    gone_calls = re.compile(r'rlk:char/yoimiya/|rlk:char/bow/(?:' + '|'.join(BOW_ONLY) + r')\b|rlk:char/weapon_item_bow')
    bad = sorted({k for k, v in fns.items() if gone_calls.search('\n'.join(code_lines(v)))})
    ck('static: no function calls a deleted bow / 요이미야 function', not bad, bad)
    obj = re.compile(r'\b(?:' + '|'.join(GONE_OBJ) + r')\b|#bowChg|#bowAim|#bowFull|#bowSlow|#yoi[A-Z]')
    bad = sorted({k for k, v in fns.items() if k != 'uninstall' and obj.search('\n'.join(code_lines(v)))})
    ck('static: no bow / 요이미야 objective or constant outside uninstall (kept there for old worlds)', not bad, bad)
    ck('static: load creates none of them any more',
       not [o for o in GONE_OBJ if f'scoreboard objectives add {o} ' in fns['load']])
    ck('static: the projectile objectives 로노바 uses stay (aKind aEl aSub aLife aIcd)',
       all(f'scoreboard objectives add {o} dummy' in fns['load'] for o in ('aKind', 'aEl', 'aSub', 'aLife', 'aIcd')))
    ck('static: no #wType 2 / #charN 2 branch is left',
       not [k for k, v in fns.items() if re.search(r'#(?:wType|charN) tmp matches 2(?:\.\.)?(?:\s|$)', '\n'.join(code_lines(v)))])
    ck('static: char/setup no longer registers her; char/reg_items has no char_yoimiya (pool, codex list)',
       'yoimiya/def' not in fns['char/setup'] and 'yoimiya' not in fns['char/reg_items'])
    ck('static: the codex label lab.char_yoimiya is gone', 'char_yoimiya' not in fns['codex/labels'])
    ck('static: the generated px/db has no aurEnd row and px/db/aurend is gone (generator row removed, core regenerated)',
       'aurEnd' not in fns['mboss/px/db'] and 'mboss/px/db/aurend' not in fns)
    core = (DP / 'tools/build_mboss_core.py').read_text(encoding='utf-8')
    ck('static: build_mboss_core.py PX_DB has no aurEnd row', "'aurEnd'" not in core)
    # the kept frame serves only 로노바's kinds (7 orb, 8 echo)
    ah = code_lines(fns['char/bow/arrow_hit'])
    ck('static: arrow_hit sends kinds 7..8 to char/ronova/proj_hit and kills anything else',
       ah == ['scoreboard players set #jend tmp 1',
              'execute if score @s aKind matches 7..8 run return run function rlk:char/ronova/proj_hit', 'kill @s'], ah)
    at = '\n'.join(code_lines(fns['char/bow/arrow_tick']) + code_lines(fns['char/bow/arrow_step']) + code_lines(fns['char/bow/arrow_end']))
    ck('static: arrow_tick / step / end have no bow kinds (1-6) and no trail call',
       not re.search(r'aKind matches [1-6](?:\.\.[1-6])?\b(?!\.\.)', at) and 'arrow_trail' not in at, re.findall(r'aKind matches \S+', at))
    ck('static: tick still flies every rlk_arrow through char/bow/arrow_tick',
       'execute as @e[tag=rlk_arrow] at @s run function rlk:char/bow/arrow_tick' in fns['tick'])
    ck('static: player_init still kills leftover rlk_arrow projectiles (로노바)', 'kill @e[tag=rlk_arrow]' in code_lines(fns['char/player_init']))
    fk = code_lines(fns['player/f_key'])
    # lane C (11-10) made plain F the parry press: its guards, then player/def/press (test_cb input)
    ck('static: plain F (player/f_key) is no bow-aim toggle any more: its guards, then the parry press (lane C)',
       not [l for l in fk if 'bow' in l or 'wType' in l] and fk[-1] == 'function rlk:player/def/press', fk)
    ck('static: the melee normal attack is #wType 1 (combat/on_attack)', any('if score #wType tmp matches 1 unless score #clShoot' in l
                                                                             for l in code_lines(fns['combat/on_attack'])))
    rc = code_lines(fns['combat/rclick_do'])
    ck('static: right click with the weapon = dash for every character (combat/rclick_do)',
       any(l.startswith('execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] at @e[tag=rlk_body,limit=1] run function rlk:player/dash') for l in rc))
    ck('static: the hotbar weapon is always char/weapon_item (player/hotbar/fix_attack)',
       'function rlk:char/weapon_item with storage rlk:chars cur.weapon' in code_lines(fns['player/hotbar/fix_attack']))
    hw = fns['view/hand_wrap'] + fns['view/av_unwrap']
    ck('static: the hand wraps have no bow models', 'bow' not in hw)
    ck('static: the migration exists and is wired (char/setup -> migrate_yoi_load; player/tick -> migrate_yoi)',
       'function rlk:char/migrate_yoi_load' in fns['char/setup']
       and 'execute if data storage rlk:mig {yoi:1b} run function rlk:char/migrate_yoi' in fns['player/tick'])
    st = code_lines(fns['char/setup'])
    ck('static: the migration runs before load_cur reads the registry',
       st.index('function rlk:char/migrate_yoi_load') < st.index('function rlk:char/load_cur with storage rlk:chars cur'))


# ================================================================================================== yoi
class LSim(PSim):
    """PSim + a log of the commands mcsim ignores that the migration must run (attribute, tellraw, scoreboard reset)."""
    def __init__(self, root):
        super().__init__(root)
        self.log = []

    def cmd(self, t, ctx):
        if t[0] in ('attribute', 'tellraw', 'title'):
            self.log.append((self.t, t[0], ctx.ex.id if ctx.ex is not None else None, ' '.join(t[1:])))
        if t[0] == 'scoreboard' and len(t) > 4 and t[1] == 'players' and t[2] == 'reset':
            self.log.append((self.t, 'reset', None, ' '.join(t[3:])))
        return super().cmd(t, ctx)


OLD_YOI = ('{id:"yoimiya",n:2,elem:1,na1:60,na2:105,aim:85,full:220,weaponType:"bow",itemId:"char_yoimiya",'
           'weapon:{item:"minecraft:bow",name:"활",lore:[],model:"minecraft:bow"},skill:{cd:300},burst:{cd:300,cost:60},'
           'info:{name:"요이미야",prof:{model:"slim",texture:"rlk:skin/yoimiya"}}}')
BOW_ITEM = {'id': 'minecraft:stick', 'count': 1,
            'c': {'minecraft:item_name': {'text': '활'}, 'minecraft:item_model': 'minecraft:bow',
                  'minecraft:custom_data': {'rlk_ui': {'role': 'attack'}}}}


def lworld():
    s = LSim(FN)
    pl = Ent('player', (0.5, 64.0, 0.5), (0.0, 0.0), ['player', 'rlk_body'])
    s.ents.append(pl)
    s.player = pl
    s.call('rlk:load', Ctx(None, (0, 0, 0), (0, 0)))
    for _ in range(5):
        ptick(s)
    return s, pl


def ptick(s):
    s.t += 1
    s.call('rlk:player/tick', pctx(s))


def restart(s, pl):
    """The server stops and starts again: the player is offline while rlk:load runs, then joins."""
    s.ents.remove(pl)
    s.player = None
    s.call('rlk:load', Ctx(None, (0, 0, 0), (0, 0)))
    s.ents.append(pl)
    s.player = pl


def arrow(s, kind):
    e = Ent('block_display', (3.5, 65.0, 0.5), (0.0, 0.0), ['rlk_arrow'])
    s.ents.append(e)
    s.setsc(('e', e.id), 'aKind', kind)
    return e


def t_yoi():
    # ---- a world saved while playing 요이미야 (state written as the old pack left it), then a server restart
    s, pl = lworld()
    P = ('e', pl.id)
    lum = copy.deepcopy(s.storage['rlk:chars']['registry']['lumine'])
    s.storage['rlk:chars']['cur'] = snbt_parse(OLD_YOI)
    s.storage.setdefault('rlk:config', {})['start_char'] = 'yoimiya'
    s.storage.setdefault('rlk:lvpick', {})['choices'] = ['whetstone', 'char_yoimiya', 'hood']
    s.storage['rlk:lvpick']['dropq'] = ['char_yoimiya', 'pebble']
    s.player.data['inv']['hotbar.0'] = copy.deepcopy(BOW_ITEM)
    a4, a7 = arrow(s, 4), arrow(s, 7)
    restart(s, pl)
    cur = s.storage['rlk:chars']['cur']
    ck('yoi: after the restart\'s load the current character is 루미네 (the registry compound, not the old 요이미야 one)',
       cur.get('id') == 'lumine' and cur.get('n') == lum.get('n') and 'weaponType' in cur and cur['weaponType'] != 'bow', cur.get('id'))
    ck('yoi: #charN 1 · #wType 1 (no handler-less 2 left)', s.sc('#charN', 'tmp') == 1 and s.sc('#wType', 'tmp') == 1,
       (s.sc('#charN', 'tmp'), s.sc('#wType', 'tmp')))
    ck('yoi: start_char 요이미야 -> 루미네', s.storage['rlk:config'].get('start_char') == 'lumine', s.storage['rlk:config'].get('start_char'))
    lv = s.storage['rlk:lvpick']
    ck('yoi: her card leaves the pending picks, the others stay in order', lv.get('choices') == ['whetstone', 'hood'], lv.get('choices'))
    ck('yoi: ... and the drop queue', lv.get('dropq') == ['pebble'], lv.get('dropq'))
    ck('yoi: the player-side flag waits for the player (rlk:mig yoi 1b)', s.storage.get('rlk:mig', {}).get('yoi') == 1)
    ck('yoi: load could not clear the old bow item (the player was offline)',
       s.player.data['inv'].get('hotbar.0', {}).get('c', {}).get('minecraft:item_model') == 'minecraft:bow')
    n0 = len(s.log)
    ptick(s)
    ptick(s)
    hb = s.player.data['inv'].get('hotbar.0') or {}
    ck('yoi: the joined player\'s first tick re-selects 루미네: hotbar.0 = 루미네\'s weapon (the bow item is gone)',
       hb.get('c', {}).get('minecraft:item_model') == lum['weapon'].get('model')
       and hb.get('c', {}).get('minecraft:custom_data', {}).get('rlk_ui', {}).get('role') == 'attack'
       and not [k for k, v in s.player.data['inv'].items() if v and v.get('c', {}).get('minecraft:item_model') == 'minecraft:bow'],
       hb)
    ck('yoi: the flag is spent (rlk:mig yoi removed)', 'yoi' not in s.storage.get('rlk:mig', {}))
    lg = s.log[n0:]
    ck('yoi: the bow-aim modifier is removed from the player',
       any(k == 'attribute' and who == pl.id and 'movement_speed modifier remove rlk:bow_aim' in a for _, k, who, a in lg))
    ck('yoi: the sidebar lines of her passives are reset (염초정화 · 소매불 · 염초화살)',
       all(any(k == 'reset' and a == f'{n} stacks' for _, k, _, a in lg) for n in ('염초정화', '소매불', '염초화살')))
    ck('yoi: the select message names 루미네 (the player sees why the character changed)',
       any(k == 'tellraw' and who == pl.id and '선택' in a for _, k, who, a in lg))
    ck('yoi: her leftover arrows are gone (the re-select\'s player_init kills every rlk_arrow, as any character change)',
       a4 not in s.ents and a7 not in s.ents)
    ck('yoi: 루미네 stays after more ticks', s.storage['rlk:chars']['cur'].get('id') == 'lumine' and s.sc('#charN', 'tmp') == 1)
    # a dropped card that survived load (a chunk that loaded only when the player came back) is cleared with its group
    s2, pl2 = lworld()
    s2.storage['rlk:chars']['cur'] = snbt_parse(OLD_YOI)
    restart(s2, pl2)
    it = Ent('item', (2.5, 64.0, 0.5), (0.0, 0.0), ['rlk_ditem', 'rlk_dgrp'])
    it.data['inv'] = {'contents': {'id': 'minecraft:player_head', 'count': 1,
                                   'c': {'minecraft:custom_data': {'rlk_ditem': {'id': 'char_yoimiya'}}}}}
    lbl = Ent('text_display', (2.5, 65.0, 0.5), (0.0, 0.0), ['rlk_dlbl'])
    keep = Ent('item', (4.5, 64.0, 0.5), (0.0, 0.0), ['rlk_ditem', 'rlk_dgrp'])
    keep.data['inv'] = {'contents': {'id': 'minecraft:flint', 'count': 1, 'c': {'minecraft:custom_data': {'rlk_ditem': {'id': 'whetstone'}}}}}
    for e, g in ((it, 41), (lbl, 41), (keep, 42)):
        s2.ents.append(e)
        s2.setsc(('e', e.id), 'dgid', g)
    s2.storage.setdefault('rlk:ditems', {}).setdefault('records', {})['k41'] = {'id': 'char_yoimiya'}
    ptick(s2)
    ck('yoi: a ground card of hers is removed with its group and record; other drops stay',
       it not in s2.ents and lbl not in s2.ents and keep in s2.ents and 'k41' not in s2.storage['rlk:ditems']['records'])
    # ---- once only: the next restart changes nothing
    s3, pl3 = lworld()
    s3.storage['rlk:chars']['cur'] = snbt_parse(OLD_YOI)
    restart(s3, pl3)
    ptick(s3)
    restart(s3, pl3)
    n0 = len(s3.log)
    ptick(s3)
    ck('yoi: once only: the next restart sets no flag and re-selects nothing',
       'yoi' not in s3.storage.get('rlk:mig', {}) and not [1 for _, k, _, a in s3.log[n0:] if k == 'attribute' and 'bow_aim' in a]
       and not [1 for _, k, _, a in s3.log[n0:] if k == 'tellraw' and '선택' in a])
    # ---- a world saved as another character: only the lists change
    s4, pl4 = lworld()
    s4.call('rlk:char/select', pctx(s4), {'id': 'skirk'})
    ptick(s4)
    s4.storage['rlk:lvpick']['choices'] = ['char_yoimiya', 'char_nefer']
    s4.storage['rlk:lvpick']['dropq'] = []
    restart(s4, pl4)
    n0 = len(s4.log)
    ptick(s4)
    ck('yoi: a world saved as 스커크 stays 스커크 (no flag, no re-select); her card leaves its picks',
       s4.storage['rlk:chars']['cur'].get('id') == 'skirk' and 'yoi' not in s4.storage.get('rlk:mig', {})
       and s4.storage['rlk:lvpick']['choices'] == ['char_nefer'] and s4.storage['rlk:lvpick']['dropq'] == []
       and not [1 for _, k, _, a in s4.log[n0:] if k == 'tellraw' and '선택' in a], (s4.storage['rlk:chars']['cur'].get('id'),
                                                                                     s4.storage['rlk:lvpick']))
    ck('yoi: the level-up character pool has no 요이미야 (new picks cannot offer her)',
       not [c for c in s4.storage['rlk:chars']['pool'] if c.get('id') == 'yoimiya'] and 'yoimiya' not in s4.storage['rlk:chars']['registry']
       and 'char_yoimiya' not in s4.storage['rlk:codex']['chars'])
    errs = [k for k in list(s.errors) + list(s4.errors) if 'migrate_yoi' in k[0]]
    ck('yoi: the migration functions ran without a sim error', not errs, errs)


# ================================================================================================== view
VIEW_GONE = ('mode', 'mode_do', 'mode_help', 'on', 'off', 'ride', 'rot', 'rot_lead', 'cam_go', 'cam_step', 'cam_put', 'cam_y',
             'cam_calc', 'dur_set', 'dur_set2', 'set', 'tune', 'tune_apply')


def t_view():
    fns = all_fn()
    ck('view: the mode switch and the shoulder camera are gone (18 view files)', not [n for n in VIEW_GONE if f'view/{n}' in fns],
       [n for n in VIEW_GONE if f'view/{n}' in fns])
    ck('view: the lobby set files of the view / side / smooth / lead buttons are gone (s20 s22 s24 s25)',
       not [n for n in ('s20', 's22', 's24', 's25') if f'lobby/set/{n}' in fns])
    gone = re.compile(r'rlk:view/(?:' + '|'.join(VIEW_GONE) + r')\b|rlk:lobby/set/s2[0245]\b|rlk_camv')
    bad = sorted({k for k, v in fns.items() if gone.search('\n'.join(code_lines(v)))})
    ck('view: nothing calls them or touches the camera mount rlk_camv', not bad, bad)
    rd_ = re.compile(r'#on view|#vmode view')
    readers = sorted(k for k, v in fns.items() if rd_.search('\n'.join(code_lines(v))))
    ck('view: #on view / #vmode view are read only by the generated guardian line and set only in load',
       readers == ['load', 'mboss/guardian/p/pull/scr_end'], readers)
    ld = code_lines(fns['load'])
    ck('view: load sets them as constants (#on view 1, #vmode view 2; no 0..1 keep of a saved first-person 0)',
       'scoreboard players set #on view 1' in ld and 'scoreboard players set #vmode view 2' in ld
       and not [l for l in ld if '#on view' in l and l != 'scoreboard players set #on view 1'], [l for l in ld if '#on view' in l])
    ck('view: the generated reader still needs both values (no regeneration)',
       'if score #on view matches 1 if score #vmode view matches 2' in fns['mboss/guardian/p/pull/scr_end'])
    ck('view: load drops the shoulder camera storage (cam, opt, optv, st, pr)',
       all(f'data remove storage rlk:view {k}' in ld for k in ('cam', 'opt', 'optv', 'st', 'pr')))
    vt = code_lines(fns['view/tick'])
    ck('view: view/tick: developer mode -> view/fps_tick, everything else the avatar and ride_tick (no rot)',
       'execute unless score @s devMode matches 1 run scoreboard players set #eff view 1' in vt
       and 'execute if score #eff view matches 0 run return run function rlk:view/fps_tick' in vt
       and 'function rlk:view/ride_tick' in vt and not [l for l in vt if 'view/rot' in l], vt)
    lb = fns['lobby/build']
    ck('view: the lobby has no 「시점」 button (k 20) and the settings door says 카메라',
       'name:"시점"' not in lb and 'k:20' not in lb and 'name:"시작 전 설정",desc:"카메라"' in lb)
    ck('view: the lobby build version is bumped to 12 (build + tick), so saved worlds rebuild without the button',
       'data modify storage rlk:lobby built set value 12' in lb and 'unless data storage rlk:lobby {built:12}' in fns['lobby/tick'])
    ck('view: lobby/act has no handlers 20 / 22 / 24 / 25; the labels have no lk20 / 22 / 24 / 25',
       not re.search(r'matches 2[0245] ', fns['lobby/act']) and not re.search(r'rlk_lk2[0245]', fns['lobby/set/labels']))
    ck('view: lobby/set/cam sets only the F5 seat (ride.d / ride.s)',
       'rlk:view cam' not in fns['lobby/set/cam'] and 'ride.d' in fns['lobby/set/cam'] and 'ride.s' in fns['lobby/set/cam'])
    rays = code_lines(fns['view/rays'])
    ck('view: the UI ray lengths are the third-person ones, unconditionally',
       rays == ['scoreboard players set #rObj view 27', 'scoreboard players set #rDit view 21', 'scoreboard players set #rDitB view 23',
                'scoreboard players set #rShop view 28', 'scoreboard players set #rShopB view 27'], rays)
    ps = [l for l in code_lines(fns['lvup/pick_sub']) if 'title @s subtitle' in l and '고를 아이템' in l]
    ck('view: the pick subtitle has one form (웅크리기), no Shift + F variant',
       len(ps) == 1 and '웅크리기(Shift)' in ps[0] and 'Shift + F' not in ps[0], ps)
    vis = re.compile(r'"[^"]*(?:1인칭|숄더뷰)[^"]*"')
    bad = sorted({k for k, v in fns.items() if not k.startswith(('boss/', 'mboss/', 'char/motion/'))
                  and vis.search('\n'.join(code_lines(v)))})
    ck('view: no player-facing text of the hand files names 1인칭 / 숄더뷰', not bad, bad)
    # ---- a world saved in first person / the shoulder view loads into F5
    for label, on, vm in (('first person', 0, 2), ('the shoulder view', 1, 1)):
        s, pl = lworld()
        s.setsc('#on', 'view', on)
        s.setsc('#vmode', 'view', vm)
        s.storage.setdefault('rlk:view', {}).update({'cam': {'right': 0.9, 'up': 0.3, 'back': 3.3}, 'opt': {'smooth': 2, 'lead': 0},
                                                     'optv': 2, 'st': {'x': 1}, 'pr': {'d': 2}})
        restart(s, pl)
        vw = s.storage['rlk:view']
        ck(f'view: a world saved in {label} loads with #on view 1 · #vmode view 2 and without the shoulder camera storage',
           s.sc('#on', 'view') == 1 and s.sc('#vmode', 'view') == 2 and not [k for k in ('cam', 'opt', 'optv', 'st', 'pr') if k in vw]
           and 'ride' in vw, (s.sc('#on', 'view'), s.sc('#vmode', 'view'), sorted(vw)))
        # its player's next view ticks: the avatar path (the avatar / seat builders are stubbed: no world in the sim)
        if label == 'first person':
            pl.tags.add('rlk_body')
            for f in ('rlk:view/spawn', 'rlk:view/ride_tick', 'rlk:view/move', 'rlk:view/av_tick', 'rlk:view/aim', 'rlk:view/slow',
                      'rlk:view/sprint_fov', 'rlk:view/mob_aggro', 'rlk:view/burst_camera_tick', 'rlk:view/menu_do',
                      'rlk:view/teardown'):
                s.cache[f] = []                    # empty bodies (PSim.stub would hide the calls from ncall)
            P = ('e', pl.id)
            for o, v in (('rdCam', 0), ('vMap', 0), ('devMode', 0), ('dead', 0), ('pkMode', 0), ('rlkMenu', 0)):
                s.setsc(P, o, v)
            c0 = dict(s.ncall)
            for _ in range(2):
                s.t += 1
                s.call('rlk:view/tick', pctx(s))
            d = {k: s.ncall[k] - c0.get(k, 0) for k in ('rlk:view/fresh', 'rlk:view/spawn', 'rlk:view/ride_tick', 'rlk:view/fps_tick')}
            ck('view: ... its player\'s next view ticks: fresh once, then the avatar path (spawn, ride_tick), never fps_tick; '
               'rlk_body leaves the player', d['rlk:view/fresh'] == 1 and d['rlk:view/spawn'] >= 1 and d['rlk:view/ride_tick'] >= 1
               and d['rlk:view/fps_tick'] == 0 and 'rlk_body' not in pl.tags, (d, sorted(pl.tags)))
            s.setsc(P, 'devMode', 1)
            c0 = dict(s.ncall)
            s.t += 1
            s.call('rlk:view/tick', pctx(s))
            ck('view: developer mode still takes the no-avatar path (view/fps_tick, the player is the body)',
               s.ncall['rlk:view/fps_tick'] - c0.get('rlk:view/fps_tick', 0) == 1 and 'rlk_body' in pl.tags
               and s.ncall['rlk:view/ride_tick'] - c0.get('rlk:view/ride_tick', 0) == 0)


# ================================================================================================== picksub
def pick_run(script, n=130, pending=2, base=None):
    """The real lvup/pick_sub (+ the real view/ttl_blank) once per tick for a player with pick(s) waiting. script =
    [(tick, holder, objective, value)], holder '@p' = the player. Returns {tick: [title args]} of the player."""
    s, pl = lworld()
    P = ('e', pl.id)
    for o, v in (('pkPending', pending), ('pkMode', 0), ('dead', 0), ('ttlT', 0), ('pkSubT', 0), ('devMode', 0)):
        s.setsc(P, o, v)
    for k, o, v in (base or (('#active', 'room', 1), ('#combat', 'room', 0), ('#mbLive', 'mb', 0))):
        s.setsc(k, o, v)
    out = {}
    for tk in range(1, n + 1):
        s.t = tk
        for at, k, o, v in script:
            if at == tk:
                s.setsc(P if k == '@p' else k, o, v)
        n0 = len(s.log)
        s.call('rlk:lvup/pick_sub', pctx(s))
        out[tk] = [a for _, kind, who, a in s.log[n0:] if kind == 'title' and who == pl.id]
    return out


def subs(out, lo=1, hi=10 ** 6):
    return [tk for tk, ts in out.items() if lo <= tk <= hi and any('subtitle' in a and '고를 아이템' in a for a in ts)]


def t_picksub():
    out = pick_run([(30, '#combat', 'room', 3), (70, '#combat', 'room', 0), (90, '#mbLive', 'mb', 1), (110, '#mbLive', 'mb', 0)])
    s_all = subs(out)
    ck('picksub: out of combat it shows and is refreshed every 20 ticks (1, 21)', subs(out, 1, 29) == [1, 21], s_all)
    ck('picksub: never during room combat (#active room 1, #combat room 3: ticks 30-69)', not subs(out, 30, 69), s_all)
    ck('picksub: the line on screen goes at once when the fight starts (subtitle "" at 30, no title clear: the F5 crosshair stays)',
       any(a.strip() == '@s subtitle ""' for a in out[30]) and not [1 for tk in range(1, 131) for a in out[tk] if a.strip().endswith('clear')],
       out[30])
    ck('picksub: it comes back within 20 ticks after the fight (70-89)', bool(subs(out, 70, 89)), s_all)
    ck('picksub: never while a boss engine is live (#mbLive mb 1: ticks 90-109), even out of a room fight', not subs(out, 90, 109), s_all)
    ck('picksub: back after the boss engine stops (110-130)', bool(subs(out, 110, 130)), s_all)
    out2 = pick_run([(40, '@p', 'pkPending', 1), (80, '#combat', 'room', 0)], pending=0,
                    base=(('#active', 'room', 1), ('#combat', 'room', 5), ('#mbLive', 'mb', 0)))
    ck('picksub: a level-up during the fight (pkPending 0 -> 1 at 40) shows nothing until the fight ends (80), then it shows',
       not subs(out2, 1, 79) and bool(subs(out2, 80, 100)), subs(out2))
    out3 = pick_run([], base=(('#active', 'room', 0), ('#combat', 'room', 4), ('#mbLive', 'mb', 0)), n=30)
    ck('picksub: a stale #combat with #active room 0 (no room run) does not hide it', subs(out3) == [1, 21], subs(out3))
    out4 = pick_run([(10, '@p', 'pkMode', 1), (30, '@p', 'pkMode', 0), (50, '@p', 'dead', 1), (70, '@p', 'dead', 0),
                     (90, '@p', 'ttlT', 30)], n=125)
    ck('picksub: the old rules hold: nothing in the selection space (pkMode 10-29), while dead (50-69), under another title (ttlT)',
       not subs(out4, 10, 29) and not subs(out4, 50, 69) and not subs(out4, 90, 119) and bool(subs(out4, 30, 49))
       and bool(subs(out4, 70, 89)), subs(out4))
    fl = code_lines(rd('lvup/pick_sub'))
    ck('picksub: the gate reads the combat states the pack\'s refusals use (lvup/toggle: #active room 1 + #combat room 1..) and #mbLive',
       'execute if score #active room matches 1 if score #combat room matches 1.. run scoreboard players set #ps tmp 0' in fl
       and 'execute if score #mbLive mb matches 1 run scoreboard players set #ps tmp 0' in fl
       and 'if score #active room matches 1 if score #combat room matches 1..' in rd('lvup/toggle'))


SECTIONS = {'static': t_static, 'yoi': t_yoi, 'view': t_view, 'picksub': t_picksub}
for name, fn in SECTIONS.items():
    if not ONLY or name in ONLY:
        print(f'== {name}')
        fn()
print(f'test_rm: {NOK} ok, {len(FAILS)} failed')
if FAILS:
    print('FAILED: ' + '; '.join(FAILS))
    sys.exit(1)
print('ALL test_rm CHECKS PASSED')
