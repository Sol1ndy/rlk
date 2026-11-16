#!/usr/bin/env python3
"""test_hwamu.py: the mythic item 「[ MYTHIC ] 화무십일홍」 (sword_hwamu), stage SR (scratchpad hr/PLAN.md §7.4, §7.6;
contract §1 SR row, §3.7). Hand-maintained files only (no generator). The item's functions, char/dmg_calc, combat/apply
(azsim: element reactions, level factor, the kill path), player/take_damage, player/def/judge, the tune engine
(items/tune/apply -> fac -> apply_loop, disp_build -> fmt) and the tooltip builder (items/build_display -> build_lore)
run for real from the datapack in the vendored sims (HR/tests/lib, read only) through SR's helpers HR/sr/srsim.py.

    python3 test_hwamu.py <datapack root> [section ...] [-v]

  static   the def (PLAN §7.4.4 verbatim, model = api.ITEM_MODEL, vanilla item, engravings), register (call after
           moon_chalice, impl list), box_exclude, the codex label, items.md (8th mythic = the in-game text at ★★★, the
           등급 규칙 exception verbatim), both lore lines = w2 l.633 / l.411, the ★★★ line = w2 l.522, the hook lines of
           PLAN §7.4.6 in place, sounds f422-f429 (#k352-#k359, the §7.4.5 recipes, every id in sound_ids.txt), static
           rules (no negative add/remove literals, lowercase ids, glyph root empty + font named, no tip text)
  pools    never offered: byrar buckets (level-up picks / boxes / shop via items/pick_cand), 나무뿌리 byeng buckets; still
           in the codex's mythic list
  tune     the tune table at stars 0-3 = PLAN §7.4.3 (the real engine's exact rounding), the stat line, the tooltip
           numbers per star
  stacks   4 hits -> 1 stack, max 5, refresh on every gain, all drop after exactly #hwStkDur ticks, ATK % per stack,
           sidebar, the cues
  cost     HP cost 4 % of current above 50 %, none at <= 50 %, never below 1
  counter  on a landed hit (queued, never inside take_damage) and on a dodge / perfect parry (combat overhaul C:
           player/def/judge's pd / loose / par3), 2-s cooldown, nearest rlk_mob <= 12 b, no target = no cooldown, damage =
           atk x coef, Electro 1U, #sub itv 1; F3 (HR-09): never on burst / fall / revive i-frames (dashInvT, player/def/inv),
           a landed (killing) hit still queues; F3 (HR-39): an invulnerable body (rlk_mb_inv) is no target (no counter, no
           cooldown; the nearest other mob instead)
  low      crit dmg + only at HP <= 60 % (exact integer threshold)
  slash    only from on_cast_burst, ICD (+ ready cue), 4-t delay, every rlk_mob <= 20 b once, crit rate only if HP <= 50 %
           at the cast (for its duration), #sub itv 1, the vig title (font, empty root) skipped while vBig >= 1 (and
           while a subtitle line is up, ttlT >= 1)
  clear    sold / dropped: stacks, hits, timers, queues, crit time, sidebar cleared once; cooldowns kept
  run      F3 (HR-10): the per-run reset (player/reset_one -> hw_reset) clears the state AND the cooldowns: no stray ready cue
           at the next grant, the first burst of the next run slashes
  view     F3 (HR-08): vBig counts down once per tick in every state (view/tick, before the developer-mode return): the vig
           shows in developer mode (no avatar; the first-person mode is gone since 11-10) after a room title; F5 / the
           selection space / dead still one per tick (no double count)
  perf     commands per tick while held: idle, in combat (steady), peak
"""
import copy
import os
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
SECTIONS = ARGS[1:] or ['static', 'pools', 'tune', 'stacks', 'cost', 'counter', 'low', 'slash', 'clear', 'run', 'view', 'perf']
sys.path.insert(0, str(DP / 'tools'))
import mboss_scarlet.api as API  # noqa: E402

FN = DP / 'data/rlk/function'


# I1b (the suites moved to R:tools/dev/sim/hr/tests): the plan and the saved wiki page are read from $HR_DOCS, else from beside
# the suite (HR/ in the scratchpad: HR/PLAN.md, HR/wiki/w2.txt). The wiki is never committed (README 0-7: saved wiki pages
# stay out) and the plan joins tools/dev/sim/hr at the release: without them the checks against them are skipped (listed).
def _doc(rel):
    for base in ([Path(os.environ['HR_DOCS'])] if os.environ.get('HR_DOCS') else []) + [HERE.parent]:
        if (base / rel).is_file():
            return (base / rel).read_text(encoding='utf-8').split('\n')
    return None


PLAN, W2 = _doc('PLAN.md'), _doc('wiki/w2.txt')
SKIPPED = []


def has(doc, what):
    if doc is None:
        SKIPPED.append(what)
    return doc is not None
ID = API.ITEM_ID
N = [0]


def ck(name, ok, info=''):
    N[0] += 1
    if VERBOSE and ok:
        print('ok  ', name, info)
    return S.ck(name, ok, info)


def rd(rel):
    return (FN / (rel + '.mcfunction')).read_text(encoding='utf-8')


def b10(name):
    """A ★★★ base constant of F:items/tune/b10 (S5 retunes #hwCtrCdT / #hwSlCoef there; the checks follow it)."""
    return int(re.search(rf'scoreboard players set {name} tmp (\d+)', rd('items/tune/b10')).group(1))


def lines(rel):
    return [l for l in rd(rel).split('\n') if l.strip() and not l.lstrip().startswith('#')]


MY_NEW = sorted(p for p in (FN / 'items/proc').glob('hw_*.mcfunction')) + [FN / 'items/mythic/sword_hwamu/def.mcfunction'] \
    + [FN / f'snd/f{i}.mcfunction' for i in range(422, 430)]


def tick(s, pl, before=None):
    """One game tick of what the item uses: rlk:tick resets the sound keys, then player/tick (`before`: what char/tick
    does first, e.g. a burst cast) -> items/hook/tick_player (as the player, at the world origin: tick functions carry
    no position)."""
    s.t += 1
    for k in [k for k in s.scores if k[1] == 'snd']:
        del s.scores[k]
    if before:
        before()
    s.call('rlk:items/hook/tick_player', S.Ctx(pl, (0.0, 0.0, 0.0), (0.0, 0.0)))


def stat(s, pl, atkpct=0, critc=0, critd=150):
    P = ('e', pl.id)
    s.setsc(P, 'atkPct', atkpct)
    s.setsc(P, 'critChance', critc)
    s.setsc(P, 'critDamage', critd)
    s.call('rlk:items/hook/stat_buffs', S.pctx(s, pl))
    return s.sc(P, 'atkPct'), s.sc(P, 'critChance'), s.sc(P, 'critDamage')


def hit(s, pl, n=1):
    for _ in range(n):
        s.call('rlk:items/hook/on_hit', S.pctx(s, pl))


def hurt(s, pl, dmg=50, dash=0):
    P = ('e', pl.id)
    s.setsc(P, 'dashInvT', dash)
    s.setsc('#dmgIn', 'tmp', dmg)
    s.setsc(P, 'hurtLv', 1)
    s.setsc(P, 'hurtElem', 0)
    n0 = len(s.log)
    s.call('rlk:player/take_damage', S.Ctx(pl, (pl.pos[0], pl.pos[1] + 1.62, pl.pos[2]), tuple(pl.rot)))
    s.setsc(P, 'dashInvT', 0)
    return [l for l in s.log[n0:] if l[1] == 'apply']


def burst(s, pl):
    s.call('rlk:items/hook/on_cast_burst', S.pctx(s, pl))


def dash(s, pl):
    """A dodge (combat overhaul C): the stamp player/def/dodge_stamp writes (dgAt = now; no i-frames any more) and the item
    hook of player/dash_go (items/hook/on_dash; the other items' lines see no item, their scores 0)."""
    P = ('e', pl.id)
    for o in ('it_sword_kirion', 'it_pain_despair', 'it_kinetic_scale', 'it_crane_feather'):
        if s.sc(P, o) is None:
            s.setsc(P, o, 0)
    for o in ('parAt', 'parLk', 'parHit', 'dgRw'):
        if s.sc(P, o) is None:
            s.setsc(P, o, -1000000)
    s.setsc(P, 'dgAt', now(s))
    s.call('rlk:items/hook/on_dash', S.pctx(s, pl))


def now(s):
    return s.t + S.GT0


def applies(s, since):
    return [l for l in s.log[since:] if l[1] == 'apply']


def plan_block(start, end_prefix):
    i = next(k for k, l in enumerate(PLAN) if l.startswith(start))
    j = next(k for k in range(i + 1, len(PLAN)) if PLAN[k].startswith(end_prefix))
    return PLAN[i:j]


# ================================================================================================== static
def t_static():
    d = rd('items/mythic/sword_hwamu/def')
    body = [l for l in d.split('\n') if l.startswith('data modify storage rlk:items registry.sword_hwamu set value ')]
    ck('def: one registry line', len(body) == 1)
    reg = S.snbt_parse(body[0].split(' set value ', 1)[1])
    if has(PLAN, 'def = PLAN §7.4.4'):
        blk = plan_block('data modify storage rlk:items registry.sword_hwamu set value', 'data modify storage rlk:items ids append')
        plan_txt = (blk[0] + ''.join(l[1:] if l.startswith(' ') else l for l in blk[1:])).split(' set value ', 1)[1]
        # combat overhaul C (11-10): the dash became the dodge / parry; the lore line says so (the only change to PLAN's value)
        plan_v = S.snbt_parse(plan_txt.replace('공격을 받거나 대쉬로 흘려내면', '공격을 받거나 닷지 · 패링으로 흘려내면'))
        ck('def = PLAN §7.4.4 (whole registry value; 대쉬 -> 닷지 · 패링, combat overhaul C)', reg == plan_v)
    ck('def: vanilla item = api.ITEM_VANILLA', reg['item'] == API.ITEM_VANILLA, reg['item'])
    ck('def: model = api.ITEM_MODEL', reg['model'] == API.ITEM_MODEL, reg['model'])
    ck('def: name = api.ITEM_NAME', reg['name'] == API.ITEM_NAME)
    ck('def: mythic accessory, atkPct 25', reg['rarity'] == 'mythic' and reg['type'] == 'accessory' and reg['stats'] == {'atkPct': 25})
    ck('def: engravings berserk + keen', reg['engravings'] == ['berserk', 'keen'])
    ck('def: ids append', 'data modify storage rlk:items ids append value "sword_hwamu"' in d.split('\n'))
    ck('def: resource ids lowercase', all(x == x.lower() for x in (reg['item'], reg['model'])))
    # lore lines (desc) verbatim from the user's page
    ea = rd('items/enh_add')
    m = re.search(r'tellraw @a\[tag=player\] (\{.*\})$', ea, re.M)
    if has(W2, 'lore 1 / lore 2 / the ★★★ line = the saved wiki page w2'):
        l633, l411, l522 = W2[632], W2[410], W2[521]
        ck('lore 1 = w2 l.633 (its own sentence, verbatim)', l633.endswith(reg['desc'][0]) and reg['desc'][0].endswith('.'),
           reg['desc'][0])
        ck('lore 2 = w2 l.411 (her line, verbatim in quotes)', reg['desc'][1] == '“' + l411 + '”', reg['desc'][1])
        ck('★★★ line in enh_add = "[홍련] " + w2 l.522', bool(m) and S.render(S.snbt_parse(m.group(1))) == '[홍련] ' + l522)
    ck('★★★ line only on the step to 3 (before the cap)', ea.index('matches 3 if data storage rlk:tmp {eid:"sword_hwamu"}')
       < ea.index('execute if score #enh tmp matches 4.. run scoreboard players set #enh tmp 3'))
    # register / impl / box_exclude / codex
    r = rd('items/register').split('\n')
    i = r.index('function rlk:items/mythic/sword_hwamu/def')
    ck('register: def call after moon_chalice, before engr_assign',
       r.index('function rlk:items/mythic/moon_chalice/def') < i < r.index('function rlk:items/engr_assign'))
    impl = S.snbt_parse(next(l for l in r if l.startswith('data modify storage rlk:items impl set value')).split(' set value ', 1)[1])
    ck('register: impl lists sword_hwamu once', impl.count(ID) == 1 and len(impl) == 95, len(impl))
    bx = next(l for l in lines('items/build_rarbuckets') if 'box_exclude set value' in l)
    ck('box_exclude += sword_hwamu', S.snbt_parse(bx.split(' set value ', 1)[1]) == ['sword_kirion', 'demonomicon', ID])
    ck('codex label (one line, like 불씨의 맹약)', 'data modify storage rlk:codex lab.sword_hwamu set value {t:"화무십일홍",dy:"-0.632"}'
       in rd('codex/labels').split('\n'))
    # items.md
    md = (DP / 'items.md').read_text(encoding='utf-8')
    if has(PLAN, 'items.md: the 등급 규칙 exception = PLAN §7.4.1'):
        exc = re.search(r'「(예외\(사용자 요청 11-04\): 화무십일홍.*?)」', '\n'.join(PLAN)).group(1)
        ck('items.md: 등급 규칙 exception verbatim (PLAN §7.4.1)', md.count(exc) == 1)
    ck('items.md: mythic — 8개', '## mythic — 8개' in md and '## mythic — 7개' not in md)
    ent = md[md.index('8. 화무십일홍 `sword_hwamu`'):]
    el = ent.rstrip('\n').split('\n')
    i0 = next(k for k, l in enumerate(el) if l.startswith('    [ MYTHIC ]'))
    ind = [l[4:] if l.startswith('    ') else l for l in el[i0:]]          # blank lines stay '' (the lore's empty lines)
    s, pl = S.world(DP)
    eng = rd('engravings/register').split('\n')
    s.cache['rlk:srtest/eng'] = [l for l in eng if l.startswith('data modify storage rlk:engravings registry.')
                                 and ('.keen ' in l or '.berserk ' in l)]
    s.call('rlk:srtest/eng', S.C0)
    S.set_star(s, 3)
    s.storage['rlk:io'] = {'src': copy.deepcopy(s.storage['rlk:items']['registry'][ID]), 'id': ID}
    s.call('rlk:items/build_display', S.C0)
    game = ['[ MYTHIC ] 화무십일홍'] + [S.render(x) for x in s.storage['rlk:io']['lore']]
    ck('items.md mirror = in-game text at ★★★ (name + lore)', ind == game,
       '\n' + '\n'.join(f'{a!r} | {b!r}' for a, b in zip(ind, game) if a != b))
    ck('items.md: 참고 line names the source', '참고: 승리의 여신: 니케 홍련' in ent)
    # hook lines (PLAN §7.4.6)
    want = {
        'items/hook/on_hit': ['execute if score @s it_sword_hwamu matches 1.. run function rlk:items/proc/hw_hit'],
        'items/hook/stat_buffs': ['execute if score @s it_sword_hwamu matches 1.. run function rlk:items/proc/hw_stat'],
        'items/hook/tick_player': ['execute if score @s it_sword_hwamu matches 1.. run function rlk:items/proc/hw_tick',
                                   'execute unless score @s it_sword_hwamu matches 1.. if score #hwOn itv matches 1 run function rlk:items/proc/hw_clear'],
        'items/hook/on_cast_burst': ['execute if score @s it_sword_hwamu matches 1.. unless score #hwSlCd itv matches 1.. run function rlk:items/proc/hw_slash_q'],
        'player/take_damage': ['execute if score @s it_sword_hwamu matches 1.. if score #hurtDmg tmp matches 1.. unless score #hwCtrCd itv matches 1.. run function rlk:items/proc/hw_ctr_q'],
        # combat overhaul C (11-10): a dodge (perfect / loose) or a perfect parry flows the hit off (player/def/judge's branches);
        # the dash's own i-frame window (hw_dash) is gone with the dash; F3 (HR-10): the per-run reset
        'player/def/pd': ['execute if score @s it_sword_hwamu matches 1.. unless score #hwCtrCd itv matches 1.. run function rlk:items/proc/hw_ctr_q'],
        'player/def/loose': ['execute if score @s it_sword_hwamu matches 1.. unless score #hwCtrCd itv matches 1.. run function rlk:items/proc/hw_ctr_q'],
        'player/def/par3': ['execute if score @s it_sword_hwamu matches 1.. unless score #hwCtrCd itv matches 1.. run function rlk:items/proc/hw_ctr_q'],
        'player/def/inv': [],
        'items/hook/on_dash': [],
        'player/reset_one': ['function rlk:items/proc/hw_reset'],
    }
    for rel, ls in want.items():
        got = [l for l in lines(rel) if 'sword_hwamu' in l or '#hwOn' in l or 'proc/hw_' in l]
        ck(f'hook {rel}: exactly the PLAN §7.4.6 line(s)', got == ls, got)
    td = lines('player/take_damage')
    ck('take_damage: after the lion line (:37)', td[-1] == want['player/take_damage'][0] and 'lion_queue' in td[-2])
    for rel in ('player/def/pd', 'player/def/loose', 'player/def/par3'):
        di = lines(rel)
        ck(f'{rel}: sets #dodged 1 before the counter line', di.index('scoreboard players set #dodged tmp 1') < di.index(want[rel][0]))
    # sounds
    sid = set((DP / 'tools/dev/sim/rd/tests/sound_ids.txt').read_text(encoding='utf-8').split())
    recipes = {422: ('block.amethyst_block.chime', '0.45', '1.3'), 423: ('block.cherry_leaves.break', '0.4', '1.2'),
               424: ('entity.player.attack.sweep', '0.7', '1.4'), 425: ('block.amethyst_block.resonate', '0.4', '1.8'),
               426: ('entity.breeze.inhale', '0.6', '0.8'), 427: ('entity.player.attack.sweep', '1.0', '0.6'),
               428: ('entity.lightning_bolt.impact', '0.35', '1.7'), 429: ('block.chain.place', '0.4', '1.6')}
    ck('api.ITEM_SND = f422-f429', API.ITEM_SND == tuple(f'f{i}' for i in range(422, 430)))
    for i, (snd, vol, pit) in recipes.items():
        ls = lines(f'snd/f{i}')
        ok = ls == [f'scoreboard players set #k{i - 70} snd 1', f'playsound minecraft:{snd} master @a ~ ~ ~ {vol} {pit}']
        ck(f'snd/f{i}: key #k{i - 70} + the §7.4.5 recipe', ok, ls)
        ck(f'snd/f{i}: vanilla id in sound_ids.txt', snd in sid or 'minecraft:' + snd in sid)
    other = set()
    for p in sorted((FN / 'snd').glob('f*.mcfunction')):
        n = int(p.stem[1:])
        if n < 422 or n > 429:
            other |= set(re.findall(r'#k(\d+) snd', p.read_text(encoding='utf-8')))
    ck('keys #k352-#k359 used by no other wrapper', not (other & {str(k) for k in range(352, 360)}))
    # the item's procs call only its own wrappers; every wrapper is called
    procs = ''.join(p.read_text(encoding='utf-8') for p in sorted((FN / 'items/proc').glob('hw_*.mcfunction')))
    called = set(re.findall(r'rlk:snd/(f\d+)', procs))
    ck('procs use exactly f422-f429', called == {f'f{i}' for i in range(422, 430)}, sorted(called))
    for i in range(422, 430):
        ck(f'f{i} guarded by #k{i - 70}', f'unless score #k{i - 70} snd matches 1 run function rlk:snd/f{i}' in procs)
    # static rules on every new file and every added line
    added = []
    for p in MY_NEW:
        added += [(p.name, l) for l in p.read_text(encoding='utf-8').split('\n')]
    for rel in ('items/register', 'items/build_rarbuckets', 'items/tune/b10', 'items/hook/on_hit', 'items/hook/stat_buffs',
                'items/hook/tick_player', 'items/hook/on_cast_burst', 'items/enh_add', 'player/take_damage',
                'player/def/pd', 'player/def/loose', 'player/def/par3', 'codex/labels', 'items/hook/on_dash', 'player/reset_one'):
        added += [(rel, l) for l in rd(rel).split('\n') if 'hw' in l or 'sword_hwamu' in l]
    neg = [(f, l) for f, l in added if re.search(r'scoreboard players (add|remove) \S+ \S+ -', l)]
    ck('no negative literal in scoreboard players add/remove', not neg, neg)
    rid = [(f, x) for f, l in added for x in re.findall(r'\b(?:minecraft|rlk):[A-Za-z0-9_./-]+', l) if x != x.lower()]
    ck('resource ids lowercase', not rid, rid)
    parts = {x for f, l in added for x in re.findall(r'particle minecraft:([a-z_]+)', l)}
    ck('particles: vanilla ids', parts <= {'dust', 'cherry_leaves', 'electric_spark', 'sweep_attack'}, parts)
    q = rd('items/proc/hw_slash_q')
    tl = [l for l in q.split('\n') if ' run title @s title ' in l]
    ck('vig: one title line', len(tl) == 1)
    comp = S.snbt_parse(tl[0].split(' run title @s title ', 1)[1])
    ck('vig: root text empty and unstyled', set(comp) == {'text', 'extra'} and comp['text'] == '', comp)
    ck('vig: the glyph api.VIG in font api.FONT on the component',
       comp['extra'][0].get('text') == chr(API.VIG) and comp['extra'][0].get('font') == API.FONT, comp['extra'][0])
    shown = [l for f, l in added if re.search(r'\b(tellraw|title)\b', l) and not l.lstrip().startswith('#')]
    ck('on-screen text: only the vig title and the ★★★ line', len(shown) == 3, shown)
    # the tune table of b10 (names, modes) = PLAN §7.4.6
    b10 = rd('items/tune/b10')
    tline = next(l for l in b10.split('\n') if l.startswith('data modify storage rlk:tune t.sword_hwamu set value'))
    if has(PLAN, 't.sword_hwamu = PLAN §7.4.6'):
        want_t = re.search(r'`t\.sword_hwamu = (\[.*?\])`', '\n'.join(PLAN)).group(1)
        ck('t.sword_hwamu = PLAN §7.4.6', S.snbt_parse(tline.split(' set value ', 1)[1]) == S.snbt_parse(want_t))
    ck('ids append sword_hwamu in b10', 'data modify storage rlk:tune ids append value "sword_hwamu"' in b10.split('\n'))
    ck('b10: constants set unconditionally (before the tables)', b10.index('scoreboard players set #hwStkAtk tmp 6')
       < b10.index('data modify storage rlk:tune t.sword_kirion'))


# ================================================================================================== pools
def t_pools():
    s, pl = S.world(DP)
    s.call('rlk:items/mythic/ember_oath/def', S.C0)      # a pool mythic with the berserk engraving, for contrast
    s.storage['rlk:items']['ids'] = ['ember_oath', ID]
    s.call('rlk:items/build_rarbuckets', S.C0)
    br = s.storage['rlk:items']['byrar']
    ck('byrar: sword_hwamu in no bucket', all(ID not in v for v in br.values()), br)
    ck('byrar: ember_oath still in mythic', br['mythic'] == ['ember_oath'], br['mythic'])
    for rar in ('common', 'rare', 'epic', 'legendary', 'mythic'):
        s.call('rlk:items/pick_cand', S.C0, {'rar': rar})
        ck(f'pick_cand {rar} (level-up / box / shop candidates): no sword_hwamu', ID not in s.storage['rlk:pick']['cand'])
    s.call('rlk:engravings/byeng_build', S.C0)
    be = s.storage['rlk:engravings']['byeng']
    ck('나무뿌리 byeng: sword_hwamu in no engraving bucket', all(ID not in v for v in be.values()), be)
    ck('나무뿌리 byeng: ember_oath under berserk', 'ember_oath' in be.get('berserk', []))
    s.call('rlk:codex/lists', S.C0)
    ck('codex: still listed in the mythic tab', ID in s.storage['rlk:codex']['byrar']['mythic'], s.storage['rlk:codex']['byrar']['mythic'])


# ================================================================================================== tune
def plan_table():
    if not has(PLAN, 'tune: the PLAN §7.4.3 values per star (the engine rounding and the tooltip are still checked)'):
        return None
    rows = {}
    i = next(k for k, l in enumerate(PLAN) if l.startswith('#### 7.4.3'))
    for l in PLAN[i:i + 20]:
        m = re.match(r'^\| (?:stat `atkPct`|`(#hw\w+)`)[^|]*\| ([adc]) \|(.*)\|\s*$', l)
        if m:
            cells = [c.strip() for c in m.group(3).split('|')][:4]
            vals = [int(re.sub(r'[^\d]', '', re.match(r'^\+?([\d  ]+)', c).group(1))) for c in cells]
            rows[m.group(1) or 'atkPct'] = (m.group(2), vals)
    return rows


def t_tune():
    rows = plan_table()
    if rows is not None:
        ck('PLAN §7.4.3 table parsed (stat + 9 constants)', len(rows) == 10, sorted(rows))
    s, pl = S.world(DP)
    t = {e['n']: e['m'] for e in S.snbt_parse(next(l for l in rd('items/tune/b10').split('\n')
                                                  if 't.sword_hwamu set value' in l).split(' set value ', 1)[1])}
    for n, (m, vals) in (rows or {}).items():
        if n != 'atkPct':
            ck(f'{n}: mode {m} as PLAN', t.get(n) == m, t.get(n))
    names = [n for n in rows if n != 'atkPct'] if rows is not None else list(t)
    eng = rd('engravings/register').split('\n')
    s.cache['rlk:srtest/eng'] = [l for l in eng if l.startswith('data modify storage rlk:engravings registry.')
                                 and ('.keen ' in l or '.berserk ' in l)]
    s.call('rlk:srtest/eng', S.C0)
    fixed = {'#hwEvery': 4, '#hwStkMax': 5, '#hwCost': 4, '#hwFloor': 50, '#hwLowHp': 60, '#hwSlHp': 50, '#hwSlDelay': 4}
    for star in range(4):
        S.set_star(s, star)
        got = {n: s.sc(n, 'tmp') for n in names}
        if rows is not None:
            exp = {n: v[1][star] for n, v in rows.items() if n != 'atkPct'}
            ck(f'star {star}: the 9 constants = PLAN §7.4.3', got == exp, (got, exp))
        ck(f'star {star}: fixed constants unchanged', all(s.sc(n, 'tmp') == v for n, v in fixed.items()))
        # the engine's rounding (base x fac + 500) / 1000 reproduced independently
        fac = s.storage['rlk:tune']['fac'][star]
        base = {e['n']: e['b'] for e in s.storage['rlk:tune']['t'][ID]}
        ck(f'star {star}: = (base x fac + 500) / 1000', all(got[n] == (base[n] * fac[t[n]] + 500) // 1000 for n in got))
        s.storage['rlk:io'] = {'src': copy.deepcopy(s.storage['rlk:items']['registry'][ID]), 'id': ID}
        s.call('rlk:items/build_display', S.C0)
        lore = [S.render(x) for x in s.storage['rlk:io']['lore']]
        if rows is not None:
            ck(f'star {star}: stat line 공격력 +{rows["atkPct"][1][star]}%', lore[0] == f'공격력 +{rows["atkPct"][1][star]}%', lore[0])
        else:
            ck(f'star {star}: stat line 공격력 +N%', re.fullmatch(r'공격력 \+\d+%', lore[0]) is not None, lore[0])
        name = S.render(s.storage['rlk:io']['name'])
        ck(f'star {star}: name with stars', name == '[ MYTHIC ] 화무십일홍 ' + '★' * star + '☆' * (3 - star), name)
        ck(f'star {star}: name dark_red (mythic)', s.storage['rlk:io']['name'].get('color') == 'dark_red')
        sec = lambda v, p: (f'{v / 20:.{p}f}'.rstrip('0').rstrip('.') if p else str(round(v / 20)))  # noqa: E731
        want = [f'육참골단: 공격력 +{got["#hwStkAtk"]}% (최대 5중첩 · {sec(got["#hwStkDur"], 1)}초)',
                f'반격 피해: 공격력의 {got["#hwCtrCoef"]}% (12칸 · 쿨타임 {sec(got["#hwCtrCdT"], 1)}초)',
                f'치명타 피해 증가: {got["#hwLowCd"]}%',
                f'홍련일섬 피해: 공격력의 {got["#hwSlCoef"]}% (20칸 · 쿨타임 {sec(got["#hwSlCdT"], 0)}초)',
                f'치명타 확률 증가: {got["#hwSlCrit"]}% ({sec(got["#hwSlCritDur"], 1)}초)']
        ck(f'star {star}: tooltip numbers = the constants', all(w in lore for w in want),
           [w for w in want if w not in lore])
        ck(f'star {star}: model + vanilla item', s.storage['rlk:io']['model'] == API.ITEM_MODEL
           and s.storage['rlk:io']['item'] == API.ITEM_VANILLA)


# ================================================================================================== stacks
def t_stacks():
    for star in (3, 1):
        s, pl = S.world(DP, hp=1000)
        S.set_star(s, star)
        per, dur = s.sc('#hwStkAtk', 'tmp'), s.sc('#hwStkDur', 'tmp')
        hit(s, pl, 3)
        ck(f'★{star}: 3 hits -> no stack', (s.sc('#hwStk', 'itv') or 0) == 0)
        hit(s, pl, 1)
        ck(f'★{star}: 4th hit -> 1 stack, ends #hwStkDur ticks later', s.sc('#hwStk', 'itv') == 1
           and s.sc('#hwTEnd', 'itv') == now(s) + dur)
        ck(f'★{star}: sidebar 육참골단 = 1', s.sc('육참골단', 'stacks') == 1)
        ck(f'★{star}: ATK % = 1 x {per}', stat(s, pl)[0] == per)
        hit(s, pl, 4 * 9)
        ck(f'★{star}: max 5 stacks (40 hits)', s.sc('#hwStk', 'itv') == 5 and s.sc('육참골단', 'stacks') == 5)
        ck(f'★{star}: ATK % = 5 x {per}', stat(s, pl)[0] == 5 * per)
        for _ in range(dur - 10):
            tick(s, pl)
        hit(s, pl, 4)
        ck(f'★{star}: a gain refreshes the timer', s.sc('#hwTEnd', 'itv') == now(s) + dur and s.sc('#hwStk', 'itv') == 5)
        for _ in range(dur - 1):
            tick(s, pl)
        ck(f'★{star}: still 5 one tick before the end', s.sc('#hwStk', 'itv') == 5)
        tick(s, pl)
        ck(f'★{star}: all stacks drop after exactly #hwStkDur ticks', s.sc('#hwStk', 'itv') == 0 and s.sc('#hwAtk', 'itv') == 0)
        ck(f'★{star}: sidebar cleared at 0', s.sc('육참골단', 'stacks') is None)
        ck(f'★{star}: no ATK left', stat(s, pl)[0] == 0)
        n0 = len(s.log)
        hit(s, pl, 4)
        snd = [l[2] for l in s.log[n0:] if l[1] == 'call' and l[2].startswith('rlk:snd/')]
        ck(f'★{star}: gain cue f422 (not f423 below 5)', snd == ['rlk:snd/f422'], snd)
        for _ in range(4):
            tick(s, pl)
            hit(s, pl, 4)
        n0 = len(s.log)
        tick(s, pl)
        hit(s, pl, 4)
        snd = [l[2] for l in s.log[n0:] if l[1] == 'call' and l[2].startswith('rlk:snd/')]
        ck(f'★{star}: at 5 stacks + f423', snd == ['rlk:snd/f422', 'rlk:snd/f423'], snd)
    # only basic hits count: a counter / slash / hit taken never adds a stack
    s, pl = S.world(DP, hp=1000)
    S.set_star(s, 3)
    S.mob(s, (4.5, 64.0, 0.5))
    for _ in range(6):
        hurt(s, pl)
        tick(s, pl)
    burst(s, pl)
    for _ in range(8):
        tick(s, pl)
    ck('only basic hits count (counters / slash / hits taken: no stack)', (s.sc('#hwStk', 'itv') or 0) == 0
       and (s.sc('#hwHits', 'itv') or 0) == 0)


# ================================================================================================== cost
def t_cost():
    for cur, mx, after in ((1000, 1000, 960), (999, 1000, 960), (501, 1000, 481), (500, 1000, 500), (400, 1000, 400),
                           (1, 1000, 1), (3, 4, 3), (130, 200, 125), (51, 100, 49)):
        s, pl = S.world(DP)
        S.set_star(s, 3)
        P = ('e', pl.id)
        s.setsc(P, 'curHealth', cur)
        s.setsc(P, 'maxHealth', mx)
        hit(s, pl, 3)
        ck(f'no cost on hits 1-3 ({cur}/{mx})', s.sc(P, 'curHealth') == cur)
        hit(s, pl, 1)
        ck(f'{cur}/{mx} -> {after} (4 % of current while > 50 %)', s.sc(P, 'curHealth') == after, s.sc(P, 'curHealth'))
    # a long fight from full HP: parks just under half, never below 1, never paid at <= 50 %
    s, pl = S.world(DP)
    S.set_star(s, 3)
    P = ('e', pl.id)
    s.setsc(P, 'curHealth', 777)
    s.setsc(P, 'maxHealth', 777)
    seen = []
    for _ in range(400):
        before = s.sc(P, 'curHealth')
        hit(s, pl, 4)
        now = s.sc(P, 'curHealth')
        seen.append(now)
        if before * 100 <= 777 * 50:
            ck('no cost at <= 50 %', now == before, (before, now))
            break
        ck('cost = floor(4 % of current)', before - now == before * 4 // 100, (before, now))
    ck('never below 1 / parks under half', min(seen) >= 1 and seen[-1] * 100 <= 777 * 50, seen[-5:])
    ck('hw_cost subtracts with operation -= only', 'scoreboard players operation @s curHealth -= #hwA itv' in rd('items/proc/hw_cost')
       and not re.search(r'players remove @s curHealth', rd('items/proc/hw_cost')))


# ================================================================================================== counter
def t_counter():
    s, pl = S.world(DP, hp=2000, atk=100)
    S.set_star(s, 3)
    near, far, out = S.mob(s, (3.5, 64.0, 0.5)), S.mob(s, (8.5, 64.0, 0.5)), S.mob(s, (0.5, 64.0, 13.5))
    inside = hurt(s, pl)
    ck('landed hit: no damage inside take_damage (queued)', inside == [] and s.sc('#hwCtrQ', 'itv') == 1)
    n0 = len(s.log)
    tick(s, pl)
    ap = applies(s, n0)
    ck('counter next tick on the nearest rlk_mob', [a[2]['target'] for a in ap] == [near.id], ap)
    a = ap[0][2]
    ck('counter: atk x #hwCtrCoef % (before the level factor)', a['dmgBase'] == 100 * 138 // 100, a)
    ck('counter: Electro 1U, item damage (#sub itv 1), not a skill / stun hit',
       (a['elem'], a['elU'], a['sub'], a['skill'], a['stun'], a['icd']) == (3, 1000, 1, 0, 0, 1), a)
    ck('#sub itv back to 0', s.sc('#sub', 'itv') == 0)
    cdt = b10('#hwCtrCdT')        # S5: the b10 base (★★★)
    ck(f'cooldown = #hwCtrCdT ({cdt} t): flag 1 until now + {cdt}', s.sc('#hwCtrCd', 'itv') == 1 and s.sc('#hwCtrEnd', 'itv') == now(s) + cdt)
    snd = [l[2] for l in s.log[n0:] if l[1] == 'call' and l[2].startswith('rlk:snd/')]
    ck('counter sounds f424 + f425', snd == ['rlk:snd/f424', 'rlk:snd/f425'], snd)
    w = s.log[n0:]
    i_fx = next(k for k, l in enumerate(w) if l[1] == 'call' and l[2] == 'rlk:items/proc/hw_ctr_fx')
    i_ap = next(k for k, l in enumerate(w) if l[1] == 'apply')
    fx = [l[2] for l in w[i_fx:i_ap] if l[1] == 'particle']
    ck('counter fx at the target, before the damage (1 sweep + 6 lilac dust + sparks)',
       [f[0].split('{')[0] for f in fx] == ['minecraft:sweep_attack'] + ['minecraft:dust'] * 6 + ['minecraft:electric_spark']
       and all(abs(f[1][0] - near.pos[0]) < 0.01 for f in fx), fx)
    # cooldown: hits during it queue nothing; after it, again
    for k in range(cdt):
        hurt(s, pl)
        if k in (0, cdt - 1):
            ck(f'no queue during the cooldown (tick {k + 1})', s.sc('#hwCtrQ', 'itv') == 0)
        n0 = len(s.log)
        tick(s, pl)
        if applies(s, n0):
            ck('no counter during the cooldown', False, s.t)
            break
    ck(f'cooldown over after {cdt} ticks', s.sc('#hwCtrCd', 'itv') == 0)
    hurt(s, pl)
    n0 = len(s.log)
    tick(s, pl)
    ck('counter again after the cooldown', len(applies(s, n0)) == 1)
    # a dodge eats a hit -> counter, no HP lost (a dodge 3 ticks before: the loose window of a normal mob)
    s, pl = S.world(DP, hp=2000)
    S.set_star(s, 3)
    m = S.mob(s, (6.5, 64.0, 0.5))
    hp0 = s.sc(('e', pl.id), 'curHealth')
    dash(s, pl)
    s.t += 3
    inside = hurt(s, pl)
    ck('a dodge (3 t before, normal mob): hit dodged (no HP lost), counter queued', inside == [] and s.sc(('e', pl.id), 'curHealth') == hp0
       and s.sc('#hwCtrQ', 'itv') == 1 and s.sc('#dodged', 'tmp') == 1)
    n0 = len(s.log)
    tick(s, pl)
    ck('dodge counter next tick', [x[2]['target'] for x in applies(s, n0)] == [m.id])
    # the framework hazard path (mboss/hz/hurt_pm calls player/def/judge directly, boss class), a perfect dodge
    s, pl = S.world(DP, hp=2000)
    S.set_star(s, 3)
    S.mob(s, (6.5, 64.0, 0.5))
    dash(s, pl)
    s.setsc('#hcC', 'tmp', 2)
    s.setsc('#dodged', 'tmp', 0)
    s.call('rlk:player/def/judge', S.pctx(s, pl))
    ck('the judge alone (a hazard, perfect dodge) queues the counter', s.sc('#hwCtrQ', 'itv') == 1 and s.sc('#dodged', 'tmp') == 1)
    # no target within 12 b: no damage, no cooldown, queue cleared
    s, pl = S.world(DP, hp=2000)
    S.set_star(s, 3)
    S.mob(s, (12.6, 64.0, 0.5))
    S.mob(s, (0.5, 64.0, -12.7))
    hurt(s, pl)
    n0 = len(s.log)
    tick(s, pl)
    ck('no target <= 12 b: no counter, no cooldown, queue cleared', not applies(s, n0)
       and (s.sc('#hwCtrCd', 'itv') or 0) == 0 and s.sc('#hwCtrQ', 'itv') == 0)
    m = S.mob(s, (0.5, 64.0, 11.9))
    hurt(s, pl)
    n0 = len(s.log)
    tick(s, pl)
    ck('a mob at 11.9 b is countered', [x[2]['target'] for x in applies(s, n0)] == [m.id])
    # a non-mob never: entities without rlk_mob
    s, pl = S.world(DP, hp=2000)
    S.set_star(s, 3)
    S.mob(s, (2.5, 64.0, 0.5), tags=('rlk_room',))
    hurt(s, pl)
    n0 = len(s.log)
    tick(s, pl)
    ck('only rlk_mob entities are countered', not applies(s, n0))
    # without the item: nothing
    s, pl = S.world(DP, hp=2000)
    s.setsc(('e', pl.id), 'it_sword_hwamu', 0)
    S.mob(s, (2.5, 64.0, 0.5))
    hurt(s, pl)
    ck('without the item: no queue', (s.sc('#hwCtrQ', 'itv') or 0) == 0)
    # ★☆☆: coefficient and cooldown follow the star
    s, pl = S.world(DP, hp=2000, atk=100)
    S.set_star(s, 1)
    S.mob(s, (2.5, 64.0, 0.5))
    hurt(s, pl)
    n0 = len(s.log)
    tick(s, pl)
    ap = applies(s, n0)
    cd1 = (b10('#hwCtrCdT') * 1200 + 500) // 1000        # ★☆☆: the c factor 1.2 (F:items/tune/register), S5: 96 t
    ck(f'★☆☆: 92 % and cooldown {cd1} t', ap and ap[0][2]['dmgBase'] == 92 and s.sc('#hwCtrEnd', 'itv') == now(s) + cd1)
    # F3 (HR-09) under combat overhaul C: a dodge (perfect 0-2 t, loose 3-6 t vs a normal mob) counts; burst / fall / revive
    # i-frames (dashInvT) never do, and they take the hit first (player/def/judge: i-frames > dodge)
    for label, inv, dash_ago, rn, want in (
            ('burst wind-up i-frames (dashInvT 24, no dodge)', 24, None, 0, False),
            ('void-fall i-frames (dashInvT 20, no dodge)', 20, None, 0, False),
            ('downed Ronova (rnDie 60, dashInvT 80, no dodge)', 80, None, 60, False),
            ('a dodge 6 ticks ago (the last loose tick)', 0, 6, 0, True),
            ('a dodge 1 tick ago (perfect)', 0, 1, 0, True),
            ('a dodge this tick, burst i-frames on (the i-frames take it)', 24, 0, 0, False)):
        s, pl = S.world(DP, hp=2000)
        S.set_star(s, 3)
        S.mob(s, (4.5, 64.0, 0.5))
        P = ('e', pl.id)
        s.setsc(P, 'rnDie', rn)
        if dash_ago is not None:
            dash(s, pl)
            s.t += dash_ago
        hp0 = s.sc(P, 'curHealth')
        hurt(s, pl, dash=inv)
        q = s.sc('#hwCtrQ', 'itv') or 0
        n0 = len(s.log)
        tick(s, pl)
        got = applies(s, n0)
        ck(f'HR-09 dodge, {label}: hit eaten (no HP lost); counter {"queued + dealt" if want else "none, no cooldown"}',
           s.sc(P, 'curHealth') == hp0 and (q == 1 and len(got) == 1 if want
                                            else q == 0 and not got and (s.sc('#hwCtrCd', 'itv') or 0) == 0),
           (q, len(got), s.sc('#hwCtrCd', 'itv')))
    # the hazard path (mboss/hz/hurt_pm -> player/def/judge) under burst i-frames, no dodge: no counter
    s, pl = S.world(DP, hp=2000)
    S.set_star(s, 3)
    S.mob(s, (6.5, 64.0, 0.5))
    s.setsc(('e', pl.id), 'dashInvT', 24)
    s.setsc('#dodged', 'tmp', 0)
    s.call('rlk:player/def/judge', S.pctx(s, pl))
    ck('HR-09 hazard dodge under burst i-frames (no dodge): avoided, no queue', s.sc('#dodged', 'tmp') == 1
       and (s.sc('#hwCtrQ', 'itv') or 0) == 0)
    # a landed hit while downed (the killing blow that downed Ronova, rnDie set by then): still queues (as designed)
    s, pl = S.world(DP, hp=2000)
    S.set_star(s, 3)
    S.mob(s, (4.5, 64.0, 0.5))
    s.setsc(('e', pl.id), 'rnDie', 60)
    hurt(s, pl, dmg=50, dash=0)
    n0 = len(s.log)
    tick(s, pl)
    ck('HR-09 a landed hit (no i-frames) still queues and counters, also while downed', len(applies(s, n0)) == 1)
    # F3 (HR-39): an invulnerable body (rlk_mb_inv: her cutscenes / ghost / gauntlets) is no target
    s, pl = S.world(DP, hp=2000)
    S.set_star(s, 3)
    boss = S.mob(s, (2.5, 64.0, 0.5), tags=('rlk_mob', 'rlk_mb_body', 'rlk_mb_inv'))
    hurt(s, pl)
    n0 = len(s.log)
    tick(s, pl)
    ck('HR-39 only an invulnerable body in range: no counter (no fx, no damage), no cooldown, queue cleared',
       not applies(s, n0) and (s.sc('#hwCtrCd', 'itv') or 0) == 0 and s.sc('#hwCtrQ', 'itv') == 0
       and not [l for l in s.log[n0:] if l[1] == 'call' and l[2] == 'rlk:items/proc/hw_ctr_fx'], (applies(s, n0), s.sc('#hwCtrCd', 'itv')))
    other = S.mob(s, (7.5, 64.0, 0.5))
    hurt(s, pl)
    n0 = len(s.log)
    tick(s, pl)
    ck('HR-39 the invulnerable body nearer, a mob at 7 b: the counter hits the mob', [a[2]['target'] for a in applies(s, n0)] == [other.id],
       [a[2]['target'] for a in applies(s, n0)])
    boss.tags.discard('rlk_mb_inv')
    for _ in range(b10('#hwCtrCdT') + 20):        # past the counter's cooldown (S5: 80 t at ★★★)
        tick(s, pl)
    hurt(s, pl)
    n0 = len(s.log)
    tick(s, pl)
    ck('HR-39 the body hittable again (rlk_mb_inv gone): countered as the nearest', [a[2]['target'] for a in applies(s, n0)] == [boss.id])


# ================================================================================================== low
def t_low():
    for cur, mx, on in ((600, 1000, True), (601, 1000, False), (1, 1000, True), (1000, 1000, False), (60, 101, True),
                        (61, 101, False), (60, 100, True), (61, 100, False)):
        s, pl = S.world(DP)
        S.set_star(s, 3)
        P = ('e', pl.id)
        s.setsc(P, 'curHealth', cur)
        s.setsc(P, 'maxHealth', mx)
        cd = stat(s, pl)[2]
        ck(f'crit dmg {cur}/{mx}: {"+30" if on else "none"}', cd == (180 if on else 150), cd)
    s, pl = S.world(DP)
    S.set_star(s, 1)
    s.setsc(('e', pl.id), 'curHealth', 100)
    ck('★☆☆: +20 crit dmg', stat(s, pl)[2] == 170)
    # the low-HP pulse: 3 lilac dust every 20 t (10 stat calls)
    n0 = len(s.log)
    for _ in range(40):
        s.t += 1
        if s.t % 2 == 0:
            stat(s, pl)
    dust = [l for l in s.log[n0:] if l[1] == 'particle' and 'dust' in l[2][0]]
    ck('low HP pulse every 20 t', len(dust) == 2, len(dust))
    s.setsc(('e', pl.id), 'it_sword_hwamu', 0)
    ck('no crit dmg without the item', stat(s, pl)[2] == 150)


# ================================================================================================== slash
def t_slash():
    s, pl = S.world(DP, hp=2000, atk=100)
    S.set_star(s, 3)
    P = ('e', pl.id)
    ms = {d: S.mob(s, (0.5 + d, 64.0, 0.5)) for d in (5, 15, 19.9)}
    far = [S.mob(s, (0.5 + 20.5, 64.0, 0.5)), S.mob(s, (0.5, 64.0, 30.5))]
    deco = S.mob(s, (3.5, 64.0, 3.5), tags=('rlk_room',))
    hit(s, pl, 8)
    hurt(s, pl)
    tick(s, pl)
    ck('basic hits / counters never start the slash', (s.sc('#hwSlQ', 'itv') or 0) == 0 and (s.sc('#hwSlCd', 'itv') or 0) == 0)
    s.setsc(P, 'curHealth', 1500)
    n0 = len(s.log)
    tick(s, pl, before=lambda: burst(s, pl))       # cast in char/tick, before the item tick of the same tick
    t0 = s.t
    cast = [l for l in s.log[n0:] if l[0] == t0]
    ck('cast: cooldown = #hwSlCdT (flag until now + 800)', s.sc('#hwSlCd', 'itv') == 1 and s.sc('#hwSlEnd', 'itv') == now(s) + 800)
    ck('cast at 75 % HP: no crit time', (s.sc('#hwCritT', 'itv') or 0) == 0)
    ck('cast cue f426 + ring (12 dust)', [l[2] for l in cast if l[1] == 'call' and l[2].startswith('rlk:snd/')] == ['rlk:snd/f426']
       and sum(1 for l in cast if l[1] == 'particle' and 'dust' in l[2][0]) == 12)
    ttl = [l for l in cast if l[1] == 'title']
    ck('vig title (times + glyph) when vBig 0, then vBig 6', len(ttl) == 2 and s.sc(P, 'vBig') == 6, ttl)
    hit_t = None
    hits = []
    for k in range(10):
        n1 = len(s.log)
        tick(s, pl)
        ap = applies(s, n1)
        if ap and hit_t is None:
            hit_t, hits = s.t - t0, ap
    ck('slash 4 t after the cast', hit_t == 4, hit_t)
    tg = sorted(a[2]['target'] for a in hits)
    ck('every rlk_mob <= 20 b once (5 / 15 / 19.9 b), none beyond, no non-mob', tg == sorted(m.id for m in ms.values()), tg)
    slc = b10('#hwSlCoef')        # S5: the b10 base (★★★)
    ck(f'slash: atk x {slc} % (one roll for all)', all(a[2]['dmgBase'] == slc for a in hits) and len({a[2]['crit'] for a in hits}) == 1)
    ck('slash: Electro 1U, item damage (#sub itv 1)', all((a[2]['elem'], a[2]['elU'], a[2]['sub'], a[2]['skill']) == (3, 1000, 1, 0) for a in hits))
    ck('#sub itv back to 0', s.sc('#sub', 'itv') == 0)
    ck('far mobs untouched', all(s.sc(('e', m.id), 'mhpC') == 100000 for m in far) and s.sc(('e', deco.id), 'mhpC') == 100000)
    snd = [l[2] for l in s.log if l[1] == 'call' and l[2] in ('rlk:snd/f427', 'rlk:snd/f428')]
    ck('slash hit sounds f427 + f428 once', snd == ['rlk:snd/f427', 'rlk:snd/f428'], snd)
    fx = [l for l in s.log if l[1] == 'call' and l[2] == 'rlk:items/proc/hw_slash_fx']
    ck('per-target fx once each', len(fx) == 3)
    # ICD: a burst during the cooldown does nothing; the ready cue when it ends; then again
    n0 = len(s.log)
    burst(s, pl)
    end = s.sc('#hwSlEnd', 'itv')
    ck('burst during the ICD: no slash queued, end unchanged', (s.sc('#hwSlQ', 'itv') or 0) == 0 and s.sc('#hwSlEnd', 'itv') == end)
    left = end - now(s)
    for _ in range(left - 1):
        tick(s, pl)
    ck('no ready cue before the end', not [l for l in s.log[n0:] if l[1] == 'call' and l[2] == 'rlk:items/proc/hw_ready'])
    tick(s, pl)
    ck('ready cue (f429) the tick the ICD ends', s.sc('#hwSlCd', 'itv') == 0 and now(s) == end and [l[2] for l in s.log[n0:] if l[1] == 'call'
                                                                                   and l[2] == 'rlk:snd/f429'] == ['rlk:snd/f429'])
    for _ in range(5):
        tick(s, pl)
    ck('no applies during the whole ICD', not applies(s, n0))
    # crit rate: only if HP <= 50 % at the cast, for #hwSlCritDur, decided at the cast
    s.setsc(P, 'curHealth', 1000)
    s.setsc(P, 'vBig', 3)
    n0 = len(s.log)
    burst(s, pl)
    ck('vig skipped while vBig >= 1', not [l for l in s.log[n0:] if l[1] == 'title'] and s.sc(P, 'vBig') == 3)
    s5, pl5 = S.world(DP, hp=2000)
    S.set_star(s5, 3)
    s5.setsc(('e', pl5.id), 'ttlT', 30)
    burst(s5, pl5)
    ck('vig skipped while a subtitle line / notice is up (ttlT >= 1)', not [l for l in s5.log if l[1] == 'title']
       and s5.sc(('e', pl5.id), 'vBig') == 0 and s5.sc('#hwSlQ', 'itv') == 1)
    ck('cast at 50 %: crit time = #hwSlCritDur', s.sc('#hwCritT', 'itv') == 1 and s.sc('#hwCritEnd', 'itv') == now(s) + 200)
    ck('crit rate +20 while on', stat(s, pl)[1] == 20)
    s.setsc(P, 'curHealth', 2000)
    tick(s, pl)
    ck('healing after the cast keeps it', stat(s, pl)[1] == 20)
    for _ in range(198):
        tick(s, pl)
    ck('still on at the last tick', s.sc('#hwCritT', 'itv') == 1 and stat(s, pl)[1] == 20)
    tick(s, pl)
    ck('off after #hwSlCritDur ticks', s.sc('#hwCritT', 'itv') == 0 and stat(s, pl)[1] == 0)
    sp = [l for l in s.log if l[1] == 'particle' and l[2][0] == 'minecraft:electric_spark' and l[0] > s.t - 201]
    ck('crit time: sparks every 10 t (19 of them)', len([l for l in sp if l[0] < s.t]) >= 19)
    s2, pl2 = S.world(DP, hp=2000)
    S.set_star(s2, 3)
    s2.setsc(('e', pl2.id), 'curHealth', 1001)
    burst(s2, pl2)
    ck('cast at 50.05 %: no crit time', (s2.sc('#hwCritT', 'itv') or 0) == 0)
    # no mob in range: no damage, the cooldown still runs (the burst was used)
    s3, pl3 = S.world(DP, hp=2000)
    S.set_star(s3, 3)
    S.mob(s3, (25.5, 64.0, 0.5))
    burst(s3, pl3)
    n0 = len(s3.log)
    for _ in range(6):
        tick(s3, pl3)
    ck('no mob <= 20 b: no damage, ICD running', not applies(s3, n0) and s3.sc('#hwSlCd', 'itv') == 1
       and s3.sc('#hwSlEnd', 'itv') == now(s3) + 794)
    # without the item: nothing
    s4, pl4 = S.world(DP, hp=2000)
    s4.setsc(('e', pl4.id), 'it_sword_hwamu', 0)
    burst(s4, pl4)
    ck('without the item: no slash', (s4.sc('#hwSlQ', 'itv') or 0) == 0 and (s4.sc('#hwSlCd', 'itv') or 0) == 0)


# ================================================================================================== clear
def t_clear():
    s, pl = S.world(DP, hp=1000)
    S.set_star(s, 3)
    P = ('e', pl.id)
    S.mob(s, (3.5, 64.0, 0.5))
    s.setsc(P, 'curHealth', 400)
    hit(s, pl, 14)
    burst(s, pl)
    tick(s, pl)
    hurt(s, pl)
    ck('setup: stacks, hits, queue, crit time, sidebar',
       s.sc('#hwStk', 'itv') == 3 and s.sc('#hwHits', 'itv') == 2 and s.sc('#hwCtrQ', 'itv') == 1
       and s.sc('#hwSlQ', 'itv') >= 1 and s.sc('#hwCritT', 'itv') >= 1 and s.sc('육참골단', 'stacks') == 3)
    cds = tuple(s.sc(k, 'itv') for k in ('#hwSlCd', '#hwSlEnd', '#hwCtrCd', '#hwCtrEnd'))
    s.setsc(P, 'it_sword_hwamu', 0)              # sold / dropped: the inventory scan sets the count to 0
    n0 = len(s.log)
    tick(s, pl)
    ck('hw_clear once', [l[2] for l in s.log[n0:] if l[1] == 'call' and l[2].startswith('rlk:items/proc/hw_')] == ['rlk:items/proc/hw_clear'])
    ck('stacks / hits / queues / crit time cleared', all((s.sc(k, 'itv') or 0) == 0 for k in
                                                         ('#hwStk', '#hwAtk', '#hwHits', '#hwCtrQ', '#hwSlQ', '#hwCritT', '#hwPulse', '#hwOn')))
    ck('sidebar cleared', s.sc('육참골단', 'stacks') is None)
    ck('cooldowns kept (dropping does not reset the ICD)', tuple(s.sc(k, 'itv') for k in ('#hwSlCd', '#hwSlEnd', '#hwCtrCd', '#hwCtrEnd')) == cds, cds)
    n0 = len(s.log)
    for _ in range(5):
        tick(s, pl)
    ck('no further item calls while not held', not [l for l in s.log[n0:] if l[1] == 'call' and l[2].startswith('rlk:items/proc/hw_')]
       and not applies(s, n0))
    ck('no stats from the item while not held', stat(s, pl) == (0, 0, 150))
    s.setsc(P, 'it_sword_hwamu', 1)
    n0 = len(s.log)
    tick(s, pl)
    ck('picked up again before its end: the ICD continues', s.sc('#hwSlCd', 'itv') == 1 and s.sc('#hwSlEnd', 'itv') == cds[1])
    s.setsc(P, 'it_sword_hwamu', 0)
    for _ in range(cds[1] - now(s) + 5):
        tick(s, pl)
    ck('dropped past its end: still flagged while not held', s.sc('#hwSlCd', 'itv') == 1)
    s.setsc(P, 'it_sword_hwamu', 1)
    n0 = len(s.log)
    tick(s, pl)
    ck('picked up after its end: released at the first tick (ready cue)', s.sc('#hwSlCd', 'itv') == 0
       and 'rlk:snd/f429' in [l[2] for l in s.log[n0:] if l[1] == 'call'])


# ================================================================================================== run (F3, HR-10)
def reset_one(s, pl):
    """The real player/reset_one with its heavy calls (not this item) stubbed, as test_moon does; its own lines run."""
    for f in ('rlk:char/start_reset', 'rlk:lvup/exit', 'rlk:player/init', 'rlk:lvup/init', 'rlk:items/tune/reapply_all',
              'rlk:player/reset_stacks', 'rlk:element/infuse_end', 'rlk:items/equip_scan'):
        s.cache[f] = []
    s.call('rlk:player/reset_one', S.pctx(s, pl))


def t_run():
    s, pl = S.world(DP, hp=1000)
    S.set_star(s, 3)
    P = ('e', pl.id)
    S.mob(s, (3.5, 64.0, 0.5))
    s.setsc(P, 'curHealth', 400)
    hit(s, pl, 14)
    tick(s, pl, before=lambda: burst(s, pl))
    hurt(s, pl)
    tick(s, pl)
    ck('HR-10 setup: a burst and a counter in the last seconds of a run (both cooldowns on, stacks, sidebar)',
       s.sc('#hwSlCd', 'itv') == 1 and s.sc('#hwCtrCd', 'itv') == 1 and s.sc('#hwStk', 'itv') >= 1
       and s.sc('육참골단', 'stacks') is not None)
    s.setsc(P, 'it_sword_hwamu', 0)                    # the run ends: reset_one clears the inventory
    reset_one(s, pl)
    tick(s, pl)
    ck('HR-10 run reset (player/reset_one): both cooldowns, stacks, hits, queues, crit time and the sidebar cleared',
       all((s.sc(k, 'itv') or 0) == 0 for k in ('#hwSlCd', '#hwCtrCd', '#hwStk', '#hwAtk', '#hwHits', '#hwCtrQ', '#hwSlQ',
                                                '#hwCritT', '#hwPulse', '#hwOn'))
       and s.sc('육참골단', 'stacks') is None,
       {k: s.sc(k, 'itv') for k in ('#hwSlCd', '#hwCtrCd', '#hwStk', '#hwOn')})
    # (a) the next run's grant, 6000 t later: no stray ready cue on the first held tick
    for _ in range(6000):
        s.t += 1
    s.setsc(P, 'it_sword_hwamu', 1)
    n0 = len(s.log)
    tick(s, pl)
    ck('HR-10 the sword held again in the next run: no stray ready cue (no hw_ready, no f429)',
       not [l for l in s.log[n0:] if l[1] == 'call' and l[2] in ('rlk:items/proc/hw_ready', 'rlk:snd/f429')])
    # (b) the sword back soon after the reset (the lobby trial): the first burst slashes
    s2, pl2 = S.world(DP, hp=1000, atk=100)
    S.set_star(s2, 3)
    S.mob(s2, (5.5, 64.0, 0.5))
    tick(s2, pl2, before=lambda: burst(s2, pl2))
    s2.setsc(('e', pl2.id), 'it_sword_hwamu', 0)
    reset_one(s2, pl2)
    for _ in range(200):
        tick(s2, pl2)
    s2.setsc(('e', pl2.id), 'it_sword_hwamu', 1)
    S.set_star(s2, 3)
    tick(s2, pl2)
    n0 = len(s2.log)
    tick(s2, pl2, before=lambda: burst(s2, pl2))
    for _ in range(6):
        tick(s2, pl2)
    ck('HR-10 the sword back 200 t after a run reset: the first burst slashes (not swallowed by the old ICD)',
       [l for l in s2.log[n0:] if l[1] == 'call' and l[2] == 'rlk:items/proc/hw_slash'] and applies(s2, n0))
    # in-run drop / pick-up keeps its rule (hw_clear keeps the cooldowns): see the clear section


# ================================================================================================== view (F3, HR-08)
VIEW_STUBS = ('rlk:view/fresh', 'rlk:view/menu_do', 'rlk:view/burst_camera_tick', 'rlk:view/map_tick', 'rlk:view/fps_tick',
              'rlk:view/spawn', 'rlk:view/mob_aggro', 'rlk:view/move', 'rlk:view/sprint_fov', 'rlk:view/av_tick',
              'rlk:view/aim', 'rlk:view/slow', 'rlk:view/seat_new', 'rlk:view/ride_mount', 'rlk:view/xhair',
              'rlk:view/ride_off', 'rlk:boss/raiden/camera/hold')


def view_world(dev=0):
    """A player with the real view/tick (and its real ride_tick / hold / sel_xhair lines); the engine calls around the vBig
    lines are stubbed (the avatar, the camera seat, the crosshair title itself). The F5 view is the only view since the
    combat overhaul (11-10, lane R: no first-person mode, no shoulder view); dev=1 = developer mode, the no-avatar path
    (view/fps_tick). #on view 1 / #vmode view 2 are the constants load sets."""
    s, pl = S.world(DP, hp=1000)
    S.set_star(s, 3)
    for f in VIEW_STUBS:
        s.cache[f] = []
    # ride_tick's seat / mount lines (`on vehicle`, `ride`) are not in the sim: dropped; every other line runs as written
    s.cache['rlk:view/ride_tick'] = [l for l in rd('view/ride_tick').split('\n')
                                     if not re.search(r'\bon vehicle\b|(^|\brun )ride ', l)]
    s.setsc('#on', 'view', 1)
    s.setsc('#vmode', 'view', 2)
    s.setsc('#vFresh', 'view', 0)
    P = ('e', pl.id)
    for o, v in (('rdCam', 0), ('vMap', 0), ('devMode', dev), ('dead', 0), ('pkMode', 0), ('rlkMenu', 0), ('vTtp', 0),
                 ('ttlT', 0), ('vMapH', 0), ('vMapL', 0), ('vMapR', 0)):
        s.setsc(P, o, v)
    s.setsc('#spr', 'view', 0)
    s.setsc('#sprNow', 'view', 0)
    s.setsc('#t', 'view', 0)
    return s, pl


def view_ticks(s, pl, n):
    for _ in range(n):
        s.t += 1
        S.run_line(s, 'function rlk:view/tick', S.Ctx(pl, tuple(pl.pos), tuple(pl.rot)))


def t_view():
    fn_all = [(p.relative_to(FN).as_posix(), l) for p in FN.rglob('*.mcfunction')
              for l in p.read_text(encoding='utf-8').split('\n') if re.search(r'scoreboard players remove \S+ vBig 1', l)]
    vt = rd('view/tick').split('\n')
    dec = 'execute if score @s vBig matches 1.. run scoreboard players remove @s vBig 1'
    first_ret = next(i for i, l in enumerate(vt) if 'return run function rlk:view/fps_tick' in l)
    rets = [i for i, l in enumerate(vt) if ' return ' in l and 'rdCam' not in l]
    ck('HR-08 one vBig count-down in the whole pack: view/tick, before the developer-mode (no avatar) return and every other return '
       '(but the legacy rdCam line)', [f for f, _ in fn_all] == ['view/tick.mcfunction'] and dec in vt
       and vt.index(dec) < first_ret and all(vt.index(dec) < i for i in rets), fn_all)
    # developer mode (no avatar: the first-person path that is left): the room title's vBig 70 runs out; the next burst shows the vig
    s, pl = view_world(dev=1)
    P = ('e', pl.id)
    s.setsc(P, 'vBig', 70)                               # room/gen_title2 at a new map
    view_ticks(s, pl, 69)
    v69 = s.sc(P, 'vBig')
    view_ticks(s, pl, 1)
    ck('HR-08 developer mode: vBig 70 -> 1 after 69 ticks, 0 after 70 (one per tick)', v69 == 1 and s.sc(P, 'vBig') == 0, (v69, s.sc(P, 'vBig')))
    n0 = len(s.log)
    burst(s, pl)
    ttl = [l for l in s.log[n0:] if l[1] == 'title']
    ck('HR-08 developer mode: the burst after the room title shows the vig (times + glyph), vBig 6', len(ttl) == 2 and s.sc(P, 'vBig') == 6, ttl)
    view_ticks(s, pl, 6)
    ck('HR-08 developer mode: the vig\'s own vBig 6 runs out in 6 ticks', s.sc(P, 'vBig') == 0)
    # dead (F5): counted down too (the shoulder-view case went with the shoulder view, 11-10)
    for label, dead, pk in (('F5 while dead', 1, 0),):
        s, pl = view_world()
        P = ('e', pl.id)
        s.setsc(P, 'dead', dead)
        s.setsc(P, 'pkMode', pk)
        s.setsc(P, 'vBig', 30)
        view_ticks(s, pl, 10)
        ck(f'HR-08 {label}: vBig 30 -> 20 after 10 ticks', s.sc(P, 'vBig') == 20, s.sc(P, 'vBig'))
    # F5 (riding) and the selection space in F5: still exactly one per tick (no double count with the old ride_tick /
    # sel_xhair lines)
    for label, pk in (('F5', 0), ('F5 selection space (pkMode 1)', 1)):
        s, pl = view_world()
        P = ('e', pl.id)
        s.setsc(P, 'pkMode', pk)
        s.setsc(P, 'vBig', 30)
        s.setsc('#xh', 'view', 0)
        view_ticks(s, pl, 10)
        ck(f'HR-08 {label}: vBig 30 -> 20 after 10 ticks (one per tick)', s.sc(P, 'vBig') == 20, s.sc(P, 'vBig'))


# ================================================================================================== perf
def t_perf():
    tp = [l for l in lines('items/hook/tick_player') if 'sword_hwamu' in l]
    sb = [l for l in lines('items/hook/stat_buffs') if 'sword_hwamu' in l]
    ck('perf: the item lines (tick_player 2, stat_buffs 1)', len(tp) == 2 and len(sb) == 1)

    def run(s, pl, ticks, events=None):
        st, ln, peak = [], [], 0
        for k in range(ticks):
            s.t += 1
            for key in [key for key in s.scores if key[1] == 'snd']:
                del s.scores[key]
            if events:
                events(s, pl, k)
            a, b = s.n_strict, s.n_lines
            c0 = S.Ctx(pl, (0.0, 0.0, 0.0), (0.0, 0.0))
            for l in tp:
                S.run_line(s, l, c0)
            if k % 2 == 0:
                for l in sb:
                    S.run_line(s, l, S.pctx(s, pl))
            st.append(s.n_strict - a)
            ln.append(s.n_lines - b)
        return st, ln

    s, pl = S.world(DP, hp=1000)
    S.set_star(s, 3)
    st, ln = run(s, pl, 400)
    idle = (sum(st) / len(st), sum(ln) / len(ln))
    ck('perf idle (held, nothing running) <= 12 per tick', idle[0] <= 12, idle)
    # combat: 2.2 basic hits / s, a hit taken every 2 s, a burst at 1 s, HP drops under 60 %, 600 ticks (cast + 30 s)
    s, pl = S.world(DP, hp=1000)
    S.set_star(s, 3)
    for d in (3, 6, 9, 14):
        S.mob(s, (0.5 + d, 64.0, 0.5), hp=10 ** 8)
    s.setsc(('e', pl.id), 'curHealth', 700)

    def ev(s, pl, k):
        if k % 9 == 0:
            hit(s, pl)
        if k % 40 == 7:
            hurt(s, pl, dmg=20)
        if k == 20:
            burst(s, pl)

    st, ln = run(s, pl, 600, ev)
    strikes = sum(sum(v) for v in s.strike_cost.values())
    avg_all = sum(st) / len(st)
    avg = (sum(st) - strikes) / len(st)
    low = s.sc(('e', pl.id), 'curHealth') * 100 <= s.sc(('e', pl.id), 'maxHealth') * 60
    ck('perf combat: HP ended <= 60 % (the low-HP branch costed too)', low)
    ck('perf combat (timers / queues / stats, strikes apart) <= 12 per tick (strict count)', avg <= 12, avg)
    PERF.update(idle_strict=round(idle[0], 2), idle_lines=round(idle[1], 2), combat_strict=round(avg, 2),
                combat_with_strikes_strict=round(avg_all, 2), combat_lines=round(sum(ln) / len(ln), 2),
                counter_strike=sorted(set(s.strike_cost.get('rlk:items/proc/hw_ctr', []))),
                slash_strike=s.strike_cost.get('rlk:items/proc/hw_slash', []), peak_strict=max(st))


PERF = {}

if __name__ == '__main__':
    for sec in SECTIONS:
        globals()['t_' + sec]()
    if PERF:
        print('perf (commands per tick while held):', PERF)
    if SKIPPED:
        print(f'SKIPPED (no PLAN.md / wiki/w2.txt in $HR_DOCS or beside the suite): {len(SKIPPED)} group(s):', '; '.join(SKIPPED))
    sys.exit(S.summary('test_hwamu', N[0]))
