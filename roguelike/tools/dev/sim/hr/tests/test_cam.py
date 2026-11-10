#!/usr/bin/env python3
"""test_cam.py: the cinematic lock of the boss framework, FN-cam (홍련 rebuild, lane H2; hr_design.md §3.0 / §5.2 / §6.2,
hr_brief.md 「조작 잠금 · 카메라」): rlk:tick's hold / release lines, F:mboss/cam/**, view/tick's guard.

    python3 test_cam.py <datapack root> [section ...] [--base <commit>]

Run it from a copy outside the datapack (tools/dev/sim/README.md §1). It only reads the tree. World: hr/h2/camsim.py (the F5
view model, the spectator rules of the 26.3 server, rlk:tick's FN-cam lines after mboss/main); the fight is the special
prototype `spproto`, the "module" is camsim's stand-in request (s.cam_req: #mbCam / #mbCamId set in every module tick).

  static  the names of hr_design §5.2; rlk:tick: hold then release right after mboss/main, the two-player guard releases;
          view/tick: exactly one guard, after the per-tick housekeeping and before the body; lvup/tick: a held player's
          sneak press is no tap; mboss/main zeroes the request before the world tick; cleanup_fight releases first; init
          releases before the helper entities die; the stand = a marker armour stand (never a marker / display),
          camera_distance 0, rlk_mb_aux + rlk_pet; no negative literal, every function reference exists
  hold    the request -> spectator on the live stand from the same tick; `spectate` issued every tick; the other stand
          = a hard cut; view/tick rests; the player's server position follows the stand; the three game modes come back;
          the request stops -> released in that tick
  paths   every exit path from a held state leaves nothing behind (camsim.clean): the end, in the intro / fight / dying
          states; pause by death, Ronova's revive, the selection space; the body removed; /reload; relog; cleanup; abort;
          the kill (won: the player ends at the dungeon return point); uninstall; the two-player guard; a request that
          outlived its fight
  stand   the live stand killed: released at once, held again when the stands are back; the idle stand killed: nothing;
          sneaking: the game drops the camera every tick, the hold takes it back every tick, never released
  idem    release twice / on a player who is not held changes nothing (a creative player stays creative); a developer-mode
          player (no avatar) is never locked; hold with no stands never switches the game mode
  cost    commands per tick: the framework's share without a lock (+1 in mboss/main, +2 in rlk:tick) and while held
  ident   against the base commit (default: the merge base with origin/wip/combat): outside F:boss/scarlet/** and
          F:mboss/cam/** only the shared files change (mboss/{main,cleanup_fight,init,uninstall}, tick, view/tick,
          lvup/tick), each by added lines only, each added command a FN-cam line
"""
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
sys.path.insert(0, str(HERE.parent / 'h2'))
import hrsim as H  # noqa: E402
import camsim as CS  # noqa: E402
from mcsim import Ctx, split  # noqa: E402

ARGS = list(sys.argv[1:])
BASE = None
if '--base' in ARGS:
    i = ARGS.index('--base')
    BASE = ARGS[i + 1]
    del ARGS[i:i + 2]
DP = Path(ARGS[0]).resolve()
SECT = ARGS[1:]
F = DP / 'data/rlk/function'
ck = H.ck
C0 = H.C0
SID = 'spproto'


def want(name):
    return not SECT or name in SECT


def fn(rel):
    return (F / f'{rel}.mcfunction').read_text(encoding='utf-8').split('\n')


def cmds(rel):
    return [l for l in fn(rel) if l.strip() and not l.startswith('#')]


# ============================================================================================================ static
def static():
    sys.path.insert(0, str(DP / 'tools'))
    import mboss_lib as L
    ck('S1 names (hr_design §5.2)', (L.CAM_REQ, L.CAM_ID, L.CAM_TAGS, L.CAM_HOLD_TAG) ==
       (('#mbCam', 'mb'), ('#mbCamId', 'mb'), {1: 'rlk_mb_cam1', 2: 'rlk_mb_cam2'}, 'rlk_mb_camh')
       and L.cam_req(2) == ['scoreboard players set #mbCam mb 1', 'scoreboard players set #mbCamId mb 2']
       and L.cam('spawn') == 'function rlk:mboss/cam/spawn' and L.cam('kill') == 'function rlk:mboss/cam/kill'
       and L.CAM_EYE == 0.0)
    for f in ('spawn', 'hold', 'release', 'kill'):
        ck(f'S1 F:mboss/cam/{f} exists', (F / f'mboss/cam/{f}.mcfunction').exists())
    # rlk:tick
    t = fn('tick')
    c = [l for l in t if l.strip() and not l.startswith('#')]
    i = c.index('execute if score #mbLive mb matches 1 run function rlk:mboss/main')
    hold = 'execute if score #mbCam mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/cam/hold'
    rel = 'execute unless score #mbCam mb matches 1 as @a[tag=rlk_mb_camh] run function rlk:mboss/cam/release'
    ck('S2 rlk:tick: hold, then release, right after mboss/main', c[i + 1:i + 3] == [hold, rel], str(c[i + 1:i + 3]))
    ck('S2 rlk:tick: no other FN-cam command after mboss/main', CS.tick_cam_lines(DP) == [hold, rel])
    g = [k for k, l in enumerate(c) if 'pcount tmp matches 2..' in l]
    gl = [c[k] for k in g]
    r2 = 'execute if score #pcount tmp matches 2.. as @a[tag=rlk_mb_camh] run function rlk:mboss/cam/release'
    ck('S2 rlk:tick: the two-player guard releases before it drops the tags and returns',
       r2 in gl and gl.index(r2) < next(k for k, l in enumerate(gl) if 'remove player' in l), str(gl))
    ck('S2 rlk:tick: view/tick runs before mboss/main (a held tick rests the view from the next tick on)',
       c.index('execute as @a[tag=player] run function rlk:view/tick') < i)
    # view/tick
    v = cmds('view/tick')
    guard = 'execute if entity @s[tag=rlk_mb_camh] run return 0'
    gi = [k for k, l in enumerate(v) if 'rlk_mb_camh' in l]
    ck('S3 view/tick: exactly one guard line', len(gi) == 1 and v[gi[0]] == guard, str([v[k] for k in gi]))
    k = gi[0]
    before = ('vBig matches 1.. run scoreboard players remove @s vBig 1', 'function rlk:view/fresh', 'function rlk:view/burst_camera_tick')
    after = ('function rlk:view/map_tick', 'function rlk:view/fps_tick', 'function rlk:view/hold', 'function rlk:view/spawn',
             'function rlk:view/move', 'function rlk:view/aim', 'function rlk:view/ride_tick', 'tag @s remove rlk_body')
    pos = lambda frag: next(j for j, l in enumerate(v) if frag in l)  # noqa: E731
    ck('S3 view/tick: the guard after the housekeeping (vBig, fresh, the burst camera)', all(pos(b) < k for b in before))
    ck('S3 view/tick: the guard before the map, the developer / dead / selection branches and the body', all(pos(a) > k for a in after))
    # lvup/tick
    lv = cmds('lvup/tick')
    tap = next(j for j, l in enumerate(lv) if l.endswith('run function rlk:lvup/sneak_tap'))
    ln = [j for j, l in enumerate(lv) if 'rlk_mb_camh' in l]
    ck('S4 lvup/tick: a held player\'s sneak press is marked before the tap line (no selection-space deny while locked)',
       len(ln) == 1 and ln[0] < tap and lv[ln[0]] ==
       'execute if score #snk tmp matches 1 unless score @s vSnk matches 1 if entity @s[tag=rlk_mb_camh] unless score @s pkMode '
       'matches 1.. run scoreboard players set @s vSnk 1', str([lv[j] for j in ln]))
    # the framework's shared files
    m = cmds('mboss/main')
    ck('S5 mboss/main: the request is zeroed before the world tick',
       m.index('scoreboard players set #mbCam mb 0') < next(j for j, l in enumerate(m) if 'function rlk:mboss/world' in l))
    cf = cmds('mboss/cleanup_fight')
    ck('S5 cleanup_fight: a held player is released first, then the request ends',
       cf[0] == 'execute as @a[tag=rlk_mb_camh] run function rlk:mboss/cam/release' and cf[1] == 'scoreboard players set #mbCam mb 0'
       and 'mboss/d/cleanup' in cf[2], str(cf[:3]))
    ini = cmds('mboss/init')
    ri = ini.index('execute as @a[tag=rlk_mb_camh] run function rlk:mboss/cam/release')
    ck('S5 mboss/init (/reload): the request off, held players released before the helper entities die',
       'scoreboard players set #mbCam mb 0' in ini[:ri] and ri < ini.index('kill @e[tag=rlk_mb_aux]')
       and 'execute unless score #mbCamId mb matches 1..2 run scoreboard players set #mbCamId mb 1' in ini)
    un = cmds('mboss/uninstall')
    ck('S5 mboss/uninstall: cleanup first (it releases), the stored return point removed',
       un[0] == 'function rlk:mboss/cleanup' and 'data remove storage rlk:mboss camret' in un)
    # the stands
    sp = cmds('mboss/cam/spawn')
    ok = len(sp) == 2
    for n, l in zip((1, 2), sp):
        ok &= l.startswith(f'execute unless entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam{n},limit=1] run summon minecraft:armor_stand ~ ~ ~ ')
        nbt = l.split('~ ~ ~ ', 1)[1]
        ok &= all(x in nbt for x in ('Marker:1b', 'Invisible:1b', 'NoGravity:1b', 'Invulnerable:1b', 'Silent:1b',
                                     'attributes:[{id:"minecraft:camera_distance",base:0d}]'))
        ok &= re.search(r'Tags:\[([^\]]*)\]', nbt).group(1) == f'"rlk_room","rlk_mb_aux","rlk_pet","rlk_mb_cam","rlk_mb_cam{n}"'
    ck('S6 cam/spawn: two marker armour stands (spectatable, camera_distance 0), rlk_room rlk_mb_aux rlk_pet, idempotent', ok, str(sp))
    ck('S6 cam/kill removes both', cmds('mboss/cam/kill') == ['kill @e[type=minecraft:armor_stand,tag=rlk_mb_cam]'])
    h = cmds('mboss/cam/hold')
    ck('S6 cam/hold: spectate is the last command of both branches (issued every held tick)',
       h[-1] == 'spectate @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1]'
       and h[-2] == 'execute if score #mbCamId mb matches 2 run return run spectate @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1]')
    r = cmds('mboss/cam/release')
    ck('S6 cam/release: a no-op without the hold tag; un-spectate before the game mode; the tags and the return point go',
       r[0] == 'execute unless entity @s[tag=rlk_mb_camh] run return 0' and r[1] == 'tag @s remove rlk_mb_camh'
       and r[2] == 'execute if entity @s[gamemode=spectator] run spectate'
       and r.index(r[2]) < next(j for j, l in enumerate(r) if ' run gamemode ' in l)
       and 'data remove storage rlk:mboss camret' in r and 'tag @s remove rlk_mb_cgS' in r and 'tag @s remove rlk_mb_cgC' in r)
    cine = (F / 'char/cine/stop.mcfunction').exists()
    ck('S6 cam/release calls char/cine/stop exactly when lane H3\'s actor exists', ('function rlk:char/cine/stop' in r) == cine,
       f'char/cine/stop exists: {cine}')
    ck('S6 cam/ret: the stored point as offsets from the origin (no block-centring of a whole x / z), lifted 0.02 b',
       cmds('mboss/cam/ret') == ['$execute in minecraft:overworld positioned 0.0 0.02 0.0 run tp @s ~$(x) ~$(y) ~$(z)'])
    # generic rules over F:mboss/cam/**
    bad, refs = [], []
    for p in sorted((F / 'mboss/cam').glob('*.mcfunction')):
        for l in p.read_text(encoding='utf-8').split('\n'):
            if l.startswith('#') or not l.strip():
                continue
            if re.search(r'scoreboard players (add|remove) \S+ \S+ -', l):
                bad.append((p.stem, l))
            for ref in re.findall(r'function (rlk:[a-z0-9_/]+)', l):
                if not (F / (ref.split(':', 1)[1] + '.mcfunction')).exists():
                    refs.append((p.stem, ref))
    ck('S7 F:mboss/cam/**: no negative literal in add / remove', not bad, str(bad))
    ck('S7 F:mboss/cam/**: every function it calls exists', not refs, str(refs))


# ============================================================================================================ helpers
def stands_at(s, a=(0.0, 3.0, 0.0), b=(4.0, 2.0, 0.0)):
    """The stands as a module's sequence makes them (cam/spawn at the body), then placed apart."""
    s.call('rlk:mboss/cam/spawn', H.bctx(s))
    by = H.body_of(s).pos
    for tag, off in (('rlk_mb_cam1', a), ('rlk_mb_cam2', b)):
        e = next(e for e in s.ents if e.alive and tag in e.tags)
        e.pos = [by[0] + off[0], by[1] + off[1], by[2] + off[2]]
        e.rot = [30.0, 10.0]


def held_world(gm='adventure', state=1, live=1):
    """A fight of the special prototype in the given framework state (0 intro, 1 fight, 2 dying) with the player held."""
    s, pl = CS.setup(DP, gm=gm)
    ok = CS.fight(s, SID, state=min(state, 1))
    assert ok, 'the fight did not start'
    if state == 2:
        H.kill(s, pl)
        assert H.mb(s, '#mbSt') == 2
    stands_at(s)
    s.cam_req = live
    CS.world(s)
    assert CS.held(s), ('not held', state, H.mb(s, '#mbSt'))
    return s, pl


def ck_clean(name, s, gm0='adventure', **kw):
    res = CS.clean(s, gm0=gm0, **kw)
    bad = [k for k, v in res.items() if not v]
    ck(name, not bad, f'left behind: {bad}')


# ============================================================================================================ hold
def hold():
    s, pl = CS.setup(DP)
    ck('H0 the fight starts with the player on the F5 seat', CS.fight(s, SID) and CS.seated(s) and CS.gm(s) == 'adventure')
    av0 = list(s.avatar().pos)
    stands_at(s)
    n0 = len(s.spectates)
    s.cam_req = 1
    CS.world(s)
    c1 = next(e for e in s.ents if e.alive and 'rlk_mb_cam1' in e.tags)
    c2 = next(e for e in s.ents if e.alive and 'rlk_mb_cam2' in e.tags)
    ck('H1 the request -> held in that tick: spectator mode, the hold tag, watching stand 1, off the seat',
       CS.held(s) and CS.gm(s) == 'spectator' and CS.watching(s) is not None and 'rlk_mb_cam1' in CS.watching(s)
       and not CS.seated(s), f'{CS.gm(s)} {CS.watching(s)}')
    ck('H1 the return point = the avatar\'s place (storage rlk:mboss camret)',
       all(abs(s.storage['rlk:mboss']['camret'][k] - v) < 0.011 for k, v in zip('xyz', av0)), str(s.storage['rlk:mboss'].get('camret')))
    ck('H1 the player\'s server position and rotation follow the stand', list(pl.pos) == list(c1.pos) and list(pl.rot) == list(c1.rot))
    r0 = s.view_rest
    CS.run(s, 10)
    ck('H2 `spectate` is issued again every held tick', len(s.spectates) - n0 == 11, str(len(s.spectates) - n0))
    ck('H2 view/tick rests every held tick (no move, no aim, no re-seat); the avatar stays', s.view_rest - r0 == 10
       and list(s.avatar().pos) == av0 and not CS.seated(s), f'{s.view_rest - r0}')
    ck('H2 the game mode is switched once', [m for _t, m in s.gm_log] == ['spectator'], str(s.gm_log))
    c1.pos[0] += 2.5
    c1.rot = [77.0, -12.0]
    CS.world(s)
    ck('H3 a moved stand (one tp per tick) takes the player with it', list(pl.pos) == list(c1.pos) and list(pl.rot) == [77.0, -12.0])
    s.cam_req = 2
    CS.world(s)
    ck('H4 the other stand made live = a hard cut in that tick', 'rlk_mb_cam2' in CS.watching(s) and list(pl.pos) == list(c2.pos))
    s.cam_req = None
    CS.world(s)
    ck_clean('H5 the request stops -> released in that tick (stands may stay: the module removes them)', s, stands=True)
    ck('H5 ... facing the boss from the seat, the avatar facing her', abs(_yaw_to(s.avatar(), H.body_of(s)) - s.avatar().rot[0]) < 1e-6
       and abs(_yaw_to(pl, H.body_of(s)) - pl.rot[0]) < 1e-6, f'{pl.rot} {s.avatar().rot}')
    ck('H5 ... no new seat was made (no F5 hint in chat again)', s.seats_made == 1, str(s.seats_made))
    CS.run(s, 3)
    ck_clean('H5 ... and stays so', s, stands=True)
    for mode in ('survival', 'creative', 'adventure'):
        s, pl = held_world(gm=mode)
        tags = {'survival': {'rlk_mb_cgS'}, 'creative': {'rlk_mb_cgC'}, 'adventure': set()}[mode]
        ck(f'H6 {mode}: remembered by a tag while held', {'rlk_mb_cgS', 'rlk_mb_cgC'} & pl.tags == tags, str(pl.tags))
        s.cam_req = None
        CS.world(s)
        ck_clean(f'H6 {mode}: given back', s, gm0=mode, stands=True)


def _near(p, q):
    """p = the stored return point of q: x / z within the hundredth it was rounded down to, y 0.01-0.03 b above."""
    return abs(p[0] - q[0]) < 0.011 and abs(p[2] - q[2]) < 0.011 and 0.009 < p[1] - q[1] < 0.031


def _yaw_to(a, b):
    import math
    y = math.degrees(math.atan2(-(b.pos[0] - a.pos[0]), b.pos[2] - a.pos[2]))
    return y


# ============================================================================================================ paths
def paths():
    # the end of the request in each framework state
    for st, name in ((0, 'intro'), (1, 'fight'), (2, 'dying')):
        s, pl = held_world(state=st)
        CS.run(s, 3)
        ck(f'P1 {name}: held through the module ticks of that state', CS.held(s) and CS.gm(s) == 'spectator' and H.mb(s, '#mbSt') == st)
        s.cam_req = None
        CS.world(s)
        ck_clean(f'P1 {name}: the end -> nothing left behind', s, stands=True)
    # pause: death (the death flow owns the player's place)
    s, pl = held_world()
    s.setsc(('e', pl.id), 'dead', 1)
    CS.world(s)
    ck('P2 death: the fight pauses, the request is gone', H.mb(s, '#mbPause') == 1 and (H.mb(s, '#mbCam') or 0) == 0)
    ck_clean('P2 death: released in that tick (the game mode back; the place is the death flow\'s)', s, stands=True, seat=False)
    s.setsc(('e', pl.id), 'dead', 0)
    s.cam_req = None                               # the module never resumes a locked sequence (§3.6)
    CS.run(s, 2)
    ck_clean('P2 death: alive again -> on the seat by view/tick', s, stands=True)
    # pause: Ronova's revive
    s, pl = held_world()
    s.setsc(('e', pl.id), 'rnDie', 30)
    CS.world(s)
    ck_clean('P3 Ronova\'s revive: released in that tick, back at the avatar', s, stands=True)
    s.cam_req = None                               # the module never resumes a locked sequence (§3.6)
    s.setsc(('e', pl.id), 'rnDie', 0)
    CS.run(s, 3)
    ck_clean('P3 ... and after the revive', s, stands=True)
    # pause: the selection space
    s, pl = held_world()
    s.setsc(('e', pl.id), 'pkMode', 1)
    CS.world(s)
    ck_clean('P4 selection space: released in that tick (its place is the selection space\'s)', s, stands=True, seat=False)
    s.setsc(('e', pl.id), 'pkMode', 0)
    s.cam_req = None
    CS.run(s, 2)
    ck_clean('P4 ... back from it: on the seat', s, stands=True)
    # the body removed (/kill): mboss/main's tail
    s, pl = held_world()
    H.body_of(s).alive = False
    s.ents = [e for e in s.ents if e.alive]
    CS.world(s)
    ck('P5 the body removed: released in that tick', not CS.held(s) and CS.gm(s) == 'adventure' and not s.stands())
    CS.run(s, 2)                                   # the zone clears in the same tick: mboss/sp/won moves the player out
    ck_clean('P5 the body removed: nothing left behind, the stands went with the helper entities', s)
    # /reload: load kills the view entities, sets #vFresh, then mboss/init
    s, pl = held_world(gm='survival')
    av0 = list(s.avatar().pos)
    for e in s.ents:
        if 'rlk_view' in e.tags:
            e.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.setsc('#vFresh', 'view', 1)
    s.call('rlk:mboss/init', C0)
    ck_clean('P6 /reload: released inside mboss/init (the avatar is gone: no seat yet)', s, gm0='survival', seat=False)
    ck('P6 /reload: the player is at the stored return point (0.02 b above it: never inside the floor)', _near(pl.pos, av0), f'{pl.pos} {av0}')
    s.cam_req = None                               # the reload hook never resumes a locked sequence
    CS.run(s, 2)
    ck_clean('P6 /reload: the new avatar is made there and the player seated', s, gm0='survival')
    ck('P6 /reload: ... at the old place', _near(s.avatar().pos, av0))
    # relog: the player is away (still spectator, still tagged), comes back with #vFresh 1 and its own camera
    s, pl = held_world(gm='creative')
    av0 = list(s.avatar().pos)
    s.ents.remove(pl)
    CS.run(s, 5)
    ck('P7 relog: away -> the fight pauses, the request is off', H.mb(s, '#mbPause') == 1 and (H.mb(s, '#mbCam') or 0) == 0)
    s.st(pl)['cam'] = None
    s.ents.append(pl)
    s.setsc('#vFresh', 'view', 1)
    s.cam_req = None
    CS.world(s)
    ck_clean('P7 relog: released in the first tick back', s, gm0='creative', stands=True, seat=False)
    ck('P7 relog: ... at the stored return point', _near(pl.pos, av0), f'{pl.pos} {av0}')
    CS.run(s, 2)
    ck_clean('P7 relog: the new avatar and the seat', s, gm0='creative', stands=True)
    # relog while the module goes on asking (a core that resumes its sequence): the rebuilt view makes the player the body
    # for a tick; the hold releases instead of leaving a tagged free spectator
    s, pl = held_world(gm='survival')
    av0 = list(s.avatar().pos)
    s.ents.remove(pl)
    CS.run(s, 3)
    s.st(pl)['cam'] = None
    s.ents.append(pl)
    s.setsc('#vFresh', 'view', 1)
    CS.world(s)
    ck_clean('P7b relog, the module still asking: released in the first tick back', s, gm0='survival', stands=True, seat=False, req=False)
    ck('P7b ... at the stored return point', _near(pl.pos, av0), f'{pl.pos} {av0}')
    s.cam_req = None                               # (a real sequence sees the release and stops asking: test_seq)
    CS.run(s, 2)
    ck_clean('P7b ... the new avatar and the seat', s, gm0='survival', stands=True)
    # cleanup (room/clear, run end, test stop)
    s, pl = held_world()
    s.call('rlk:mboss/cleanup', C0)
    ck_clean('P8 mboss/cleanup: released at once, no stand', s)
    CS.run(s, 2)
    ck_clean('P8 ... and after', s)
    # abort (no kill: the cancel path)
    s, pl = held_world()
    s.call('rlk:mboss/test/abort', H.ctx(pl))
    CS.run(s, 3)
    ck_clean('P9 test/abort: released, no stand', s)
    # the kill while held through the death sequence: won -> the dungeon return point
    s, pl = held_world()
    ret = dict(s.storage['rlk:mboss']['ret'])
    H.kill(s, pl)
    CS.run(s, 3)
    ck('P10 kill: still held in the death sequence while the module asks', CS.held(s) and H.mb(s, '#mbSt') == 2)
    CS.until(s, lambda s: (H.mb(s, '#mbLive') or 0) == 0, 200)
    CS.run(s, 2)
    ck_clean('P10 kill: after the death sequence nothing is left behind', s)
    ck('P10 kill: the player (and the avatar) are at the dungeon return point, not in the arena',
       abs(s.avatar().pos[0] - ret['x']) < 0.02 and abs(s.avatar().pos[2] - ret['z']) < 0.02, f'{s.avatar().pos} {ret}')
    # uninstall
    s, pl = held_world(gm='survival')
    s.call('rlk:mboss/uninstall', C0)
    ck_clean('P11 uninstall: released by its cleanup, no stand', s, gm0='survival')
    # the two-player guard of rlk:tick
    s, pl = held_world()
    line = next(l for l in fn('tick') if 'pcount tmp matches 2..' in l and 'rlk_mb_camh' in l)
    s.setsc('#pcount', 'tmp', 2)
    s.cmd(split(line), C0)
    ck_clean('P12 the two-player guard: released by its own line', s, stands=True, req=False)
    # a request that outlived its fight (#mbLive 0, #mbCam 1)
    s, pl = held_world()
    s.setsc('#mbLive', 'mb', 0)
    s.setsc('#mbCam', 'mb', 1)
    s.run_cam_lines()
    ck_clean('P13 a request without a fight: dropped and released', s, stands=True)


# ============================================================================================================ stand
def stand():
    s, pl = held_world(gm='survival')
    live = next(e for e in s.ents if e.alive and 'rlk_mb_cam1' in e.tags)
    live.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.net_tick(pl)
    ck('K1 the live stand killed: the game drops the camera', s.st(pl)['cam'] is None and CS.gm(s) == 'spectator')
    CS.world(s)
    ck_clean('K1 ... the next tick releases the player (never a free spectator)', s, gm0='survival', stands=True, req=False)
    CS.run(s, 5)
    ck('K1 ... stays released while the stand is missing, though the module still asks',
       not CS.held(s) and CS.gm(s) == 'survival' and CS.seated(s))
    s.call('rlk:mboss/cam/spawn', H.bctx(s))
    CS.world(s)
    ck('K2 the stands are back (cam/spawn is idempotent): held again', CS.held(s) and CS.gm(s) == 'spectator'
       and 'rlk_mb_cam1' in CS.watching(s) and len(s.stands()) == 2)
    idle = next(e for e in s.ents if e.alive and 'rlk_mb_cam2' in e.tags)
    idle.alive = False
    s.ents = [e for e in s.ents if e.alive]
    CS.run(s, 3)
    ck('K3 the idle stand killed: the hold goes on', CS.held(s) and 'rlk_mb_cam1' in CS.watching(s))
    # sneaking
    s, pl = held_world()
    pl.data['sneak'] = True
    seen = []
    for _ in range(8):
        CS.world(s)
        seen.append((CS.held(s), CS.gm(s), s.st(pl)['cam']))
    ck('K4 sneaking: the game drops the camera after every tick ...', all(c is None for _h, _g, c in seen), str(seen))
    n0 = len(s.spectates)
    CS.world(s)
    ck('K4 ... and the hold takes it back in every tick; never released', all(h and g == 'spectator' for h, g, _c in seen)
       and len(s.spectates) == n0 + 1)
    pl.data['sneak'] = False
    CS.world(s)
    ck('K4 sneak released: watching the stand again', CS.watching(s) is not None and 'rlk_mb_cam1' in CS.watching(s))
    s.cam_req = None
    pl.data['sneak'] = True
    CS.world(s)
    ck_clean('K5 the end while sneaking: released; view/ride_tick\'s sneak rule owns the seat', s, stands=True, seat=False)
    pl.data['sneak'] = False
    CS.run(s, 2)
    ck_clean('K5 ... seated once the key is up', s, stands=True)


# ============================================================================================================ idem
def idem():
    s, pl = CS.setup(DP, gm='creative')
    CS.fight(s, SID)
    snap = (CS.gm(s), set(pl.tags), list(pl.pos), CS.seated(s))
    for _ in range(2):
        s.call('rlk:mboss/cam/release', H.ctx(pl))
    ck('I1 release on a player who is not held changes nothing (creative stays creative)',
       (CS.gm(s), set(pl.tags), list(pl.pos), CS.seated(s)) == snap and not s.gm_log)
    s, pl = held_world(gm='creative')
    s.cam_req = None
    CS.world(s)
    n = len(s.gm_log)
    s.call('rlk:mboss/cam/release', H.ctx(pl))
    s.call('rlk:mboss/cam/release', H.ctx(pl))
    ck_clean('I2 release again after a release: nothing more happens', s, gm0='creative', stands=True)
    ck('I2 ... no game mode change', len(s.gm_log) == n)
    # no stands: the request alone never switches the game mode
    s, pl = CS.setup(DP)
    CS.fight(s, SID)
    s.cam_req = 1
    CS.run(s, 3)
    ck('I3 a request without stands: not held, adventure, seated', not CS.held(s) and CS.gm(s) == 'adventure' and CS.seated(s)
       and not s.gm_log)
    # developer mode: the player is the body
    s, pl = CS.setup(DP)
    s.setsc(('e', pl.id), 'devMode', 1)
    CS.fight_dev = True
    z, a = H.rift_zone(s, SID)
    pl.pos = list(a.pos)
    H.enter(s, a)
    CS.until(s, lambda s: H.body_of(s) is not None and (H.mb(s, '#mbSt') or 0) == 1, 900)
    stands_at(s)
    s.cam_req = 1
    CS.run(s, 4)
    ck('I4 developer mode (no avatar, the player is the body): never locked', not CS.held(s) and CS.gm(s) == 'adventure'
       and 'rlk_body' in pl.tags and not s.gm_log, f'{CS.gm(s)} {pl.tags & {"rlk_body", "rlk_mb_camh"}}')


# ============================================================================================================ cost
def cost():
    s, pl = CS.setup(DP)
    CS.fight(s, SID)
    k0 = len(s.cam_cost)
    CS.run(s, 20)
    free = s.cam_cost[k0:]
    stands_at(s)
    s.cam_req = 1
    CS.world(s)
    first = s.cam_cost[-1]
    k1 = len(s.cam_cost)
    CS.run(s, 20)
    heldc = s.cam_cost[k1:]
    s.cam_req = None
    CS.world(s)
    rel = s.cam_cost[-1]
    print(f'   cost of rlk:tick\'s FN-cam lines per tick: free {max(free)}, the first held tick {first}, held {max(heldc)}, '
          f'the release tick {rel}; mboss/main +1 in every fight tick')
    m = cmds('mboss/main')
    ck('C1 mboss/main pays one command for the request', sum(l.startswith('scoreboard') and 'mbCam' in l for l in m) == 1)
    ck('C1 rlk:tick pays two commands in a tick without a lock', len(CS.tick_cam_lines(DP)) == 2 and set(free) == {2}, str(set(free)))
    ck('C2 a held tick costs at most 12 commands', max(heldc) <= 12, str(max(heldc)))
    ck('C2 the first held tick and the release tick at most 30 each', first <= 30 and rel <= 30, f'{first} {rel}')


# ============================================================================================================ ident
SHARED = ('mboss/main', 'mboss/cleanup_fight', 'mboss/init', 'mboss/uninstall', 'tick', 'view/tick', 'lvup/tick')
CAM_WORDS = ('mbCam', 'mboss/cam/', 'camret', 'rlk_mb_camh')
# the other H lanes' shared lines on a merged tree: lane H1's FN-bal (#mbBalOff: bal/boss/may, fight_vars, cleanup_fight)
# and her registry record (intro 1450 / death 1494)
H1_FILES = ('bal/boss/may', 'mboss/fight_vars', 'mboss/register')
H1_WORDS = ('mbBalOff', 'id:"scarlet"')


def ident():
    repo = DP.parent
    git = lambda *a: subprocess.run(['git', '-C', str(repo), *a], capture_output=True, text=True)  # noqa: E731
    base = BASE or git('merge-base', 'HEAD', 'origin/wip/combat').stdout.strip()
    if not base:
        print('   ident: no base commit (pass --base): SKIPPED')
        return
    names = git('diff', '--name-status', base, '--', 'roguelike/data').stdout.split('\n')
    names += [f'A\t{p}' for p in git('ls-files', '--others', '--exclude-standard', '--', 'roguelike/data').stdout.split('\n') if p]
    pre = '\troguelike/data/rlk/function/'
    other = [n for n in names if n.strip() and pre + 'boss/scarlet/' not in n and pre + 'mboss/cam/' not in n
             and pre + 'char/cine/' not in n]
    mine = sorted(f'M{pre}{n}.mcfunction' for n in SHARED)
    h1 = sorted(f'M{pre}{n}.mcfunction' for n in H1_FILES)
    extra = sorted(set(other) - set(mine) - set(h1))
    ck(f'D1 against {base[:9]}: outside F:boss/scarlet, F:mboss/cam (and lane H3\'s F:char/cine) only the shared files change '
       f'(FN-cam\'s seven; lane H1\'s FN-bal / registry three on a merged tree)', set(mine) <= set(other) and not extra, str(extra))
    new = [n for n in names if pre + 'mboss/cam/' in n]
    ck('D1 F:mboss/cam/** is new', new and all(n.startswith('A\t') for n in new), str(new))
    for n in SHARED + tuple(x for x in H1_FILES if f'M{pre}{x}.mcfunction' in other):
        d = git('diff', '-U0', base, '--', f'roguelike/data/rlk/function/{n}.mcfunction').stdout.split('\n')
        rem = [l for l in d if l.startswith('-') and not l.startswith('---')]
        add = [l[1:] for l in d if l.startswith('+') and not l.startswith('+++')]
        code = [l for l in add if l.strip() and not l.startswith('#')]
        if n in H1_FILES:
            ck(f'D2 {n} (lane H1): every changed command is a FN-bal line or her registry record',
               all(any(w in l for w in H1_WORDS) for l in code + [l[1:] for l in rem if not l[1:].startswith('#')]), f'{rem} {code}')
            continue
        cam = [l for l in code if any(w in l for w in CAM_WORDS)]
        rest = [l for l in code if l not in cam]
        ck(f'D2 {n}: added lines only, every added command a FN-cam line (or lane H1\'s #mbBalOff)',
           not rem and cam and all(any(w in l for w in H1_WORDS) for l in rest), f'removed {rem} added {code}')


SECTIONS = [('static', static), ('hold', hold), ('paths', paths), ('stand', stand), ('idem', idem), ('cost', cost), ('ident', ident)]
for name, f in SECTIONS:
    if want(name):
        print(f'== {name}')
        f()
H.summary("TEST_CAM")
