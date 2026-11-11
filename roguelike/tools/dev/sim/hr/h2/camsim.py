#!/usr/bin/env python3
"""camsim.py: the world of lane H2's suites (hr/tests/test_cam.py, test_seq.py): hrsim.ScSim + the F5 view and the
cinematic lock (FN-cam, tools/build_mboss_core.py mboss/cam/**; hr_design.md §3.0 / §5.2). Scratch tool, never shipped;
it only reads hr/tests/lib (the vendored sims are not edited).

What it adds to ScSim:
- the player as the game has it in the F5 view: an avatar (mannequin rlk_av = the body rlk_body), the seat (armor_stand
  rlk_vseat riding the avatar) and the player riding the seat. The REAL view/tick runs for the player every tick (so its
  FN-cam guard sits where it sits in the file); its leaf functions are models here: view/spawn (the avatar at the
  player), view/ride_tick (the seat, the re-mount rule with the REAL view/ride_mount: not while sneaking), view/hold,
  view/fps_tick (developer mode: the player is the body, the view entities go), view/fresh (after /reload or a relog);
  the rest (move, aim, av_tick, the crosshair, the menu ...) are empty;
- the game rules the lock stands on (26.3 server jar, tools/build_mboss_core.py FN-cam): `gamemode` (spectator dismounts,
  leaving spectator resets the camera), `spectate [target]` (refused unless the player is in spectator mode, refused for
  a marker entity: no client tracking range), `ride`, a teleport of a player dismounts and resets the camera, and the
  player's own server tick after the functions (ServerPlayer.tick): a spectating player is snapped to the camera
  entity's position and rotation, sneaking or a dead camera entity ends the spectating; sneaking leaves a vehicle;
- selector argument gamemode=<mode> / gamemode=!<mode>;
- rlk:tick's FN-cam lines (read from the tested tree's tick.mcfunction) right after mboss/main, as in the file;
- logs: s.spectates (tick, the stand's tags), s.gm_log (tick, mode), s.attr_log, s.view_rest (ticks view/tick rested).
- s.cam_req (None | 1 | 2): a stand-in module request: while set, every module tick of the framework (mboss/d/tick,
  d/intro_tick, d/death_tick) sets #mbCam mb 1 and #mbCamId mb, as a module's locked sequence does.
"""
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tests' / 'lib'))
import hrsim as H  # noqa: E402
import mcsim  # noqa: E402
from mcsim import Ent, Ctx, split  # noqa: E402

C0 = H.C0
HOLD_TAG, CAM_TAG = 'rlk_mb_camh', 'rlk_mb_cam'
GM = ('survival', 'creative', 'adventure', 'spectator')
MODULE_TICKS = ('rlk:mboss/d/tick', 'rlk:mboss/d/intro_tick', 'rlk:mboss/d/death_tick')
VIEW_EMPTY = ('rlk:view/menu_do', 'rlk:view/burst_camera_tick', 'rlk:view/map_tick', 'rlk:view/move', 'rlk:view/sprint_fov',
              'rlk:view/av_tick', 'rlk:view/aim', 'rlk:view/slow', 'rlk:view/mob_aggro', 'rlk:boss/raiden/camera/hold',
              'rlk:view/sel_xhair', 'rlk:view/xhair', 'rlk:view/hand_wrap')
SEAT_UP = 1.9          # the seat above the avatar's feet, the riding player above the seat (positions only for show)


class CamSim(H.ScSim):
    def __init__(self, root):
        super().__init__(root)
        self.spectates, self.gm_log, self.attr_log = [], [], []
        self.view_rest = 0
        self.cam_req = None
        self.cam_lines = []
        self._cam_done = False
        self.view_on = False          # make_view() turns the F5 model on
        self.n_ride_tick = 0          # view/ride_tick runs (the body of view/tick reached)
        self.seats_made = 0
        self.cam_cost = []            # commands of rlk:tick's FN-cam lines per tick (hold / release included)

    # ------------------------------------------------------------------ player state
    @staticmethod
    def st(e):
        d = e.data
        d.setdefault('gm', 'adventure')
        d.setdefault('cam', None)
        d.setdefault('riding', None)
        return d

    def ent(self, eid):
        return next((e for e in self.ents if e.alive and e.id == eid), None)

    def avatar(self):
        return next((e for e in self.ents if e.alive and 'rlk_av' in e.tags), None)

    def seat(self):
        return next((e for e in self.ents if e.alive and 'rlk_vseat' in e.tags), None)

    def stands(self):
        return [e for e in self.ents if e.alive and CAM_TAG in e.tags]

    def unseat(self, e):
        self.st(e)['riding'] = None

    # ------------------------------------------------------------------ selectors: gamemode=
    def select(self, sel, ctx):
        if 'gamemode=' not in sel:
            return super().select(sel, ctx)
        head, body = sel[:2], sel[3:-1]
        keep, want = [], []
        for a in re.split(r',(?![^{\[]*[}\]])', body):
            (want if a.startswith('gamemode=') else keep).append(a)
        base = head + ('[' + ','.join(keep) + ']' if keep else '')
        res = super().select(base, ctx)
        for w in want:
            v = w.split('=', 1)[1]
            if v.startswith('!'):
                res = [e for e in res if e.etype == 'player' and self.st(e)['gm'] != v[1:]]
            else:
                res = [e for e in res if e.etype == 'player' and self.st(e)['gm'] == v]
        return res

    def _targets(self, tok, ctx):
        return ([ctx.ex] if ctx.ex is not None and ctx.ex.alive else []) if tok == '@s' else self.select(tok, ctx)

    # ------------------------------------------------------------------ execute: a missing entity ends the branch
    def execute(self, t, ctx):
        """`facing entity <sel>`, `positioned as <sel>`, `rotated as <sel>` with no such entity: the game runs nothing (mcsim
        indexes the empty selection). Checked up to the first `as` / `run` (after an `as` mcsim recurses into here)."""
        i = 0
        while i < len(t) and t[i] not in ('run', 'as'):
            if t[i] == 'facing' and i + 2 < len(t) and t[i + 1] == 'entity':
                if not self._targets(t[i + 2], ctx):
                    return 0
                i += 4
            elif t[i] in ('positioned', 'rotated') and i + 2 < len(t) and t[i + 1] == 'as':
                if not self._targets(t[i + 2], ctx):
                    return 0
                i += 3
            else:
                i += 1
        return super().execute(t, ctx)

    # ------------------------------------------------------------------ commands
    def cmd(self, t, ctx):
        c = t[0]
        if c == 'gamemode':
            assert t[1] in GM, t
            es = self._targets(t[2], ctx) if len(t) > 2 else ([ctx.ex] if ctx.ex else [])
            for e in es:
                d = self.st(e)
                if d['gm'] == t[1]:
                    continue
                d['gm'] = t[1]
                self.gm_log.append((self.t, t[1]))
                if t[1] == 'spectator':
                    d['riding'] = None            # ServerPlayer.setGameMode: stopRiding
                else:
                    d['cam'] = None               # ... setCamera(this)
            self.ncmd += 1
            return 1 if es else 0
        if c == 'spectate':
            self.ncmd += 1
            pl = ctx.ex if len(t) < 3 else (self._targets(t[2], ctx) or [None])[0]
            if pl is None or pl.etype != 'player' or self.st(pl)['gm'] != 'spectator':
                return 0                          # ERROR_NOT_SPECTATOR
            if len(t) == 1:
                self.st(pl)['cam'] = None
                return 1
            tg = self._targets(t[1], ctx)
            if not tg or tg[0] is pl or tg[0].etype == 'marker':
                return 0                          # no entity / ERROR_SELF / ERROR_CANNOT_SPECTATE (tracking range 0)
            if self.st(pl)['cam'] != tg[0].id:
                pl.pos = list(tg[0].pos)          # setCamera: teleportTo the camera
            self.st(pl)['cam'] = tg[0].id
            self.spectates.append((self.t, frozenset(tg[0].tags)))
            return 1
        if c == 'ride':
            self.ncmd += 1
            es = self._targets(t[1], ctx)
            if not es:
                return 0
            e = es[0]
            if t[2] == 'dismount':
                ok = self.st(e)['riding'] is not None
                self.st(e)['riding'] = None
                return 1 if ok else 0
            v = self._targets(t[3], ctx)
            if not v or self.st(e)['riding'] is not None:
                return 0
            self.st(e)['riding'] = v[0].id
            return 1
        if c == 'attribute':
            self.ncmd += 1
            self.attr_log.append((self.t, ' '.join(t[1:])))
            return 1
        if c == 'data' and len(t) > 3 and t[1] == 'get' and t[2] == 'entity' and not self._targets(t[3], ctx):
            return 0                                   # no such entity: the command fails (mcsim indexes the empty selection)
        if c == 'tp':
            # a teleported player leaves its vehicle and its camera (TeleportCommand: resetCamera)
            for e in self._targets(t[1], ctx):
                if e.etype == 'player':
                    d = self.st(e)
                    d['riding'], d['cam'] = None, None
        return super().cmd(t, ctx)

    # ------------------------------------------------------------------ function hooks
    def call(self, fid, ctx, macro=None):
        if fid in MODULE_TICKS and self.cam_req:
            self.setsc('#mbCam', 'mb', 1)
            self.setsc('#mbCamId', 'mb', int(self.cam_req))
        if fid == 'rlk:mboss/main' and not self._cam_done and len(self.stack) == 0:
            r = super().call(fid, ctx, macro)
            self.run_cam_lines()
            return r
        if self.view_on:
            if fid in VIEW_EMPTY:
                return 1
            hook = {'rlk:view/spawn': self.v_spawn, 'rlk:view/ride_tick': self.v_ride_tick, 'rlk:view/hold': self.v_hold,
                    'rlk:view/fps_tick': self.v_fps, 'rlk:view/fresh': self.v_fresh}.get(fid)
            if hook:
                hook(ctx)
                return 1
        return super().call(fid, ctx, macro)

    def run_cam_lines(self):
        """rlk:tick's FN-cam lines (after mboss/main)."""
        self._cam_done = True
        n0 = self.ncmd
        for ln in self.cam_lines:
            self.cmd(split(ln), C0)
        self.cam_cost.append(self.ncmd - n0)

    # ------------------------------------------------------------------ the F5 view model
    def v_spawn(self, ctx):
        for e in self.ents:
            if 'rlk_view' in e.tags:
                e.alive = False
        self.ents = [e for e in self.ents if e.alive]
        pl = ctx.ex
        av = Ent('mannequin', ctx.pos, (pl.rot[0], 0.0), ['rlk_view', 'rlk_av', 'rlk_body', 'rlk_pet'])
        av.data['eye'] = 1.62
        self.ents.append(av)
        self.unseat(pl)

    def v_ride_tick(self, ctx):
        self.n_ride_tick += 1
        pl, av = ctx.ex, self.avatar()
        if av is None:
            return
        seat = self.seat()
        if seat is None:
            seat = Ent('armor_stand', (av.pos[0], av.pos[1] + SEAT_UP, av.pos[2]), (0.0, 0.0), ['rlk_view', 'rlk_vseat', 'rlk_pet'])
            self.ents.append(seat)
            self.seats_made += 1
        self.st(seat)['riding'] = av.id
        if self.st(pl)['riding'] != seat.id:
            if self._sneak(pl):
                pl.pos = [seat.pos[0], seat.pos[1] + 0.99, seat.pos[2]]
            else:
                self.call('rlk:view/ride_mount', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))

    def v_hold(self, ctx):
        pl = ctx.ex
        seat = self.seat()
        if seat is not None:
            self.unseat(pl)
            seat.alive = False
            self.ents = [e for e in self.ents if e.alive]

    def _teardown(self, pl):
        av = self.avatar()
        if av is not None and not (self.sc(('e', pl.id), 'pkMode') or 0) >= 1 and (self.sc(('e', pl.id), 'dead') or 0) != 1:
            pl.pos = list(av.pos)
            self.st(pl)['cam'] = None
        self.unseat(pl)
        for e in self.ents:
            if 'rlk_view' in e.tags:
                e.alive = False
        self.ents = [e for e in self.ents if e.alive]
        pl.tags.add('rlk_body')

    def v_fps(self, ctx):
        pl = ctx.ex
        if any('rlk_view' in e.tags for e in self.ents if e.alive):
            self._teardown(pl)
        pl.tags.add('rlk_body')

    def v_fresh(self, ctx):
        self.setsc('#vFresh', 'view', 0)
        if any('rlk_view' in e.tags for e in self.ents if e.alive):
            self._teardown(ctx.ex)

    # ------------------------------------------------------------------ the player's own server tick
    def net_tick(self, pl):
        d = self.st(pl)
        if d['cam'] is not None:
            cam = self.ent(d['cam'])
            if cam is not None:
                pl.pos, pl.rot = list(cam.pos), list(cam.rot)
                if self._sneak(pl):
                    d['cam'] = None               # wantsToStopRiding
            else:
                d['cam'] = None                   # the camera entity is dead
        if d['riding'] is not None:
            v = self.ent(d['riding'])
            if v is None or self._sneak(pl):
                d['riding'] = None
        seat, av = self.seat(), self.avatar()
        if seat is not None and av is not None:
            seat.pos = [av.pos[0], av.pos[1] + SEAT_UP, av.pos[2]]
            if d['riding'] == seat.id:
                pl.pos = [seat.pos[0], seat.pos[1] + 0.5, seat.pos[2]]


# ---------------------------------------------------------------------------------------------------- setup / tick
def tick_cam_lines(dp):
    """The FN-cam lines of rlk:tick after mboss/main (the commands, in file order)."""
    lines = (Path(dp) / 'data/rlk/function/tick.mcfunction').read_text(encoding='utf-8').split('\n')
    i = next(i for i, l in enumerate(lines) if l.strip() == 'execute if score #mbLive mb matches 1 run function rlk:mboss/main')
    return [l for l in lines[i + 1:] if 'rlk:mboss/cam/' in l and not l.startswith('#')]


def setup(dp, cls=CamSim, view=True, gm='adventure', **kw):
    """H.setup_sc with the CamSim world; view: the F5 model on (the avatar and the seat are made by the first tick)."""
    s, pl = H.setup_sc(dp, cls=cls, **kw)
    s.cam_lines = tick_cam_lines(dp)
    s.st(pl)['gm'] = gm
    pl.data['eye'] = 0.1
    if view:
        make_view(s)
    return s, pl


def make_view(s):
    pl = s.player()
    s.view_on = True
    pl.tags.discard('rlk_body')
    for o in ('vBig', 'vMap', 'vMapH', 'vMapL', 'vMapR', 'rlkMenu', 'devMode', 'dead', 'pkMode', 'rdCam'):
        if s.sc(('e', pl.id), o) is None:
            s.setsc(('e', pl.id), o, 0)
    s.setsc('#vFresh', 'view', 0)
    s.setsc('#t', 'view', 0)
    s.setsc('#spr', 'view', 0)
    s.setsc('#sprNow', 'view', 0)


def view_tick(s):
    """rlk:tick's `execute as @a[tag=player] run function rlk:view/tick` (the REAL file; its leaves are the models above)."""
    pl = s.player()
    if pl is None or not s.view_on:
        return
    n0 = s.n_ride_tick
    s.call('rlk:view/tick', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    if HOLD_TAG in pl.tags and s.n_ride_tick == n0:
        s.view_rest += 1              # the guard ended view/tick before its body (no move, no aim, no re-seat)


def world(s):
    """One game tick: rlk:tick's view/tick for the player, the fight tick (H.world_sc: mboss/main, then here the FN-cam
    lines as in rlk:tick), then the player's own server tick."""
    view_tick(s)
    s._cam_done = False
    H.world_sc(s)
    if not s._cam_done:
        s.run_cam_lines()
    pl = s.player()
    if pl is not None:
        s.net_tick(pl)


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


def fight(s, sid, limit=900, state=1):
    """The rift of special `sid` entered (the REAL sp/gate), ticks until #mbSt = state. Returns ok."""
    z, a = H.rift_zone(s, sid)
    s.player().pos = list(a.pos)
    r = H.enter(s, a)
    s.zone_sc = z
    if not r:
        return False
    return until(s, lambda s: H.body_of(s) is not None and (H.mb(s, '#mbSt') or 0) == state
                 and s.avatar() is not None, limit)


def held(s):
    pl = s.player()
    return pl is not None and HOLD_TAG in pl.tags


def gm(s):
    return s.st(s.player())['gm']


def watching(s):
    """The tags of the stand the player spectates, or None."""
    pl = s.player()
    e = s.ent(s.st(pl)['cam']) if s.st(pl)['cam'] is not None else None
    return frozenset(e.tags) if e is not None else None


def seated(s):
    pl, seat = s.player(), s.seat()
    return seat is not None and s.st(pl)['riding'] == seat.id


def clean(s, gm0='adventure', stands=False, seat=True, req=True):
    """The hand-back invariants: {name: ok}. The player is not held, in the game mode it had, not spectating; no hold /
    game-mode tag; the stored return point gone; with `req`: the request is off; with `seat`: at the avatar and on the F5
    seat; `stands` False: no camera stand left."""
    pl = s.player()
    av = s.avatar()
    d = s.st(pl)
    out = {
        'not held': HOLD_TAG not in pl.tags,
        f'game mode {gm0}': d['gm'] == gm0,
        'not spectating': d['cam'] is None,
        'no game-mode tag': not ({'rlk_mb_cgS', 'rlk_mb_cgC'} & pl.tags),
        'return point cleared': 'camret' not in s.storage.get('rlk:mboss', {}),
    }
    if req:
        out['request off'] = (s.sc('#mbCam', 'mb') or 0) == 0
    if seat:
        out['on the F5 seat'] = seated(s)
        out['at the avatar'] = av is not None and math.hypot(pl.pos[0] - av.pos[0], pl.pos[2] - av.pos[2]) < 1e-6
    if not stands:
        out['no camera stand'] = not s.stands()
    return out
