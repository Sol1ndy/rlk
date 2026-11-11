"""The camera tracks of 홍련's locked sequences (hr_design.md §3.0 / §5.2; round V lane VC: v_brief.md §3 "VC" 1-3). Pure
data + line builders: no files are written here; seq.py merges a track's lines into its sequence's timeline.

The mechanism (FN-cam of the framework, tools/mboss_lib.py / tools/build_mboss_core.py; the client and server facts are in
tools/dev/plan/combat/review/v/client_facts.md and vc_progress.md): the module sets `#mbCam mb 1` every tick of a locked
sequence and `#mbCamId mb` 1 (camera A = rlk_mb_cam1) or 2 (B = rlk_mb_cam2); rlk:tick spectates the live camera. A camera
is an empty item_display. The game is played in F5: the client looks from 4 blocks BEHIND a non-living camera entity along
its view, so a camera is placed AT the wanted viewpoint, aimed, and mboss/cam/fix puts its rotation on the 360 / 256 degree
grid (the only rotations that reach the client exactly) and moves it 4 blocks forward. Everything below speaks of the
viewpoint ("eye"); the entity is always eye + 4 * forward.

- A shot = keyframes. Between two keyframes the CLIENT interpolates position and rotation linearly over the display's
  teleport_duration (<= 59 ticks): one placement per segment at its first tick (the target = the segment's end), the
  duration set one tick ahead (the client applies a duration to the moves that arrive after it). No per-tick placement,
  so no 1.4-degree stepping: a slow pan is one long constant-speed move between two grid rotations.
- A hard cut = the other camera made live. The idle camera is prepared PRE ticks ahead: duration 0 (t - 3), the placement
  at the shot's first keyframe (t - 2: with duration 0 the client snaps, no glide), the first segment's duration (t - 1);
  it has stood still at its place for two ticks when it goes live. Consecutive shots alternate A / B and every shot lasts
  at least PRE ticks (asserted); the last move of a shot ends before the next cut.
- Subjects that move: a look or eye point in her frame (HR) is resolved against her body when the placement runs. A
  segment's target is where she WILL be at its end: `her(t)` (the sequence's own table of her moves on the stage) gives
  the displacement and the turn over the segment, added to her place at the first tick (`lead`). track() cuts a span into
  such segments (a walk, a turn); chase() is for the two shots whose subject crosses the frame fast (a leap, the arc
  back): a placement every tick at the client's 3-tick interpolation, which smooths the grid steps.
- A new camera reaches the client with the pose of its summon: Track.spawn() makes each one where its first shot puts it
  (mboss/cam/spawn_at: the rotation in the summon NBT).

Points: ST(r, u, f) / ST2(r, u, f) in the stage frames (r to the actor's right, u up, f forward; the markers rlk_hr_stage /
rlk_hr_stage2, pitch 0), HR(r, u, f) at her body (f along her facing, r her right), W(x, y, z) world, ENT(selector, anchor)
an entity (a look point only).
`clamp`: the eye is pulled into the walk disc of the arena after it is placed (mboss/ar/clampw, 24.3 b from the axis) and
aimed again; after mboss/cam/fix the entity (4 blocks further along the view) is pulled in too and kept off the floor
(`inside`, the module's function), so the 4-block line the client looks along lies inside the disc, above the ground. Shots of a fixed stage (CS0) are checked offline instead (test_seq) and skip it.
`lift`: a clamped track's low eye (below LOW over the stage floor) is not left inside a plant of the field.
`over`: with the actor's back at the wall the clamp brings an eye meant to be behind the actor onto it: the track's over
function may put the lens over the actor's head instead.
"""
import math

import mboss_lib as L

PRE = 3                       # ticks an idle camera is prepared before its cut (duration 0, the snap, the next duration)
SEG_MAX = L.CAM_SEG_MAX       # the longest segment (teleport_duration is clamped to 59)
TURN_MAX = 12.0               # degrees a segment may turn (the entity swings on a 4-block arm: the eye's path stays
#                               within 4 (1 - cos 6) = 0.02 b of the straight line)
CHASE_DUR = 3                 # chase(): the interpolation length of the per-tick placements
BACK = L.CAM_BACK
GRID = L.CAM_GRID
LOW = 1.05                    # an eye lower than this over the stage floor can sit inside dry grass (1 b tall)
FRAMES = ('ST', 'ST2', 'HR', 'W')
CLAMP = 'function rlk:mboss/ar/clampw'
FIX = L.cam('fix')


def ST(r, u, f):
    return ('ST', float(r), float(u), float(f))


def ST2(r, u, f):
    return ('ST2', float(r), float(u), float(f))


def HR(r, u, f):
    return ('HR', float(r), float(u), float(f))


def W(x, y, z):
    return ('W', float(x), float(y), float(z))


def ENT(selector, anchor='eyes'):
    assert anchor in ('eyes', 'feet')
    return ('ENT', selector, anchor)


def num(v):
    return L.num(float(v), 3)


def _xyz(p):
    """An absolute point written so the game takes it as it is (x / z keep a decimal point: api.xyz's rule)."""
    def exact(v):
        s = num(v)
        return s if '.' in s else s + '.0'
    return f'{exact(p[1])} {num(p[2])} {exact(p[3])}'


def _local(p):
    return f'^{num(-p[1])} ^{num(p[2])} ^{num(p[3])}'


def lerp_pt(a, b, u):
    assert a[0] == b[0] and a[0] != 'ENT', (a, b)
    return (a[0],) + tuple(a[i] + (b[i] - a[i]) * u for i in (1, 2, 3))


def ease(kind, u):
    if kind == 'l':
        return u
    assert kind == 'io', kind
    return u * u * (3 - 2 * u)


def quant(deg):
    """A rotation on the grid the client gets (the nearest step, as mboss/cam/grid does it)."""
    return math.floor((deg + GRID / 2) / GRID) * GRID


class Key:
    """One placement: at tick `t` the camera is sent to (eye, look) as they will be at tick `at` (the segment's end);
    dur = the interpolation length that move uses (0 = a snap: the first keyframe of a shot)."""

    def __init__(self, t, at, eye, look, dur, keep=False):
        self.t, self.at, self.eye, self.look, self.dur, self.keep = t, at, eye, look, dur, keep


class Shot:
    def __init__(self, t, cam, eye, look, name, clamp, sub=()):
        self.t, self.cam, self.eye, self.look, self.name, self.clamp = t, cam, eye, look, name, clamp
        self.sub = tuple(sub)     # who the shot is of: 'her' / 'actor' / 'moon' (their heads / the disc must be in frame, unhidden)
        self.moves = []           # (t0, t1, eye0, eye1, look0, look1, ease, kind): kind 'move' | 'track' | 'chase'
        self.keys = []            # the placements after the first keyframe (Key), in tick order
        self.end = None           # the first tick this shot is no longer live

    def at(self, t):
        """(eye, look) points at tick t of the shot (the last move reached stays)."""
        eye, look = self.eye, self.look
        for t0, t1, e0, e1, l0, l1, k, _kind in self.moves:
            if t < t0:
                break
            u = ease(k, min(1.0, (t - t0) / (t1 - t0)))
            eye = lerp_pt(e0, e1, u)
            look = l1 if l0[0] == 'ENT' or l1[0] == 'ENT' else lerp_pt(l0, l1, u)
        return eye, look

    def moving(self, t):
        return any(t0 <= t <= t1 for t0, t1, *_r in self.moves)

    def last_motion(self):
        """The last tick the client still moves this shot's camera (the end of its last segment)."""
        return max([k.at for k in self.keys], default=self.t)


class Track:
    """The camera track of one sequence. anchors: {'ST': selector, 'ST2': selector, 'HR': selector}; t_end: the first tick
    without the lock; her: tick -> (frame 'ST' | 'ST2', r, u, f, yaw) = her body on the stage as the sequence moves it (the
    lead of a segment whose points are in her frame), None: she is taken where she is."""

    def __init__(self, seq, anchors, t_end, clamp=True, lift=None, over=None, her=None, inside=None):
        self.seq, self.anchors, self.t_end, self.clamp, self.lift = seq, dict(anchors), t_end, clamp, lift
        self.over = over            # a function run as the camera after the clamp of a stage eye (the lens off the actor)
        self.inside = inside or CLAMP   # a clamped track: run as the camera ENTITY after mboss/cam/fix (into the disc, off the floor)
        self.her = her
        self.shots = []

    # ---- the table --------------------------------------------------------------------------------------------------
    def cut(self, t, cam, eye, look, name='', sub=(), clamp=None):
        """A hard cut to camera `cam`. sub: what the shot must show (the shot sheets check it): 'her', 'actor', 'moon';
        'actor?' = the actor as foreground of a shot from behind it, which a stage with the wall behind the actor cannot
        give (the clamp, `over`): required only where the eye is not clamped."""
        assert cam in (1, 2) and eye[0] in FRAMES and look[0] in FRAMES + ('ENT',), (self.seq, t, eye, look)
        if self.shots:
            p = self.shots[-1]
            assert t > p.t and p.cam != cam, f'{self.seq} {t}: consecutive shots must alternate the camera'
            assert t - p.t >= PRE, f'{self.seq} {t}: the shot before lasts {t - p.t} t: the idle camera needs {PRE} t to settle'
            assert p.last_motion() < t, f'{self.seq} {t}: a move of the shot before runs into the cut'
            p.end = t
        assert all(x in ('her', 'actor', 'moon', 'actor?') for x in sub), sub
        s = Shot(t, cam, eye, look, name, self.clamp if clamp is None else clamp, sub)
        s.end = self.t_end
        self.shots.append(s)
        return s

    def _span(self, t0, t1):
        s = self.shots[-1]
        assert s.t <= t0 < t1 < s.end, (self.seq, t0, t1, s.t, s.end)
        assert t0 >= max(s.t, 1), (self.seq, t0)
        assert s.last_motion() <= t0, (self.seq, t0, 'overlaps the move before')
        assert not (s.t == 0 and t0 < 2), f'{self.seq}: a move of the first shot starts at tick 2 or later (its duration is set a tick ahead)'
        return s

    def move(self, t0, t1, eye=None, look=None, ease='l'):
        """The live shot moves: eye and / or look go from where they are to the given points over t0..t1, as straight
        constant-speed segments of at most SEG_MAX ticks and TURN_MAX degrees ('io': eased, as a few segments)."""
        s = self._span(t0, t1)
        e0, l0 = s.at(t0)
        e1, l1 = eye or e0, look or l0
        s.moves.append((t0, t1, e0, e1, l0, l1, ease, 'move'))
        n = max(1, math.ceil((t1 - t0) / SEG_MAX), math.ceil(self.turn(e0, l0, t0, e1, l1, t1) / TURN_MAX))
        if ease == 'io':
            n = max(n, min(6, max(3, (t1 - t0) // 3)))
        n = min(n, t1 - t0)
        cuts = [t0 + round((t1 - t0) * i / n) for i in range(n + 1)]
        keep = e0[0] == l0[0] == e1[0] == l1[0] != 'ENT' and self.parallel(e0, l0, e1, l1)   # the view direction stays
        for a, b in zip(cuts, cuts[1:]):
            e, lk = s.at(b)
            s.keys.append(Key(a, b, e, lk, b - a, keep))
        return s

    def track(self, t0, t1, every=20):
        """The live shot follows its points through t0..t1 while she moves (a walk, a turn): a segment every `every` ticks
        to where its eye and look points will be at the segment's end (her frame led by her(t))."""
        s = self._span(t0, t1)
        assert self.her is not None, self.seq
        e0, l0 = s.at(t0)
        s.moves.append((t0, t1, e0, e0, l0, l0, 'l', 'track'))
        n = max(1, math.ceil((t1 - t0) / min(every, SEG_MAX)))
        cuts = [t0 + round((t1 - t0) * i / n) for i in range(n + 1)]
        for a, b in zip(cuts, cuts[1:]):
            s.keys.append(Key(a, b, e0, l0, b - a))
        return s

    def chase(self, t0, t1):
        """The live shot is aimed at its look point again every tick of t0..t1 (a subject that crosses the frame fast), the
        client smoothing the placements over CHASE_DUR ticks."""
        s = self._span(t0, t1)
        e0, l0 = s.at(t0)
        s.moves.append((t0, t1, e0, e0, l0, l0, 'l', 'chase'))
        for t in range(t0, t1):
            s.keys.append(Key(t, t + 1, e0, l0, CHASE_DUR))
        return s

    # ---- her frame at a later tick ------------------------------------------------------------------------------------
    def lead(self, t, at):
        """(dr, du, df, dyaw, frame) her body moves between ticks t and at by her(t) (None: no table, no move, or the move
        crosses stage frames)."""
        if self.her is None or at == t:
            return None
        a, b = self.her(t), self.her(at)
        if a[0] != b[0]:
            return None
        d = tuple(b[i] - a[i] for i in (1, 2, 3)) + ((b[4] - a[4] + 180.0) % 360.0 - 180.0,)
        return None if all(abs(v) < 1e-9 for v in d) else d + (a[0],)

    def nominal(self, p, t):
        """A point in stage coordinates (frame, r, u, f) by her(t) (the build-time estimate of a turn; W / ENT: None)."""
        if p[0] in ('ST', 'ST2'):
            return p
        if p[0] != 'HR' or self.her is None:
            return None
        fr, r, u, f, yaw = self.her(t)
        a = math.radians(yaw)
        return (fr, r + p[1] * math.cos(a) + p[3] * math.sin(a), u + p[2], f + p[3] * math.cos(a) - p[1] * math.sin(a))

    def turn(self, e0, l0, t0, e1, l1, t1):
        """Degrees the view direction turns between two keyframes (0 when it cannot be told at build time)."""
        pts = [self.nominal(p, t) for p, t in ((e0, t0), (l0, t0), (e1, t1), (l1, t1))]
        if any(p is None for p in pts) or len({p[0] for p in pts}) != 1:
            return 0.0
        d0, d1 = (tuple(b[i] - a[i] for i in (1, 2, 3)) for a, b in ((pts[0], pts[1]), (pts[2], pts[3])))
        n0, n1 = math.sqrt(sum(v * v for v in d0)), math.sqrt(sum(v * v for v in d1))
        if n0 < 1e-6 or n1 < 1e-6:
            return 0.0
        return math.degrees(math.acos(max(-1.0, min(1.0, sum(a * b for a, b in zip(d0, d1)) / (n0 * n1)))))

    @staticmethod
    def parallel(e0, l0, e1, l1):
        """Both keyframes look along the same direction (a push-in, a pull-back, a side track): the rotation of the first
        is kept, so the grid rounding of two nearly equal directions cannot differ by a step."""
        d0 = [l0[i] - e0[i] for i in (1, 2, 3)]
        d1 = [l1[i] - e1[i] for i in (1, 2, 3)]
        n0, n1 = math.sqrt(sum(v * v for v in d0)), math.sqrt(sum(v * v for v in d1))
        return n0 > 1e-6 and n1 > 1e-6 and sum(a * b for a, b in zip(d0, d1)) / (n0 * n1) > 1 - 1e-7

    # ---- the lines --------------------------------------------------------------------------------------------------
    def _at(self, frame, lead=None):
        if frame != 'HR':
            return f'at {self.anchors[frame]}'
        if lead is None:
            return f'at {self.anchors["HR"]} rotated ~ 0'
        dr, du, df, dyaw, fr = lead
        mv = f' rotated as {self.anchors[fr]} positioned ^{num(-dr)} ^{num(du)} ^{num(df)}' if any(abs(v) > 1e-9 for v in (dr, du, df)) else ''
        return f'at {self.anchors["HR"]}{mv} rotated as {self.anchors["HR"]} rotated ~{num(dyaw) if abs(dyaw) > 1e-9 else ""} 0'

    def _sel(self, cam):
        return L.cam_sel(cam)

    def place(self, cam, eye, sel=None, lead=None):
        sel = sel or self._sel(cam)
        if eye[0] == 'W':
            return f'tp {sel} {_xyz(eye)}'
        return f'execute {self._at(eye[0], lead)} run tp {sel} {_local(eye)}'

    def aim(self, cam, look, sel=None, lead=None):
        sel = sel or self._sel(cam)
        if look[0] == 'W':
            return f'rotate {sel} facing {_xyz(look)}'
        if look[0] == 'ENT':
            return f'rotate {sel} facing entity {look[1]} {look[2]}'
        return f'execute {self._at(look[0], lead)} run rotate {sel} facing {_local(look)}'

    def place_aim(self, cam, eye, look, clamp, sel=None, lead=None, keep=False):
        """The lines that put camera `cam` (or the entity `sel`) AT the viewpoint `eye` looking at `look` (one command when
        both are in one frame and unclamped). keep: the rotation stays as it is (a move along the view axis)."""
        sel = sel or self._sel(cam)
        if keep:
            return [self.place(cam, eye, sel, lead)] + ([f'execute as {sel} run {CLAMP}'] if clamp else [])
        if not clamp and eye[0] == look[0]:
            if eye[0] == 'W':
                return [f'tp {sel} {_xyz(eye)} facing {_xyz(look)}']
            return [f'execute {self._at(eye[0], lead)} run tp {sel} {_local(eye)} facing {_local(look)}']
        staged = clamp and eye[0] in ('ST', 'ST2')
        out = [self.place(cam, eye, sel, lead)] + ([f'execute as {sel} run {CLAMP}'] if clamp else [])
        out += ([f'execute as {sel} run {self.over}'] if staged and self.over else []) + [self.aim(cam, look, sel, lead)]
        if staged and self.lift and eye[2] < LOW:
            out += [f'execute as {sel} run {self.lift}', self.aim(cam, look, sel, lead)]
        return out

    def put(self, cam, eye, look, clamp, lead=None, keep=False):
        """A whole placement of a camera: at the viewpoint, aimed, then mboss/cam/fix (the grid, 4 blocks forward) and, on
        a clamped track, the entity pulled into the walk disc too."""
        sel = self._sel(cam)
        return [*self.place_aim(cam, eye, look, clamp, lead=lead, keep=keep), f'execute as {sel} run {FIX}',
                *([f'execute as {sel} run {self.inside}'] if clamp else [])]

    def spawn(self, helper, summon, cams=(1, 2), first=None):
        """The lines that make the cameras where their first shots put them: per camera a one-tick helper (`summon` makes
        it, `helper` selects it) is placed and aimed as that shot's viewpoint (clamp, over, lift as the shot has them), the
        camera is made from it with mboss/cam/spawn_at (the rotation on the grid in the summon NBT, 4 blocks forward) and
        the helper goes. `first`: {cam: shot} to use instead of each camera's first shot of this track."""
        out = []
        for cam in cams:
            s = (first or {}).get(cam) or next((x for x in self.shots if x.cam == cam), None)
            if s is None:
                continue
            out += [summon, *self.place_aim(cam, s.eye, s.look, s.clamp, sel=helper),
                    f'execute at {helper} rotated as {helper} run {L.cam("spawn_at", id=cam)}', f'kill {helper}',
                    *([f'execute as {self._sel(cam)} run {self.inside}'] if s.clamp else [])]
        return out

    def lines(self):
        """{tick: [lines]}: before each cut the idle camera's preparation, at the cut the live id, per segment its duration a
        tick ahead and its placement. Tick 0's shot has no preparation: its camera is made at its place in the sequence's
        start (spawn())."""
        out = {}

        def add(t, *ls):
            out.setdefault(t, []).extend(ls)
        for i, s in enumerate(self.shots):
            if s.t > 0:
                assert s.t - PRE >= (self.shots[i - 1].t if i else 0), (self.seq, s.t)
                add(s.t - 3, L.cam('spawn'), L.cam_dur(s.cam, 0))      # a camera that was killed is back for this cut (idempotent)
                add(s.t - 2, *self.put(s.cam, s.eye, s.look, s.clamp))
            add(s.t, f'scoreboard players set {L.CAM_ID[0]} {L.CAM_ID[1]} {s.cam}')
            dur = 0
            for k in s.keys:
                if k.dur != dur:
                    assert k.t - 1 >= max(s.t - 1, 0), (self.seq, s.name, k.t)
                    add(k.t - 1, L.cam_dur(s.cam, k.dur))
                    dur = k.dur
                add(k.t, *self.put(s.cam, k.eye, k.look, s.clamp, lead=self.lead(k.t, k.at), keep=k.keep))
        return {t: [x for x in ls if x] for t, ls in sorted(out.items())}

    # ---- queries (tests, the shot sheets) -----------------------------------------------------------------------------
    def shot_at(self, t):
        for s in reversed(self.shots):
            if s.t <= t:
                return s
        return None

    def cuts(self):
        return [(s.t, s.cam, s.name) for s in self.shots]

    def segments(self):
        """[(shot name, cam, t, at, dur, keep)] of every placement after a shot's first keyframe."""
        return [(s.name, s.cam, k.t, k.at, k.dur, k.keep) for s in self.shots for k in s.keys]

    def table(self):
        """[(t, end, cam, name, eye, look, [(t0, t1, eye1, look1, ease, kind)])] of the track (the design's shot table)."""
        return [(s.t, s.end, s.cam, s.name, s.eye, s.look, [(m[0], m[1], m[3], m[5], m[6], m[7]) for m in s.moves]) for s in self.shots]


# ---- geometry for the tests and the shot sheets (the same frames in Python) -------------------------------------------------
def basis(yaw):
    """(forward, left) unit vectors (x, z) of a Minecraft yaw (0 = +z, 90 = -x)."""
    a = math.radians(yaw)
    return (-math.sin(a), math.cos(a)), (math.cos(a), math.sin(a))


def forward(yaw, pitch):
    """The unit view vector of a Minecraft rotation."""
    y, p = math.radians(yaw), math.radians(pitch)
    return (-math.sin(y) * math.cos(p), -math.sin(p), math.cos(y) * math.cos(p))


def viewpoint(pos, rot, back=BACK):
    """Where the client looks from when it spectates a non-living entity at pos / rot in F5: `back` blocks behind it."""
    f = forward(rot[0], rot[1])
    return tuple(pos[i] - back * f[i] for i in range(3))


def to_world(p, frames):
    """A point in world coordinates. frames: {'ST' | 'ST2' | 'HR': ((x, y, z), yaw)}, 'ENT': {selector: (x, y, z) of the anchor}."""
    if p[0] == 'W':
        return (p[1], p[2], p[3])
    if p[0] == 'ENT':
        return tuple(frames['ENT'][p[1]])
    (ox, oy, oz), yaw = frames[p[0]]
    f, lf = basis(yaw)
    r, u, fw = p[1], p[2], p[3]
    return (ox - r * lf[0] + fw * f[0], oy + u, oz - r * lf[1] + fw * f[1])


def yaw_pitch(eye, look):
    dx, dy, dz = (look[i] - eye[i] for i in range(3))
    return math.degrees(math.atan2(-dx, dz)), math.degrees(-math.atan2(dy, math.hypot(dx, dz)))
