#!/usr/bin/env python3
"""test_cam.py: the cinematic lock of the boss framework, FN-cam (홍련 rebuild, lane H2; round V lane VC: v_brief.md §3 "VC"):
rlk:tick's hold / release lines, F:mboss/cam/**, view/tick's guard.

    python3 test_cam.py <datapack root> [section ...] [--base <commit>]

Run it from a copy outside the datapack (tools/dev/sim/README.md §1). It only reads the tree. World: hr/h2/camsim.py (the F5
view model, the spectator rules of the 26.3 server, the client's picture of a display camera, the player's own tick with
the tick-advancement reward, rlk:tick's FN-cam lines after mboss/main); the fight is the special prototype `spproto`, the
"module" is camsim's stand-in request (s.cam_req: #mbCam / #mbCamId set in every module tick).

  static  the names; rlk:tick: hold then release right after mboss/main, the two-player guard releases; view/tick: exactly
          one guard; lvup/tick; mboss/main zeroes the request; cleanup_fight / init release first; the camera = an EMPTY
          item_display (never a living entity: a spectator sees those as ghosts) carrying two text_displays; the tick
          advancement and its reward; no negative literal, every function reference exists
  hold    the request -> spectator on the live camera from the same tick, on the SERVER and on the CLIENT; `spectate`
          issued every tick; the other camera = a hard cut; view/tick rests; the three game modes come back; the request
          stops -> released in that tick
  lock    (VC 4, 9) while held: the player's entity and block interaction ranges are 0 (the base and other modifiers
          untouched), the sidebar is off, the F5 seat (an armour stand) is gone; at the release: the modifiers gone, the
          sidebar back, the seat made again without the chat hint, an empty action bar after the mount
  grid    (VC 1, 2) mboss/cam/fix: any rotation ends on the 360 / 256 grid (the nearest step, idempotent, the bytes the
          client gets are exact), the entity 4 blocks before the viewpoint along that rotation; OnGround flips on every
          other placement; spawn_at: the same pose in the summon NBT
  client  (VC 1, 3) a segment: the duration a tick ahead, one placement, the client's camera moves linearly and arrives
          on time; a cut to a camera prepared with duration 0 shows no glide
  post    (VC 5, 6) Shift: the game ends the spectate in the player's own tick, mboss/cam/post gives the camera back in
          the same tick: the client is on the live camera after EVERY tick; a camera the client did not have when the
          hold began (a place still arriving): attached as soon as it has it (the re-send), never a free spectator after;
          a movement key: the camera is re-sent; the player's own view = the shot's (4 blocks back)
  text    (VC 10) the line and the hint of every camera: set, cleared, their geometry (lower third, >= 28 px / 16 px at
          a field of view of 70 .. 90)
  paths   every exit path from a held state leaves nothing behind (camsim.clean)
  stand   the live camera killed: released at once, held again when the cameras are back; the idle one killed: nothing
  idem    release twice / on a player who is not held changes nothing; a developer-mode player is never locked
  cost    commands per tick: the framework's share without a lock and while held
  ident   against the base commit (default: origin/wip/v): outside F:boss/scarlet/**, F:mboss/cam/** and F:char/cine/**
          only the listed shared files change
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
       and L.CAM_EYE == 0.0 and L.CAM_BACK == 4.0 and abs(L.CAM_GRID - 1.40625) < 1e-12 and L.CAM_SEG_MAX == 59)
    for f in ('spawn', 'spawn_at', 'spawn_in', 'grid', 'fix', 'hold', 'hold_in', 'post', 'release', 'back', 'ret', 'seat', 'kill'):
        ck(f'S1 F:mboss/cam/{f} exists', (F / f'mboss/cam/{f}.mcfunction').exists())
    ck('S1 L.cam(\'spawn_at\', id=2), cam(\'fix\'), cam_dur, cam_resend',
       L.cam('spawn_at', id=2) == 'function rlk:mboss/cam/spawn_at {id:2}' and L.cam('fix') == 'function rlk:mboss/cam/fix'
       and L.cam_dur(2, 40) == 'data merge entity @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] {teleport_duration:40}'
       and 'mbCamRe' in L.cam_resend(40))
    import json
    adv = json.loads((DP / 'data/rlk/advancement/mboss/cam_post.json').read_text(encoding='utf-8'))
    ck('S1 the tick advancement rlk:mboss/cam_post: trigger minecraft:tick, reward mboss/cam/post, no display',
       adv == {'criteria': {'t': {'trigger': 'minecraft:tick'}}, 'rewards': {'function': 'rlk:mboss/cam/post'}}, str(adv))
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
    # the cameras
    sp = cmds('mboss/cam/spawn')
    ok = len(sp) == 2
    living = ('armor_stand', 'husk', 'zombie', 'mannequin', 'interaction')
    for n_, l in zip((1, 2), sp):
        ok &= l.startswith(f'execute unless entity @e[type=minecraft:item_display,tag=rlk_mb_cam{n_},limit=1] run summon minecraft:item_display ~ ~ ~ ')
        nbt = l.split('~ ~ ~ ', 1)[1]
        head = nbt.split('Passengers:')[0]
        ok &= 'item:' not in head and 'teleport_duration:0' in head and not any(x in nbt for x in living)
        ok &= re.search(r'Tags:\[([^\]]*)\]', head).group(1) == f'"rlk_room","rlk_mb_aux","rlk_pet","rlk_mb_camx","rlk_mb_cam","rlk_mb_cam{n_}"'
        ps = re.findall(r'\{id:"minecraft:text_display",Tags:\[([^\]]*)\]', nbt)
        ok &= len(ps) == 2 and '"rlk_mb_camt"' in ps[0] and '"rlk_mb_camk"' in ps[1] and all('"rlk_mb_camx"' in x and '"rlk_mb_aux"' in x for x in ps)
        ok &= all(f'"rlk_mb_camx{n_}"' in x and f'"rlk_mb_camx{3 - n_}"' not in x for x in ps)      # (round W) whose texts they are
        ok &= nbt.count('billboard:"center"') == 2 and nbt.count('see_through:0b') == 2 and nbt.count('background:0,text:""') == 2
    ck('S6 cam/spawn: two EMPTY item_displays (no item, no living entity), each carrying its line and its hint text_display '
       '(billboard center, empty), rlk_room rlk_mb_aux, idempotent', ok, str(sp)[:300])
    ck('S6 cam/kill removes the cameras and their texts and blanks the stored line and hint',
       cmds('mboss/cam/kill') == ['kill @e[tag=rlk_mb_camx]', 'data modify storage rlk:mboss camtx set value {line:{text:"",background:0},hint:{text:"",background:0}}'])
    tx = cmds('mboss/cam/text')
    ck('S6 (round W) cam/text: per live camera the OTHER camera\'s texts blanked, the live one\'s line and hint from storage; the live rule is '
       'cam/hold\'s (2, else 1)', len(tx) == 6 and all(l.startswith('execute unless score #mbCamId mb matches 2 as ') for l in tx[:3])
       and all(l.startswith('execute if score #mbCamId mb matches 2 as ') for l in tx[3:])
       and 'tag=rlk_mb_camx2] run data merge entity @s {text:"",background:0}' in tx[0] and 'tag=rlk_mb_camx1] run data merge entity @s {text:"",background:0}' in tx[3]
       and all(f'tag={tg},tag=rlk_mb_camx{n_}] run data modify entity @s {{}} merge from storage rlk:mboss camtx.{k}' in tx[i]
               for i, tg, n_, k in ((1, 'rlk_mb_camt', 1, 'line'), (2, 'rlk_mb_camk', 1, 'hint'), (4, 'rlk_mb_camt', 2, 'line'), (5, 'rlk_mb_camk', 2, 'hint'))), str(tx)[:300])
    h = cmds('mboss/cam/hold')
    ck('S6 cam/hold: spectate is the last command of both branches (issued every held tick); the tick advancement armed before it',
       h[-1] == 'spectate @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1]'
       and h[-2] == 'execute if score #mbCamId mb matches 2 run return run spectate @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1]'
       and 'advancement revoke @s only rlk:mboss/cam_post' in h and not any('in_sneak' in l for l in h), str(h[-3:]))
    po = cmds('mboss/cam/post')
    ck('S6 cam/post: only for a held spectator while the request is on; the re-send (`spectate` alone) before the live camera',
       po[0] == 'execute unless entity @s[tag=rlk_mb_camh] run return 0' and po[1] == 'execute unless score #mbCam mb matches 1 run return 0'
       and po[2] == 'execute unless entity @s[gamemode=spectator] run return 0'
       and po[3] == 'execute if score #mbCamRe mb matches 1.. run spectate' and po[-1].startswith('spectate @e[type=minecraft:item_display,tag=rlk_mb_cam1'),
       str(po))
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
        e.rot = [1.40625 * 21, 1.40625 * 7]        # a rotation on the grid, as mboss/cam/fix leaves every camera


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
    ck('H1 the request -> held in that tick: spectator mode, the hold tag, watching camera 1, off the seat',
       CS.held(s) and CS.gm(s) == 'spectator' and CS.watching(s) is not None and 'rlk_mb_cam1' in CS.watching(s)
       and not CS.seated(s), f'{CS.gm(s)} {CS.watching(s)}')
    ck('H1 ... and the CLIENT looks through camera 1 (the camera packet was sent and applied)',
       CS.client_on(s) is not None and 'rlk_mb_cam1' in CS.client_on(s), str(s.cam_packets[-3:]))
    ck('H1 the return point = the avatar\'s place (storage rlk:mboss camret)',
       all(abs(s.storage['rlk:mboss']['camret'][k] - v) < 0.011 for k, v in zip('xyz', av0)), str(s.storage['rlk:mboss'].get('camret')))
    ck('H1 the player\'s server position and rotation follow the stand', list(pl.pos) == list(c1.pos) and list(pl.rot) == list(c1.rot))
    r0 = s.view_rest
    CS.run(s, 10)
    ck('H2 `spectate` is issued again every held tick (by the hold and by post in the player\'s own tick)', len(s.spectates) - n0 == 22,
       str(len(s.spectates) - n0))
    ck('H2 view/tick rests every held tick (no move, no aim, no re-seat); the avatar stays', s.view_rest - r0 == 10
       and list(s.avatar().pos) == av0 and not CS.seated(s), f'{s.view_rest - r0}')
    ck('H2 the game mode is switched once', [m for _t, m in s.gm_log] == ['spectator'], str(s.gm_log))
    c1.pos[0] += 2.5
    c1.rot = [77.0, -12.0]
    CS.world(s)
    ck('H3 a moved stand (one tp per tick) takes the player with it', list(pl.pos) == list(c1.pos) and list(pl.rot) == [77.0, -12.0] and 'rlk_mb_cam1' in CS.client_on(s))
    s.cam_req = 2
    CS.world(s)
    ck('H4 the other camera made live = a hard cut in that tick (server and client)', 'rlk_mb_cam2' in CS.watching(s)
       and list(pl.pos) == list(c2.pos) and 'rlk_mb_cam2' in CS.client_on(s))
    s.cam_req = None
    CS.world(s)
    ck_clean('H5 the request stops -> released in that tick (stands may stay: the module removes them)', s, stands=True)
    ck('H5 ... facing the boss from the seat, the avatar facing her', abs(_yaw_to(s.avatar(), H.body_of(s)) - s.avatar().rot[0]) < 1e-6
       and abs(_yaw_to(pl, H.body_of(s)) - pl.rot[0]) < 1e-6, f'{pl.rot} {s.avatar().rot}')
    ck('H5 ... the seat is back in the release tick, made by mboss/cam/seat (no F5 hint in chat again)',
       s.seats_made == 1 and s.seat() is not None and not any('F5' in x or '시점' in x for _t, x in s.tells), f'{s.seats_made} {s.tells}')
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
    s.st(pl)['cam'] = s.st(pl)['ccam'] = None      # a new connection: the client is on its own player
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
    s.st(pl)['cam'] = s.st(pl)['ccam'] = None      # a new connection: the client is on its own player
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
    s, pl = held_world()
    s.cam_req = None
    pl.data['sneak'] = True
    CS.world(s)
    ck_clean('K5 the end while sneaking: released; view/ride_tick\'s sneak rule owns the seat', s, stands=True, seat=False)
    pl.data['sneak'] = False
    CS.run(s, 2)
    ck_clean('K5 ... seated once the key is up', s, stands=True)


# ============================================================================================================ lock
def lock():
    s, pl = CS.setup(DP)
    CS.fight(s, SID)
    ck('L0 before the lock: the seat (an armour stand) exists, the sidebar is the pack\'s', s.seat() is not None and s.sidebar == 'stacks')
    stands_at(s)
    s.cam_req = 1
    CS.world(s)
    er, br = s.attr(pl, 'minecraft:entity_interaction_range'), s.attr(pl, 'minecraft:block_interaction_range')
    ck('L1 (VC 4) held: the player\'s entity and block interaction ranges are 0 (a left click picks nothing)', er == 0 and br == 0, f'{er} {br}')
    ms = s.mods(pl)
    ck('L1 ... by a modifier that multiplies the total by 0 (the base is not written)',
       ms['minecraft:entity_interaction_range'] == {'rlk:mb_cam': (-1.0, 'add_multiplied_total')}
       and ms['minecraft:block_interaction_range'] == {'rlk:mb_cam': (-1.0, 'add_multiplied_total')}
       and not any(' base ' in a and 'interaction_range' in a for _t, a in s.attr_log), str(ms))
    ck('L2 (VC 9) held: the sidebar is off', s.sidebar is None)
    living = [e.etype for e in s.ents if e.alive and e.etype == 'armor_stand']
    ck('L2 (VC 7) held: no armour stand is left in the world (the F5 seat is removed: a spectator would see its ghost)', not living, str(living))
    ck('L3 (VC 5) the player\'s own third-person view = the shot\'s viewpoint 0.2 b higher (scale 0.125 x camera distance 32 = 4 b back)',
       abs(s.attr(pl, 'minecraft:scale') - 0.125) < 1e-9 and abs(s.attr(pl, 'minecraft:camera_distance') - 32) < 1e-9
       and all(abs(a - b - (0.2025 if i == 1 else 0)) < 1e-6 for i, (a, b) in enumerate(zip(CS.own_view(s)[0], CS.client_view(s)[0]))),
       f'{CS.own_view(s)} {CS.client_view(s)}')
    CS.run(s, 6)
    ck('L4 ... all of it for the whole hold', s.attr(pl, 'minecraft:entity_interaction_range') == 0 and s.sidebar is None and s.seat() is None)
    n_ab = len(s.abar)
    s.cam_req = None
    CS.world(s)
    ck_clean('L5 the release: nothing left (the modifiers gone, the sidebar back, the client on its own view)', s, stands=True)
    ck('L5 ... the ranges are the base again', s.attr(pl, 'minecraft:entity_interaction_range') == 3.0 and s.attr(pl, 'minecraft:scale') == 0.0625)
    ck('L5 ... seated on a new seat in the same tick, an empty action bar sent after the mount (no "Press Shift to Dismount")',
       CS.seated(s) and len(s.abar) > n_ab and s.abar[-1][1] == '""', str(s.abar[n_ab:]))
    ck('L5 ... no chat line', not s.tells, str(s.tells))
    # loot lines held back during the lock (the pack's sapphire line) are told at the release
    s, pl = held_world()
    s.setsc('#mbCamSap', 'mb', 3)
    s.cam_req = None
    CS.world(s)
    ck('L6 a sapphire gain counted during the lock is told once at the release', len(s.tells) == 1 and '사파이어' in s.tells[0][1]
       and (s.sc('#mbCamSap', 'mb') or 0) == 0, str(s.tells))


# ============================================================================================================ grid
def grid():
    import math
    import random
    s, pl = CS.setup(DP)
    CS.fight(s, SID)
    s.call('rlk:mboss/cam/spawn', H.bctx(s))
    cam = next(e for e in s.ents if e.alive and 'rlk_mb_cam1' in e.tags)
    by = H.body_of(s).pos
    rnd = random.Random(7)
    bad, flips = [], []
    for k in range(400):
        v = [by[0] + rnd.uniform(-9, 9), by[1] + rnd.uniform(0.2, 6), by[2] + rnd.uniform(-9, 9)]
        yaw, pitch = rnd.uniform(-180, 180), rnd.uniform(-90, 90)
        if k < 6:
            yaw, pitch = [(0, 0), (179.9, 89.9), (-180, -90), (90, 90), (-0.71, 0.70), (1.40625 * 7, -1.40625 * 3)][k]
        cam.pos, cam.rot = list(v), [yaw, pitch]
        s.call('rlk:mboss/cam/fix', Ctx(cam, tuple(cam.pos), tuple(cam.rot)))
        flips.append(cam.data.get('og'))
        r = cam.rot
        f = CS.forward(r)
        dy = abs((r[0] - yaw + 180) % 360 - 180)
        ok = (CS.on_grid(r) and dy <= CS.GRID / 2 + 1e-6 and abs(r[1] - pitch) <= CS.GRID / 2 + 1e-6
              and all(abs(cam.pos[i] - (v[i] + 4 * f[i])) < 1e-9 for i in range(3))
              and all(math.floor(x * 256.0 / 360.0) * 360.0 / 256.0 == x for x in r))
        if not ok:
            bad.append((yaw, pitch, r, cam.pos, v))
    ck('G1 (VC 1, 2) cam/fix, 400 poses: the rotation on the 360 / 256 grid (the nearest step; the byte the client gets is exact), '
       'the entity 4 b before the viewpoint along it', not bad, str(bad[:3]))
    ck('G1 ... OnGround false on every other placement (the float sync packet), true on the others',
       flips[:6] == [False, True, False, True, False, True] and set(flips[0::2]) == {False} and set(flips[1::2]) == {True}, str(flips[:8]))
    cam.pos, cam.rot = [by[0], by[1] + 2, by[2]], [1.40625 * 40, 1.40625 * 5]
    p0 = list(cam.pos)
    s.call('rlk:mboss/cam/grid', Ctx(cam, tuple(cam.pos), tuple(cam.rot)))
    ck('G2 a rotation already on the grid stays', cam.rot == [1.40625 * 40, 1.40625 * 5], str(cam.rot))
    s.call('rlk:mboss/cam/kill', C0)
    v, rot = (by[0] + 1.5, by[1] + 2.25, by[2] - 3.0), (-137.25, 12.5)
    s.call('rlk:mboss/cam/spawn_at', Ctx(None, v, rot), {'id': 2})
    c2 = [e for e in s.ents if e.alive and 'rlk_mb_cam2' in e.tags]
    sp = c2[0].data.get('spawn') if c2 else None
    f = CS.forward(sp[1]) if sp else (0, 0, 0)
    ck('G3 cam/spawn_at {id:2}: one camera B, its summon pose (the spawn packet) = the grid rotation nearest the aim and the '
       'place 4 b before the viewpoint; its two texts with it',
       len(c2) == 1 and not any('rlk_mb_cam1' in e.tags for e in s.ents if e.alive) and sp is not None and CS.on_grid(sp[1])
       and abs(sp[1][0] - rot[0]) <= CS.GRID / 2 and abs(sp[1][1] - rot[1]) <= CS.GRID / 2
       and all(abs(sp[0][i] - (v[i] + 4 * f[i])) < 1e-9 for i in range(3))
       and len(s.cam_texts(CS.LINE_TAG)) == 1 and len(s.cam_texts(CS.HINT_TAG)) == 1, str(sp))
    ck('G3 ... the helper marker is gone, the camera carries the FN-cam tags',
       not any('rlk_mb_camr' in e.tags for e in s.ents if e.alive) and {'rlk_mb_cam', 'rlk_mb_camx', 'rlk_mb_aux', 'rlk_room'} <= c2[0].tags)
    y0 = c2[0].pos[1]
    s.call('rlk:mboss/cam/spawn_at', Ctx(None, (by[0], by[1] + 5, by[2]), (0.0, 0.0)), {'id': 2})
    ck('G3 ... idempotent: a second call leaves the camera where it is', len([e for e in s.ents if e.alive and 'rlk_mb_cam2' in e.tags]) == 1
       and abs(c2[0].pos[1] - y0) < 1e-9)


# ============================================================================================================ client
def client():
    sys.path.insert(0, str(DP / 'tools'))
    import mboss_lib as L
    s, pl = held_world()
    cam1 = next(e for e in s.ents if e.alive and 'rlk_mb_cam1' in e.tags)
    cam2 = next(e for e in s.ents if e.alive and 'rlk_mb_cam2' in e.tags)
    CS.run(s, 2)
    p0, r0 = tuple(cam1.data['cl'][0]), tuple(cam1.data['cl'][1])
    p1, r1 = (p0[0] + 3.0, p0[1] + 0.5, p0[2] - 2.0), (1.40625 * 30, 1.40625 * 4)
    s.cmd(split(L.cam_dur(1, 20)), C0)                 # the duration one tick ahead ...
    CS.world(s)
    cam1.pos, cam1.rot = list(p1), list(r1)            # ... then the one placement of the segment
    path = []
    for _ in range(22):
        CS.world(s)
        path.append((tuple(cam1.data['cl'][0]), tuple(cam1.data['cl'][1])))
    lin = all(max(abs(path[j][0][i] - (p0[i] + (p1[i] - p0[i]) * (j + 1) / 20)) for i in range(3)) < 1e-9
              and max(abs(path[j][1][i] - (r0[i] + (r1[i] - r0[i]) * (j + 1) / 20)) for i in range(2)) < 1e-9 for j in range(20))
    ck('C1 (VC 1) a segment: one placement, the client moves the camera linearly (position and rotation) and arrives after its '
       '20 ticks; nothing moves afterwards', lin and path[20] == path[19] == (p1, r1), str(path[:2]))
    ck('C1 ... one move packet for the whole segment, its rotation on the grid', cam1.data['segs'][-1][1] == 20
       and CS.on_grid(cam1.data['sent'][-1]), str(cam1.data['segs'][-3:]))
    # a duration set in the tick of its own move applies one move late (the data packet follows the move packet)
    s.cmd(split(L.cam_dur(1, 5)), C0)
    cam1.pos = [p1[0] + 1.0, p1[1], p1[2]]
    CS.world(s)
    ck('C2 a duration set in the tick of the move itself is too late: the client still used the old one (20)',
       cam1.data['segs'][-1][1] == 20, str(cam1.data['segs'][-2:]))
    # a hard cut the way cam.py prepares it: duration 0 (t - 3), the placement (t - 2), the first segment's duration (t - 1)
    q, rq = (p0[0] - 6.0, p0[1] + 1.0, p0[2] + 4.0), (-1.40625 * 50, 1.40625 * 9)
    s.cmd(split(L.cam_dur(2, 0)), C0)
    CS.world(s)
    cam2.pos, cam2.rot = list(q), list(rq)
    CS.world(s)
    settled = (tuple(cam2.data['cl'][0]), tuple(cam2.data['cl'][1])) == (q, rq) and cam2.data['steps'] == 0
    s.cmd(split(L.cam_dur(2, 30)), C0)
    CS.world(s)
    s.cam_req = 2
    CS.world(s)
    v = CS.client_cam(s)
    ck('C3 (VC 3) a prepared cut: the idle camera snapped (no glide) two ticks before, the first frame of the new shot is its '
       'place exactly', settled and v == (q, rq) and 'rlk_mb_cam2' in CS.client_on(s), f'{settled} {v}')
    # ... and what an unprepared cut looks like (the 11-11 build: the camera placed in the tick of the cut): a slide
    s.cam_req = 1
    cam1.pos, cam1.rot = [q[0] + 5, q[1], q[2]], [0.0, 0.0]
    CS.world(s)
    v = CS.client_cam(s)
    ck('C3 ... (control) an idle camera moved in the tick of its cut with a duration still set slides into the shot',
       v is not None and v[0] != tuple(cam1.pos), str(v))


# ============================================================================================================ post
def post():
    sys.path.insert(0, str(DP / 'tools'))
    import mboss_lib as L
    # Shift: the game ends the spectate in the player's own tick; mboss/cam/post spectates again in the same tick
    s, pl = held_world()
    cam1 = next(e for e in s.ents if e.alive and 'rlk_mb_cam1' in e.tags)
    CS.run(s, 4)
    pl.data['sneak'] = True
    seen, k0, r0 = [], len(s.cam_packets), len(s.post_runs)
    for k in range(12):
        cam1.pos = [cam1.pos[0] + 0.1, cam1.pos[1], cam1.pos[2]]
        CS.world(s)
        seen.append((CS.held(s), CS.gm(s), CS.client_on(s) is not None and 'rlk_mb_cam1' in CS.client_on(s),
                     CS.watching(s) is not None and 'rlk_mb_cam1' in CS.watching(s)))
    ck('P1 (VC 5) Shift held 12 ticks: after EVERY tick the client and the server are on the live camera; never released',
       all(h and g == 'spectator' and c and w for h, g, c, w in seen), str(seen))
    pk = s.cam_packets[k0:]
    ck('P1 ... per tick the game takes the camera away and post gives it back (two camera packets in one server tick, '
       'the last one the camera)', len(pk) == 24 and all(pk[2 * i][1] is None and pk[2 * i + 1][1] == cam1.id and pk[2 * i][0] == pk[2 * i + 1][0]
                                                         for i in range(12)), str(pk[:4]))
    ck('P1 ... post ran once per held tick', len(s.post_runs) - r0 == 12)
    s.cam_req = 2
    CS.world(s)
    ck('P1 ... a cut while Shift is held: the client is on camera B', CS.client_on(s) is not None and 'rlk_mb_cam2' in CS.client_on(s))
    pl.data['sneak'] = False
    s.cam_req = 1
    CS.run(s, 3)
    k1 = len(s.cam_packets)
    CS.run(s, 10)
    ck('P2 no key down, nothing changing: no camera packet at all (post is a no-op)', len(s.cam_packets) == k1 and 'rlk_mb_cam1' in CS.client_on(s))
    # the arrival: the client does not have the camera entity when the hold begins (its chunk is not sent yet): the camera
    # packet is ignored, the server counts the camera as set, a plain `spectate` is a no-op -> the 11-11 free flight
    for resend, name in ((0, 'no re-send asked'), (44, 'the module asked for 44 ticks of re-send (CS0)')):
        s, pl = CS.setup(DP)
        CS.fight(s, SID)
        s.pair_later = True
        stands_at(s)
        if resend:
            s.cmd(split(L.cam_resend(resend)), C0)
        s.cam_req = 1
        CS.run(s, 8)
        free = CS.client_on(s) is None and CS.watching(s) is not None
        s.pair_later = False                       # the chunk has been sent: the server pairs the entity in the player's tick
        CS.world(s)
        on = CS.client_on(s) is not None and 'rlk_mb_cam1' in CS.client_on(s)
        if resend:
            ck(f'P3 (VC 6) the camera unknown to the client for 8 ticks, {name}: attached in the tick the client gets the entity',
               free and on, f'{free} {on} {s.cam_packets[-4:]}')
            CS.run(s, 60)
            k2 = len(s.cam_packets)
            CS.run(s, 10)
            ck('P3 ... the re-sends end by themselves', len(s.cam_packets) == k2 and (s.sc('#mbCamRe', 'mb') or 0) == 0)
        else:
            ck(f'P4 (control) {name} beyond the first {L.CAM_RESEND_HOLD} ticks: the client stays on its own view (the bug)', free and not on)
            pl.data['keys'] = {'b', 'jump'}        # the player tries to fly: a movement key
            CS.world(s)
            ck('P4 (VC 6) ... a movement key: the camera is re-sent in that tick, the client is attached (no free flight)',
               CS.client_on(s) is not None and 'rlk_mb_cam1' in CS.client_on(s), str(s.cam_packets[-3:]))
            k3 = len(s.cam_packets)
            CS.run(s, 8)
            n_re = (len(s.cam_packets) - k3) // 2
            ck('P4 ... while the key stays down: re-sent every fourth tick', n_re == 2, str(n_re))
            pl.data['keys'] = set()
            CS.run(s, 2)
            k4 = len(s.cam_packets)
            CS.run(s, 8)
            ck('P4 ... key up: no more packets', len(s.cam_packets) == k4)


# ============================================================================================================ text
def text():
    import math
    sys.path.insert(0, str(DP / 'tools'))
    import mboss_lib as L
    s, pl = held_world()
    line = '{text:"낭자 생각은 어떤가?",color:"#F2D0E8"}'
    hint = '{text:"",extra:[{text:"⊙ 건너뛰기",color:"#FFFFFF"},{text:" · Space 길게",color:"#A8A8B0"}]}'

    def run(lines):
        for ln in lines:
            s.cmd(split(ln), C0)

    def of(cam, tag):
        return [e for e in s.cam_texts(tag) if f'rlk_mb_camx{cam}' in e.tags]
    run(L.cam_line(line))
    tx = s.cam_texts(CS.LINE_TAG)
    lv, idle = of(1, CS.LINE_TAG), of(2, CS.LINE_TAG)
    ck('T1 (VC 10; round W) cam_line: the text on the line display of the LIVE camera only, on a dark backdrop; the idle camera\'s is empty',
       len(tx) == 2 and len(lv) == 1 and len(idle) == 1 and lv[0].data['text'] == '낭자 생각은 어떤가?' and (lv[0].data['bg'] & 0xFF000000) >= 0x80000000
       and (lv[0].data['bg'] & 0xFFFFFF) == 0 and idle[0].data['text'] == '' and idle[0].data['bg'] == 0, str([(e.data['text'], e.data['bg']) for e in tx]))
    run(L.cam_hint(hint))
    hx = s.cam_texts(CS.HINT_TAG)
    ck('T1 cam_hint: on the hint display of the live camera only; the line untouched', len(hx) == 2
       and '건너뛰기' in of(1, CS.HINT_TAG)[0].data['text'] and 'Space' in of(1, CS.HINT_TAG)[0].data['text'] and of(2, CS.HINT_TAG)[0].data['text'] == ''
       and lv[0].data['text'] == '낭자 생각은 어떤가?', str([e.data['text'] for e in hx]))
    # a cut: the other camera live -> mboss/cam/text (cam.py calls it at every cut) moves both texts with it
    s.cam_req = 2
    H.set_mb(s, '#mbCamId', 2) if hasattr(H, 'set_mb') else s.setsc('#mbCamId', 'mb', 2)
    run([L.cam('text')])
    ck('T1 (round W) after a cut (the other camera live + mboss/cam/text): the line and the hint are on the new live camera, the old one\'s are blank',
       of(2, CS.LINE_TAG)[0].data['text'] == '낭자 생각은 어떤가?' and '건너뛰기' in of(2, CS.HINT_TAG)[0].data['text']
       and all(e.data['text'] == '' and e.data['bg'] == 0 for e in of(1, CS.LINE_TAG) + of(1, CS.HINT_TAG)),
       str([(sorted(t for t in e.tags if 'camx' in t), e.data['text']) for e in tx + hx]))
    # a camera made anew (a skip): mboss/cam/kill blanks the store, new cameras start empty
    run(L.cam_line(None))
    run(L.cam_hint(None))
    ck('T1 cleared: empty text, no backdrop', all(e.data['text'] == '' and e.data['bg'] == 0 for e in tx + hx))
    run(L.cam_line(line))
    run([L.cam('kill')])
    st = s.storage.get('rlk:mboss', {}).get('camtx', {})
    ck('T1 (round W) cam/kill: the stored line and hint are blank (a camera made afterwards cannot show an old line)',
       st.get('line') == {'text': '', 'background': 0} and st.get('hint') == {'text': '', 'background': 0}, str(st))
    # the geometry (TextDisplayRenderer: the block's bottom edge is the origin, a line 9 font px of 0.025 x scale; billboard
    # "center": translation x right, y up, z toward the eye, which is 4 b behind the camera entity). Round W: checked at the
    # fields of view 70 / 90 / 110 (mboss_lib.CAM_FOVS; 90 is the user's): the line in the lower part and whole on a 16 : 9
    # picture, the hint in the top right and whole, the two never overlapping, glyph sizes at 1080p
    rows = []
    AR = 16 / 9
    for name, spec, width, need in (('line', L.CAM_LINE, 192, {70: 36, 90: 32, 110: 22}), ('hint', L.CAM_HINT, 96, {70: 20, 90: 18, 110: 12})):
        for fov in L.CAM_FOVS:
            x0, x1, y0, y1 = L.cam_text_box(spec, width, fov)
            glyph = 8 * L.cam_text_px(spec, fov)
            rows.append((name, fov, round((y0 + y1) / 2, 3), round(glyph, 1), round((x1 - x0) * 540)))
            inside = -AR * 0.98 < x0 and x1 < AR * 0.98 and -0.98 < y0 and y1 < 0.98
            where = (y1 < -1 / 3 and abs((x0 + x1) / 2) < 1e-9) if name == 'line' else (y0 > 0.38 and x0 > 0.5)
            ck(f'T2 the {name} at a field of view of {fov:.0f}: whole on a 16 : 9 picture (x {x0:.2f}..{x1:.2f} of +-{AR:.2f}, y {y0:.2f}..{y1:.2f}), '
               f'{"centred in the lower part" if name == "line" else "in the top right"}, glyphs {glyph:.0f} px >= {need[int(fov)]} at 1080p',
               inside and where and glyph >= need[int(fov)])
    for fov in L.CAM_FOVS:
        a, b = L.cam_text_box(L.CAM_LINE, 192, fov), L.cam_text_box(L.CAM_HINT, 96, fov)
        ck(f'T2 at {fov:.0f} the line and the hint do not overlap', b[2] > a[3] + 0.05)
    lt, ht = L.cam_text_geom(L.CAM_LINE), L.cam_text_geom(L.CAM_HINT)
    ck('T2 the texts are 0.3 b before the eye (nothing of a shot is nearer to the lens)', abs(4.0 - lt[1] - 0.3) < 1e-9 and abs(4.0 - ht[1] - 0.3) < 1e-9, f'{lt} {ht}')
    sp = cmds('mboss/cam/spawn')[0]
    tr = re.findall(r'translation:\[(-?[0-9.]+)f,(-?[0-9.]+)f,(-?[0-9.]+)f\]', sp)
    ck('T2 the summon NBT carries that geometry', len(tr) == 2 and abs(float(tr[0][1]) - lt[0]) < 1e-4 and abs(float(tr[1][1]) - ht[0]) < 1e-4
       and abs(float(tr[0][0])) < 1e-9 and abs(float(tr[1][0]) - L.cam_text_tx(L.CAM_HINT)) < 1e-4 and all(abs(float(z) - 3.7) < 1e-9 for _x, _y, z in tr), str(tr))
    print('   text geometry (name, fov, middle y, glyph px, box width px at 1080p):', rows)


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
    # (round V: the tick advancement armed, the movement-key check, mboss/cam/post in the player's own tick)
    ck('C2 a held tick costs at most 24 commands (post included)', max(heldc) <= 24, str(max(heldc)))
    actor_stop = (F / 'char/cine/stop.mcfunction').exists()        # lane H3's actor: the release ends it (its own commands)
    ck(f'C2 the first held tick at most 56, the release tick at most {70 if actor_stop else 50}'
       f'{" (with char/cine/stop, the actor\'s own end)" if actor_stop else ""}', first <= 56 and rel <= (70 if actor_stop else 50), f'{first} {rel}')


# ============================================================================================================ ident
# round V: what lane VC may change outside F:boss/scarlet/**, F:mboss/cam/** and F:char/cine/** (generated): the two hand
# files of the loot line held back during a lock and of the lure's blank skin, the comment of lvup/tick, the tick
# advancement; everything else under data/ must be byte-identical to the base
VC_FILES = ('roguelike/data/rlk/function/combat/sap_absorb.mcfunction', 'roguelike/data/rlk/function/cm/lure_new.mcfunction',
            'roguelike/data/rlk/function/lvup/tick.mcfunction', 'roguelike/data/rlk/function/tick.mcfunction',
            'roguelike/data/rlk/advancement/mboss/cam_post.json')


def other_lanes():
    """Round V integration: on the merged tree the other lanes' files differ from the base too. They are the round V groups of
    ident_hr.py (lane VB: the gauge's dividers; lane VP: the beat and its clock users; the integration's own), read from there;
    round W integration: and the round W groups (lane WP's dodge set, the integration's own)."""
    try:
        import ident_hr as IH
    except Exception as e:      # noqa: BLE001
        print(f'   ident: ident_hr.py not readable ({e}): the other lanes\' files are not excused')
        return []
    return [p for g, p in IH.PATS if g.startswith(('round V', 'round W')) and g != IH.LANE_VC]


BEAT_WORDS = ('#btK cb', '#btAdj cb', '#btHold cb')      # lane VP's lines / conditions in rlk:tick (the beat's clock and gates)


def ident():
    repo = DP.parent
    git = lambda *a: subprocess.run(['git', '-C', str(repo), *a], capture_output=True, text=True)  # noqa: E731
    base = BASE or git('merge-base', 'HEAD', 'origin/wip/v').stdout.strip()
    if not base:
        print('   ident: no base commit (pass --base): SKIPPED')
        return
    names = [l.split('\t')[-1] for l in git('diff', '--name-status', base, '--', 'roguelike/data').stdout.split('\n') if l.strip()]
    names += [p for p in git('ls-files', '--others', '--exclude-standard', '--', 'roguelike/data').stdout.split('\n') if p]
    pre = 'roguelike/data/rlk/function/'
    own = (pre + 'boss/scarlet/', pre + 'mboss/cam/', pre + 'char/cine/')
    other = sorted(n for n in set(names) if not n.startswith(own))
    oth = other_lanes()
    extra = [n for n in other if n not in VC_FILES and not any(p.fullmatch(n[len('roguelike/'):]) for p in oth)]
    ck(f'D1 against {base[:9]}: outside F:boss/scarlet, F:mboss/cam and F:char/cine only lane VC\'s listed files change '
       f'(and the files of the other round V / W lanes: ident_hr.py\'s round V / W groups)', not extra, str(extra))
    for n in other:
        if not n.endswith('.mcfunction') or n not in VC_FILES:
            continue
        d = git('diff', '-U0', base, '--', n).stdout.split('\n')
        add = [l[1:] for l in d if l[:1] == '+' and not l.startswith('+++') and l[1:].strip() and not l[1:].startswith('#')]
        rem = [l[1:] for l in d if l[:1] == '-' and not l.startswith('---') and l[1:].strip() and not l[1:].startswith('#')]
        ck(f'D2 {n.rsplit("/", 2)[-2]}/{n.rsplit("/", 1)[-1]}: every added command is a lock line (rlk_mb_camh / #mbCamSap / the blank skin) '
           'or a line of lane VP\'s beat clock (#btK / #btAdj / #btHold cb); a removed command comes back inside an added one',
           all(any(w in l for w in ('rlk_mb_camh', 'mbCamSap', 'rlk:skin/blank') + BEAT_WORDS) for l in add)
           and all(any(r[:36] in a_ or r[-60:] in a_ for a_ in add) for r in rem), f'{add} {rem}')


SECTIONS = [('static', static), ('hold', hold), ('lock', lock), ('grid', grid), ('client', client), ('post', post), ('text', text),
            ('paths', paths), ('stand', stand), ('idem', idem), ('cost', cost), ('ident', ident)]
for name, f in SECTIONS:
    if want(name):
        print(f'== {name}')
        f()
H.summary("TEST_CAM")
