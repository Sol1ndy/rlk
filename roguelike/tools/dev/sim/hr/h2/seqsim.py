#!/usr/bin/env python3
"""seqsim.py: 홍련's sequences (tools/mboss_scarlet/seq.py, lane H2) in the lane's world camsim.CamSim, driven as the core
contract says and nothing more: #sq hr 0 + seq/<name>/start as the body, then #sq + 1 and seq/<name>/tick every fight tick,
the signal #sq_sig read and cleared right after it, until #sqdone. The driver runs at the head of the module tick (the
framework's mboss/d/tick), before the core's own tick, whose state is parked (#ph = the cs1 phase with no sequence of its
own: it only runs the rig tick, the looks and the ambience), so the suites stay valid while lane H1 rebuilds the core.
Scratch tool, never shipped; reads hr/tests/lib and hr/h2/camsim.py.

Recorded per driven tick in s.rec (a dict per tick): sq, live (camera id), cam {1, 2: (pos, rot)}, body (pos, yaw), stage /
stage2 (pos, yaw), avatar pos, held, gm, sig, kit [(sub, args)], cmds.
"""
import math
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


class SeqSim(CS.CamSim):
    def __init__(self, root):
        super().__init__(root)
        self.drive = None           # {'name', 'args', 't', 'stop'}
        self.rec = []
        self.sigs = []              # (sequence, #sq, signal)
        self.done = []              # (sequence, #sq at #sqdone)
        self.actor_log = []         # (world tick, call, executor etype, pos, rot, macro, #cavT) of rlk:char/cine/*
        self.titles_log = []

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

    def actor_root(self):
        return next((e for e in self.ents if e.alive and 'rlk_cine_root' in e.tags), None)

    @property
    def actor_on(self):
        return self.actor_root() is not None

    def call2(self, fid, ctx, macro=None):
        if fid == 'rlk:mboss/d/tick' and self.drive:
            self.step()
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
        for r in s.rec[k:]:
            r['view'] = CS.client_view(s)          # the client's picture after this tick (camsim's spawn / glide model)
            r['srv'] = None
            pl = s.player()
            e = s.ent(s.st(pl)['cam']) if pl is not None and s.st(pl)['cam'] is not None else None
            if e is not None:
                r['srv'] = (tuple(e.pos), tuple(e.rot))
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
    tags = ('rlk_hr_stage', 'rlk_hr_stage2', 'rlk_hr_sqh', 'rlk_hr_sqp', 'rlk_mb_cam', 'rlk_hr_ev')
    ents = [(e.etype, sorted(t for t in e.tags if t in tags)) for e in s.ents if e.alive and any(t in e.tags for t in tags)]
    if ents:
        out['entities'] = ents
    if (s.sc('#mbNoLeash', 'mb') or 0) != 0:
        out['#mbNoLeash'] = s.sc('#mbNoLeash', 'mb')
    if s.actor_on:
        out['actor'] = 'still spawned'
    return out
