#!/usr/bin/env python3
"""test_cb.py: the combat overhaul's lane C (parry on F, the dodge, the damage context, unparriable attacks) against one
datapack root (read only).

    python3 test_cb.py <datapack root> [section ...]
      sections: static input lock judge tiers dodge cool context energy cd bal boss near raiden readers fx beat bossloop beatloop cost
                (default: all)

  static   the dash charges / HUD gauge / dash_iframe / hurt_nd are gone; dashInvT is written only by the non-dodge
           i-frames; the tick order (the input pre-pass before view/tick, player/tick, the cm worlds, Raiden, the bosses;
           the dodge-start box around the cm worlds); lores and the tutorial say 닷지 / 패링, no 대쉬; the generated
           framework lines (np_def's rule, the glint, hurt_ctx, hz/hit_near, pj/step_n, hurt_pm's judge) and Raiden's land
  input    the real F path (rlk:tick's pre-pass lines -> player/def/input -> f_key -> press): an accepted press stamps
           parAt = now and locks #parGap; a press inside the lockout is ignored and blocks every press for #parRe ticks
           (#parMl cb); refusals (map, selection, dead, burst cast, Ronova revival, Raiden camera); Shift+F is not a
           parry; a right-click on the eye shield is consumed by the pre-pass (dodge in the same tick); the held
           use-item click (rcU) fires on ticks 1, 5, 9 ... only, with no fail sound while held (review A-02); F and a
           right-click in one tick both act (A-08); a player without stamps keeps the first dodge and the dodge-start
           box always goes (A-07)
  lock     review A-01: the whiff streak (lock 12 / 24 / 36 / 48 t, cleared by a pause or a tier 2-3 parry, kept by tier
           1), presses every 1-2 t are accepted once, blind pressing at every period 1-40 t and at irregular gaps keeps
           <= 10 % of the ticks in a perfect window (and of real strikes), legit play is never refused (h - 1 for chains
           with gaps >= 10 t, F every 3 t and every 2 t in any phase), one mistimed or stray press costs at most the
           next hit, mashing through a 3-t string parries one cut
  judge    the order i-frames > perfect dodge > perfect parry > loose dodge > tier 2 > tier 1 > hit, the outputs
           (#dodged / #parT / #pdg), the one-shot context reset, no-dodge (ignores dodges and i-frames), no-parry
  tiers    the real hit (cm/hit_me -> cm/hit_pl -> hit_pl2 -> take_damage) with F pressed 0..12 t before the hit: tier 3
           at 0-2 t (no damage), tier 2 at 3-5 t (20 % kept), tier 1 at 6-9 t (50 % kept), none at 10+; one press parries
           every hit of one tick, then it is spent; no knockback / hurt flash on a parry
  dodge    perfect 0-2 t for every class; loose 3-6 t for normal and elite, not for bosses; 7+ nothing
  cool     review A-12: the dodge cooldown is 18 t after a dodge that avoided nothing and 12 t after one that avoided an
           attack (perfect or loose; the refund once per dodge); 질주 2 = 14 / 10; the fail sound only on a fresh press
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
           the perfect dodge's red ghost and wash, the effect entities age out; nothing is aged away in its spawn tick
           (A-05: the jolt's two turns are one tick apart, the star grows after its first tick); the ghost is never
           killed where it stood (A-03: glow off and moved to the far chunk first), it faces as the body did (A-06);
           the crosshair is sent in the tick an overlay ends (A-09)
  beat     round V, lane VP (the perfect parry / dodge beat, #btOn tmp 1): the hold schedule and the untouchable ticks of both
           beats, the clock (#now cb counts world ticks, #btLag grows by N = 5 / 7), (a)(b) the same scripted fights with the
           beat on and off give identical events on the beat's clock and take exactly N real ticks more per beat (chains 10 /
           3 / 2 t apart, mistimed presses, dodge cooldowns), (c) nothing hurts during a beat, (d) back-to-back beats, (e)
           death / revival wait / selection space / map / cutscene / camera lock / reload / lost tag leave nothing held,
           a freeze started during the hold survives the release, the gates and clock users are in place, the idle cost
  beatloop beatloop_hr.py (홍련's two gauntlets and her free fight in the suites' H1 world, same proof) and
           beatloop_cb.py for the three mid-bosses: a real fight with the beat on = the same fight with it off, world tick by
           world tick (every `# mb` score, the body, the hazard clocks, health, the dodge cooldown), held = 5 / 7 per beat
  bossloop review A-11: a real mid-boss fight (the vendored azsim world of tools/dev/sim/hr/tests/lib, read only) with
           rlk:tick's pre-pass lines and its mboss/near_all line in the world loop: the pre-pass runs every tick, the
           near pass only in the window, a dodge whose body has left finds its perfect dodge through near_all
  cost     the pre-pass costs a handful of commands per idle tick

Harness: lib/psim.py + lib/mcsim.py (lane R's vendored harness) with gametime (`time query gametime` = s.gt) and a call log.
Prints one line per check; exit 1 on any failure. Run it from a copy outside the datapack (tools/dev/sim/README.md 1).
"""
import random
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
from psim import PSim, Ent, Ctx, pctx  # noqa: E402
from mcsim import split  # noqa: E402

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
                      'rlk:player/def/fx/glint', 'rlk:char/motion/guard', 'rlk:mboss/hurt_dodge', 'rlk:combat/rclick_do',
                      'rlk:player/dash_fail', 'rlk:snd/f228', 'rlk:char/cast_skill_r', 'rlk:bal/take', 'rlk:bal/grog/start',
                      'rlk:view/xhair', 'rlk:player/def/box_end', 'rlk:player/def/beat/start_p', 'rlk:player/def/beat/start_d',
                      'rlk:player/def/beat/end', 'rlk:player/def/beat/rock_on', 'rlk:player/def/beat/rock_off',
                      'rlk:char/motion/beat/parry', 'rlk:char/motion/beat/dodge', 'rlk:char/motion/beat/wglow_off',
                      'rlk:char/motion/beat/tint_off', 'rlk:player/def/fx/p3_star', 'rlk:player/def/fx/p3_shatter',
                      'rlk:player/def/fx/p3_bolt', 'rlk:player/def/beat/hold_on', 'rlk:player/def/beat/hold_off'}
        self.titles = []
        self.cmdlog = []                 # (gametime, text) of the rotate / data merge entity commands
        self.killed = []                 # (type, tags, position, data) of every entity a kill removed

    def cmd(self, t, ctx):
        if t[:3] == ['time', 'query', 'gametime']:
            self.n += 1
            return self.gt
        if t[0] == 'title':
            self.titles.append(' '.join(t[1:]))
        if t[0] == 'rotate' and len(t) == 4:               # relative to the command's rotation, as the game does
            self.n += 1
            self.cmdlog.append((self.gt, ' '.join(t)))
            for e in self.select(t[1], ctx):
                e.rot = [ctx.rot[i] + float(v[1:] or 0) if v.startswith('~') else float(v) for i, v in enumerate(t[2:4])]
            return 1
        if t[:3] == ['data', 'merge', 'entity'] and len(t) >= 5:
            self.n += 1
            self.cmdlog.append((self.gt, ' '.join(t)))
            m = re.search(r'Glowing:(\d)b', t[4])
            m2 = re.search(r'NoAI:(\d)b', t[4])
            for e in (self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]):
                if m:
                    e.data['Glowing'] = int(m.group(1))
                if m2:
                    e.data['NoAI'] = int(m2.group(1))
            return 1
        if t[0] == 'kill' and len(t) == 2 and t[1].startswith('@'):   # the game's result: how many it removed (0 = it fails)
            self.n += 1
            es = self.select(t[1], ctx)
            for e in es:
                self.killed.append((e.etype, sorted(e.tags), tuple(e.pos), dict(e.data)))
                e.alive = False
            self.ents = [e for e in self.ents if e.alive]
            return len(es)
        if t[:3] == ['data', 'remove', 'entity'] and len(t) == 5 and re.fullmatch(r'[A-Za-z_]+', t[4]):
            self.n += 1
            for e in (self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]):
                e.data.pop(t[4], None)
            return 1
        return super().cmd(t, ctx)

    def execute(self, t, ctx):
        # `if|unless data entity <sel> interaction|attack` at the head of an execute (after `as <sel>` too: psim recurses
        # here): a click the entity really holds. psim answers every entity data test with true, so every eye shield in
        # the world would be "clicked" on every tick
        if len(t) > 4 and t[0] in ('if', 'unless') and t[1:3] == ['data', 'entity'] and t[4] == '{NoAI:1b}':
            es = self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]
            if (bool(es) and es[0].data.get('NoAI') == 1) == (t[0] == 'unless'):
                return 0
            return self.execute(t[5:], ctx) if len(t) > 5 else 1
        if len(t) > 4 and t[0] in ('if', 'unless') and t[1:3] == ['data', 'entity'] and t[4] in ('interaction', 'attack'):
            es = self.select(t[3], ctx)
            if (bool(es) and t[4] in es[0].data) == (t[0] == 'unless'):
                return 0
            return self.execute(t[5:], ctx) if len(t) > 5 else 1
        return super().execute(t, ctx)

    def select(self, sel, ctx):
        res = super().select(sel, ctx)                     # (mcsim ignores the argument it does not know)
        m = re.search(r'[\[,]x_rotation=([^,\]]+)', sel)
        if m:
            lo, dots, hi = m.group(1).partition('..')
            hi = hi if dots else lo
            res = [e for e in res if (lo == '' or e.rot[1] >= float(lo)) and (hi == '' or e.rot[1] <= float(hi))]
        return res

    def call(self, fid, ctx, macro=None):
        if fid in self.watch:
            self.log.append((fid, sorted(ctx.ex.tags) if ctx.ex is not None else None, macro, tuple(ctx.pos)))
        return super().call(fid, ctx, macro)

    def calls(self, fid):
        return [c for c in self.log if c[0] == fid]


def world(beat=0):
    """beat: #btOn tmp. The sections written before round V test the combat logic in un-slowed terms, so they run with
    the perfect parry / dodge beat's world hold off (0: effects only, exactly the 11-11b clock); the `beat` section (and
    test_beat.py) runs with it on (1, the pack's default) and proves the two agree."""
    s = CSim(FN)
    pl = Ent('player', (0.5, 64.0, 0.5), (0.0, 0.0), ['player', 'rlk_body'])
    s.ents.append(pl)
    s.player = pl
    s.call('rlk:load', Ctx(None, (0, 0, 0), (0, 0)))
    s.btOnLoad = s.sc('#btOn', 'tmp')
    s.setsc('#btOn', 'tmp', beat)
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


UI = {'id': 'minecraft:stick', 'count': 1, 'c': {'minecraft:custom_data': {'rlk_ui': {'role': 'attack'}}}}
C0 = Ctx(None, (0, 0, 0), (0, 0))
_TICK = code(rd('tick'))
_I0 = next(i for i, l in enumerate(_TICK) if l.startswith('execute store result score #now cb run time query gametime'))
_I1 = next((i for i, l in enumerate(_TICK) if 'player/def/box_end' in l), None)
if _I1 is None:                          # (the tree before the review fixes: the kill line)
    _I1 = next(i for i, l in enumerate(_TICK) if 'kill @e[tag=rlk_dgo]' in l)
PRE = _TICK[_I0:_I1 + 1]                 # rlk:tick's pre-pass: #now, player/def/input, #dgOpen, the dodge-start box
COOL = next(l for l in code(rd('player/tick')) if 'remove @s dashCool 1' in l)


def prepass(s, f=False, rc=False, swap=False, rcu=False, item=None):
    """The next game tick's pre-pass, run from rlk:tick's own lines. f: F was pressed (the held item is in the off hand;
    swap = the main hand is empty, as the real swap leaves it); rc: a right-click sits on the eye shield; rcu: the F5
    use-item click (the advancement of the tick before). Returns (F accepted, dodge started)."""
    s.gt += 1
    pl = s.player
    inv = s.inv_of(pl)
    it = dict(item or UI)
    inv['hotbar.0'] = dict(it)
    if f:
        inv['weapon.offhand'] = dict(it)
        P(s, 'sneakT', 0)
        if swap:
            inv.pop('hotbar.0', None)
    if rc:
        sh = getattr(s, 'eye', None)
        if sh is None or sh not in s.ents:
            sh = s.eye = Ent('interaction', (0.5, 65.6, 0.8), (0.0, 0.0), ['atkBlock'])
            s.ents.append(sh)
        sh.data['interaction'] = {'timestamp': s.gt}
    if rcu:
        P(s, 'rcU', 1)
    a0, d0 = P(s, 'parAt'), P(s, 'dgAt')
    for l in PRE:
        s.cmd(split(l), C0)
    inv.pop('weapon.offhand', None)
    inv['hotbar.0'] = dict(it)
    return P(s, 'parAt') == s.gt and a0 != s.gt, P(s, 'dgAt') == s.gt and d0 != s.gt


def cooldown(s):
    """player/tick's dodge cooldown line (the rest of player/tick is not needed here)"""
    s.cmd(split(COOL), pctx(s))


def fresh(s):
    """no press, no dodge, no lock, no streak (the state of a new player)"""
    nopress(s)
    P(s, 'parLk', -1000000)
    P(s, 'dashCool', 0)
    for n, v in (('#parWs', 0), ('#parMl', -1000000), ('#dgRf', -1000000), ('#dgTry', -1000000)):
        s.setsc(n, 'cb', v)


def no_errors(s, name):
    # (fx/t_star stores an entity's transformation: psim has no entity NBT store)
    bad = {k: v for k, v in s.errors.items() if k[0].startswith(('rlk:player/def', 'rlk:player/f_key', 'rlk:player/dash',
                                                                  'rlk:combat/rc', 'rlk:engravings/'))
           and k[0] not in ('rlk:player/def/fx/t_star', 'rlk:player/def/fx/t_burst')}
    ck(f'{name}: the simulator ran every command of the parry / dodge functions (no swallowed error)', not bad, list(bad)[:4])


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
    inp = code(fns['player/def/input'])
    i_rst = next((i for i, l in enumerate(inp) if 'set @s rcT 0' in l), -1)
    i_rc = next((i for i, l in enumerate(inp) if 'function rlk:player/def/rc' in l and 'rc_int' not in l), -1)
    ck('static: the pre-pass tests the release (rcT 0 unless rcU) before player/def/rc clears rcU (review A-02)', -1 < i_rst < i_rc, (i_rst, i_rc))
    ck('static: rlk:tick removes the dodge-start box through player/def/box_end (#dgBox, now >= #dgKill; review A-07)',
       any('#dgBox cb matches 1' in l and '#now cb >= #dgKill cb' in l and 'player/def/box_end' in l for l in tick))
    ck('static: dodge_stamp initialises a player without stamps before it writes, flags the box and turns it as the body '
       '(reviews A-07, A-06)', all(x in fns['player/def/dodge_stamp'] for x in (
           'unless score @s parHit matches -2147483648.. run function rlk:player/def/reset', 'set #dgBox cb 1',
           'rotated as @e[tag=rlk_body,limit=1] as @e[tag=rlk_dgo,limit=1] run rotate @s ~ 0'))
       and fns['player/def/dodge_stamp'].index('player/def/reset') < fns['player/def/dodge_stamp'].index('operation @s dgAt = #now cb'))
    ck('static: no effect entity is removed with a bare kill while it is a living ghost: fx/tick sends the mannequin through '
       'fx/ghost_out one tick before its end, pd_ghost never kills (review A-03)',
       'kill' not in '\n'.join(code(fns['player/def/fx/pd_ghost'])) and 'fx/ghost_out' in fns['player/def/fx/pd_ghost']
       and code(fns['player/def/fx/tick']).index(next(l for l in code(fns['player/def/fx/tick']) if 'fx/ghost_out' in l))
       < code(fns['player/def/fx/tick']).index(next(l for l in code(fns['player/def/fx/tick']) if 'run kill @s' in l))
       and all(x in fns['player/def/fx/ghost_out'] for x in ('Glowing:0b', 'in minecraft:overworld run tp @s 1000000.5 400 1000000.5'))
       and 'forceload add 1000000 1000000' in fns['load'])
    vt = code(fns['view/tick'])
    arm, dec = 'execute if score @s vBig matches 1 run scoreboard players set #xh view 9', 'execute if score @s vBig matches 1.. run scoreboard players remove @s vBig 1'
    ck('static: view/tick re-arms the crosshair (#xh view 9) on the tick vBig ends, right before its one count-down line (review A-09)',
       arm in vt and dec in vt and vt.index(arm) + 1 == vt.index(dec))
    hud = fns['player/hud/tick']
    ck('static: the HUD actionbar has no dash gauge', 'line[]' not in hud and 'dashRegen' not in hud)
    lores = [k for k in fns if re.match(r'char/[a-z]+/def$', k)]
    ck('static: the 7 weapon lores and the tutorial give both dodge cooldowns (0.9초, 피하면 0.6초)', all(
        '0.9초' in fns[k] and '0.6초' in fns[k] for k in lores + ['lobby/tut/s1']), [k for k in lores + ['lobby/tut/s1'] if '0.9초' not in fns[k]])
    ck('static: all 7 weapon lores say 우클릭 · 닷지 and F 키 · 패링 (no 대쉬)', len(lores) == 7 and all(
        '우클릭 · 닷지' in fns[k] and 'F 키 · 패링' in fns[k] and '대쉬' not in fns[k] for k in lores), lores)
    user = [k for k, v in fns.items() if ('대쉬' in '\n'.join(l for l in v.split('\n') if not l.lstrip().startswith('#')))
            and not k.startswith(('player/def', 'load'))]
    ck('static: no user-facing text says 대쉬 any more', not user, user[:8])
    ck('static: the tutorial step 1 is 이동 · 닷지 · 패링 (target 닷지 · 패링 3번)', '이동 · 닷지 · 패링' in fns['lobby/tut/s1']
       and '닷지 · 패링 3번 하기' in fns['lobby/tut/s1'])
    ck('static: 질주 (2) = 닷지 재사용 대기 -20 % (lore and engravings/scan_more: both cooldowns)', '닷지 재사용 대기 ' in fns['engravings/register']
       and '#dashCoolBase' in fns['engravings/scan_more'] and '#dashCoolHitBase' in fns['engravings/scan_more'])
    ck('static: 화무십일홍 lore: 닷지 · 패링으로 흘려내면', '닷지 · 패링으로 흘려내면' in fns['items/mythic/sword_hwamu/def'])
    # generated framework lines
    npd = fns.get('mboss/hz/np_def', '')
    # (review B-01, fix lane FB: no size thresholds any more; the details are test_np.py's)
    ck('static: hz/np_def: unparriable by default only no-dodge, per mille, re-arm, full / mask (no size threshold)',
       all(x in npd for x in ('mbHzND matches 1 run return run scoreboard players set @s mbHzNP 1',
                              'mbHzPm matches 1.. run return run scoreboard players set @s mbHzNP 1',
                              'mbHzRA matches 1.. run return run scoreboard players set @s mbHzNP 1',
                              'mbHzK matches 5..6 run scoreboard players set @s mbHzNP 1'))
       and 'mbHzR ' not in npd
       and npd.split('\n').index('scoreboard players set @s mbHzNP 0') < npd.split('\n').index('execute if score @s mbHzND matches 1 run return run scoreboard players set @s mbHzNP 1'))
    ck('static: hz/init sets mbHzNP from #hzNoParry or np_def; the glint is hz/np_auto\'s (unparriable, dodgeable, tell >= 12)',
       'mbHzNP = #hzNoParry mb' in fns['mboss/hz/init'] and 'mboss/hz/np_auto' in fns['mboss/hz/init']
       and 'function rlk:mboss/np_glint' in fns.get('mboss/hz/np_auto', ''))
    ck('static: opts_reset resets #hzNoParry / #pjNoParry to -1', 'set #hzNoParry mb -1' in fns['mboss/opts_reset']
       and 'set #pjNoParry mb -1' in fns['mboss/opts_reset'])
    ck('static: mboss/hurt -> hurt_ctx -> cm/hit_pl2 (one path; no zero-and-restore of dashInvT)',
       'function rlk:mboss/hurt_ctx' in fns['mboss/hurt'] and 'hurt_nd' not in fns['mboss/hurt'] and 'dashInvT' not in fns['mboss/hurt'])
    ck('static: hz/hurt_pm calls the judge (no own dash check)', 'player/def/judge' in fns['mboss/hz/hurt_pm']
       and 'dashInvT' not in fns['mboss/hz/hurt_pm'])
    near = [l for l in tick if 'mboss/near_all' in l]
    # (HI, 11-11: lane H2's FN-cam hold / release lines sit right after mboss/main as well - they alone may stand between)
    ck('static: rlk:tick runs mboss/near_all right after mboss/main (FN-cam\'s lines only between), only in the window (live, not paused); hz/near and pj/near '
       'are dodgeable-only; mboss/world, hz/all, pj/all and pj/tick carry no lane C line',
       len(near) == 1 and tick.index(near[0]) > i_mb and all('rlk:mboss/cam/' in l for l in tick[i_mb + 1:tick.index(near[0])])
       and '#dgOpen cb matches 1' in near[0] and '#mbPause mb matches 1' in near[0]
       and 'mboss/hz/near' in fns['mboss/near_all'] and 'mboss/pj/near' in fns['mboss/near_all']
       and 'unless score @s mbHzND matches 0 run return 0' in fns['mboss/hz/near']
       and 'unless score @s mbPjND matches 0 run return 0' in fns['mboss/pj/near']
       and not any(x in fns[f] for f in ('mboss/world', 'mboss/hz/all', 'mboss/pj/all', 'mboss/pj/tick') for x in ('dgOpen', 'near')))
    ck('static: Raiden land sets the context, land_nd = #hcND 1 without dashInvT, try re-tests at the dodge start',
       '#hcNP tmp 1' in fns['boss/raiden/hazard/land'] and 'dashInvT' not in fns['boss/raiden/hazard/land_nd']
       and '#hcND tmp 1' in fns['boss/raiden/hazard/land_nd'] and 'hazard/try_near' in fns['boss/raiden/hazard/try'])
    ck('static: rlk:bal/hit is lane B\'s (takes #n bal through bal/take) and the perfect parry calls it as the attacker',
       'function rlk:bal/take' in fns.get('bal/hit', '')
       and 'execute as @e[tag=rlk_hc_atk,limit=1] at @s run function rlk:bal/hit {n:1}' in fns['player/def/par3_go'])
    ck('static: the guard clip exists for the three rig characters', all(f'char/motion/clips/{c}/guard/start' in fns
       for c in ('arle', 'skirk', 'navia')) and fns.get('char/motion/guard', '').count('clip:"guard"') == 3)
    gl = fns.get('player/def/fx/g/glint', '') + fns.get('player/def/fx/g/t_streak', '')
    ck('static: the glyph commands name the font rlk:cb on every component with an empty root', 'font:"rlk:cb"' in gl
       and '{text:"",extra:[' in gl)


# ================================================================================================== input
def t_input():
    s, pl = world()
    inv = s.inv_of(pl)
    fresh(s)
    s.log.clear()
    acc, _ = prepass(s, f=True)
    ck('input: F (offhand UI item, no sneak) -> parAt = now, lock until now + #parGap', acc and P(s, 'parAt') == s.gt
       and P(s, 'parLk') == s.gt + G(s, '#parGap'), (P(s, 'parAt'), P(s, 'parLk')))
    ck('input: the press plays the guard (char/motion/guard)', bool(s.calls('rlk:char/motion/guard')))
    t0 = s.gt
    prepass(s)
    prepass(s)
    acc, _ = prepass(s, f=True)
    ck('input: a press inside the lockout is ignored (parAt and parLk kept) and blocks every press until now + #parRe (#parMl cb)',
       not acc and P(s, 'parAt') == t0 and P(s, 'parLk') == t0 + G(s, '#parGap') and G(s, '#parMl', 'cb') == s.gt + G(s, '#parRe'),
       (P(s, 'parAt'), P(s, 'parLk'), G(s, '#parMl', 'cb'), s.gt))
    for _ in range(40):
        prepass(s)
    acc, _ = prepass(s, f=True)
    ck('input: after a pause longer than the lock, F is accepted again', acc)
    for o, v in (('vMap', 1), ('pkMode', 1), ('dead', 1), ('buT', 5), ('rnDie', 3), ('rdCam', 1), ('pmMoveLock', 1)):
        fresh(s)
        P(s, o, v)
        acc, _ = prepass(s, f=True)
        ck(f'input: refused while {o} {v}', not acc and P(s, 'parAt') == -1000000)
        P(s, o, 0)
    fresh(s)
    s.gt += 1
    inv['weapon.offhand'] = dict(UI)
    P(s, 'sneakT', 1)
    for l in PRE:
        s.cmd(split(l), C0)
    inv.pop('weapon.offhand', None)
    P(s, 'sneakT', 0)
    ck('input: Shift+F (sneakT >= 1) is not a parry (player/hotbar/tick keeps lvup/toggle)', P(s, 'parAt') == -1000000)
    # right-click on the eye shield, consumed by the pre-pass: the dodge starts in this tick
    fresh(s)
    _, dg = prepass(s, rc=True)
    sh = s.eye
    ck('input: a right-click on the eye shield is consumed by the pre-pass and dodges in the same tick (dgAt = now)',
       dg and 'interaction' not in sh.data and P(s, 'dashCool') == G(s, '#dashCoolT'), (sh.data, P(s, 'dgAt'), s.gt))
    ck('input: the dodge leaves its start box rlk_dgo and opens the window (#dgEnd = now + 2, #dgOpen 1)',
       len(s.select('@e[tag=rlk_dgo]', pctx(s))) == 1 and G(s, '#dgEnd', 'cb') == s.gt + G(s, '#dgPW') - 1 and G(s, '#dgOpen', 'cb') == 1)
    opened = []
    for _ in range(4):
        prepass(s)
        opened.append((G(s, '#dgOpen', 'cb'), len(s.select('@e[tag=rlk_dgo]', pctx(s)))))
    ck('input: rlk:tick keeps the window open 2 more ticks and removes the box on the tick after (player/def/box_end)',
       opened == [(1, 1), (1, 1), (0, 0), (0, 0)] and G(s, '#dgBox', 'cb') == 0, opened)
    # a chapter boss's hit proxy (rlk_mb_px) and a foreign interaction (a lobby object): the proxy's right-click is consumed
    # by the pre-pass too, the foreign one is left alone
    fresh(s)
    px = Ent('interaction', (3.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mb_px', 'boss'])
    lo = Ent('interaction', (5.5, 64.0, 0.5), (0.0, 0.0), ['rlk_lobj'])
    s.ents += [px, lo]
    px.data['interaction'] = {'timestamp': s.gt + 1}
    lo.data['interaction'] = {'timestamp': s.gt + 1}
    _, dg = prepass(s)
    ck('input: a boss proxy right-click is consumed by the pre-pass (dodge now), a lobby interaction is left alone',
       'interaction' not in px.data and 'interaction' in lo.data and dg)
    t1 = P(s, 'dgAt')
    for _ in range(5):
        prepass(s)
        cooldown(s)
    s.call('rlk:player/dash', pctx(s))
    ck('input: a second dodge inside the cooldown is refused (no charges any more)', P(s, 'dgAt') == t1)
    # review A-02: the F5 use-item click (rcU, set by the advancement of the tick before) held for 30 ticks
    fresh(s)
    s.log.clear()
    hold, rct, dodges = [], [], []
    for k in range(30):
        for key in [key for key in s.scores if key[1] == 'snd']:
            del s.scores[key]                              # rlk:tick line 3
        n0 = len(s.calls('rlk:combat/rclick_do'))
        _, dg = prepass(s, rcu=True)
        if len(s.calls('rlk:combat/rclick_do')) > n0:
            hold.append(k)
        if dg:
            dodges.append(k)
        rct.append(P(s, 'rcT'))
        cooldown(s)
    ck('input: a held use-item click (rcU every tick, 30 t) is a right-click on ticks 0, 4, 8 ... only (review A-02)',
       hold == list(range(0, 30, 4)), hold)
    ck('input: ... rcT counts the held ticks (1..30) and the dodge repeats only when the cooldown is over',
       rct == list(range(1, 31)) and dodges == [0, 20], (rct[:6], dodges))
    ck('input: ... and no fail sound plays while it is held (dash_fail is silent on the 4-t repeats)',
       len(s.calls('rlk:player/dash_fail')) == 6 and not s.calls('rlk:snd/f228'), (len(s.calls('rlk:player/dash_fail')), len(s.calls('rlk:snd/f228'))))
    prepass(s)
    ck('input: ... the tick after the release rcT is 0 again', P(s, 'rcT') == 0, P(s, 'rcT'))
    # a skill item held the same way: the skill is cast on ticks 0 and 4, not on every tick
    fresh(s)
    s.stub.add('rlk:char/cast_skill_r')
    s.log.clear()
    SK = {'id': 'minecraft:stick', 'count': 1, 'c': {'minecraft:custom_data': {'rlk_ui': {'role': 'skill'}}}}
    for k in range(6):
        prepass(s, rcu=True, item=SK)
    ck('input: a held skill item casts on ticks 0 and 4 only (스커크 fast move no longer ends one tick after it starts)',
       len(s.calls('rlk:char/cast_skill_r')) == 2, len(s.calls('rlk:char/cast_skill_r')))
    s.stub.discard('rlk:char/cast_skill_r')
    prepass(s)
    inv['hotbar.0'] = dict(UI)
    # a fresh click inside the cooldown plays the fail sound once; its 4-t repeat (a held click on the eye shield) is silent
    fresh(s)
    prepass(s, rc=True)
    for _ in range(7):
        prepass(s)
        cooldown(s)
    s.log.clear()
    prepass(s, rc=True)
    a1 = len(s.calls('rlk:snd/f228'))
    for _ in range(3):
        prepass(s)
    prepass(s, rc=True)
    ck('input: a new click inside the cooldown plays the fail sound, the repeat 4 t later does not',
       a1 == 1 and len(s.calls('rlk:snd/f228')) == 1 and len(s.calls('rlk:player/dash_fail')) == 2, (a1, len(s.calls('rlk:snd/f228'))))
    # review A-08: F and a right-click in one tick (the swap has emptied the main hand)
    fresh(s)
    acc, dg = prepass(s, f=True, rc=True, swap=True)
    ck('input: F and a right-click in the same tick both act (parry stamp and dodge; review A-08)',
       acc and dg and 'interaction' not in s.eye.data and P(s, 'dashCool') == G(s, '#dashCoolT'), (acc, dg, P(s, 'dashCool')))
    # review A-07: a player saved before the overhaul (no stamps at all): the first dodge is kept, the box goes
    e = brain(s)
    for o in ('parAt', 'parLk', 'parHit', 'dgAt', 'dgRw'):
        s.scores.pop((('e', pl.id), o), None)
    P(s, 'dashCool', 0)
    P(s, 'energy', 0)
    _, dg = prepass(s, rc=True)
    lost = cm_hit(s, e, 60)
    ck('input: a player without stamps: the dodge and a strike in the same tick = a perfect dodge (review A-07)',
       dg and lost == 0 and G(s, '#pdg') == 1 and P(s, 'dgAt') == s.gt and P(s, 'energy') == 1000, (dg, lost, G(s, '#pdg'), P(s, 'energy')))
    for _ in range(4):
        prepass(s)
    ck('input: ... and the dodge-start box is removed after the window', not s.select('@e[tag=rlk_dgo]', pctx(s)))
    # a box that could not be removed on its tick (rlk:tick returned early, its chunk was not loaded, a server stop)
    fresh(s)
    prepass(s, rc=True)
    s.gt += 6                                              # the ticks of the window and the kill tick never ran
    prepass(s)
    ck('input: a dodge-start box that missed its tick is removed on the next tick that runs', not s.select('@e[tag=rlk_dgo]', pctx(s))
       and G(s, '#dgBox', 'cb') == 0)
    fresh(s)
    P(s, 'dashCool', 0)
    prepass(s, rc=True)
    box = s.select('@e[tag=rlk_dgo]', pctx(s))[0]
    s.ents.remove(box)                                     # (its chunk is not loaded: the kill finds nothing)
    for _ in range(5):
        prepass(s)
    f1 = G(s, '#dgBox', 'cb')
    s.ents.append(box)
    prepass(s)
    ck('input: ... while its chunk is not loaded the removal is retried every tick (#dgBox stays 1) until it succeeds',
       f1 == 1 and not s.select('@e[tag=rlk_dgo]', pctx(s)) and G(s, '#dgBox', 'cb') == 0, (f1, G(s, '#dgBox', 'cb')))
    fresh(s)
    P(s, 'dashCool', 0)
    prepass(s, rc=True)
    s.ents.remove(s.select('@e[tag=rlk_dgo]', pctx(s))[0])
    s.gt += 210
    prepass(s)
    ck('input: ... and the retry stops after 200 t (the next dodge removes a leftover)', G(s, '#dgBox', 'cb') == 0)
    no_errors(s, 'input')


# ================================================================================================== the parry lock (A-01)
def chain(s, e, hits, presses):
    """One fight on the real path: F in the pre-pass of the ticks in `presses`, a real strike (cm/hit_me) on the ticks in
    `hits` (tick numbers from 0; the ticks between are skipped: the lock is made of game-time stamps only).
    -> (tier per hit, number of presses that were not accepted)"""
    fresh(s)
    t0 = s.gt
    tiers, refused = [], 0
    for t in sorted(set(hits) | set(presses)):
        s.gt = t0 + t
        acc, _ = prepass(s, f=(t in presses))
        refused += (t in presses) and not acc
        if t in hits:
            cm_hit(s, e, 60)
            tiers.append(G(s, '#parT'))
    return tiers, refused


def blind(s, e, press, total, st=None):
    """Blind pressing: F on the ticks of `press`. Without strikes: the share of ticks in which a parriable strike would
    get tier 3 / 2 / 1 / none. With strikes (a set of ticks): per-strike tiers and the damage taken. Ticks without a
    press or a strike only read the stamps."""
    fresh(s)
    w3, w2, w1 = G(s, '#parW3'), G(s, '#parW2'), G(s, '#parW1')
    share, tiers, acc, lost = [0, 0, 0, 0], [0, 0, 0, 0], 0, 0
    t0 = s.gt
    for t in range(total):
        if t in press or (st is not None and t in st):
            s.gt = t0 + t
            a, _ = prepass(s, f=(t in press))
            acc += a
        now = t0 + t + 1
        p = now - P(s, 'parAt')
        k = 0
        if P(s, 'parHit') < P(s, 'parAt') and p >= 0:
            k = 3 if p < w3 else 2 if p < w2 else 1 if p < w1 else 0
        share[k] += 1
        if st is not None and t in st:
            lost += cm_hit(s, e, 60)
            tiers[G(s, '#parT')] += 1
    s.gt = t0 + total
    return acc, [100.0 * x / total for x in share], tiers, lost


def t_lock():
    s, pl = world()
    e = brain(s)
    # thousands of parries follow: their effect entities (never aged here) would only slow every selector down
    s.stub |= {'rlk:player/def/fx/p1', 'rlk:player/def/fx/p2', 'rlk:player/def/fx/p3', 'rlk:player/def/guard'}
    ck('lock: the constants (load): #parGap 12, streak cap 3 within 80 t, cleared from tier 2, #parRe 3, #parChain 1',
       (G(s, '#parGap'), G(s, '#parWsMax'), G(s, '#parWsT'), G(s, '#parWsClr'), G(s, '#parRe'), G(s, '#parChain')) == (12, 3, 80, 2, 3, 1),
       (G(s, '#parGap'), G(s, '#parWsMax'), G(s, '#parWsT'), G(s, '#parWsClr'), G(s, '#parRe'), G(s, '#parChain')))
    gap = G(s, '#parGap') or 12
    # the whiff streak: every accepted press that follows an unused one within #parWsT lengthens the lock
    fresh(s)
    locks = []
    for k in range(6):
        acc, _ = prepass(s, f=True)
        locks.append((acc, P(s, 'parLk') - s.gt, G(s, '#parWs', 'cb')))
        for _ in range(P(s, 'parLk') - s.gt - 1):
            prepass(s)
    ck('lock: unused presses one after the other: the lock is 12 / 24 / 36 / 48 / 48 t (the whiff streak 0-3)',
       locks == [(True, gap * (min(k, 3) + 1), min(k, 3)) for k in range(6)], locks)
    for _ in range(81):
        prepass(s)
    acc, _ = prepass(s, f=True)
    ck('lock: a pause longer than #parWsT after an unused press clears the streak (lock 12 again)',
       acc and P(s, 'parLk') - s.gt == gap and G(s, '#parWs', 'cb') == 0, (acc, P(s, 'parLk') - s.gt, G(s, '#parWs', 'cb')))

    def streak2():
        fresh(s)
        prepass(s, f=True)
        for _ in range(gap - 1):
            prepass(s)
        prepass(s, f=True)
        for _ in range(2 * gap - 1):
            prepass(s)
        prepass(s, f=True)                                 # the third unused press in a row: streak 2
        return G(s, '#parWs', 'cb')
    for ago, tier, keep in ((7, 1, True), (4, 2, False), (1, 3, False)):
        w = streak2()
        for _ in range(ago):
            prepass(s)
        cm_hit(s, e, 30)
        got = (G(s, '#parT'), G(s, '#parWs', 'cb'), P(s, 'parLk') - s.gt)
        acc, _ = prepass(s, f=True)
        ck(f'lock: streak 2, then a tier-{tier} parry: the streak is {"kept" if keep else "cleared"}, the next press is taken '
           f'on the next tick (lock {gap * (3 if keep else 1)})', w == 2 and got == (tier, 2 if keep else 0, G(s, '#parChain'))
           and acc and P(s, 'parLk') - s.gt == gap * (3 if keep else 1), (w, got, acc, P(s, 'parLk') - s.gt))
    # ignored presses: nothing is accepted for #parRe ticks after one, a parry does not clear that
    fresh(s)
    prepass(s, f=True)
    for _ in range(gap - 2):
        prepass(s)
    a1, _ = prepass(s, f=True)                             # tick 11: inside the lock -> ignored
    a2, _ = prepass(s, f=True)                             # tick 12: the lock is over, but 1 t after an ignored press
    prepass(s)
    prepass(s)
    a3, _ = prepass(s, f=True)                             # 3 t after the last ignored press
    ck('lock: a press 1 t after an ignored press is ignored too (even with the lock over); 3 t after the last one it is taken',
       (a1, a2, a3) == (False, False, True), (a1, a2, a3))
    for per in (1, 2):
        acc, share, _, _ = blind(s, e, set(range(0, 240, per)), 240)
        ck(f'lock: F every {per} t for 240 t (mashing, a held key) is accepted once', acc == 1, acc)
    # blind pressing (the reviewer's loop 1): every regular period and irregular gaps
    worst = (0, None, 100, None, 0, None)
    pats = [(f'every {p} t', set(range(0, 600, p))) for p in range(3, 41)]
    for lo, hi in ((2, 3), (3, 4), (3, 5), (4, 6), (5, 8), (8, 14), (10, 20), (12, 30), (20, 40)):
        r, t, press = random.Random(7), 0, set()
        while t < 600:
            press.add(t)
            t += r.randint(lo, hi)
        pats.append((f'gaps {lo}-{hi} t', press))
    for name, press in pats:
        acc, share, _, _ = blind(s, e, press, 600)
        dmg = share[0] + 0.5 * share[1] + 0.2 * share[2]
        if share[3] > worst[0]:
            worst = (share[3], name) + worst[2:]
        if dmg < worst[2]:
            worst = worst[:2] + (dmg, name) + worst[4:]
        if acc > worst[4]:
            worst = worst[:4] + (acc, name)
    ck(f'lock: blind F at every period 3-40 t and 9 irregular rhythms, 600 t each: at most {worst[0]:.1f} % of the ticks are in a '
       f'perfect window (<= 10; {worst[1]}), a strike would still do {worst[2]:.1f} % of its damage (>= 70; {worst[3]}), at most '
       f'{worst[4]} presses accepted (<= 18; {worst[5]})', worst[0] <= 10 and worst[2] >= 70 and worst[4] <= 18, worst)
    # ... and against real strikes (the reviewer's loop 2: cm/hit_me at random 20-60 t gaps)
    r, t, st = random.Random(11), 0, set()
    while True:
        t += r.randint(20, 60)
        if t >= 9000:
            break
        st.add(t)
    _, _, _, base = blind(s, e, set(), 9000, st)
    out = []
    for name, press in (('every 4 t', set(range(0, 9000, 4))), ('every 12 t', set(range(0, 9000, 12))), ('every 13 t', set(range(0, 9000, 13)))):
        acc, _, tiers, lost = blind(s, e, press, 9000, st)
        out.append((name, round(100.0 * tiers[3] / len(st), 1), round(100.0 * lost / base, 1), acc))
    ck(f'lock: blind F against {len(st)} real strikes (9000 t): {out} (name, % perfect <= 10, % of the damage >= 70, presses)',
       all(o[1] <= 10 and o[2] >= 70 for o in out), out)
    # legit play is never refused
    for g_ in (10, 11, 12, 15, 20, 40):
        hits = [20 + g_ * i for i in range(7)]
        tiers, ref = chain(s, e, set(hits), {h - 1 for h in hits})
        ck(f'lock: F one tick before every hit of a {g_}-t chain: 7 perfect parries, no press refused', tiers == [3] * 7 and ref == 0, (tiers, ref))
    for g_, phases in ((3, (0, 1, 2)), (2, (0, 1))):
        for ph in phases:
            hits = [20 + g_ * i for i in range(9)]
            tiers, ref = chain(s, e, set(hits), {h - ph for h in hits})
            ck(f'lock: a {g_}-t string with F every {g_} t, {ph} t before each cut: 9 perfect parries, no press refused',
               tiers == [3] * 9 and ref == 0, (tiers, ref))
    # one mistake costs at most the next hit
    bad = []
    for g_ in (10, 11, 12, 13, 16, 24):
        hits = [40 + g_ * i for i in range(8)]
        proper = {h - 1 for h in hits}
        for early in range(10, 31):                        # the first press is too early
            tiers, _ = chain(s, e, set(hits), (proper - {hits[0] - 1}) | {hits[0] - early})
            if tiers[1:] != [3] * 7:
                bad.append(('early', g_, early, tiers))
        for late in range(1, g_ - 1):                      # a press comes after its hit
            tiers, _ = chain(s, e, set(hits), (proper - {hits[2] - 1}) | {hits[2] + late})
            if tiers[:2] != [3, 3] or tiers[4:] != [3] * 4:
                bad.append(('late', g_, late, tiers))
        for x in range(hits[2] + 1, hits[3] - 1):          # one extra press between two hits
            tiers, _ = chain(s, e, set(hits), proper | {x})
            if tiers[:3] != [3] * 3 or tiers[4:] != [3] * 4:
                bad.append(('stray', g_, x - hits[2], tiers))
    ck('lock: chains of 10-24 t: one press too early, one too late or one extra press costs at most the next hit '
       '(every later h - 1 press is a perfect parry)', not bad, bad[:4])
    bad = []
    hits = [20 + 3 * i for i in range(9)]
    for ph in (0, 1, 2):
        for k in range(1, 8):
            for dx in (1, 2):
                x = hits[k] - ph + dx
                presses = {h - ph for h in hits}
                if x in presses:
                    continue
                tiers, _ = chain(s, e, set(hits), presses | {x})
                if tiers.count(0) > 1 or len([t for t in tiers if t != 3]) > 2:
                    bad.append((ph, k, dx, tiers))
    ck('lock: a 3-t string: one extra F (a double tap) loses at most one cut', not bad, bad[:4])
    got = []
    for per in (1, 2):
        for start in range(10, 20):
            tiers, _ = chain(s, e, set(hits), set(range(start, hits[-1] + 1, per)))
            got.append(len([t for t in tiers if t]))
    ck('lock: mashing F every 1-2 t through a 3-t string parries the first cut or two (the first press, and a second one '
       '2 t later that follows a parry), never the string', max(got) <= 2, got)
    no_errors(s, 'lock')


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
    ck('tiers: after a parry the next press is allowed from the next tick (parLk = parry tick + #parChain 1)',
       P(s, 'parLk') == P(s, 'parHit') + G(s, '#parChain') and G(s, '#parChain') == 1)


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


# ================================================================================================== dodge cooldown (A-12)
def t_cool():
    s, pl = world()
    e = brain(s)
    ck('cool: #dashCoolT 18 (a dodge that avoided nothing), #dashCoolHitT 12 (one that avoided an attack)',
       (G(s, '#dashCoolT'), G(s, '#dashCoolHitT'), G(s, '#dashCoolBase'), G(s, '#dashCoolHitBase')) == (18, 12, 18, 12),
       (G(s, '#dashCoolT'), G(s, '#dashCoolHitT')))

    def again(hit_at=None, cls=0, hits=1):
        """a dodge on tick 0, a strike `hit_at` ticks later (or none), a right-click on every later tick: -> the tick of
        the next dodge, what the strike did"""
        fresh(s)
        P(s, 'energy', 0)
        prepass(s, rc=True)
        cooldown(s)
        res = None
        for k in range(1, 40):
            _, dg = prepass(s, rc=True)
            if dg:
                return k, res
            if hit_at is not None and k == hit_at:
                for _ in range(hits):
                    if cls == 2:
                        full(s)
                        hp0 = P(s, 'curHealth')
                        for o, v in (('#cmDmg', 60), ('#cmLv', 1), ('#cmEl', 0), ('#cmKB', 0), ('#hcC', 2), ('#hcK', 1)):
                            s.setsc(o, 'tmp', v)
                        s.call('rlk:cm/hit_pl2', pctx(s))
                        lost = hp0 - P(s, 'curHealth')
                    else:
                        lost = cm_hit(s, e, 60)
                res = (lost, G(s, '#pdg'))
            cooldown(s)
        return None, res
    ck('cool: a dodge that meets no attack: the next one 18 t later', again() == (18, None), again())
    ck('cool: a perfect dodge (strike 1 t after): the next one 12 t later', again(1) == (12, (0, 1)), again(1))
    ck('cool: ... also when the strike comes in the dodge tick itself or 2 t after', again(2) == (12, (0, 1)), again(2))
    ck('cool: a loose dodge of a normal mob (strike 5 t after): 12 t too', again(5) == (12, (0, 0)), again(5))
    ck('cool: two strikes avoided by one dodge refund once (12 t, not 6)', again(1, hits=2)[0] == 12, again(1, hits=2))
    r = again(4, cls=2)
    ck('cool: a boss strike 4 t after the dodge is not avoided: 18 t', r[0] == 18 and r[1][0] > 0, r)
    r = again(8)
    ck('cool: a strike after the window (8 t) lands: 18 t', r[0] == 18 and r[1][0] > 0, r)
    s.setsc('dash', 'engN', 2)
    s.call('rlk:engravings/scan_more', pctx(s))
    ck('cool: 질주 2 (-20 %, rounded): 14 t / 10 t after an avoided attack', (G(s, '#dashCoolT'), G(s, '#dashCoolHitT')) == (14, 10)
       and again()[0] == 14 and again(1)[0] == 10, (G(s, '#dashCoolT'), G(s, '#dashCoolHitT'), again()[0], again(1)[0]))
    s.setsc('dash', 'engN', 0)
    s.call('rlk:engravings/scan_more', pctx(s))
    ck('cool: without the engraving the two values are the base again', (G(s, '#dashCoolT'), G(s, '#dashCoolHitT')) == (18, 12))
    # dodging on every tick the cooldown allows, standing in a swordsman's reach (the reviewer's loop, 3000 t)
    r_, t, st = random.Random(11), 0, set()
    while True:
        t += r_.randint(20, 60)
        if t >= 3000:
            break
        st.add(t)
    fresh(s)
    s.stub |= {'rlk:player/def/fx/pd', 'rlk:player/dash_go'}
    s.cache_dash = None
    land = perf = dodges = 0
    s.stub.discard('rlk:player/dash_go')
    s.stub |= {'rlk:char/motion/dash', 'rlk:items/hook/on_dash', 'rlk:player/dash_dir'}
    for t in range(3000):
        _, dg = prepass(s, rc=True)
        dodges += dg
        cooldown(s)
        if t in st:
            lost = cm_hit(s, e, 60)
            perf += G(s, '#pdg') == 1
            land += lost > 0
    s.stub -= {'rlk:player/def/fx/pd', 'rlk:char/motion/dash', 'rlk:items/hook/on_dash', 'rlk:player/dash_dir'}
    n = len(st)
    ck(f'cool: dodging whenever the cooldown allows against {n} strikes of a normal mob: {land} land (>= 45 %), {perf} perfect '
       f'(<= 25 %), {dodges} dodges in 3000 t (<= 3000 / 12)', land >= 0.45 * n and perf <= 0.25 * n and dodges <= 250, (land, perf, dodges, n))
    no_errors(s, 'cool')


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
    tk = s.calls('rlk:bal/take')
    ck('bal: the pip is taken at the enemy (as the enemy, at its position; review B-05)', len(tk) == 1 and tk[0][3] == tuple(e.pos), tk)
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
    # review B-05: the groggy starts where the enemy is
    far = brain(s, (), pos=(14.5, 64.0, 3.5), cid=31)
    gauge(s, far)
    s.setsc(('e', far.id), 'bal', 1)
    nopress(s)
    s.gt += 40
    press(s, 1)
    cm_hit(s, far, 30)
    gs = s.calls('rlk:bal/grog/start')
    ck('bal: the last pip by a perfect parry starts the groggy at the enemy 14 b away, not at the player',
       bal(s, far) == 0 and len(gs) == 1 and gs[0][3] == tuple(far.pos) and 'rlk_cmb' in gs[0][1], (bal(s, far), gs))
    far.alive = False
    s.ents.remove(far)
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
    cases = [('disc r 3.2', dict(K=1, R=3200), 0), ('disc r 4.5', dict(K=1, R=4500), 0), ('sector r 6', dict(K=3, R=6000), 0),
             ('sector r 12', dict(K=3, R=12000), 0), ('line 5 b', dict(K=4, R=5000), 0), ('line 14 b', dict(K=4, R=14000), 0),
             ('ring', dict(K=2, R=3000), 0), ('full', dict(K=5, R=20000), 1), ('mask', dict(K=6, R=0), 1),
             ('no-dodge disc r 2', dict(K=1, R=2000, ND=1), 1), ('per-mille disc', dict(K=1, R=2000, Pm=250), 1),
             ('re-arm disc', dict(K=1, R=2000, RA=10), 1)]
    for name, kw, want in cases:
        ck(f'boss: np_def {name} -> {"unparriable" if want else "parryable"}', hzm(s, **kw) == want)
    # hz/init applies the explicit option
    body = Ent('husk', (8.5, 64.0, 0.5), (0.0, 0.0), ['rlk_mb_body', 'boss'])
    s.ents.append(body)
    init = rd('mboss/hz/init')
    ck('boss: hz/init: #hzNoParry 0 / 1 / 2 overrides the rule (only -1 runs np_def)',
       'execute unless score @s mbHzNP matches 0..2 run function rlk:mboss/hz/np_def' in init)
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
    # (reviews B-04 / B-11, fix lane FB: the glint means "cannot be parried: dodge it"; every unparriable hazard of hers is
    # no-dodge or a field / safe dome, so hazard/new flashes none)
    ck('raiden: no hazard flashes the warning glint (her unparriable ones are no-dodge / fields: B-04, B-11)',
       not any('glint' in l for l in new.split('\n') if l and not l.startswith('#')))
    left = [p.relative_to(FN).as_posix() for p in FN.rglob('*.mcfunction') if 'rd_glint' in p.read_text(encoding='utf-8') or p.stem == 'rd_glint']
    ck('raiden: the unused player/def/fx/rd_glint is gone and nothing names it', not left, left)


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
    # a perfect-window pass asked through q_pf0 / q_pf1 (no judge call) is an avoided attack for the dodge cooldown too
    fresh(s)
    prepass(s, rc=True)
    c0 = P(s, 'dashCool')
    r0 = s.call('rlk:player/def/q_pf0', Ctx(None, (0, 0, 0), (0, 0)))
    c1 = P(s, 'dashCool')
    s.gt += 1
    r1 = s.call('rlk:player/def/q_pf1', Ctx(None, (0, 0, 0), (0, 0)))
    ck('readers: 홍련 pip query in the dodge window refunds the dodge cooldown once (18 -> 12: her 12-t chain stays doable with '
       'dodges alone)', bool(r0) and bool(r1) and (c0, c1, P(s, 'dashCool')) == (G(s, '#dashCoolT'), G(s, '#dashCoolHitT'), G(s, '#dashCoolHitT')),
       (r0, r1, c0, c1, P(s, 'dashCool')))
    fresh(s)
    P(s, 'dashCool', 7)
    press(s, 0)
    r0 = s.call('rlk:player/def/q_pf0', Ctx(None, (0, 0, 0), (0, 0)))
    ck('readers: ... an F window answers the query without touching the dodge cooldown', bool(r0) and P(s, 'dashCool') == 7)
    for g_ in list(s.select('@e[tag=rlk_dgo]', pctx(s))):
        g_.alive = False
    s.ents = [x for x in s.ents if x.alive]
    nopress(s)
    P(s, 'dashCool', 0)
    # (HI, 11-11: the rebuilt 홍련 takes a gauntlet segment on a judged perfect parry only, hr_design §1.2 - no q_pf query)
    pip = rd('boss/scarlet/shield/tick') or ''
    ck('readers: 홍련 shield/tick takes a segment on a judged perfect parry (#mbDodgeOk + #parT 3; no dashInvT, no q_pf query)',
       '#mbDodgeOk mb' in pip and 'unless score #parT tmp matches 3 run return 0' in pip and 'dashInvT' not in pip and 'q_pf' not in pip)
    ck('readers: the shield rush contact ends on a perfect parry', 'execute if score #parT tmp matches 3 run tag @s add rlk_sh_rhit' in rd('cm/sh/rcontact'))
    ck('readers: Apep\'s organism bolt ends when parried (tier 3) and flies on when dodged',
       'execute if score #dodged tmp matches 1 unless score #parT tmp matches 3 run return 0' in rd('boss/apep/org/pj_end'))
    ck('readers: the item hooks on_parry / on_pdodge / on_parry_press exist; on_dash keeps the item effects (no hw_dash)',
       all(rd(f'items/hook/{h}') is not None for h in ('on_parry', 'on_pdodge', 'on_parry_press')) and 'hw_dash' not in rd('items/hook/on_dash'))
    ck('readers: the tutorial step 1 counts dodges and F presses', '#tutC lob 1' in rd('items/hook/on_parry_press'))
    ck('readers: knockback start / tick and hurt_elem still read the non-dodge i-frames (dashInvT)', all('dashInvT' in rd(f) for f in
       ('player/knockback/start', 'player/knockback/tick', 'player/hurt_elem')))


# ================================================================================================== fx
CLOCK = next(l for l in _TICK if 'player/def/beat/clock' in l)
ADJ = next(l for l in _TICK if l == 'scoreboard players operation #now cb -= #btAdj cb')
FXW = next(l for l in _TICK if 'player/def/fx/world' in l)
POST = next(l for l in _TICK if 'player/def/beat/post' in l)


def eot(s):
    """the rest of a game tick after its hits: rlk:tick's effect line and the beat's post line"""
    s.cmd(split(FXW), C0)
    s.cmd(split(POST), C0)


def sot(s):
    """the head of the next game tick: the game time and rlk:tick's beat-clock lines"""
    s.gt += 1
    s.setsc('#now', 'cb', s.gt)
    s.cmd(split(CLOCK), C0)
    s.cmd(split(ADJ), C0)


def fxn(s, tag):
    return len(s.select(f'@e[tag={tag}]', pctx(s)))


def t_fx():
    s, pl = world()
    e = brain(s)
    s.titles.clear()
    nopress(s)
    press(s, 1)
    P(s, 'vBig', 0)
    P(s, 'ttlT', 0)
    pl.rot = [40.0, 20.0]
    s.cmdlog.clear()
    t0 = s.gt
    cm_hit(s, e, 20)
    ck('fx: a perfect parry starts the beat on the contact tick: kind 1, the contact marker, a small spark, the attacker tagged, '
       'the avatar motion; no starburst and no overlay yet', G(s, '#btK', 'cb') == 1 and G(s, '#btA', 'cb') == 0 and fxn(s, 'rlk_bt_pt') == 1
       and fxn(s, 'rlk_cb_spark') == 1 and fxn(s, 'rlk_cb_star') == 0 and not s.titles and 'rlk_bt_atk' in e.tags
       and len(s.calls('rlk:char/motion/beat/parry')) == 1, (G(s, '#btK', 'cb'), fxn(s, 'rlk_cb_spark'), s.titles))
    seen = []
    for k in range(1, 21):
        eot(s)
        sot(s)
        seen.append((fxn(s, 'rlk_cb_star'), fxn(s, 'rlk_cb_bolt'), G(s, '#btK', 'cb'), P(s, 'vBig')))
    star = [x[0] for x in seen]
    ck('fx: the starburst appears 2 ticks after the contact at full size, stands through the freeze (ticks 2-5), starts to go on '
       'the release tick 6 and is removed 2 ticks later', star[:8] == [0, 1, 1, 1, 1, 1, 1, 0], star)
    mg = [(t - t0, c) for t, c in s.cmdlog if c.startswith('data merge') and 'scale:[0f,0f,0f]' in c]
    ck('fx: ... the contact spark shrinks from tick 1, the starburst from the end of the last freeze tick (5: seen from the release)',
       [m[0] for m in mg] == [1, 5], mg[:3])
    ck('fx: the warm tint + streak overlay (title, vBig 7) comes with the starburst on tick 2', any('title' in t for t in s.titles)
       and seen[1][3] == 7 and seen[0][3] == 0, (s.titles[-2:], [x[3] for x in seen[:3]]))
    ck('fx: lightning cards crawl over the attacker on ticks 7-15 only', [k + 1 for k, x in enumerate(seen) if x[1]][:1] == [7]
       and max(k + 1 for k, x in enumerate(seen) if x[1]) <= 17 and len(s.calls('rlk:player/def/fx/p3_bolt')) == 9,
       ([k + 1 for k, x in enumerate(seen) if x[1]], len(s.calls('rlk:player/def/fx/p3_bolt'))))
    ck('fx: the shatter on tick 6, the weapon glow off on tick 12, the beat over on tick 17; nothing is left afterwards',
       len(s.calls('rlk:player/def/fx/p3_shatter')) == 1 and len(s.calls('rlk:char/motion/beat/wglow_off')) >= 1
       and [x[2] for x in seen][15:18] == [1, 0, 0] and not s.select('@e[tag=rlk_cb_fx]', pctx(s)) and fxn(s, 'rlk_bt_pt') == 0
       and 'rlk_bt_atk' not in e.tags, ([x[2] for x in seen], fxn(s, 'rlk_bt_pt')))
    ck('fx: the perfect parry never turns the view (the 11-11b jolt is gone: the freeze is the impact)',
       not [c for _, c in s.cmdlog if c.startswith('rotate @s')] and [round(v, 3) for v in pl.rot] == [40.0, 20.0],
       ([c for _, c in s.cmdlog if c.startswith('rotate')], pl.rot))
    pl.rot = [0.0, 0.0]
    for tier, ago in ((2, 4), (1, 7)):
        s.titles.clear()
        s.log.clear()
        s.gt += 30
        nopress(s)
        press(s, ago)
        P(s, 'vBig', 0)
        n0 = fxn(s, 'rlk_cb_spark')
        cm_hit(s, e, 20)
        ck(f'fx: tier {tier} looks like a normal guard: one small spark, no starburst, no overlay, no beat, no view turn',
           G(s, '#parT') == tier and fxn(s, 'rlk_cb_spark') == n0 + 1 and fxn(s, 'rlk_cb_star') == 0 and not s.titles
           and G(s, '#btK', 'cb') == 0 and P(s, 'vBig') == 0, (G(s, '#parT'), fxn(s, 'rlk_cb_spark'), s.titles))
        for _ in range(6):
            eot(s)
            sot(s)
    src = {n: rd(f'player/def/fx/{n}') for n in ('p1_at', 'p2_at', 'p3_at', 'p3_star', 'p2', 'p1')}
    ck('fx: tiers 2 / 1 draw no flash particle, no star glyph and no title; their sound is the thin chain tick, not the perfect '
       'parry\'s anvil / trident clang or the amethyst ring', all('flash' not in src[n] and 'g/star' not in src[n] and 'ovl' not in src[n]
       and 'anvil' not in src[n] and 'resonate' not in src[n] for n in ('p1_at', 'p2_at', 'p1', 'p2'))
       and 'block.chain.hit' in src['p1_at'] and 'block.chain.hit' in src['p2_at'] and 'anvil' in src['p3_at'] and 'resonate' in src['p3_star'])
    ck('fx: every effect entity is gone', not s.select('@e[tag=rlk_cb_fx]', pctx(s)))
    s.titles.clear()
    s.gt += 30
    nopress(s)
    dodge(s, 0)
    s.ents.append(Ent('interaction', (0.5, 64.0, 0.5), (0.0, 0.0), ['rlk_dgo', 'rlk_pet']))
    P(s, 'vBig', 0)
    cm_hit(s, e, 20)
    ck('fx: a perfect dodge: beat kind 2, the dark vignette overlay (vBig 17), the ghost mannequin (team rlk_cbred), the burst card',
       any('title' in t for t in s.titles) and bool(s.select('@e[tag=rlk_cb_ghost]', pctx(s))) and G(s, '#btK', 'cb') == 2
       and P(s, 'vBig') == 17 and fxn(s, 'rlk_cb_burst') == 1, (s.titles[-1:], G(s, '#btK', 'cb'), P(s, 'vBig')))
    for _ in range(30):
        eot(s)
        sot(s)
    ck('fx: ... the avatar\'s flip starts on tick 5, the tint goes on the landing tick 21, the beat is over on tick 27 and '
       'every effect entity is gone', len(s.calls('rlk:char/motion/beat/dodge')) == 1 and len(s.calls('rlk:char/motion/beat/tint_off')) >= 1
       and G(s, '#btK', 'cb') == 0 and not s.select('@e[tag=rlk_cb_fx]', pctx(s)),
       (len(s.calls('rlk:char/motion/beat/dodge')), G(s, '#btK', 'cb')))

    def age():
        """the rest of this tick, then the next tick's head"""
        eot(s)
        sot(s)
    for g in list(s.select('@e[tag=rlk_dgo]', pctx(s))):
        g.alive = False
    s.ents = [x for x in s.ents if x.alive]
    # reviews A-03 / A-06: the red ghost through the real path (right-click -> the dodge-start box -> a strike in the window)
    fresh(s)
    pl.rot = [135.0, 0.0]
    prepass(s, rc=True)
    box = s.select('@e[tag=rlk_dgo]', pctx(s))
    ck('fx: the dodge-start box takes the body\'s yaw (review A-06)', len(box) == 1 and [round(v, 1) for v in box[0].rot] == [135.0, 0.0],
       [b.rot for b in box])
    pl.pos = [3.5, 64.0, 0.5]                                # the body has moved on; the swordsman strikes the start
    pl.rot = [20.0, 0.0]
    s.killed.clear()
    P(s, 'vBig', 0)
    s.call('rlk:player/def/ghost_on', C0)
    lost = cm_hit(s, e, 20)
    s.call('rlk:player/def/ghost_off', C0)
    gh = s.select('@e[tag=rlk_cb_ghost]', pctx(s))
    ck('fx: the afterimage stands at the dodge start and faces as the body did then (yaw 135), not south',
       lost == 0 and len(gh) == 1 and [round(v, 1) for v in gh[0].pos] == [0.5, 64.0, 0.5] and [round(v, 1) for v in gh[0].rot] == [135.0, 0.0],
       (lost, [(g.pos, g.rot) for g in gh]))
    g0 = gh[0]
    life = []
    for k in range(10):
        life.append((g0.alive, 'rlk_cb_ghost' in g0.tags, tuple(round(v, 1) for v in g0.pos), g0.data.get('Glowing')))
        age()
    FAR = (1000000.5, 400.0, 1000000.5)
    ck('fx: the ghost is shown 8 ticks where it was made; then its glow is switched off and it is moved to the far chunk '
       '(review A-03)', all(x == (True, True, (0.5, 64.0, 0.5), None) for x in life[:8]) and life[8] == (True, False, FAR, 0), life)
    dead = [k for k in s.killed if k[0] == 'mannequin']
    ck('fx: ... and it is killed only there, one tick later, with the glow off (no death animation at the dodge start)',
       not g0.alive and life[9][0] is False and len(dead) == 1 and dead[0][2] == FAR and dead[0][3].get('Glowing') == 0, (life[9], dead))
    # a second perfect dodge while a ghost is still up: the old one is moved out, never killed in place
    pl.pos = [0.5, 64.0, 0.5]
    fresh(s)
    prepass(s, rc=True)
    cm_hit(s, e, 20)
    first = s.select('@e[tag=rlk_cb_ghost]', pctx(s))[0]
    age()
    age()
    s.killed.clear()
    P(s, 'dashCool', 0)
    s.gt += 20
    prepass(s, rc=True)
    cm_hit(s, e, 20)
    ck('fx: a new ghost moves the earlier one out first (glow off, far chunk), it is not killed in place',
       len(s.select('@e[tag=rlk_cb_ghost]', pctx(s))) == 1 and first.alive and tuple(first.pos) == FAR and first.data.get('Glowing') == 0
       and not [k for k in s.killed if k[0] == 'mannequin'], (first.pos, first.data, s.killed))
    for _ in range(12):
        age()
    ck('fx: ... and both are gone afterwards, each killed at the far chunk', not s.select('@e[tag=rlk_cb_fx]', pctx(s))
       and [k[2] for k in s.killed if k[0] == 'mannequin'] == [FAR, FAR], [k[2] for k in s.killed if k[0] == 'mannequin'])
    pl.rot = [0.0, 0.0]
    # review A-09: the crosshair comes back in the tick the overlay ends (view/tick's vBig line, then view/ride_tick's lines)
    vb = [l for l in code(rd('view/tick')) if 'score @s vBig matches' in l]
    xh = [l for l in code(rd('view/ride_tick')) if '#xh view' in l]
    nopress(s)
    s.gt += 40
    press(s, 1)
    P(s, 'vBig', 0)
    cm_hit(s, e, 20)
    age()
    age()                                                    # the overlay goes up on tick 2 of the beat (vBig 7)
    s.setsc('#xh', 'view', 1)                                # the 10-tick resend has just fired
    s.log.clear()
    sent = []
    for k in range(1, 11):                                   # the view ticks from the overlay's tick on
        for l in vb + xh:
            s.cmd(split(l), pctx(s))
        if s.calls('rlk:view/xhair'):
            sent.append(k)
            s.log.clear()
    ck('fx: after the 7-tick parry overlay the crosshair is sent on its 7th tick, not up to 9 ticks later (review A-09)',
       len(xh) == 3 and sent[:1] == [7], (len(xh), sent))
    for _ in range(20):
        age()
    no_errors(s, 'fx')


# ================================================================================================== the beat (round V, lane VP)
def drive(on, hits, f_at=(), rc_at=(), total=120, cls=0, rc_every=False, log_cool=False):
    """One scripted fight on the beat's clock. hits / f_at / rc_at are COMBAT ticks (0 = the first tick): a strike of the
    swordsman lands on the world tick `c`, F / a right-click arrive on the first real tick whose pre-pass carries combat
    tick `c` (during a hold that is the tick the world resumes on). World things (the strike, the dodge cooldown line) run
    only on ticks the beat does not hold, as the gated dispatchers do. -> (events in combat ticks, real ticks used, sim)"""
    s, pl = world(beat=on)
    e = brain(s)
    fresh(s)
    P(s, 'energy', 0)
    ev, real, base = [], 0, None
    sent_f, sent_rc = set(), set()
    while True:
        c = s.gt + 1 - (G(s, '#btLag', 'cb') or 0)           # the combat tick the next pre-pass carries
        if base is None:
            base = c
        k = c - base
        if k >= total:
            break
        f = k in f_at and k not in sent_f
        rc = (k in rc_at or rc_every) and k not in sent_rc
        sent_f.add(k)
        sent_rc.add(k)
        acc, dg = prepass2(s, f=f, rc=rc)
        real += 1
        hold = G(s, '#btHold', 'cb') == 1
        if f:
            ev.append((k, 'F', acc))
        if dg:
            ev.append((k, 'dodge'))
        if not hold:
            if k in hits:
                full(s)
                hp0 = P(s, 'curHealth')
                if cls == 2:
                    for o, v in (('#cmDmg', 60), ('#cmLv', 1), ('#cmEl', 0), ('#cmKB', 0), ('#hcC', 2), ('#hcK', 1)):
                        s.setsc(o, 'tmp', v)
                    s.call('rlk:cm/hit_pl2', pctx(s))
                else:
                    s.setsc('#cmDmg', 'tmp', 60)
                    s.call('rlk:cm/hit_me', Ctx(e, tuple(e.pos), tuple(e.rot)))
                ev.append((k, 'hit', hp0 - P(s, 'curHealth'), G(s, '#parT'), G(s, '#pdg'), G(s, '#dodged')))
            if log_cool:
                ev.append((k, 'cool', P(s, 'dashCool')))
        cooldown(s)
        eot(s)
    return ev, real, s


def prepass2(s, f=False, rc=False):
    """prepass() for a beat-on world: the accepted F / started dodge are read on the beat's clock (#now cb), not s.gt"""
    a0, d0 = P(s, 'parAt'), P(s, 'dgAt')
    prepass(s, f=f, rc=rc)
    now = G(s, '#now', 'cb')
    return P(s, 'parAt') == now and a0 != now, P(s, 'dgAt') == now and d0 != now


def t_beat():
    # ---- the schedule: which real ticks hold the world, which are untouchable, the clock's lag (N = 5 / 7)
    for kind, name, holds, inv, endA in ((1, 'perfect parry', [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 17),
                                         (2, 'perfect dodge', [1, 6, 7, 9, 10, 12, 13], list(range(1, 15)), 27)):
        s, pl = world(beat=1)
        e = brain(s)
        fresh(s)
        prepass2(s)
        lag0 = G(s, '#btLag', 'cb') or 0
        now0 = G(s, '#now', 'cb')
        if kind == 1:
            press(s, 1)
            P(s, 'parAt', now0 - 1)
        else:
            dodge(s, 0)
            P(s, 'dgAt', now0)
        lost = cm_hit(s, e, 60)
        cooldown(s)
        eot(s)
        got_h, got_i, nows, K = [], [], [], []
        for a in range(1, endA + 3):
            prepass2(s)
            if G(s, '#btHold', 'cb') == 1:
                got_h.append(a)
            if G(s, '#btInv', 'cb') == 1:
                got_i.append(a)
            nows.append(G(s, '#now', 'cb') - now0)
            K.append(G(s, '#btK', 'cb'))
            cooldown(s)
            eot(s)
        n = len(holds)
        want_now, c = [], 0
        for a in range(1, endA + 3):
            if a not in holds:
                c += 1
            want_now.append(c if a not in holds else c + 1)
        ck(f'beat: a {name} (no damage) holds the world on real ticks {holds} after the hit and nowhere else',
           lost == 0 and got_h == holds, (lost, got_h))
        ck(f'beat: ... the player is untouchable on ticks {inv[0]}-{inv[-1]}', got_i == inv, got_i)
        ck(f'beat: ... the clock: #now cb counts only world ticks (a held tick carries the tick the world resumes on), '
           f'#btLag grew by exactly {n}', nows == want_now and G(s, '#btLag', 'cb') - lag0 == n and G(s, '#btAdj', 'cb') == G(s, '#btLag', 'cb'),
           (nows, G(s, '#btLag', 'cb') - lag0))
        ck(f'beat: ... it is over on tick {endA} (#btK 0, nothing held, no tags, the fov modifier call made)', K[endA - 2] == kind
           and K[endA - 1] == 0 and G(s, '#btHold', 'cb') == 0 and G(s, '#btInv', 'cb') == 0 and 'rlk_bt_atk' not in e.tags
           and e.data.get('NoAI') in (0, None) and 'rlk_bt_noai' not in e.tags, (K[endA - 3:endA + 1], e.data, sorted(e.tags)))
    # ---- (a) / (b): the same fight with the beat on and off gives the same events on the beat's clock, N real ticks later
    cases = [
        ('a 7-hit chain 10 t apart, F one tick before each', dict(hits=[10 + 10 * i for i in range(7)], f_at=[9 + 10 * i for i in range(7)], total=100), 7, 0),
        ('a 9-hit string 3 t apart, F in rhythm', dict(hits=[12 + 3 * i for i in range(9)], f_at=[12 + 3 * i for i in range(9)], total=70), 9, 0),
        ('a 9-hit string 2 t apart, F in rhythm', dict(hits=[12 + 2 * i for i in range(9)], f_at=[12 + 2 * i for i in range(9)], total=60), 9, 0),
        ('late and early presses (tiers 1-3 and misses) on a 12-t chain', dict(hits=[20 + 12 * i for i in range(6)],
                                                                          f_at=[19, 28, 37, 55, 68, 80, 81], total=110), None, 0),
        ('boss-class strikes 20 t apart, a right-click every tick (dodge cooldown 18 / 12)', dict(hits=[15 + 20 * i for i in range(5)],
                                                                                            rc_every=True, total=120, cls=2, log_cool=True), None, None),
        ('normal-mob strikes 25 t apart, a dodge one tick before each', dict(hits=[20 + 25 * i for i in range(4)],
                                                                         rc_at=[19 + 25 * i for i in range(4)], total=120), 0, 4),
    ]
    for name, kw, n_par, n_dg in cases:
        ev0, real0, s0 = drive(0, **kw)
        ev1, real1, s1 = drive(1, **kw)
        par = len([x for x in ev1 if x[1] == 'hit' and x[3] == 3])
        pdg = len([x for x in ev1 if x[1] == 'hit' and x[4] == 1])
        # a strike on a world tick inside a dodge beat is voided by design (untouchable): keep it out of the comparison
        lag = (G(s1, '#btLag', 'cb') or 0) - (s1.lag0 if hasattr(s1, 'lag0') else 0)
        ck(f'beat: {name}: the beat on and off give the same events on the beat\'s clock ({len(ev1)} events, {par} perfect parries, '
           f'{pdg} perfect dodges)', ev0 == ev1 and len(ev1) >= 4 and (n_par is None or par == n_par) and (n_dg is None or pdg == n_dg),
           [(a, b) for a, b in zip(ev0, ev1) if a != b][:3] or (len(ev0), len(ev1), par, pdg))
        ck(f'beat: ... and takes exactly 5 real ticks more per perfect parry and 7 per perfect dodge ({real1} = {real0} + 5 x {par} '
           f'+ 7 x {pdg})', real1 == real0 + 5 * par + 7 * pdg, (real0, real1, par, pdg))
    # ---- (c): untouchable for the beat
    s, pl = world(beat=1)
    e = brain(s)
    fresh(s)
    prepass2(s)
    press(s, 1)
    P(s, 'parAt', G(s, '#now', 'cb') - 1)
    cm_hit(s, e, 60)
    cooldown(s)
    eot(s)
    lost, extra = [], 0
    for a in range(1, 8):
        prepass2(s)
        n_p3 = len(s.calls('rlk:player/def/fx/p3'))
        full(s)
        hp0 = P(s, 'curHealth')
        s.setsc('#cmDmg', 'tmp', 60)
        s.call('rlk:cm/hit_me', Ctx(e, tuple(e.pos), tuple(e.rot)))            # a vanilla / stray hit in the freeze
        d1 = hp0 - P(s, 'curHealth')
        full(s)
        hp0 = P(s, 'curHealth')
        for o, v in (('#cmDmg', 60), ('#cmLv', 1), ('#cmEl', 0), ('#cmKB', 0), ('#hcC', 2), ('#hcK', 3), ('#hcND', 1), ('#hcNP', 1)):
            s.setsc(o, 'tmp', v)
        s.call('rlk:cm/hit_pl2', pctx(s))                                       # an undodgeable, unparriable boss hit
        d2 = hp0 - P(s, 'curHealth')
        full(s)
        hp0 = P(s, 'curHealth')
        s.setsc('#dmg', 'tmp', 30)
        s.setsc('#elem', 'tmp', 1)
        s.call('rlk:player/hurt_elem', pctx(s))                                 # a reaction DoT tick
        d3 = hp0 - P(s, 'curHealth')
        lost.append((d1, d2, d3))
        extra += len(s.calls('rlk:player/def/fx/p3')) - n_p3
        cooldown(s)
        eot(s)
    ck('beat: (c) during the freeze (ticks 1-5) a melee hit, an undodgeable unparriable boss hit and a DoT tick take nothing, '
       'start nothing; from the release tick they hurt again', all(x == (0, 0, 0) for x in lost[:5]) and all(v > 0 for v in lost[5])
       and extra == 0, (lost, extra))
    # a hit on a world tick inside the dodge beat: voided unless it is answered perfectly (then it counts as that answer)
    ev, real, s = drive(1, hits=[20, 24, 26], rc_at=[19], total=60, cls=2)
    hv = [x for x in ev if x[1] == 'hit']
    ck('beat: (c) boss strikes 4 and 6 world ticks after a perfectly dodged one (inside its beat) take nothing and are no dodge '
       'event', len(hv) == 3 and hv[0][2:] == (0, 0, 1, 1) and hv[1][2:] == (0, 0, 0, 1) and hv[2][2:] == (0, 0, 0, 1), hv)
    ev, real, s = drive(1, hits=[20, 25], rc_at=[19], f_at=[24], total=60, cls=2)
    hv = [x for x in ev if x[1] == 'hit']
    ck('beat: (d) a perfect parry inside a dodge beat is a perfect parry and starts its own beat (the dodge beat is closed first)', len(hv) == 2 and hv[1][3] == 3 and len(s.calls('rlk:player/def/beat/start_p')) == 1
       and G(s, '#btK', 'cb') == 0 and G(s, '#btHold', 'cb') == 0, (hv, real))
    # ---- (d): back-to-back beats leave nothing behind
    ev, real, s = drive(1, hits=[10 + 10 * i for i in range(7)], f_at=[9 + 10 * i for i in range(7)], total=100)
    e = [x for x in s.ents if 'rlk_cmb' in x.tags][0]
    ck('beat: (d) seven perfect parries 10 t apart: seven beats, each closed before the next hit (the mob is free between them, '
       'no tag or marker is left)', len(s.calls('rlk:player/def/beat/start_p')) == 7 and len(s.calls('rlk:player/def/beat/hold_on')) == 7
       and len(s.calls('rlk:player/def/beat/hold_off')) == 7 and e.data.get('NoAI') == 0 and 'rlk_bt_noai' not in e.tags
       and not s.select('@e[tag=rlk_bt_pt]', pctx(s)) and not s.select('@e[tag=rlk_bt_rk]', pctx(s)),
       (len(s.calls('rlk:player/def/beat/start_p')), len(s.calls('rlk:player/def/beat/hold_on')), e.data))
    # ---- (e): every exit leaves nothing frozen
    def frozen_then(what, kind=1, at=3):
        s, pl = world(beat=1)
        e = brain(s)
        e2 = brain(s, pos=(4.5, 64.0, 2.5), cid=8)
        P2 = ('e', e2.id)
        s.setsc(P2, 'frzT', 40)
        e2.data['NoAI'] = 1                                   # a mob that was frozen before the beat
        fresh(s)
        prepass2(s)
        if kind == 1:
            P(s, 'parAt', G(s, '#now', 'cb') - 1)
            P(s, 'parHit', -1000000)
        else:
            P(s, 'dgAt', G(s, '#now', 'cb'))
            P(s, 'dgRw', -1000000)
        cm_hit(s, e, 60)
        eot(s)
        for _ in range(at):
            prepass2(s)
            eot(s)
        held = (G(s, '#btHold', 'cb'), e.data.get('NoAI'), 'rlk_bt_noai' in e.tags, 'rlk_bt_noai' in e2.tags)
        what(s, pl)
        prepass2(s)
        eot(s)
        full(s)
        after = (G(s, '#btK', 'cb'), G(s, '#btHold', 'cb'), G(s, '#btInv', 'cb'), e.data.get('NoAI'), 'rlk_bt_noai' in e.tags,
                 e2.data.get('NoAI'), 'rlk_bt_atk' in e.tags, len(s.select('@e[tag=rlk_bt_pt]', pctx(s))),
                 G(s, '#btAdj', 'cb') == G(s, '#btLag', 'cb'))
        return held, after
    FREE = (0, 0, 0, 0, False, 1, False, 0, True)
    exits = [('the player dies', lambda s, pl: P(s, 'dead', 1)), ('Ronova falls (revival wait)', lambda s, pl: P(s, 'rnDie', 1)),
             ('the selection space opens', lambda s, pl: P(s, 'pkMode', 1)), ('the map opens', lambda s, pl: P(s, 'vMap', 1)),
             ('a cutscene starts (#mbCine)', lambda s, pl: s.setsc('#mbCine', 'mb', 1)),
             ('a cutscene camera lock is requested (#mbCam)', lambda s, pl: s.setsc('#mbCam', 'mb', 1)),
             ('/reload (rlk:load)', lambda s, pl: s.call('rlk:load', C0)),
             ('the player tag is gone', lambda s, pl: pl.tags.discard('player'))]
    for name, what in exits:
        for kind, at in ((1, 3), (2, 6)):
            held, after = frozen_then(what, kind, at)
            ck(f'beat: (e) {name} during a {"parry freeze" if kind == 1 else "dodge slow motion"}: the next tick nothing is held (the '
               f'mob has its AI back, a mob frozen before keeps its own NoAI, no tag, the clock keeps its lag)',
               held == (1, 1, True, False) and after == FREE, (held, after))
    # a freeze that starts during the hold is not undone by the release, and its "was NoAI before" note is corrected
    s, pl = world(beat=1)
    e = brain(s)
    fresh(s)
    prepass2(s)
    P(s, 'parAt', G(s, '#now', 'cb') - 1)
    P(s, 'parHit', -1000000)
    cm_hit(s, e, 60)
    eot(s)
    prepass2(s)
    eot(s)
    s.setsc(('e', e.id), 'frzT', 40)                          # element/frz_on during the hold: it sees NoAI 1 and notes rlk_noai
    e.tags.add('rlk_noai')
    for _ in range(8):
        prepass2(s)
        eot(s)
    ck('beat: (e) a mob the player froze during the hold stays frozen after the release (NoAI 1) and loses the wrong rlk_noai '
       'note, so the freeze\'s own end gives its AI back', e.data.get('NoAI') == 1 and 'rlk_noai' not in e.tags and 'rlk_bt_noai' not in e.tags,
       (e.data, sorted(e.tags)))
    # ---- the gates are where the worlds start
    fns = {n: rd(n) for n in ('mboss/main', 'cm/world', 'cm/pj/world', 'mob/tick', 'player/tick', 'tick', 'player/hurt_elem', 'mboss/pl_dot2',
                              'mboss/np_gate', 'player/def/judge2', 'player/def/q_pf0', 'player/def/q_pf1', 'player/def/dodge_stamp')}
    ck('beat: rlk:tick gates mboss/main, cm/world, cm/pj/world, Raiden\'s world and the near pass (one condition on each line: no '
       'command more when no beat runs); mob/tick the stun, balance and element timers; player/tick the dodge cooldown',
       all(any(k in l and 'unless score #btHold cb matches 1' in l for l in code(fns[n])) for n, k in (
           ('tick', 'function rlk:mboss/main'), ('tick', 'function rlk:cm/world'), ('tick', 'function rlk:cm/pj/world'),
           ('tick', 'boss/raiden/world'), ('tick', 'mboss/near_all'), ('mob/tick', 'remove @s stunT 1'), ('mob/tick', 'rlk:bal/tick'),
           ('mob/tick', 'rlk:element/tick'), ('player/tick', 'remove @s dashCool 1')))
       and all('#btHold' not in fns[n] for n in ('mboss/main', 'cm/world', 'cm/pj/world')))
    ck('beat: the untouchable test sits in judge2 after the perfect dodge and the perfect parry, in player/hurt_elem and in '
       'mboss/pl_dot2; the clock users (judge, dodge_stamp, q_pf0 / q_pf1, np_gate) subtract #btAdj',
       code(fns['player/def/judge2']).index('execute if score #btInv cb matches 1 run return run function rlk:player/def/beat/inv')
       > max(i for i, l in enumerate(code(fns['player/def/judge2'])) if 'player/def/par3' in l or 'player/def/pd' in l)
       and all('#btInv cb matches 1' in fns[n] for n in ('player/hurt_elem', 'mboss/pl_dot2'))
       and all('-= #btAdj cb' in fns[n] for n in ('player/def/q_pf0', 'player/def/q_pf1', 'player/def/dodge_stamp', 'mboss/np_gate')))
    kits = [p for p in FN.rglob('fx/e/world.mcfunction')] + [p for p in FN.rglob('fx/e/make.mcfunction')]
    own = [p for p in kits if 'scarlet' not in p.as_posix()]
    ck(f'beat: the effect kits\' clocks ({len(own)} world / make functions of 6 kits; 홍련\'s is lane VB\'s) subtract the held '
       'ticks (#btLag), and every kit world skips a held tick (it only re-schedules itself)', len(own) >= 12
       and all('-= #btLag cb' in p.read_text(encoding='utf-8') for p in own)
       and all('execute if score #btHold cb matches 1 run return run schedule function' in p.read_text(encoding='utf-8')
               for p in own if p.name == 'world.mcfunction'),
       [p.as_posix()[-40:] for p in own if '-= #btLag cb' not in p.read_text(encoding='utf-8')])
    # ---- the default and the cost
    s, pl = world(beat=1)
    ck('beat: rlk:load sets #btOn tmp 1 (the beat is on by default) and keeps #btLag', s.btOnLoad == 1 and G(s, '#btLag', 'cb') == 0)
    s.setsc('#btLag', 'cb', 77)
    s.call('rlk:load', C0)
    ck('beat: ... a second load keeps the lag (the stamps are on that clock) and #btAdj follows it', G(s, '#btLag', 'cb') == 77 and G(s, '#btAdj', 'cb') == 77)
    s, pl = world(beat=1)
    fresh(s)
    prepass2(s)
    n0 = s.n
    s.cmd(split(CLOCK), C0)
    s.cmd(split(ADJ), C0)
    s.cmd(split(POST), C0)
    ck(f'beat: with no beat running rlk:tick pays {s.n - n0} commands for it (<= 3)', s.n - n0 <= 3, s.n - n0)
    no_errors(s1, 'beat')


# ================================================================================================== boss world loop (A-11)
def t_bossloop():
    import subprocess
    r = subprocess.run([sys.executable, str(HERE / 'bossloop_cb.py'), str(DP)], capture_output=True, text=True, timeout=1800)
    n = 0
    for line in r.stdout.split('\n'):
        if line.startswith(('ok   ', 'FAIL ')):
            n += 1
            name, _, info = line[5:].partition('  -- ')
            ck(name, line.startswith('ok'), info)
    ck('bossloop: bossloop_cb.py ran to the end (5+ checks, exit 0)', n >= 5 and r.returncode == 0, (n, r.returncode, r.stderr[-400:]))


def t_beatloop():
    import subprocess
    for boss in ('1', '2', '3'):
        r = subprocess.run([sys.executable, str(HERE / 'beatloop_cb.py'), str(DP), boss], capture_output=True, text=True, timeout=2400)
        n = 0
        for line in r.stdout.split('\n'):
            if line.startswith(('ok   ', 'FAIL ')):
                n += 1
                name, _, info = line[5:].partition('  -- ')
                ck(name if boss == '1' or 'boss n' in name else f'{name} [boss n {boss}]', line.startswith('ok'), info)
        ck(f'beatloop: beatloop_cb.py boss n {boss} ran to the end (7+ checks, exit 0)', n >= 7 and r.returncode == 0, (n, r.returncode, r.stderr[-400:]))
    r = subprocess.run([sys.executable, str(HERE / 'beatloop_hr.py'), str(DP)], capture_output=True, text=True, timeout=2400)
    n = 0
    for line in r.stdout.split('\n'):
        if line.startswith(('ok   ', 'FAIL ')):
            n += 1
            name, _, info = line[5:].partition('  -- ')
            ck(name, line.startswith('ok'), info)
    ck('beatloop: beatloop_hr.py (홍련: both gauntlets and the free fight) ran to the end (9 checks, exit 0)', n >= 9 and r.returncode == 0,
       (n, r.returncode, r.stderr[-400:]))


# ================================================================================================== cost
def t_cost():
    s, pl = world()
    s.setsc('#now', 'cb', s.gt)
    n0 = s.n
    s.call('rlk:player/def/input', pctx(s))
    n = s.n - n0
    ck(f'cost: the idle pre-pass runs {n} commands (<= 6)', n <= 6, n)


SECTIONS = [('static', t_static), ('input', t_input), ('lock', t_lock), ('judge', t_judge), ('tiers', t_tiers), ('dodge', t_dodge), ('cool', t_cool),
            ('context', t_context), ('energy', t_energy), ('cd', t_cd), ('bal', t_bal), ('boss', t_boss), ('near', t_near), ('raiden', t_raiden),
            ('readers', t_readers), ('fx', t_fx), ('beat', t_beat), ('bossloop', t_bossloop), ('beatloop', t_beatloop), ('cost', t_cost)]
for name, fn in SECTIONS:
    if run(name):
        fn()
print(f'test_cb: {NOK}/{NOK + len(FAILS)} passed')
if FAILS:
    print('FAILED: ' + ', '.join(FAILS[:30]))
    sys.exit(1)
