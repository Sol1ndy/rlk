#!/usr/bin/env python3
"""test_fw_ap.py: the AP-FW framework gaps (Apep's FN list after AZ-CM; scratchpad az/contract/cm.md 22),
on cproto in the cp_test arena.

    python3 test_fw_ap.py <worktree>/roguelike

A tree without the AP-FW stage (no F:mboss/hz/safe_new: AZ-CM as merged, the Azhdaha branches) is skipped with rc 0, so
run_all.sh stays usable on those trees.

 1. APEP-02 / FN-15 per-mille hazards (#hzPm / #hzPmL): pl_dot share of max HP, no defence, the hazard's element for the
    shields, lethal flag (default 1), dash dodge unless #hzNoDodge, hit / dodge events, re-arm, the volley group, a mask
    hazard with a dome, one-shot options (reset, never left set), L.hz_opts(pm=, pm_lethal=)
 2. APEP-04 mask safe groups from hz/safe_new (negative ids, a number space apart from the hazard ids): a shared group of
    dome markers protects against its masks, survives their expiry, never matches a default-group mask whose id equals
    the group's absolute value, and the allocator wraps; legacy groups (0 = own id, positive) unchanged
 3. APEP-07 the look record look_<aid>: right during a look / build job, after done, after a restore, gone after an abort
    or a clear; the stub arena's ensure writes it
 4. APEP-08 music pools: the measured track table, music_len, load_registry rejects a pool len that would cut a track
 5. APEP-09 the real + stub manifest merge: a stub fallback clip below id 1000 or a duplicate id fails the core build
 6. APEP-11 cine: a hazard, a projectile and a volley group are refused without being consumed; they hit after the cine
 7. FN-29 aux presentation options (#auxShW / #auxShH / #auxHbY) and FN-30 mv/step_flat
 8. APEP-03 / -06 / -10 (fixed in the AZ-CM recheck) are still covered where they were: test_fw_az 3j/3k, 8d-8f, test_px 12
"""
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DP = Path(sys.argv[1]).resolve()
if not (DP / 'data/rlk/function/mboss/hz/safe_new.mcfunction').exists():
    print(f'SKIP: {DP} has no AP-FW stage (no mboss/hz/safe_new); nothing to test')
    sys.exit(0)
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE / 'lib'))
import cmsim as M  # noqa: E402
from mcsim import Ctx, Ent, split  # noqa: E402

sys.path.insert(0, str(DP / 'tools'))
import mboss_lib as L  # noqa: E402

C0 = M.C0
check = M.check
REG = json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
AR = REG['arenas']['cp_test']
CX, CZ = AR['cx'], AR['cz']
F = DP / 'data/rlk/function'


def st(s):
    return s.storage.setdefault('rlk:mboss', {})


def logged(s):
    log = []
    orig = s.call

    def call(fid, ctx, macro=None):
        log.append((s.t, fid, ctx.ex, tuple(ctx.pos), dict(macro) if macro else None))
        if fid == 'rlk:cm/hit_pl2' and getattr(s, 'ifr', False) and (s.sc('#mbNoDodge', 'mb') or 0) != 1 and ctx.ex is not None:
            s.setsc(('e', ctx.ex.id), 'dashInvT', 1)
        if fid == 'rlk:mboss/hz/hurt_pm' and getattr(s, 'ifr', False):     # the i-frames at the moment of the hit (as above)
            s.setsc(('e', s.player().id), 'dashInvT', 1)
        return orig(fid, ctx, macro)
    s.call = call
    return log


def setup():
    s, pl = M.setup(DP)
    s.setsc('#chapter', 'room', 2)
    log = logged(s)
    M.fight(s, 'cproto', 2)
    s.setsc('#cpCool', 'mb', 99999)
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
    s.ifr = on
    s.setsc(('e', pl.id), 'dashInvT', 1 if on else 0)


def opt(s, **kw):
    for k, v in kw.items():
        s.setsc('#' + k, 'mb', v)


def events(s):
    return {k: M.mb(s, k) or 0 for k in ('#mbHitEv', '#mbHitEl', '#mbHitSrc', '#mbDodgeEv', '#mbDodgeOk')}


def clear_events(s):
    for k in ('#mbHitEv', '#mbDodgeEv', '#mbDodgeOk', '#mbHitSrc', '#mbHitEl'):
        s.setsc(k, 'mb', 0)


def hz(s, hid):
    return [e for e in s.ents if e.alive and 'rlk_mb_hz' in e.tags and M.esc(s, e, 'mbHzI') == hid][0]


def disc(s, x, z, r=30, tell=20, dmg=50, **kw):
    opt(s, **kw)
    s.call('rlk:mboss/hz/disc', at(x, z), {'r': r, 'tell': tell, 'dmg': dmg})
    return M.mb(s, '#hzLast')


def marker(s, x, z, g, y=201.0):
    e = Ent('marker', (x, y, z), tags=['rlk_room', 'rlk_mb_aux', 'rlk_mb_hzsafe'])
    s.ents.append(e)
    s.setsc(('e', e.id), 'mbHzSG', g)
    return e


def mask(s, cx, cz, r0=25, tell=20, dmg=50, **kw):
    opt(s, hzR0=r0, **kw)
    s.call('rlk:mboss/hz/mask', at(cx, cz), {'tell': tell, 'dmg': dmg})
    return M.mb(s, '#hzLast')


def called(log, i0, fid):
    return any(r[1] == fid for r in log[i0:])


# ------------------------------------------------------------------------------------------------- 1 per-mille hazards
print('== 1. APEP-02 per-mille hazards (#hzPm / #hzPmL)')
check('1a L.hz_opts(pm=30, pm_lethal=0) sets the two one-shot options',
      L.hz_opts(pm=30, pm_lethal=0) == ['scoreboard players set #hzPm mb 30', 'scoreboard players set #hzPmL mb 0'],
      L.hz_opts(pm=30, pm_lethal=0))
try:
    L.hz_opts(pm_lethal=0)
    check('1b L.hz_opts(pm_lethal=) without pm is refused', False)
except AssertionError:
    check('1b L.hz_opts(pm_lethal=) without pm is refused', True)
s, pl, log, b = setup()
pl.pos = [CX, 201.0, CZ]
M.moved(s)
s.setsc(('e', pl.id), 'def', 400)
clear_events(s)
i0 = len(log)
hid = disc(s, CX, CZ, hzPm=30, hzPmL=0, hzEl=7)
m = hz(s, hid)
check('1c the hazard stores mbHzPm 30 / mbHzPmL 0; both options are unset after the call (reset, one-shot)',
      M.esc(s, m, 'mbHzPm') == 30 and M.esc(s, m, 'mbHzPmL') == 0 and M.mb(s, '#hzPm') is None and M.mb(s, '#hzPmL') is None,
      (M.esc(s, m, 'mbHzPm'), M.esc(s, m, 'mbHzPmL'), M.mb(s, '#hzPm'), M.mb(s, '#hzPmL')))
M.run(s, 24)
ev = events(s)
check('1d the hit takes 30 per mille of max HP 5000 = 150 HP through mboss/pl_dot (defence 400 ignored), not mboss/hurt',
      hp(s, pl) == 4850 and called(log, i0, 'rlk:mboss/pl_dot') and not called(log, i0, 'rlk:cm/hit_pl2'), (hp(s, pl),))
check('1e a hit event: #mbHitEv 1, element 7, source 1 (hazard); never element/player_hit',
      ev['#mbHitEv'] == 1 and ev['#mbHitEl'] == 7 and ev['#mbHitSrc'] == 1 and not called(log, i0, 'rlk:element/player_hit'), ev)
check('1f one hit per hazard (mbHzHit 1, no second hit in the active window)', M.esc(s, m, 'mbHzHit') == 1 if m.alive else hp(s, pl) == 4850)
# lethal flag
s.setsc(('e', pl.id), 'curHealth', 10)
disc(s, CX, CZ, hzPm=900, hzPmL=0)
M.run(s, 24)
check('1g #hzPmL 0: a 900 per mille hit leaves 1 HP', hp(s, pl) == 1, hp(s, pl))
s.setsc(('e', pl.id), 'curHealth', 10)
hid = disc(s, CX, CZ, hzPm=900)
check('1h #hzPmL unset = lethal (mbHzPmL 1)', M.esc(s, hz(s, hid), 'mbHzPmL') == 1)
M.run(s, 24)
check('1i ... and the hit kills (0 HP)', hp(s, pl) == 0, hp(s, pl))
# dodge / no-dodge
s, pl, log, b = setup()
pl.pos = [CX, 201.0, CZ]
M.moved(s)
clear_events(s)
iframes(s, pl, True)
hid = disc(s, CX, CZ, hzPm=200)
m = hz(s, hid)
M.run(s, 24)
ev = events(s)
# combat overhaul C (11-10): i-frames avoid it through player/def/judge (the dodge event only; #mbDodgeOk is for a perfect
# dodge / parry)
check('1j i-frames dodge a per-mille hazard: no HP lost, a dodge event (#mbDodgeOk 0: not a perfect dodge), consumed',
      hp(s, pl) == 5000 and ev['#mbDodgeEv'] == 1 and ev['#mbDodgeOk'] == 0 and ev['#mbHitEv'] == 0, (hp(s, pl), ev))
iframes(s, pl, False)
clear_events(s)
for o in ('parAt', 'parLk', 'parHit', 'dgRw'):
    s.setsc(('e', pl.id), o, -1000000)
disc(s, CX, CZ, hzPm=200)
s.setsc(('e', pl.id), 'dgAt', s.t + 19)      # a dodge started 0-2 t before the strike (tell 20)
M.run(s, 24)
ev = events(s)
check('1j2 a perfect dodge avoids a per-mille hazard (boss class: only the perfect window): no HP lost, #mbDodgeOk 1',
      hp(s, pl) == 5000 and ev['#mbDodgeEv'] == 1 and ev['#mbDodgeOk'] == 1 and ev['#mbHitEv'] == 0, (hp(s, pl), ev))
s.setsc(('e', pl.id), 'dgAt', -1000000)
iframes(s, pl, True)
clear_events(s)
disc(s, CX, CZ, hzPm=200, hzNoDodge=1)
M.run(s, 24)
check('1k #hzNoDodge 1: the per-mille hit lands through the i-frames (1000 HP)', hp(s, pl) == 4000, hp(s, pl))
iframes(s, pl, False)
# shields: the hazard's element against an element shield (250 % against its own element)
s.setsc(('e', pl.id), 'curHealth', 5000)
s.setsc(('e', pl.id), 'shieldHP', 1000)
s.setsc(('e', pl.id), 'shieldT', 400)
s.setsc(('e', pl.id), 'shieldEl', 7)
disc(s, CX, CZ, hzPm=40, hzEl=7)
M.run(s, 24)
check('1l the hazard element feeds the shield: a Dendro hit of 200 on a Dendro shield takes 80 shield, no HP',
      hp(s, pl) == 5000 and s.sc(('e', pl.id), 'shieldHP') == 920, (hp(s, pl), s.sc(('e', pl.id), 'shieldHP')))
s.setsc(('e', pl.id), 'shieldHP', 0)
# re-arm (the 종말의 여파 field ticks)
s.setsc(('e', pl.id), 'curHealth', 5000)
disc(s, CX, CZ, tell=10, hzPm=30, hzPmL=0, hzRearm=15, hzAct=60, hzNoDodge=1, hzNR=1)
M.run(s, 75)
check('1m a re-arming per-mille field (re-arm 15 t over a 60-t window): 4 ticks of 150 HP', hp(s, pl) == 5000 - 4 * 150, hp(s, pl))
# volley group
s.call('rlk:mboss/lib_clear', C0)
s.setsc(('e', pl.id), 'curHealth', 5000)
s.call('rlk:mboss/grp_new', C0)
g = M.mb(s, '#mbGrp')
s.setsc('#hzGrp', 'mb', g)
disc(s, CX, CZ, tell=10, hzPm=100)
s.setsc('#hzGrp', 'mb', g)
disc(s, CX, CZ, tell=12, hzPm=100)
M.run(s, 20)
check('1n a volley group of two per-mille hazards: one hit (500 HP), #mbGrpL = the group', hp(s, pl) == 4500 and M.mb(s, '#mbGrpL') == g,
      (hp(s, pl), M.mb(s, '#mbGrpL'), g))
# mask blast with a dome (Q2's 800 per mille blast)
for label, pos, want in (('inside the dome', (CX + 2.0, CZ), 5000), ('outside', (CX + 8.0, CZ), 1000)):
    s, pl, log, b = setup()
    pl.pos = [pos[0], 201.0, pos[1]]
    M.moved(s)
    s.call('rlk:mboss/hz/safe_new', C0)
    g = M.mb(s, '#mbSafeG')
    marker(s, CX, CZ, g)
    mask(s, CX, CZ, r0=45, tell=20, dmg=1, hzSafeG=g, hzPm=800, hzNoDodge=1)
    M.run(s, 26)
    check(f'1o a per-mille mask (800, lethal) with a dome of r 4.5, player {label}: HP {want}', hp(s, pl) == want, hp(s, pl))
# a plain hazard after a per-mille one is a plain hit again
s, pl, log, b = setup()
pl.pos = [CX, 201.0, CZ]
M.moved(s)
disc(s, CX, CZ, hzPm=30)
i0 = len(log)
hid = disc(s, CX, CZ, tell=22)
check('1p the next hazard without #hzPm has no mbHzPm (a % hit through mboss/hurt)', M.esc(s, hz(s, hid), 'mbHzPm') is None)
M.run(s, 26)
check('1q ... and lands through cm/hit_pl2', called(log, i0, 'rlk:cm/hit_pl2'))
s.setsc('#hzPmL', 'mb', 0)
s.call('rlk:mboss/cleanup_fight', C0)
check('1r cleanup_fight drops a pending #hzPmL', M.mb(s, '#hzPmL') is None)

# ------------------------------------------------------------------------------------------------- 2 safe groups
print('== 2. APEP-04 mask safe groups from hz/safe_new')
s, pl, log, b = setup()
s.call('rlk:mboss/hz/safe_new', C0)
g1 = M.mb(s, '#mbSafeG')
s.call('rlk:mboss/hz/safe_new', C0)
g2 = M.mb(s, '#mbSafeG')
check('2a hz/safe_new hands out negative ids, a new one per call', g1 is not None and g1 <= -1 and g2 == g1 - 1, (g1, g2))
s.setsc('#mbSafeN', 'mb', -999999)
s.call('rlk:mboss/hz/safe_new', C0)
check('2b it wraps from -1 000 000 back to -1', M.mb(s, '#mbSafeG') == -1, M.mb(s, '#mbSafeG'))
check("2c L.hz_safe_new() / L.hz_opts(safe_g='cur')", L.hz_safe_new() == 'function rlk:mboss/hz/safe_new'
      and L.hz_opts(safe_g='cur') == ['scoreboard players operation #hzSafeG mb = #mbSafeG mb'])
s, pl, log, b = setup()
pl.pos = [CX + 0.5, 201.0, CZ]
M.moved(s)
h0 = hp(s, pl)
s.call('rlk:mboss/hz/safe_new', C0)
g = M.mb(s, '#mbSafeG')
dome = marker(s, CX, CZ, g)
s.setsc('#hzSafeG', 'mb', 0)
s.call('rlk:mboss/hz/safe_new', C0)          # #mbSafeG moves on; the group of the dome is g
s.setsc('#mbSafeG', 'mb', g)
for line in L.hz_opts(safe_g='cur'):
    s.cmd(split(line), C0)
h1 = mask(s, CX, CZ, tell=10)
s.cmd(split(L.hz_opts(safe_g='cur')[0]), C0)
h2 = mask(s, CX, CZ, tell=14)
check('2d two masks of the shared group store it (mbHzSG = the negative group)', M.esc(s, hz(s, h1), 'mbHzSG') == g
      and M.esc(s, hz(s, h2), 'mbHzSG') == g, (M.esc(s, hz(s, h1), 'mbHzSG'), g))
M.run(s, 40)
check('2e the dome spares the player from both and survives their expiry (the module owns shared markers)',
      hp(s, pl) == h0 and dome.alive, (h0, hp(s, pl), dome.alive))
# the APEP-04 repro: a default-group mask whose own id equals the group number (|g|) must neither match nor kill the dome
s.setsc('#hzId', 'mb', -g - 1)               # the next hazard id = -g (= |g|)
hid = mask(s, CX, CZ, tell=10)
check(f'2f an unrelated default-group mask with id {hid} = |group| resolves to its own id (never the dome group)',
      hid == -g and M.esc(s, hz(s, hid), 'mbHzSG') == hid, (hid, g))
M.run(s, 30)
check('2g ... the dome does not protect against it (hit) and its expiry leaves the dome alone', hp(s, pl) < h0 and dome.alive,
      (hp(s, pl), dome.alive))
# legacy groups unchanged: 0 = own id (own markers expire with it), an explicit positive group as before
s, pl, log, b = setup()
pl.pos = [CX + 0.5, 201.0, CZ]
M.moved(s)
h0 = hp(s, pl)
hid = mask(s, CX, CZ, tell=10, hzSafeG=0)
own = marker(s, CX, CZ, hid)
M.run(s, 30)
check('2h #hzSafeG 0: the group is the own id, its marker protects and goes with it', hp(s, pl) == h0 and not own.alive)
hid = mask(s, CX, CZ, tell=10, hzSafeG=7)
check('2i an explicit positive group (legacy) is stored as given', M.esc(s, hz(s, hid), 'mbHzSG') == 7)

# ------------------------------------------------------------------------------------------------- 3 look record
print('== 3. APEP-07 the look record look_<aid>')
AID = 'cp_test'
LOOKS = AR['looks']


def look(s):
    return st(s).get('look_' + AID)


def stamp(s):
    return st(s).get('built_' + AID)


def built(s, limit=400):
    return M.until(s, lambda s: (M.mb(s, '#mbArBuild') or 0) == 0, limit)


s, pl = M.setup(DP)
s.call(f'rlk:mboss/ar/{AID}/fl_on', C0)
s.call(f'rlk:mboss/arena/{AID}/build', C0)
check(f'3a a build job: look_{AID} = "{LOOKS[0]}" from the start (no stamp yet)', look(s) == LOOKS[0] and stamp(s) is None,
      (look(s), stamp(s)))
built(s)
check('3b after the build: stamp and look record agree', stamp(s) == f'{AID}@{AR["ver"]}:{LOOKS[0]}' and look(s) == LOOKS[0])
s.call(f'rlk:mboss/arena/{AID}/look/{LOOKS[1]}', C0)
check(f'3c a look job to "{LOOKS[1]}": the stamp is gone, the record already says "{LOOKS[1]}" (A2 during the job)',
      stamp(s) is None and look(s) == LOOKS[1] and st(s).get('arjob', {}).get('kind') == 'look', (stamp(s), look(s)))
s.call('rlk:mboss/init', C0)
check('3d /reload (mboss/init) mid-job keeps the record and the job', look(s) == LOOKS[1] and (M.mb(s, '#mbArBuild') or 0) >= 1)
built(s)
check('3e done: stamp "<aid>@<ver>:<look>" and the same look record', stamp(s) == f'{AID}@{AR["ver"]}:{LOOKS[1]}' and look(s) == LOOKS[1])
r = s.call(f'rlk:mboss/arena/{AID}/look/{LOOKS[0]}', C0)
check('3f a refused look call (another job would block; here none) starts the restore: record = the default look',
      look(s) == LOOKS[0] and stamp(s) is None)
s.call('rlk:mboss/arena/abort', C0)
check('3g an aborted job leaves neither a stamp nor a look record (a half-swapped look is no look)', stamp(s) is None and look(s) is None)
r = s.call(f'rlk:mboss/arena/{AID}/ensure', C0)
check('3h ensure after the abort: fail, a full build, record = the default look', not r and look(s) == LOOKS[0]
      and st(s).get('arjob', {}).get('kind') == 'build')
built(s)
s.call(f'rlk:mboss/arena/{AID}/look/{LOOKS[1]}', C0)
s.setsc('#mbArBuild', 'mb', 5)
r = s.call(f'rlk:mboss/arena/{AID}/look/{LOOKS[0]}', C0)
check('3i a look call refused while a job runs changes nothing', look(s) == LOOKS[1])
s.setsc('#mbArBuild', 'mb', 1)
built(s)
s.call(f'rlk:mboss/arena/{AID}/clear', C0)
check('3j clear drops the stamp and the record', stamp(s) is None and look(s) is None)
stub = [aid for aid, a in REG['arenas'].items() if L.theme_module(a['theme']) is None]
if stub:
    a0 = REG['arenas'][stub[0]]
    s.call(f'rlk:mboss/arena/{stub[0]}/ensure', C0)
    check(f'3k the stub arena {stub[0]}: ensure writes look_{stub[0]} = "{a0["looks"][0]}"', st(s).get('look_' + stub[0]) == a0['looks'][0])
s.call('rlk:mboss/uninstall', C0)
check('3l uninstall removes every look record', not [k for k in st(s) if k.startswith('look_')])

# ------------------------------------------------------------------------------------------------- 4 music pools
print('== 4. APEP-08 music pools')
AP_MUSIC = ('minecraft:music.overworld.deep_dark', 'minecraft:music.nether.soul_sand_valley', 'minecraft:music.overworld.lush_caves')
check("4a Apep's three events are vanilla random-track pools (2, 5, 15 tracks)", [len(L.MUSIC_TRACKS[e]) for e in AP_MUSIC] == [2, 5, 15])
check('4b music_len: the pools re-pick after their longest track (6870 / 6376 / 6881 t); single tracks loop exactly',
      [L.music_len(e) for e in AP_MUSIC] == [6870, 6376, 6881] and L.music_len('minecraft:music.end') == 18090
      and L.music_len('minecraft:music.dragon') == 6883)


def reg_ok(edit):
    tmp = Path(tempfile.mkdtemp(prefix='fwap_reg_', dir=HERE / 'tmp' if (HERE / 'tmp').exists() else None))
    try:
        reg = json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
        edit(reg)
        p = tmp / 'mboss_registry.json'
        p.write_text(json.dumps(reg, ensure_ascii=False), encoding='utf-8')
        old = L.REGISTRY
        L.REGISTRY = p
        try:
            L.load_registry()
            return True, ''
        except AssertionError as e:
            return False, str(e)
        finally:
            L.REGISTRY = old
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def music_edit(ev, ln):
    def edit(reg):
        M.entry(reg, 'cproto')['music'] = {'1': {'ev': ev, 'len': ln}}
    return edit


ok, msg = reg_ok(music_edit(AP_MUSIC[0], 2400))
check('4c load_registry rejects a pool with a len that would cut the picked track (deep_dark, len 2400)', not ok and 'pool' in msg, msg)
for ln in (0, 6870, 9000):
    ok, msg = reg_ok(music_edit(AP_MUSIC[0], ln))
    check(f'4d ... and accepts len {ln} (0 = play once, >= 6870 = re-pick period)', ok, msg)
ok, msg = reg_ok(music_edit('minecraft:music.end', 1200))
check('4e a single-track event may use any len (an intended cut is allowed)', ok, msg)

# ------------------------------------------------------------------------------------------------- 5 manifest merge
print('== 5. APEP-09 the real + stub manifest merge (fallback ids >= 1000, unique)')
V = M.variant(DP, lambda reg: None, 'fwap_px', gens=())
try:
    tools = V / 'tools'
    stub = json.loads((tools / 'mboss_cproto_rig_manifest.json').read_text(encoding='utf-8'))
    real = json.loads(json.dumps(stub))
    real['source'] = 'rig'
    dropped = real['clips'][-1]['name']
    real['clips'] = real['clips'][:-1]
    (tools / 'mboss_cproto').mkdir(exist_ok=True)

    def core_build(stub_clips):
        sm = json.loads(json.dumps(stub))
        sm['clips'] = stub_clips
        (tools / 'mboss_cproto_rig_manifest.json').write_text(json.dumps(real), encoding='utf-8')
        (tools / 'mboss_cproto' / 'stub_rig_manifest.json').write_text(json.dumps(sm), encoding='utf-8')
        r = subprocess.run([sys.executable, 'tools/build_mboss_core.py'], cwd=V, capture_output=True, text=True)
        return r.returncode, ((r.stdout + r.stderr).strip().splitlines() or [''])[-1][-300:]

    low = [dict(c) for c in stub['clips']]
    rc, out = core_build(low)
    check(f'5a a stub fallback clip ({dropped}) with an id below 1000 beside the real manifest fails the core build',
          rc != 0 and 'ids >= 1000' in out, out)
    hi = [dict(c, id=1000 + k) for k, c in enumerate(stub['clips'])]
    rc, out = core_build(hi)
    check('5b stub ids 1000 + k: the merge builds (the real clips plus the one fallback)', rc == 0, out)
    dup = [dict(c, id=1000) for c in stub['clips']]
    real['clips'] = real['clips'][:-1]
    rc, out = core_build(dup)
    check('5c two fallback clips with the same id fail the build', rc != 0 and 'used by two clips' in out, out)
finally:
    M.drop_variant(V)

# ------------------------------------------------------------------------------------------------- 6 cine
print('== 6. APEP-11 a cine refuses hits without consuming them')
s, pl, log, b = setup()
pl.pos = [CX, 201.0, CZ]
M.moved(s)
s.call('rlk:mboss/cine/start', C0)
s.setsc('#cpCine', 'mb', 100000)            # cproto's own cine clock (its tick ends a cine at 0)
hid = disc(s, CX, CZ, tell=5, hzAct=30)
m = hz(s, hid)
M.run(s, 10)
check('6a a hazard during the cine: no HP lost, not consumed (mbHzHit 0)', hp(s, pl) == 5000 and M.esc(s, m, 'mbHzHit') == 0,
      (hp(s, pl), M.esc(s, m, 'mbHzHit')))
s.setsc('#cpCine', 'mb', 0)
s.call('rlk:mboss/cine/end', C0)
M.run(s, 3)
check('6b the cine ends inside its active window: the hazard hits', hp(s, pl) < 5000 and M.esc(s, m, 'mbHzHit') == 1)
# projectile
s, pl, log, b = setup()
e = Ent('block_display', (CX, 202.1, CZ), (0.0, 0.0), ['rlk_room', 'rlk_mb_aux', 'rlk_mb_fwpj'])
s.ents.append(e)
pl.pos = [CX, 201.0, CZ]
M.moved(s)
s.call('rlk:mboss/pj/launch', Ctx(e, tuple(e.pos), (0.0, 0.0)), {'spd': 1, 'life': 80, 'dmg': 60, 'hr': 6})
s.call('rlk:mboss/cine/start', C0)
i0 = len(log)
s.setsc('#pjEv', 'mb', 0)
s.call('rlk:mboss/pj/hit', Ctx(e, tuple(e.pos), (0.0, 0.0)))
check('6c a projectile hit during the cine: refused, mbPjHit 0, no pj_end event 4, no HP lost',
      M.esc(s, e, 'mbPjHit') == 0 and not called(log, i0, 'rlk:mboss/d/pj_end') and hp(s, pl) == 5000)
s.call('rlk:mboss/cine/end', C0)
s.call('rlk:mboss/pj/hit', Ctx(e, tuple(e.pos), (0.0, 0.0)))
check('6d after the cine the same projectile hits (mbPjHit 1, HP lost)', M.esc(s, e, 'mbPjHit') == 1 and hp(s, pl) < 5000)
# volley group
s, pl, log, b = setup()
pl.pos = [CX, 201.0, CZ]
M.moved(s)
s.call('rlk:mboss/grp_new', C0)
g = M.mb(s, '#mbGrp')
gl0 = M.mb(s, '#mbGrpL')
s.call('rlk:mboss/cine/start', C0)
s.setsc('#cpCine', 'mb', 100000)
s.setsc('#hzGrp', 'mb', g)
h1 = disc(s, CX, CZ, tell=4)
s.setsc('#hzGrp', 'mb', g)
h2 = disc(s, CX, CZ, tell=12)
M.run(s, 8)
check('6e a volley group during the cine: not marked landed (#mbGrpL unchanged), its members still armed',
      M.mb(s, '#mbGrpL') == gl0 and M.esc(s, hz(s, h2), 'mbHzHit') == 0, (M.mb(s, '#mbGrpL'), gl0))
s.setsc('#cpCine', 'mb', 0)
s.call('rlk:mboss/cine/end', C0)
M.run(s, 8)
check('6f after the cine the group lands once', hp(s, pl) < 5000 and M.mb(s, '#mbGrpL') == g)

# ------------------------------------------------------------------------------------------------- 7 aux options, step_flat
print('== 7. FN-29 aux presentation options, FN-30 mv/step_flat')
check('7a L.aux_opts(4.4, 4.6, 1.5) -> #auxShW 44, #auxShH 46, #auxHbY 15', L.aux_opts(4.4, 4.6, 1.5) ==
      ['scoreboard players set #auxShW mb 44', 'scoreboard players set #auxShH mb 46', 'scoreboard players set #auxHbY mb 15'])
s, pl, log, b = setup()
sh0 = {e.id for e in s.ents if 'rlk_mshield' in e.tags}
s.cache['rlk:mboss/aux/hb_y'] = ['scoreboard players add #HBY mb 1']     # `execute on passengers` is beyond mcsim (7e: text)
opt(s, auxShW=44, auxShH=46, auxHbY=15, auxHp=500)
s.call('rlk:mboss/aux/spawn', at(CX + 3, CZ))
a = [e for e in s.ents if e.alive and 'rlk_mb_auxlast' in e.tags][0]
sh = [e for e in s.ents if e.alive and 'rlk_mshield' in e.tags and e.id not in sh0]
check('7b aux/spawn with #auxShW 44 / #auxShH 46: one click shield of 4.4 x 4.6, linked by msid, synced',
      len(sh) == 1 and abs(float(sh[0].data.get('width', 0)) - 4.4) < 1e-6 and abs(float(sh[0].data.get('height', 0)) - 4.6) < 1e-6
      and M.esc(s, sh[0], 'msid') == M.esc(s, a, 'msid') and M.esc(s, a, 'msid') is not None and 'rlk_msync' in sh[0].tags,
      [(e.data.get('width'), e.data.get('height'), sorted(e.tags)) for e in sh])
check('7c aux/setup ran aux/hb_y once; the options are unset after the spawn (one-shot, never left behind)',
      M.mb(s, '#HBY') == 1 and all(M.mb(s, k) is None for k in ('#auxShW', '#auxShH', '#auxHbY')))
s.call('rlk:mob/shield_ensure', Ctx(a, tuple(a.pos), (0, 0)))
sh = [e for e in s.ents if e.alive and 'rlk_mshield' in e.tags and e.id not in sh0]
check('7d mob/shield_ensure keeps it (no 1.2 x 2.2 default beside it)', len(sh) == 1 and abs(float(sh[0].data.get('width', 0)) - 4.4) < 1e-6,
      [(e.data.get('width'), e.data.get('height')) for e in sh])
txt = (F / 'mboss/aux/hb_y.mcfunction').read_text(encoding='utf-8').splitlines()
ys, t = {}, None
for ln in txt:
    if ln.startswith('scoreboard players operation #t mb = #auxHbY'):
        t = 15
    elif ln.startswith('scoreboard players operation #t mb *= #c10'):
        t *= 10
    elif ln.startswith('scoreboard players add #t mb'):
        t += int(ln.split()[-1])
    elif 'transformation.translation[1]' in ln:
        ys[ln.split('tag=')[1].split(']')[0]] = t / 100
check('7e aux/hb_y with #auxHbY 15 puts the HP-bar passengers 1.5 b higher (bar/fill/number 1.75, level 1.93, icon 2.32)',
      ys == {'rlk_hb_bg': 1.75, 'rlk_hb_fg': 1.75, 'rlk_hb_num': 1.75, 'rlk_hb_lv': 1.93, 'rlk_hb_icon': 2.32}, ys)
opt(s, auxHp=500)
s.call('rlk:mboss/aux/spawn', at(CX - 3, CZ))
sh1 = [e for e in s.ents if e.alive and 'rlk_mshield' in e.tags and e.id not in sh0 and e.id != sh[0].id]
check('7f the next aux without the options gets no early shield (mob/shield_ensure makes the default one later), no hb_y',
      not sh1 and M.mb(s, '#HBY') == 1)
w = Ent('marker', (CX + 2.0, 203.4, CZ), (270.0, 0.0), ['rlk_room', 'rlk_mb_aux', 'rlk_mb_fwwalk'])
s.ents.append(w)
s.call('rlk:mboss/mv/step_flat', Ctx(w, tuple(w.pos), (270.0, 30.0)), {'spd': 0.5})
check('7g step_flat {spd:0.5} heading +x: 0.5 b forward (pitch ignored), y on the arena floor (cy 201)',
      abs(w.pos[0] - (CX + 2.5)) < 1e-6 and abs(w.pos[1] - AR['cy']) < 1e-6 and abs(w.pos[2] - CZ) < 1e-6, w.pos)
w.pos = [CX + AR['walk'] - 0.5, 201.0, CZ]
s.call('rlk:mboss/mv/step_flat', Ctx(w, tuple(w.pos), (270.0, 0.0)), {'spd': 1.0})
check(f'7h a step out of the walk disc is pulled back inside walk - 0.7 ({AR["walk"] - 0.7} b)',
      math.hypot(w.pos[0] - CX, w.pos[2] - CZ) <= AR['walk'] - 0.7 + 1e-6, w.pos)
check("7i L.step_flat(0.3)", L.step_flat(0.3) == 'function rlk:mboss/mv/step_flat {spd:0.3}', L.step_flat(0.3))

M.summary('FW-AP')
