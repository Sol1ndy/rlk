#!/usr/bin/env python3
"""test_chapter.py: the chapter-boss mode (AZ-CM, scratchpad az/contract/cm.md 15.1) on the proto chapter boss cproto.

    python3 test_chapter.py <worktree>/roguelike

Reusable by Apep (FN-10: runs unchanged on any branch): every section takes the boss id / arena id from the registry
(BOSS below), and every routing expectation is derived from the registry under test (CH: the enabled chapter entries,
routed(): the first route:true entry of a chapter by ascending n, as cb/route orders its lines; RD_CH: the first chapter
that no route:true entry claims, for the Raiden checks); the cp_test-specific blocks (look names, sentinel, floor ring)
read tools/mboss_arena_<theme>.py.

 1. registry storage (creg / cbyid = the enabled chapter entries, mid-boss reg untouched, azhdaha as registered)
 2. routing: chapters 1 / 2 / 3 / 4 / 7 as the registry routes them (shipped: Raiden everywhere), #cbForce only under
    #mbTest 1, never #mbForce; a variant registry (cproto route:true in chapters 2 and 4) routes exactly those chapters (S5: 2 and 5, chapter 4 is routed since the arlecchino I1)
 3. #cbForce / #cbAuto / cprep reset by run/start, run/end, test/end, test/abort
 4. entrance build -> cb/prep: cprep, forceload of the arena box, the sliced build job, stamp + sentinel
 5. the gate: oact 16, peaceful / zst / body guards, "준비 중" while #mbArBuild >= 1
 6. spawn: the boss body, #mbMode 1, #mbAr, no roll / met / #mbForce, title, HP pool
 7. kill: gold x15 x chapter and 2 sapphires (no mid-boss multipliers), no boxes, k_chapter, forceload released
 8. abort -> the gate returns with the same cprep; a second press fights again
 9. cb/lose and test/lose; the test defeat / won messages
10. title swap, repool + #mbTot, test/level
11. music: set / loop / every-100-t stopsound music / phase change without overlap / pause halt + resume / stop
12. cp_test looks: look job (1 slice), per-look stamps, ensure restores the default look
13. cleanup paths: room/clear, room/wipe, room/remove, uninstall, reload; forceload released; barrier sweep {y0,y1}
    (variant registry with cp_test sweep)
14. Raiden smoke (chapter RD_CH): a narukami zone builds, boss_spawn reaches boss/raiden/spawn, combat_clear spawns
    k_chapter
15. CM fix round regressions: a chapter test session after the kill (#cbForce / #cbAuto 0, the next boss map routes as
    in a run, a later mid-boss win / defeat speaks mid-boss), test/start_ch from a chapter session (STATE-1, IDENTITY-6);
    a fight that ends while its arena's job runs, mboss/cleanup during a job (STATE-2); a manual gate press ends the
    test auto press (STATE-4); the dev view releases its forceload, the entrance prep keeps its own (STATE-6);
    uninstall removes the chapter scratch keys (STATE-7)
16. recheck PERF-1: every chapter arena's ar/<aid>/loaded fails while any chunk of its box (not only a corner or the
    centre) is still loading
17. merge prep PERF-2: ar/<aid>/fl_off itself aborts a running job of that arena (a release from anywhere, e.g. a
    direct ar/fl_off, never leaves a job waiting 200 t for chunks), never a job of another arena; the gate's next press
    is not refused
"""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import cmsim as M  # noqa: E402
from mcsim import Ctx  # noqa: E402

DP = Path(sys.argv[1]).resolve()
C0 = M.C0
check = M.check
BOSS = 'cproto'
REG = json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
B = M.entry(REG, BOSS)
AID = B['arena']
AR = REG['arenas'][AID]
sys.path.insert(0, str(DP / 'tools'))
THEME = __import__('mboss_arena_' + AR['theme'])
BOX = AR['box']


def chaps(reg):
    """The enabled chapter entries of a registry (rlk:mboss creg[], cb/route_force), by ascending n."""
    return sorted((b for b in reg['boss'] if b.get('kind') == 'chapter' and b.get('enabled', True)), key=lambda b: b['n'])


def routed(reg, ch):
    """The chapter boss cb/route lays out for chapter `ch` (the first route:true entry claiming it by ascending n), or None
    (Raiden)."""
    return next((b['id'] for b in chaps(reg) if b.get('route', True) and ch in b.get('ch', [])), None)


CH = chaps(REG)
CH_IDS = sorted(b['id'] for b in CH)
RD_CH = next((c for c in range(1, 10) if routed(REG, c) is None), None)     # a chapter Raiden still ends


def st(s):
    return s.storage.setdefault('rlk:mboss', {})


def box_chunks():
    return {(cx, cz) for cx in range(BOX['x0'] >> 4, (BOX['x1'] >> 4) + 1) for cz in range(BOX['z0'] >> 4, (BOX['z1'] >> 4) + 1)}


def box_forceloaded(s):
    return box_chunks() <= set(s.fl)


def box_released(s):
    return not (box_chunks() & set(s.fl))


def gold_of(s):
    return s.sc(('e', s.player().id), 'gold') or 0


def fresh(dp=DP, chapter=1):
    s, pl = M.setup(dp)
    s.setsc('#chapter', 'room', chapter)
    s.setsc(('e', pl.id), 'gold', 0)
    s.cache.pop('rlk:combat/gold_absorb', None)      # the real absorb (player gold += gval)
    return s, pl


def built(s, limit=400):
    return M.until(s, lambda s: (M.mb(s, '#mbArBuild') or 0) == 0, limit)


def stamp(s):
    return st(s).get('built_' + AID)


def mark(s):
    return len(s.tells)


def tells_since(s, m):
    return '\n'.join(x for _, x in s.tells[m:])


# ------------------------------------------------------------------------------------------------- 1 registry
print('== 1. registry storage')
s, pl = fresh()
mb = st(s)
creg = mb.get('creg', [])
check(f'1a creg holds the enabled chapter bosses of the registry ({", ".join(CH_IDS)}), {BOSS} among them',
      sorted(r['id'] for r in creg) == CH_IDS and BOSS in CH_IDS, [r['id'] for r in creg])
check('1b cbyid.cproto = the creg record (n 98, kind chapter, arena cp_test, ar 9)',
      mb['cbyid'][BOSS]['n'] == B['n'] and mb['cbyid'][BOSS].get('kind') == 'chapter' and mb['cbyid'][BOSS].get('ar') == AR['n']
      and mb['cbyid'][BOSS].get('arena') == AID, {k: mb['cbyid'][BOSS].get(k) for k in ('n', 'kind', 'arena', 'ar')})
check('1c the mid-boss reg / byid hold no chapter entry', all(r.get('kind', 'mid') != 'chapter' for r in mb.get('reg', []))
      and BOSS not in mb.get('byid', {}), [r['id'] for r in mb.get('reg', [])])
check('1d #mbCN = the number of enabled chapter bosses', M.mb(s, '#mbCN') == len(CH), (M.mb(s, '#mbCN'), len(CH)))
AZE = next((b for b in REG['boss'] if b['id'] == 'azhdaha'), None)
if AZE is None:
    check('1e azhdaha: no registry entry, nothing in cbyid', 'azhdaha' not in mb['cbyid'])
elif not AZE.get('enabled', True):
    check('1e azhdaha: registered disabled (no creg, no cbyid)', 'azhdaha' not in mb['cbyid'] and 'azhdaha' not in [r['id'] for r in creg])
else:
    check('1e azhdaha: enabled -> its cbyid record (n, arena)', mb['cbyid'].get('azhdaha', {}).get('n') == AZE['n'], mb['cbyid'].get('azhdaha'))
rec = mb['cbyid'][BOSS]
check('1f the record carries px / pxBase / phases / res[9] / music', rec.get('px') in (1, True) and rec.get('pxBase') == B['pxBase']
      and list(rec.get('phases', [])) == B['phases'] and len(rec.get('res', [])) == 9
      and rec['music']['1']['ev'] == B['music']['1']['ev'], {k: rec.get(k) for k in ('px', 'pxBase', 'phases', 'res')})


# ------------------------------------------------------------------------------------------------- 2 routing
print('== 2. routing')


def route(s, chapter, test=0, force=0):
    s.setsc('#mbTest', 'mb', test)
    s.setsc('#cbForce', 'mb', force)
    s.setsc('#mbForce', 'mb', 0)
    rd0 = s.sc('#RDLAYOUT', 'azs') or 0
    zs = M.boss_map(s, chapter)
    cur = s.storage.get('rlk:room', {}).get('cur') or {}
    ids = [z.get('boss_id') for z in cur.get('zones', [])]
    return (s.sc('#RDLAYOUT', 'azs') or 0) - rd0, ids, zs


def route_ok(rd, ids, exp):
    """Raiden (exp None): its layout ran and no chapter boss zone; else exactly that boss's layout."""
    return (rd == 0 and exp in ids) if exp else (rd == 1 and not any(i in CH_IDS for i in ids))


s, pl = fresh()
for ch in (1, 2, 3, 4, 7):
    rd, ids, _ = route(s, ch)
    exp = routed(REG, ch)
    check(f'2a chapter {ch}: {exp or "Raiden (cb/route falls through)"} as the registry routes it', route_ok(rd, ids, exp), (rd, ids, exp))
check('2a0 a chapter no route:true entry claims exists (Raiden checks below use it)', RD_CH is not None, RD_CH)
rd, ids, _ = route(s, RD_CH, test=0, force=B['n'])
check(f'2b #cbForce without #mbTest: ignored (chapter {RD_CH}: Raiden)', route_ok(rd, ids, None), (rd, ids))
rd, ids, zs = route(s, 2, test=1, force=B['n'])
check('2c #cbForce under #mbTest 1: the cproto entrance layout (zone boss_id cproto, cboss 1b, fn cboss_cproto)',
      rd == 0 and BOSS in ids and any(z.data.get('cboss') in (1, True) and z.data.get('fn') == f'cboss_{BOSS}' for z in zs), (rd, ids))
check('2d no routing path sets #mbForce', (M.mb(s, '#mbForce') or 0) == 0, M.mb(s, '#mbForce'))
rd, ids, _ = route(s, 2, test=1, force=77)
check('2e #cbForce of an unknown n: Raiden (route_force falls through)', route_ok(rd, ids, None), (rd, ids))


def v_route(reg):
    # chapter 5 (not 4): since the arlecchino I1 chapter 4 is routed (two route:true entries may not share a chapter)
    M.entry(reg, BOSS).update({'ch': [2, 5], 'route': True})


V1 = M.variant(DP, v_route, 'route')
try:
    s, pl = fresh(V1)
    VREG = json.loads((V1 / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
    lines = [x for x in (V1 / 'data/rlk/function/mboss/cb/route.mcfunction').read_text(encoding='utf-8').split('\n') if x and not x.startswith('#')]
    want = [f'execute if score #chapter room matches {c} run return run function rlk:mboss/cb/layout {{id:"{bid}"}}'
            for n, c, bid in sorted((b['n'], c, b['id']) for b in chaps(VREG) if b.get('route', True) for c in b.get('ch', []))]
    check('2f variant (cproto ch [2,5], route:true): cb/route = the force line, one line per routed chapter (cproto 2 and 5 '
          'among them, by n), then Raiden', lines == [lines[0]] + want + ['function rlk:room/raiden/layout'] and 'route_force' in lines[0]
          and all(f'matches {c} run return run function rlk:mboss/cb/layout {{id:"{BOSS}"}}' in '\n'.join(lines) for c in (2, 5)), lines)
    for ch in (1, 2, 3, 4, 5):
        rd, ids, _ = route(s, ch)
        exp = routed(VREG, ch)
        check(f'2g variant chapter {ch}: {exp or "Raiden"}', route_ok(rd, ids, exp), (rd, ids, exp))
finally:
    M.drop_variant(V1)


# ------------------------------------------------------------------------------------------------- 3 resets
print('== 3. #cbForce / #cbAuto / cprep resets')
for fn in ('rlk:run/start', 'rlk:run/end', 'rlk:mboss/test/end', 'rlk:mboss/cb/run_reset'):
    s, pl = fresh()
    s.setsc('#mbTest', 'mb', 1)
    s.setsc('#cbForce', 'mb', B['n'])
    s.setsc('#cbAuto', 'mb', 1)
    st(s)['cprep'] = {BOSS: {'gate': {'l1': '{text:"x"}'}}}
    for k in ('rlk:player/reset_one', 'rlk:lobby/go'):
        s.cache.setdefault(k, [])
    try:
        s.call(fn, Ctx(pl, tuple(pl.pos), (0, 0)))
    except Exception as ex:  # noqa: BLE001  the run functions reach engine parts the sim does not model
        print('     (', fn, 'raised', type(ex).__name__, str(ex)[:120], ')')
    check(f'3a {fn}: #cbForce 0, #cbAuto 0, cprep removed', (M.mb(s, '#cbForce') or 0) == 0 and (M.mb(s, '#cbAuto') or 0) == 0
          and 'cprep' not in st(s), (M.mb(s, '#cbForce'), M.mb(s, '#cbAuto'), 'cprep' in st(s)))


# ------------------------------------------------------------------------------------------------- 4 entrance + prep
print('== 4. entrance build -> cb/prep')
s, pl = fresh(chapter=2)
s.setsc('#mbTest', 'mb', 1)
s.setsc('#cbForce', 'mb', B['n'])
zs = M.boss_map(s, 2)
z9 = [z for z in zs if s.sc(('e', z.id), 'zkind') == 9][0]
check('4a before the entrance is built: no cprep, no forceload, no job', 'cprep' not in st(s) and box_released(s)
      and (M.mb(s, '#mbArBuild') or 0) == 0)
t0 = s.t
s.call('rlk:room/zone_build', Ctx(z9, tuple(z9.pos), (0, 0)))
cp = st(s).get('cprep', {}).get(BOSS)
check('4b zone build -> room/cboss/<id>/build -> cb/prep: cprep.<id> with gate l1..l3, title, sub',
      bool(cp) and all(k in cp.get('gate', {}) for k in ('l1', 'l2', 'l3')) and 'title' in cp and 'sub' in cp, cp)
check('4c the arena box is forceloaded', box_forceloaded(s), sorted(s.fl))
check('4d a sliced build job runs (#mbArBuild >= 1, arjob on cp_test, job_tick scheduled)',
      (M.mb(s, '#mbArBuild') or 0) >= 1 and st(s).get('arjob', {}).get('aid') == AID and 'rlk:mboss/arena/job_tick' in s.sched,
      (M.mb(s, '#mbArBuild'), st(s).get('arjob'), sorted(s.sched)))
check('4e the entrance blocks are built (zone 2 floor at the gate)', s.blocks.get((0, 200, 14)) is not None, s.blocks.get((0, 200, 14)))
nsl = st(s).get('arjob', {}).get('n')
ok = built(s)
check('4f the job ends within 400 t; slices <= 40', ok and nsl is not None and nsl <= 40, (ok, nsl, s.t - t0))
want = f'{AID}@{AR["ver"]}:{AR["looks"][0]}'
check('4g stamp = "<aid>@<ver>:<default look>"', stamp(s) == want, stamp(s))
(sx, sy, sz), sb = THEME.SENTINEL
check('4h the sentinel block stands', s.blocks.get((sx, sy, sz)) == sb.replace('minecraft:', ''), s.blocks.get((sx, sy, sz)))
lay = THEME.arena_layout(AR['looks'][0])
miss = [p for p, b in lay.items() if s.blocks.get(p, 'air').split('[')[0] != b.replace('minecraft:', '').split('[')[0]]
check('4i every block of the default look is in place', not miss, (len(miss), miss[:4]))
check('4j ensure now returns 1 (built, loaded, default look)', s.call('rlk:mboss/arena/' + AID + '/ensure', C0) == 1)
check('4k cb/prep did not start a fight (#combat 0, no body)', (s.sc('#combat', 'room') or 0) == 0 and M.body_of(s) is None)


# ------------------------------------------------------------------------------------------------- 5 the gate
print('== 5. the gate')


def objs(s, oact):
    return [e for e in s.ents if e.alive and 'rlk_obj' in e.tags and s.sc(('e', e.id), 'oact') == oact]


def setup_entrance(chapter=2, dp=DP, wait=True):
    s, pl = fresh(dp, chapter)
    s.setsc('#mbTest', 'mb', 1)
    s.setsc('#cbForce', 'mb', B['n'])
    zs = M.boss_map(s, chapter)
    z9, gate = M.entrance(s, zs)
    pl.pos = [z9.pos[0], 201.0, z9.pos[2] + 4]
    if wait:
        built(s)
    return s, pl, z9, M.gate_of(s)


s, pl, z9, gate = setup_entrance(wait=False)
check('5a zone_enter -> cb/enter: zst 3 and the gate object (oact 16, oarg = registry n) at the zone centre',
      gate is not None and s.sc(('e', z9.id), 'zst') == 3 and s.sc(('e', gate.id), 'oarg') == B['n']
      and abs(gate.pos[0] - z9.pos[0]) < 0.01 and abs(gate.pos[2] - z9.pos[2]) < 0.01, gate and (gate.pos, z9.pos))
lbl = [e for e in s.ents if e.alive and 'rlk_olbl' in e.tags]
check('5b the gate label and two icons come from cprep (k_cboss3)', len(lbl) == 1
      and len([e for e in s.ents if e.alive and 'rlk_odisp' in e.tags]) == 2)
t0 = mark(s)
check('5c an arena job runs right after the entrance build', (M.mb(s, '#mbArBuild') or 0) >= 1, M.mb(s, '#mbArBuild'))
M.click(s, gate)
check('5d pressed while #mbArBuild >= 1: "경기장을 준비하는 중" and the gate stays (no zone fight)',
      '경기장을 준비하는 중' in tells_since(s, t0) and M.gate_of(s) is gate and (s.sc('#combat', 'room') or 0) == 0)
built(s)
s.difficulty = 0
t0 = mark(s)
M.click(s, gate)
check('5e peaceful: refused with the difficulty hint, the gate stays', '평화로움' in tells_since(s, t0) and M.gate_of(s) is gate
      and (s.sc('#combat', 'room') or 0) == 0)
s.difficulty = 2
s.setsc(('e', z9.id), 'zst', 1)
t0 = mark(s)
M.click(s, gate)
check('5f the zone is not cleared (zst != 3): nothing happens', M.gate_of(s) is gate and (s.sc('#combat', 'room') or 0) == 0
      and not tells_since(s, t0), tells_since(s, t0)[-200:])
s.setsc(('e', z9.id), 'zst', 3)
fake = M.Ent('husk', (0.0, 201.0, 0.0), tags=['rlk_mb_body'])
s.ents.append(fake)
M.click(s, gate)
check('5g a boss body already exists: nothing happens', M.gate_of(s) is gate and (s.sc('#combat', 'room') or 0) == 0)
fake.alive = False
s.ents = [e for e in s.ents if e.alive]
s.setsc('#combat', 'room', 7)
M.click(s, gate)
check('5h during a zone fight room/obj/click refuses the press', M.gate_of(s) is gate)
s.setsc('#combat', 'room', 0)
t0 = len(s.titles)
M.click(s, gate)
check('5i pressed when ready: the object goes, the zone fight starts (#combat = zid, #spawnT 30), #cbWait 0',
      M.gate_of(s) is None and s.sc('#combat', 'room') == s.sc(('e', z9.id), 'zid') and s.sc('#spawnT', 'room') == 30
      and (M.mb(s, '#cbWait') or 0) == 0, (s.sc('#combat', 'room'), s.sc('#spawnT', 'room')))
tt = ' '.join(x for _, x in s.titles[t0:])
check('5j the gate title / subtitle come from cprep.<id>', f'cprep.{BOSS}.title' in tt and f'cprep.{BOSS}.sub' in tt, tt[:200])

# ------------------------------------------------------------------------------------------------- 6 spawn
print('== 6. spawn')
met0 = copy.deepcopy(st(s).get('met'))
ok = M.until(s, lambda s: M.body_of(s) is not None, 200)
b = M.body_of(s)
cur = st(s).get('cur', {})
check('6a #spawnT 0 -> room/boss_spawn -> cb/spawn_route -> cb/start: the body exists, cur = cbyid.<id>', ok and cur.get('id') == BOSS,
      cur.get('id'))
check('6b fight_vars: #mbMode 1, #mbAr = arena n, #mbPx 1; #mbForce 0; met unchanged (no roll, no met append)',
      M.mb(s, '#mbMode') == 1 and M.mb(s, '#mbAr') == AR['n'] and M.mb(s, '#mbPx') == 1 and (M.mb(s, '#mbForce') or 0) == 0
      and st(s).get('met') == met0, (M.mb(s, '#mbMode'), M.mb(s, '#mbAr'), M.mb(s, '#mbPx'), st(s).get('met'), met0))
tags = b.tags
check('6c the body: boss + rlk_mb_body + rlk_mb_big, no miniboss (the boss economy)',
      {'boss', 'rlk_mb_body', 'rlk_mb_big'} <= tags and 'miniboss' not in tags, sorted(tags))
p = pl.pos
check('6d the player stands at the arena start', abs(p[0] - AR['start']['x']) < 0.6 and abs(p[2] - AR['start']['z']) < 0.6, p)
tot = M.mb(s, '#mbTot')
check('6e the first pool: mhpM = #mbTot x phases[0] / 100', tot and M.esc(s, b, 'mhpM') == tot * B['phases'][0] // 100,
      (tot, M.esc(s, b, 'mhpM')))
ok = M.until(s, lambda s: M.mb(s, '#mbSt') == 1, 300)
check('6f the intro ends: #mbSt 1, the proxies live (normal set)', ok and st(s).get('px', {}).get('set') == 'normal',
      st(s).get('px', {}).get('set'))
check('6g #cbWait was reset by the successful spawn', (M.mb(s, '#cbWait') or 0) == 0)


# ------------------------------------------------------------------------------------------------- 7 kill
print('== 7. kill -> the boss economy, k_chapter')


def to_fight(chapter=2, dp=DP):
    s, pl = fresh(dp, chapter)
    z9, gate = M.fight(s, BOSS, chapter)
    return s, pl, z9


def kill(s):
    """Phase 1 ends at its floor (cproto: #mbFloor 1 -> phase2, the 40 % pool), then one big hit through a proxy."""
    s.setsc('#mbFloorHit', 'mb', 1)
    M.run(s, 2)
    b = M.body_of(s)
    s.setsc(('e', b.id), 'mhpC', 5)
    px = [e for e in M.proxies(s) if 'rlk_mob' in e.tags]
    M.A.strike(s, px[0] if px else b, 100000)
    return M.until(s, lambda s: M.body_of(s) is None, 200)


CH = 3
s, pl, z9 = to_fight(CH)
gold0 = gold_of(s)
sap0 = s.sc('#SAP', 'azs') or 0
gmin, gmax, gmul, bsap = (s.sc(k, 'tmp') for k in ('#mobGoldMin', '#mobGoldMax', '#bossGoldMul', '#bossSapphire'))
check('7a engine constants: #bossGoldMul 15, #bossSapphire 2', gmul == 15 and bsap == 2, (gmul, bsap))
dead = kill(s)
check('7b the kill ends the body', dead)
ok = M.until(s, lambda s: bool(objs(s, 8)), 200)
check('7c combat_clear -> cb/clear -> cb/won (killed) -> room/obj/k_chapter (oact 8) at the zone', ok and objs(s, 8)
      and abs(objs(s, 8)[0].pos[0] - z9.pos[0]) < 0.6, [e.pos for e in objs(s, 8)])
got = gold_of(s) - gold0
check(f'7d gold: one drop of random({gmin}..{gmax}) x chapter {CH} x 15, absorbed by cb/won (the arena box)',
      gmin * CH * gmul <= got <= gmax * CH * gmul, (got, gmin * CH * gmul, gmax * CH * gmul))
check('7e two sapphires (#bossSapphire), not the mid-boss #mbSap', (s.sc('#SAP', 'azs') or 0) - sap0 == bsap, (s.sc('#SAP', 'azs') or 0) - sap0)
check('7f no reward boxes (#mbBoxOn 0, no oact 15 object, no box entity)', (M.mb(s, '#mbBoxOn') or 0) == 0 and not objs(s, 15)
      and not [e for e in s.ents if e.alive and any(t.startswith('rlk_mb_box') for t in e.tags)])
check('7g the arena forceload is released', box_released(s), sorted(set(s.fl) & box_chunks()))
check('7h after the fight: #mbMode 0, music off, no proxies, no px storage; #mbAr keeps its value',
      (M.mb(s, '#mbMode') or 0) == 0 and (M.mb(s, '#mbMusPh') or 0) == 0 and 'mus' not in st(s) and not M.proxies(s)
      and 'px' not in st(s) and M.mb(s, '#mbAr') == AR['n'])
check('7i the player is back in the dungeon (ret position, not the arena)', abs(pl.pos[0] - AR['cx']) > 40, pl.pos)
check('7j cprep stays for the map (run_reset clears it)', BOSS in st(s).get('cprep', {}))

# ------------------------------------------------------------------------------------------------- 8 abort
print('== 8. abort -> the gate returns with the same cprep')
s, pl, z9 = to_fight(2)
cp0 = copy.deepcopy(st(s)['cprep'][BOSS])
gold0 = gold_of(s)
m0 = mark(s)
s.call('rlk:mboss/test/abort', M.Ctx(pl, tuple(pl.pos), (0, 0)))
ok = M.until(s, lambda s: M.gate_of(s) is not None, 100)
g2 = M.gate_of(s)
check('8a test/abort: no kill -> cb/won cancels -> the gate object again (oact 16) at the zone centre', ok and g2 is not None
      and abs(g2.pos[0] - z9.pos[0]) < 0.6 and not objs(s, 8))
check('8b the same cprep (texts, roll)', st(s)['cprep'][BOSS] == cp0, (st(s)['cprep'][BOSS], cp0))
check('8c the cancel message, no gold, forceload released', '취소' in tells_since(s, m0) and gold_of(s) == gold0 and box_released(s))
M.click(s, g2)
ok = M.until(s, lambda s: M.mb(s, '#mbSt') == 1, 400)
check('8d pressing again fights again (forceload back, the arena still built)', ok and box_forceloaded(s) and M.body_of(s) is not None)

# ------------------------------------------------------------------------------------------------- 9 lose
print('== 9. cb/lose, test/lose')
m0 = mark(s)
s.call('rlk:mboss/test/lose', M.Ctx(pl, tuple(pl.pos), (0, 0)))
check('9a test/lose -> cb/lose: #mbLost 1, the player at 0 HP (the normal death path)', M.mb(s, '#mbLost') == 1
      and s.sc(('e', pl.id), 'curHealth') == 0, (M.mb(s, '#mbLost'), s.sc(('e', pl.id), 'curHealth')))
st(s)['tlast'] = {'id': BOSS, 'ch': 2, 'cb': 1}      # as test/chapter_ch saves it
s.call('rlk:mboss/test/defeat', M.Ctx(pl, tuple(pl.pos), (0, 0)))
txt = tells_since(s, m0)
check('9b the test defeat message offers the chapter replay (test/chapter_ch {id,ch})', 'chapter_ch' in txt and BOSS in txt, txt[-300:])
s2, pl2 = fresh()
m0 = mark(s2)
s2.call('rlk:mboss/test/lose', M.Ctx(pl2, tuple(pl2.pos), (0, 0)))
check('9c test/lose without a boss: refused', (M.mb(s2, '#mbLost') or 0) == 0 and '없습니다' in tells_since(s2, m0))

# ------------------------------------------------------------------------------------------------- 10 title, repool, level
print('== 10. title swap, repool + #mbTot, test/level')
s, pl, z9 = to_fight(2)
b = M.body_of(s)
tot = M.mb(s, '#mbTot')
s.call('rlk:mboss/cproto/test', M.Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 40})
check('10a mboss/title: cur.title / cur.sub replaced (the bars read cur.title)', '이름 교체' in json.dumps(st(s)['cur']['title'], ensure_ascii=False),
      st(s)['cur'].get('title'))
s.setsc('#mbFloorHit', 'mb', 1)
M.run(s, 2)
check('10b phase 2 (floor reached): repool 40 -> mhpM = mhpC = #mbTot x 40 / 100, #mbTot unchanged, #mbRamp >= 1',
      M.esc(s, b, 'mhpM') == tot * 40 // 100 and M.esc(s, b, 'mhpC') == tot * 40 // 100 and M.mb(s, '#mbTot') == tot
      and (M.mb(s, '#mbRamp') or 0) >= 1 and M.mb(s, '#mbPoolPct') == 40, (M.esc(s, b, 'mhpM'), tot, M.mb(s, '#mbRamp')))
check('10c phase 2 title and music phase 2', '2단계' in json.dumps(st(s)['cur']['title'], ensure_ascii=False) and M.mb(s, '#mbMusPh') == 2)
s.cache['rlk:mob/level_apply'] = ['scoreboard players set @s mhpM 77700', 'scoreboard players set @s mhpC 77700']
s.call('rlk:mboss/test/level', M.Ctx(pl, tuple(pl.pos), (0, 0)), {'lv': 9})
check('10d test/level: #mbTot = the new full HP, the split re-applied (mhpM = #mbTot x 40 / 100)',
      M.mb(s, '#mbTot') == 77700 and M.esc(s, b, 'mhpM') == 77700 * 40 // 100, (M.mb(s, '#mbTot'), M.esc(s, b, 'mhpM')))
s.call('rlk:mboss/repool', C0, {'pct': 250})
check('10e repool clamps pct to 1..100', M.mb(s, '#mbPoolPct') == 100 and M.esc(s, b, 'mhpM') == 77700)
s.setsc('#mbTot', 'mb', 2000000000)
s.call('rlk:mboss/repool', C0, {'pct': 60})
check('10f repool is overflow-safe (#mbTot 2e9 x 60 %)', M.esc(s, b, 'mhpM') == 2000000000 // 100 * 60, M.esc(s, b, 'mhpM'))


# ------------------------------------------------------------------------------------------------- 10b the test command
print('== 10b. test/chapter_ch (the command path)')
s, pl = fresh()
s.gen_hook = lambda s: M.boss_map(s, s.sc('#chapter', 'room'))
s.setsc('#active', 'room', 0)
s.call('rlk:mboss/test/chapter_ch', M.Ctx(pl, tuple(pl.pos), (0, 0)), {'id': BOSS, 'ch': 3})
check('10g chapter_ch: tlast {id, ch 3, cb 1b}, #mbTest 1, #cbForce = n, #cbAuto 1, #chapter 3, #mbForce 0',
      st(s).get('tlast') == {'id': BOSS, 'ch': 3, 'cb': 1} and M.mb(s, '#mbTest') == 1 and M.mb(s, '#cbForce') == B['n']
      and M.mb(s, '#cbAuto') == 1 and s.sc('#chapter', 'room') == 3 and (M.mb(s, '#mbForce') or 0) == 0, st(s).get('tlast'))
check('10h the entrance was built (cprep), the gate stands, test/cwait scheduled', BOSS in st(s).get('cprep', {})
      and M.gate_of(s) is not None and 'rlk:mboss/test/cwait' in s.sched)
ok = M.until(s, lambda s: M.mb(s, '#mbSt') == 1, 600)
check('10i cwait presses the gate once the arena job ended (#cbAuto 0 after), the fight starts', ok and (M.mb(s, '#cbAuto') or 0) == 0)
s.call('rlk:mboss/test/stop', M.Ctx(pl, tuple(pl.pos), (0, 0)))
check('10j test/stop: #cbForce 0, #mbTest 0, the fight gone, forceload released', (M.mb(s, '#cbForce') or 0) == 0
      and (M.mb(s, '#mbTest') or 0) == 0 and M.body_of(s) is None and box_released(s))
s, pl = fresh()
s.setsc('#active', 'room', 1)
m0 = mark(s)
s.call('rlk:mboss/test/chapter_ch', M.Ctx(pl, tuple(pl.pos), (0, 0)), {'id': BOSS, 'ch': 1})
check('10k0 chapter_ch during a run (no test): refused (run/stop first)', (M.mb(s, '#cbForce') or 0) == 0 and 'run/stop' in tells_since(s, m0))
s.setsc('#active', 'room', 0)
s.difficulty = 0
m0 = mark(s)
s.call('rlk:mboss/test/chapter_ch', M.Ctx(pl, tuple(pl.pos), (0, 0)), {'id': BOSS, 'ch': 1})
check('10k1 chapter_ch on peaceful: refused', (M.mb(s, '#cbForce') or 0) == 0 and '평화로움' in tells_since(s, m0))
s.difficulty = 2
m0 = mark(s)
s.call('rlk:mboss/test/chapter_ch', M.Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 'nosuch', 'ch': 1})
check('10k chapter_ch of an unknown id: refused', (M.mb(s, '#cbForce') or 0) == 0 and '등록되지 않았거나' in tells_since(s, m0))
s.gen_hook = lambda s: M.boss_map(s, s.sc('#chapter', 'room'))
s.call('rlk:mboss/test/chapter', M.Ctx(pl, tuple(pl.pos), (0, 0)), {'id': BOSS})
check('10l test/chapter {id} -> chapter_ch in the boss\'s first chapter (none: 1)', st(s).get('tlast', {}).get('ch') == ((B.get('ch') or [1])[0]),
      st(s).get('tlast'))

# ------------------------------------------------------------------------------------------------- 11 music
print('== 11. music')


def plays(s, t0=0, name='music.'):
    return [(t, ev) for t, ev, _ in s.sounds if t >= t0 and ev.startswith(name)]


s, pl, z9 = to_fight(2)
mus = st(s).get('mus')
check('11a fight start: music/set {ph:1} -> mus {ph 1, ev, len} from cur.music."1"; #mbMusPh 1',
      mus == {'ph': 1, 'ev': B['music']['1']['ev'], 'len': B['music']['1']['len']} and M.mb(s, '#mbMusPh') == 1, mus)
check('11b the track plays in the record category at the player', any(ev == B['music']['1']['ev'].split(':')[-1] for _, ev in plays(s)),
      plays(s))
t0 = s.t
M.run(s, 200)
nst = [t for t, x in s.stops if t > t0 and x == 'music']
check('11c vanilla music stopped every 100 t (stopsound @a[tag=player] music)', len(nst) == 2 and nst[1] - nst[0] == 100, nst)
s.setsc('#mbMusT', 'mb', B['music']['1']['len'] - 1)
t1 = s.t
M.run(s, 1)
ev1 = B['music']['1']['ev']
check('11d at len the track restarts from 0 (stop record <ev>, play <ev>, #mbMusT 0)',
      any(x == 'record ' + ev1 for t, x in s.stops if t > t1) and plays(s, t1 + 1) and (M.mb(s, '#mbMusT') or 0) <= 1, plays(s, t1 + 1))
t2 = s.t
s.call('rlk:mboss/cproto/test', M.Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 41})
ev2 = B['music']['2']['ev']
st2 = [x for t, x in s.stops if t >= t2]
check('11e music/set {ph:2}: the phase-1 track stops before the phase-2 track plays (no overlap)',
      ('record ' + ev1) in st2 and plays(s, t2) and plays(s, t2)[-1][1] == ev2.split(':')[-1] and M.mb(s, '#mbMusPh') == 2, (st2, plays(s, t2)))
s.setsc(('e', pl.id), 'pkMode', 1)
t3 = s.t
M.run(s, 3)
check('11f the pause edge halts the track (stop record <ev>), #mbMusPh and mus kept, no replay while paused',
      any(x == 'record ' + ev2 for t, x in s.stops if t > t3) and M.mb(s, '#mbMusPh') == 2 and st(s).get('mus', {}).get('ph') == 2
      and not plays(s, t3 + 1))
s.setsc(('e', pl.id), 'pkMode', 0)
t4 = s.t
M.run(s, 2)
check('11g resume restarts the phase track from its start', plays(s, t4 + 1) and plays(s, t4 + 1)[0][1] == ev2.split(':')[-1]
      and (M.mb(s, '#mbMusT') or 0) <= 2)
s.call('rlk:mboss/cproto/test', M.Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 42})
check('11h music/set {ph:0} -> music/stop: mus removed, #mbMusPh 0', 'mus' not in st(s) and M.mb(s, '#mbMusPh') == 0)
s.call('rlk:mboss/music/set', C0, {'ph': 7})
check('11i a phase without a track stops the music', 'mus' not in st(s) and M.mb(s, '#mbMusPh') == 0)
s.call('rlk:mboss/music/set', C0, {'ph': 1})
s.call('rlk:mboss/death_start', M.Ctx(M.body_of(s), tuple(M.body_of(s).pos), (0, 0)))
check('11j death_start stops the music', 'mus' not in st(s) and M.mb(s, '#mbMusPh') == 0)

# ------------------------------------------------------------------------------------------------- 12 looks
print('== 12. cp_test looks')
s, pl, z9, gate = setup_entrance()
looks = AR['looks']
diff = {p for lk in looks for p in set(THEME.arena_layout(lk).items()) ^ set(THEME.arena_layout(looks[0]).items())}
s.call(f'rlk:mboss/arena/{AID}/look/{looks[1]}', C0)
check('12a a look job: one slice (the look diff), the stamp dropped until done', st(s).get('arjob', {}).get('n') == 1
      and st(s).get('arjob', {}).get('kind') == 'look' and stamp(s) is None, st(s).get('arjob'))
built(s)
lay1 = THEME.arena_layout(looks[1])
miss = [p for p, b in lay1.items() if s.blocks.get(p, 'air').split('[')[0] != b.replace('minecraft:', '').split('[')[0]]
check(f'12b stamp "{AID}@{AR["ver"]}:{looks[1]}" and every block of that look', stamp(s) == f'{AID}@{AR["ver"]}:{looks[1]}' and not miss,
      (stamp(s), len(miss)))
r = s.call(f'rlk:mboss/arena/{AID}/ensure', C0)
check('12c ensure in the other look: fail, and the default-look job starts', not r and st(s).get('arjob', {}).get('look') == looks[0]
      and st(s).get('arjob', {}).get('kind') == 'look', st(s).get('arjob'))
built(s)
lay0 = THEME.arena_layout(looks[0])
miss = [p for p, b in lay0.items() if s.blocks.get(p, 'air').split('[')[0] != b.replace('minecraft:', '').split('[')[0]]
check('12d the default look is back (stamp, blocks); ensure returns 1', stamp(s) == f'{AID}@{AR["ver"]}:{looks[0]}' and not miss
      and s.call(f'rlk:mboss/arena/{AID}/ensure', C0) == 1, (stamp(s), len(miss)))
s.call(f'rlk:mboss/ar/{AID}/fl_off', C0)
pl.pos = [0.5, 201.0, 33.5]
r = s.call(f'rlk:mboss/arena/{AID}/ensure', C0)
check('12e built but not loaded: fail and a verify job (no rebuild)', not r and st(s).get('arjob', {}).get('kind') == 'verify')
fills0 = s.fills
s.call(f'rlk:mboss/ar/{AID}/fl_on', C0)
built(s)
check('12f the verify job ends once the chunks load: stamp kept, nothing rebuilt', stamp(s) == f'{AID}@{AR["ver"]}:{looks[0]}'
      and s.fills == fills0, (stamp(s), s.fills - fills0))
(sx, sy, sz), sb = THEME.SENTINEL
s.setb(sx, sy, sz, 'air')
r = s.call(f'rlk:mboss/arena/{AID}/ensure', C0)
check('12g a wrong sentinel: ensure fails and starts a full build', not r and st(s).get('arjob', {}).get('kind') == 'build')
built(s)
check('12h the build restores the sentinel and the stamp', stamp(s) == f'{AID}@{AR["ver"]}:{looks[0]}' and s.blocks.get((sx, sy, sz)) is not None)
s.call(f'rlk:mboss/arena/{AID}/ensure', C0)
s.call(f'rlk:mboss/ar/{AID}/fl_off', C0)
s.call(f'rlk:mboss/arena/{AID}/rebuild', C0)
M.run(s, 210)
check('12i a job whose chunks never load aborts after 200 t (#mbArBuild 0, no stamp, no arjob)', (M.mb(s, '#mbArBuild') or 0) == 0
      and stamp(s) is None and 'arjob' not in st(s), (M.mb(s, '#mbArBuild'), stamp(s)))


# ------------------------------------------------------------------------------------------------- 13 cleanup paths
print('== 13. cleanup paths')


def safe_call(s, fid, ctx=C0, macro=None):
    try:
        return s.call(fid, ctx, macro)
    except Exception as ex:  # noqa: BLE001  engine parts the sim does not model (after the mboss lines)
        print('     (', fid, 'raised', type(ex).__name__, str(ex)[:100], ')')


def gone(s):
    return (M.body_of(s) is None and not M.proxies(s) and 'mus' not in st(s) and (M.mb(s, '#mbMusPh') or 0) == 0
            and (M.mb(s, '#mbMode') or 0) == 0 and box_released(s) and (M.mb(s, '#mbPushOn') or 0) == 0
            and (M.mb(s, '#mbCine') or 0) == 0 and not [e for e in s.ents if e.alive and 'rlk_mb_arena_prop' in e.tags])


for fid in ('rlk:room/clear', 'rlk:room/wipe', 'rlk:mboss/cleanup'):
    s, pl, z9 = to_fight(2)
    props0 = len([e for e in s.ents if e.alive and 'rlk_mb_arena_prop' in e.tags])
    safe_call(s, fid)
    check(f'13a {fid}: the fight, proxies, music, props, cine / push flags and the arena forceload are gone (props were {props0})',
          gone(s) and props0 >= 1, (M.body_of(s) is not None, len(M.proxies(s)), st(s).get('mus'), M.mb(s, '#mbMode'), box_released(s)))
s, pl, z9 = to_fight(2)
safe_call(s, 'rlk:room/remove')
check('13b room/remove -> cb/remove: fight gone, the arena cleared while loaded (floor air), stamp dropped, forceload released',
      gone(s) and s.blocks.get((AR['cx'], AR['cy'] - 1, AR['cz'])) is None and stamp(s) is None, (stamp(s), s.blocks.get((AR['cx'], AR['cy'] - 1, AR['cz']))))
s, pl, z9, gate = setup_entrance(wait=False)
check('13c (a job runs)', (M.mb(s, '#mbArBuild') or 0) >= 1)
safe_call(s, 'rlk:room/remove')
check('13d room/remove during an arena job: aborted (#mbArBuild 0, no arjob, no stamp, job_tick unscheduled)',
      (M.mb(s, '#mbArBuild') or 0) == 0 and 'arjob' not in st(s) and stamp(s) is None and 'rlk:mboss/arena/job_tick' not in s.sched)
s, pl, z9 = to_fight(2)
safe_call(s, 'rlk:mboss/uninstall')
mbst = st(s)
check('13e mboss/uninstall mid-fight: forceload released, music stopped, chapter storage removed, no job',
      box_released(s) and 'mus' not in mbst and not any(k in mbst for k in ('creg', 'cbyid', 'cprep', 'arjob', 'built_' + AID))
      and 'rlk:mboss/arena/job_tick' not in s.sched, sorted(k for k in mbst if k in ('creg', 'cbyid', 'cprep', 'arjob', 'built_' + AID)))
s, pl, z9 = to_fight(2)
uu0 = sorted(getattr(e, 'uuid', None) or '' for e in M.proxies(s))
set0 = st(s)['px']['set']
s.call('rlk:mboss/init', C0)
M.run(s, 2)
uu1 = sorted(getattr(e, 'uuid', None) or '' for e in M.proxies(s))
check('13f /reload mid-fight (mboss/init -> reload): the body stays, the proxies come back with the same UUIDs and set, forceload kept',
      M.body_of(s) is not None and uu1 == uu0 and len(uu1) == 2 and st(s)['px']['set'] == set0 and box_forceloaded(s), (uu0, uu1))
check('13g after /reload the fight runs on (#mbSt 1, #mbMode 1, #mbAr)', M.mb(s, '#mbSt') == 1 and M.mb(s, '#mbMode') == 1
      and M.mb(s, '#mbAr') == AR['n'])
s, pl, z9, gate = setup_entrance(wait=False)
s.sched.clear()
s.call('rlk:mboss/init', C0)
check('13h /reload during an arena job: mboss/init re-arms job_tick', 'rlk:mboss/arena/job_tick' in s.sched)
check('13i ... and the job completes', built(s) and stamp(s) == f'{AID}@{AR["ver"]}:{AR["looks"][0]}')


def v_sweep(reg):
    reg['arenas'][AID]['sweep'] = {'y0': 201, 'y1': 202}


V2 = M.variant(DP, v_sweep, 'sweep')
try:
    line = f'function rlk:mboss/arena/{AID}/sweep {{y0:201,y1:202}}'
    for f in ('cb/won', 'cleanup', 'cb/remove'):
        txt = (V2 / f'data/rlk/function/mboss/{f}.mcfunction').read_text(encoding='utf-8')
        check(f'13j variant (cp_test sweep {{201,202}}): mboss/{f} runs arena/{AID}/sweep with it', line in txt)
    txt = (DP / 'data/rlk/function/mboss/cleanup.mcfunction').read_text(encoding='utf-8')
    check('13k the shipped registry (no sweep) has no sweep line', f'arena/{AID}/sweep' not in txt)

    def barriers(s):
        return [p for p, b in s.blocks.items() if b == 'barrier']

    for f, how in (('rlk:mboss/cleanup', 'cleanup'), ('rlk:room/remove', 'remove'), ('won', 'cb/won')):
        s, pl, z9 = to_fight(2, V2)
        cx, cz = AR['cx'], AR['cz']
        for x, y, z in ((cx, 201, cz), (cx + 3, 202, cz - 2), (cx - 5, 201, cz + 4)):
            s.setb(x, y, z, 'barrier')
        s.setb(cx + 12, 201, cz, 'barrier')           # beyond walk - 0.5: never touched
        if f == 'won':
            s.call('rlk:mboss/test/abort', M.Ctx(pl, tuple(pl.pos), (0, 0)))
            M.until(s, lambda s: M.gate_of(s) is not None, 100)
        else:
            safe_call(s, f)
        left = barriers(s)
        if how == 'remove':      # cb/remove sweeps, then arena/<aid>/clear airs the whole box
            check('13l variant: remove sweeps the band and clears the box (no barrier left)', left == [], left)
        else:
            check(f'13l variant: {how} sweeps the barrier band inside walk (the one outside stays)', left == [(cx + 12, 201, cz)], left)
finally:
    M.drop_variant(V2)

# ------------------------------------------------------------------------------------------------- 14 Raiden smoke
print(f'== 14. Raiden smoke (chapter {RD_CH})')
s, pl = fresh(chapter=RD_CH)
rd0 = s.sc('#RDLAYOUT', 'azs') or 0
s.call('rlk:room/pick/boss', C0)
check('14a room/pick/boss -> cb/route -> room/raiden/layout', (s.sc('#RDLAYOUT', 'azs') or 0) == rd0 + 1)
z = M.Ent('marker', (0.5, 201.0, 14.5), tags=['rlk_room', 'rlk_zone'])
z.data = {'boss_id': 'narukami', 'fn': 'boss_narukami', 'id': 2, 'kind': 9}
s.ents.append(z)
for o, v in (('zid', 2), ('zkind', 9), ('zst', 0)):
    s.setsc(('e', z.id), o, v)
zc = M.Ctx(z, tuple(z.pos), (0, 0))
b0, c0 = s.sc('#RDBUILD', 'azs') or 0, len(st(s).get('cprep', {}))
s.call('rlk:room/zone_build', zc)
check('14b a narukami zone builds through room/raiden/build (no chapter build, no cprep)', (s.sc('#RDBUILD', 'azs') or 0) == b0 + 1
      and len(st(s).get('cprep', {})) == c0 and (M.mb(s, '#mbArBuild') or 0) == 0)
s.call('rlk:room/boss_spawn', zc)
check('14c room/boss_spawn reaches boss/raiden/spawn (stubbed)', (s.sc('#RDSPAWN', 'azs') or 0) == 1 and M.body_of(s) is None)
for e in s.ents:
    if 'rlk_azs_raiden' in e.tags:
        e.alive = False
s.ents = [e for e in s.ents if e.alive]
s.call('rlk:room/combat_clear', zc)
check('14d combat_clear still spawns k_chapter (oact 8) for Raiden', len(objs(s, 8)) == 1 and (M.mb(s, '#mbKilled') or 0) == 0)

# ------------------------------------------------------------------------------------------------- 15 fix-round regressions
print('== 15. CM fix round: test-session state, jobs at fight end, auto press, dev view, uninstall')


def pctx(s):
    pl = s.player()
    return M.Ctx(pl, tuple(pl.pos), (0, 0))


def gen_hook(s):
    M.boss_map(s, s.sc('#chapter', 'room'))


# STATE-1: a chapter test session after the kill
s, pl = fresh()
s.gen_hook = gen_hook
s.setsc('#active', 'room', 0)
s.call('rlk:mboss/test/chapter_ch', pctx(s), {'id': BOSS, 'ch': 2})
ok = M.until(s, lambda s: M.mb(s, '#mbSt') == 1, 600)
m0 = mark(s)
dead = ok and kill(s)
M.until(s, lambda s: bool(objs(s, 8)), 200)
txt = tells_since(s, m0)
check('15a STATE-1 chapter test kill: test/won -> test/cwon: #cbForce 0, #cbAuto 0 (the test session itself goes on, #mbTest 1)',
      dead and (M.mb(s, '#cbForce') or 0) == 0 and (M.mb(s, '#cbAuto') or 0) == 0 and M.mb(s, '#mbTest') == 1 and objs(s, 8),
      (dead, M.mb(s, '#cbForce'), M.mb(s, '#cbAuto'), M.mb(s, '#mbTest')))
check('15b ... the chapter wording and the test/chapter_ch replay link of this boss and chapter',
      '챕터 보스 테스트' in txt and f'chapter_ch {{id:"{BOSS}",ch:2}}' in txt and st(s).get('tlast', {}).get('cb') in (1, True), txt[-300:])
rd0 = s.sc('#RDLAYOUT', 'azs') or 0
zs = M.boss_map(s, 3)
ids = [z.data.get('boss_id') for z in zs]
exp = routed(REG, 3)
check(f'15c ... the next chapter\'s boss map (k_chapter -> chapter 3) routes as in a run: {exp or "Raiden"}',
      route_ok((s.sc('#RDLAYOUT', 'azs') or 0) - rd0, ids, exp), (ids, exp))
# a later mid-boss fight in the same session (k_chapter -> a 중간보스 node): its won / defeat speak mid-boss
st(s)['cur'] = {'id': 'guardian', 'n': 1}
s.setsc('#mbKilled', 'mb', 1)
m0 = mark(s)
s.call('rlk:mboss/test/won', C0, {'id': 'guardian'})
txt = tells_since(s, m0)
check('15d ... a later mid-boss win in that session: the mid-boss wording and test/start_ch link (no chapter_ch {id:"guardian"})',
      '중간보스 테스트' in txt and 'start_ch {id:"guardian"' in txt and 'chapter_ch' not in txt and 'cb' not in st(s).get('tlast', {}), txt[-300:])
st(s)['tlast'] = {'id': BOSS, 'ch': 2, 'cb': 1}
st(s)['cur'] = {'id': 'guardian', 'n': 1}
m0 = mark(s)
s.call('rlk:mboss/test/defeat', pctx(s))
txt = tells_since(s, m0)
check('15e ... a defeat by that mid-boss: the mid-boss wording and test/start_ch link (the fight decides, not the session)',
      'start_ch {id:"guardian"' in txt and 'chapter_ch' not in txt, txt[-300:])
# STATE-1 / IDENTITY-6: a mid-boss test started from a chapter session never routes boss maps to the chapter boss
s, pl = fresh()
s.gen_hook = gen_hook
s.setsc('#active', 'room', 0)
s.call('rlk:mboss/test/chapter_ch', pctx(s), {'id': BOSS, 'ch': 2})
M.until(s, lambda s: M.mb(s, '#mbSt') == 1, 600)
s.gen_hook = lambda s: None
safe_call(s, 'rlk:mboss/test/start_ch', pctx(s), {'id': 'proto', 'ch': RD_CH})
check('15f IDENTITY-6 test/start_ch from a chapter session: #cbForce 0, #cbAuto 0, #mbForce = proto',
      (M.mb(s, '#cbForce') or 0) == 0 and (M.mb(s, '#cbAuto') or 0) == 0 and M.mb(s, '#mbForce') == M.entry(REG, 'proto')['n'],
      (M.mb(s, '#cbForce'), M.mb(s, '#cbAuto'), M.mb(s, '#mbForce')))
rd0 = s.sc('#RDLAYOUT', 'azs') or 0
zs = M.boss_map(s, RD_CH)
check(f'15g ... its boss map of chapter {RD_CH} is Raiden\'s', route_ok((s.sc('#RDLAYOUT', 'azs') or 0) - rd0, [z.data.get('boss_id') for z in zs], None))

# STATE-2: the fight ends while a job of its arena runs (a module look swap / rebuild)
s, pl, z9 = to_fight(2)
s.call(f'rlk:mboss/arena/{AID}/rebuild', C0)
check('15h (a job of the fight arena runs: #mbArBuild >= 1, arjob on it)', (M.mb(s, '#mbArBuild') or 0) >= 1
      and st(s).get('arjob', {}).get('aid') == AID)
s.call('rlk:mboss/test/abort', pctx(s))
ok = M.until(s, lambda s: M.gate_of(s) is not None, 100)
check('15i STATE-2 cb/won ends that job before the forceload goes: #mbArBuild 0, no arjob, job_tick unscheduled, forceload released',
      ok and (M.mb(s, '#mbArBuild') or 0) == 0 and 'arjob' not in st(s) and 'rlk:mboss/arena/job_tick' not in s.sched and box_released(s),
      (M.mb(s, '#mbArBuild'), st(s).get('arjob'), box_released(s)))
m0 = mark(s)
M.click(s, M.gate_of(s))
check('15j ... the next press is not refused ("준비 중"): the fight starts (forceload back)', '준비하는 중' not in tells_since(s, m0)
      and M.gate_of(s) is None and box_forceloaded(s), tells_since(s, m0)[-200:])
ok = M.until(s, lambda s: M.mb(s, '#mbSt') == 1, 600)
check('15k ... ensure rebuilt the arena (stamp back) and the fight runs', ok and stamp(s) == f'{AID}@{AR["ver"]}:{AR["looks"][0]}', stamp(s))
s, pl, z9, gate = setup_entrance(wait=False)
check('15l (an entrance job runs)', (M.mb(s, '#mbArBuild') or 0) >= 1)
safe_call(s, 'rlk:mboss/cleanup')
check('15m STATE-2 mboss/cleanup during a job of a chapter arena: the job ends with its forceload (#mbArBuild 0, no arjob, '
      'job_tick unscheduled, no stamp of the half-built arena)', (M.mb(s, '#mbArBuild') or 0) == 0 and 'arjob' not in st(s)
      and 'rlk:mboss/arena/job_tick' not in s.sched and stamp(s) is None and box_released(s))

# STATE-4: a manual press ends the test's auto press
s, pl = fresh()
s.gen_hook = gen_hook
s.setsc('#active', 'room', 0)
s.call('rlk:mboss/test/chapter_ch', pctx(s), {'id': BOSS, 'ch': 2})
M.until(s, lambda s: (M.mb(s, '#mbArBuild') or 0) == 0, 400)
M.click(s, M.gate_of(s))
check('15n STATE-4 a manual gate press inside the cwait window: #cbAuto 0 (cb/g/<id>)', (M.mb(s, '#cbAuto') or 0) == 0, M.mb(s, '#cbAuto'))
M.until(s, lambda s: M.mb(s, '#mbSt') == 1, 300)
m0 = mark(s)
s.call('rlk:mboss/test/abort', pctx(s))
M.until(s, lambda s: M.gate_of(s) is not None, 50)
M.run(s, 12)
check('15o ... a gate that comes back inside the window is not pressed for the player', M.gate_of(s) is not None
      and (s.sc('#combat', 'room') or 0) == 0, (M.gate_of(s), s.sc('#combat', 'room')))
M.run(s, 300)
check('15p ... and no "경기장 준비 시간 초과" line later', '시간 초과' not in tells_since(s, m0))

# STATE-6: the dev view releases its forceload once built; the entrance prep keeps its own for the fight
s, pl = fresh()
s.setsc('#active', 'room', 0)
s.call(f'rlk:mboss/ar/{AID}/test', pctx(s))
check('15q (the dev view forceloads the box and builds)', box_forceloaded(s) and (M.mb(s, '#mbArBuild') or 0) >= 1)
built(s)
check('15r STATE-6 dev view outside a run: the finished job releases the forceload (stamp kept)', box_released(s)
      and stamp(s) == f'{AID}@{AR["ver"]}:{AR["looks"][0]}', (sorted(set(s.fl) & box_chunks()), stamp(s)))
s, pl, z9, gate = setup_entrance(wait=True)
check('15s ... in a run the entrance prep\'s job keeps the forceload for the fight', box_forceloaded(s) and (M.mb(s, '#mbArBuild') or 0) == 0)

# STATE-7: uninstall removes the chapter scratch keys
s, pl = fresh()
s.gen_hook = gen_hook
s.setsc('#active', 'room', 0)
s.call('rlk:mboss/test/chapter', pctx(s), {'id': BOSS})
M.until(s, lambda s: M.mb(s, '#mbSt') == 1, 600)
s.call('rlk:mboss/px/state', C0, {'set': 'normal'})
for aid in REG['arenas']:
    s.call(f'rlk:mboss/arena/{aid}/sweep', C0, {'y0': 201, 'y1': 202})
have = sorted(k for k in ('cbg', 'tch', 'pxq', 'arsw') if k in st(s))
safe_call(s, 'rlk:mboss/uninstall')
left = sorted(k for k in ('cbg', 'tch', 'pxq', 'arsw', 'cbl', 'creg', 'cbyid', 'cprep', 'arjob') if k in st(s))
check(f'15t STATE-7 uninstall mid-fight after test/chapter removes the chapter scratch keys (had {have})', not left and len(have) >= 3, left)

print('== 16. recheck: a chapter arena counts as loaded only when every chunk of its box is (PERF-1)')
for aid, a in REG['arenas'].items():
    s, pl = M.setup(DP)
    pl.pos = [0.5, 201.0, 33.5]
    s.call(f'rlk:mboss/ar/{aid}/fl_on', C0)
    M.run(s, M.LOAD_DELAY[0] + 1)
    all_in = s.call(f'rlk:mboss/ar/{aid}/loaded', C0)
    bx = a['box']
    probes = {(bx['x0'] >> 4, bx['z0'] >> 4), (bx['x1'] >> 4, bx['z1'] >> 4), (a['cx'] >> 4, a['cz'] >> 4)}
    inner = sorted(c for c in s.fl if bx['x0'] >> 4 <= c[0] <= bx['x1'] >> 4 and bx['z0'] >> 4 <= c[1] <= bx['z1'] >> 4 and c not in probes)
    late = inner[len(inner) // 2]
    s.fl[late] = s.t          # this one chunk is still loading (forced chunks load in no fixed order)
    one_late = s.call(f'rlk:mboss/ar/{aid}/loaded', C0)
    check(f'16 {aid}: ar/{aid}/loaded is 1 with the whole box loaded and fails while chunk {late} (not a corner / the centre) still loads',
          all_in == 1 and not one_late, (all_in, one_late))

print('== 17. merge prep: releasing the forceload aborts a running job of that arena (PERF-2)')
s, pl, z9, gate = setup_entrance(wait=False)
check('17a (an entrance job of the arena runs, its box forceloaded)', (M.mb(s, '#mbArBuild') or 0) >= 1
      and st(s).get('arjob', {}).get('aid') == AID and box_forceloaded(s))
for other in REG['arenas']:
    if other != AID:
        s.call(f'rlk:mboss/ar/{other}/fl_off', C0)
check('17b ar/<aid>/fl_off of another arena leaves the job alone', (M.mb(s, '#mbArBuild') or 0) >= 1
      and st(s).get('arjob', {}).get('aid') == AID)
safe_call(s, f'rlk:mboss/ar/{AID}/fl_off')
check('17c PERF-2 ar/<aid>/fl_off called directly (no cb/won, no cleanup) during its job: the job ends at once '
      '(#mbArBuild 0, no arjob, job_tick unscheduled, no stamp of the half-built arena) and the box is released',
      (M.mb(s, '#mbArBuild') or 0) == 0 and 'arjob' not in st(s) and 'rlk:mboss/arena/job_tick' not in s.sched
      and stamp(s) is None and box_released(s), (M.mb(s, '#mbArBuild'), st(s).get('arjob'), sorted(s.sched), stamp(s)))
m0 = mark(s)
M.run(s, 5)
M.click(s, M.gate_of(s))
check('17d ... the next gate press is not refused ("준비 중"): the fight starts (forceload back)', '준비하는 중' not in tells_since(s, m0)
      and M.gate_of(s) is None and box_forceloaded(s), tells_since(s, m0)[-200:])
ok = M.until(s, lambda s: M.mb(s, '#mbSt') == 1, 600)
check('17e ... ensure rebuilt the arena (stamp back) and the fight runs', ok and stamp(s) == f'{AID}@{AR["ver"]}:{AR["looks"][0]}', stamp(s))

M.summary('CHAPTER')
