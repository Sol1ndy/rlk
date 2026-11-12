#!/usr/bin/env python3
"""test_fw_az.py: the framework helpers the chapter bosses (Azhdaha, Apep) need (scratchpad az/contract/cm.md 13, 7.2,
8, 11, 15.3), on cproto in the cp_test arena.

    python3 test_fw_az.py <worktree>/roguelike

 1. N4 mask hazard: safe inside any safe circle of its group with the 0.3 b pad, a horizontal test, other groups do not
    protect, no radius limit, #hzNoDodge, a shared #hzSafeG (two masks, the module's markers survive), own markers expire
 2. N7 events: #mbHitEv / El / Sh / RA / Src for hazards, projectiles, direct calls; #mbDodgeEv / #mbDodgeOk only for a
    one-shot strike (tell >= 12, no re-arm) and projectiles; refused hits set nothing
 3. pl_dot: per mille of max HP, i-frames ignored, no defence, guard then element shield (250 % vs its element),
    non-lethal floor (lethal option), refused while dead / cine / dying, every input reset (incl. a one-shot #mbNoRx set
    for it, which never reaches the next direct hurt; cleanup_fight clears it too: recheck APEP-03)
 4. NoRx: no element/player_hit for #hzNR / #pjNR / #mbNoRx hits; the hit keeps its element; without it the reaction runs
 5. floor: clamp, #mbFloorHit on <=, #mbFloorRaw, true damage bypasses it
 6. per-element RES on an aux object (#auxResEl / #auxResElV) next to its flat RES
 7. cine: hurt and pl_dot refused, the bars stay, cleanup_fight resets it
 8. push ring: radial to `to` over kb ticks, no damage / no event, a landing inside a live hazard is skipped; a far player
    (|dx|, |dz| > 32 b) is never pushed (no int32 overflow), r / to clamped to 320 / 600 (recheck APEP-06)
 9. lockv: ring buffer, dash ticks skipped, v = (newest - oldest) / 5, sprint cap 280 mb/t, lead, walk clamp, re-tag keep
10. mv/local: #mbLf / #mbLs in the anchor frame
11. hz/extend {n}: active window and life grow together
12. #pjNoDodge: the projectile hit ignores the dash i-frames
13. bossui: #buHpCol 0 / #buNoNum 0 draw the M0 line byte for byte (the bossui of the release 22ba247 = M0 039b911's, loaded beside); colour 3 and gold 10;
    no numbers; the options reset after each draw
14. mid-boss fights: mres 0 / no rlk_mb_resel / plaza (#mbAr 0, #mbMode 0) unchanged
15. the mboss_lib call builders
16. merge prep PERF-4: the per-tick body position cache mv/plpos: at most one entity NBT read of the player's body per
    live chapter tick (lv_sample, mv/local, push/capsule, hz/hit_mask, mv/lockv share it; 6 before), a second call in the
    same tick reuses it, the next tick reads again, a push that moved the player and the chapter arena's tp_in drop it
"""
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import cmsim as M  # noqa: E402
from mcsim import Ctx, Ent  # noqa: E402

DP = Path(sys.argv[1]).resolve()
C0 = M.C0
check = M.check
REG = json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
AR = REG['arenas']['cp_test']
REPO = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/az/wt_cm')
if not REPO.exists():                  # the worktree was removed after its merge: any clone of the repo has the commits
    REPO = Path('/home/user/rlk')        # (read-only git commands: archive / ls-tree / show)


def st(s):
    return s.storage.setdefault('rlk:mboss', {})


def logged(s):
    log = []
    orig = s.call

    def call(fid, ctx, macro=None):
        log.append((s.t, fid, ctx.ex, tuple(ctx.pos), dict(macro) if macro else None))
        if fid == 'rlk:cm/hit_pl2' and getattr(s, 'ifr', False) and (s.sc('#mbNoDodge', 'mb') or 0) != 1 and ctx.ex is not None:
            s.setsc(('e', ctx.ex.id), 'dashInvT', 1)      # i-frames at the moment of the hit (a no-dodge hit ignores them)
        if fid == 'rlk:cm/hit_pl2' and getattr(s, 'pdg', False) and ctx.ex is not None:
            # combat overhaul C: a dodge started this tick (the stamp player/def/dodge_stamp writes) = a perfect dodge
            for o in ('parAt', 'parLk', 'parHit', 'dgRw'):
                if s.sc(('e', ctx.ex.id), o) is None:
                    s.setsc(('e', ctx.ex.id), o, -1000000)
            s.setsc(('e', ctx.ex.id), 'dgAt', s.t)
        return orig(fid, ctx, macro)
    s.call = call
    return log


def setup():
    s, pl = M.setup(DP)
    s.setsc('#chapter', 'room', 2)
    log = logged(s)
    M.fight(s, 'cproto', 2)
    s.setsc('#cpCool', 'mb', 99999)      # no boss pattern: every hazard here is the test's
    s.setsc('#cpPat', 'mb', 0)
    s.call('rlk:mboss/lib_clear', C0)
    for o, v in (('curHealth', 5000), ('maxHealth', 5000), ('def', 0), ('dashInvT', 0), ('shieldHP', 0), ('gShield', 0)):
        s.setsc(('e', pl.id), o, v)
    return s, pl, log, M.body_of(s)


def hp(s, pl):
    return s.sc(('e', pl.id), 'curHealth')


def at(x, z, y=201.0):
    return Ctx(None, (x, y, z), (0.0, 0.0))


def iframes(s, pl, on):
    """The dash i-frames: dashInvT 1 for every player hit (the harness world tick resets the score, so the call wrapper
    sets it right before cm/hit_pl2) and the score itself (pl_dot reads it)."""
    s.ifr = on
    s.setsc(('e', pl.id), 'dashInvT', 1 if on else 0)


def events(s):
    return {k: M.mb(s, k) or 0 for k in ('#mbHitEv', '#mbHitEl', '#mbHitSh', '#mbHitRA', '#mbHitSrc', '#mbDodgeEv', '#mbDodgeOk')}


def clear_events(s):
    for k in ('#mbHitEv', '#mbDodgeEv', '#mbDodgeOk', '#mbHitRA', '#mbHitSh', '#mbHitSrc', '#mbHitEl'):
        s.setsc(k, 'mb', 0)


def opt(s, **kw):
    for k, v in kw.items():
        s.setsc('#' + k, 'mb', v)


def mask(s, cx, cz, r0=25, tell=20, dmg=50, safe=(), group=0, **kw):
    """hz/mask at (cx, cz) with safe markers at `safe` (their mbHzSG = the resolved group)."""
    opt(s, hzR0=r0, hzSafeG=group, **kw)
    s.call('rlk:mboss/hz/mask', at(cx, cz), {'tell': tell, 'dmg': dmg})
    g = group or M.mb(s, '#hzLast')
    for (x, z, *y) in safe:
        e = Ent('marker', (x, y[0] if y else 201.0, z), tags=['rlk_room', 'rlk_mb_aux', 'rlk_mb_hzsafe'])
        s.ents.append(e)
        s.setsc(('e', e.id), 'mbHzSG', g)
    return M.mb(s, '#hzLast'), g


CX, CZ = AR['cx'], AR['cz']

# ------------------------------------------------------------------------------------------------- 1 mask
print('== 1. N4 mask hazard')
cases = [('inside the circle', (CX + 1.0, CZ), False), ('inside the 0.3 pad (2.75 b)', (CX + 2.75, CZ), False),
         ('just outside the pad (2.9 b)', (CX + 2.9, CZ), True), ('far away (9 b, no radius limit)', (CX - 9.0, CZ), True)]
for label, (px_, pz), hit in cases:
    s, pl, log, b = setup()
    pl.pos = [px_, 201.0, pz]
    M.moved(s)
    h0 = hp(s, pl)
    hid, g = mask(s, CX, CZ, safe=[(CX, CZ)])
    m = [e for e in s.ents if e.alive and 'rlk_mb_hz' in e.tags and M.esc(s, e, 'mbHzI') == hid][0]
    check(f'1a {label}: the mask stores its resolved group (own id {hid})', M.esc(s, m, 'mbHzSG') == hid and M.esc(s, m, 'mbHzK') == 6)
    M.run(s, 24)
    check(f'1b {label}: {"hit" if hit else "safe"}', (hp(s, pl) < h0) == hit, (h0, hp(s, pl)))
s, pl, log, b = setup()
pl.pos = [CX + 0.5, 201.0, CZ]
M.moved(s)
h0 = hp(s, pl)
mask(s, CX, CZ, safe=[(CX, CZ, 204.0)])
M.run(s, 24)
check('1c horizontal test: a safe marker 3 b above still protects', hp(s, pl) == h0)
s, pl, log, b = setup()
pl.pos = [CX + 0.5, 201.0, CZ]
M.moved(s)
h0 = hp(s, pl)
hid, g = mask(s, CX, CZ)
e = Ent('marker', (CX, 201.0, CZ), tags=['rlk_room', 'rlk_mb_aux', 'rlk_mb_hzsafe'])
s.ents.append(e)
s.setsc(('e', e.id), 'mbHzSG', g + 1000)
M.run(s, 24)
check('1d a safe marker of another group does not protect', hp(s, pl) < h0)
s, pl, log, b = setup()
pl.pos = [CX + 6.0, 201.0, CZ]
M.moved(s)
iframes(s, pl, True)
h0 = hp(s, pl)
mask(s, CX, CZ, safe=[(CX, CZ)])
M.run(s, 24)
check('1e dash i-frames dodge a normal mask (no HP lost, a dodge event)', hp(s, pl) == h0 and (M.mb(s, '#mbDodgeEv') or 0) >= 1)
s, pl, log, b = setup()
pl.pos = [CX + 6.0, 201.0, CZ]
M.moved(s)
iframes(s, pl, True)
h0 = hp(s, pl)
mask(s, CX, CZ, safe=[(CX, CZ)], hzNoDodge=1)
M.run(s, 24)
check('1f #hzNoDodge: the mask lands through the i-frames', hp(s, pl) < h0)
s, pl, log, b = setup()
pl.pos = [CX + 0.5, 201.0, CZ + 5.0]
M.moved(s)
h0 = hp(s, pl)
h1, _ = mask(s, CX, CZ, group=7, tell=20)
h2, _ = mask(s, CX, CZ, group=7, tell=22, safe=[(CX, CZ + 5.0)])
ms = [e for e in s.ents if e.alive and 'rlk_mb_hz' in e.tags and M.esc(s, e, 'mbHzI') in (h1, h2)]
check('1g shared #hzSafeG 7: both masks store group 7', sorted(M.esc(s, e, 'mbHzSG') for e in ms) == [7, 7])
M.run(s, 40)
safe_left = [e for e in s.ents if e.alive and 'rlk_mb_hzsafe' in e.tags]
check('1h both masks spare the player inside the shared circle; after they expire the module\'s markers survive',
      hp(s, pl) == h0 and len(safe_left) == 1, (h0, hp(s, pl), len(safe_left)))
s, pl, log, b = setup()
pl.pos = [CX + 0.5, 201.0, CZ]
M.moved(s)
mask(s, CX, CZ, tell=10, safe=[(CX, CZ), (CX + 3.0, CZ)])
M.run(s, 40)
check('1i a mask made with #hzSafeG 0 takes its own safe markers when it expires (hz/mask_end)',
      not [e for e in s.ents if e.alive and 'rlk_mb_hzsafe' in e.tags])

# ------------------------------------------------------------------------------------------------- 2 events
print('== 2. N7 hit / dodge events')


def disc(s, x, z, r=30, tell=20, dmg=50, **kw):
    opt(s, **kw)
    s.call('rlk:mboss/hz/disc', at(x, z), {'r': r, 'tell': tell, 'dmg': dmg})
    return M.mb(s, '#hzLast')


s, pl, log, b = setup()
pl.pos = [CX, 201.0, CZ]
M.moved(s)
clear_events(s)
disc(s, CX, CZ, hzEl=3)
M.run(s, 24)
ev = events(s)
check('2a a landed hazard: #mbHitEv 1, #mbHitEl = its element, #mbHitSrc 1, #mbHitRA 0, #mbHitSh 0',
      ev['#mbHitEv'] == 1 and ev['#mbHitEl'] == 3 and ev['#mbHitSrc'] == 1 and ev['#mbHitRA'] == 0 and ev['#mbHitSh'] == 0, ev)
clear_events(s)
s.setsc(('e', pl.id), 'shieldHP', 500)
s.setsc(('e', pl.id), 'shieldT', 400)
disc(s, CX, CZ, hzRearm=10, hzAct=30)
M.run(s, 24)
ev = events(s)
check('2b a re-arming hazard with a shield up: #mbHitRA 1, #mbHitSh 1', ev['#mbHitEv'] >= 1 and ev['#mbHitRA'] == 1 and ev['#mbHitSh'] == 1, ev)
s.setsc(('e', pl.id), 'shieldHP', 0)
s.call('rlk:mboss/lib_clear', C0)
# combat overhaul C (11-10): #mbDodgeOk = a perfect dodge / perfect parry (the timing judge, any tell) of a non-re-arming
# attack; i-frames (burst, revive, fall) give the dodge event only
for tell, how, ok in ((20, 'pdg', 1), (8, 'pdg', 1), (20, 'ifr', 0)):
    clear_events(s)
    iframes(s, pl, how == 'ifr')
    s.pdg = how == 'pdg'
    disc(s, CX, CZ, tell=tell)
    M.run(s, tell + 4)
    ev = events(s)
    check(f'2c a {"perfect-dodged" if how == "pdg" else "i-frame-dodged"} one-shot strike with tell {tell}: #mbDodgeEv 1, '
          f'#mbDodgeOk {ok}', ev['#mbDodgeEv'] == 1 and ev['#mbDodgeOk'] == ok and ev['#mbHitEv'] == 0, ev)
clear_events(s)
iframes(s, pl, False)
s.pdg = True
disc(s, CX, CZ, tell=20, hzRearm=10, hzAct=12)
M.run(s, 24)
ev = events(s)
check('2d a perfect-dodged re-arming hazard: dodge events but #mbDodgeOk 0', ev['#mbDodgeEv'] >= 1 and ev['#mbDodgeOk'] == 0, ev)
s.pdg = False
iframes(s, pl, False)
s.call('rlk:mboss/lib_clear', C0)
clear_events(s)
s.setsc('#mbHitPct', 'mb', 50)
s.setsc('#cmEl', 'tmp', 0)
s.call('rlk:mboss/hurt', Ctx(b, tuple(b.pos), (0, 0)))
ev = events(s)
check('2e a direct mboss/hurt: #mbHitSrc 3', ev['#mbHitEv'] == 1 and ev['#mbHitSrc'] == 3, ev)
clear_events(s)
s.setsc(('e', pl.id), 'dead', 1)
s.call('rlk:mboss/hurt', Ctx(b, tuple(b.pos), (0, 0)))
s.setsc(('e', pl.id), 'dead', 0)
check('2f a refused hit (dead) sets no event', events(s)['#mbHitEv'] == 0 and events(s)['#mbDodgeEv'] == 0)


def projectile(s, b, pl, nododge=0, norx=0, el=-1):
    e = Ent('block_display', (b.pos[0], b.pos[1] + 1.2, b.pos[2]), (0.0, 0.0), ['rlk_room', 'rlk_mb_aux', 'rlk_mb_fwpj'])
    s.ents.append(e)
    opt(s, pjNoDodge=nododge, pjNR=norx, pjEl=el)
    dx, dz = pl.pos[0] - e.pos[0], pl.pos[2] - e.pos[2]
    yaw = math.degrees(math.atan2(-dx, dz))
    s.call('rlk:mboss/pj/launch', Ctx(e, tuple(e.pos), (yaw, 0.0)), {'spd': 5, 'life': 60, 'dmg': 60, 'hr': 6})
    return e


s, pl, log, b = setup()
pl.pos = [b.pos[0], 201.0, b.pos[2] + 4.0]
M.moved(s)
clear_events(s)
s.pdg = True
projectile(s, b, pl)
M.run(s, 30)
s.pdg = False
ev = events(s)
check('2g a perfect-dodged projectile: #mbDodgeEv 1, #mbDodgeOk 1', ev['#mbDodgeEv'] == 1 and ev['#mbDodgeOk'] == 1, ev)

# ------------------------------------------------------------------------------------------------- 3 pl_dot
print('== 3. pl_dot')


def dot(s, pct=30, el=0, lethal=0):
    opt(s, mbDotPct=pct, mbDotEl=el, mbDotLethal=lethal)
    s.call('rlk:mboss/pl_dot', C0)
    return M.mb(s, '#mbDotDmg')


s, pl, log, b = setup()
d = dot(s)
check('3a 30 per mille of max HP 5000 = 150 HP, #mbDotDmg 150', hp(s, pl) == 4850 and d == 150, (hp(s, pl), d))
check('3b every input reset after the call', all((M.mb(s, k) or 0) == 0 for k in ('#mbDotPct', '#mbDotEl', '#mbDotLethal')))
iframes(s, pl, True)
h0 = hp(s, pl)
dot(s)
check('3c dash i-frames do not block it (and are restored)', hp(s, pl) == h0 - 150 and s.sc(('e', pl.id), 'dashInvT') == 1)
iframes(s, pl, False)
s.setsc(('e', pl.id), 'def', 400)
h0 = hp(s, pl)
dot(s)
check('3d no defence', hp(s, pl) == h0 - 150)
s.setsc(('e', pl.id), 'def', 0)
s.setsc(('e', pl.id), 'gShield', 100)
s.setsc(('e', pl.id), 'shieldHP', 1000)
s.setsc(('e', pl.id), 'shieldT', 400)
s.setsc(('e', pl.id), 'shieldEl', 1)
h0 = hp(s, pl)
dot(s, pct=60, el=1)
check('3e guard shield first (100), then the pyro shield at 250 % (200 dmg -> 80 shield)', s.sc(('e', pl.id), 'gShield') == 0
      and s.sc(('e', pl.id), 'shieldHP') == 920 and hp(s, pl) == h0, (s.sc(('e', pl.id), 'gShield'), s.sc(('e', pl.id), 'shieldHP'), h0 - hp(s, pl)))
s.setsc(('e', pl.id), 'shieldHP', 0)
s.setsc(('e', pl.id), 'curHealth', 10)
dot(s, pct=900)
check('3f non-lethal: the player keeps 1 HP', hp(s, pl) == 1)
dot(s, pct=900, lethal=1)
check('3g #mbDotLethal 1: can kill', hp(s, pl) == 0)
s.setsc(('e', pl.id), 'curHealth', 5000)
for gate, fn in (('dead', lambda s: s.setsc(('e', pl.id), 'dead', 1)), ('cine', lambda s: s.setsc('#mbCine', 'mb', 1)),
                 ('dying (#mbSt 2)', lambda s: s.setsc('#mbSt', 'mb', 2)), ('selection', lambda s: s.setsc(('e', pl.id), 'pkMode', 1))):
    fn(s)
    d = dot(s)
    check(f'3h refused while {gate}: no HP lost, #mbDotDmg 0, inputs reset', hp(s, pl) == 5000 and d == 0 and (M.mb(s, '#mbDotPct') or 0) == 0)
    s.setsc(('e', pl.id), 'dead', 0)
    s.setsc('#mbCine', 'mb', 0)
    s.setsc('#mbSt', 'mb', 1)
    s.setsc(('e', pl.id), 'pkMode', 0)
check('3i no hit event from a DoT', (M.mb(s, '#mbHitEv') or 0) == 0)
s, pl, log, b = setup()
s.setsc('#mbNoRx', 'mb', 1)
dot(s, pct=30, el=7)
nr = M.mb(s, '#mbNoRx') or 0
i0 = len(log)
s.setsc('#mbHitPct', 'mb', 50)
s.setsc('#cmEl', 'tmp', 1)
s.call('rlk:mboss/hurt', Ctx(b, tuple(b.pos), (0, 0)))
check('3j a one-shot #mbNoRx set for a pl_dot is spent by it: the next direct pyro hurt runs element/player_hit',
      nr == 0 and any(r[1] == 'rlk:element/player_hit' for r in log[i0:]), nr)
s.setsc('#mbNoRx', 'mb', 1)
s.call('rlk:mboss/cleanup_fight', C0)
check('3k cleanup_fight clears a pending #mbNoRx', (M.mb(s, '#mbNoRx') or 0) == 0)

# ------------------------------------------------------------------------------------------------- 4 NoRx
print('== 4. NoRx')
for label, kw, want in (('#hzNR 1', {'hzNR': 1}, False), ('no option', {}, True)):
    s, pl, log, b = setup()
    pl.pos = [CX, 201.0, CZ]
    M.moved(s)
    i0 = len(log)
    disc(s, CX, CZ, hzEl=1, **kw)
    M.run(s, 24)
    ran = any(r[1] == 'rlk:element/player_hit' for r in log[i0:])
    check(f'4a a pyro hazard with {label}: element/player_hit {"runs" if want else "skipped"}; the hit landed with element 1',
          ran == want and M.mb(s, '#mbHitEl') == 1 and hp(s, pl) < 5000, (ran, M.mb(s, '#mbHitEl')))
s, pl, log, b = setup()
pl.pos = [b.pos[0], 201.0, b.pos[2] + 4.0]
M.moved(s)
i0 = len(log)
projectile(s, b, pl, norx=1, el=1)
M.run(s, 30)
check('4b a projectile with #pjNR 1: no element/player_hit, the hit landed', not any(r[1] == 'rlk:element/player_hit' for r in log[i0:])
      and hp(s, pl) < 5000)
i0 = len(log)
s.setsc('#mbNoRx', 'mb', 1)
s.setsc('#mbHitPct', 'mb', 50)
s.setsc('#cmEl', 'tmp', 1)
s.call('rlk:mboss/hurt', Ctx(b, tuple(b.pos), (0, 0)))
check('4c a direct hurt with one-shot #mbNoRx: skipped, then reset (#mbNoRx 0, #mbNRNow 0)', not any(r[1] == 'rlk:element/player_hit' for r in log[i0:])
      and (M.mb(s, '#mbNoRx') or 0) == 0 and (M.mb(s, '#mbNRNow') or 0) == 0)

# ------------------------------------------------------------------------------------------------- 5 floor
print('== 5. floor')
s, pl, log, b = setup()
s.setsc('#mbFloor', 'mb', 4000)
s.setsc(('e', b.id), 'mhpC', 5000)
s.setsc(('e', b.id), 'mhpM', 100000)
for k, v in (('#dmg', 999999), ('#trueDmg', 0)):
    s.setsc(k, 'tmp', v)
s.setsc('#mbFloorHit', 'mb', 0)
s.call('rlk:mboss/floor', Ctx(b, tuple(b.pos), (0, 0)))
check('5a clamp: #dmg = mhpC - floor (1000), #mbFloorHit 1, #mbFloorRaw = the raw 999999', s.sc('#dmg', 'tmp') == 1000
      and M.mb(s, '#mbFloorHit') == 1 and M.mb(s, '#mbFloorRaw') == 999999)
s.setsc('#mbFloorHit', 'mb', 0)
s.setsc('#dmg', 'tmp', 1000)
s.call('rlk:mboss/floor', Ctx(b, tuple(b.pos), (0, 0)))
check('5b a hit that lands exactly on the floor (mhpC - dmg = floor) sets #mbFloorHit', M.mb(s, '#mbFloorHit') == 1 and s.sc('#dmg', 'tmp') == 1000)
s.setsc('#mbFloorHit', 'mb', 0)
s.setsc('#dmg', 'tmp', 999)
s.call('rlk:mboss/floor', Ctx(b, tuple(b.pos), (0, 0)))
check('5c above the floor: unchanged, no #mbFloorHit', M.mb(s, '#mbFloorHit') == 0 and s.sc('#dmg', 'tmp') == 999)
s.setsc('#mbFloor', 'mb', 0)
s.setsc('#dmg', 'tmp', 999999)
s.call('rlk:mboss/floor', Ctx(b, tuple(b.pos), (0, 0)))
check('5d #mbFloor 0: no clamp', s.sc('#dmg', 'tmp') == 999999)
s.setsc('#mbFloor', 'mb', 4000)
s.setsc(('e', b.id), 'mhpC', 5000)
s.setsc('#mbTrue', 'mb', 4500)
s.setsc('#mbTrueEl', 'mb', 0)
s.call('rlk:mboss/true_hit', Ctx(b, tuple(b.pos), (0, 0)))
check('5e true damage bypasses the floor (mboss/true_hit)', M.esc(s, b, 'mhpC') < 4000, M.esc(s, b, 'mhpC'))

# ------------------------------------------------------------------------------------------------- 6 aux RES
print('== 6. per-element RES on an aux object')
s, pl, log, b = setup()
s.call('rlk:mboss/cproto/test', Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 50})
aux = [e for e in s.ents if e.alive and 'rlk_mb_cproto_aux' in e.tags]
check('6a cproto test 50 made an aux object with rlk_mb_resel', aux and 'rlk_mb_resel' in aux[0].tags, aux and sorted(aux[0].tags))
if aux:
    a = aux[0]
    check('6b aux RES: element 1 = #auxResElV 50, the others = #auxRes 10', M.esc(s, a, 'mbRes1') == 50
          and all(M.esc(s, a, f'mbRes{k}') == 10 for k in (0, 2, 3, 4, 5, 6, 7, 8)), [M.esc(s, a, f'mbRes{k}') for k in range(9)])
    s.call('rlk:combat/melee_begin', Ctx(pl, tuple(pl.pos), (0, 0)))
    for k, v in (('#dmg', 1000), ('#elem', 1), ('#crit', 0), ('#trueDmg', 0), ('#elU', 0), ('#icd', 0)):
        s.setsc(k, 'tmp', v)
    i0 = len(log)
    s.call('rlk:mboss/res_pre', Ctx(a, tuple(a.pos), (0, 0)))
    check('6c res_pre on the aux picks mres = mbRes<#elem> (50)', M.esc(s, a, 'mres') == 50, M.esc(s, a, 'mres'))

# ------------------------------------------------------------------------------------------------- 7 cine
print('== 7. cine')
s, pl, log, b = setup()
s.call('rlk:mboss/cproto/test', Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 7})
check('7a cine/start: #mbCine 1', M.mb(s, '#mbCine') == 1)
pl.pos = [CX, 201.0, CZ]
M.moved(s)
clear_events(s)
disc(s, CX, CZ, tell=5)
M.run(s, 8)
check('7b hurt refused during the cine (no HP lost, no event)', hp(s, pl) == 5000 and (M.mb(s, '#mbHitEv') or 0) == 0)
check('7c pl_dot refused during the cine', dot(s) == 0 and hp(s, pl) == 5000)
check('7d the bars stay (mboss/bars ran during the cine)', any(r[1] == 'rlk:mboss/bars' for r in log[-400:]))
s.call('rlk:mboss/cleanup_fight', C0)
check('7e cleanup_fight resets #mbCine', (M.mb(s, '#mbCine') or 0) == 0)

# ------------------------------------------------------------------------------------------------- 8 push ring
print('== 8. push ring')
s, pl, log, b = setup()
pl.pos = [b.pos[0] + 3.0, 201.0, b.pos[2]]
M.moved(s)
h0 = hp(s, pl)
clear_events(s)
s.call('rlk:mboss/push/ring', Ctx(b, tuple(b.pos), (0, 0)), {'r': 60, 'to': 65, 'kb': 4})
M.run(s, 6)
d = math.hypot(pl.pos[0] - b.pos[0], pl.pos[2] - b.pos[2])
check('8a a player within r (3 b < 6 b) ends at `to` (6.5 b) on its bearing; no damage, no event',
      abs(d - 6.5) < 0.15 and abs(pl.pos[2] - b.pos[2]) < 0.05 and hp(s, pl) == h0 and (M.mb(s, '#mbHitEv') or 0) == 0, (round(d, 3), pl.pos))
pl.pos = [b.pos[0] + 7.0, 201.0, b.pos[2]]
M.moved(s)
s.call('rlk:mboss/push/ring', Ctx(b, tuple(b.pos), (0, 0)), {'r': 60, 'to': 65, 'kb': 4})
M.run(s, 6)
check('8b a player outside r is not moved', abs(pl.pos[0] - (b.pos[0] + 7.0)) < 1e-6)
pl.pos = [b.pos[0] + 3.0, 201.0, b.pos[2]]
M.moved(s)
disc(s, b.pos[0] + 6.5, b.pos[2], r=15, tell=40)
s.call('rlk:mboss/push/ring', Ctx(b, tuple(b.pos), (0, 0)), {'r': 60, 'to': 65, 'kb': 4})
M.run(s, 6)
check('8c a landing point inside a live hazard disc: skipped (not moved)', abs(pl.pos[0] - (b.pos[0] + 3.0)) < 1e-6, pl.pos)
for dxy in (30.0, 33.0, 34.0):
    s, pl, log, b = setup()
    anc = Ent('marker', (b.pos[0] - dxy / 2, 201.0, b.pos[2] - dxy / 2), tags=['rlk_room', 'rlk_mb_aux'])
    s.ents.append(anc)
    pl.pos = [anc.pos[0] + dxy, 201.0, anc.pos[2] + dxy]
    M.moved(s)
    i0 = len(log)
    s.call('rlk:mboss/push/ring', Ctx(anc, tuple(anc.pos), (0, 0)), {'r': 80, 'to': 85, 'kb': 4})
    ran = sorted({r[1] for r in log[i0:] if r[1] in ('rlk:mboss/push/ring_start', 'rlk:mboss/push/ring_land', 'rlk:mboss/pull/start')})
    check(f'8d a player {dxy} b / {dxy} b from a ring of 8 b is not pushed (no int32 overflow)', not ran, ran)
s, pl, log, b = setup()
pl.pos = [b.pos[0] + 40.0, 201.0, b.pos[2]]
M.moved(s)
s.call('rlk:mboss/push/ring', Ctx(b, tuple(b.pos), (0, 0)), {'r': 900, 'to': 2000, 'kb': 4})
check('8e r and to are clamped to 320 / 600 tenths (a player 40 b out is outside even an r 90 b ring)',
      M.mb(s, '#prR') == 320 and M.mb(s, '#prTo') == 600 and abs(pl.pos[0] - (b.pos[0] + 40.0)) < 1e-6, (M.mb(s, '#prR'), M.mb(s, '#prTo')))
for label, cx, cz in (('the arena centre', AR['cx'], AR['cz']), ('a far corner (start 40 b away on x)', AR['start']['x'] - 40.0, AR['start']['z'] + 10.0)):
    s, pl, log, b = setup()
    anc = Ent('marker', (cx, 201.0, cz), tags=['rlk_room', 'rlk_mb_aux'])
    s.ents.append(anc)
    pl.pos = [cx, 201.0, cz]
    M.moved(s)
    i0 = len(log)
    s.call('rlk:mboss/push/ring', Ctx(anc, tuple(anc.pos), (0, 0)), {'r': 30, 'to': 35, 'kb': 4})
    pp = [e for e in s.ents if e.alive and 'rlk_mb_pullpt' in e.tags]
    sx, sz = AR['start']['x'] - cx, AR['start']['z'] - cz
    ok = False
    if pp:
        dx, dz = pp[0].pos[0] - cx, pp[0].pos[2] - cz
        ok = abs(math.hypot(dx, dz) - 3.5) < 0.05 and abs(math.atan2(dx, dz) - math.atan2(sx, sz)) < 0.01
    check(f'8f a player at the ring centre ({label}) is aimed at `to` on the bearing to the arena start (ring_start)', ok,
          [round(v, 3) for v in pp[0].pos] if pp else sorted({r[1] for r in log[i0:] if 'push' in r[1] or 'pull' in r[1]}))

# ------------------------------------------------------------------------------------------------- 9 lockv
print('== 9. lockv')
s, pl, log, b = setup()
s.call('rlk:mboss/lib_clear', C0)
x0 = CX - 4.0
pl.pos = [x0, 201.0, CZ]
M.moved(s)
for i in range(8):
    pl.pos[0] = x0 + 0.1 * i
    M.run(s, 1)
lv = st(s).get('lv', [])
check('9a the ring buffer holds 6 samples of the player (x in mb)', len(lv) == 6 and lv[-1]['x'] == round((x0 + 0.7) * 1000), lv[-2:])
s.setsc(('e', pl.id), 'dashMoveT', 1)
pl.pos[0] = x0 + 3.0
M.run(s, 1)
check('9b a dash tick is skipped (the buffer keeps the last non-dash sample)', st(s)['lv'][-1]['x'] == round((x0 + 0.7) * 1000))
s.setsc(('e', pl.id), 'dashMoveT', 0)
pl.pos[0] = x0 + 0.7
M.run(s, 1)
for i in range(5):
    pl.pos[0] = x0 + 0.7 + 0.1 * (i + 1)
    M.run(s, 1)
s.call('rlk:mboss/mv/lockv', Ctx(b, tuple(b.pos), (0, 0)), {'lead': 10})
lk = [e for e in s.ents if e.alive and 'rlk_mb_lock' in e.tags]
check('9c v = (newest - oldest) / 5 = 100 mb/t along x, #mbV 100', M.mb(s, '#mbVx') == 100 and M.mb(s, '#mbVz') == 0 and M.mb(s, '#mbV') == 100,
      (M.mb(s, '#mbVx'), M.mb(s, '#mbVz'), M.mb(s, '#mbV')))
check('9d the lock marker at p + v x lead (1 b ahead), y = the arena cy', len(lk) == 1 and abs(lk[0].pos[0] - (pl.pos[0] + 1.0)) < 0.02
      and lk[0].pos[1] == AR['cy'], lk and lk[0].pos)
st(s)['lv'] = [{'x': int((CX - 5) * 1000) + 3000 * i, 'z': CZ * 1000} for i in range(6)]
s.call('rlk:mboss/mv/lockv', Ctx(b, tuple(b.pos), (0, 0)), {'lead': 10})
lk = [e for e in s.ents if e.alive and 'rlk_mb_lock' in e.tags]
dm = math.hypot(lk[0].pos[0] - CX, lk[0].pos[2] - CZ) if lk else 99
check('9e sprint cap: |v| 3000 -> 280 mb/t; the far lock point is clamped inside walk - 0.7; one marker (the old one killed)',
      M.mb(s, '#mbV') == 280 and abs(M.mb(s, '#mbVx') - 280) <= 1 and len(lk) == 1 and dm <= AR['walk'] - 0.7 + 0.05, (M.mb(s, '#mbV'), M.mb(s, '#mbVx'), round(dm, 2)))
lk[0].tags.discard('rlk_mb_lock')
lk[0].tags.add('rlk_mb_cp_kept')
s.call('rlk:mboss/mv/lockv', Ctx(b, tuple(b.pos), (0, 0)), {'lead': 0})
check('9f a kept marker (rlk_mb_lock removed by the module) survives the next lockv', lk[0].alive
      and len([e for e in s.ents if e.alive and 'rlk_mb_lock' in e.tags]) == 1)

# ------------------------------------------------------------------------------------------------- 10 local
print('== 10. mv/local')
s, pl, log, b = setup()
b.rot = [90.0, 0.0]           # facing -x
pl.pos = [b.pos[0] - 3.0, 201.0, b.pos[2] - 1.0]
M.moved(s)
s.call('rlk:mboss/mv/local', Ctx(b, tuple(b.pos), tuple(b.rot)))
check('10a anchor yaw 90 (facing -x): a player 3 b ahead and 1 b to the right -> #mbLf 3000, #mbLs -1000',
      abs(M.mb(s, '#mbLf') - 3000) <= 5 and abs(M.mb(s, '#mbLs') + 1000) <= 5, (M.mb(s, '#mbLf'), M.mb(s, '#mbLs')))

# ------------------------------------------------------------------------------------------------- 11 extend
print('== 11. hz/extend')
s, pl, log, b = setup()
s.call('rlk:mboss/cproto/test', Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 60})
hz = [e for e in s.ents if e.alive and 'rlk_mb_hz' in e.tags and M.esc(s, e, 'mbHzI') == M.mb(s, '#hzLast')]
check('11a cproto test 60: hz/extend {n:40} grows mbHzA and mbHzL by 40 (80 + 40 active)', hz and M.esc(s, hz[0], 'mbHzA') == 120,
      hz and (M.esc(s, hz[0], 'mbHzA'), M.esc(s, hz[0], 'mbHzL')))

# ------------------------------------------------------------------------------------------------- 12 pjNoDodge
print('== 12. #pjNoDodge')
for nd in (1, 0):
    s, pl, log, b = setup()
    pl.pos = [b.pos[0], 201.0, b.pos[2] + 4.0]
    M.moved(s)
    iframes(s, pl, True)
    projectile(s, b, pl, nododge=nd)
    M.run(s, 30)
    check(f'12a #pjNoDodge {nd}: the projectile {"lands through" if nd else "is dodged by"} the i-frames', (hp(s, pl) < 5000) == bool(nd), hp(s, pl))

# ------------------------------------------------------------------------------------------------- 13 bossui
print('== 13. bossui options')


def m0_bossui():
    out = subprocess.run(['git', '-C', str(REPO), 'ls-tree', '-r', '--full-tree', '--name-only', '22ba247',
                          'roguelike/data/rlk/function/bossui'], capture_output=True, text=True, check=True).stdout.split()
    fs = {}
    for n in out:
        txt = subprocess.run(['git', '-C', str(REPO), 'show', f'22ba247:{n}'], capture_output=True, text=True, check=True).stdout
        fs['rlk:bossui/' + n.split('/bossui/')[1][:-len('.mcfunction')]] = [l for l in txt.split('\n')]
    return fs


def draw(s, b, hpv, mx, sub=0, submax=1, col=0, hpcol=None, nonum=None):
    for k, v in (('#buHp', hpv), ('#buMax', mx), ('#buSub', sub), ('#buSubMax', submax), ('#buSubCol', col)):
        s.setsc(k, 'bu', v)
    if hpcol is not None:
        s.setsc('#buHpCol', 'bu', hpcol)
    if nonum is not None:
        s.setsc('#buNoNum', 'bu', nonum)
    s.call('rlk:bossui/draw', Ctx(b, tuple(b.pos), (0, 0)))
    return json.dumps(s.storage.get('rlk:bu', {}).get('line'), ensure_ascii=False, sort_keys=True)


s, pl, log, b = setup()
s.cache.pop('rlk:bossui/draw', None)          # fgsim stubs the bar drawing
s.call('rlk:bossui/init', C0)
cases = [(30000, 60000, 0, 1, 0), (1, 100000, 50, 100, 3), (60000, 60000, 7, 9, 8)]
now = [draw(s, b, *c) for c in cases]
s0, pl0 = M.setup(DP)
s0.cache.pop('rlk:bossui/draw', None)
for k, v in m0_bossui().items():
    s0.cache[k] = v
s0.call('rlk:bossui/init', C0)
b0 = Ent('husk', (0.0, 201.0, 0.0), tags=['rlk_mb_body'])
s0.ents.append(b0)
old = [draw(s0, b0, *c) for c in cases]
check('13a #buHpCol / #buNoNum unset or 0: the drawn line equals M0\'s for every case', now == old, [i for i in range(3) if now[i] != old[i]])
s.call('rlk:bossui/init', C0)
line = json.loads(draw(s, b, 30000, 60000, hpcol=3))
check('13b #buHpCol 3: the HP run in SUB_COLORS[3] (#4FB8FF)', line and line[0].get('color') == '#4FB8FF', line[:1])
check('13c ... and the options reset after the draw', (s.sc('#buHpCol', 'bu') or 0) == 0 and (s.sc('#buNoNum', 'bu') or 0) == 0)
line = json.loads(draw(s, b, 30000, 60000, hpcol=10))
check('13d #buHpCol 10: gold #EDCF63', line and line[0].get('color') == '#EDCF63')
line = json.loads(draw(s, b, 30000, 60000, nonum=1))
check('13e #buNoNum 1: no hp/max numbers (no score component)', line and not any('score' in x for x in line))
s.setsc('#buHpCol', 'bu', 3)
s.call('rlk:mboss/bars', Ctx(b, tuple(b.pos), (0, 0)))
check('13f mboss/bars resets the options before d/bars every call (cproto phase 1 sets none)', (s.sc('#buHpCol', 'bu') or 0) == 0)

# ------------------------------------------------------------------------------------------------- 14 mid-boss
print('== 14. mid-boss fights unchanged')
import azsim as A  # noqa: E402
s, zone, pl = A.setup(force=1, dp=DP, cls=M.CmSim)
log = logged(s)
s.setsc('#mbForce', 'mb', REG['boss'][[b_['id'] for b_ in REG['boss']].index('proto')]['n'] if 'proto' in [b_['id'] for b_ in REG['boss']] else 1)
ok = A.to_fight(s, zone)
b = A.body_of(s)
check('14a a mid-boss fight (proto): plaza (#mbAr 0, #mbMode 0), no rlk_mb_resel / rlk_mb_big, mres 0, no proxies',
      b is not None and (M.mb(s, '#mbAr') or 0) == 0 and (M.mb(s, '#mbMode') or 0) == 0 and not ({'rlk_mb_resel', 'rlk_mb_big'} & b.tags)
      and (M.esc(s, b, 'mres') or 0) == 0 and not M.proxies(s), b and sorted(b.tags))
if b is not None:
    A.strike(s, b, 500, elem=1)
    check('14b a hit on the mid-boss never runs res_pre / px / the chapter floor', not any(r[1] in ('rlk:mboss/res_pre', 'rlk:mboss/px/dup',
          'rlk:mboss/floor') for r in log), sorted({r[1] for r in log if r[1].startswith('rlk:mboss/res') or 'px/' in r[1]}))


# ------------------------------------------------------------------------------------------------- 15 lib builders
print('== 15. mboss_lib call builders (cm.md 13.10)')
sys.path.insert(0, str(DP / 'tools'))
import mboss_lib as L  # noqa: E402
want = [
    (L.hz_mask(2.5, 30, 110), ['scoreboard players set #hzR0 mb 25', 'function rlk:mboss/hz/mask {tell:30,dmg:110}']),
    (L.hz_extend(40), 'function rlk:mboss/hz/extend {n:40}'),
    (L.lockv(10), 'function rlk:mboss/mv/lockv {lead:10}'),
    (L.local(), 'function rlk:mboss/mv/local'),
    (L.pl_dot(30, 1), ['scoreboard players set #mbDotPct mb 30', 'scoreboard players set #mbDotEl mb 1',
                       'scoreboard players set #mbDotLethal mb 0', 'function rlk:mboss/pl_dot']),
    (L.push_ring(8, 4), 'function rlk:mboss/push/ring {r:80,to:85,kb:4}'),
    (L.push_ring(8, 4, 12), 'function rlk:mboss/push/ring {r:80,to:120,kb:4}'),
    (L.cine(1), 'function rlk:mboss/cine/start'), (L.cine(0), 'function rlk:mboss/cine/end'),
    (L.repool(40), 'function rlk:mboss/repool {pct:40}'),
    (L.music(2), 'function rlk:mboss/music/set {ph:2}'),
    (L.px_state('normal'), 'function rlk:mboss/px/state {set:"normal"}'),
]
for got, exp in want:
    check(f'15a {exp if isinstance(exp, str) else exp[-1]}', got == exp, got)
check('15b hz_opts(norx, safe_g) / pj_opts(nododge, norx) set the one-shot options',
      L.hz_opts(norx=1, safe_g=7) == ['scoreboard players set #hzNR mb 1', 'scoreboard players set #hzSafeG mb 7']
      and L.pj_opts(nododge=1, norx=1) == ['scoreboard players set #pjNoDodge mb 1', 'scoreboard players set #pjNR mb 1'])
bad = 0
for f in (lambda: L.push_ring(8, 4, 5), lambda: L.repool(0), lambda: L.repool(101), lambda: L.music(12), lambda: L.hz_extend(0),
          lambda: L.pl_dot(0, 1), lambda: L.hz_mask(-1, 30, 10)):
    try:
        f()
    except AssertionError:
        bad += 1
check('15c every builder asserts its range (7 bad calls refused)', bad == 7, bad)


# ------------------------------------------------------------------------------------------------- 16 PERF-4
print('== 16. merge prep: the per-tick body position cache (PERF-4)')
AID = [x for x in REG['boss'] if x['id'] == 'cproto'][0]['arena']
import re  # noqa: E402
import mcsim as MCS  # noqa: E402
BODY_READ = re.compile(r'(?:(?:if|unless) data entity|data get entity|from entity) @e\[tag=rlk_body')
reads = [0]
by_fn = {}
M0_READERS = {'rlk:mboss/hz/hit'}        # M0 text (the height band of every hazard's strike tick), not chapter runtime
_split = MCS.split


def counting_split(x):
    if BODY_READ.search(x):
        fn = s.stack[-1] if s.stack else '?'
        by_fn[fn] = by_fn.get(fn, 0) + len(BODY_READ.findall(x))
        if fn not in M0_READERS:
            reads[0] += len(BODY_READ.findall(x))
    return _split(x)


s, pl, log, b = setup()
s.call('rlk:mboss/px/state', C0, {'set': 'normal'})
s.call('rlk:mboss/cproto/test', Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 30})       # the push every tick (#cpPush 1)
mask(s, b.pos[0] + 12.0, b.pos[2], r0=10, tell=3)                                 # a live mask hazard (hz/hit_mask)
pl.pos = [b.pos[0] + 0.3, b.pos[1], b.pos[2] + 0.2]                                # inside the body capsule: pushed out
M.moved(s)
MCS.split = counting_split
per = []
moved_ticks = 0
n0 = len(log)
over = []
for _ in range(30):
    reads[0] = 0
    p0 = list(pl.pos)
    M.run(s, 1)
    per.append(reads[0])
    moved_ticks += pl.pos != p0
    if reads[0] > 1 + (pl.pos != p0):        # a push that moved the player may cause one re-read (16c)
        over.append(reads[0])
MCS.split = _split
ran = {r[1] for r in log[n0:]}
need = {'rlk:mboss/mv/lv_sample', 'rlk:mboss/push/capsule', 'rlk:mboss/mv/local', 'rlk:mboss/hz/hit_mask'}
check('16a (the readers ran in these ticks: lv_sample, push/capsule -> mv/local, hz/hit_mask)', need <= ran, sorted(need - ran))
check('16a a live chapter tick with the push requested (the player pushed out of the body capsule, a mask hazard live): the '
      'chapter runtime reads the player\'s body NBT once per tick, only in mv/plpos (lv_sample, mv/local, push/capsule, '
      'hz/hit_mask share it; 6 reads before), plus one re-read after a push that moved the player',
      not over and sum(per) >= 25 and moved_ticks >= 1 and set(by_fn) - M0_READERS == {'rlk:mboss/mv/plpos'}, (per, moved_ticks, by_fn))
# same tick: a second call reuses the value; the next tick reads again
pl.pos = [b.pos[0] + 5.0, 201.0, b.pos[2] + 1.0]
M.moved(s)
MCS.split = counting_split
reads[0] = 0
s.call('rlk:mboss/mv/plpos', C0)
x1 = M.mb(s, '#mbPX')
pl.pos = [b.pos[0] + 6.0, 201.0, b.pos[2] + 1.0]                                    # moved, no tick, no chapter teleport
s.call('rlk:mboss/mv/plpos', C0)
x2, r_same = M.mb(s, '#mbPX'), reads[0]
s.t += 1                                                                            # the next game tick
s.call('rlk:mboss/mv/plpos', C0)
x3, r_next = M.mb(s, '#mbPX'), reads[0]
MCS.split = _split
check('16b mv/plpos: #mbPX = the body x in mb; a second call in the same tick reuses it (one read); the next tick reads again',
      x1 == math.floor((b.pos[0] + 5.0) * 1000) and x2 == x1 and r_same == 1 and x3 == math.floor((b.pos[0] + 6.0) * 1000) and r_next == 2,
      (x1, x2, x3, r_same, r_next))
# a push that moves the player drops the cache inside the tick
pl.pos = [b.pos[0] + 0.3, b.pos[1], b.pos[2] + 0.2]
M.moved(s)
s.call('rlk:mboss/mv/plpos', C0)
xa, pa = M.mb(s, '#mbPX'), list(pl.pos)
s.call('rlk:mboss/push/capsule', Ctx(b, tuple(b.pos), tuple(b.rot)))
g_after = M.mb(s, '#mbPlG')
s.call('rlk:mboss/mv/plpos', C0)
check('16c push/capsule moved the player in this tick: #mbPlG -1, the next mv/plpos (same tick) reads the new position',
      (M.mb(s, '#puDone') or 0) == 1 and pl.pos != pa and g_after == -1 and xa == math.floor(pa[0] * 1000)
      and M.mb(s, '#mbPX') == math.floor(pl.pos[0] * 1000), (xa, M.mb(s, '#mbPX'), pa, pl.pos, g_after, M.mb(s, '#puDone')))
# the chapter arena's tp_in (out of bounds) drops it too
s.call('rlk:mboss/mv/plpos', C0)
s.call(f'rlk:mboss/ar/{AID}/tp_in', Ctx(pl, tuple(pl.pos), (0, 0)))
check(f'16d ar/{AID}/tp_in (the player back at the arrival spot): #mbPlG -1, the next mv/plpos reads the arrival spot',
      M.mb(s, '#mbPlG') == -1 and s.call('rlk:mboss/mv/plpos', C0) == 1 and M.mb(s, '#mbPX') == math.floor(pl.pos[0] * 1000),
      (M.mb(s, '#mbPlG'), M.mb(s, '#mbPX'), pl.pos))

# 17 (AZ FIX round, FAIR-3): #mbGrpL keeps only the last landed group, and a re-arming field ticking under the player
# overwrote it every 10 t, so a later member of an earlier one-shot volley group started live. #mbGrpL2 (the last group
# landed by a one-shot hit) keeps that group spent; #mbGrpL itself is unchanged (the mid-boss state stays the M0 one).
s, pl, log, b = setup()
pl.pos = [CX, 201.0, CZ]
M.moved(s)
s.call('rlk:mboss/grp_new', C0)
g1 = M.mb(s, '#mbGrp')
disc(s, CX, CZ, tell=4, dmg=40, hzGrp=g1)
M.run(s, 8)
s.call('rlk:mboss/grp_new', C0)
g2 = M.mb(s, '#mbGrp')
disc(s, CX, CZ, tell=1, dmg=10, hzRearm=10, hzAct=60, hzGrp=g2)
M.run(s, 14)
l1, l2 = M.mb(s, '#mbGrpL'), M.mb(s, '#mbGrpL2')
idb = disc(s, CX, CZ, tell=4, dmg=40, hzGrp=g1)
M.run(s, 10)
hits_b = [e for e in log if e[1] == 'rlk:mboss/hz/hurt' and e[2] is not None and s.sc(('e', e[2].id), 'mbHzI') == idb]
check('17a a field of another group ticking under the player overwrites #mbGrpL (as in M0) but not #mbGrpL2',
      l1 == g2 and l2 == g1, (g1, g2, l1, l2))
check('17b a member of the spent one-shot group made after the field tick starts harmless (no hit)', not hits_b, len(hits_b))
s.call('rlk:mboss/grp_new', C0)
g3 = M.mb(s, '#mbGrp')
idc = disc(s, CX, CZ, tell=4, dmg=40, hzGrp=g3)
M.run(s, 8)
hits_c = [e for e in log if e[1] == 'rlk:mboss/hz/hurt' and e[2] is not None and s.sc(('e', e[2].id), 'mbHzI') == idc]
check('17c a fresh group still lands (one hit)', len(hits_c) == 1, len(hits_c))

M.summary('FW_AZ')
