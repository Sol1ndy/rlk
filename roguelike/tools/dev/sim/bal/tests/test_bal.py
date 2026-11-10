#!/usr/bin/env python3
"""test_bal.py — the balance gauge (균형치) and groggy layer rlk:bal/** (combat overhaul lane B).

    python3 test_bal.py [<roguelike dir>]        (default: the tree this file sits in; run from a copy, sim README 1)

Unit level on the real datapack functions (lib/balsim.py: everything outside the allowlist is a logged stub):
  G  generator: tools/build_balance.py twice into a scratch tree = the committed bal/** byte for byte
  H  the hook lines in the shared files (place and order)
  T  tiers / exclusions / the pip row (spawn, left end, re-setup, no duplicate)
  P  bal/hit: pips, clamp, flash, return values, refusal while groggy; regen delay / step / stop
  S  sources: burst window (2 pips, once per 40 t), strong reactions (table, 30 t window), both on one hit
  D  groggy damage bonus through the real combat/apply_mods (per tier)
  C  cm family: entry (cancel, NoAI, held, cooldowns), no attack start while groggy (real per-mob ticks), exit
  V  vanilla family + freeze in both orders (NoAI restored exactly)
  B  bosses: registry bosses without the "bal" flag get no gauge; Raiden: may / ok / pending, stun rdSgStun 4,
     100 t, bal_off ends it; the fight-tick order (pause = no clock)
  K  cleanup: death (row orphan killed by mob/hb_cleanup), uninstall, /reload (bal/load keeps state, catch-up init)
  $  per-tick cost (idle mob, regen, groggy)
"""
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
from balsim import BalSim, ck, summary  # noqa: E402

DP = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parents[4]
FN = DP / 'data/rlk/function'
R = []
PIPS = {1: 4, 2: 7, 3: 12}
GRG = {1: 60, 2: 80, 3: 100}
AMP = {1: 150, 2: 140, 3: 130}
RD = {1: 200, 2: 240, 3: 300}
RS = {1: 60, 2: 80, 3: 100}


def lines(rel):
    return [l for l in (FN / (rel + '.mcfunction')).read_text(encoding='utf-8').split('\n')]


def sim(**kw):
    s = BalSim(DP, **kw)
    s.run('bal/load')
    return s


def mob(s, tags=('rlk_room', 'rlk_zmob', 'rlk_m_husk'), etype='husk', **scores):
    e = s.spawn(etype, tags=tags, **scores)
    e.tags.add('rlk_mob')
    s.run('bal/init', e)
    return e


def brain(s, m, extra=(), **scores):
    tags = ['rlk_room', 'rlk_zmob', 'rlk_cmb', f'rlk_cm_{m}'] + list(extra)
    base = dict(cmId=7, cmS=0, cmCd=0, cmCd2=0, stunT=-1, frzT=0, mlv=3)
    base.update(scores)
    return mob(s, tags=tags, **base)


def row_text(s, e):
    p = [x for x in s.passengers(e) if 'rlk_hb_bal' in x.tags]
    return p[0].text['extra'][0]['text'] if p and p[0].text else None


def glyphs(t):
    return ''.join({'': 'F', '': 'e', '': 'x', '': 'G', '': 'F', '': 'e', '': 'x',
                    '': 'G'}.get(c, '') for c in t)


# ======================================================================= G generator
def t_gen():
    tmp = HERE / 'tmp/gen'
    shutil.rmtree(tmp, ignore_errors=True)
    (tmp / 'tools').mkdir(parents=True)
    (tmp / 'data/rlk/function').mkdir(parents=True)
    shutil.copy(DP / 'tools/build_balance.py', tmp / 'tools/build_balance.py')
    for k in range(2):
        subprocess.run([sys.executable, '-I', str(tmp / 'tools/build_balance.py')], check=True, capture_output=True)

    def tree(root):
        return {p.relative_to(root).as_posix(): hashlib.sha1(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*.mcfunction'))}
    a, b = tree(tmp / 'data/rlk/function/bal'), tree(FN / 'bal')
    ck(R, 'G1 build_balance.py (two runs) = committed bal/**', a == b, set(a) ^ set(b) or [k for k in a if a[k] != b.get(k)])
    rp = HERE / 'tmp/rp'
    shutil.rmtree(rp, ignore_errors=True)
    rp.mkdir(parents=True)
    subprocess.run([sys.executable, '-I', str(tmp / 'tools/build_balance.py'), '--resourcepack', str(rp)], check=True, capture_output=True)
    import json
    font = json.loads((rp / 'assets/rlk/font/bal.json').read_text(encoding='utf-8'))
    ids = [p.get('file', '') for p in font['providers']]
    ck(R, 'G2 font rlk:bal: 8 bitmap glyphs + space + default reference, lowercase ids',
       len([i for i in ids if i]) == 8 and font['providers'][-1] == {'type': 'reference', 'id': 'minecraft:default'}
       and all(i == i.lower() for i in ids), ids)
    sp = [p for p in font['providers'] if p['type'] == 'space'][0]['advances']
    ck(R, 'G3 the boss row adds no width: back 200, 12 x (5 + 1 + 2), pad to 200', 12 * 8 + sp[chr(0xED21)] == 200
       and sp[chr(0xED20)] == 2 and sp[chr(0xED22)] == -200, sp)
    shutil.rmtree(HERE / 'tmp', ignore_errors=True)


# ======================================================================= H hooks
def t_hooks():
    def has_after(rel, anchor, line):
        L = lines(rel)
        return anchor in L and line in L and L.index(line) > L.index(anchor)

    ck(R, 'H1 mob/setup: bal/init after rlk_mob', has_after('mob/setup', 'tag @s add rlk_mob', 'function rlk:bal/init'))
    ck(R, 'H2 mob/tick: bal/tick (every enemy but Raiden, whose own tick runs it) after the stun clock',
       has_after('mob/tick', 'execute if score @s stunT matches 0 run function rlk:mob/unstun',
                 'execute if score @s balT matches 1.. unless entity @s[tag=rlk_raiden] run function rlk:bal/tick'))
    L = lines('combat/apply_mods')
    hook = 'execute if score @s balMax matches 1.. run function rlk:bal/mods'
    ck(R, 'H3 combat/apply_mods: one line for the groggy bonus and the sources, before the boss incoming hooks (HP floors)',
       hook in L and L.index(hook) < L.index('execute if entity @s[tag=rlk_raiden] run function rlk:boss/raiden/incoming')
       < L.index('execute if entity @s[tag=rlk_mb_body] run function rlk:mboss/d/incoming')
       and not [l for l in lines('combat/apply') if 'bal' in l])
    ck(R, 'H4 bal/mods: groggy -> the bonus only; no source on a killing blow',
       lines('bal/mods')[2] == 'execute if score @s grgT matches 1.. run return run function rlk:bal/amp'
       and 'execute if score #dmg tmp >= @s mhpC run return 0' in lines('bal/mods'))
    ck(R, 'H5 burst stamp: the game time in items/hook/burst_dmg, cleared in char/after_hit; clear_atkflags untouched',
       'execute store result score #burstDmg tmp run time query gametime' in lines('items/hook/burst_dmg')
       and not [l for l in lines('combat/clear_atkflags') if 'burst' in l]
       and lines('char/after_hit')[2] == 'scoreboard players set #burstDmg tmp 0')
    js, jh = lines('char/lumine/jav_spawn'), lines('char/lumine/jav_hit')
    ck(R, 'H6 Lumine javelins: stamp off after the stored damage, on again at the hit',
       js.index('scoreboard players set #burstDmg tmp 0') == js.index('function rlk:items/hook/burst_dmg') + 2
       and jh.index('execute store result score #burstDmg tmp run time query gametime') == jh.index('function rlk:combat/clear_atkflags') + 1)
    ck(R, 'H7 cm/tick: the groggy hold after the freeze cancel, before the mob ticks',
       has_after('cm/tick', 'execute if score @s frzT matches 1.. if score @s cmS matches 1.. run function rlk:cm/cancel',
                 'execute if score @s grgT matches 1.. run function rlk:bal/fam/cm_tick')
       and lines('cm/tick').index('execute if score @s grgT matches 1.. run function rlk:bal/fam/cm_tick')
       < lines('cm/tick').index('execute if score #cmDown tmp matches 1 run function rlk:cm/down'))
    ck(R, 'H8 element/frz_end keeps NoAI while groggy',
       'execute unless entity @s[tag=rlk_noai] unless score @s grgT matches 1.. run data merge entity @s {NoAI:0b}' in lines('element/frz_end'))
    rigs = ['sw', 'ar', 'fm', 'im', 'sh', 'cn', 'kr', 'nj', 'cc', 'ci', 'cs', 'rv', 'pc']
    sw = {'ns': 'c2', 'sl': 'c2', 'ss': 'c2', 'sp': 'c2', 'dr': 'c2', 'fu': 'c3', 'em': 'c3', 'sb': 'c3', 'cw': 'c3'}
    bad = [m for m in rigs if f'execute if score @s grgT matches 1.. run return run function rlk:cm/{m}/rig/frozen' not in lines(f'cm/{m}/rig/tick')]
    bad += [m for m, c in sw.items() if f'execute if score @s grgT matches 1.. run return run function rlk:cm/{c}/rig_frozen' not in lines(f'cm/{m}/rig/tick')]
    ck(R, 'H9 every cm rig tick holds the pose while groggy (22 rigs)', not bad, bad)
    ck(R, 'H10 cm/sb/tick: the brood cycle stops while groggy', 'execute if score @s grgT matches 1.. run return 0' in lines('cm/sb/tick'))
    hb = lines('mob/hb_cleanup')
    ck(R, 'H11 mob/hb_cleanup kills orphan rows', 'kill @e[tag=rlk_hb_bal,tag=!rlk_hb_ok]' in hb and 'tag @e[tag=rlk_hb_bal] remove rlk_hb_ok' in hb)
    ft, dt = lines('mboss/fight_tick'), [l for l in lines('mboss/d/tick') if l and not l.startswith('#')]
    ck(R, 'H12 mboss/fight_tick unchanged; d/tick: every flagged line skips a groggy body, the last line runs d/bal_tick',
       not [l for l in ft if 'bal' in l]
       and all('unless score @s grgT matches 1.. run return run function' in l for l in dt[:-1])
       and dt[-1] == 'execute if score @s grgT matches 1.. run return run function rlk:mboss/d/bal_tick', dt[-2:])
    for rel, bar in (('mboss/bars', 'rlk:mboss_state'), ('boss/raiden/bars', 'rlk:narukami_state')):
        L = lines(rel)
        want = (f'bossbar set {bar} name [{{nbt:"line[]",storage:"rlk:bu",interpret:true,separator:""}},'
                '{nbt:"brow",storage:"rlk:bal",interpret:true}]')
        ck(R, f'H13 {rel}: the boss row is the second component of the bossui line (no command added)', want in L)
    ck(R, 'H14 bossui/draw untouched (no balance option)', not [l for l in lines('bossui/draw') if 'bal' in l or 'Pip' in l])
    rt = lines('boss/raiden/tick')
    ck(R, 'H15 boss/raiden/tick: the bal clock after the death check (world pause skips the tick)',
       rt.index('execute if score @s balT matches 1.. run function rlk:bal/boss/tick') == rt.index(
           'execute if score @s rdDeath matches 1 run return run function rlk:boss/raiden/death/tick') + 2)
    ck(R, 'H16 load / uninstall', 'function rlk:bal/load' in lines('load') and 'function rlk:bal/uninstall' in lines('uninstall'))


# ======================================================================= T tiers and the row
def t_tiers():
    s = sim()
    n = mob(s)
    sw = brain(s, 'sw')
    kr = brain(s, 'kr', extra=('rlk_c2e',))
    pc = brain(s, 'pc', extra=('rlk_c3e',))
    ci = brain(s, 'ci', extra=('rlk_c2e',))
    aux = mob(s, tags=('rlk_room', 'rlk_mb_aux', 'rlk_mb_hit'))
    lob = mob(s, tags=('rlk_lobby', 'rlk_tutT'), etype='zombie')
    pod = mob(s, tags=('rlk_room', 'rlk_c3pod'))
    body = mob(s, tags=('rlk_room', 'rlk_mb_body', 'boss', 'miniboss'))
    rd = mob(s, tags=('rlk_room', 'boss', 'rlk_raiden'), rdPhase=0)
    got = {k: (s.s(e, 'balC'), s.s(e, 'balMax'), s.s(e, 'bal')) for k, e in
           dict(vanilla=n, sw=sw, kr=kr, pc=pc, ci=ci, aux=aux, lobby=lob, pod=pod, body_unflagged=body, raiden=rd).items()}
    want = dict(vanilla=(1, 4, 4), sw=(1, 4, 4), kr=(2, 7, 7), pc=(2, 7, 7), ci=(0, 0, 0), aux=(0, 0, 0), lobby=(0, 0, 0),
                pod=(0, 0, 0), body_unflagged=(0, 0, 0), raiden=(3, 12, 12))
    ck(R, 'T1 tiers: normal 4 (vanilla, swarm), elite 7 (c2e / c3e), boss 12 (Raiden); none for cicin, aux, lobby, pods, '
          'an unflagged registry boss', got == want, {k: v for k, v in got.items() if want[k] != v})
    rows = {k: [x for x in s.passengers(e) if 'rlk_hb_bal' in x.tags] for k, e in dict(n=n, kr=kr, ci=ci, rd=rd).items()}
    ck(R, 'T2 one pip row for normal / elite, none for excluded and bosses',
       [len(rows[k]) for k in ('n', 'kr', 'ci', 'rd')] == [1, 1, 0, 0], {k: len(v) for k, v in rows.items()})
    tr4, tr7 = rows['n'][0].nbt['translation'], rows['kr'][0].nbt['translation']
    ok = all(abs((t[0] - m * 10 * 0.025 * 0.5 / 2) - (-0.8)) < 1e-3 for t, m in ((tr4, 4), (tr7, 7)))
    ck(R, 'T3 the row starts at the HP bar\'s left end (x -0.8), under the bar (y 0.02)', ok and tr4[1] == 0.02, (tr4, tr7))
    ck(R, 'T4 full rows: FFFF / FFFFFFF', glyphs(row_text(s, n)) == 'FFFF' and glyphs(row_text(s, kr)) == 'FFFFFFF',
       (row_text(s, n), row_text(s, kr)))
    s.set(n, 'bal', 2)
    s.run('bal/init', n)          # set up again (a burrower surfacing): gauge kept, no second row
    ck(R, 'T5 re-setup keeps the gauge and the single row', s.s(n, 'bal') == 2 and
       len([x for x in s.passengers(n) if 'rlk_hb_bal' in x.tags]) == 1)
    for x in [x for x in s.passengers(n) if 'rlk_hb_bal' in x.tags]:
        x.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.run('bal/init', n)
    ck(R, 'T6 re-setup without a row (it went with the old head bar) gets one back, drawn',
       len([x for x in s.passengers(n) if 'rlk_hb_bal' in x.tags]) == 1 and glyphs(row_text(s, n)) == 'FFee')


# ======================================================================= P pips and regen
def t_pips():
    for tier, (m, extra) in {1: ('sw', ()), 2: ('kr', ('rlk_c2e',))}.items():
        s = sim()
        e = brain(s, m, extra=extra)
        r = s.run('bal/hit', e, {'n': 1})
        mx = PIPS[tier]
        ck(R, f'P1.{tier} hit 1: {mx}->{mx - 1}, returns 1, regen delay {RD[tier]}, flash {6}',
           r == 1 and s.s(e, 'bal') == mx - 1 and s.s(e, 'balT') == RD[tier] and s.s(e, 'balF') == 6)
        ck(R, f'P2.{tier} the lost pip flashes white, then turns empty after 6 t',
           glyphs(row_text(s, e)) == 'F' * (mx - 1) + 'x')
        for _ in range(6):
            s.run('bal/tick', e)
        ck(R, f'P3.{tier} flash over', glyphs(row_text(s, e)) == 'F' * (mx - 1) + 'e', row_text(s, e))
        for _ in range(RD[tier] - 6 - 1):
            s.run('bal/tick', e)
        b1 = s.s(e, 'bal')
        s.run('bal/tick', e)
        ck(R, f'P4.{tier} +1 pip exactly {RD[tier]} t after the last loss (full again: regen stops, balT 0)',
           b1 == mx - 1 and s.s(e, 'bal') == mx and s.s(e, 'balT') == 0, (b1, s.s(e, 'bal'), s.s(e, 'balT')))
        s.run('bal/hit', e, {'n': 2})
        for _ in range(RD[tier]):
            s.run('bal/tick', e)
        a = s.s(e, 'bal')
        for _ in range(RS[tier]):
            s.run('bal/tick', e)
        ck(R, f'P5.{tier} then +1 per {RS[tier]} t', a == mx - 1 and s.s(e, 'bal') == mx and s.s(e, 'balT') == 0, (a, s.s(e, 'bal')))
        s.run('bal/hit', e, {'n': 1})
        for _ in range(RD[tier] // 2):
            s.run('bal/tick', e)
        s.run('bal/hit', e, {'n': 1})
        ck(R, f'P6.{tier} a new loss restarts the delay', s.s(e, 'balT') == RD[tier] and s.s(e, 'bal') == mx - 2)
        r = s.run('bal/hit', e, {'n': 99})
        ck(R, f'P7.{tier} over-kill clamps at 0 and the groggy starts', r == 1 and s.s(e, 'bal') == 0 and s.s(e, 'grgT') == GRG[tier]
           and 'rlk_bal_grog' in e.tags)
        ck(R, f'P8.{tier} refused while groggy (fails, nothing changes)', s.run('bal/hit', e, {'n': 1}) == 0 and s.s(e, 'grgT') == GRG[tier])
        ck(R, f'P9.{tier} the groggy row', glyphs(row_text(s, e)) == 'G' * mx, row_text(s, e))
        for _ in range(GRG[tier] - 1):
            s.run('bal/tick', e)
        g1 = s.s(e, 'grgT')
        s.run('bal/tick', e)
        ck(R, f'P10.{tier} groggy {GRG[tier]} t, then a full gauge and no regen clock',
           g1 == 1 and s.s(e, 'grgT') == 0 and s.s(e, 'bal') == mx and s.s(e, 'balT') == 0 and 'rlk_bal_grog' not in e.tags
           and glyphs(row_text(s, e)) == 'F' * mx)
    s = sim()
    ex = mob(s, tags=('rlk_room', 'rlk_cm_ci', 'rlk_cmb', 'rlk_c2e'))
    ck(R, 'P11 no gauge: bal/hit fails', s.run('bal/hit', ex, {'n': 1}) == 0 and s.s(ex, 'grgT') == 0)
    e = mob(s)
    ck(R, 'P12 n 0 fails', s.run('bal/hit', e, {'n': 0}) == 0 and s.s(e, 'bal') == 4)


# ======================================================================= S sources
def t_sources():
    s = sim()
    e = mob(s, mhpC=1000)
    s.setsc('#dmg', 'tmp', 10)
    s.setsc('#burstDmg', 'tmp', s.gametime)
    s.setsc('#rx', 'tmp', 0)
    s.run('bal/mods', e)
    a = s.s(e, 'bal')
    s.tick(10)
    s.setsc('#burstDmg', 'tmp', s.gametime)
    s.run('bal/mods', e)                  # the same burst's next hit
    b = s.s(e, 'bal')
    s.tick(30)                               # 40 t after the first: a new burst counts
    s.setsc('#burstDmg', 'tmp', s.gametime)
    s.run('bal/mods', e)
    ck(R, 'S1 burst: 2 pips, once per target per 40 t', (a, b, s.s(e, 'bal')) == (2, 2, 0), (a, b, s.s(e, 'bal')))
    ck(R, 'S2 ... and the 4-pip mob is groggy after two bursts', s.s(e, 'grgT') == 60)
    s = sim()
    e = mob(s, mhpC=1000)
    s.setsc('#dmg', 'tmp', 10)
    s.setsc('#rx', 'tmp', 0)
    s.setsc('#burstDmg', 'tmp', s.gametime - 1)
    s.run('bal/mods', e)
    st = s.s(e, 'bal')
    s.setsc('#burstDmg', 'tmp', s.gametime)
    s.setsc('#dmg', 'tmp', 1000)
    s.run('bal/mods', e)
    ck(R, 'S2b a stale stamp (an earlier tick) and a killing blow take no balance', (st, s.s(e, 'bal')) == (4, 4), (st, s.s(e, 'bal')))
    table = {1: 1, 2: 1, 3: 1, 4: 1, 5: 0, 6: 1, 7: 2, 8: 0, 9: 0, 10: 0, 11: 0, 15: 0, 16: 0, 17: 1, 18: 0, 19: 1, 20: 0, 21: 0, 22: 0, 23: 0}
    got = {}
    for rx in table:
        s = sim()
        e = brain(s, 'kr', extra=('rlk_c2e',), mhpC=1000)
        s.setsc('#dmg', 'tmp', 10)
        s.setsc('#burstDmg', 'tmp', 0)
        s.setsc('#rx', 'tmp', rx)
        s.run('bal/mods', e)
        got[rx] = 7 - s.s(e, 'bal')
    ck(R, 'S3 strong reactions: vaporize / melt / overload / superconduct / frozen 1, shatter 2, void burn / judgement 1, '
          'the rest 0', got == table, {k: v for k, v in got.items() if table[k] != v})
    s = sim()
    e = brain(s, 'kr', extra=('rlk_c2e',), mhpC=1000)
    s.setsc('#dmg', 'tmp', 10)
    s.setsc('#burstDmg', 'tmp', 0)
    s.setsc('#rx', 'tmp', 3)
    s.run('bal/mods', e)
    s.tick(29)
    s.run('bal/mods', e)
    a = s.s(e, 'bal')
    s.tick(1)
    s.run('bal/mods', e)
    ck(R, 'S4 reactions: once per target per 30 t', (a, s.s(e, 'bal')) == (6, 5), (a, s.s(e, 'bal')))
    s = sim()
    e = brain(s, 'kr', extra=('rlk_c2e',), mhpC=1000)
    s.setsc('#dmg', 'tmp', 10)
    s.setsc('#burstDmg', 'tmp', s.gametime)
    s.setsc('#rx', 'tmp', 7)
    s.run('bal/mods', e)
    ck(R, 'S5 a burst that shatters: 2 + 2 pips on one hit', s.s(e, 'bal') == 3)
    s.setsc('#burstDmg', 'tmp', 0)
    s.setsc('#rx', 'tmp', 0)
    n0 = s.cmd_count
    s.run('bal/mods', e)
    ck(R, 'S6 a plain hit on a gauge costs the two tests of bal/mods', s.cmd_count - n0 <= 3 and s.s(e, 'bal') == 3, s.cmd_count - n0)
    # the flag's life: burst_dmg sets it, after_hit / clear_atkflags clear it (real functions)
    s = sim()
    pl = s.spawn('player', tags=('player',))
    s.setsc('#burstDmg', 'tmp', 0)
    s.run('items/hook/burst_dmg', pl)
    on = s.sc('#burstDmg', 'tmp')
    s.run('char/after_hit', pl)
    off = s.sc('#burstDmg', 'tmp')
    ck(R, 'S7 #burstDmg: the game time in burst_dmg, 0 after after_hit', (on, off) == (s.gametime, 0), (on, off))


# ======================================================================= D damage bonus
def t_amp():
    for tier, tags in {1: ('rlk_room', 'rlk_m_husk'), 2: ('rlk_room', 'rlk_cmb', 'rlk_cm_kr', 'rlk_c2e'),
                       3: ('rlk_room', 'boss', 'rlk_raiden')}.items():
        s = sim()
        e = mob(s, tags=tags, rdPhase=0)
        s.setsc('#dmg', 'tmp', 1000)
        s.setsc('#tfm', 'tmp', 0)
        s.setsc('#charN', 'tmp', 1)
        s.run('combat/apply_mods', e)
        base = s.sc('#dmg', 'tmp')
        s.set(e, 'grgT', 5)
        s.setsc('#dmg', 'tmp', 1000)
        s.run('combat/apply_mods', e)
        ck(R, f'D1.{tier} groggy: damage x{AMP[tier]} % (combat/apply_mods)', (base, s.sc('#dmg', 'tmp')) == (1000, AMP[tier] * 10),
           (base, s.sc('#dmg', 'tmp')))


# ======================================================================= C cm family
ATTACK_START = r'(/start|_go|/b_start|/a_start|/f_start|/d_try|/sstart|/rstart|/pack_go|/line_go)$'


def t_cm():
    for m, extra, cms in (('sw', (), 1), ('ar', (), 1), ('fm', (), 2), ('kr', ('rlk_c2e',), 2), ('sh', (), 3),
                          ('cs', ('rlk_c3e',), 1), ('rv', ('rlk_c3e',), 3)):
        s = sim(extra_real=(f'rlk:cm/{m}/tick',))
        body = s.spawn('player', pos=(1.5, 201.0, 0.5), tags=('rlk_body',))
        nbt = {'NoAI': 1} if m == 'rv' else {}
        e = brain(s, m, extra=extra, cmS=cms, cmCd=0, cmCd2=0)
        e.nbt.update(nbt)
        e.tags.add('rlk_cmch')
        s.setsc('#cmDown', 'tmp', 0)
        s.run('bal/hit', e, {'n': 99})
        tier = 2 if extra else 1
        ck(R, f'C1.{m} entry: attack cancelled (cmS 0, charge tag off), AI off, stunned, cooldowns held',
           s.s(e, 'cmS') == 0 and 'rlk_cmch' not in e.tags and e.nbt.get('NoAI') == 1 and s.s(e, 'stunT') == 2
           and s.s(e, 'cmCd') >= 10 and s.s(e, 'cmCd2') >= 10 and s.s(e, 'grgT') == GRG[tier],
           (s.s(e, 'cmS'), e.nbt, s.s(e, 'stunT'), s.s(e, 'cmCd')))
        s.stubbed.clear()
        for k in range(GRG[tier] - 1):
            s.run('bal/tick', e)                 # mob/tick's line
            s.run('cm/tick', e)                  # cm/world's line
        starts = s.stub_calls(ATTACK_START)
        ck(R, f'C2.{m} {GRG[tier] - 1} groggy ticks: no attack start, still held',
           not starts and s.s(e, 'cmS') == 0 and e.nbt.get('NoAI') == 1 and s.s(e, 'grgT') == 1, starts[:3])
        s.run('bal/tick', e)
        ck(R, f'C3.{m} exit: full gauge, AI back as it was (rv stays NoAI), stun released next mob tick',
           s.s(e, 'grgT') == 0 and s.s(e, 'bal') == PIPS[tier] and e.nbt.get('NoAI', 0) == (1 if m == 'rv' else 0)
           and s.s(e, 'stunT') == 0 and 'rlk_bal_noai' not in e.tags, (e.nbt, s.s(e, 'stunT')))
    for m, extra in (('sw', ()), ('ar', ()), ('kr', ('rlk_c2e',))):
        s = sim(extra_real=(f'rlk:cm/{m}/tick',))
        s.spawn('player', pos=(1.5, 201.0, 0.5), tags=('rlk_body',))
        e = brain(s, m, extra=extra, cmS=0, cmCd=0, cmCd2=0)
        s.setsc('#cmDown', 'tmp', 0)
        s.run('cm/tick', e)
        ck(R, f'C0.{m} control: the same brain, not groggy, starts an attack on that tick', bool(s.stub_calls(ATTACK_START)),
           s.stub_calls()[:6])
    s = sim()
    dr = brain(s, 'dr', extra=('rlk_c2', 'rlk_c2a', 'rlk_dr_drum'))
    s.setsc('#c2DrI', 'tmp', 40)
    s.run('bal/hit', dr, {'n': 4})
    ck(R, 'C4 a groggy drummer stops drumming', 'rlk_dr_drum' not in dr.tags and s.s(dr, 'c2T2') == 40)


# ======================================================================= V vanilla + freeze
def t_vanilla():
    def fresh(noai=0):
        s = sim()
        s.stub_fns['rlk:element/frz_measure'] = lambda S, c, m: (S.setsc('#fzW', 'tmp', 600), S.setsc('#fzH', 'tmp', 1950))
        s.setsc('#neg1', 'tmp', -1)
        e = mob(s)
        e.nbt['NoAI'] = noai
        s.set(e, 'frzT', 0)
        return s, e

    def freeze(s, e, t):
        s.setsc('#frzTicks', 'tmp', t)
        s.run('element/frz_start', e)

    def thaw(s, e):
        s.run('element/frz_end', e)

    for noai in (0, 1):
        s, e = fresh(noai)
        s.run('bal/hit', e, {'n': 4})
        on = e.nbt.get('NoAI')
        for _ in range(60):
            s.run('bal/tick', e)
        ck(R, f'V1.{noai} vanilla groggy: NoAI on, then back to {noai}', (on, e.nbt.get('NoAI', 0), s.s(e, 'grgT')) == (1, noai, 0))
        # freeze first, groggy inside it, freeze ends first
        s, e = fresh(noai)
        freeze(s, e, 40)
        s.run('bal/hit', e, {'n': 4})
        thaw(s, e)
        mid = e.nbt.get('NoAI')
        for _ in range(60):
            s.run('bal/tick', e)
        ck(R, f'V2.{noai} freeze -> groggy -> thaw -> groggy end: AI held through, then {noai}',
           (mid, e.nbt.get('NoAI', 0)) == (1, noai) and not ({'rlk_noai', 'rlk_bal_noai'} & e.tags), (mid, e.nbt, e.tags))
        # groggy first, freeze inside it, groggy ends first, then the thaw
        s, e = fresh(noai)
        s.run('bal/hit', e, {'n': 4})
        freeze(s, e, 200)
        for _ in range(60):
            s.run('bal/tick', e)
        mid = e.nbt.get('NoAI')
        thaw(s, e)
        ck(R, f'V3.{noai} groggy -> freeze -> groggy end -> thaw: frozen keeps NoAI, the thaw restores {noai}',
           (mid, e.nbt.get('NoAI', 0)) == (1, noai) and not ({'rlk_noai', 'rlk_bal_noai'} & e.tags), (mid, e.nbt, e.tags))
        # freeze first, groggy inside, groggy ends while frozen, then the thaw
        s, e = fresh(noai)
        freeze(s, e, 200)
        s.run('bal/hit', e, {'n': 4})
        for _ in range(60):
            s.run('bal/tick', e)
        mid = e.nbt.get('NoAI')
        thaw(s, e)
        ck(R, f'V4.{noai} freeze -> groggy -> groggy end -> thaw: {noai} at the end',
           (mid, e.nbt.get('NoAI', 0)) == (1, noai) and not ({'rlk_noai', 'rlk_bal_noai'} & e.tags), (mid, e.nbt, e.tags))


# ======================================================================= B bosses
def t_boss():
    s = sim()
    rd = mob(s, tags=('rlk_room', 'boss', 'rlk_raiden'), rdPhase=0, rdPat=0, rdDeath=0, rdBlink=0, rdNext=0, rdSgEye=0,
             rdTime=0, rdGo=0, rdSgGs=0, rdSgCt=0, rdSgStun=0)
    for k, v in dict(rdPhase=2).items():
        s.set(rd, k, v)
    ck(R, 'B1 Raiden refuses balance damage outside the Shogun phase (Tenma: the armour is the gauge)',
       s.run('bal/hit', rd, {'n': 1}) == 0 and s.s(rd, 'bal') == 12)
    s.set(rd, 'rdPhase', 0)
    s.set(rd, 'rdPat', 5)
    r = s.run('bal/hit', rd, {'n': 12})
    ck(R, 'B2 at 0 inside 찰나의 포영 (pattern 5): pending, no stun yet',
       r == 1 and 'rlk_bal_pend' in rd.tags and s.s(rd, 'grgT') == 0 and s.s(rd, 'rdPat') == 5)
    ck(R, 'B3 pending: further balance damage fails', s.run('bal/hit', rd, {'n': 1}) == 0)
    s.run('bal/boss/tick', rd)
    ck(R, 'B4 still in pattern 5: still pending', 'rlk_bal_pend' in rd.tags)
    s.set(rd, 'rdPat', 3)
    s.run('bal/boss/tick', rd)
    ck(R, 'B5 the next allowed tick: the stun (rdPat 98, rdSgStun 4) for 100 t',
       'rlk_bal_pend' not in rd.tags and s.s(rd, 'grgT') == 100 and s.s(rd, 'rdPat') == 98 and s.s(rd, 'rdSgStun') == 4
       and bool(s.stub_calls(r'raiden/hazard/finish$')))
    s.storage.setdefault('rlk:bal', {})
    ck(R, 'B6 the boss row shows the groggy look', glyphs(s.storage['rlk:bal']['brow']['extra'][0]['text']) == 'G' * 12)
    for k in range(99):
        s.set(rd, 'rdTime', k + 1)
        s.run('boss/raiden/sg/stun_tick', rd)
        s.run('bal/boss/tick', rd)
    ck(R, 'B7 her stun tick does not end a balance stun at 100 by itself', s.s(rd, 'rdSgStun') == 4 and s.s(rd, 'grgT') == 1
       and not s.stub_calls(r'raiden/finish$'))
    s.run('bal/boss/tick', rd)
    ck(R, 'B8 the gauge clock ends it: stun_end (finish), full gauge',
       s.s(rd, 'grgT') == 0 and s.s(rd, 'rdSgStun') == 0 and bool(s.stub_calls(r'raiden/finish$')) and s.s(rd, 'bal') == 12
       and glyphs(s.storage['rlk:bal']['brow']['extra'][0]['text']) == 'F' * 12)
    for k, v in dict(rdNext=7).items():
        s.set(rd, k, v)
    s.set(rd, 'rdPat', 0)
    ck(R, 'B9 bal_ok refuses the forced follow-up (rdNext 7)', s.run('boss/raiden/bal_ok', rd) == 0)
    s.set(rd, 'rdNext', 0)
    ck(R, 'B10 bal_ok allows an idle Shogun', s.run('boss/raiden/bal_ok', rd) == 1)
    # registry bosses: the dispatchers name exactly the flagged entries (check_mboss_pack checks it against the registry)
    import json
    reg = json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
    flagged = sorted(b['n'] for b in reg['boss'] if b.get('bal') and b.get('enabled', True))
    import re as _re
    got = sorted(int(x) for x in _re.findall(r'matches (\d+) ', '\n'.join(lines('mboss/d/bal_has'))))
    ck(R, 'B11 mboss/d/bal_has = the registry entries flagged "bal"', got == flagged, (got, flagged))
    s = sim()
    s.setsc('#mbId', 'mb', 99999)
    body = mob(s, tags=('rlk_room', 'rlk_mb_body', 'boss'))
    ck(R, 'B12 an unflagged registry boss has no gauge', s.s(body, 'balMax') == 0)
    s = sim()
    s.setsc('#mbSt', 'mb', 0)
    s.stub_fns['rlk:mboss/d/bal_has'] = lambda S, c, m: 1
    s.real = tuple(r for r in s.real if r != 'rlk:mboss/d/bal_')
    body = mob(s, tags=('rlk_room', 'rlk_mb_body', 'boss'))
    ck(R, 'B13 a flagged registry boss: 12 pips, refused in the intro (#mbSt 0)', s.s(body, 'balMax') == 12
       and s.run('bal/hit', body, {'n': 1}) == 0)
    s.setsc('#mbSt', 'mb', 1)
    s.setsc('#mbCine', 'mb', 1)
    ck(R, 'B14 ... and in a cutscene (#mbCine 1)', s.run('bal/hit', body, {'n': 1}) == 0)
    s.setsc('#mbCine', 'mb', 0)
    s.setsc('#mbBarOff', 'mb', 1)
    ck(R, 'B15 ... and while the bars are off (#mbBarOff 1)', s.run('bal/hit', body, {'n': 1}) == 0)
    s.setsc('#mbBarOff', 'mb', 0)
    s.stub_fns['rlk:mboss/d/bal_ok'] = lambda S, c, m: 0
    ck(R, 'B16 in the fight: taken; at 0 with bal_ok refusing -> pending', s.run('bal/hit', body, {'n': 12}) == 1
       and 'rlk_bal_pend' in body.tags and not s.stub_calls(r'mboss/d/bal_on$'))
    s.stub_fns['rlk:mboss/d/bal_ok'] = lambda S, c, m: 1
    s.run('bal/boss/tick', body)
    ck(R, 'B17 bal_ok allows: bal_on once, grgT 100', s.s(body, 'grgT') == 100 and len(s.stub_calls(r'mboss/d/bal_on$')) == 1)
    for _ in range(100):
        s.run('bal/boss/tick', body)
    ck(R, 'B18 100 t later: bal_off once, full gauge', len(s.stub_calls(r'mboss/d/bal_off$')) == 1 and s.s(body, 'bal') == 12)
    s.run('bal/hit', body, {'n': 1})
    t0 = s.s(body, 'balT')
    s.setsc('#mbPause', 'mb', 1)
    s.run('bal/tick', body)
    paused = s.s(body, 'balT')
    s.setsc('#mbPause', 'mb', 0)
    s.setsc('#mbSt', 'mb', 2)
    s.run('bal/tick', body)
    dying = s.s(body, 'balT')
    s.setsc('#mbSt', 'mb', 1)
    s.run('bal/tick', body)
    ck(R, 'B19 a registry boss through mob/tick (bal/tick): the clock stops while the fight is paused or not in its fight state',
       (t0, paused, dying, s.s(body, 'balT')) == (300, 300, 300, 299), (t0, paused, dying, s.s(body, 'balT')))


# ======================================================================= K cleanup
def t_cleanup():
    s = sim()
    e = mob(s)
    k = brain(s, 'kr', extra=('rlk_c2e',))
    s.run('bal/hit', k, {'n': 7})
    row = [x for x in s.passengers(e) if 'rlk_hb_bal' in x.tags][0]
    e.alive = False                          # killed
    s.ents = [x for x in s.ents if x.alive]
    row.vehicle = None
    s.run('mob/hb_cleanup')
    ck(R, 'K1 death: the orphan row is killed by mob/hb_cleanup, the living mob keeps its row', not row.alive
       and len([x for x in s.passengers(k) if 'rlk_hb_bal' in x.tags]) == 1)
    s.run('bal/load')
    ck(R, 'K2 /reload (bal/load again): the groggy and the gauge go on', s.s(k, 'grgT') == 80 and s.s(k, 'bal') == 0)
    old = s.spawn('husk', tags=('rlk_room', 'rlk_mob'))
    s.run('bal/load')
    ck(R, 'K3 /reload into an older world: a mob without a gauge gets one', s.s(old, 'balMax') == 4
       and len([x for x in s.passengers(old) if 'rlk_hb_bal' in x.tags]) == 1)
    s.run('uninstall' if False else 'bal/uninstall')
    left = [o for (_, o) in s.scores if o in ('bal', 'balMax', 'balT', 'grgT', 'balC', 'balF', 'balQ', 'balX')]
    ck(R, 'K4 uninstall: the groggy brain gets its AI back, rows gone, scores gone, tables gone',
       k.nbt.get('NoAI', 0) == 0 and not [x for x in s.ents if 'rlk_hb_bal' in x.tags] and not left
       and 'rlk_bal_grog' not in k.tags and not s.storage.get('rlk:bal'), (k.nbt, left[:4], s.storage.get('rlk:bal', {}).keys()))


# ======================================================================= $ cost
def t_cost():
    s = sim()
    e = brain(s, 'sw')
    s.run('bal/hit', e, {'n': 1})
    for _ in range(10):
        s.run('bal/tick', e)
    n0 = s.cmd_count
    s.run('bal/tick', e)
    regen = s.cmd_count - n0
    s.run('bal/hit', e, {'n': 9})
    n0 = s.cmd_count
    s.run('bal/tick', e)
    grog = s.cmd_count - n0
    ck(R, f'$1 a regen tick <= 6 commands ({regen}), a groggy tick <= 14 ({grog}) — only while pips are missing / groggy',
       regen <= 6 and grog <= 14, (regen, grog))
    L = [l for l in lines('mob/tick') if 'bal' in l and not l.startswith('#')]
    ck(R, '$2 an idle mob pays one score test in mob/tick', len(L) == 1 and L[0].startswith('execute if score @s balT matches 1..'))


for t in (t_gen, t_hooks, t_tiers, t_pips, t_sources, t_amp, t_cm, t_vanilla, t_boss, t_cleanup, t_cost):
    print(f'--- {t.__name__}')
    try:
        t()
    except Exception as ex:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        ck(R, f'{t.__name__} crashed', False, repr(ex))
sys.exit(summary(R))
