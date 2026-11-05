#!/usr/bin/env python3
"""test_moon.py: the run buff 「월하대작」 (objective hrMoon), stage SR (scratchpad hr/PLAN.md §7.5, §7.6; contract §1 SR row,
§3.7). Hand-maintained files only. items/stat_light (-> player/level/apply, items/hook/stat_buffs -> player/hr_moon/apply),
player/reset_one and player/update_item run for real from the datapack in the vendored sims (HR/tests/lib, read only)
through SR's helpers HR/sr/srsim.py; update_item_macro's line is filled with the game's macro stringification and its
lore parsed back.

    python3 test_moon.py <datapack root> [section ...] [-v]

  static  load (objective beside nodeHp, the 조절 지점 constants = api.BUFF_VALUES['run'] under api.BUFF_FP), uninstall,
          reset_one, the stat_buffs line, hr_moon/apply, update_item (hash, $(moon)), update_item_macro (`,$(moon)` last),
          the status format = api.EV_TEXT['status'], static rules
  stat    stat_buffs adds exactly +20 ampAtk / +10 crit / +10 move when hrMoon 1, nothing when 0
  atk     final ATK = old x 1.20 (+-1) through the real stat_light (several bases / % / flat), crit and move final values
  reset   reset_one clears it (run scope); the documented forever switch (F3, HR-11: load's #hrMoonRun 0) keeps it; uninstall
          removes it
  lore    the stat-item lore line present iff on, its numbers = the constants (also changed ones), its scope word from
          #hrMoonRun ("이번 런" / "영구", F3 HR-11), the hash changes with it
  F3 (HR-11): the scope is one switch: api.EVENT['buff_scope'] (the event texts) and load's 조절 지점 (#hrMoon* =
  api.BUFF_VALUES[scope], #hrMoonRun 1 / 0) agree; reset_one and update_item read #hrMoonRun (no line to delete)
"""
import copy
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'sr'))
import srsim as S  # noqa: E402

ARGS = [a for a in sys.argv[1:] if a != '-v']
VERBOSE = '-v' in sys.argv[1:]
DP = Path(ARGS[0]).resolve()
SECTIONS = ARGS[1:] or ['static', 'stat', 'atk', 'reset', 'lore']
sys.path.insert(0, str(DP / 'tools'))
import mboss_scarlet.api as API  # noqa: E402

FN = DP / 'data/rlk/function'
N = [0]
OBJ = API.BUFF_OBJ
FPA, FPC, FPS = API.BUFF_FP
RUN = API.BUFF_VALUES['run']
# F3 (HR-11): the scope words (api.BUFF_SCOPE_WORDS; the literal fallback lets the suite run on a tree before F3)
SCOPE_WORDS = getattr(API, 'BUFF_SCOPE_WORDS', {'run': ('이번 런 동안', '이번 런'), 'forever': ('영구히', '영구')})


def ck(name, ok, info=''):
    N[0] += 1
    if VERBOSE and ok:
        print('ok  ', name, info)
    return S.ck(name, ok, info)


def rd(rel):
    return (FN / (rel + '.mcfunction')).read_text(encoding='utf-8')


def lines(rel):
    return [l for l in rd(rel).split('\n') if l.strip() and not l.lstrip().startswith('#')]


# ================================================================================================== static
def t_static():
    ld = rd('load').split('\n')
    ck('api: objective hrMoon, constants #hrMoonAtk / Crit / Spd', OBJ == 'hrMoon' and API.BUFF_FP == ('#hrMoonAtk', '#hrMoonCrit', '#hrMoonSpd'))
    ck('load: objective added once, beside nodeHp', ld.count('scoreboard objectives add hrMoon dummy') == 1
       and ld.index('scoreboard objectives add hrMoon dummy') == ld.index('scoreboard objectives add nodeHp dummy') + 2)
    k = ld.index('# ===== 조절 지점 =====')
    for fp, v in zip(API.BUFF_FP, RUN):
        ln = f'scoreboard players set {fp} tmp {v}'
        ck(f'load 조절 지점: {ln} (= api.BUFF_VALUES run)', ld.count(ln) == 1 and ld.index(ln) > k)
    ck('load: the forever values (api.BUFF_VALUES forever) named in the comment',
       ' · '.join(map(str, API.BUFF_VALUES['forever'])) in rd('load'))
    ck('load: the rift hook line still right under 조절 지점', ld[k + 1] == '# rift (build_rift.py)'
       and ld[k + 2] == 'scoreboard players set #riftPm room 30')
    un = rd('uninstall').split('\n')
    ck('uninstall: objective removed once (beside nodeHp)', un.count('scoreboard objectives remove hrMoon') == 1
       and un.index('scoreboard objectives remove hrMoon') == un.index('scoreboard objectives remove nodeHp') + 1)
    ro = lines('player/reset_one')
    ck('reset_one: the scope line reads load\'s #hrMoonRun (HR-11: run unless 0)',
       ro.count('execute unless score #hrMoonRun tmp matches 0 run scoreboard players set @s hrMoon 0') == 1
       and 'scoreboard players set @s hrMoon 0' not in ro, [l for l in ro if 'hrMoon' in l])
    scope = API.EVENT['buff_scope']
    run_flag = 1 if scope == 'run' else 0
    vals = [f'scoreboard players set {fp} tmp {v}' for fp, v in zip(API.BUFF_FP, API.BUFF_VALUES[scope])]
    flag = f'scoreboard players set #hrMoonRun tmp {run_flag}'
    ck(f'HR-11 one switch: load\'s 조절 지점 = api.EVENT buff_scope "{scope}" (#hrMoon* = api.BUFF_VALUES[{scope}], '
       f'#hrMoonRun {run_flag} right after them)', flag in ld and all(v in ld for v in vals)
       and ld.index(flag) == ld.index(vals[-1]) + 1, [l for l in ld if '#hrMoon' in l])
    cm = ld[ld.index(vals[0]) - 3:ld.index(vals[0])]
    ck('HR-11 load: the switch comment names #hrMoonRun 0, the forever values and api.EVENT buff_scope',
       any('#hrMoonRun 0' in l for l in cm) and any("EVENT['buff_scope']" in l for l in cm), cm)
    sb = [l for l in lines('items/hook/stat_buffs') if 'hrMoon' in l]
    ck('stat_buffs: one line', sb == ['execute if score @s hrMoon matches 1.. run function rlk:player/hr_moon/apply'], sb)
    ap = lines('player/hr_moon/apply')
    ck('hr_moon/apply = ampAtk / critChance / moveSpeed += the constants',
       ap == [f'scoreboard players operation @s ampAtk += {FPA} tmp', f'scoreboard players operation @s critChance += {FPC} tmp',
              f'scoreboard players operation @s moveSpeed += {FPS} tmp'], ap)
    ui = rd('player/update_item')
    ck('update_item: hrMoon joins the hash', 'scoreboard players operation #uh tmp += @s hrMoon' in ui
       and ui.index('#uh tmp += @s hrMoon') < ui.index('run return 0'))
    m = re.search(r'set value (\{translate:"rlk\.hr_moon".*\})$', ui, re.M)
    ck('update_item: the on-line is a translate with fallback', bool(m))
    comp = S.snbt_parse(m.group(1))
    ck('status format with the run constants = api.EV_TEXT status', S.render(dict(comp, **{'with': list(RUN) + ['이번 런']}))
       == API.EV_TEXT['status'], S.render(dict(comp, **{'with': list(RUN) + ['이번 런']})))
    ck('HR-11 update_item: the scope word is with[3] ("이번 런"), "영구" when #hrMoonRun 0',
       comp.get('with', [None] * 4)[3:] == [SCOPE_WORDS['run'][1]]
       and f'execute if score @s hrMoon matches 1.. if score #hrMoonRun tmp matches 0 run data modify storage rlk:item moon.with[3] '
           f'set value "{SCOPE_WORDS["forever"][1]}"' in ui.split('\n'), comp.get('with'))
    ck('status line colour #DDE6FF, not italic', comp.get('color') == '#DDE6FF' and comp.get('italic') == 0)
    ck('update_item: numbers stored from the constants', all(f'run scoreboard players get {fp} tmp' in ui for fp in API.BUFF_FP))
    um = rd('player/update_item_macro')
    ck('update_item_macro: $(moon) is the last lore entry', ',$(moon)],minecraft:custom_data={rlk_stat:1b}]' in um and um.count('$(moon)') == 1)
    mine = [l for rel in ('load', 'uninstall', 'player/reset_one', 'player/update_item', 'items/hook/stat_buffs',
                          'player/hr_moon/apply') for l in rd(rel).split('\n') if 'hrMoon' in l or 'hr_moon' in l]
    ck('no negative literal in add/remove', not [l for l in mine if re.search(r'scoreboard players (add|remove) \S+ \S+ -', l)])
    ck('ids lowercase', all(x == x.lower() for l in mine for x in re.findall(r'\brlk:[A-Za-z0-9_./-]+', l)))


# ================================================================================================== stat
def stat_once(s, pl, moon, atkpct=0, crit=5, move=100):
    P = ('e', pl.id)
    s.setsc(P, OBJ, moon)
    s.setsc(P, 'ampAtk', 100)
    s.setsc(P, 'atkPct', atkpct)
    s.setsc(P, 'critChance', crit)
    s.setsc(P, 'moveSpeed', move)
    n0 = len(s.log)
    s.call('rlk:items/hook/stat_buffs', S.pctx(s, pl))
    calls = [l[2] for l in s.log[n0:] if l[1] == 'call' and l[2] == 'rlk:player/hr_moon/apply']
    return s.sc(P, 'ampAtk'), s.sc(P, 'critChance'), s.sc(P, 'moveSpeed'), s.sc(P, 'atkPct'), calls


def t_stat():
    s, pl = S.world(DP)
    s.setsc(('e', pl.id), 'it_sword_hwamu', 0)
    off = stat_once(s, pl, 0)
    on = stat_once(s, pl, 1)
    ck('off: nothing added, apply not called', off[:4] == (100, 5, 100, 0) and not off[4], off)
    ck('on: ampAtk +20 / crit +10 / move +10 exactly', on[:4] == (100 + RUN[0], 5 + RUN[1], 100 + RUN[2], 0) and len(on[4]) == 1, on)
    # with the sword held too (both rolls cannot happen in one run, but a lobby copy can be held with the buff)
    s.setsc(('e', pl.id), 'it_sword_hwamu', 1)
    S.set_star(s, 3)
    on2 = stat_once(s, pl, 1, atkpct=10)
    ck('with the sword: the buff adds the same, atkPct untouched by it', on2[:3] == (120, 15, 110) and on2[3] == 10, on2)
    # changed constants follow (조절 지점)
    for fp, v in zip(API.BUFF_FP, (25, 12, 7)):
        s.setsc(fp, 'tmp', v)
    on3 = stat_once(s, pl, 1)
    ck('changed constants (25 / 12 / 7) follow', on3[:3] == (125, 17, 107), on3)


# ================================================================================================== atk
def t_atk():
    s, pl = S.world(DP)
    P = ('e', pl.id)
    s.setsc(P, 'it_sword_hwamu', 0)
    for lv, pct, flat in ((1, 0, 0), (10, 0, 0), (10, 37, 0), (25, 120, 15), (40, 233, 41), (7, 5, 3)):
        out = {}
        for moon in (0, 1):
            s.setsc(P, 'level', lv)
            s.setsc(P, OBJ, moon)
            for o in ('eqAtkPct', 'eqAtkFlat', 'eqCritChance', 'eqMoveSpeed', 'eqHpPct', 'eqHpFlat', 'eqDefPct', 'eqDefFlat'):
                s.setsc(P, o, 0)
            s.setsc(P, 'eqAtkPct', pct)
            s.setsc(P, 'eqAtkFlat', flat)
            for o, v in (('base_critChance', 5), ('base_critDamage', 50), ('base_moveSpeed', 100), ('base_atkSpeed', 100),
                         ('base_elemMastery', 0), ('base_energyRecharge', 100), ('hpMaxPrev', -1), ('nodeHp', 0)):
                s.setsc(P, o, v)
            s.call('rlk:items/stat_light', S.pctx(s, pl))
            out[moon] = (s.sc(P, 'atk'), s.sc(P, 'critChance'), s.sc(P, 'moveSpeed'))
        old, new = out[0][0], out[1][0]
        ck(f'Lv {lv} +{pct}% +{flat}: ATK {old} -> {new} = x1.20 (+-1)', abs(new - old * 120 / 100) <= 1, (old, new))
        ck(f'Lv {lv}: crit +{RUN[1]}, move +{RUN[2]}', out[1][1] - out[0][1] == RUN[1] and out[1][2] - out[0][2] == RUN[2], out)
    # the multiplier comes after every atkPct (not diluted by item ATK %): +100 % items -> still x1.20 of the total
    ck('ampAtk is applied after atkPct and flat (stat_light:47-48)', 'scoreboard players operation @s atk *= @s ampAtk' in rd('items/stat_light'))


# ================================================================================================== reset
def load_k(s):
    """load's 조절 지점 lines of the buff (#hrMoon* incl. #hrMoonRun) run in s."""
    s.cache['rlk:srtest/moon_k'] = [l for l in rd('load').split('\n') if l.startswith('scoreboard players set #hrMoon')]
    s.call('rlk:srtest/moon_k', S.C0)


def reset_world():
    s, pl = S.world(DP)
    load_k(s)
    for f in ('rlk:char/start_reset', 'rlk:lvup/exit', 'rlk:player/init', 'rlk:lvup/init', 'rlk:items/tune/reapply_all',
              'rlk:player/reset_stacks', 'rlk:element/infuse_end', 'rlk:items/equip_scan'):
        s.cache[f] = []                    # the heavy calls of reset_one (not this buff); its own lines run for real
    return s, pl


def t_reset():
    s, pl = reset_world()
    P = ('e', pl.id)
    s.setsc(P, OBJ, 1)
    s.setsc(P, 'sapphire', 7)
    s.call('rlk:player/reset_one', S.pctx(s, pl))
    ck('reset_one (run scope): hrMoon 0', s.sc(P, OBJ) == 0)
    ck('reset_one: sapphire kept (the only cross-run value)', s.sc(P, 'sapphire') == 7)
    # the forever switch of PLAN §7.5.3 (F3, HR-11): load's #hrMoonRun 0, nothing to delete
    src = rd('player/reset_one').split('\n')
    gl = 'execute unless score #hrMoonRun tmp matches 0 run scoreboard players set @s hrMoon 0'
    ck('reset_one: the switch is documented right above the line', gl in src and '영구' in src[src.index(gl) - 1])
    s, pl = reset_world()
    P = ('e', pl.id)
    s.setsc('#hrMoonRun', 'tmp', 0)
    s.setsc(P, OBJ, 1)
    s.call('rlk:player/reset_one', S.pctx(s, pl))
    ck('HR-11 forever switch (load\'s #hrMoonRun 0): hrMoon kept by reset_one', s.sc(P, OBJ) == 1)
    s, pl = S.world(DP)
    for f in ('rlk:char/start_reset', 'rlk:lvup/exit', 'rlk:player/init', 'rlk:lvup/init', 'rlk:items/tune/reapply_all',
              'rlk:player/reset_stacks', 'rlk:element/infuse_end', 'rlk:items/equip_scan'):
        s.cache[f] = []
    s.setsc(('e', pl.id), OBJ, 1)
    s.call('rlk:player/reset_one', S.pctx(s, pl))
    ck('reset_one without load\'s constant (#hrMoonRun unset): the run scope (cleared)', s.sc(('e', pl.id), OBJ) == 0)
    # run start / run failure / rlk:reset reach reset_one (PLAN §7.5.2)
    callers = [p.relative_to(FN).as_posix() for p in FN.rglob('*.mcfunction') if 'function rlk:player/reset_one' in p.read_text(encoding='utf-8')]
    ck('reset_one is reached by run start / run fail / reset', all(any(c.startswith(x) for c in callers) for x in ('run/start', 'run/fail', 'reset')), callers)
    # uninstall: the objective goes (the scores with it)
    s, pl = S.world(DP)
    s.setsc(('e', pl.id), OBJ, 1)
    for l in [l for l in lines('uninstall') if l.endswith(' hrMoon')]:
        t = l.split()
        if t[:3] == ['scoreboard', 'objectives', 'remove']:
            for k in [k for k in s.scores if k[1] == t[3]]:
                del s.scores[k]
    ck('uninstall: hrMoon scores gone', s.sc(('e', pl.id), OBJ) is None)


# ================================================================================================== lore
def item_lore(s, pl):
    """Run the real player/update_item; fill update_item_macro's line with the recorded arguments (the game's macro
    stringification) and return (the lore as rendered strings, the lore components, the hash)."""
    s.macro_calls.clear()
    s.items_present = False
    s.call('rlk:player/update_item', S.pctx(s, pl))
    assert s.macro_calls, 'update_item_macro not called'
    args = s.macro_calls[-1][1]
    line = rd('player/update_item_macro').strip()[1:]
    cmd = S._sub(line, args)
    m = re.search(r'minecraft:lore=(\[.*\]),minecraft:custom_data=', cmd)
    lore = S.snbt_parse(m.group(1))
    return [S.render(x) for x in lore], lore, s.sc('#uh', 'tmp')


def t_lore():
    s, pl = S.world(DP)
    P = ('e', pl.id)
    for o, v in (('level', 12), ('xp', 3), ('xpNeed', 60), ('curHealth', 200), ('maxHealth', 232), ('atk', 120),
                 ('base_atk', 32), ('def', 40), ('base_def', 32), ('elemMastery', 0), ('moveSpeed', 110), ('atkSpeed', 100),
                 ('critChance', 15), ('critDamage', 50), ('gold', 99), ('sapphire', 2), ('energyRecharge', 100),
                 ('base_maxHealth', 232), ('uiHash', 0)):
        s.setsc(P, o, v)
    for b in ('physBonus', 'pyroBonus', 'hydroBonus', 'electroBonus', 'cryoBonus', 'geoBonus', 'anemoBonus', 'dendroBonus'):
        s.setsc(P, b, 0)
    s.setsc(P, OBJ, 0)
    off, offc, h0 = item_lore(s, pl)
    s.setsc(P, OBJ, 1)
    on, onc, h1 = item_lore(s, pl)
    ck('off: no status line anywhere', API.EV_TEXT['status'] not in off and not any('월하대작' in x for x in off))
    ck('off: the last entry is an empty text', off[-1] == '' and offc[-1] == {'text': '', 'italic': 0}, offc[-1])
    ck('on: the last entry = api.EV_TEXT status (numbers = the constants)', on[-1] == API.EV_TEXT['status'], on[-1])
    ck('on: exactly one status line', sum(1 for x in on if '월하대작' in x) == 1)
    ck('on / off: every other line identical', on[:-1] == off[:-1])
    ck('the hash changes with hrMoon (the item is rebuilt when the buff turns on)', h0 != h1)
    ck('lore entries: stat lines unchanged count (+0 when off, the status replaces the empty last line)', len(on) == len(off))
    for fp, v in zip(API.BUFF_FP, (25, 12, 7)):
        s.setsc(fp, 'tmp', v)
    on2, _, _ = item_lore(s, pl)
    ck('changed constants: the line shows them', on2[-1] == '☾ 월하대작 · 최종 공격력 +25% · 치명타 확률 +12% · 이동 속도 +7% (이번 런)', on2[-1])
    for fp, v in zip(API.BUFF_FP, API.BUFF_VALUES['forever']):
        s.setsc(fp, 'tmp', v)
    s.setsc('#hrMoonRun', 'tmp', 0)
    on3, _, _ = item_lore(s, pl)
    ck('HR-11 the forever switch (8 / 4 / 4, #hrMoonRun 0): the line shows "(영구)" and the numbers',
       on3[-1] == '☾ 월하대작 · 최종 공격력 +8% · 치명타 확률 +4% · 이동 속도 +4% (영구)', on3[-1])
    RENDER['off'], RENDER['on'] = off, on


RENDER = {}

if __name__ == '__main__':
    for sec in SECTIONS:
        globals()['t_' + sec]()
    sys.exit(S.summary('test_moon', N[0]))
