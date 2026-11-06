#!/usr/bin/env python3
"""test_arlecchino.py (S3): the 아를레키노 module core in the knsim world (S:ar/s3/lib/knsim.py; PLAN §4, §7, §11.3).

    python3 test_arlecchino.py [<roguelike dir>] [section ...]

 1 static: the 17 hooks + prep + test/help + init; every rlk:boss/arlecchino reference resolves; standing rules (no
   negative add/remove literals, vanilla sounds only, no font, the only texts are names / phase titles / pattern names /
   the badge / dialog lines / help rows, every tp is rotation-only or behind mv/ok); no ranged immunity and no Pyro
   resistance anywhere (res {"*":10}, no projectile filter, no evasion, an empty incoming)
 2 phases: intro -> P1a -> (70 % floor) E70 -> P1b -> (floor 1) T -> P2 -> death; floors stop a hit at the floor, the
   step waits for the next decision; E70 once; titles, music 1 at 136 / 2 at T 140, repool 36, rlk_mb_inv / cine
 3 Bond of Life: a bol hit (+6 %, her heal, #given), x2.5 only while bonded (#mbBolRe), plain hits never bond, the DoT
   only after her bond and never lethal, the forced bond (+18 %, the skip states), clear -> 선혈의 충격 + badge, cleanup
   takes back only her part (a Clorinde / Arlecchino player keeps her own)
 4 the normal-attack predicate per attack kind (+ the per-character table of the engine files)
 5 the shock: break inside a window (cancel, clamped true damage 15 % / 12.5 %, brk -> stun, the F schedule restart),
   the 2 % burst outside, the clamp (never skips E70 / T), the stun
 6 heal orbs: 3 per forced bond, 6-14 b, 120 deg apart, <= 3 alive, tagged, cleanup
 7 AI over seeded runs: weights per band, A only within reach, cooldowns, no immediate repeat, the far rule, the F
   schedule (first >= 240 t after E70, then >= 900 t and >= 3 others)
 8 pause / reload per phase (intro, pattern, E70 before / after its brand, T, stun), the schedule clock frozen in a pause
 9 cleanup leaves no rlk_kn_* entity and no kn score; every test id runs
10 per-tick command cost of a fight tick (vs Apep ~ 830)
"""
import math
import random
import re
import sys
from pathlib import Path

SCR = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
sys.path.insert(0, str(SCR / 'ar/s3/lib'))
import knsim as T  # noqa: E402
from mcsim import Ctx  # noqa: E402

check, summary = T.check, T.summary
ARGS = sys.argv[1:]
DP = Path(ARGS[0]) if ARGS and '/' in ARGS[0] else T.DEFAULT_DP
SECTIONS = [a for a in ARGS if '/' not in a]
SND = set((SCR / 'rd/tests/sound_ids.txt').read_text().split())
ROOT = 'rlk:boss/arlecchino/'


def bctx(s):
    b = T.body(s)
    return Ctx(b, tuple(b.pos), tuple(b.rot))


def call(s, rel):
    return s.call(ROOT + rel, bctx(s))


def fresh(hp=200000, hold=True):
    s, pl = T.setup(dp=DP, hp=hp)
    T.fight(s)
    if hold:
        T.test_id(s, 99)
    T.run(s, 3, T.heal_player)
    return s


def heal_run(s, n):
    T.run(s, n, T.heal_player)


def tid(s, key):
    return {k: v for v, k in s.api.TEST_IDS.items()}[key]


# ------------------------------------------------------------------------------------------------------------- 1 static
def glyph_ok(st):
    """A line naming a font: a list filter on it (`sub[{extra:[{font:..}]}]`), or a text value whose root is an empty
    unstyled `{text:"",extra:[..]}` with the font only on extra elements (no glyph-font inheritance)."""
    st = re.sub(r'\[\{extra:\[\{font:"[a-z0-9_:/]+"\}\]\}\]', '', st)
    if 'font:' not in st:
        return True
    m = re.search(r' value (\{.*\})$', st)
    if not m:
        return False
    from mcsim import Sim
    v = Sim.snbt(m.group(1))
    if set(v) != {'text', 'extra'} or v['text'] != '':
        return False

    def nofont_root(x):
        return 'font' not in x
    return nofont_root(v)


def static():
    s = fresh()
    api = s.api
    root = Path(s.root) / 'boss/arlecchino'
    files = {p.relative_to(root).with_suffix('').as_posix(): p for p in root.rglob('*.mcfunction')}
    need = api.L.HOOKS + api.L.HELP_HOOKS + api.L.CHAPTER_HOOKS + ['init']
    check('static: the 17 hooks + prep + test/help + init exist', all(h in files for h in need), [h for h in need if h not in files])
    allfn = {f'rlk:{p.relative_to(Path(s.root)).with_suffix("").as_posix()}' for p in Path(s.root).rglob('*.mcfunction')}
    missing, neg, sounds, fonts, texts, tps, macro_bad = [], [], [], [], set(), [], []
    for rel, p in files.items():
        for i, ln in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
            st = ln.strip()
            if not st or st.startswith('#'):
                continue
            if st.startswith('$') != ('$(' in st):
                macro_bad.append(f'{rel}:{i}')
            for m in re.finditer(r'function (rlk:[a-z0-9_./-]+)(\$\()?', st):
                if m.group(2):                                # a macro id: some function must carry that prefix
                    if not any(f.startswith(m.group(1)) for f in allfn):
                        missing.append(f'{rel}:{i} -> {m.group(1)}$(..)')
                elif m.group(1) not in allfn:
                    missing.append(f'{rel}:{i} -> {m.group(1)}')
            if re.search(r'scoreboard players (add|remove) \S+ \S+ -\d', st):
                neg.append(f'{rel}:{i}')
            for m in re.finditer(r'playsound (minecraft:[a-z0-9_.]+)', st):
                if m.group(1) not in SND:
                    sounds.append(m.group(1))
            if 'font:' in st and not glyph_ok(st):
                fonts.append(f'{rel}:{i}')
            for m in re.finditer(r'(?<![A-Za-z_])(?:text|t):"([^"]*)"', st):
                texts.add(m.group(1).strip())
            if re.search(r'(^|run )tp ', st):
                tps.append((rel, st))
    check('static: every function reference resolves', not missing, missing[:5])
    check('static: macro lines carry $(..), others none', not macro_bad, macro_bad[:5])
    check('static: no negative scoreboard add/remove literal', not neg, neg[:5])
    check('static: vanilla sounds only', not sounds, sorted(set(sounds))[:5])
    check('static: no font on any text (no glyph-font inheritance)', not fonts, fonts[:5])
    allowed = ({'', api.NAME, api.SUB, api.TITLE_P1[0], api.TITLE_P1[1], api.TITLE_P2[0], api.TITLE_P2[1],
                f'  {api.BADGE}', api.BADGE, api.BANNER} | set(api.PATTERN_NAMES.values()) | set(api.LINES.values())
               | set(api.GATE_LINES) | {f'  {n}' for n in api.TEST_HELP_NAMES} | {str(n) for n in api.TEST_HELP_NAMES}
               | set(api.TEST_HELP_NAMES.values()) | {' — ', '—', f'{api.NAME} 시험 번호'}
               | {api.BADGE.lstrip('◆'), '$(t)'})     # the kit: badge name after its glyph; the typed step (fx/hud/e/ln_show)
    # the kit (I1): typed dialog steps (prefixes of a line), the banner's two coloured phrases, the badge glyph (PUA)
    typed = lambda t: any(v.startswith(t) for v in api.LINES.values())  # noqa: E731
    banner = lambda t: api.BANNER.startswith(t) or api.BANNER.endswith(t)  # noqa: E731
    glyph = lambda t: len(t) == 1 and 0xE000 <= ord(t) <= 0xF8FF  # noqa: E731
    odd = sorted(t for t in texts if t not in allowed and not t.startswith('lock {id:') and not t.startswith('/function')
                 and not (t and (typed(t) or banner(t) or glyph(t))))
    check('static: texts are names / titles / pattern names / the badge / dialog / gate / help rows only', not odd, odd)
    # the body's teleports; the kit's cards / followers / demo props, the rig's parts and anchor and the intro's wisp
    # markers move display / marker entities (never the body); Q0's hover spot is a marker placed through mv/ok; the G
    # cross blades step behind mv/ok's block tests on the walk disc (p1.BLADE_OK)
    walk_ok = lambda l: ('if block ~ ~ ~ #rlk:dash_pass if block ~ ~1 ~ #rlk:dash_pass' in l  # noqa: E731
                         and 'tag=rlk_mb_arena,distance=..' in l)
    tp_bad = [t for t in tps if not ('mv/ok' in t[1] or walk_ok(t[1]) or re.search(r'tp @s ~ ~ ~ (~|\$\(yaw\))', t[1])
                                     or 'tp @s ~ ~ ~ ~ 0' in t[1] or t[0] in ('core/dash/step', 'core/clamp', 'core/ground')
                                     or t[0].startswith(('fx/', 'rig/follow/', 'rig/anchor/'))
                                     or (t[0] == 'seq/intro/tick' and 'tp @e[type=marker,tag=rlk_kn_wisp_' in t[1])
                                     or (t[0] == 'p/q0/f/spot' and 'positioned as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] positioned ~ ~10 ~ run tp @s' in t[1]))]
    check('static: every tp is rotation-only, a probe / clamp step, behind mv/ok or its block tests', not tp_bad, tp_bad[:3])
    ground = files['core/ground'].read_text()
    check('static: core/ground puts her on the floor below only through mv/ok, else the arena centre',
          'if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~' in ground and 'positioned as @e[type=minecraft:marker,tag=rlk_mb_arena' in ground)
    # the user's changes: no ranged immunity, no Pyro resistance
    check('no Pyro resistance: registry res {"*": 10} (every element 10 %)', api.BOSS['res'] == {'*': 10}, api.BOSS['res'])
    inc = [ln for ln in files['incoming'].read_text().splitlines() if ln.strip() and not ln.startswith('#')]
    check('no ranged immunity: the incoming hook has no commands (no damage filter of any kind)', not inc, inc)
    src = '\n'.join(p.read_text() for rel, p in files.items() if not rel.startswith(('rig_stub/',)))
    filt = [w for w in ('bowHit', 'aKind', 'rlk_arr', 'jdmg', 'evade', 'dodge_pj', 'rlk_mb_inv') if w in src]
    inv_lines = [ln for rel, p in files.items() for ln in p.read_text().splitlines()
                 if 'tag @s add rlk_mb_inv' in ln and rel not in ('core/e70_go', 'core/tr/start', 'core/replay/start')]
    check('no ranged immunity: no projectile filter / evasion; rlk_mb_inv only in E70 (before its brand), T and the replay',
          not [w for w in filt if w != 'rlk_mb_inv'] and not inv_lines, (filt, inv_lines))
    return files


# ------------------------------------------------------------------------------------------------------------- 2 phases
def phases():
    s, pl = T.setup(dp=DP, hp=40000)
    api = s.api
    T.fight(s, skip_intro=False)
    log = {'music': [], 'title': [], 'ring': [], 'repool': [], 'cine': []}
    o_call = s.call

    def spy(fid, ctx, macro=None):
        if fid == 'rlk:mboss/music/set':
            log['music'].append((s.t, T.kn(s, '#sq'), dict(macro or {})))
        elif fid == 'rlk:mboss/push/ring':
            log['ring'].append((s.t, T.kn(s, '#sq')))
        elif fid == 'rlk:mboss/title':
            log['title'].append((s.t, T.kn(s, '#sq'), dict(macro or {})))
        elif fid == 'rlk:mboss/repool':
            log['repool'].append((s.t, T.kn(s, '#sq'), dict(macro or {})))
        elif fid in ('rlk:mboss/cine/start', 'rlk:mboss/cine/end'):
            log['cine'].append((s.t, fid[-5:]))
        return o_call(fid, ctx, macro)
    s.call = spy
    T.until(s, lambda s: T.mb(s, '#mbSt') == 1, 400, T.heal_player)
    b = T.body(s)
    tot = T.mb(s, '#mbTot')
    mh = T.esc(s, b, 'mhpM')
    check('phases: the intro ends at its clip end (fight state, P1a, vulnerable)',
          T.kn(s, '#ph') == api.PH['p1a'] and 150 <= s.t <= 156 and 'rlk_mb_inv' not in b.tags, s.t)
    check('phases: the P1 pool is 64 % of the total', mh == tot * 64 // 100, (mh, tot))
    check('phases: the P1 title at intro 80, music 1 at 136, the push ring at 140',
          any(t[1] == 80 and t[2].get('title') == api.TITLE_P1[0] for t in log['title'])
          and any(m[1] == 136 and m[2].get('ph') == 1 for m in log['music']) and any(r[1] == 140 for r in log['ring']), log)
    fl70 = mh // 100 * 70
    check('phases: P1a floor = 70 % of the P1 pool', T.mb(s, '#mbFloor') == fl70, (T.mb(s, '#mbFloor'), fl70))
    seq = [T.kn(s, '#ph')]

    def track(s):
        T.heal_player(s)
        ph = T.kn(s, '#ph')
        if ph != seq[-1]:
            seq.append(ph)
    T.until(s, lambda s: 1 <= (T.kn(s, '#pat') or 0) <= 13, 400, track)
    patn = T.kn(s, '#pat')
    T.hit_body(s, dmg=mh, el=0)
    T.world(s)
    check('phases: a huge hit stops at the 70 % floor, E70 is reserved', T.hp(s) == fl70 and T.kn(s, '#fl') == 1, (T.hp(s), fl70))
    check('phases: E70 waits for the next decision (the pattern goes on)', T.kn(s, '#pat') == patn and T.kn(s, '#ph') == 1)
    T.until(s, lambda s: T.kn(s, '#ph') == api.PH['e70'], 400, track)
    b = T.body(s)
    bol0 = T.pbol(s)
    check('phases: E70 starts at the next decision, invulnerable', 'rlk_mb_inv' in b.tags and T.kn(s, '#pat') == 20)
    T.until(s, lambda s: (T.kn(s, '#pt') or 0) >= 70, 120, track)
    T.world(s)
    b = T.body(s)
    pmax = T.pmax(s)
    check('phases: E70 brand (70): hittable again, floor -> 1, the forced bond (+18 %), 3 heal orbs',
          'rlk_mb_inv' not in b.tags and T.mb(s, '#mbFloor') == 1 and T.pbol(s) - bol0 == pmax * 18 // 100
          and len(T.ents(s, 'rlk_kn_orb')) == 3, (T.pbol(s), bol0, pmax, len(T.ents(s, 'rlk_kn_orb'))))
    T.until(s, lambda s: T.kn(s, '#ph') == api.PH['p1b'], 120, track)
    check('phases: P1b after E70', T.kn(s, '#ph') == api.PH['p1b'] and T.kn(s, '#e70') == 2)
    T.until(s, lambda s: 1 <= (T.kn(s, '#pat') or 0) <= 13, 600, track)
    T.hit_body(s, dmg=mh * 2, el=0)
    T.world(s)
    check('phases: a P1b hit stops at 1 HP, T is reserved (not E70 again)', T.hp(s) == 1 and T.kn(s, '#fl') == 2, (T.hp(s), T.kn(s, '#fl')))
    T.until(s, lambda s: T.kn(s, '#ph') == api.PH['t'], 400, track)
    b = T.body(s)
    check('phases: T at the next decision: invulnerable, cine on', 'rlk_mb_inv' in b.tags and T.mb(s, '#mbCine') == 1)
    T.until(s, lambda s: T.kn(s, '#ph') == api.PH['p2'], 300, track)
    b = T.body(s)
    mh2 = T.esc(s, b, 'mhpM')
    check('phases: repool 36 at T 140, music 2, the P2 title', any(r[1] == 140 and r[2].get('pct') == 36 for r in log['repool'])
          and any(m[2].get('ph') == 2 and m[1] == 140 for m in log['music'])
          and any(t[2].get('title') == api.TITLE_P2[0] for t in log['title']) and mh2 == tot * 36 // 100, (log['repool'], mh2))
    check('phases: P2 after T: vulnerable, cine off, no floor', 'rlk_mb_inv' not in b.tags and T.mb(s, '#mbCine') == 0
          and T.mb(s, '#mbFloor') == 0)
    T.run(s, 30, track)
    T.hit_body(s, dmg=mh2 * 3, el=0)
    T.world(s)
    seq.append(T.kn(s, '#ph')) if T.kn(s, '#ph') != seq[-1] else None
    check('phases: the order intro P1a E70 P1b T P2 death', seq == [1, 2, 3, 4, 5, 6], seq)
    T.until(s, lambda s: T.body(s) is None, 200)
    check('phases: the death sequence runs until the framework removes the body', T.body(s) is None)
    s.call = o_call


# ------------------------------------------------------------------------------------------------------------- 3 bond
def bond():
    api = fresh().api
    s = fresh()
    pmax = T.pmax(s)
    b = T.body(s)
    mh = T.esc(s, b, 'mhpM')
    s.setsc(('e', b.id), 'mhpC', mh // 2)
    # a landed bol hit (FN-1, live since I1: the framework raises #mbHitBol = the option value)
    s.setsc('#mbHitEv', 'mb', 1)
    s.setsc('#mbHitBol', 'mb', api.BOL_HIT)
    heal_run(s, 1)
    check('bond: a landed bol hit adds 6 % max HP, #bonded 1, #given = the amount', T.pbol(s) == pmax * 6 // 100
          and T.kn(s, '#bonded') == 1 and T.kn(s, '#given') == pmax * 6 // 100, (T.pbol(s), T.kn(s, '#given')))
    check('bond: she heals 1 % of the pool per landed bol hit', T.hp(s) == mh // 2 + mh * 10 // 1000, (T.hp(s), mh))
    check(f'bond: #mbBolRe {api.BOL_REHIT_PCT} while her bond is on the player', T.mb(s, '#mbBolRe') == api.BOL_REHIT_PCT)
    # DoT every 50 t, non-lethal
    pl = s.player()
    s.setsc(('e', pl.id), 'curHealth', pmax)
    T.run(s, 50)
    lost = pmax - s.sc(('e', pl.id), 'curHealth')
    check('bond: the DoT takes 1 % max HP every 50 t while bonded', lost == max(1, pmax * 10 // 1000), (lost, pmax))
    s.setsc(('e', pl.id), 'curHealth', 1)
    T.run(s, 101)
    check('bond: the DoT never kills (1 HP stays 1)', s.sc(('e', pl.id), 'curHealth') == 1 and s.sc(('e', pl.id), 'dead') in (0, None))
    # a real BoL hit from a pattern (G cross1 on a standing player) and a plain string that never bonds
    s2 = fresh()
    T.test_id(s2, 99)
    pl2 = s2.player()
    b2 = T.body(s2)
    T.place_player(s2, b2.pos[0], b2.pos[2] + 3)
    T.test_id(s2, tid(s2, 'a2'))
    T.until(s2, lambda s: (T.kn(s, '#pat') or 0) == 0, 200, T.heal_player)
    check('bond: a plain string (A) lands but never bonds', len(s2.phits) >= 2 and T.pbol(s2) == 0 and T.kn(s2, '#bonded') == 0,
          (len(s2.phits), T.pbol(s2)))
    T.test_id(s2, tid(s2, 'g1'))
    T.until(s2, lambda s: (T.kn(s, '#pt') or 0) >= 36, 100, T.heal_player)
    check('bond: G cross1 on a standing player bonds 6 % (pattern BoL hit)', T.pbol(s2) == T.pmax(s2) * 6 // 100
          and T.kn(s2, '#bonded') == 1, (T.pbol(s2), [h[0] for h in s2.phits]))
    check(f'bond: x{api.BOL_REHIT_PCT / 100} only while bonded: #mbBolRe {api.BOL_REHIT_PCT} now', T.mb(s2, '#mbBolRe') == api.BOL_REHIT_PCT)
    # clear -> shock (the existing player/heal clears the bond first)
    T.test_id(s2, 22)
    T.run(s2, 1, T.heal_player)
    sub = str(s2.storage.get('rlk:mboss', {}).get('sub'))
    check('bond: a heal clears her bond -> 선혈의 충격 armed, #bonded / #given 0, badge on the bar',
          T.pbol(s2) == 0 and T.kn(s2, '#shock') == 1 and T.kn(s2, '#bonded') == 0 and T.kn(s2, '#given') == 0
          and api.BADGE.lstrip('◆') in sub and "'font': 'rlk:mboss_kn'" in sub,      # the kit draws ◆ as its glyph
          (T.pbol(s2), T.kn(s2, '#shock'), sub))
    check('bond: #mbBolRe back to 100 after the clear', T.mb(s2, '#mbBolRe') == 100)
    # a Clorinde / Arlecchino player's own bond: no DoT, x1, kept by cleanup
    s3 = fresh()
    pl3 = s3.player()
    pmax3 = T.pmax(s3)
    s3.setsc(('e', pl3.id), 'bol', 30)
    s3.setsc(('e', pl3.id), 'curHealth', pmax3)
    T.run(s3, 120)
    check('bond: the player\'s own bond (not hers): no DoT, #mbBolRe 100', s3.sc(('e', pl3.id), 'curHealth') == pmax3
          and T.mb(s3, '#mbBolRe') == 100, (s3.sc(('e', pl3.id), 'curHealth'), pmax3))
    T.test_id(s3, 21)
    check('bond: the forced bond adds 18 % on top of the own bond', T.pbol(s3) == 30 + pmax3 * 18 // 100, T.pbol(s3))
    call(s3, 'cleanup')
    check('bond: cleanup takes back only her part (the own 30 stays)', T.pbol(s3) == 30, T.pbol(s3))
    # forced-bond skip states
    for obj, v in (('dead', 1), ('rnDie', 1), ('pkMode', 1), ('vMap', 1)):
        s4 = fresh()
        pl4 = s4.player()
        s4.setsc(('e', pl4.id), obj, v)
        n0 = len(T.ents(s4, 'rlk_kn_orb'))
        s4.call(ROOT + 'bond/force', T.C0)
        check(f'bond: no forced bond while {obj} {v} (no bond, no orbs)', T.pbol(s4) == 0 and len(T.ents(s4, 'rlk_kn_orb')) == n0)


# ------------------------------------------------------------------------------------------------------------- 4 predicate
KIND_EXPECT = {'melee_na': 1, 'melee_extra': 1, 'bow_na': 1, 'bow_aim': 0, 'skill': 0, 'skill_icd': 0, 'reaction': 0, 'item': 0}


def predicate():
    s = fresh()
    api = s.api
    for kind, want in KIND_EXPECT.items():
        s.setsc('#shock', 'kn', 1)
        s.setsc('#shk_hit', 'kn', 0)
        T.hit_body(s, dmg=5, el=0, kind=kind)
        check(f'predicate: a {kind} hit {"arms" if want else "does not arm"} the shock resolve', (T.kn(s, '#shk_hit') or 0) == want,
              T.kn(s, '#shk_hit'))
    s.setsc('#shk_hit', 'kn', 0)
    s.setsc('#mbTrue', 'mb', 5)
    s.setsc('#mbTrueEl', 'mb', 1)
    call(s, 'test/shock')
    s.setsc('#shk_hit', 'kn', 0)
    s.call('rlk:mboss/true_hit', bctx(s))
    check('predicate: true damage never counts', (T.kn(s, '#shk_hit') or 0) == 0)
    s.setsc('#shock', 'kn', 0)
    T.hit_body(s, dmg=5, el=0, kind='melee_na')
    check('predicate: without an armed shock nothing is recorded', (T.kn(s, '#shk_hit') or 0) == 0)
    # the engine files behind the table (F:char/*, F:combat/*): which attack kinds carry which flags
    F = Path(s.root)

    def has(rel, *pats):
        t = (F / f'{rel}.mcfunction').read_text()
        return all(p in t for p in pats)
    rows = [
        ('melee normal (all melee chars)', has('combat/find_immediate', 'scoreboard players set #icd tmp 1', 'set #skillDmg tmp 0', 'set #tfm tmp 0')),
        ('melee extra hits (clorinde / arlecchino / navia / nefer)', has('char/melee/extra', 'set #icd tmp 1', 'set #skillDmg tmp 0')),
        ('skirk 5-hit extra', has('char/skirk/na_extra', 'set #icd tmp 1', 'set #skillDmg tmp 0')),
        ('bow normal shot aIcd 1 (yoimiya)', has('char/bow/na_shot', 'set #aIcd tmp 1')),
        ('bow aimed / charged shot aIcd 0', has('char/bow/release', 'set #aIcd tmp 0')),
        ('clorinde pistol normal shot', has('char/clorinde/shoot', 'clear_atkflags', 'set #icd tmp 1')),
        ('ronova orbs 1-3 pIcd 1, the 4th 0', has('char/ronova/na', 'set #pIcd tmp 1', 'matches 3.. run scoreboard players set #pIcd tmp 0')),
        ('nefer phantasm self hits', has('char/nefer/ph_self', 'set #icd tmp 1')),
        ('every skill / burst (char/dmg_calc #skillDmg 1)', has('char/dmg_calc', 'set #skillDmg tmp 1')),
        ('item procs #sub itv 1 around the hit (kirion)', has('items/proc/kirion_slash', 'set #sub itv 1')),
    ]
    check('predicate: the engine flags behind the per-character table', all(r[1] for r in rows), [r[0] for r in rows if not r[1]])


# ------------------------------------------------------------------------------------------------------------- 5 shock
def shock():
    s = fresh()
    api = s.api
    b = T.body(s)
    T.place_player(s, b.pos[0], b.pos[2] + 6)
    mh = T.esc(s, b, 'mhpM')
    T.test_id(s, tid(s, 'f1'))
    T.until(s, lambda s: (T.kn(s, '#pt') or 0) >= 40, 60, T.heal_player)
    b = T.body(s)
    check('shock: F window open at 22..159 (body tag rlk_kn_win)', T.kn(s, '#win') == 1 and api.TAGS['win'] in b.tags)
    T.test_id(s, 23)
    hp0 = T.hp(s)
    T.hit_body(s, dmg=10, el=0, kind='melee_na')
    hp1 = T.hp(s)
    T.run(s, 1, T.heal_player)
    hp2 = T.hp(s)
    clk = T.kn(s, '#clk')
    check('shock: a normal hit inside the window breaks F: cancelled, stun, true 15 % of the pool',
          T.kn(s, '#pat') == 50 and T.kn(s, '#stun') == 1 and hp1 - hp2 == mh * 150 // 1000 and not T.ents(s, 'rlk_kn_p_f1')
          and T.kn(s, '#win') == 0 and T.kn(s, '#shock') == 0, (T.kn(s, '#pat'), hp0, hp1, hp2, mh))
    check('shock: the stun = brk 20 t + 140 t', T.kn(s, '#stun_t') == api.STUN_T + 20 - 0 or T.kn(s, '#stun_t') == api.STUN_T + 19,
          T.kn(s, '#stun_t'))
    T.until(s, lambda s: (T.kn(s, '#stun') or 0) == 0, 200, T.heal_player)
    clk_end = T.kn(s, '#clk')
    check('shock: the stun ends after 160 t, the F schedule restarts from its end (+900)',
          159 <= clk_end - clk <= 162 and T.kn(s, '#sch_f') == clk_end + 900 - 0 and T.kn(s, '#pat') == 0,
          (clk_end - clk, T.kn(s, '#sch_f'), clk_end))
    # outside a window: the 2 % burst, the pattern goes on
    s = fresh()
    b = T.body(s)
    mh = T.esc(s, b, 'mhpM')
    T.place_player(s, b.pos[0], b.pos[2] + 3)
    T.test_id(s, tid(s, 'a4'))
    T.run(s, 5, T.heal_player)
    T.test_id(s, 23)
    T.hit_body(s, dmg=10, el=0, kind='melee_na')
    h1 = T.hp(s)
    T.run(s, 1, T.heal_player)
    check('shock: outside a window the crimson burst (true 2 % of the pool), the pattern goes on',
          h1 - T.hp(s) == mh * 20 // 1000 and T.kn(s, '#pat') == tid(s, 'a4') and T.kn(s, '#shock') == 0, (h1 - T.hp(s), mh))
    # the clamp: never skips E70 / T
    s = fresh()
    b = T.body(s)
    fl = T.mb(s, '#mbFloor')
    s.setsc(('e', b.id), 'mhpC', fl + 50)
    call(s, 'test/brk')
    check('shock: the break clamps above the P1a floor (HP = floor + 1, E70 not skipped)', T.hp(s) == fl + 1 and T.kn(s, '#ph') == 1,
          (T.hp(s), fl))
    T.test_id(s, 30)
    b = T.body(s)
    s.setsc(('e', b.id), 'mhpC', 30)
    call(s, 'test/brk')
    check('shock: the break clamps above the P1b floor 1 (HP 2, T not skipped)', T.hp(s) == 2 and T.kn(s, '#ph') == 3, T.hp(s))
    T.test_id(s, 31)
    b = T.body(s)
    mh2 = T.esc(s, b, 'mhpM')
    s.setsc(('e', b.id), 'mhpC', mh2)
    call(s, 'test/brk')
    check('shock: a P2 break takes 12.5 % of the P2 pool', mh2 - T.hp(s) == mh2 * 125 // 1000, (mh2, T.hp(s)))
    # the stun under-bar
    T.run(s, 2, T.heal_player)
    check('shock: the stun under-bar counts down (#buSub)', (T.kn(s, '#stun') == 1) and s.sc('#buSub', 'bu') == T.kn(s, '#stun_t'),
          (s.sc('#buSub', 'bu'), T.kn(s, '#stun_t')))


# ------------------------------------------------------------------------------------------------------------- 6 orbs
def orbs():
    s = fresh()
    api = s.api
    T.test_id(s, 28)
    o = T.ents(s, 'rlk_kn_orb')
    d = [math.hypot(e.pos[0] - api.CX, e.pos[2] - api.CZ) for e in o]
    ang = sorted(math.degrees(math.atan2(e.pos[2] - api.CZ, e.pos[0] - api.CX)) % 360 for e in o)
    gaps = [round((ang[(i + 1) % 3] - ang[i]) % 360) for i in range(3)] if len(ang) == 3 else []
    check('orbs: 3 heal orbs 6-14 b from the centre, 120 deg apart, tagged rlk_kn_orb + rlk_mb_aux',
          len(o) == 3 and all(5.9 <= x <= 14.1 for x in d) and all(abs(g - 120) <= 1 for g in gaps)
          and all('rlk_mb_aux' in e.tags and 'rlk_healorb' in e.tags for e in o), (d, gaps))
    T.test_id(s, 21)
    check('orbs: a second forced bond keeps <= 3 alive (the older ones go)', len(T.ents(s, 'rlk_kn_orb')) == 3)
    call(s, 'cleanup')
    check('orbs: cleanup removes them', not T.ents(s, 'rlk_kn_orb'))


# ------------------------------------------------------------------------------------------------------------- 7 AI
def ai_runs():
    api = fresh().api
    gid = {'a2': 'A', 'a4': 'A', 'a5': 'A', 'b1': 'B', 'b2': 'B', 'c1': 'C', 'c2': 'C', 'd1': 'D', 'd2': 'D', 'e1': 'E',
           'f1': 'F', 'g1': 'G', 'h1': 'H', 'e70': 'E70'}

    def spy_run(s, n, mover):
        starts = []
        o_call = s.call

        def spy(fid, ctx, macro=None):
            if fid.startswith(ROOT + 'core/start/'):
                k = fid.rsplit('/', 1)[1]
                b = T.body(s)
                pl = s.player()
                starts.append((s.t, T.kn(s, '#clk'), k, math.hypot(b.pos[0] - pl.pos[0], b.pos[2] - pl.pos[2]), T.kn(s, '#ph')))
            return o_call(fid, ctx, macro)
        s.call = spy
        T.run(s, n, mover)
        s.call = o_call
        return starts
    # (a) P1a, a player standing 3 b away
    s, pl = T.setup(dp=DP, hp=4000000, seed=7)
    T.fight(s)
    T.run(s, 30, T.heal_player)

    def stay(d):
        def m(s):
            T.heal_player(s)
            if s.t % 20 == 0:
                b = T.body(s)
                p = s.player()
                dx, dz = p.pos[0] - b.pos[0], p.pos[2] - b.pos[2]
                r = math.hypot(dx, dz) or 1
                if abs(r - d) > 1.0:
                    x, z = b.pos[0] + dx / r * d, b.pos[2] + dz / r * d
                    if math.hypot(x - api.CX, z - api.CZ) < 22:
                        T.place_player(s, x, z)
        return m
    st = spy_run(s, 4000, stay(3.0))
    groups = [gid[k] for _, _, k, _, _ in st]
    cnt = {g: groups.count(g) for g in set(groups)}
    check('AI: P1a near (3 b): A dominates, D never (near weight 0)', cnt.get('A', 0) > max(cnt.get('B', 0), cnt.get('C', 0))
          and cnt.get('D', 0) <= 1, cnt)
    rep = [(st[i][2], st[i + 1][2]) for i in range(len(st) - 1) if gid[st[i][2]] == gid[st[i + 1][2]]]
    check('AI: no immediate repeat of a group', not rep, rep[:3])
    far_a = [x for x in st if gid[x[2]] == 'A' and x[3] > 7.3]
    check('AI: A starts only within reach (<= 7 b; she walks in from 4.5 b)', not far_a, far_a[:3])
    # (b) P1b, a wandering player: cooldowns, the F schedule
    s, pl = T.setup(dp=DP, hp=4000000, seed=11)
    T.fight(s)
    T.test_id(s, 30)
    rng = random.Random(5)

    def wander(s):
        T.heal_player(s)
        if s.t % 60 == 0:
            a = rng.uniform(0, 2 * math.pi)
            r = rng.uniform(2, 18)
            T.place_player(s, api.CX + math.cos(a) * r, api.CZ + math.sin(a) * r)
    clk0 = T.kn(s, '#clk')
    st = spy_run(s, 9000, wander)
    bad_cd = []
    last = {}
    for t, clk, k, d, ph in st:
        g = gid[k]
        if g in last and g in api.COOLDOWN and clk - last[g] < api.COOLDOWN[g]:
            bad_cd.append((k, clk - last[g], api.COOLDOWN[g]))
        last[g] = clk
    check('AI: cooldowns hold over a seeded 9000 t P1b run', not bad_cd, bad_cd[:4])
    groups = [gid[k] for _, _, k, _, _ in st]
    keys = {k for _, _, k, _, _ in st}
    check('AI: the P1b kit is used (E, F, G, H picked; the <= 70 % variants a4 / a5 / b2 / c2 / d2 only)',
          all(g in groups for g in 'EFGH') and not keys & {'a2', 'b1', 'c1', 'd1'}, {g: groups.count(g) for g in set(groups)})
    fs = [(clk, i) for i, (t, clk, k, d, ph) in enumerate(st) if k == 'f1']
    first_ok = fs and fs[0][0] - clk0 >= api.SCHEDULE['F']['first_after'][1]
    gaps = [(fs[i + 1][0] - fs[i][0], fs[i + 1][1] - fs[i][1] - 1) for i in range(len(fs) - 1)]
    check('AI: F first >= 240 t after E70 / P1b, then >= 900 t (+ its 232 t) and >= 3 others between',
          bool(first_ok) and all(g >= 900 and n >= 3 for g, n in gaps), (fs[:1], clk0, gaps))
    # (c) the far rule: D 60 % / C
    picks = []
    for seed in range(8):
        s, pl = T.setup(dp=DP, hp=4000000, seed=100 + seed)
        T.fight(s)
        T.run(s, 2, T.heal_player)

        def farp(s):
            T.heal_player(s)
            b = T.body(s)
            if math.hypot(s.player().pos[0] - b.pos[0], s.player().pos[2] - b.pos[2]) < 15:
                ang = math.atan2(b.pos[2] - api.CZ, b.pos[0] - api.CX) + math.pi
                T.place_player(s, api.CX + math.cos(ang) * 20, api.CZ + math.sin(ang) * 20)
        st = spy_run(s, 300, farp)
        picks += [gid[k] for _, _, k, d, _ in st]
    cnt = {g: picks.count(g) for g in set(picks)}
    check('AI: a far player (> 14 b) gets the gap closers D / C (B only by weight)', cnt.get('D', 0) + cnt.get('C', 0) >= len(picks) * 0.6
          and cnt.get('A', 0) == 0, cnt)


# ------------------------------------------------------------------------------------------------------------- 8 pause / reload
def reload_(s):
    """/reload as the game does it for the fight: mboss/init kills the aux entities (rig parts, hazards, markers, orbs),
    then mboss/reload for the surviving body."""
    for e in s.ents:
        if e.alive and 'rlk_mb_aux' in e.tags and 'rlk_mb_body' not in e.tags:
            e.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.call('rlk:mboss/reload', bctx(s))


def pause_reload():
    api = fresh().api
    # pause freezes the module clock
    s = fresh(hold=False)
    pl = s.player()
    c0 = T.kn(s, '#clk')
    s.setsc(('e', pl.id), 'dead', 1)
    T.run(s, 40)
    c1 = T.kn(s, '#clk')
    s.setsc(('e', pl.id), 'dead', 0)
    heal_run(s, 5)
    check('pause: the module clock (cooldowns / schedules) does not run while paused', c1 == c0 and T.kn(s, '#clk') > c1, (c0, c1))
    # intro
    s, pl = T.setup(dp=DP, hp=200000)
    T.fight(s, skip_intro=False)
    T.until(s, lambda s: (T.kn(s, '#sq') or 0) >= 50, 100, T.heal_player)
    reload_(s)
    heal_run(s, 2)
    cur = s.storage['rlk:mboss']['cur']
    check('reload: in the intro -> the end of the intro (fight, P1a, the P1 title)', T.mb(s, '#mbSt') == 1 and T.kn(s, '#ph') == 1
          and cur['title']['text'] == api.TITLE_P1[0], (T.mb(s, '#mbSt'), T.kn(s, '#ph'), cur.get('title')))
    # a pattern
    s = fresh()
    T.test_id(s, tid(s, 'g1'))
    heal_run(s, 20)
    reload_(s)
    heal_run(s, 1)
    check('reload: in a pattern -> cancelled + recovery (no marker left)', (T.kn(s, '#pat') or 0) == 0 and (T.kn(s, '#rec') or 0) > 0
          and not T.ents(s, 'rlk_kn_p'))
    # E70 before / after its brand
    for at, want_ph, label in ((30, 1, 'before its brand -> reserved again (P1a)'), (80, 3, 'after its brand -> done (P1b)')):
        s = fresh()
        T.test_id(s, 20)
        T.until(s, lambda s: (T.kn(s, '#pt') or 0) >= at, 120, T.heal_player)
        reload_(s)
        heal_run(s, 1)
        b = T.body(s)
        check(f'reload: E70 {label}', T.kn(s, '#ph') == want_ph and 'rlk_mb_inv' not in b.tags
              and (T.kn(s, '#fl') == (1 if at < 70 else 0)), (T.kn(s, '#ph'), T.kn(s, '#fl')))
    # T
    s = fresh()
    tot = T.mb(s, '#mbTot')
    T.test_id(s, 26)
    heal_run(s, 60)
    reload_(s)
    heal_run(s, 2)
    b = T.body(s)
    check('reload: in T -> finished (P2, the P2 pool, vulnerable, cine off)', T.kn(s, '#ph') == 5 and T.esc(s, b, 'mhpM') == tot * 36 // 100
          and 'rlk_mb_inv' not in b.tags and T.mb(s, '#mbCine') == 0, (T.kn(s, '#ph'), T.esc(s, b, 'mhpM')))
    # stun
    s = fresh()
    T.test_id(s, 29)
    heal_run(s, 60)
    left = T.kn(s, '#stun_t')
    reload_(s)
    heal_run(s, 1)
    check('reload: in a stun -> the rest of it', T.kn(s, '#stun') == 1 and T.kn(s, '#stun_t') == left - 1 and T.kn(s, '#pat') == 50,
          (T.kn(s, '#stun_t'), left))


# ------------------------------------------------------------------------------------------------------------- 9 cleanup / test ids
def cleanup_ids():
    api = fresh().api
    s = fresh()
    pl = s.player()
    s.setsc(('e', pl.id), 'bol', 25)
    T.test_id(s, 21)
    T.test_id(s, 23)
    T.test_id(s, tid(s, 'h1'))
    heal_run(s, 25)
    call(s, 'cleanup')
    left = [sorted(e.tags) for e in s.ents if e.alive and any(t.startswith('rlk_kn_') for t in e.tags)]
    kn_scores = [k for k in s.scores if k[1] == 'kn']
    check('cleanup: no rlk_kn_* entity, no kn score, the shock reset, only her bond removed',
          not left and not kn_scores and T.pbol(s) == 25 and T.mb(s, '#mbBolRe') == 100, (left[:3], kn_scores[:3], T.pbol(s)))
    errs = []
    for n in sorted(api.TEST_IDS):
        s = fresh()
        try:
            T.test_id(s, n)
            heal_run(s, 30)
        except Exception as e:  # noqa: BLE001
            errs.append((n, repr(e)[:120]))
    check('tests: every test id runs (P2 ids degrade: no S4 pattern -> P2 only)', not errs, errs[:3])
    s = fresh()
    T.test_id(s, 27)
    T.run(s, 5)
    check('tests: 27 (death) kills her through the death sequence', T.kn(s, '#ph') == 6 or T.body(s) is None)


# ------------------------------------------------------------------------------------------------------------- 10 cost
def cost():
    s, pl = T.setup(dp=DP, hp=4000000, seed=3)
    api = s.api
    T.fight(s)
    rng = random.Random(3)

    def mover(q):
        T.heal_player(q)
        if q.t % 50 == 0:
            T.place_player(q, api.CX + rng.uniform(-8, 8), api.CZ + rng.uniform(-8, 8))
    n0 = len(s.cmd_hist)
    T.run(s, 1200, mover)
    h = s.cmd_hist[n0:]
    avg = sum(h) / len(h)
    T.test_id(s, 30)
    n1 = len(s.cmd_hist)
    T.run(s, 1200, mover)
    h2 = s.cmd_hist[n1:]
    avg2 = sum(h2) / len(h2)
    print(f'     cost: P1a {avg:.1f} avg / {max(h)} max, P1b {avg2:.1f} avg / {max(h2)} max commands per world tick')
    check('cost: a fight tick averages below Apep (~830 commands)', avg < 830 and avg2 < 830, (avg, avg2))


SECS = {'static': static, 'phases': phases, 'bond': bond, 'predicate': predicate, 'shock': shock, 'orbs': orbs,
        'ai': ai_runs, 'reload': pause_reload, 'cleanup': cleanup_ids, 'cost': cost}
for name, f in SECS.items():
    if not SECTIONS or name in SECTIONS:
        f()
summary('test_arlecchino')
