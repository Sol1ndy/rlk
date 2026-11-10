"""The camera tracks of 홍련's locked sequences (hr_design.md §3.0 / §5.2; owner lane H2). Pure data + line builders: no
files are written here; seq.py merges a track's lines into its sequence's timeline (seq/<name>/k/<t>).

The mechanism (FN-cam of the framework, tools/build_mboss_core.py; facts checked against the 26.3 server jar): the module
sets `#mbCam mb 1` every tick of a locked sequence and `#mbCamId mb` 1 (camera A = rlk_mb_cam1) or 2 (B = rlk_mb_cam2);
rlk:tick spectates the live stand. A stand is a marker armour stand: its position IS the eye point (mboss_lib.CAM_EYE 0).
- A hard cut = the other stand made live. The client glides an entity to a new place over 3 ticks, so the idle stand is
  put at the next shot's eye PRE ticks before the cut (each of those ticks, so a frame that still settles is followed)
  and is in place when it goes live. Consecutive shots therefore alternate A / B (asserted).
- A move = one tp per tick on the live stand (the client's own interpolation makes it smooth).
- Rotation reaches the client in 1.4-degree steps (the entity move packets pack it into a byte), interpolated over 3
  ticks: a pan slower than about 0.4 deg / tick shows single nudges (slow_pans() lists them for the in-game check).

Points: ST(r, u, f) / ST2(r, u, f) in the stage frames (r to the actor's right, u up, f forward; the markers rlk_hr_stage /
rlk_hr_stage2, pitch 0), HR(r, u, f) at her body (f along her facing, r her right), W(x, y, z) world, ENT(selector, anchor)
an entity (a look point only). An eye point is taken when the shot is placed (and during its moves); a look point in HR /
ENT is aimed at again every tick (she walks, leaps, is thrown), ST / ST2 / W looks are fixed.
`clamp`: the eye is pulled into the walk disc of the arena after it is placed (mboss/ar/clampw, 24.3 b from the axis) and
aimed again - a stage near the wall never puts the lens into the bamboo. Shots of a fixed stage (CS0) are checked
offline instead (test_seq) and skip it.
`lift`: a clamped track's low eye (below LOW over the stage floor) is not left inside a plant of the field: after it is
placed and aimed the track's lift function (the module's, @s = the stand) may raise it, and it is aimed again.
`over`: with the actor's back at the wall the clamp brings an eye meant to be behind the actor onto it: after the clamp of
a stage eye the track's over function (the module's, @s = the stand) may put the lens over the actor's head instead.
"""
import math

import mboss_lib as L

PRE = 4                       # ticks the idle stand is placed before its cut (>= the client's 3 interpolation steps)
SLOW_PAN = 0.4                # deg / tick: below it a rotation shows as single 1.4-degree nudges
LOW = 1.05                    # an eye lower than this over the stage floor can sit inside dry grass (1 b tall)
FRAMES = ('ST', 'ST2', 'HR', 'W')
CLAMP = 'function rlk:mboss/ar/clampw'


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


class Shot:
    def __init__(self, t, cam, eye, look, name, clamp, sub=()):
        self.t, self.cam, self.eye, self.look, self.name, self.clamp = t, cam, eye, look, name, clamp
        self.sub = tuple(sub)     # who the shot is of: 'her' / 'actor' / 'moon' (their heads / the disc must be in frame, unhidden)
        self.moves = []           # (t0, t1, eye0, eye1, look0, look1, ease)
        self.end = None           # the first tick this shot is no longer live

    def at(self, t):
        """(eye, look) points at tick t of the shot (the last move reached stays)."""
        eye, look = self.eye, self.look
        for t0, t1, e0, e1, l0, l1, k in self.moves:
            if t < t0:
                break
            u = ease(k, min(1.0, (t - t0) / (t1 - t0)))
            eye = lerp_pt(e0, e1, u)
            look = l1 if l0[0] == 'ENT' or l1[0] == 'ENT' else lerp_pt(l0, l1, u)
        return eye, look

    def moving(self, t):
        return any(t0 <= t <= t1 for t0, t1, *_r in self.moves)


class Track:
    """The camera track of one sequence. anchors: {'ST': selector, 'ST2': selector, 'HR': selector}; cams: {1: selector,
    2: selector} (mboss_lib.cam_sel); t_end: the first tick without the lock."""

    def __init__(self, seq, anchors, t_end, clamp=True, lift=None, over=None):
        self.seq, self.anchors, self.t_end, self.clamp, self.lift = seq, dict(anchors), t_end, clamp, lift
        self.over = over            # a function run as the stand after the clamp of a stage eye (the lens off the actor)
        self.shots = []

    # ---- the table --------------------------------------------------------------------------------------------------
    def cut(self, t, cam, eye, look, name='', sub=(), clamp=None):
        assert cam in (1, 2) and eye[0] in FRAMES and look[0] in FRAMES + ('ENT',), (self.seq, t, eye, look)
        if self.shots:
            p = self.shots[-1]
            assert t > p.t and p.cam != cam, f'{self.seq} {t}: consecutive shots must alternate the camera (a cut on one stand glides)'
            assert not p.moves or p.moves[-1][1] < t, f'{self.seq} {t}: a move of the shot before runs past the cut'
            p.end = t
        assert all(x in ('her', 'actor', 'moon') for x in sub), sub
        s = Shot(t, cam, eye, look, name, self.clamp if clamp is None else clamp, sub)
        s.end = self.t_end
        self.shots.append(s)
        return s

    def move(self, t0, t1, eye=None, look=None, ease='l'):
        """The live shot moves: eye and / or look go from where they are to the given points over t0..t1."""
        s = self.shots[-1]
        assert s.t <= t0 < t1 < s.end, (self.seq, t0, t1, s.t, s.end)
        assert not s.moves or s.moves[-1][1] <= t0, (self.seq, t0)
        e0, l0 = s.at(t0)
        s.moves.append((t0, t1, e0, eye or e0, l0, look or l0, ease))
        return s

    # ---- the lines --------------------------------------------------------------------------------------------------
    def _at(self, frame):
        return f'at {self.anchors[frame]}' + (' rotated ~ 0' if frame == 'HR' else '')

    def _sel(self, cam):
        return L.cam_sel(cam)

    def place(self, cam, eye):
        sel = self._sel(cam)
        if eye[0] == 'W':
            return f'tp {sel} {_xyz(eye)}'
        return f'execute {self._at(eye[0])} run tp {sel} {_local(eye)}'

    def aim(self, cam, look):
        sel = self._sel(cam)
        if look[0] == 'W':
            return f'rotate {sel} facing {_xyz(look)}'
        if look[0] == 'ENT':
            return f'rotate {sel} facing entity {look[1]} {look[2]}'
        return f'execute {self._at(look[0])} run rotate {sel} facing {_local(look)}'

    def place_aim(self, cam, eye, look, clamp):
        """The lines that put stand `cam` at `eye` looking at `look` (one command when both are in one frame and unclamped)."""
        sel = self._sel(cam)
        if not clamp and eye[0] == look[0]:
            if eye[0] == 'W':
                return [f'tp {sel} {_xyz(eye)} facing {_xyz(look)}']
            return [f'execute {self._at(eye[0])} run tp {sel} {_local(eye)} facing {_local(look)}']
        staged = clamp and eye[0] in ('ST', 'ST2')
        out = [self.place(cam, eye)] + ([f'execute as {sel} run {CLAMP}'] if clamp else [])
        out += ([f'execute as {sel} run {self.over}'] if staged and self.over else []) + [self.aim(cam, look)]
        if staged and self.lift and eye[2] < LOW:
            out += [f'execute as {sel} run {self.lift}', self.aim(cam, look)]
        return out

    def lines(self):
        """{tick: [lines]}: the placements before each cut, the cut (the live id), the moves, the per-tick aim of a moving
        look point. Tick 0's shot has no placement ticks: the stands are made in its tick (a new entity does not glide)."""
        out = {}

        def add(t, *ls):
            out.setdefault(t, []).extend(ls)
        for i, s in enumerate(self.shots):
            lo = max(s.t - PRE, self.shots[i - 1].t + 1 if i else 0, 0)
            for t in range(lo, s.t):
                if t == lo:
                    add(t, L.cam('spawn'))                 # a stand that was killed is back for this cut (idempotent)
                add(t, *self.place_aim(s.cam, s.eye, s.look, s.clamp))
            add(s.t, f'scoreboard players set {L.CAM_ID[0]} {L.CAM_ID[1]} {s.cam}', *self.place_aim(s.cam, s.eye, s.look, s.clamp))
            for t in range(s.t + 1, s.end):
                eye, look = s.at(t)
                if s.moving(t):
                    add(t, *self.place_aim(s.cam, eye, look, s.clamp))
                elif look[0] in ('HR', 'ENT'):
                    add(t, self.aim(s.cam, look))
        return {t: [x for x in ls if x] for t, ls in out.items()}

    # ---- queries (tests, the shot sheets) -----------------------------------------------------------------------------
    def shot_at(self, t):
        for s in reversed(self.shots):
            if s.t <= t:
                return s
        return None

    def cuts(self):
        return [(s.t, s.cam, s.name) for s in self.shots]

    def table(self):
        """[(t, end, cam, name, eye, look, [(t0, t1, eye1, look1, ease)])] of the track (the design's shot table)."""
        return [(s.t, s.end, s.cam, s.name, s.eye, s.look, [(m[0], m[1], m[3], m[5], m[6]) for m in s.moves]) for s in self.shots]


# ---- geometry for the tests and the shot sheets (the same frames in Python) -------------------------------------------------
def basis(yaw):
    """(forward, left) unit vectors (x, z) of a Minecraft yaw (0 = +z, 90 = -x)."""
    a = math.radians(yaw)
    return (-math.sin(a), math.cos(a)), (math.cos(a), math.sin(a))


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


def slow_pans(track, frames_at):
    """[(seq, shot name, t0, t1, degrees per tick)] of the moves whose view direction turns slower than SLOW_PAN (and at
    all): the in-game check list for the 1.4-degree rotation steps. frames_at(t) -> the frames dict of to_world."""
    out = []
    for s in track.shots:
        for t0, t1, *_r in s.moves:
            fr0, fr1 = frames_at(t0), frames_at(t1)
            e0, l0 = s.at(t0)
            e1, l1 = s.at(t1)
            a = yaw_pitch(to_world(e0, fr0), to_world(l0, fr0))
            b = yaw_pitch(to_world(e1, fr1), to_world(l1, fr1))
            d = math.hypot((b[0] - a[0] + 180) % 360 - 180, b[1] - a[1])
            rate = d / (t1 - t0)
            if 0.02 < rate < SLOW_PAN:
                out.append((track.seq, s.name, t0, t1, round(rate, 3), round(d, 2)))
    return out
