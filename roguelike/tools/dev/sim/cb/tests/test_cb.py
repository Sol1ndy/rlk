#!/usr/bin/env python3
"""test_cb.py: the combat overhaul's lane C (parry on F, the dodge, the damage context, unparriable attacks) against one
datapack root (read only).

    python3 test_cb.py <datapack root> [section ...]
      sections: static input judge tiers dodge context energy cd bal boss near raiden readers fx cost   (default: all)

  static   the dash charges / HUD gauge / dash_iframe / hurt_nd are gone; dashInvT is written only by the non-dodge
           i-frames; the tick order (the input pre-pass before view/tick, player/tick, the cm worlds, Raiden, the bosses;
           the dodge-start box around the cm worlds); lores and the tutorial say 닷지 / 패링, no 대쉬; the generated
           framework lines (np_def's rule, the glint, hurt_ctx, hz/hit_near, pj/step_n, hurt_pm's judge) and Raiden's land
  input    the real F path (player/def/input -> f_key -> press): an accepted press stamps parAt = now and locks #parGap;
           presses inside the lockout only push it (now + #parRe: mashing and a held key never press again); refusals
           (map, selection, dead, burst cast, Ronova revival, Raiden camera); Shift+F is not a parry; a right-click on
           the eye shield is consumed by the pre-pass (dodge in the same tick) and the dodge cooldown / no charges
  judge    the order i-frames > perfect dodge > perfect parry > loose dodge > tier 2 > tier 1 > hit, the outputs
           (#dodged / #parT / #pdg), the one-shot context reset, no-dodge (ignores dodges and i-frames), no-parry
  tiers    the real hit (cm/hit_me -> cm/hit_pl -> hit_pl2 -> take_damage) with F pressed 0..12 t before the hit: tier 3
           at 0-2 t (no damage), tier 2 at 3-5 t (20 % kept), tier 1 at 6-9 t (50 % kept), none at 10+; one press parries
           every hit of one tick, then it is spent; no knockback / hurt flash on a parry
  dodge    perfect 0-2 t for every class; loose 3-6 t for normal and elite, not for bosses; 7+ nothing
  context  cm brain / projectile (owner by cmId) / elite class / Raiden / the boss framework (hurt_ctx: boss body) /
           vanilla (ctx_va): attacker tag rlk_hc_atk, class, kind; the tag never outlives the judge
  energy   +10 pt (1000) once per dodge (a second hit in the same window gives none), clamped at the burst cost, 스커크
           in 일곱빛 섬광 gets none
  cd       char/cd_cut: -20 t on skillCd (clamped at 0), 나비아 / 네페르 advance the charge timer (nvCT / nfCT) only while
           a charge is missing; a perfect parry calls it once per press and rlk:bal/hit {n:1} on the attacker
  bal      lane B's real gauge: a perfect parry on a strike takes exactly one pip from the attacker (cm brain, a
           projectile's owner, an elite, a boss body), once per press; tiers 1-2 / a dodge / an unparriable attack take
           none; a groggy enemy or a boss that refuses balance keeps its pips while the parry still works
  boss     hz/np_def per shape and option, pj/launch's no-parry, hurt_dodge's #mbDodgeOk (perfect dodge / perfect parry
           only), hz/hurt_pm through the judge (a perfect dodge avoids; a parry does not), np_glint spacing / #mbNpOwn
  near     the perfect-window re-test at the dodge's start: a disc hazard that misses the moved body but covers the dodge
           start is a perfect dodge (no damage, reward); a no-dodge hazard is never re-tested; outside the window nothing
  raiden   land: kind / no-parry context, land_nd = #hcND (no dashInvT juggling), no knockback when parried
  readers  화무십일홍 (queued by a dodge / perfect parry, not by i-frames), 홍련 pips (q_pf0 / q_pf1), the shield rush
           ends on a perfect parry, Apep's parried bolt ends, the item hooks, the tutorial counter
  fx       each tier's effects (star glyph text_display, overlays only when no other big title / bottom line is up),
           the perfect dodge's red ghost and wash, the effect entities age out
  cost     the pre-pass costs a handful of commands per idle tick

Harness: lib/psim.py + lib/mcsim.py (lane R's vendored harness) with gametime (`time query gametime` = s.gt) and a call log.
Prints one line per check; exit 1 on any failure. Run it from a copy outside the datapack (tools/dev/sim/README.md 1).
"""
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
from psim import PSim, Ent, Ctx, pctx  # noqa: E402

ARGS = [a for a in sys.argv[1:] if not a.startswith('-')]
DP = Path(ARGS[0]).resolve()
ONLY = set(ARGS[1:])
FN = DP / 'data/rlk/function'
TOOLS = DP / 'tools'
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


def code(text):
    return [l for l in (text or '').split('\n') if l.strip() and not l.lstrip().startswith('#')]


# ================================================================================================== the harness
class CSim(PSim):
    def __init__(self, root):
        super().__init__(root)
        self.gt = 100000
        self.log = []                    # (fid, executor tags, macro) of the watched functions
        self.watch = {'rlk:bal/hit', 'rlk:items/proc/hw_ctr_q', 'rlk:player/def/fx/p3', 'rlk:player/def/fx/p2',
                      'rlk:player/def/fx/p1', 'rlk:player/def/fx/pd', 'rlk:player/knockback/start', 'rlk:cm/hurt_fx',
                      'rlk:char/cd_cut', 'rlk:items/hook/on_parry', 'rlk:items/hook/on_pdodge', 'rlk:player/dash_go',
                      'rlk:player/def/fx/glint', 'rlk:char/motion/guard', 'rlk:mboss/hurt_dodge'}
        self.titles = []

    def cmd(self, t, ctx):
        if t[:3] == ['time', 'query', 'gametime']:
            self.n += 1
            return self.gt
        if t[0] == 'title':
            self.titles.append(' '.join(t[1:]))
        if t[:3] == ['data', 'remove', 'entity'] and len(t) == 5 and re.fullmatch(r'[A-Za-z_]+', t[4]):
            self.n += 1
            for e in (self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]):
                e.data.pop(t[4], None)
            return 1
        return super().cmd(t, ctx)

    def call(self, fid, ctx, macro=None):
        if fid in self.watch:
            self.log.append((fid, sorted(ctx.ex.tags) if ctx.ex is not None else None, macro))
        return super().call(fid, ctx, macro)

    def calls(self, fid):
        return [c for c in self.log if c[0] == fid]


def world():
    s = CSim(FN)
    pl = Ent('player', (0.5, 64.0, 0.5), (0.0, 0.0), ['player', 'rlk_body'])
    s.ents.append(pl)
    s.player = pl
    s.call('rlk:load', Ctx(None, (0, 0, 0), (0, 0)))
    for _ in range(5):
        s.t += 1
        s.gt += 1
        s.call('rlk:player/tick', pctx(s))
    for o in ('dashInvT', 'dashCool', 'dashMoveT'):
        s.setsc(('e', pl.id), o, 0)
    full(s)
    return s, pl


def full(s):
    pl = s.player
    s.setsc(('e', pl.id), 'curHealth', s.sc(('e', pl.id), 'maxHealth') or 1000)
    for o in ('shieldHP', 'gShield', 'dead', 'buT', 'rnDie', 'pkMode', 'vMap', 'rdCam', 'pmMoveLock'):
        s.setsc(('e', pl.id), o, 0)


def P(s, o, v=None):
    pl = s.player
    if v is None:
        return s.sc(('e', pl.id), o)
    s.setsc(('e', pl.id), o, v)


def G(s, name, obj='tmp'):
    return s.sc(name, obj)


def brain(s, tags=(), pos=(2.5, 64.0, 0.5), cid=7):
    e = Ent('husk', pos, (90.0, 0.0), ['rlk_cmb', 'rlk_mob', 'rlk_cm_sw'] + list(tags))
    s.ents.append(e)
    s.setsc(('e', e.id), 'mlv', 1)
    s.setsc(('e', e.id), 'cmId', cid)
    return e


def press(s, ago):
    """the F press `ago` ticks before now (the stamp the real press writes; input tests use the real path)"""
    P(s, 'parAt', s.gt - ago)
    P(s, 'parLk', s.gt - ago + 12)
    P(s, 'parHit', -1000000)


def dodge(s, ago):
    P(s, 'dgAt', s.gt - ago)
    P(s, 'dgRw', -1000000)


def nopress(s):
    P(s, 'parAt', -1000000)
    P(s, 'parHit', -1000000)
    P(s, 'dgAt', -1000000)
    P(s, 'dgRw', -1000000)


def cm_hit(s, e, dmg=40):
    """a real custom-mob melee hit: cm/hit_me as the brain (#cmDmg) -> cm/hit_pl -> hit_pl2 -> take_damage"""
    full(s)
    hp0 = P(s, 'curHealth')
    s.setsc('#cmDmg', 'tmp', dmg)
    s.log.clear()
    s.call('rlk:cm/hit_me', Ctx(e, tuple(e.pos), tuple(e.rot)))
    return hp0 - P(s, 'curHealth')


def judge(s, K=1, C=0, NP=0, ND=0):
    s.setsc('#hcK', 'tmp', K)
    s.setsc('#hcC', 'tmp', C)
    s.setsc('#hcNP', 'tmp', NP)
    s.setsc('#hcND', 'tmp', ND)
    s.setsc('#dodged', 'tmp', 0)
    s.log.clear()
    s.call('rlk:player/def/judge', pctx(s))
    return G(s, '#dodged'), G(s, '#parT'), G(s, '#pdg')


def run(name):
    return not ONLY or name in ONLY


# ================================================================================================== static
def t_static():
    fns = {p.relative_to(FN).as_posix()[:-len('.mcfunction')]: p.read_text(encoding='utf-8') for p in FN.rglob('*.mcfunction')}
    gone = ('player/dash_regen', 'player/dash_refill', 'player/dash_iframe', 'player/hud/build', 'player/hud/build_slot',
            'player/hud/part', 'mboss/hurt_nd', 'items/proc/hw_dash')
    ck('static: the dash charge / gauge / i-frame files and mboss/hurt_nd are gone', not [g for g in gone if g in fns],
       [g for g in gone if g in fns])
    bad = [k for k, v in fns.items() if k != 'uninstall' and re.search(r'\b(dashCharge|dashRegen|#dashMax|#dashRegenT|#hudSeg|hudKey|hwDashEnd)\b', '\n'.join(code(v)))]
    ck('static: nothing reads the dash charges, the gauge or the hwamu dash stamp (uninstall still removes the old objectives)', not bad, bad[:8])
    writers = sorted(k for k, v in fns.items() for l in code(v) if re.search(r'scoreboard players (set|operation) \S+ dashInvT (?!=)', l)
                     or re.search(r'scoreboard players set \S+ dashInvT \d', l))
    ok_w = {'char/burst_wind', 'char/motion/events/navia/burst', 'char/motion/events/skirk/burst_jin',
            'char/motion/events/skirk/burst_metsu', 'char/motion/events/arle/burst', 'char/ronova/revive', 'room/fall/player',
            'player/init', 'mboss/pl_dot2'}
    ck('static: dashInvT is written only by the non-dodge i-frames (burst, revive, fall), init and pl_dot2', set(writers) <= ok_w,
       sorted(set(writers) - ok_w))
    ck('static: player/dash_go writes no i-frames (the dodge stamp instead)', 'dashInvT' not in '\n'.join(code(fns['player/dash_go']))
       and 'function rlk:player/def/dodge_stamp' in fns['player/dash_go'])
    tick = code(fns['tick'])
    idx = lambda pat: next((i for i, l in enumerate(tick) if pat in l), -1)  # noqa: E731
    i_in, i_view, i_pt, i_cm, i_rd, i_mb = (idx('player/def/input'), idx('function rlk:view/tick'), idx('function rlk:player/tick'),
                                             idx('function rlk:cm/world'), idx('boss/raiden/world'), idx('mboss/main'))
    ck('static: rlk:tick runs the input pre-pass before view/tick, player/tick, the cm worlds, Raiden and the bosses',
       -1 < i_in < i_view < i_pt < i_cm < i_rd < i_mb, (i_in, i_view, i_pt, i_cm, i_rd, i_mb))
    i_on, i_off, i_pj = idx('player/def/ghost_on'), idx('player/def/ghost_off'), idx('function rlk:cm/pj/world')
    ck('static: the dodge-start box replaces the body around cm/world and cm/pj/world only while the window is open',
       i_on < i_cm < i_pj < i_off < i_rd and '#dgOpen cb matches 1' in tick[i_on] and '#dgOpen cb matches 1' in tick[i_off])
    ck('static: the player/hotbar/tick F line is gone (F = player/def/input -> player/f_key), Shift+F stays',
       'player/f_key' not in '\n'.join(code(fns['player/hotbar/tick'])) and fns['player/hotbar/tick'].count('lvup/toggle') == 2)
    ck('static: view/ride_tick no longer handles rcU (the pre-pass does)', 'rc_hold' not in '\n'.join(code(fns['view/ride_tick']))
       and 'player/def/rc' in fns['player/def/input'] and 'combat/rc_hold' in fns['player/def/rc'])
    hud = fns['player/hud/tick']
    ck('static: the HUD actionbar has no dash gauge', 'line[]' not in hud and 'dashRegen' not in hud)
    lores = [k for k in fns if re.match(r'char/[a-z]+/def$', k)]
    ck('static: all 7 weapon lores say 우클릭 · 닷지 and F 키 · 패링 (no 대쉬)', len(lores) == 7 and all(
        '우클릭 · 닷지' in fns[k] and 'F 키 · 패링' in fns[k] and '대쉬' not in fns[k] for k in lores), lores)
    user = [k for k, v in fns.items() if ('대쉬' in '\n'.join(l for l in v.split('\n') if not l.lstrip().startswith('#')))
            and not k.startswith(('player/def', 'load'))]
    ck('static: no user-facing text says 대쉬 any more', not user, user[:8])
    ck('static: the tutorial step 1 is 이동 · 닷지 · 패링 (target 닷지 · 패링 3번)', '이동 · 닷지 · 패링' in fns['lobby/tut/s1']
       and '닷지 · 패링 3번 하기' in fns['lobby/tut/s1'])
    ck('static: 질주 (2) = 닷지 재사용 대기 -20 % (lore and engravings/scan_more)', '닷지 재사용 대기 ' in fns['engravings/register']
       and '#dashCoolBase' in fns['engravings/scan_more'])
    ck('static: 화무십일홍 lore: 닷지 · 패링으로 흘려내면', '닷지 · 패링으로 흘려내면' in fns['items/mythic/sword_hwamu/def'])
    # generated framework lines
    npd = fns.get('mboss/hz/np_def', '')
    ck('static: hz/np_def: no-dodge, per mille, re-arm, ring, full / mask, disc >= 4.5 b, sector / line >= 8 b',
       all(x in npd for x in ('mbHzND matches 1 run return 0', 'mbHzPm matches 1.. run return 0', 'mbHzRA matches 1.. run return 0',
                              'mbHzK matches 1 if score @s mbHzR matches ..4499 run return run scoreboard players set @s mbHzNP 0',
                              'mbHzK matches 3..4 if score @s mbHzR matches ..7999 run return run scoreboard players set @s mbHzNP 0'))
       and npd.split('\n').index('scoreboard players set @s mbHzNP 1') < npd.split('\n').index('execute if score @s mbHzND matches 1 run return 0'))
    ck('static: hz/init sets mbHzNP from #hzNoParry or np_def and flashes np_glint for a real hit',
       'mbHzNP = #hzNoParry mb' in fns['mboss/hz/init'] and 'mboss/np_glint' in fns['mboss/hz/init'])
    ck('static: opts_reset resets #hzNoParry / #pjNoParry to -1', 'set #hzNoParry mb -1' in fns['mboss/opts_reset']
       and 'set #pjNoParry mb -1' in fns['mboss/opts_reset'])
    ck('static: mboss/hurt -> hurt_ctx -> cm/hit_pl2 (one path; no zero-and-restore of dashInvT)',
       'function rlk:mboss/hurt_ctx' in fns['mboss/hurt'] and 'hurt_nd' not in fns['mboss/hurt'] and 'dashInvT' not in fns['mboss/hurt'])
    ck('static: hz/hurt_pm calls the judge (no own dash check)', 'player/def/judge' in fns['mboss/hz/hurt_pm']
       and 'dashInvT' not in fns['mboss/hz/hurt_pm'])
    near = [l for l in tick if 'mboss/near_all' in l]
    ck('static: rlk:tick runs mboss/near_all right after mboss/main, only in the window (live, not paused); hz/near and pj/near '
       'are dodgeable-only; mboss/world, hz/all, pj/all and pj/tick carry no lane C line',
       len(near) == 1 and tick.index(near[0]) == i_mb + 1 and '#dgOpen cb matches 1' in near[0] and '#mbPause mb matches 1' in near[0]
       and 'mboss/hz/near' in fns['mboss/near_all'] and 'mboss/pj/near' in fns['mboss/near_all']
       and 'unless score @s mbHzND matches 0 run return 0' in fns['mboss/hz/near']
       and 'unless score @s mbPjND matches 0 run return 0' in fns['mboss/pj/near']
       and not any(x in fns[f] for f in ('mboss/world', 'mboss/hz/all', 'mboss/pj/all', 'mboss/pj/tick') for x in ('dgOpen', 'near')))
    ck('static: Raiden land sets the context, land_nd = #hcND 1 without dashInvT, try re-tests at the dodge start',
       '#hcNP tmp 1' in fns['boss/raiden/hazard/land'] and 'dashInvT' not in fns['boss/raiden/hazard/land_nd']
       and '#hcND tmp 1' in fns['boss/raiden/hazard/land_nd'] and 'hazard/try_near' in fns['boss/raiden/hazard/try'])
    ck('static: rlk:bal/hit is lane B\'s (takes #n bal through bal/take) and the perfect parry calls it as the attacker',
       'function rlk:bal/take' in fns.get('bal/hit', '')
       and 'execute as @e[tag=rlk_hc_atk,limit=1] run function rlk:bal/hit {n:1}' in fns['player/def/par3_go'])
    ck('static: the guard clip exists for the three rig characters', all(f'char/motion/clips/{c}/guard/start' in fns
       for c in ('arle', 'skirk', 'navia')) and fns.get('char/motion/guard', '').count('clip:"guard"') == 3)
    gl = fns.get('player/def/fx/g/glint', '') + fns.get('player/def/fx/g/t_streak', '')
    ck('static: the glyph commands name the font rlk:cb on every component with an empty root', 'font:"rlk:cb"' in gl
       and '{text:"",extra:[' in gl)


# ================================================================================================== input
def t_input():
    s, pl = world()
    inv = s.inv_of(pl)
    UI = {'id': 'minecraft:stick', 'count': 1, 'c': {'minecraft:custom_data': {'rlk_ui': {'role': 'attack'}}}}
    nopress(s)
    P(s, 'parLk', -1000000)
    s.setsc('#now', 'cb', s.gt)

    def f(sneak=0):
        inv['weapon.offhand'] = dict(UI)
        P(s, 'sneakT', sneak)
        s.setsc('#now', 'cb', s.gt)
        s.log.clear()
        s.call('rlk:player/def/input', pctx(s))
        inv.pop('weapon.offhand', None)
    f()
    ck('input: F (offhand UI item, no sneak) -> parAt = now, lock until now + #parGap', P(s, 'parAt') == s.gt
       and P(s, 'parLk') == s.gt + G(s, '#parGap'), (P(s, 'parAt'), P(s, 'parLk')))
    ck('input: the press plays the guard (char/motion/guard)', bool(s.calls('rlk:char/motion/guard')))
    t0 = s.gt
    s.gt += 3
    f()
    ck('input: a press inside the lockout is ignored (parAt kept) and pushes the lock to now + #parRe at least',
       P(s, 'parAt') == t0 and P(s, 'parLk') == max(t0 + G(s, '#parGap'), s.gt + G(s, '#parRe')))
    # mash every 3 ticks: never accepted again
    acc = 0
    for _ in range(12):
        s.gt += 3
        before = P(s, 'parAt')
        f()
        acc += P(s, 'parAt') != before
    ck('input: mashing F every 3 t (or a held key repeating) is never accepted again', acc == 0)
    s.gt += 40
    f()
    ck('input: after a pause longer than the lock, F is accepted again', P(s, 'parAt') == s.gt)
    for o, v in (('vMap', 1), ('pkMode', 1), ('dead', 1), ('buT', 5), ('rnDie', 3), ('rdCam', 1), ('pmMoveLock', 1)):
        s.gt += 40
        P(s, o, v)
        before = P(s, 'parAt')
        f()
        ck(f'input: refused while {o} {v}', P(s, 'parAt') == before)
        P(s, o, 0)
    s.gt += 40
    before = P(s, 'parAt')
    f(sneak=1)
    ck('input: Shift+F (sneakT >= 1) is not a parry (player/hotbar/tick keeps lvup/toggle)', P(s, 'parAt') == before)
    # right-click on the eye shield, consumed by the pre-pass: the dodge starts in this tick
    s.gt += 40
    P(s, 'dashCool', 0)
    sh = Ent('interaction', (0.5, 65.6, 0.8), (0.0, 0.0), ['atkBlock'])
    sh.data['interaction'] = {'timestamp': s.gt}
    s.ents.append(sh)
    inv['hotbar.0'] = dict(UI)
    s.call('rlk:player/def/input', pctx(s))
    ck('input: a right-click on the eye shield is consumed by the pre-pass and dodges in the same tick (dgAt = now)',
       'interaction' not in sh.data and P(s, 'dgAt') == s.gt and P(s, 'dashCool') == G(s, '#dashCoolT'),
       (sh.data, P(s, 'dgAt'), s.gt))
    ck('input: the dodge leaves its start box rlk_dgo and opens the window (#dgEnd = now + 2)',
       len(s.select('@e[tag=rlk_dgo]', pctx(s))) == 1 and G(s, '#dgEnd', 'cb') == s.gt + G(s, '#dgPW') - 1)
    # a chapter boss's hit proxy (rlk_mb_px) and a foreign interaction (a lobby object): the proxy's right-click is consumed
    # by the pre-pass too, the foreign one is left alone
    s.gt += 40
    P(s, 'dashCool', 0)
    px = Ent('interaction', (3.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mb_px', 'boss'])
    px.data['interaction'] = {'timestamp': s.gt}
    lo = Ent('interaction', (5.5, 64.0, 0.5), (0.0, 0.0), ['rlk_lobj'])
    lo.data['interaction'] = {'timestamp': s.gt}
    s.ents += [px, lo]
    s.call('rlk:player/def/input', pctx(s))
    ck('input: a boss proxy right-click is consumed by the pre-pass (dodge now), a lobby interaction is left alone',
       'interaction' not in px.data and 'interaction' in lo.data and P(s, 'dgAt') == s.gt)
    t1 = P(s, 'dgAt')
    s.gt += 5
    s.call('rlk:player/dash', pctx(s))
    ck('input: a second dodge inside the cooldown is refused (no charges any more)', P(s, 'dgAt') == t1)
    ck('input: #dashCoolT 12 by default', G(s, '#dashCoolT') == 12)
    s.setsc('dash', 'engN', 2)
    s.call('rlk:engravings/scan_more', pctx(s))
    ck('input: 질주 2: the cooldown is 9 (-20 %)', G(s, '#dashCoolT') == 9, G(s, '#dashCoolT'))
    s.setsc('dash', 'engN', 0)
    s.call('rlk:engravings/scan_more', pctx(s))


# ================================================================================================== judge
def t_judge():
    s, pl = world()
    nopress(s)
    ck('judge: nothing open -> hit (#dodged 0, #parT 0)', judge(s) == (0, 0, 0))
    P(s, 'dashInvT', 3)
    ck('judge: i-frames (dashInvT) avoid (no reward, no hwamu)', judge(s)[0] == 1 and not s.calls('rlk:player/def/fx/pd'))
    ck('judge: a no-dodge hit ignores the i-frames', judge(s, ND=1)[0] == 0)
    P(s, 'dashInvT', 0)
    dodge(s, 1)
    press(s, 1)
    ck('judge: a perfect dodge wins over a perfect parry (#pdg 1, #parT 0)', judge(s) == (1, 0, 1))
    dodge(s, 4)
    press(s, 1)
    ck('judge: a perfect parry wins over a loose dodge', judge(s) == (1, 3, 0))
    dodge(s, 4)
    press(s, 4)
    ck('judge: a loose dodge wins over a tier-2 parry (normal class)', judge(s) == (1, 0, 0))
    dodge(s, 4)
    press(s, 4)
    ck('judge: against a boss the loose window does nothing -> tier 2', judge(s, C=2) == (0, 2, 0))
    nopress(s)
    press(s, 1)
    ck('judge: an unparriable hit ignores the F press', judge(s, NP=1) == (0, 0, 0))
    nopress(s)
    dodge(s, 1)
    ck('judge: a no-dodge hit ignores the perfect dodge', judge(s, ND=1) == (0, 0, 0))
    ck('judge: the context is one-shot (all #hc* 0 after the call)', all(G(s, k) == 0 for k in ('#hcK', '#hcC', '#hcNP', '#hcND')))
    nopress(s)
    P(s, 'parAt', s.gt + 2)
    P(s, 'parHit', -1000000)
    ck('judge: a press stamped in the future (never) is ignored', judge(s)[1] == 0)


# ================================================================================================== tiers (the real hit)
def t_tiers():
    s, pl = world()
    e = brain(s)
    nopress(s)
    base = cm_hit(s, e, 60)
    ck('tiers: an unparried cm hit takes damage and plays the hurt flash + knockback start', base > 0
       and s.calls('rlk:cm/hurt_fx') and s.calls('rlk:player/knockback/start'), base)
    expect = {}
    for ago in range(0, 13):
        nopress(s)
        press(s, ago)
        lost = cm_hit(s, e, 60)
        tier = G(s, '#parT')
        want = 3 if ago <= 2 else 2 if ago <= 5 else 1 if ago <= 9 else 0
        wl = 0 if want == 3 else max(1, base * 20 // 100) if want == 2 else max(1, base * 50 // 100) if want == 1 else base
        expect[ago] = (tier, lost)
        ck(f'tiers: F {ago} t before the hit -> tier {want}, HP lost {wl}', tier == want and lost == wl, (tier, lost, base))
        if want:
            ck(f'tiers: tier {want} ({ago} t): no hurt flash, no knockback', not s.calls('rlk:cm/hurt_fx')
               and not s.calls('rlk:player/knockback/start'))
    # one press = one tick of hits
    nopress(s)
    press(s, 1)
    l1 = cm_hit(s, e, 60)
    l2 = cm_hit(s, e, 60)
    ck('tiers: two hits in the same tick are both parried by one press (tier 3 twice), rewards once',
       l1 == 0 and l2 == 0 and G(s, '#parT') == 3 and len(s.calls('rlk:bal/hit')) == 0)
    s.gt += 1
    l3 = cm_hit(s, e, 60)
    ck('tiers: the next tick the press is spent (the hit lands)', l3 == base and G(s, '#parT') == 0, (l3, G(s, '#parT')))
    ck('tiers: after a parry the next press is allowed 2 t later (parLk = parry tick + #parChain)',
       P(s, 'parLk') == P(s, 'parHit') + G(s, '#parChain'))


# ================================================================================================== dodge windows
def t_dodge():
    s, pl = world()
    for cls, tags in (('normal', ()), ('elite', ('rlk_c2e',)), ('elite3', ('rlk_c3e',))):
        e = brain(s, tags)
        for ago in range(0, 9):
            nopress(s)
            dodge(s, ago)
            lost = cm_hit(s, e, 50)
            want_avoid = ago <= 6
            ck(f'dodge: {cls}, dodge {ago} t before the hit -> {"avoided" if want_avoid else "hit"}'
               + (' (perfect)' if ago <= 2 else ''), (lost == 0) == want_avoid and (G(s, '#pdg') == 1) == (ago <= 2), (lost, G(s, '#pdg')))
        e.alive = False
        s.ents.remove(e)
    # boss class through the framework context
    nopress(s)
    for ago in range(0, 8):
        dodge(s, ago)
        d, p, pdg = judge(s, K=3, C=2)
        ck(f'dodge: boss, dodge {ago} t before -> {"perfect" if ago <= 2 else "hit"}', (d == 1) == (ago <= 2) and pdg == (1 if ago <= 2 else 0))


# ================================================================================================== context
def t_context():
    s, pl = world()
    nopress(s)
    e = brain(s, ('rlk_c2e',), cid=11)
    s.call('rlk:player/def/ctx_cm', Ctx(e, tuple(e.pos), tuple(e.rot)))
    ck('context: a cm brain is the attacker (rlk_hc_atk), elite class 1, kind 1', 'rlk_hc_atk' in e.tags and G(s, '#hcC') == 1
       and G(s, '#hcK') == 1)
    judge(s, K=G(s, '#hcK'), C=G(s, '#hcC'))
    ck('context: the judge removes the attacker tag', not s.select('@e[tag=rlk_hc_atk]', pctx(s)))
    pj = Ent('block_display', (1.5, 65.0, 0.5), (0.0, 0.0), ['rlk_cmp', 'rlk_cmp_ar'])
    s.ents.append(pj)
    s.setsc(('e', pj.id), 'cmId', 11)
    other = brain(s, (), cid=12)
    s.setsc('#hcK', 'tmp', 0)
    s.call('rlk:player/def/ctx_cm', Ctx(pj, tuple(pj.pos), tuple(pj.rot)))
    ck('context: a cm projectile -> its owner brain (same cmId) is the attacker, kind 2', 'rlk_hc_atk' in e.tags
       and 'rlk_hc_atk' not in other.tags and 'rlk_hc_atk' not in pj.tags and G(s, '#hcK') == 2)
    judge(s)
    rd_ = Ent('marker', (3.5, 64.0, 0.5), (0.0, 0.0), ['rlk_rd_hazard'])
    rai = Ent('husk', (6.5, 64.0, 0.5), (0.0, 0.0), ['rlk_raiden'])
    s.ents += [rd_, rai]
    s.setsc('#hcK', 'tmp', 2)
    s.call('rlk:player/def/ctx_cm', Ctx(rd_, tuple(rd_.pos), tuple(rd_.rot)))
    ck('context: a Raiden hazard -> Raiden is the attacker, boss class, the kind land set is kept', 'rlk_hc_atk' in rai.tags
       and G(s, '#hcC') == 2 and G(s, '#hcK') == 2)
    judge(s)
    body = Ent('husk', (8.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mb_body', 'boss'])
    hz = Ent('marker', (2.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mb_hz'])
    s.ents += [body, hz]
    for k, want in ((1, 1), (2, 3), (3, 1), (4, 1), (5, 3), (6, 3)):
        s.setsc(('e', hz.id), 'mbHzK', k)
        s.setsc('#mbSrcIn', 'mb', 1)
        s.setsc('#mbNoDodge', 'mb', 1 if k == 6 else 0)
        s.setsc('#mbNoParry', 'mb', 1 if k >= 5 else 0)
        s.call('rlk:mboss/hurt_ctx', Ctx(hz, tuple(hz.pos), tuple(hz.rot)))
        ck(f'context: boss hazard kind {k} -> boss body attacker, class 2, kind {want}, ND / NP from the one-shot inputs',
           'rlk_hc_atk' in body.tags and G(s, '#hcC') == 2 and G(s, '#hcK') == want and G(s, '#hcND') == (1 if k == 6 else 0)
           and G(s, '#hcNP') == (1 if k >= 5 else 0))
        judge(s, K=G(s, '#hcK'), C=2, NP=G(s, '#hcNP'), ND=G(s, '#hcND'))
    s.setsc('#mbSrcIn', 'mb', 2)
    s.call('rlk:mboss/hurt_ctx', Ctx(hz, tuple(hz.pos), tuple(hz.rot)))
    ck('context: a boss prop -> kind 2', G(s, '#hcK') == 2)
    judge(s)
    vm = Ent('zombie', (2.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mob', 'miniboss'])
    s.ents.append(vm)
    s.setsc('#hcC', 'tmp', 0)
    s.call('rlk:player/def/ctx_va', Ctx(vm, tuple(vm.pos), tuple(vm.rot)))
    ck('context: a vanilla attacker tagged miniboss -> attacker tag, boss class', 'rlk_hc_atk' in vm.tags and G(s, '#hcC') == 2)
    judge(s)
    ck('context: hit_pl through cm: a real hit leaves no rlk_hc_atk behind', (cm_hit(s, e, 10) >= 0)
       and not s.select('@e[tag=rlk_hc_atk]', pctx(s)))


# ================================================================================================== energy
def t_energy():
    s, pl = world()
    e = brain(s)
    cost = G(s, '#burstCost100')
    P(s, 'energy', 0)
    nopress(s)
    dodge(s, 1)
    cm_hit(s, e, 30)
    ck('energy: a perfect dodge gives +1000 (10 pt)', P(s, 'energy') == 1000, P(s, 'energy'))
    ck('energy: ... with the red effect and the item hook', bool(s.calls('rlk:player/def/fx/pd')) and bool(s.calls('rlk:items/hook/on_pdodge')))
    cm_hit(s, e, 30)
    ck('energy: a second hit avoided by the same dodge gives no more', P(s, 'energy') == 1000 and G(s, '#pdg') == 1)
    s.gt += 30
    dodge(s, 2)
    cm_hit(s, e, 30)
    ck('energy: the next dodge rewards again', P(s, 'energy') == 2000)
    dodge(s, 4)
    s.gt += 1
    P(s, 'energy', 0)
    dodge(s, 4)
    cm_hit(s, e, 30)
    ck('energy: a loose dodge (3-6 t) gives nothing', P(s, 'energy') == 0)
    P(s, 'energy', cost - 300)
    dodge(s, 0)
    cm_hit(s, e, 30)
    ck('energy: clamped at the burst cost', P(s, 'energy') == cost, (P(s, 'energy'), cost))
    s.setsc('#skMode', 'tmp', 1)
    P(s, 'energy', 0)
    s.gt += 30
    dodge(s, 0)
    cm_hit(s, e, 30)
    ck('energy: 스커크 in 일곱빛 섬광 (#skMode 1) gets none', P(s, 'energy') == 0)
    s.setsc('#skMode', 'tmp', 0)


# ================================================================================================== cd cut + balance
def t_cd():
    s, pl = world()
    e = brain(s)
    for char_n, label in ((1, '루미네'), (4, '클로린드'), (5, '아를레키노'), (3, '스커크'), (7, '로노바')):
        s.setsc('#charN', 'tmp', char_n)
        P(s, 'skillCd', 100)
        s.setsc('#cut', 'cb', 20)
        s.call('rlk:char/cd_cut', pctx(s))
        a = P(s, 'skillCd')
        P(s, 'skillCd', 7)
        s.call('rlk:char/cd_cut', pctx(s))
        ck(f'cd: {label}: skillCd -20 t (100 -> 80), clamped at 0 (7 -> 0)', a == 80 and P(s, 'skillCd') == 0, (a, P(s, 'skillCd')))
    s.setsc('#charN', 'tmp', 6)
    P(s, 'nvC', 0)
    P(s, 'nvCT', 30)
    s.call('rlk:char/cd_cut', pctx(s))
    ck('cd: 나비아 (no charge): the charge timer nvCT +20', P(s, 'nvCT') == 50)
    P(s, 'nvC', 2)
    P(s, 'nvCT', 0)
    s.call('rlk:char/cd_cut', pctx(s))
    ck('cd: 나비아 full (2 charges): nothing to cut', P(s, 'nvCT') == 0)
    s.setsc('#charN', 'tmp', 8)
    P(s, 'nfC', 1)
    P(s, 'nfCT', 10)
    s.call('rlk:char/cd_cut', pctx(s))
    ck('cd: 네페르 (1 charge): nfCT +20', P(s, 'nfCT') == 30)
    s.setsc('#charN', 'tmp', 1)
    P(s, 'skillCd', 200)
    nopress(s)
    press(s, 0)
    cm_hit(s, e, 30)
    cm_hit(s, e, 30)
    ck('cd: a perfect parry cuts the skill once per press (200 -> 180) even with two hits in the tick', P(s, 'skillCd') == 180,
       P(s, 'skillCd'))
    nopress(s)
    press(s, 1)
    s.log.clear()
    s.setsc('#hcK', 'tmp', 0)
    s.setsc('#cmDmg', 'tmp', 30)
    full(s)
    s.call('rlk:cm/hit_me', Ctx(e, tuple(e.pos), tuple(e.rot)))
    bh = s.calls('rlk:bal/hit')
    ck('cd: a perfect parry calls rlk:bal/hit {n:1} as the attacker (the cm brain)', len(bh) == 1 and 'rlk_cmb' in bh[0][1]
       and bh[0][2] == {'n': 1}, bh)
    nopress(s)
    press(s, 4)
    s.log.clear()
    cm_hit(s, e, 30)
    ck('cd: a tier-2 parry neither cuts the skill nor takes balance', not s.calls('rlk:bal/hit') and not s.calls('rlk:char/cd_cut'))


# ================================================================================================== balance (lane B's gauge)
def gauge(s, e):
    """the enemy's gauge as mob/setup makes it (rlk:bal/init as the new mob) -> (bal, balMax, balC)"""
    s.call('rlk:bal/init', Ctx(e, tuple(e.pos), tuple(e.rot)))
    return bal(s, e), s.sc(('e', e.id), 'balMax'), s.sc(('e', e.id), 'balC')


def bal(s, e):
    return s.sc(('e', e.id), 'bal')


def t_bal():
    s, pl = world()
    e = brain(s)
    b0, mx, c = gauge(s, e)
    ck('bal: a cm brain gets lane B\'s normal gauge (balC 1, full)', c == 1 and mx >= 2 and b0 == mx, (b0, mx, c))
    nopress(s)
    press(s, 1)
    lost = cm_hit(s, e, 30)
    ck('bal: a perfect parry on a strike takes exactly one pip from the attacker (and no damage)', bal(s, e) == mx - 1 and lost == 0,
       (bal(s, e), mx, lost))
    cm_hit(s, e, 30)
    ck('bal: a second hit in the same tick (the same press) takes no second pip', bal(s, e) == mx - 1, bal(s, e))
    s.gt += 1
    l2 = cm_hit(s, e, 30)
    ck('bal: the press is spent: the next tick\'s hit lands and takes no pip', bal(s, e) == mx - 1 and l2 > 0, (bal(s, e), l2))
    for ago, tier in ((4, 2), (7, 1)):
        nopress(s)
        press(s, ago)
        cm_hit(s, e, 30)
        ck(f'bal: a tier-{tier} parry takes no pip', bal(s, e) == mx - 1 and G(s, '#parT') == tier, (bal(s, e), G(s, '#parT')))
    nopress(s)
    dodge(s, 1)
    cm_hit(s, e, 30)
    ck('bal: a perfect dodge takes no pip', bal(s, e) == mx - 1, bal(s, e))
    nopress(s)
    s.gt += 40
    press(s, 0)
    cm_hit(s, e, 30)
    ck('bal: a new press, a new perfect parry: one more pip', bal(s, e) == mx - 2, bal(s, e))
    # a projectile: the pip comes off its owner, not off another brain
    other = brain(s, (), pos=(4.5, 64.0, 0.5), cid=12)
    gauge(s, other)
    pj = Ent('block_display', (1.5, 65.0, 0.5), (0.0, 0.0), ['rlk_cmp', 'rlk_cmp_ar'])
    s.ents.append(pj)
    s.setsc(('e', pj.id), 'cmId', 7)
    nopress(s)
    s.gt += 40
    press(s, 2)
    full(s)
    s.setsc('#hcK', 'tmp', 0)
    s.setsc('#dmgIn', 'tmp', 30)
    s.setsc('#cmDmg', 'tmp', 30)
    before = (bal(s, e), bal(s, other))
    hp0 = P(s, 'curHealth')
    s.call('rlk:cm/hit_pl', Ctx(pj, tuple(pj.pos), tuple(pj.rot)))
    ck('bal: a perfectly parried projectile takes one pip from its owner brain only',
       (bal(s, e), bal(s, other)) == (before[0] - 1, before[1]) and P(s, 'curHealth') == hp0, (before, bal(s, e), bal(s, other)))
    # an elite: one pip of its larger gauge
    el = brain(s, ('rlk_c2e',), pos=(3.5, 64.0, 2.5), cid=21)
    eb, emx, ec = gauge(s, el)
    nopress(s)
    s.gt += 40
    press(s, 1)
    cm_hit(s, el, 30)
    ck('bal: an elite (balC 2): one pip of its gauge', ec == 2 and emx > mx and bal(s, el) == emx - 1, (eb, emx, ec, bal(s, el)))
    # a groggy attacker refuses balance damage: the parry itself still works
    s.setsc(('e', el.id), 'grgT', 40)
    nopress(s)
    s.gt += 40
    press(s, 1)
    P(s, 'skillCd', 100)
    lost = cm_hit(s, el, 30)
    ck('bal: a groggy attacker keeps its pips (rlk:bal/hit fails), the perfect parry still nullifies and cuts the skill',
       bal(s, el) == emx - 1 and lost == 0 and P(s, 'skillCd') == 80, (bal(s, el), lost, P(s, 'skillCd')))
    # a registry boss body in the fight state (bal/boss/may): one pip of the boss gauge
    body = Ent('husk', (8.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mb_body', 'rlk_mob', 'boss'])
    s.ents.append(body)
    for o, v in (('balMax', 12), ('bal', 12), ('balC', 3), ('grgT', 0), ('balT', 0)):
        s.setsc(('e', body.id), o, v)
    for o, v in (('#mbSt', 1), ('#mbCine', 0), ('#mbBarOff', 0), ('#mbAtk', 100), ('#mbDmgMul', 100), ('#mbKB', 0), ('#mbLv', 1)):
        s.setsc(o, 'mb', v)

    def boss_hit(np=0):
        """a real framework strike: mboss/hurt as the body (#mbHitPct 100 -> hurt_ctx -> cm/hit_pl2 -> take_damage)"""
        nopress(s)
        s.gt += 40
        press(s, 1)
        full(s)
        for o, v in (('#mbHitPct', 100), ('#mbNoParry', np), ('#mbNoDodge', 0), ('#mbSrc', 0), ('#mbNoRx', 0)):
            s.setsc(o, 'mb', v)
        hp0 = P(s, 'curHealth')
        s.call('rlk:mboss/hurt', Ctx(body, tuple(body.pos), (0, 0)))
        return hp0 - P(s, 'curHealth')

    lost = boss_hit()
    ck('bal: boss body (balC 3), a perfectly parried strike: exactly one pip, no damage', bal(s, body) == 11 and lost == 0,
       (bal(s, body), lost))
    lost = boss_hit(np=1)
    ck('bal: boss body, an unparriable attack: the press does nothing (damage lands, no pip)', bal(s, body) == 11 and lost > 0,
       (bal(s, body), lost))
    s.setsc('#mbBarOff', 'mb', 1)
    lost = boss_hit()
    ck('bal: a boss with hidden bars refuses the pip (bal/boss/may); the parry still nullifies', bal(s, body) == 11 and lost == 0,
       (bal(s, body), lost))
    s.setsc('#mbBarOff', 'mb', 0)
    s.setsc(('e', body.id), 'bal', 1)
    lost = boss_hit()
    ck('bal: the last pip by a perfect parry empties the gauge (lane B\'s groggy takes over: grgT or pending)',
       bal(s, body) == 0 and lost == 0 and ((s.sc(('e', body.id), 'grgT') or 0) >= 1 or 'rlk_bal_pend' in body.tags),
       (bal(s, body), s.sc(('e', body.id), 'grgT'), sorted(body.tags)))


# ================================================================================================== boss framework
def hzm(s, K, R=2000, ND=0, Pm=None, RA=0, opt=-1, D=100):
    m = Ent('marker', (2.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mb_hz'])
    s.ents.append(m)
    for o, v in (('mbHzK', K), ('mbHzR', R), ('mbHzND', ND), ('mbHzRA', RA), ('mbHzD', D)):
        s.setsc(('e', m.id), o, v)
    if Pm is not None:
        s.setsc(('e', m.id), 'mbHzPm', Pm)
    s.setsc('#hzNoParry', 'mb', opt)
    s.call('rlk:mboss/hz/np_def', Ctx(m, tuple(m.pos), tuple(m.rot)))
    return s.sc(('e', m.id), 'mbHzNP')


def t_boss():
    s, pl = world()
    cases = [('disc r 3.2', dict(K=1, R=3200), 0), ('disc r 4.5', dict(K=1, R=4500), 1), ('sector r 6', dict(K=3, R=6000), 0),
             ('sector r 12', dict(K=3, R=12000), 1), ('line 5 b', dict(K=4, R=5000), 0), ('line 14 b', dict(K=4, R=14000), 1),
             ('ring', dict(K=2, R=3000), 1), ('full', dict(K=5, R=20000), 1), ('mask', dict(K=6, R=0), 1),
             ('no-dodge disc r 2', dict(K=1, R=2000, ND=1), 1), ('per-mille disc', dict(K=1, R=2000, Pm=250), 1),
             ('re-arm disc', dict(K=1, R=2000, RA=10), 1)]
    for name, kw, want in cases:
        ck(f'boss: np_def {name} -> {"unparriable" if want else "parryable"}', hzm(s, **kw) == want)
    # hz/init applies the explicit option
    body = Ent('husk', (8.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mb_body', 'boss'])
    s.ents.append(body)
    init = rd('mboss/hz/init')
    ck('boss: hz/init: #hzNoParry 0 / 1 overrides the rule (only -1 runs np_def)',
       'execute unless score @s mbHzNP matches 0..1 run function rlk:mboss/hz/np_def' in init)
    launch = rd('mboss/pj/launch')
    ck('boss: pj/launch: props parryable unless no-dodge (or #pjNoParry)', 'mbPjNP = #pjNoParry mb' in launch
       and 'unless score @s mbPjNP matches 0..1 run scoreboard players operation @s mbPjNP = @s mbPjND' in launch)
    # hurt_dodge
    for pdg, par, want in ((1, 0, 1), (0, 3, 1), (0, 0, 0), (0, 2, 0)):
        s.setsc('#mbDodgeOk', 'mb', 0)
        s.setsc('#pdg', 'tmp', pdg)
        s.setsc('#parT', 'tmp', par)
        s.call('rlk:mboss/hurt_dodge', Ctx(body, tuple(body.pos), (0, 0)))
        ck(f'boss: hurt_dodge: #pdg {pdg} #parT {par} -> #mbDodgeOk {want}', G(s, '#mbDodgeOk', 'mb') == want)
    # hz/hurt_pm through the judge
    m = Ent('marker', (0.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mb_hz'])
    s.ents.append(m)
    for o, v in (('mbHzK', 5), ('mbHzPm', 250), ('mbHzND', 0), ('mbHzNP', 1), ('mbHzE', 0), ('mbHzPmL', 1), ('mbHzG', 0)):
        s.setsc(('e', m.id), o, v)
    s.setsc('#mbSt', 'mb', 1)
    for label, setup, want_lost in (('a perfect dodge avoids', lambda: dodge(s, 1), False),
                                    ('a perfect parry does not (unparriable)', lambda: press(s, 1), True),
                                    ('i-frames avoid (not no-dodge)', lambda: P(s, 'dashInvT', 4), False)):
        nopress(s)
        full(s)
        setup()
        hp0 = P(s, 'curHealth')
        s.call('rlk:mboss/hz/hurt_pm', Ctx(m, tuple(m.pos), (0, 0)))
        lost = hp0 - P(s, 'curHealth')
        ck(f'boss: hz/hurt_pm (250 per mille): {label}', (lost > 0) == want_lost, lost)
        P(s, 'dashInvT', 0)
    # np_glint spacing / module opt-out
    s.setsc('#mbNpAt', 'mb', -1000000)
    s.setsc('#mbNpOwn', 'mb', 0)
    s.setsc('#mbCine', 'mb', 0)
    s.log.clear()
    s.call('rlk:mboss/np_glint', Ctx(body, tuple(body.pos), (0, 0)))
    s.call('rlk:mboss/np_glint', Ctx(body, tuple(body.pos), (0, 0)))
    n1 = len(s.calls('rlk:player/def/fx/glint'))
    s.gt += G(s, '#npGap')
    s.call('rlk:mboss/np_glint', Ctx(body, tuple(body.pos), (0, 0)))
    n2 = len(s.calls('rlk:player/def/fx/glint'))
    s.setsc('#mbNpOwn', 'mb', 1)
    s.gt += 50
    s.call('rlk:mboss/np_glint', Ctx(body, tuple(body.pos), (0, 0)))
    n3 = len(s.calls('rlk:player/def/fx/glint'))
    ck('boss: np_glint: once per #npGap (a volley warns once), again after it, never with #mbNpOwn 1', (n1, n2, n3) == (1, 2, 2),
       (n1, n2, n3))
    ck('boss: the glint puts the glyph text_display on the boss (rlk_cb_glint)', bool(s.select('@e[tag=rlk_cb_glint]', pctx(s))))


# ================================================================================================== near miss
def t_near():
    s, pl = world()
    body = Ent('husk', (12.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mb_body', 'boss'])
    s.ents.append(body)
    s.setsc('#mbSt', 'mb', 1)
    s.setsc('#mbCine', 'mb', 0)
    s.setsc('#mbAtk', 'mb', 50)
    s.setsc('#mbDmgMul', 'mb', 100)
    s.setsc('#mbLv', 'mb', 1)

    def hazard(ND=0):
        m = Ent('marker', (0.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mb_hz'])
        s.ents.append(m)
        for o, v in (('mbHzK', 1), ('mbHzR', 2000), ('mbHzRR', 2300 * 2300), ('mbHzRI', 0), ('mbHzY0', -500), ('mbHzY1', 3500),
                     ('mbHzD', 100), ('mbHzE', 0), ('mbHzB', 0), ('mbHzKD', 0), ('mbHzND', ND), ('mbHzNP', 0), ('mbHzNR', 0),
                     ('mbHzG', 0), ('mbHzRA', 0), ('mbHzHit', 0), ('mbHzFX', 0), ('mbHzFZ', 1000)):
            s.setsc(('e', m.id), o, v)
        return m

    def go(dodged_ago, ND=0, start=(0.5, 64.0, 0.5)):
        for g in s.select('@e[tag=rlk_dgo]', pctx(s)):
            g.alive = False
        s.ents = [e for e in s.ents if e.alive]
        nopress(s)
        full(s)
        P(s, 'energy', 0)
        pl.pos = [start[0] + 3.5, 64.0, start[2]]      # the body has already moved 3.5 b away
        if dodged_ago is not None:
            dodge(s, dodged_ago)
            s.ents.append(Ent('interaction', start, (0.0, 0.0), ['rlk_dgo', 'rlk_pet']))
            s.setsc('#dgOpen', 'cb', 1 if dodged_ago <= 2 else 0)
        else:
            s.setsc('#dgOpen', 'cb', 0)
        m = hazard(ND)
        hp0 = P(s, 'curHealth')
        s.setsc(('e', m.id), 'mbHzT', 5)
        s.setsc(('e', m.id), 'mbHzW', 5)
        s.setsc(('e', m.id), 'mbHzA', 1)
        s.call('rlk:mboss/hz/hit', Ctx(m, tuple(m.pos), (0, 0)))           # hz/tick's own test (misses the moved body)
        if (G(s, '#dgOpen', 'cb') or 0) == 1:
            s.call('rlk:mboss/hz/near', Ctx(m, tuple(m.pos), (0, 0)))      # hz/all's pass in the window
        return hp0 - P(s, 'curHealth'), s.sc(('e', m.id), 'mbHzHit'), G(s, '#pdg')
    lost, used, pdg = go(1)
    ck('near: a disc that misses the moved body but covers the dodge start (1 t ago) = a perfect dodge (no damage, +10 pt)',
       lost == 0 and used == 1 and pdg == 1 and P(s, 'energy') == 1000, (lost, used, pdg, P(s, 'energy')))
    ck('near: the body mark is back on the player afterwards', 'rlk_body' in pl.tags and not s.select('@e[tag=rlk_body_real]', pctx(s))
       and all('rlk_body' not in g.tags for g in s.select('@e[tag=rlk_dgo]', pctx(s))))
    lost, used, pdg = go(1, ND=1)
    ck('near: a no-dodge hazard is never re-tested at the dodge start (it misses the moved body)', lost == 0 and used == 0)
    lost, used, pdg = go(5)
    ck('near: outside the perfect window there is no re-test', lost == 0 and used == 0 and P(s, 'energy') == 0)
    pl.pos = [0.5, 64.0, 0.5]


# ================================================================================================== Raiden
def t_raiden():
    land = rd('boss/raiden/hazard/land')
    ck('raiden: land: kind 2 for sweep / slab / orb, 1 for rects, else 3', 'rdHK matches 5..7 run scoreboard players set #hcK tmp 2' in land
       and 'rdHK matches 3..4 run scoreboard players set #hcK tmp 1' in land and 'set #hcK tmp 3' in land)
    ck('raiden: land: nododge and kinds 9 / 10 are unparriable', 'rlk_rd_nododge] run scoreboard players set #hcNP tmp 1' in land
       and 'rdHK matches 9..10 run scoreboard players set #hcNP tmp 1' in land)
    ck('raiden: land: the context is reset after the call (a refused hurt leaves nothing)', all(f'scoreboard players set {k} tmp 0' in
       land.split('function rlk:boss/raiden/hurt')[-1] for k in ('#hcK', '#hcNP', '#hcND')))
    ck('raiden: land: no knockback when dodged or parried', 'unless score #dodged tmp matches 1 unless score #parT tmp matches 1..' in land)
    new = rd('boss/raiden/hazard/new')
    ck('raiden: a damaging nododge hazard flashes the glint on Raiden (spaced, fx/rd_glint)', 'player/def/fx/rd_glint' in new)
    s, pl = world()
    rai = Ent('husk', (6.5, 64.0, 0.5), (0.0, 0.0), ['rlk_raiden'])
    s.ents.append(rai)
    s.setsc('#rdNpAt', 'cb', -1000000)
    s.log.clear()
    m = Ent('marker', (2.5, 64.0, 0.5), (0.0, 0.0), [])
    s.call('rlk:player/def/fx/rd_glint', Ctx(m, tuple(m.pos), (0, 0)))
    s.call('rlk:player/def/fx/rd_glint', Ctx(m, tuple(m.pos), (0, 0)))
    ck('raiden: rd_glint at most once per #npGap', len(s.calls('rlk:player/def/fx/glint')) == 1)


# ================================================================================================== readers
def t_readers():
    s, pl = world()
    e = brain(s)
    P(s, 'it_sword_hwamu', 1)
    s.setsc('#hwCtrCd', 'itv', 0)
    for label, setup, want in (('a perfect dodge', lambda: dodge(s, 1), 1), ('a loose dodge', lambda: dodge(s, 5), 1),
                               ('a perfect parry', lambda: press(s, 0), 1), ('i-frames', lambda: P(s, 'dashInvT', 3), 0),
                               ('a landed hit', lambda: None, 1)):
        nopress(s)
        s.gt += 40
        setup()
        cm_hit(s, e, 20)
        n = len(s.calls('rlk:items/proc/hw_ctr_q'))
        ck(f'readers: 화무십일홍 검신합일 is queued by {label}: {"yes" if want else "no"}', (n >= 1) == bool(want), n)
        P(s, 'dashInvT', 0)
    P(s, 'it_sword_hwamu', 0)
    # 홍련's pips: q_pf0 / q_pf1
    for label, setup, w0, w1 in (('a dodge 2 t ago', lambda: dodge(s, 2), 1, 1), ('a dodge 3 t ago', lambda: dodge(s, 3), 0, 1),
                                 ('a dodge 4 t ago', lambda: dodge(s, 4), 0, 0), ('an F press 0 t ago', lambda: press(s, 0), 1, 0),
                                 ('nothing', lambda: None, 0, 0)):
        nopress(s)
        setup()
        r0 = s.call('rlk:player/def/q_pf0', Ctx(None, (0, 0, 0), (0, 0)))
        r1 = s.call('rlk:player/def/q_pf1', Ctx(None, (0, 0, 0), (0, 0)))
        ck(f'readers: 홍련 pip window, {label}: q_pf0 {w0} / q_pf1 {w1}', (bool(r0), bool(r1)) == (bool(w0), bool(w1)), (r0, r1))
    pip = rd('boss/scarlet/shield/pip')
    ck('readers: 홍련 shield/pip reads q_pf0 at s and q_pf1 at s + 1 (no dashInvT)', 'q_pf0' in pip and 'q_pf1' in pip and 'dashInvT' not in pip)
    ck('readers: the shield rush contact ends on a perfect parry', 'execute if score #parT tmp matches 3 run tag @s add rlk_sh_rhit' in rd('cm/sh/rcontact'))
    ck('readers: Apep\'s organism bolt ends when parried (tier 3) and flies on when dodged',
       'execute if score #dodged tmp matches 1 unless score #parT tmp matches 3 run return 0' in rd('boss/apep/org/pj_end'))
    ck('readers: the item hooks on_parry / on_pdodge / on_parry_press exist; on_dash keeps the item effects (no hw_dash)',
       all(rd(f'items/hook/{h}') is not None for h in ('on_parry', 'on_pdodge', 'on_parry_press')) and 'hw_dash' not in rd('items/hook/on_dash'))
    ck('readers: the tutorial step 1 counts dodges and F presses', '#tutC lob 1' in rd('items/hook/on_parry_press'))
    ck('readers: knockback start / tick and hurt_elem still read the non-dodge i-frames (dashInvT)', all('dashInvT' in rd(f) for f in
       ('player/knockback/start', 'player/knockback/tick', 'player/hurt_elem')))


# ================================================================================================== fx
def t_fx():
    s, pl = world()
    e = brain(s)
    s.titles.clear()
    nopress(s)
    press(s, 1)
    P(s, 'vBig', 0)
    P(s, 'ttlT', 0)
    cm_hit(s, e, 20)
    ck('fx: a perfect parry: the starburst text_display (rlk_cb_star) and the arc / jolt markers', bool(s.select('@e[tag=rlk_cb_star]', pctx(s)))
       and bool(s.select('@e[tag=rlk_cb_arc]', pctx(s))) and bool(s.select('@e[tag=rlk_cb_jolt]', pctx(s))))
    ck('fx: ... and the streak overlay on the title (vBig = 6)', any('' in t for t in s.titles) and P(s, 'vBig') == 6, s.titles[-2:])
    s.titles.clear()
    s.gt += 30
    nopress(s)
    press(s, 4)
    P(s, 'ttlT', 30)
    P(s, 'vBig', 0)
    cm_hit(s, e, 20)
    ck('fx: tier 2 under a bottom line (ttlT): no overlay (the line keeps its times), the small star still shows',
       not s.titles and len(s.select('@e[tag=rlk_cb_star]', pctx(s))) == 2)
    P(s, 'ttlT', 0)
    s.titles.clear()
    s.gt += 30
    nopress(s)
    dodge(s, 0)
    s.ents.append(Ent('interaction', (0.5, 64.0, 0.5), (0.0, 0.0), ['rlk_dgo', 'rlk_pet']))
    P(s, 'vBig', 0)
    cm_hit(s, e, 20)
    ck('fx: a perfect dodge: the wash overlay and the red ghost mannequin (team rlk_cbred, 8 t)', any('' in t for t in s.titles)
       and bool(s.select('@e[tag=rlk_cb_ghost]', pctx(s))))
    for _ in range(12):
        s.call('rlk:player/def/fx/world', Ctx(None, (0, 0, 0), (0, 0)))
    ck('fx: every effect entity is gone after 12 ticks of fx/world', not s.select('@e[tag=rlk_cb_fx]', pctx(s)))


# ================================================================================================== cost
def t_cost():
    s, pl = world()
    s.setsc('#now', 'cb', s.gt)
    n0 = s.n
    s.call('rlk:player/def/input', pctx(s))
    n = s.n - n0
    ck(f'cost: the idle pre-pass runs {n} commands (<= 6)', n <= 6, n)


SECTIONS = [('static', t_static), ('input', t_input), ('judge', t_judge), ('tiers', t_tiers), ('dodge', t_dodge),
            ('context', t_context), ('energy', t_energy), ('cd', t_cd), ('bal', t_bal), ('boss', t_boss), ('near', t_near), ('raiden', t_raiden),
            ('readers', t_readers), ('fx', t_fx), ('cost', t_cost)]
for name, fn in SECTIONS:
    if run(name):
        fn()
print(f'test_cb: {NOK}/{NOK + len(FAILS)} passed')
if FAILS:
    print('FAILED: ' + ', '.join(FAILS[:30]))
    sys.exit(1)
