#!/usr/bin/env python3
"""seqsim.py: 홍련's sequences (tools/mboss_scarlet/seq.py, lane H2) in the lane's world camsim.CamSim, driven as the core
contract says and nothing more: #sq hr 0 + seq/<name>/start as the body, then #sq + 1 and seq/<name>/tick every fight tick,
the signal #sq_sig read and cleared right after it, until #sqdone. The driver runs at the head of the module tick (the
framework's mboss/d/tick), before the core's own tick, whose state is parked (#ph = the cs1 phase with no sequence of its
own: it only runs the rig tick, the looks and the ambience), so the suites stay valid while lane H1 rebuilds the core.
Scratch tool, never shipped; reads hr/tests/lib and hr/h2/camsim.py.

Recorded per driven tick in s.rec (a dict per tick): sq, live (camera id), body (pos, yaw), stage / stage2 (pos, yaw),
avatar pos, held, gm, sig, kit [(sub, args)], cmds; and, filled in when the world tick is over (the client's tick):
  ent {1, 2: (pos, rot)}    the camera ENTITIES on the server (a display stands 4 b before its viewpoint);
  cam {1, 2: (pos, rot)}    the VIEWPOINT of each camera as the client shows it (its interpolated pose, 4 b back along it):
                            what the picture is taken from - the shot sheets and the framing read this;
  cl {1, 2: (pos, rot, steps left, known)}  the client's entity pose and its running interpolation;
  view / srv                the picture's viewpoint through the camera the CLIENT is on / the same from the server pose;
  con                       the camera the client looks through (1 / 2, None: its own player);
  text / hint               the line and the hint on the live camera's texts;
  rig                       where her model stands (the rig's follow: see SeqSim.rig_follow);
  living                    the living entities in the world (type, their framework tags): a spectator sees every
                            invisible one of them as a ghost unless its texture is blank.
"""
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'tests' / 'lib'))
import hrsim as H  # noqa: E402
import camsim as CS  # noqa: E402
from mcsim import Ctx, split  # noqa: E402

C0 = H.C0
ROOT = H.ROOT_SC
CX, CY, CZ = 880.0, 201.0, 8.0
PARK_PH = 2                 # the core's cs1 phase: with #sqn 0 its state function does nothing
HUSK_EYE = 1.74             # her body: a husk at scale 1 (api.BOSS)
TRACE = []                  # the function path at a crash (see SeqSim.call)
# entity types a spectator never sees a ghost of (displays draw only their content, the others have no renderer; the local
# player is drawn only when it is the camera entity)
NOT_LIVING = ('marker', 'item_display', 'block_display', 'text_display', 'interaction', 'item', 'player', 'experience_orb')
LIVING_KEYS = ('rlk_av', 'rlk_vseat', 'rlk_mb_body', 'rlk_lure', 'rlk_mb_cam', 'rlk_mb_px')


class SeqSim(CS.CamSim):
    def __init__(self, root):
        super().__init__(root)
        self.drive = None           # {'name', 'args', 't', 'stop'}
        self.rec = []
        self.sigs = []              # (sequence, #sq, signal)
        self.done = []              # (sequence, #sq at #sqdone)
        self.actor_log = []         # (world tick, call, executor etype, pos, rot, macro, #cavT) of rlk:char/cine/*
        self.titles_log = []
        self.rig_pos, self.rig_cache = None, None
        self._fresh = []            # the records of this world tick (client_tick fills in the client's side)

    def rig_follow(self, fid, ctx):
        """Her model's place as the rig keeps it (boss/scarlet/rig/follow): rig/tick moves the parts to the EXECUTION position
        of its call when the body's place or yaw differs from the cached one (and caches the body's); rig/follow_now always.
        The hook's execution position is the body's place when the hook was entered: a body teleported inside the hook
        leaves her model behind unless rig/follow_now runs at the body afterwards (seq.RIG_NOW)."""
        b = H.body_of(self)
        if b is None:
            return
        cur = (tuple(math.floor(v * 100) for v in b.pos), math.floor(b.rot[0] * 100))
        if fid.endswith('/follow_now') or cur != self.rig_cache:
            self.rig_pos, self.rig_cache = tuple(ctx.pos), cur

    def client_tick(self):
        super().client_tick()
        pl = self.player()
        d = self.st(pl) if pl is not None else {}
        for r in self._fresh:
            ent, cam, cl = {}, {}, {}
            for i in (1, 2):
                e = next((e for e in self.ents if e.alive and f'rlk_mb_cam{i}' in e.tags), None)
                ent[i] = (tuple(e.pos), tuple(e.rot)) if e else None
                if e is not None and 'cl' in e.data:
                    cp, cr = tuple(e.data['cl'][0]), tuple(e.data['cl'][1])
                    f = CS.forward(cr)
                    cam[i] = (tuple(cp[k] - CS.BACK * f[k] for k in range(3)), cr)
                    cl[i] = (cp, cr, e.data['steps'], e.data.get('known', True))
                else:
                    cam[i], cl[i] = None, None
            r['ent'], r['cam'], r['cl'] = ent, cam, cl
            r['view'] = CS.client_view(self)
            e = self.ent(d.get('cam')) if d.get('cam') is not None else None
            r['srv'] = None
            if e is not None:
                f = CS.forward(e.rot)
                r['srv'] = (tuple(e.pos[k] - CS.BACK * f[k] for k in range(3)), tuple(e.rot))
            ce = self.ent(d.get('ccam')) if d.get('ccam') is not None else None
            r['con'] = next((i for i in (1, 2) if ce is not None and f'rlk_mb_cam{i}' in ce.tags), None)
            live = next((e for e in self.ents if e.alive and f'rlk_mb_cam{r["live"]}' in e.tags), None)
            tx = {t: next((x.data.get('text', '') for x in self.ents if x.alive and t in x.tags and live is not None
                           and x.data.get('riding') == live.id), None) for t in (CS.LINE_TAG, CS.HINT_TAG)}
            r['text'], r['hint'] = tx[CS.LINE_TAG], tx[CS.HINT_TAG]
            # (round W, WC 7) every text display that shows something: (the camera it rides 1 | 2, 0 = none; its tag; the text)
            cam_of = {e.id: i for i in (1, 2) for e in self.ents if e.alive and f'rlk_mb_cam{i}' in e.tags}
            r['texts'] = sorted((cam_of.get(x.data.get('riding'), 0), tg, x.data.get('text', '')) for x in self.ents
                                if x.alive and x.etype == 'text_display' and x.data.get('text') for tg in (CS.LINE_TAG, CS.HINT_TAG) if tg in x.tags)
            r['rig'] = self.rig_pos
            r['props'] = self.props()
            r['living'] = sorted({(e.etype, tuple(sorted(t for t in e.tags if t in LIVING_KEYS))) for e in self.ents
                                  if e.alive and e.etype not in NOT_LIVING})
            b = H.body_of(self)
            r['body1'] = (tuple(b.pos), b.rot[0]) if b else None      # her body when the tick is over
        self._fresh = []

    def call(self, fid, ctx, macro=None):
        TRACE.append(fid)                   # the function path of a crash (a suite prints it; popped on a normal return)
        try:
            r = self.call2(fid, ctx, macro)
        except Exception:
            if TRACE and TRACE[0] != '!':
                TRACE.insert(0, '!')            # frozen: the path at the first raise
            raise
        if not TRACE or TRACE[0] != '!':
            TRACE.pop()
        return r

    # ---- (round W) the sequence's prop cards (rlk_hr_sqp: the petals): their model and scale, for the shot sheets and the
    # petal checks (the kit's dress functions are stubs here: fx/prop/petal_big {look} = model petal_big_<k> at 0.8)
    PROP_LOOK = {'whole': 0, 'cut': 1, 'split': 2}

    def cmd(self, t, ctx):
        n0 = len(self.ents)
        r = super().cmd(t, ctx)
        if t[0] == 'summon' and 'item_display' in t[1] and len(t) > 5 and '"rlk_hr_sqp"' in t[5] and len(self.ents) > n0:
            e = self.ents[-1]
            m = re.search(r'"minecraft:item_model":"([^"]+)"', t[5])
            k = re.search(r'scale:\[(-?[0-9.]+)f', t[5])
            e.data['model'] = m.group(1) if m else None
            e.data['scale'] = float(k.group(1)) if k else 1.0
        if t[0] == 'data' and len(t) >= 5 and t[1] == 'merge' and t[2] == 'entity' and 'scale:[' in t[4]:
            for e in self._targets(t[3], ctx):
                if 'rlk_hr_sqp' in e.tags:
                    e.data['scale'] = float(re.search(r'scale:\[(-?[0-9.]+)f', t[4]).group(1))
        return r

    def props(self):
        return [dict(pos=tuple(e.pos), model=e.data.get('model'), scale=e.data.get('scale', 1.0), tags=sorted(x for x in e.tags if x.startswith('rlk_hr_sqp_')))
                for e in self.ents if e.alive and e.etype.endswith('item_display') and 'rlk_hr_sqp' in e.tags]

    def actor_root(self):
        return next((e for e in self.ents if e.alive and 'rlk_cine_root' in e.tags), None)

    @property
    def actor_on(self):
        return self.actor_root() is not None

    def call2(self, fid, ctx, macro=None):
        if fid == 'rlk:mboss/d/tick' and self.drive:
            self.step()
        if fid in (ROOT + 'rig/tick', ROOT + 'rig/follow_now'):
            self.rig_follow(fid, ctx)
        if fid == ROOT + 'fx/prop/petal_big' and ctx.ex is not None and 'rlk_hr_sqp' in ctx.ex.tags:
            ctx.ex.data['model'] = f'rlk:mboss/hr_kit/petal_big_{self.PROP_LOOK[(macro or {}).get("look", "whole")]}'
            ctx.ex.data['scale'] = 0.8
        if fid.startswith('rlk:char/cine/'):
            call = fid.rsplit('/', 1)[1]
            ex = ctx.ex
            self.actor_log.append((self.t, call, ex.etype if ex is not None else None, tuple(ctx.pos), tuple(ctx.rot), dict(macro or {}),
                                   self.sc('#cavT', 'cine')))
            # lane H3's actor as far as the sequences see it (its own suite is hr/tests/test_actor.py): spawn makes the root
            # marker (once; called again it moves it), stop removes it; the root dies with the framework's helper sweeps
            if call == 'spawn':
                root = self.actor_root()
                if root is None:
                    self.cmd(split('summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_cine_root"]}'), ctx)
                    root = self.actor_root()
                root.pos, root.rot = list(ctx.pos), [ctx.rot[0], 0.0]
            elif call == 'stop':
                for e in self.ents:
                    if 'rlk_cine_root' in e.tags:
                        e.alive = False
                self.ents = [e for e in self.ents if e.alive]
            return 1
        return super().call(fid, ctx, macro)

    # ---- the driver -----------------------------------------------------------------------------------------------------
    def step(self):
        d = self.drive
        b = H.body_of(self)
        if b is None:
            return
        b.data.setdefault('eye', HUSK_EYE)   # `facing entity <her body> eyes`: the husk's eye height (the lib leaves it 0)
        ctx = Ctx(b, tuple(b.pos), tuple(b.rot))
        k0, n0 = len(self.kitl), self.ncmd
        if d['t'] < 0:
            for k, v in (('#sq', 0), ('#sqdone', 0), ('#sq_sig', 0)):
                self.setsc(k, 'hr', v)
            d['t'] = 0
            self.call(f'{ROOT}seq/{d["name"]}/start', ctx, d.get('args'))
        else:
            self.setsc('#sq', 'hr', (self.sc('#sq', 'hr') or 0) + 1)
            d['t'] = self.sc('#sq', 'hr')
            self.call(f'{ROOT}seq/{d["name"]}/tick', ctx)
        sg = self.sc('#sq_sig', 'hr') or 0
        if sg:
            self.sigs.append((d['name'], self.sc('#sq', 'hr'), sg))
            self.setsc('#sq_sig', 'hr', 0)
        self.rec.append(self.snap(d['name'], sg, [(c, a) for _t, c, a in self.kitl[k0:]], self.ncmd - n0))
        self._fresh.append(self.rec[-1])
        if (self.sc('#sqdone', 'hr') or 0) == 1:
            self.done.append((d['name'], self.sc('#sq', 'hr')))
            self.setsc('#sqdone', 'hr', 0)
            nxt = d.get('then')
            self.drive = dict(name=nxt[0], args=nxt[1], t=-1, then=None) if nxt else None
            if nxt:
                self.step()          # the core starts the next sequence in the same tick (ending -> event)

    def marker(self, tag):
        e = next((e for e in self.ents if e.alive and tag in e.tags and e.etype == 'marker'), None)
        return (tuple(e.pos), e.rot[0]) if e else None

    def snap(self, name, sg, kit, cmds):
        b = H.body_of(self)
        pl = self.player()
        av = self.avatar()
        cams = {}
        for i in (1, 2):
            e = next((e for e in self.ents if e.alive and f'rlk_mb_cam{i}' in e.tags), None)
            cams[i] = (tuple(e.pos), tuple(e.rot)) if e else None
        return dict(seq=name, sq=self.sc('#sq', 'hr'), t=self.t, live=self.sc('#mbCamId', 'mb'), cam=cams,
                    body=(tuple(b.pos), b.rot[0]) if b else None, stage=self.marker('rlk_hr_stage'),
                    stage2=self.marker('rlk_hr_stage2'), avatar=tuple(av.pos) if av else None,
                    req=self.sc('#mbCam', 'mb') or 0, cx=self.sc('#sq_cx', 'hr') or 0, sig=sg, kit=kit, cmds=cmds,
                    held=CS.HOLD_TAG in pl.tags if pl else None, gm=self.st(pl)['gm'] if pl else None)


# ---------------------------------------------------------------------------------------------------- setup
def setup(dp, **kw):
    s, pl = CS.setup(dp, cls=SeqSim, **kw)
    s.storage.setdefault('rlk:pinv', {}).setdefault('order', [])    # a run's inventory record (the coda's grant reads it)
    return s, pl


def fight(s, park=True, limit=1200):
    """Her rift entered (the REAL sp/gate) until her body, the avatar and the arena exist; park: the intro ended at once
    (core/intro/done) and the core parked (see the module doc), the AI held. Returns ok."""
    z, a = H.rift_zone(s, 'scarlet')
    s.player().pos = list(a.pos)
    r = H.enter(s, a)
    s.zone_sc = z
    ok = bool(r) and CS.until(s, lambda s: H.body_of(s) is not None and s.avatar() is not None
                              and (H.mb(s, '#mbSt') or 0) == 0 and (s.sc('#sq', 'hr') or 0) >= 1, limit)
    if ok and park:
        H.call_sc(s, 'core/intro/done')
        park_core(s)
        CS.run(s, 2)
    return ok


def park_core(s):
    H.hold(s, True)
    for k, v in (('#ph', PARK_PH), ('#sqn', 0), ('#pat', 0), ('#rp', 0), ('#rvw', 0), ('#fl', 0)):
        s.setsc(k, 'hr', v)
    s.setsc('#mbFloor', 'mb', 0)
    s.setsc('#mbCine', 'mb', 0)
    b = H.body_of(s)
    b.tags.discard('rlk_mb_mv')


def place(s, av_xz, her_xz, av_yaw=None):
    """The avatar (the stage's origin) and her on the floor; the avatar faces her unless av_yaw is given."""
    av = s.avatar()
    av.pos = [float(av_xz[0]), CY, float(av_xz[1])]
    b = H.body_of(s)
    b.pos = [float(her_xz[0]), CY, float(her_xz[1])]
    b.tags.discard('rlk_mb_mv')
    yaw = math.degrees(math.atan2(-(b.pos[0] - av.pos[0]), b.pos[2] - av.pos[2]))
    av.rot = [yaw if av_yaw is None else float(av_yaw), 0.0]
    b.rot = [(yaw + 180.0) % 360 - 180, 0.0]
    H.C.moved(s)


def polar(r, bearing):
    """A floor point (x, z) at distance r from the arena centre on a compass bearing (0 = north = -z, 90 = east = +x)."""
    a = math.radians(bearing)
    return (CX + r * math.sin(a), CZ - r * math.cos(a))


def play(s, name, args=None, then=None, limit=None, each=None, until=None):
    """Drive sequence `name` from its start until #sqdone (or `until(s)`); returns the recorded ticks of this run."""
    k0 = len(s.rec)
    s.drive = dict(name=name, args=args, t=-1, then=then)
    n = 0
    lim = limit or 4000
    while s.drive is not None and n < lim:
        if each:
            each(s)
        k = len(s.rec)
        CS.world(s)
        n += 1
        if until and until(s):
            break
    return s.rec[k0:]


def go(s, n, each=None):
    for _ in range(n):
        if each:
            each(s)
        CS.world(s)


def stop(s):
    s.drive = None


def leftovers(s):
    """What a sequence may leave behind: {what: [...]} of the entities and flags that must be gone after a hand-back."""
    out = {}
    tags = ('rlk_hr_stage', 'rlk_hr_stage2', 'rlk_hr_sqh', 'rlk_hr_sqp', 'rlk_mb_cam', 'rlk_mb_camx', 'rlk_hr_ev')
    ents = [(e.etype, sorted(t for t in e.tags if t in tags)) for e in s.ents if e.alive and any(t in e.tags for t in tags)]
    if ents:
        out['entities'] = ents
    if (s.sc('#mbNoLeash', 'mb') or 0) != 0:
        out['#mbNoLeash'] = s.sc('#mbNoLeash', 'mb')
    if s.actor_on:
        out['actor'] = 'still spawned'
    return out
