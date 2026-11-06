#!/usr/bin/env python3
"""knsim.py: the 아를레키노 (Arlecchino) test world of the S3 suites (scratch tool, never shipped; the lead merges it with
S1's AR/tests/lib/knsim.py at I1).

Built on vendored, unchanged copies of the AP harness (lib/cmsim.py on lib/azsim.py, lib/fgsim.py, lib/mcsim.py from
S:ap/tests/lib; md5 e9ccb446 / f463344b / fa9456c8 / 7ac6cf81). The registry entry arlecchino is disabled and S1's arena
fl_ruins is not on this branch, so the fight is entered the way the brief allows ("call hooks directly"):

- every generated dispatcher F:mboss/d/<hook> gets one more line for #mbId 12 -> rlk:boss/arlecchino/<hook> (incoming as
  the chapter wrapper cb/inc: module incoming, then mboss/floor), test as the macro form;
- the arena dispatchers F:mboss/ar/{ok,leash,marker,oob,clampw,sweep} answer for arena n 4 = fl_ruins from
  api.ARENA_SPEC (ok: inside safe - 0.5 b of the axis with free feet / head, the plaza's rule; leash walk / walk + 3;
  marker at the centre, rotation 180; #mbArW10 / #mbArS10 = walk / safe x 10 after fight_vars);
- fight(s): rlk:mboss cur = the registry record of arlecchino as the core would compile it (kind "chapter", ar 4,
  phases [64,36], res all 10), then the REAL mboss/start_go at a zone marker (fight_vars, ar/marker, d/spawn,
  start_body (the 64 % pool), tp_in, bars);
- combat/heal_orb_spawn (an azsim leaf stub) summons a plain rlk_healorb item so the orb rules can be checked.

Helpers: kn(s, name) (a kn score), mb, body, hit_body (a player hit through the REAL combat/apply with the flags of the
attack kind), test_id, run / until, per-tick command counts (s.cmd_hist), the rig call log (s.rigl), every hazard made
(s.hzr: options, position, yaw, #pt / #pat), every projectile launch (s.pjs), every player hit (s.phits).
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cmsim as C  # noqa: E402
import azsim as A  # noqa: E402
import mcsim  # noqa: E402
from mcsim import Ent, Ctx  # noqa: E402

C0 = C.C0
FAIL = C.FAIL
check = C.check
summary = C.summary
S = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
DEFAULT_DP = S / 'ar/wt_i1/roguelike'
NID = 12
ROOT = 'rlk:boss/arlecchino/'
HOOKS = ['spawn', 'intro_tick', 'tick', 'on_hit', 'aux_hit', 'pause', 'resume', 'death_start', 'death_tick', 'cleanup',
         'reload', 'bars', 'hz_vis', 'pj_end', 'uninstall', 'test_help']


def load_api(dp):
    tools = str(Path(dp) / 'tools')
    if tools not in sys.path:
        sys.path.insert(0, tools)
    from mboss_arlecchino import api, s3lib, p1, ai, bond, core  # noqa: F401
    return api


class KnSim(C.CmSim):
    def __init__(self, root):
        super().__init__(root)
        self.ncmd = 0
        self.cmd_hist = []
        self.rigl = []
        self.fcalls = {}
        self.phits = []          # (tick, % of the base hit, element, #pat) of every player hit (cm/hit_pl2)
        self.hzr = []            # every hazard made (hz/make): its options, the position / yaw, #pt / #pat of kn

    def cmd(self, t, ctx):
        self.ncmd += 1
        if t[0] == 'scoreboard' and len(t) == 5 and t[1] == 'players' and t[2] == 'reset' and t[3] == '*':
            for k in [k for k in self.scores if k[1] == t[4]]:
                del self.scores[k]
            return 1
        return super().cmd(t, ctx)

    def call(self, fid, ctx, macro=None):
        if fid.startswith(ROOT + 'rig_stub/') or fid.startswith(ROOT + 'rig/'):
            self.rigl.append((self.t, fid.split('/', 3)[3]))
        if fid == 'rlk:mboss/hz/make':
            g = lambda k: self.sc(k, 'mb')  # noqa: E731
            self.hzr.append(dict(t=self.t, tell=g('#hzW'), dmg=g('#hzD'), kind=g('#hzK'), r=g('#hzR'), a=g('#hzAng'),
                                 hw=g('#hzHW'), act=g('#hzAct'), quiet=g('#hzQuiet'), el=g('#hzEl'), back=g('#hzBack'),
                                 grp=g('#hzGrp'), kb=g('#hzKB'), sfx=g('#hzSfx'), pos=tuple(ctx.pos), yaw=ctx.rot[0],
                                 pt=self.sc('#pt', 'kn'), pat=self.sc('#pat', 'kn'), mbgrp=g('#mbGrp'),
                                 bolw=self.sc('#bolw', 'kn'), bol=g('#hzBol')))
        if fid == 'rlk:cm/hit_pl2':
            self.phits.append((self.t, self.sc('#mbHitPct', 'mb'), self.sc('#cmEl', 'tmp'), self.sc('#pat', 'kn')))
        if fid.startswith(ROOT):
            k = fid[len(ROOT):]
            self.fcalls[k] = self.fcalls.get(k, 0) + 1
        return super().call(fid, ctx, macro)


def install_kn(s, api):
    root = Path(s.root)
    for h in HOOKS:
        p = root / f'mboss/d/{h}.mcfunction'
        lines = p.read_text(encoding='utf-8').rstrip('\n').split('\n')
        tgt = 'test/help' if h == 'test_help' else h
        extra = f'execute if score #mbId mb matches {NID} run return run function {ROOT}{tgt}'
        s.cache[f'rlk:mboss/d/{h}'] = [ln for ln in lines if not ln.startswith('#')] + [extra]
    tl = [ln for ln in (root / 'mboss/d/test.mcfunction').read_text(encoding='utf-8').rstrip('\n').split('\n')
          if not ln.startswith('#')]
    tl.insert(len(tl) - 1, f'$execute if score #mbId mb matches {NID} run return run function {ROOT}test {{id:$(id)}}')
    s.cache['rlk:mboss/d/test'] = tl
    inc = [ln for ln in (root / 'mboss/d/incoming.mcfunction').read_text(encoding='utf-8').rstrip('\n').split('\n')
           if not ln.startswith('#')]
    s.cache['rlk:mboss/d/incoming'] = inc + [f'execute if score #mbId mb matches {NID} run return run function rlk:mboss/cb/inc/arlecchino']
    s.cache['rlk:mboss/cb/inc/arlecchino'] = [f'function {ROOT}incoming', 'function rlk:mboss/floor']
    a = api.ARENA_SPEC
    ok_r = a['safe'] - 0.5
    n = a['n']
    for name, extra in (
            ('ok', [f'execute if score #mbAr mb matches {n} positioned ~ {a["cy"]} ~ unless entity @e[tag=rlk_mb_arena,distance=..{ok_r},limit=1] run return fail',
                    f'execute if score #mbAr mb matches {n} unless block ~ ~ ~ #rlk:dash_pass run return fail',
                    f'execute if score #mbAr mb matches {n} unless block ~ ~1 ~ #rlk:dash_pass run return fail',
                    f'execute if score #mbAr mb matches {n} run return 1']),
            ('leash', [f'execute if score #mbAr mb matches {n} at @s positioned ~ {a["cy"]} ~ if entity @e[tag=rlk_mb_arena,distance=..{a["walk"]},limit=1] run return 0',
                       f'execute if score #mbAr mb matches {n} at @s positioned ~ {a["cy"]} ~ unless entity @e[tag=rlk_mb_arena,distance=..{a["walk"] + 3},limit=1] run return run function rlk:mboss/mv/home',
                       f'execute if score #mbAr mb matches {n} at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run return run tp @s ~ ~ ~']),
            ('marker', [f'execute if score #mbAr mb matches {n} run return run summon minecraft:marker {a["cx"]} {a["cy"]} {a["cz"]} '
                        '{Tags:["rlk_room","rlk_mb_aux","rlk_mb_arena"],Rotation:[180.0f,0.0f]}']),
            ('oob', [f'execute if score #mbAr mb matches {n} run return 0']),
            ('clampw', [f'execute if score #mbAr mb matches {n} run return 0']),
            ('sweep', [f'execute if score #mbAr mb matches {n} run return 0'])):
        p = root / f'mboss/ar/{name}.mcfunction'
        lines = [ln for ln in p.read_text(encoding='utf-8').rstrip('\n').split('\n') if not ln.startswith('#')] if p.exists() else []
        s.cache[f'rlk:mboss/ar/{name}'] = extra + lines
    fv = [ln for ln in (root / 'mboss/fight_vars.mcfunction').read_text(encoding='utf-8').rstrip('\n').split('\n')
          if not ln.startswith('#')]
    fv += [f'execute if score #mbAr mb matches {n} run scoreboard players set #mbArW10 mb {int(a["walk"] * 10)}',
           f'execute if score #mbAr mb matches {n} run scoreboard players set #mbArS10 mb {int(a["safe"] * 10)}']
    s.cache['rlk:mboss/fight_vars'] = fv
    # the heal orb (an azsim leaf stub): a plain item at the spot, so the orb rules can be checked
    s.cache['rlk:combat/heal_orb_spawn'] = ['scoreboard players add #HEALORB azs 1',
                                             'summon minecraft:item ~ ~0.6 ~ {Tags:["rlk_healorb"]}']


def cur_snbt(api):
    b = api.BOSS
    a = api.ARENA_SPEC
    st = a['start']
    mus = ','.join(f'"{k}":{{ev:"{v["ev"]}",len:{int(v["len"]) if str(v["len"]).isdigit() else 0}}}' for k, v in b['music'].items())
    res = [b['res'].get(str(i), b['res'].get('*', 0)) for i in range(9)]
    phases = ','.join(str(x) for x in b['phases'])
    return ('{' + f'id:"{b["id"]}",n:{b["n"]},w:{b.get("w", 0)},minCh:{b["minCh"]},maxCh:{b["maxCh"]},name:"{b["name"]}",'
            f'sub:"{b["sub"]}",color:"{b["color"]}",el:{b["el"]},hp:{b["hp"]},xp:{b["xp"]},atk:{b["atk"]},lvAdd:{b["lvAdd"]},'
            f'dmgMul:{b["dmgMul"]},goldMul:{b["goldMul"]},sap:{b["sap"]},picks:{b["picks"]},scale:{b["scale"]}d,'
            f'intro:{b["intro"]},death:{b["death"]},deathSnd:0b,hit:{{w:{b["hit"]["w"]}f,h:{b["hit"]["h"]}f}},'
            f'start:{{x:{st["x"]}d,y:{st["y"]}d,z:{st["z"]}d,yaw:{st["yaw"]}f,pitch:{st["pitch"]}f}},'
            f'title:{{text:"{b["name"]}",color:"{b["color"]}",bold:true}},kind:"chapter",ar:{a["n"]},px:0b,shield:1b,'
            f'phases:[{phases}],res:[{",".join(str(x) for x in res)}],music:{{{mus}}}' + '}')


def setup(dp=None, hp=40000, lv=20, seed=1102, player_level=20):
    dp = Path(dp or DEFAULT_DP)
    a_start = (760.5, 201.0, 30.5)
    s, zone, pl = A.setup(force=0, lv=lv, hp=hp, seed=seed, player_level=player_level, player_pos=a_start,
                          dp=dp, cls=KnSim)
    C.install(s, lv=lv, hp=hp)
    s.call('rlk:mboss/init', C0)
    zone.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.setsc('#mapIdx', 'room', 5)
    s.setsc('#mapType', 'room', 8)
    s.setsc('#chapter', 'room', 4)
    api = load_api(dp)
    install_kn(s, api)
    s.api = api
    s.setsc(('e', pl.id), 'bol', 0)
    s.setsc(('e', pl.id), 'vMap', 0)
    s.setsc('#bolMax', 'tmp', 200)
    return s, pl


def fight(s, skip_intro=True, limit=400):
    api = s.api
    s.storage.setdefault('rlk:mboss', {})['cur'] = mcsim.Sim.snbt(cur_snbt(api))
    z = Ent('marker', (760.5, 201.0, 40.5), tags=['rlk_zone', 'rlk_room'])
    s.ents.append(z)
    s.call('rlk:mboss/start_go', Ctx(z, tuple(z.pos), (0, 0)))
    pl = s.player()
    pl.pos = [760.5, 201.0, 30.5]
    C.moved(s)
    if skip_intro:
        until(s, lambda s: (s.sc('#mbSt', 'mb') or 0) == 1, limit)
    return body(s)


def world(s):
    n0 = s.ncmd
    C.world(s)
    s.cmd_hist.append(s.ncmd - n0)


def run(s, n, each=None):
    for _ in range(n):
        if each:
            each(s)
        world(s)


def until(s, cond, limit=1500, each=None):
    for _ in range(limit):
        if cond(s):
            return True
        if each:
            each(s)
        world(s)
    return cond(s)


def kn(s, k):
    return s.sc(k, 'kn')


def mb(s, k):
    return s.sc(k, 'mb')


def body(s):
    return C.body_of(s)


def esc(s, e, o):
    return s.sc(('e', e.id), o)


def ents(s, tag, etype=None):
    return [e for e in s.ents if e.alive and tag in e.tags and (etype is None or e.etype == etype)]


def test_id(s, n):
    pl = s.player()
    return s.call('rlk:mboss/test/pattern', Ctx(pl, tuple(pl.pos), tuple(pl.rot)), {'id': n})


def place_player(s, x, z, y=201.0):
    pl = s.player()
    pl.pos = [float(x), float(y), float(z)]
    C.moved(s)
    return pl


def heal_player(s):
    pl = s.player()
    s.setsc(('e', pl.id), 'curHealth', s.sc(('e', pl.id), 'maxHealth'))
    s.setsc(('e', pl.id), 'dead', 0)


# attack kinds as the engine sets the flags before combat/apply (char/* and combat/*; the per-character table of
# test_arlecchino's normal-attack section reads the real files for these)
KINDS = {
    'melee_na': dict(icd=1, skill=0, tfm=0, sub=0),        # combat/find_immediate (sword / scythe / spear / kick)
    'melee_extra': dict(icd=1, skill=0, tfm=0, sub=0),     # char/melee/extra, char/skirk/na_extra
    'bow_na': dict(icd=1, skill=0, tfm=0, sub=0),          # char/bow/arrow_hit, aIcd 1 (na_shot)
    'bow_aim': dict(icd=0, skill=0, tfm=0, sub=0),         # char/bow/arrow_hit, aIcd 0 (release: aimed / charged shot)
    'skill': dict(icd=0, skill=1, tfm=0, sub=0),           # char/dmg_calc (#skillDmg 1)
    'skill_icd': dict(icd=1, skill=1, tfm=0, sub=0),       # lumine crystal / javelin (#icd 1 + #skillDmg 1)
    'reaction': dict(icd=0, skill=0, tfm=1, sub=0),        # element/aoe_hit, dot, lunar/hit
    'item': dict(icd=1, skill=0, tfm=0, sub=1),            # items/proc/* (#sub itv 1)
}


def hit_body(s, dmg=50, el=0, elU=1000, kind='melee_na'):
    """A player hit on the body as combat/apply sees it: combat/clear_atkflags, then the flags of the attack kind."""
    b = body(s)
    f = KINDS[kind]
    s.call('rlk:combat/clear_atkflags', Ctx(b, tuple(b.pos), tuple(b.rot)))
    s.setsc('#dmg', 'tmp', dmg)
    s.setsc('#crit', 'tmp', 0)
    s.setsc('#stunHit', 'tmp', 0)
    s.setsc('#elem', 'tmp', el)
    s.setsc('#elU', 'tmp', elU if el else 0)
    s.setsc('#icd', 'tmp', f['icd'])
    s.setsc('#skillDmg', 'tmp', f['skill'])
    s.setsc('#tfm', 'tmp', f['tfm'])
    s.setsc('#sub', 'itv', f['sub'])
    s.setsc('#trueDmg', 'tmp', 0)
    s.setsc('#mbPart', 'mb', 0)
    r = s.call('rlk:combat/apply', Ctx(b, tuple(b.pos), tuple(b.rot)))
    s.setsc('#sub', 'itv', 0)
    return r


def hp(s):
    b = body(s)
    return esc(s, b, 'mhpC') if b else None


def pbol(s):
    return s.sc(('e', s.player().id), 'bol') or 0


def pmax(s):
    return s.sc(('e', s.player().id), 'maxHealth')
