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
- (round V, lane VC) the client's picture of the cameras (empty item_displays; 26.3 bytecode, vc_progress.md "Verified"):
  a new entity reaches the client with the pose of its summon; each later change of its server pose is a move the client
  gets at the end of that server tick: rotation as bytes (360 / 256 degrees, floored) unless the entity's OnGround flag
  differs from the one last sent (then the float sync packet); the move is applied with the interpolation length the
  client had BEFORE this tick (teleport_duration is entity data, sent after the move): 0 = a snap, else position and
  rotation go there linearly over that many client ticks (a new target restarts from where the entity is).
  e.data['cl'] = [pos, rot] after each world tick, e.data['sent'] = every rotation sent, e.data['segs'] = [(tick, length)].
- the client's camera: s.st(pl)['ccam'] = the entity the CLIENT looks through (None: its own player). The server sends a
  camera packet only when its own camera changes; the client ignores one for an entity it does not have. An entity is
  known to the client from its summon unless s.pair_later is set (a place still arriving: its chunk is not sent yet); the
  server pairs it in the player's own tick (ChunkMap.move) once s.pair_later is off. client_view(s) = (viewpoint,
  rotation) of the picture: 4 blocks behind a display camera along its view (F5), or the player's own third-person view.
- the game's player tick (net_tick): a spectating player is snapped to the camera, sneaking ends the spectate, and then
  the `tick` advancement trigger fires: mboss/cam/post runs when the hold armed it this tick (advancement revoke).
- the hold's attribute modifiers (s.mods(e)), the sidebar (s.sidebar), action bars (s.abar; tellraws are cmsim's s.tells), the
  input predicates rlk:in_jump / in_f / in_b / in_l / in_r / in_sprint (e.data['keys']), data merge on the cameras and
  their texts (teleport_duration, OnGround, text, background), the passengers of a summon (the texts).
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
CAM_PART, LINE_TAG, HINT_TAG = 'rlk_mb_camx', 'rlk_mb_camt', 'rlk_mb_camk'
GRID = 360.0 / 256.0
BACK = 4.0
POST_ADV, POST_FN = 'rlk:mboss/cam_post', 'rlk:mboss/cam/post'
KEYS = {'rlk:in_jump': 'jump', 'rlk:in_f': 'f', 'rlk:in_b': 'b', 'rlk:in_l': 'l', 'rlk:in_r': 'r', 'rlk:in_sprint': 'sprint'}
ATTR_BASE = {'minecraft:entity_interaction_range': 3.0, 'minecraft:block_interaction_range': 4.5, 'minecraft:scale': 0.0625,
             'minecraft:camera_distance': 0.0}
GM = ('survival', 'creative', 'adventure', 'spectator')
MODULE_TICKS = ('rlk:mboss/d/tick', 'rlk:mboss/d/intro_tick', 'rlk:mboss/d/death_tick')
VIEW_EMPTY = ('rlk:view/ride_apply', 'rlk:view/menu_do', 'rlk:view/burst_camera_tick', 'rlk:view/map_tick', 'rlk:view/move', 'rlk:view/sprint_fov',
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
        self.pair_later = False       # True: a new entity is not known to the client until this is off (a place arriving)
        self.post_armed = set()       # players whose tick advancement is revoked (the reward runs in their next own tick)
        self.post_runs = []           # ticks mboss/cam/post ran
        self.cam_packets = []         # (tick, entity id | None, applied by the client)
        self.sidebar = 'stacks'
        self.abar = []

    # ------------------------------------------------------------------ player state
    @staticmethod
    def st(e):
        d = e.data
        d.setdefault('gm', 'adventure')
        d.setdefault('cam', None)
        d.setdefault('ccam', None)
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

    def cam_texts(self, tag=LINE_TAG):
        return [e for e in self.ents if e.alive and tag in e.tags]

    def mods(self, e):
        return e.data.setdefault('mods', {})

    def attr(self, e, name):
        """An attribute's value: the base (ATTR_BASE) with the modifiers the functions added."""
        base = ATTR_BASE[name]
        ms = self.mods(e).get(name, {}).values()
        v = base + sum(a for a, op in ms if op == 'add_value')
        v += base * sum(a for a, op in ms if op == 'add_multiplied_base')
        for a, op in ms:
            if op == 'add_multiplied_total':
                v *= 1 + a
        return v

    def set_camera(self, pl, ent):
        """ServerPlayer.setCamera: a packet only when the camera changes; the client ignores an entity it does not have."""
        d = self.st(pl)
        new = ent.id if ent is not None else None
        if d['cam'] == new:
            return
        d['cam'] = new
        if ent is not None:
            pl.pos = list(ent.pos)
        ok = ent is None or ent.data.get('known', True)
        if ok:
            d['ccam'] = new
        self.cam_packets.append((self.t, new, ok))

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
            if t[i] in ('if', 'unless') and i + 2 < len(t) and t[i + 1] == 'predicate' and t[i + 2] in KEYS:
                ok = ctx.ex is not None and KEYS[t[i + 2]] in ctx.ex.data.get('keys', ())
                if ok == (t[i] == 'unless'):
                    return 0
                return self.execute(t[:i] + t[i + 3:], ctx)
            i += 1
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

    # ------------------------------------------------------------------ the client's picture of the cameras
    def spawned(self, e, nbt=''):
        """A camera was summoned: the spawn packet carries this pose and its entity data."""
        import re as _re
        m = _re.search(r'teleport_duration:(\d+)', nbt.split('Passengers:')[0])
        e.data['dur'] = int(m.group(1)) if m else 0
        e.data['og'] = False
        e.data['spawn'] = (list(e.pos), list(e.rot))
        e.data['sent'], e.data['segs'] = [tuple(e.rot)], []
        e.data['known'] = not self.pair_later

    def client_tick(self):
        """One client tick of every camera: a changed server pose is a move (bytes, or floats when OnGround flipped) that
        starts an interpolation of the length the client had before this tick, then the new length arrives."""
        for e in self.stands():
            d = e.data
            if not d.get('known', True):
                continue
            if 'cl' not in d:
                sp = d.get('spawn') or (list(e.pos), list(e.rot))
                d['cl'], d['tgt'], d['steps'], d['cdur'] = [list(sp[0]), list(sp[1])], (tuple(sp[0]), tuple(sp[1])), 0, d.get('dur', 0)
                d['og_sent'], d['last'] = False, (tuple(sp[0]), tuple(sp[1]))
            srv = (tuple(e.pos), tuple(e.rot))
            flt = d.get('og', False) != d['og_sent']
            if srv != d['last'] or flt:
                rot = srv[1] if flt else tuple(math.floor(v * 256.0 / 360.0) * 360.0 / 256.0 for v in srv[1])
                d['sent'].append(rot)
                d['og_sent'], d['last'] = d.get('og', False), srv
                tgt = (srv[0], rot)
                if d['cdur'] == 0:
                    d['cl'], d['tgt'], d['steps'] = [list(tgt[0]), list(tgt[1])], tgt, 0
                elif not (d['steps'] > 0 and tgt == d['tgt']):
                    d['tgt'], d['steps'] = tgt, d['cdur']
                    d['segs'].append((self.t, d['cdur']))
            d['cdur'] = d.get('dur', 0)
            if d['steps'] > 0:
                k = d['steps']
                d['cl'][0] = [a + (b - a) / k for a, b in zip(d['cl'][0], d['tgt'][0])]
                d['cl'][1] = [a + ((b - a + 180) % 360 - 180) / k for a, b in zip(d['cl'][1], d['tgt'][1])]
                d['steps'] = k - 1

    # ------------------------------------------------------------------ commands
    def cmd(self, t, ctx):
        c = t[0]
        if c == 'summon' and 'item_display' in t[1] and f'"{CAM_TAG}"' in (t[5] if len(t) > 5 else ''):
            n0 = len(self.ents)
            r = super().cmd(t, ctx)
            if len(self.ents) > n0:
                cam = self.ents[-1]
                self.spawned(cam, t[5])
                for tags in re.findall(r'\{id:"minecraft:text_display",Tags:\[([^\]]*)\]', t[5]):   # its passengers
                    p = Ent('text_display', tuple(cam.pos), (0.0, 0.0), re.findall(r'"([^"]+)"', tags))
                    p.data.update(riding=cam.id, text='', bg=0)
                    self.ents.append(p)
            return r
        if c == 'data' and len(t) >= 5 and t[1] == 'merge' and t[2] == 'entity':
            self.ncmd += 1
            es = self._targets(t[3], ctx)
            for e in es:
                m = re.search(r'teleport_duration:(\d+)', t[4])
                if m:
                    e.data['dur'] = int(m.group(1))
                m = re.search(r'OnGround:(\d)b', t[4])
                if m:
                    e.data['og'] = m.group(1) == '1'
                if e.etype == 'text_display' and 'text:' in t[4]:
                    e.data['text'] = ''.join(re.findall(r'text:"([^"]*)"', t[4]))
                    m = re.search(r'background:(-?\d+)', t[4])
                    e.data['bg'] = int(m.group(1)) if m else e.data.get('bg', 0)
            return 1 if es else 0
        if c == 'advancement' and t[1] == 'revoke' and t[3] == 'only' and t[4] == POST_ADV:
            self.ncmd += 1
            for e in self._targets(t[2], ctx):
                self.post_armed.add(e.id)
            return 1
        if c == 'scoreboard' and t[1] == 'objectives' and t[2] == 'setdisplay' and t[3] == 'sidebar':
            self.ncmd += 1
            self.sidebar = t[4] if len(t) > 4 else None
            return 1
        if c == 'title' and len(t) > 2 and t[2] == 'actionbar':
            self.abar.append((self.t, ' '.join(t[3:])))

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
                    self.set_camera(e, None)      # ... setCamera(this)
            self.ncmd += 1
            return 1 if es else 0
        if c == 'spectate':
            self.ncmd += 1
            pl = ctx.ex if len(t) < 3 else (self._targets(t[2], ctx) or [None])[0]
            if pl is None or pl.etype != 'player' or self.st(pl)['gm'] != 'spectator':
                return 0                          # ERROR_NOT_SPECTATOR
            if len(t) == 1:
                self.set_camera(pl, None)
                return 1
            tg = self._targets(t[1], ctx)
            if not tg or tg[0] is pl or tg[0].etype == 'marker':
                return 0                          # no entity / ERROR_SELF / ERROR_CANNOT_SPECTATE (tracking range 0)
            self.set_camera(pl, tg[0])            # setCamera: teleportTo the camera, the packet when it changed
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
            if len(t) >= 6 and t[3] == 'modifier':
                for e in self._targets(t[1], ctx):
                    ms = self.mods(e).setdefault(t[2], {})
                    if t[4] == 'add':
                        ms.setdefault(t[5], (float(t[6]), t[7]))
                    elif t[4] == 'remove':
                        ms.pop(t[5], None)
            return 1
        if c == 'data' and len(t) > 3 and t[1] == 'get' and t[2] == 'entity' and not self._targets(t[3], ctx):
            return 0                                   # no such entity: the command fails (mcsim indexes the empty selection)
        if c == 'tp':
            # a teleported player leaves its vehicle and its camera (TeleportCommand: resetCamera)
            for e in self._targets(t[1], ctx):
                if e.etype == 'player':
                    self.st(e)['riding'] = None
                    self.set_camera(e, None)
            r = super().cmd(t, ctx)
            for e in self._targets(t[1], ctx):
                if e.etype != 'player':
                    e.data['og'] = True           # TeleportCommand: setOnGround(true)
            return r
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
            self.set_camera(pl, None)
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
                if not self.pair_later:           # ChunkMap.move(player): entities whose chunk has been sent are paired
                    for e in self.ents:
                        if e.alive and e.data.get('known') is False:
                            e.data['known'] = True
                if self._sneak(pl):
                    self.set_camera(pl, None)     # wantsToStopRiding
            else:
                self.set_camera(pl, None)         # the camera entity is dead
        elif not self.pair_later:
            for e in self.ents:
                if e.alive and e.data.get('known') is False:
                    e.data['known'] = True
        if pl.id in self.post_armed:              # CriteriaTriggers.TICK right after the camera handling: the reward
            self.post_armed.discard(pl.id)
            self.post_runs.append(self.t)
            self.call(POST_FN, Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
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
    s.client_tick()


def forward(rot):
    y, p = math.radians(rot[0]), math.radians(rot[1])
    return (-math.sin(y) * math.cos(p), -math.sin(p), math.cos(y) * math.cos(p))


def client_view(s):
    """(viewpoint, rot) of the held player's picture in F5: 4 blocks behind the client pose of the camera the CLIENT is on
    (None when the client is on its own player: own_view)."""
    pl = s.player()
    cid = s.st(pl).get('ccam') if pl is not None else None
    e = s.ent(cid) if cid is not None else None
    if e is None or 'cl' not in e.data:
        return None
    pos, rot = e.data['cl']
    f = forward(rot)
    return tuple(pos[i] - BACK * f[i] for i in range(3)), tuple(rot)


def client_cam(s):
    """(pos, rot) of the camera entity as the client has it (None when the client is not on a camera)."""
    pl = s.player()
    cid = s.st(pl).get('ccam') if pl is not None else None
    e = s.ent(cid) if cid is not None else None
    if e is None or 'cl' not in e.data:
        return None
    return tuple(e.data['cl'][0]), tuple(e.data['cl'][1])


def own_view(s):
    """(viewpoint, rot) of the player's own third-person picture where the server keeps a spectating player (at the
    camera entity, its rotation): the eye 1.62 x scale over the feet, pulled back scale x camera_distance."""
    pl = s.player()
    sc, cd = s.attr(pl, 'minecraft:scale'), s.attr(pl, 'minecraft:camera_distance')
    f = forward(pl.rot)
    return tuple(pl.pos[i] + (1.62 * sc if i == 1 else 0.0) - sc * cd * f[i] for i in range(3)), tuple(pl.rot)


def on_grid(rot, eps=1e-6):
    return all(abs(v / GRID - round(v / GRID)) < eps for v in rot)


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
    """The tags of the camera the player spectates (the server's view of it), or None."""
    pl = s.player()
    e = s.ent(s.st(pl)['cam']) if s.st(pl)['cam'] is not None else None
    return frozenset(e.tags) if e is not None else None


def client_on(s):
    """The tags of the camera the CLIENT looks through, or None (its own player)."""
    pl = s.player()
    e = s.ent(s.st(pl).get('ccam')) if s.st(pl).get('ccam') is not None else None
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
        'the client on its own view': d.get('ccam') is None,
        'no hold modifier left': not any(v for v in s.mods(pl).values()),
        'the sidebar back': s.sidebar == 'stacks',
    }
    if req:
        out['request off'] = (s.sc('#mbCam', 'mb') or 0) == 0
    if seat:
        out['on the F5 seat'] = seated(s)
        out['at the avatar'] = av is not None and math.hypot(pl.pos[0] - av.pos[0], pl.pos[2] - av.pos[2]) < 1e-6
    if not stands:
        out['no camera stand'] = not [e for e in s.ents if e.alive and CAM_PART in e.tags]
    return out
