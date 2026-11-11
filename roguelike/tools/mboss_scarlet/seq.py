"""Sequences of 홍련 (Scarlet) on the new combat: CS0 `intro` (+ the skip), CS1 `cs1` (+ the skip), the lead-ins `lead60` /
`lead5` / `lead_re {g}`, the repel counter `repel {at}`, the `ending` and the event coda `event` (tools/dev/plan/combat/
hr_design.md §3, §8; owner lane H2). The camera tables live here too (tools/mboss_scarlet/cam.py builds their lines).

CONTRACT = 2 below is the marker tools/build_mboss_scarlet.py looks for (api.SEQ_CONTRACT): this file implements api.SEQS.

Contract (api.Service): SERVICES = one api.Service per api.SEQS name; build(W) writes only under seq/ (W =
api.Writer('S2b', api.OWN['S2b'])): the entry points seq/<name>/{start,tick,cancel} (+ seq/<name>/skip of api.SEQ_EXTRA) and
their internal files: k/<t> | k/<a>_<b> (the lines of a tick or of a run of equal ticks), kb/<a>_<b> (dispatch), m/<key> (body
moves, the stage, turns), and for a locked sequence lock / unlock / fin / cam (+ c/, cb/: the camera lines); seq/lib/ shared. The core sets #sq hr 0 and calls start
(@s = the body, at it), then adds 1 to #sq and calls tick every tick; rig/tick runs after the module logic, so her clip
shows tick e when #sq = e. A sequence sets #sqdone hr 1 at its length (api.SEQ_LEN). cancel has no executor, is idempotent
and removes only what the sequence made.

Division of work (unchanged): the core owns invulnerability, cine, the bars, the gauge, floors, the phase switch, the HP
steps, the kill, the death finish and the skip input; a sequence signals it through #sq_sig hr = api.SIG in the beat's tick
(repel hp1 / hp2 / hp3 at api.COUNTER_EV, lead5 / lead_re refill) and never calls core functions. A sequence owns its
clips, rig looks / anchors / her yaw, the kit's effects, props, sounds, lines, overlays, the look requests, the music line
of its music event, the title, her body moves, and (new) the stage, the camera and the lock request, the actor calls.

The lock (hr_design §3.0, the framework's FN-cam): a locked sequence calls its seq/<name>/lock every tick of its lock span:
the request `#mbCam mb 1` (api.cam_req), the actor's clock and tick (api.actor*, '' until lane H3's manifest exists), the
camera lines of the tick. The framework holds the player in spectator mode on the live camera stand and releases them the
tick the request stops. If the player was released while the sequence held them (#sq_h hr 1 = this run has seen the hold; a
pause: death, Ronova's revive, a menu; /reload; a relog; a killed stand), or the hold never came by tick 3, `lock` calls
`unlock`: #sq_cx hr 1 = no lock for the rest of this run (the stands and the actor go, the avatar shows, the sequence plays
on unlocked with its timing and its signals, as the 11-06 cutscenes did). The core ends a paused / reloaded sequence itself
(§3.6): `cancel` (the request taken back, the stands, the stage, the actor, the kit's line / overlay and the HUD hold gone
in that tick) + its own end state. The lethal repel hands its actor to the ending (#sq_keep hr; lane H3's clips meet).

The stage (rlk_hr_stage, a marker made at tick 0): origin = the avatar's feet on the floor, forward = the bearing avatar
-> her, unless ST(0, 0, FMAX) fails mboss/mv/ok, then avatar -> the arena centre (nearer than 0.6 b to her: the avatar's
own facing first). CS0's stage is fixed (api.CS0_P0, toward her seat) and the avatar is moved there at its tick 0, the one
avatar teleport. ST(r, u, f): r to the actor's right, u up, f forward. The ending adds ST2 (rlk_hr_stage2) from her
landing mark on. Every staged point of hers is checked with seq/lib/ok (the arena floor inside the barrier ring with free
feet and head; mv/ok's safe disc would refuse a contact point next to a player who stands near the wall) or mv/ok itself
where the design names it (the stage's forward, her CS1 mark, the ending's landing mark).

World entities a sequence makes: the stage markers, a one-tick helper marker, the kit prop cards (petals: rlk_hr_sqp), the
event's thrown sword / moonlight orb, the cameras and their texts (the framework's, mboss/cam/spawn_at), all tagged rlk_room
rlk_mb_aux.

Round V (lane VC, tools/dev/plan/combat/v_brief.md §3 "VC"; the facts in review/v/client_facts.md and vc_progress.md):
- the camera: empty item_displays seen from 4 blocks behind (F5), keyframes the client interpolates, every rotation on the
  360 / 256 grid, cuts between settled cameras (cam.py);
- her lines in a locked sequence are drawn on the camera's text_display (lower third, dark backdrop; say()); the kit's
  subtitle line only when no camera holds the player (the developer mode, a run that lost its lock);
- the skip is the jump key held SKIP_HOLD ticks (seq/<name>/skipin; Shift ends a spectate inside the game and stays
  free), its prompt the camera's hint text; the core's own Shift input (core/skip) rests while #skip hr is -1;
- an instant move of her body is followed by RIG_NOW: the rig's follow runs in the tick's stale execution position, so
  without it her model stays where the body was until the body moves again (the 11-11 test: the CS0 skip showed an empty
  mark and she popped in when the fight began).
"""
import json
import math

from . import api
from . import cam as C

CONTRACT = 2

L, K = api.L, api.K
OBJ, NS = api.OBJ, api.NS
CY = api.CY
SEQ = f'{NS}seq'
BODY = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'            # the framework body (mboss/body)
PLB = '@e[tag=rlk_body,limit=1]'                                     # the player's body (the avatar; the player in developer mode)
PL = '@a[tag=player,limit=1]'
STAGE_T = api.TAGS['stage']
STAGE2_T = STAGE_T + '2'
STAGE = f'@e[type=minecraft:marker,tag={STAGE_T},limit=1]'
STAGE2 = f'@e[type=minecraft:marker,tag={STAGE2_T},limit=1]'
ANCHOR = f'@e[type=minecraft:marker,tag={api.TAGS["anchor"]},limit=1]'
ARENA = '@e[tag=rlk_mb_arena,limit=1]'
EV_T = api.TAGS['ev']
PROP_T = 'rlk_hr_sqp'                                                # the kit prop cards a sequence makes (the petals)
HELP_T = 'rlk_hr_sqh'                                                # a one-tick helper marker (killed in the same function)
HELP = f'@e[type=minecraft:marker,tag={HELP_T},limit=1]'
OK = 'function rlk:mboss/mv/ok'                                      # the safe disc (22.5 b) with free feet and head
OKW = f'function {SEQ}/lib/ok'                                       # the arena floor inside the barrier ring, free feet and head
OKW_R = 26.5
LIFT = f'function {SEQ}/lib/lift'                                    # a low camera eye out of the field's plants (cam.Track lift)
PLANTS = ('minecraft:short_dry_grass', 'minecraft:tall_dry_grass', 'minecraft:crimson_roots')
LIFT_TO, LIFT_AHEAD = 1.15, 0.9
OVER = f'function {SEQ}/lib/over'                                    # a clamped stage eye off the actor (cam.Track over)
OVER_R, OVER_TO = 1.0, 2.5                                           # nearer than OVER_R to the stage origin -> OVER_TO over the floor
CAMIN = f'function {SEQ}/lib/camin'                                  # a camera ENTITY of a clamped track (cam.Track inside)
CAMIN_MIN = 0.3                                                      # ... at least this far over the floor
DIST = 'function rlk:mboss/mv/dist'                                  # -> #mbDist mb (tenths, horizontal, @s -> the player's body)
HOLD_TAG = L.CAM_HOLD_TAG
CAM = {1: L.cam_sel(1), 2: L.cam_sel(2)}
# her model after an instant move of the body (tp): the rig's parts are put at the body NOW (rig/follow_now resets the
# follow's cache; rig/tick's own follow later in the tick runs in the stale execution position of the hook)
RIG_NOW = f'execute at @s rotated as @s rotated ~ 0 run {api.rig("follow_now")}'
SKIP_FP, SKIP_STEP_FP, SKIP_DONE_FP, SKIP_NOW_FP = '#sq_sk', '#sq_sks', '#sq_skd', '#sq_skn'   # the skip input (skipin)
SKIP_KEY_HINT = ' · Space 길게'                                       # the pack's control hint after api.SKIP_TEXT
SKIP_COLS = ('#A8A8B0', '#BEBEC5', '#D3D3D9', '#E9E9EC', '#FFFFFF')   # the prompt brightening in api.SKIP_STEPS steps
LINE_GAP = 2                                                         # ticks per typing step (two syllables per step)
TYPE_SND = 'execute as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0'
CX_FP = '#sq_cx'                                                     # 1: this run of a locked sequence lost its lock
HELD_FP = '#sq_h'                                                    # 1: this run of a locked sequence has seen the player held
GRANT_BY = 3                                                         # a run never held by this tick gives the lock up
KEEP_FP = '#sq_keep'                                                 # 1: the repel's actor is handed to the ending (the lethal kick)
ACTOR_ROOT = '@e[type=minecraft:marker,tag=rlk_cine_root,limit=1]'    # lane H3's actor (its manifest's tags.root)
RIG_T = f'{api.RIG_OBJ_PREFIX}T'                                     # the rig's clip tick (S2a's objective, tools/scarlet_rig_api.md)
A, B = 1, 2                                                          # camera A = rlk_mb_cam1, B = rlk_mb_cam2
ST, ST2, HR, WP, ENT = C.ST, C.ST2, C.HR, C.W, C.ENT
MOON = WP(*api.MOON_POS)
# lock spans [t0, t1) on the sequence clock (hr_design §3.0): the request runs on t0 .. t1 - 1; the coda's black (CODA_BLACK)
# is opaque from E116, so its hand-back at E118 happens under it (HF-B, HB-05)
LOCK = {'intro': (0, api.SEQ_LEN['intro']), 'cs1': (0, api.SEQ_LEN['cs1']), 'repel': (0, api.SEQ_LEN['repel']),
        'ending': (0, api.SEQ_LEN['ending'] + 1), 'event': (0, 118)}
TRACKS = {}                                                          # name -> cam.Track (filled by the builders; tests read it)
STAGED = {}                                                          # name -> [(tick, 'ST' | 'ST2', f, note)]: her marks on the axis


def num(v):
    return L.num(v, 3)


def tags(*extra):
    return '[' + ','.join(f'"{t}"' for t in ('rlk_room', 'rlk_mb_aux') + extra) + ']'


def sq(t):
    return f'execute if score #sq {OBJ} matches {t}'


def ev(clip, e, d=0):
    """The played tick of a clip event (+ an offset for a tick that is not a contract event)."""
    return api.ev(clip, e) + d


def sset(k, v):
    return f'scoreboard players set {k} {OBJ} {v}'


class Seq:
    """One sequence's timeline: tick -> lines (tick 0 = start, after its own head lines)."""

    def __init__(self, name):
        self.name, self.t = name, {}

    def at(self, t, *cmds):
        assert isinstance(t, int) and t >= 0, (self.name, t)
        for c in cmds:
            if isinstance(c, (list, tuple)):
                self.at(t, *c)
            elif c:
                self.t.setdefault(t, []).append(c)
        return self

    def fx(self, t, anchor, cmd):
        """A kit line at a rig anchor of the shown clip tick (rig/anchor/<a> moves the one rlk_hr_anchor marker)."""
        if cmd:
            self.at(t, api.rig(f'anchor/{anchor}'), f'execute at {ANCHOR} run {cmd}')
        return self

    def me(self, t, cmd, y=1.1):
        """A line at her (chest height), rotated as her."""
        if cmd:
            self.at(t, f'execute positioned ~ ~{num(y)} ~ rotated as @s rotated ~ 0 run {cmd}')
        return self

    def st(self, t, pt, cmd, frame=None):
        """A line at a stage point ST(r, u, f) (or ST2), rotated as the stage."""
        if cmd:
            self.at(t, f'execute {at_pt(pt)} run {cmd}')
        return self


def at_pt(pt):
    """The execute chain of a point: ST / ST2 at the stage marker (its yaw, pitch 0), HR at her body, W absolute."""
    if pt[0] == 'W':
        return f'positioned {C._xyz(pt)}'
    anchor = {'ST': STAGE, 'ST2': STAGE2, 'HR': BODY}[pt[0]]
    return f'at {anchor}' + (' rotated ~ 0' if pt[0] == 'HR' else '') + f' positioned {C._local(pt)}'


def floor_pt(f, r=0.0, frame='ST'):
    """A floor point of the stage axis (r to the side) as an execute chain."""
    return at_pt((frame, float(r), 0.0, float(f)))


# The cutscenes the footage plays without the HUD hold the player's actionbar HUD on every tick (hudHold 2; player/hud/tick
# rests while it is >= 1); every locked sequence does (the spectator has no hotbar to go with it, hr_design §3.0), and each
# blanks the last actionbar once at its start (the hold only stops new sends).
HUD_OFF = ('intro', 'cs1', 'repel', 'ending', 'event')
HUD_HOLD = 'scoreboard players set @a[tag=player] hudHold 2'
HUD_BLANK = 'title @a[tag=player] actionbar ""'
HUD_FREE = 'scoreboard players set @a[tag=player] hudHold 0'          # a cancel: the HUD is back at once
NO_LEASH = ('cs1', 'repel')        # fight-state sequences with contact marks next to the avatar: the arena leash rests


# ---- her body on the stage as the sequences move it (the same table as tools/scarlet_cine.mjs ROOTS, which her clips are
# choreographed to; test_seq compares it with her_tracks.json): [t0, t1, from, to, apex, yaw0, yaw1, frame], a row holds its
# end until the next one starts; yaw 0 faces +f, 180 faces the actor. cam.Track leads a segment's points in her frame by it.
def _row(t0, t1, a, b=None, h=0.0, y0=180.0, y1=None, fr='ST'):
    return (t0, t1, tuple(map(float, a)), tuple(map(float, b or a)), float(h), float(y0), float(y0 if y1 is None else y1), fr)


THROW_H = 6                                 # (HF-B) the throw's root apex, tenths (= tools/scarlet_cine.mjs THROW_H)
_SF = round(math.dist(api.CS0_P0[::2], api.SEAT_POS[::2]), 2)
HER = {
    'intro': [_row(0, 840, (0, 0, _SF), y0=0), _row(840, 880, (0, 0, _SF), y0=0, y1=180), _row(880, 1052, (0, 0, _SF)),
              _row(1052, 1148, (0, 0, _SF), (0, 0, 13.5)), _row(1234, 1258, (0, 0, 13.5), (0, 0, 6.5), 4.5), _row(1258, 1440, (0, 0, 6.5))],
    'cs1': [_row(0, 6, (0, 0, 9)), _row(6, 10, (0, 0, 9), (0, 0, 1.5)), _row(34, 50, (0, 0, 1.5), (0, 0, 9), 1.2), _row(50, 720, (0, 0, 9))],
    'repel': [_row(0, 6, (0, 1, 1), (0, 0, 1.3)), _row(30, 36, (0, 0, 1.3), (0, 0, 1.1)), _row(56, 64, (0, 0, 1.1), (0, 0, 1.2)),
              _row(78, 101, (0, 0, 1.2), (0, 0, 3), THROW_H / 10), _row(129, 135, (0, 0, 3), (0, 0, 8)), _row(135, 140, (0, 0, 8), (0, 0, 9))],
    'ending': [_row(0, 6, (0, 0, 4.2)), _row(6, 22, (0, 0, 4.2), (0, 0, 4.6)), _row(50, 54, (0, 0, 4.6), (0, 0, 2.9)),
               _row(80, 86, (0, 0, 2.9), (0, 0, 6)), _row(116, 136, (0, 0, 6), (0, 0, 11), 1.2), _row(150, 188, (0, 0, 11), (0, 0, 4)),
               _row(204, 216, (0, 0, 4), (0, 6, 3.6)), _row(222, 228, (0, 6, 3.6), (0, 6, 3.2)), _row(250, 262, (0, 6, 3.2), (0, 6.4, 3.4)),
               _row(276, 286, (0, 6.4, 3.4), (0, 6, 3.3)), _row(314, 334, (0, 6, 3.3), (0, 0, 9), 4),
               _row(334, 650, (0, 0, 9), fr='ST2'), _row(650, 700, (0, 0, 9), y0=180, y1=360, fr='ST2'),
               _row(700, 1072, (0, 0, 9), y0=0, fr='ST2'), _row(1072, 1094, (0, 0, 9), y0=0, y1=180, fr='ST2'),
               _row(1094, 1154, (0, 0, 9), (0, 0, 4.5), fr='ST2'), _row(1154, 1500, (0, 0, 4.5), fr='ST2')],
    'event': [_row(0, 200, (0, 0, 4.5), fr='ST2')],
}


def her_of(name):
    """tick -> (frame, r, u, f, yaw): her body on the stage at a tick of sequence `name` (HER)."""
    rows = HER[name]

    def at(t):
        r = rows[0]
        for x in rows:
            if t >= x[0]:
                r = x
        u = max(0.0, min(1.0, (t - r[0]) / max(1, r[1] - r[0])))
        p = [a + (b - a) * u for a, b in zip(r[2], r[3])]
        p[1] += 4 * r[4] * u * (1 - u)
        return (r[7], p[0], p[1], p[2], r[5] + (r[6] - r[5]) * u)
    return at


# ---- her lines in a locked sequence: on the camera's text (mboss_lib.cam_line): typed two syllables per LINE_GAP ticks with
# the kit's own typing sound, held for api.LINE_AT's ticks on screen, a line of api.LINE_PAGES as consecutive pages (the hold
# split by their lengths). The text is in the world, 0.3 b before the lens: a full-screen overlay (a title) covers it, so
# nothing is ever typed over the black of a skip. Without a held player (the developer mode, a run that lost its lock)
# there is no camera text: the kit's subtitle line plays instead.
def line_steps(lid, hold):
    """[(dt, text | None)]: the camera-text steps of line `lid` on its own clock (None = cleared at its end)."""
    pages = api.LINE_PAGES.get(lid) or (api.LINES[lid],)
    assert ' '.join(pages) == api.LINES[lid] and all('"' not in p and '\\' not in p for p in pages), lid
    total = sum(len(p) for p in pages)
    out, t0 = [], 0
    for i, pg in enumerate(pages):
        t1 = hold if i == len(pages) - 1 else t0 + max(round(hold * len(pg) / total), LINE_GAP * ((len(pg) + 1) // 2) + 10)
        idx = [k for k, ch in enumerate(pg) if ch != ' ']                # two syllables a step, spaces come along
        cuts = [idx[k + 1] + 1 for k in range(0, len(idx), 2) if k + 1 < len(idx)]
        if not cuts or cuts[-1] != len(pg):
            cuts.append(len(pg))
        for j, c in enumerate(cuts):
            assert t0 + j * LINE_GAP < t1 - 8, (lid, pg, t0, t1)
            out.append((t0 + j * LINE_GAP, pg[:c]))
        t0 = t1
    return out + [(hold, None)]


def say(s, t, lid, cond=''):
    """Line `lid` from tick t of timeline s (cond: an execute condition for both drawings, e.g. the coda's branch)."""
    hold = api.LINE_AT[lid][2]
    held = f'entity @a[tag=player,tag={HOLD_TAG}]'
    kit = line(lid)
    pre = f'{cond} ' if cond else ''
    if kit:
        s.at(t, f'execute {pre}unless {held} run {kit}')
    for dt, text in line_steps(lid, hold):
        comp = None if text is None else f'{{text:"{text}",color:"{api.LINE_COLOR}"}}'
        cl = L.cam_line(comp)
        s.at(t + dt, f'execute {cond} {cl[8:]}' if cond else cl)
        if text is not None:
            s.at(t + dt, f'execute {pre}if {held} {TYPE_SND[8:]}')
    return s


def _tree(W, name, kind, ticks, lines_of, head):
    """A dispatch tree over `ticks`: consecutive ticks with the same lines share one leaf (<kind>/<t> or <kind>/<a>_<b>),
    branch files <kind>b/<a>_<b>, at most 8 children a level. Returns the root's lines. kind 'k' (the timeline) / 'c' (the
    camera)."""
    base = f'{SEQ}/{name}'
    runs = []                                   # [t0, t1, lines]
    for t in ticks:
        ls = list(lines_of(t))
        if runs and runs[-1][1] == t - 1 and runs[-1][2] == ls:
            runs[-1][1] = t
        else:
            runs.append([t, t, ls])
    leaves = []
    for t0, t1, ls in runs:
        rel = f'{kind}/{t0}' if t0 == t1 else f'{kind}/{t0}_{t1}'
        when = f'#sq {t0}' if t0 == t1 else f'#sq {t0}..{t1}'
        W.w(f'seq/{name}/{rel}', [f'# {name}: {head} at {when} (@s = the body).', *ls])
        leaves.append((t0, t1, f'{sq(t0 if t0 == t1 else f"{t0}..{t1}")} run return run function {base}/{rel}'))

    def node(ls):
        if len(ls) <= 8:
            return [x[2] for x in ls]
        size = math.ceil(len(ls) / 8)
        out = []
        for i in range(0, len(ls), size):
            g = ls[i:i + size]
            if len(g) == 1:
                out.append(g[0][2])
                continue
            a, b = g[0][0], g[-1][1]
            W.w(f'seq/{name}/{kind}b/{a}_{b}', [f'# {name}: {head}, the ticks {a}..{b}.'] + node(g))
            out.append(f'{sq(f"{a}..{b}")} run return run function {base}/{kind}b/{a}_{b}')
        return out
    return node(leaves)


HELP_SUMMON = f'execute at {STAGE} run summon minecraft:marker ~ ~ ~ {{Tags:{tags(HELP_T)}}}'


def stands(tr, first=None):
    """A locked sequence's start (and a skip's landing): the old cameras gone, both made where their first shots put them
    (cam.Track.spawn: a one-tick helper at the stage placed and aimed as the shot, mboss/cam/spawn_at: the rotation on the
    grid in the summon NBT, the entity 4 blocks before the viewpoint). The first frame anyone sees is tick 2 or later: every
    locked sequence opens on a full mask (CS0 black, CS1 and the ending white, the repel gold). `first`: {cam: shot}."""
    return [L.cam('kill'), *tr.spawn(HELP, HELP_SUMMON, first=first)]


def skip_cams(tr, shot):
    """A skip's cameras (under its black): both made anew on `shot` (new entities: nothing still glides), `shot`'s live at
    once; only while the run still has its lock."""
    out = [*stands(tr, first={A: shot, B: shot}), f'scoreboard players set {L.CAM_ID[0]} {L.CAM_ID[1]} {shot.cam}']
    return gate(f'unless score {CX_FP} {OBJ} matches 1', out)


def skip_files(W, name, tr):
    """seq/<name>/skipin (+ skipgo, skipoff): the skip input of a locked sequence, every tick of it (@s = the body): the jump
    key held api.SKIP_HOLD ticks inside api.SKIP[name]['window'] (Shift ends a spectate inside the game: it is no input
    here); the prompt 「⊙ 건너뛰기 · Space 길게」 on the camera's hint text, brightening in api.SKIP_STEPS steps (on the action
    bar when no camera holds the player). The core's own Shift input rests (#skip hr -1: core/skip returns at once); its test
    hook #skp hr (the skip at that tick) is honoured here."""
    base = f'{SEQ}/{name}'
    (lo, hi), to = api.SKIP[name]['window'], api.SKIP[name]['to']
    held = f'entity @a[tag=player,tag={HOLD_TAG}]'
    comp = lambda k: (f'{{text:"",extra:[{{text:"{api.SKIP_TEXT}",color:"{SKIP_COLS[k]}"}},'      # noqa: E731
                      f'{{text:"{SKIP_KEY_HINT}",color:"{SKIP_COLS[0]}"}}]}}')
    rows = []
    for k in range(api.SKIP_STEPS + 1):
        a, b = (0, 0) if k == 0 else ((k - 1) * 5 + 1, k * 5 if k < api.SKIP_STEPS else api.SKIP_HOLD - 1)
        rng = f'{a}..{b}' if a != b else str(a)
        rows += [f'execute if score {SKIP_FP} {OBJ} matches {rng} unless score {SKIP_STEP_FP} {OBJ} matches {k} {L.cam_hint(comp(k))[8:]}',
                 f'execute if score {SKIP_FP} {OBJ} matches {rng} unless {held} run title @a[tag=player] actionbar {comp(k)}',
                 f'execute if score {SKIP_FP} {OBJ} matches {rng} run {sset(SKIP_STEP_FP, k)}']
    W.w(f'seq/{name}/skipin', [
        f'# The {name} skip input (@s = the body, every tick of the sequence; v_brief VC 5): from {lo} to {hi} the prompt',
        f'# {api.SKIP_TEXT}{SKIP_KEY_HINT}; holding the jump key (rlk:in_jump) brightens it in {api.SKIP_STEPS} steps of 5 t, a release',
        f'# resets the count; {api.SKIP_HOLD} t held -> the skip (skipgo: seq/{name}/skip, then #sq = {to - 1}: the next tick is {to}).',
        '# The core\'s Shift input (core/skip) rests while #skip is -1.',
        sset('#skip', -1),
        f'execute if score {SKIP_DONE_FP} {OBJ} matches 1 run return 0',
        f'execute if score #skp {OBJ} matches 1.. if score #sq {OBJ} = #skp {OBJ} run return run function {base}/skipgo',
        f'execute if score #sq {OBJ} matches {hi + 1}.. run return run function {base}/skipoff',
        f'execute unless score #sq {OBJ} matches {lo}..{hi} run return 0',
        f'execute as {PL} if predicate rlk:in_jump run scoreboard players add {SKIP_FP} {OBJ} 1',
        f'execute as {PL} unless predicate rlk:in_jump run {sset(SKIP_FP, 0)}',
        f'execute if score {SKIP_FP} {OBJ} matches {api.SKIP_HOLD}.. run return run function {base}/skipgo',
        *rows, HUD_HOLD])
    W.w(f'seq/{name}/skipoff', [f'# The {name} skip prompt off for good (the window ended, the skip).',
                                sset(SKIP_DONE_FP, 1), L.cam_hint(None),
                                f'execute unless {held} run title @a[tag=player] actionbar ""'])
    W.w(f'seq/{name}/skipgo', [
        f'# The {name} skip (@s = the body): the prompt gone, the sequence\'s skip (the black, its state at tick {to}), then the',
        f'# clock jumps: the next tick is {to}. {SKIP_NOW_FP}: the rest of this tick\'s timeline is not played.',
        f'function {base}/skipoff', sset('#skp', 0), f'function {base}/skip', sset('#sq', to - 1), sset(SKIP_NOW_FP, 1)])
    return [f'function {base}/skipin',
            f'execute if score {SKIP_NOW_FP} {OBJ} matches 1 run return run {sset(SKIP_NOW_FP, 0)}']


def actor_lines(call, **macro):
    """An actor call (api.actor: '' until lane H3's manifest exists) as a list."""
    a = api.actor(call, **macro)
    return [a] if a else []


def actor_man():
    """Lane H3's actor manifest (tools/player_motion/cine/manifest.json: per clip its length, footfall ticks `steps` and per
    tick the root's `shift` and the hands / head / sword points in the stage frame), None until it exists."""
    if not api.actor_ready():
        return None
    m = json.loads(api.ACTOR_MANIFEST.read_text(encoding='utf-8'))
    assert m['tags']['root'] in ACTOR_ROOT and m['calls']['spawn'] == 'rlk:char/cine/spawn', (m['tags'], m['calls'])
    assert all(m['clips'][c]['len'] == n for c, n in (('cs0', api.SEQ_LEN['intro']), ('cs1', api.SEQ_LEN['cs1']), ('repel', api.SEQ_LEN['repel']),
                                                       ('ending', api.SEQ_LEN['ending']), ('coda', api.SEQ_LEN['event']))), 'actor clip lengths'
    return m


def actor_steps(clip, lo, hi, fallback):
    """[(tick, the root's f)] of the actor's footfalls in lo..hi: the manifest's `steps` of `clip` (H3), else `fallback`."""
    m = actor_man()
    if not m:
        return list(fallback)
    c = m['clips'][clip]
    return [(t, c['tick']['shift'][t][2]) for t in c['steps'] if lo <= t <= hi]


def actor_spawn(clip, carry=False, chained=False):
    """The actor at the stage, rotated as it, playing `clip` (spawn runs as the player; never in developer mode: the player
    is the body there and nothing is hidden). `carry`: the sequence before hands its actor over (the ending after the repel's
    lethal kick, the coda after the ending: H3's clips meet pose-exact, repel 129 = ending 0, ending 1372 = coda 0): no new
    spawn while it stands. `chained`: the start inherits the lock state (write(chain=True)): no actor for a run whose lock
    was already lost."""
    sp = api.actor('spawn')
    if not sp:
        return []
    cx = f'unless score {CX_FP} {OBJ} matches 1 ' if chained else ''
    root = f'unless entity {ACTOR_ROOT} ' if carry else ''
    return [f'execute {cx}as {PL} unless entity @s[tag=rlk_body] {root}at {STAGE} run {sp}',
            *[(f'execute {cx}run {x}' if cx else x) for x in actor_lines('play', clip=clip)]]


def write(W, name, s, head, length, start_head=(), cancel=(), macro=False, track=None, chain=False, fin=True, keep=False, skip=False):
    """seq/<name>/{start,tick,cancel} + k/<t> + kb/<a>_<b>; for a locked sequence (LOCK) also lock / unlock / fin / cam +
    c/<t> + cb/<a>_<b>. start = its head lines, #sqdone 0, the lock of tick 0, then the tick-0 lines. `chain`: the lock is
    inherited from the sequence before (the coda after the ending): the interrupt flag is not reset. `fin`: the stands,
    the actor and the stage go at the first tick without the lock (False: the next sequence takes them over). `keep`: a
    cancel while KEEP_FP is 1 leaves the actor standing for the sequence the core starts in the same tick (the repel's
    lethal kick -> death_start -> core/stop_all -> the ending); the framework's release stops it if none follows."""
    base = f'{SEQ}/{name}'
    hold = [HUD_HOLD] if name in HUD_OFF else []
    blank = [HUD_BLANK] if name in HUD_OFF else []
    lock = LOCK.get(name)
    lock0, lockn = [], []
    leash_off = ['scoreboard players set #mbNoLeash mb 0'] if name in NO_LEASH else []
    if lock:
        t0, t1 = lock
        assert t0 == 0 and track is not None, name
        cl = track.lines()
        assert all(0 <= t < t1 for t in cl), (name, [t for t in cl if not 0 <= t < t1])
        root = _tree(W, name, 'c', sorted(cl), lambda t: cl[t], 'the camera')
        W.w(f'seq/{name}/cam', [f'# {head}', '# The camera lines of this tick (@s = the body; from lock, only while the lock holds).', *root])
        req = api.cam_req()
        W.w(f'seq/{name}/lock', [
            f'# {head}',
            f'# The lock of this tick (@s = the body; #sq {t0}..{t1 - 1} while {CX_FP} is not 1): the request the framework holds the',
            '# player on (#mbCam mb 1, cleared by mboss/main every tick), the actor on the sequence clock, the camera lines.',
            f'# {HELD_FP} = this run has seen the player held. Released after that (a pause, /reload, a relog, a killed stand), or',
            f'# never held by tick {GRANT_BY} (the framework holds in the tick of the first request made inside mboss/main, one tick',
            '# later for a start outside it: a kill by a hit) -> no lock for the rest of the run (unlock). Never in the developer',
            '# mode: its player is the body and is never held.',
            f'execute if entity @a[tag=player,tag={HOLD_TAG}] run scoreboard players set {HELD_FP} {OBJ} 1',
            f'execute if score {HELD_FP} {OBJ} matches 1 unless entity @a[tag=player,tag={HOLD_TAG}] unless entity @a[tag=player,tag=rlk_body] '
            f'run return run function {base}/unlock',
            f'execute if score #sq {OBJ} matches {GRANT_BY}.. unless score {HELD_FP} {OBJ} matches 1 unless entity @a[tag=player,tag=rlk_body] '
            f'run return run function {base}/unlock',
            *([req] if isinstance(req, str) and req else list(req or [])),
            *[x for x in (api.actor_clock(),) if x],
            *[f'execute as {PL} run {x}' for x in actor_lines('tick')],
            f'function {base}/cam'])
        W.w(f'seq/{name}/unlock', [
            f'# {head}',
            '# The lock is lost for this run (@s = the body): the stands and the actor go (the framework already released the',
            '# player and showed the avatar); the sequence plays on unlocked.',
            sset(CX_FP, 1), L.cam('kill'), *actor_lines('stop')])
        W.w(f'seq/{name}/fin', [
            f'# {head}',
            '# The first tick without the lock (the framework releases the player in this tick): the stands, the actor and the',
            '# stage go.', L.cam('kill'), *actor_lines('stop'), f'kill @e[type=minecraft:marker,tag={STAGE_T}]',
            f'kill @e[type=minecraft:marker,tag={STAGE2_T}]', sset(HELD_FP, 0), *leash_off])
        call = f'execute unless score {CX_FP} {OBJ} matches 1 run function {base}/lock'
        lock0 = [call]
        lockn = [f'execute if score #sq {OBJ} matches ..{t1 - 1} unless score {CX_FP} {OBJ} matches 1 run function {base}/lock']
        if fin:
            s.at(t1, f'function {base}/fin')
    # a cancel releases everything at once (the core cancels on a pause / reload and goes to the end state itself): the lock
    # request of this tick taken back (the framework then releases the player in this tick), the kit's line / overlay off,
    # the HUD hold ended
    release = [x for x in (f'scoreboard players set {L.CAM_REQ[0]} {L.CAM_REQ[1]} 0', K.hud('clear'), L.cam_line(None), L.cam_hint(None),
                           HUD_FREE) if x]
    skipin = skip_files(W, name, track) if skip else []
    skip0 = [sset(SKIP_FP, 0), sset(SKIP_STEP_FP, -1), sset(SKIP_DONE_FP, 0), sset(SKIP_NOW_FP, 0), sset('#skip', -1)] if skip else []
    stop_lines = actor_lines('stop')
    if keep and stop_lines:
        stop_lines = [f'execute unless score {KEEP_FP} {OBJ} matches 1 run {x}' for x in stop_lines] + [sset(KEEP_FP, 0)]
    W.w(f'seq/{name}/start', [f'# {head}', f'# Start (@s = the body, at it; #sq {OBJ} = 0){" — macro" if macro else ""}.',
                              *[c for c in start_head if c], sset('#sqdone', 0),
                              *([sset(CX_FP, 0), sset(HELD_FP, 0)] if lock and not chain else []), *skip0, *hold, *blank, *lock0,
                              *s.t.get(0, [])])
    ticks = sorted(t for t in s.t if t > 0)
    assert all(t <= length for t in ticks), (name, max(ticks), length)
    root = _tree(W, name, 'k', ticks, lambda t: s.t[t], 'the timeline')
    W.w(f'seq/{name}/tick', [f'# {head}',
                             f'# Tick (@s = the body; #sq {OBJ} 1.. = the clip tick shown this game tick); #sqdone at {length}.',
                             f'{sq(f"{length}..")} run scoreboard players set #sqdone {OBJ} 1', *hold, *lockn, *skipin, *root])
    W.w(f'seq/{name}/cancel', [f'# {head}', '# Cancel (no executor; idempotent): what this sequence made.',
                               f'kill @e[type=minecraft:marker,tag={STAGE_T}]', f'kill @e[type=minecraft:marker,tag={STAGE2_T}]',
                               f'kill @e[type=minecraft:marker,tag={HELP_T}]',
                               *([L.cam('kill'), *stop_lines, sset(CX_FP, 0), sset(HELD_FP, 0), *release] if lock else []), *leash_off,
                               *[c for c in cancel if c]])


# ---- common pieces ----------------------------------------------------------------------------------------------------------
def lib(W):
    """seq/lib/ok: the check of a staged point of hers (see the module doc)."""
    W.w('seq/lib/ok', [
        f'# At a proposed feet position of a staged move: on the arena floor inside the barrier ring ({num(OKW_R)} b from the axis:',
        '# the walk disc and the ring up to the out-of-bounds line) with free feet and head. The stage axis from the avatar to',
        '# its mv/ok-checked forward point lies inside it, also when the avatar stands outside the safe disc.',
        f'execute positioned ~ {CY} ~ unless entity @e[tag=rlk_mb_arena,distance=..{num(OKW_R)},limit=1] run return fail',
        'execute unless block ~ ~ ~ #rlk:dash_pass run return fail',
        'execute unless block ~ ~1 ~ #rlk:dash_pass run return fail',
        'return 1'])
    up = f'execute at @s run tp @s ~ {num(CY + LIFT_TO)} ~'
    W.w('seq/lib/lift', [
        '# @s = a camera stand on a low eye point of a staged shot, placed and aimed: the lens is not left inside a plant of',
        f'# the field (dry grass; crimson roots in the crimson look; 1 b tall): its own cell or the cell {num(LIFT_AHEAD)} b along its',
        f'# view holds one -> the stand goes to {num(LIFT_TO)} b over the floor (the caller aims it again).',
        *[f'execute at @s if block ~ ~ ~ {b} run return run {up}' for b in PLANTS],
        *[f'execute at @s rotated ~ 0 positioned ^ ^ ^{num(LIFT_AHEAD)} if block ~ ~ ~ {b} run return run {up}' for b in PLANTS]])
    W.w('seq/lib/camin', [
        '# @s = a camera entity of a dynamic stage after mboss/cam/fix (4 b before its viewpoint along its view): pulled into',
        f'# the walk disc as the viewpoint was, and not left lower than {num(CAMIN_MIN)} b over the floor (a lens that looks down at',
        '# something near it: the client looks along the 4-block line from the viewpoint to the entity; in the ground the game',
        '# would cut that line short). The rotation stays: the viewpoint moves by as much as the entity.',
        'function rlk:mboss/ar/clampw',
        f'execute store result score #sq_cy {OBJ} run data get entity @s Pos[1] 100',
        f'execute if score #sq_cy {OBJ} matches ..{round((CY + CAMIN_MIN) * 100) - 1} at @s run tp @s ~ {num(CY + CAMIN_MIN)} ~'])
    W.w('seq/lib/over', [
        '# @s = a camera stand placed on a stage eye point and pulled into the walk disc: when the actor stands with its back',
        f'# at the wall, an eye meant to be behind it lands on it. A lens nearer than {num(OVER_R)} b (on the floor plane) to the stage',
        f'# origin = the actor\'s place goes {num(OVER_TO)} b over the floor: over its head (the caller aims it afterwards).',
        *[f'execute at @s positioned ~ {CY} ~ if entity @e[type=minecraft:marker,tag={tg},distance=..{num(OVER_R)}] run return run '
          f'tp @s ~ {num(CY + OVER_TO)} ~' for tg in (STAGE_T, STAGE2_T)]])


class Moves:
    """Helper functions seq/<name>/m/<key> (@s = the body): candidate destinations tried in order (return at the first)."""

    def __init__(self, name):
        self.name, self.files, self.done = name, {}, set()

    def add(self, key, lines, head):
        assert key not in self.files, (self.name, key)
        self.files[key] = [f'# {head} (@s = the body).'] + [x for x in lines if x]
        return f'function {SEQ}/{self.name}/m/{key}'

    def ref(self, key):
        return f'function {SEQ}/{self.name}/m/{key}'

    def write(self, W):
        """Write the helpers added since the last call (a sequence with a skip adds more after its timeline is written)."""
        for k, v in self.files.items():
            if k not in self.done:
                W.w(f'seq/{self.name}/m/{k}', v)
                self.done.add(k)

    def stage(self, fmax):
        """m/stage: the stage marker at the avatar's feet on the floor, forward toward her (the avatar's own facing when she
        is nearer than 0.6 b), toward the arena centre when ST(0, 0, fmax) fails mv/ok; her yaw toward the actor."""
        return self.add('stage', [
            f'kill @e[type=minecraft:marker,tag={STAGE_T}]', f'kill @e[type=minecraft:marker,tag={STAGE2_T}]',
            f'execute at {PLB} positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:{tags(STAGE_T)}}}',
            f'execute as {STAGE} at @s facing entity {BODY} feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0', DIST,
            f'execute if score #mbDist mb matches ..6 as {STAGE} at @s rotated as {PLB} rotated ~ 0 run tp @s ~ ~ ~ ~ 0',
            f'execute as {STAGE} at @s positioned ^ ^ ^{num(fmax)} unless {OK} at @s facing entity {ARENA} feet rotated ~ 0 '
            'run tp @s ~ ~ ~ ~ 0'],
            f'The stage of this sequence (hr_design §3.0; FMAX {fmax})')

    def turn(self, key, target, cap, what):
        """m/<key>: the body turns at most `cap` degrees toward `target` (an execute `facing` argument) this tick, yaw only."""
        c = round(cap * 100)
        return self.add(key, [
            f'execute store result score #sq_y0 {OBJ} run data get entity @s Rotation[0] 100',
            f'execute at @s run summon minecraft:marker ~ ~ ~ {{Tags:{tags(HELP_T)}}}',
            f'execute at @s facing {target} run tp {HELP} ~ ~ ~ ~ 0',
            f'execute store result score #sq_y1 {OBJ} run data get entity {HELP} Rotation[0] 100',
            f'kill @e[type=minecraft:marker,tag={HELP_T}]',
            f'scoreboard players operation #sq_y1 {OBJ} -= #sq_y0 {OBJ}', f'scoreboard players add #sq_y1 {OBJ} 90000',
            f'scoreboard players operation #sq_y1 {OBJ} %= #c36000 mb', f'scoreboard players remove #sq_y1 {OBJ} 18000',
            f'execute if score #sq_y1 {OBJ} matches {c + 1}.. run scoreboard players set #sq_y1 {OBJ} {c}',
            f'execute if score #sq_y1 {OBJ} matches ..-{c + 1} run scoreboard players set #sq_y1 {OBJ} -{c}',
            f'scoreboard players operation #sq_y0 {OBJ} += #sq_y1 {OBJ}',
            f'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #sq_y0 {OBJ}'],
            f'The body turns at most {num(cap)} degrees toward {what} this tick, yaw only')


def cand(pos, mv, ok=OKW):
    """One candidate line: at pos (an execute positioning chain) if `ok` then the move."""
    return f'execute {pos} if {ok} run return run {mv}'


def glide(t):
    return f'function rlk:mboss/mv/glide {{t:{t}}}'


def leap(t, h):
    return f'function rlk:mboss/mv/leap {{t:{t},h:{h}}}'


TP = 'tp @s ~ ~ ~'                                   # an instant placement (her yaw kept)
STOP = 'function rlk:mboss/mv/stop'
FACE_ACTOR = f'execute rotated as {STAGE} run rotate @s ~180 0'      # her yaw = the stage yaw + 180 (hr_design §3.0 Facing)
FACE_ACTOR2 = f'execute rotated as {STAGE2} run rotate @s ~180 0'
FACE_PLB = f'execute facing entity {PLB} feet run rotate @s ~ 0'      # toward the avatar (lead-ins, the skip)


def near(d, side=0):
    """d b from the avatar on its line to her (side b to its left), on the floor."""
    return f'at {PLB} facing entity @s feet rotated ~ 0 positioned ^{num(side)} ^ ^{num(d)} positioned ~ {CY} ~'


def gate(cond, cmds):
    """cmds behind an execute condition (an 'execute ...' line gets the condition inserted)."""
    out = []
    for c in cmds if isinstance(cmds, (list, tuple)) else [cmds]:
        if c:
            out.append(f'execute {cond} {c[8:]}' if c.startswith('execute ') else f'execute {cond} run {c}')
    return out


def rock(look):
    """The kit's seat_rock (the core's decor prop at api.deco()['seat_rock']) re-looked."""
    p = api.deco()['seat_rock']
    c = K.prop('seat_rock', look=look)
    return (f'execute positioned {api.xyz(p, 3)} as @e[type=minecraft:item_display,tag={api.TAGS["deco"]},'
            f'distance=..1,limit=1] run {c}') if c else None


def rock_kill():
    p = api.deco()['seat_rock']
    return f'execute positioned {api.xyz(p, 3)} run kill @e[type=minecraft:item_display,tag={api.TAGS["deco"]},distance=..1]'


def halo(bright):
    """The core's decor moon halo in the bright look of the arena's current look (moon -> p1b, crimson -> p2b) or back."""
    out = []
    for look, base in (('moon', 'p1'), ('crimson', 'p2')):
        c = K.prop('moon_halo', look=base + ('b' if bright else ''))
        if c:
            out.append(f'execute if data storage rlk:mboss {{look_{api.AID}:"{look}"}} as @e[type=minecraft:item_display,'
                       f'tag={api.TAGS["deco_moon_halo"]}] run {c}')
    return out


def line(i):
    return K.hud('line', id=i)


def snd(name):
    return K.snd(name)


def raw(event, vol, pitch=1.0):
    """A vanilla sound the kit has no recipe for, at the execution position (mboss_lib.sound: vanilla events only)."""
    return L.sound(event, vol, pitch)


def gold(t_in, hold, t_out):
    """The deflect's gold wash: lane H2c's `gold` overlay glyph (live since the HI merge). The `white` fallback only shows
    if the kit is ever built without the H2c block (api.K returns '' for an undeclared overlay)."""
    return K.ovl('gold', t_in, hold, t_out) or K.ovl('white', t_in, hold, t_out)


def sig(name):
    return f'scoreboard players set {api.SEQ_SIGNAL} {OBJ} {api.SIG[name]}'


# ---- the big petal (kit prop petal_big, about 0.4 b of petal on a 0.8-b card): an item_display the sequence carries. It
# faces the lens by itself (billboard "center": the kit dresses it "fixed", so the billboard is set again after each look).
# Round V (T1-STAGE-1): a petal is never nearer than 1.5 b to the lens (petal-sized on the screen) and during a line it
# passes BEHIND her, never across her face.
PETAL_BB = 'data merge entity @s {billboard:"center"}'


def petal_summon(tag, pos, cam=None, look='whole'):
    c = K.prop('petal_big', look=look)
    if not c:
        return []
    sel = f'@e[type=minecraft:item_display,tag={tag},limit=1]'
    return [f'kill @e[type=minecraft:item_display,tag={tag}]',
            f'execute {pos} run summon minecraft:item_display ~ ~ ~ {{Tags:{tags(PROP_T, tag)},teleport_duration:1,view_range:2f}}',
            f'execute as {sel} run {c}', f'execute as {sel} run {PETAL_BB}']


def petal_move(tag, pos, cam=None):
    if not K.prop('petal_big', look='whole'):
        return None
    return f'execute as @e[type=minecraft:item_display,tag={tag},limit=1] {pos} run tp @s ~ ~ ~'


def petal_look(tag, look):
    c = K.prop('petal_big', look=look)
    sel = f'@e[type=minecraft:item_display,tag={tag},limit=1]'
    return [f'execute as {sel} run {c}', f'execute as {sel} run {PETAL_BB}'] if c else None


def petal_kill(tag):
    return f'kill @e[type=minecraft:item_display,tag={tag}]'


def before_cam(cam, x, y, d):
    """A point d b before the LENS of camera `cam` (x to its left, y up, in its view frame): the camera entity stands
    mboss_lib.CAM_BACK = 4 b before the lens, so the point is d - 4 along the entity's own view."""
    return f'at {CAM[cam]} positioned ^{num(x)} ^{num(y)} ^{num(d - L.CAM_BACK)}'


PETAL = tuple(f'{PROP_T}_{i}' for i in range(1, 6))
KILL_PROPS = f'kill @e[type=minecraft:item_display,tag={PROP_T}]'


# =============================================================================================================================
# CS0 — intro (hr_design §3.1; clip intro 1290 + intro_end 150 = 1440) and its skip. The stage is fixed: origin api.CS0_P0
# (start + 6 b toward her seat), forward to the seat 20.73 b ahead; her, the seat and the moon are on its axis.
P0 = api.CS0_P0
SEAT_F = round(math.dist(P0[::2], api.SEAT_POS[::2]), 2)             # 20.73
YAW0 = math.degrees(math.atan2(-(api.SEAT_POS[0] - P0[0]), api.SEAT_POS[2] - P0[2]))
assert abs(SEAT_F - 20.73) < 0.01, SEAT_F
WALK_F, END_F = 13.5, api.CS0_END_DIST                               # she walks to f 13.5, leaps to f 6.5 (control)
# CS0's opening mask (ovl g, in, hold, out). Round V (T1-START-1, T1-GHOST-3): the arena is still arriving on the client for
# about 1.4 s after tick 0 (missing chunk columns show the sky; a camera entity in a chunk that is not sent yet is not
# known to the client): the black holds 34 t and is gone by 42; I1 and I2 are timed after it.
CS0_MASK = ('black', 0, 34, 8)
CS0_RESEND = 44                                                      # ticks the hold re-sends the camera for real (the arrival)
I2_T = 76                                                            # the cut to the side track


def build_intro(W):
    s, mv = Seq('intro'), Moves('intro')
    e = lambda k, d=0: ev('intro', k, d)                              # noqa: E731
    x = lambda k, d=0: api.SKIP_T + ev('intro_end', k, d)             # noqa: E731  intro_end events on the intro clock
    # ---- the camera: 20 shots (the stage is fixed and every eye is checked offline: no clamp)
    tr = C.Track('intro', {'ST': STAGE, 'HR': BODY}, LOCK['intro'][1], clamp=False, her=her_of('intro'))
    # (the design's start f -9.0 is in the barrier ring, 26.6 b from the axis: f -7.4 is the walk disc's edge)
    # round V: the black of the arrival covers ticks 0-41 (CS0_MASK): I1 pushes in behind the walking actor 24-74, the side
    # track follows the last of the walk (the actor's f = -6 + 0.075 (t - 20), at the origin at 100)
    # (round V: the client's 4-b line from the viewpoint must clear the barrier ring by its 0.1-b corner rays: f -7.0)
    tr.cut(0, A, ST(0.6, 1.9, -7.0), ST(0, 1.4, -3.0), 'I1 arrival', ('actor',))
    tr.move(24, 74, ST(0.6, 1.7, -4.5), ST(0, 1.4, 0.0))
    tr.cut(I2_T, B, ST(-7.0, 1.2, -2.0), ST(0, 1.2, -2.0), 'I2 side track', ('actor',))
    tr.move(I2_T, 102, ST(-7.0, 1.2, -0.2), ST(0, 1.2, -0.2))
    tr.cut(110, A, ST(-3.0, 1.5, 14.0), WP(MOON[1] - 6, MOON[2], MOON[3]), 'I3 moon', ('moon',))
    tr.move(110, 169, look=MOON)
    tr.cut(170, B, HR(0.9, 0.75, 0.9), HR(0.25, 0.62, 0.35), 'I4 petal on her hand', ('her',))
    tr.move(220, 236, look=HR(0.3, 0.8, 0.1))
    tr.move(236, 249, look=HR(0, 1.55, 0))
    # (round V, VC 10: line 1 sits in the lower third; the lens looks at her shoulder so her face is in the upper half)
    tr.cut(250, A, HR(1.1, 1.42, 0.25), HR(0, 1.2, 0.05), 'I5 profile', ('her',))
    tr.move(250, 319, eye=HR(1.1, 1.42, 0.35))
    tr.cut(320, B, HR(-0.55, 0.5, -0.7), HR(-0.35, 1.05, 0.5), 'I6 bottle', ('her',))
    # (round V: level with the cup. The client looks from 4 b behind the camera entity, so the entity of a lens that looks
    # down at something low would be under the floor: the design's eye 0.6 b up looking 25 degrees down)
    tr.cut(410, A, HR(1.15, 0.42, 0.6), HR(0.45, 0.4, 0), 'I7 cup', ())
    tr.cut(460, B, HR(0.75, 1.0, -0.9), MOON, 'I8 cup to the moon', ('her', 'moon'))
    # (HF-B, HB-06: every line on a shot close on her, lines 4-10) I9 pushed in: the design's 2.4 b from her head -> 2.0-1.7
    tr.cut(536, A, HR(-1.2, 1.55, -1.6), HR(0.15, 1.3, 0.5), 'I9 over her shoulder', ('her',))
    tr.move(536, 665, eye=HR(-1.0, 1.5, -1.3))
    # the guest (no line) until line 5; line 5 (690-819): her face from before her (the cup set down 700-712), then I11 framing
    # her face with both hands on the sword, then she stands up on the rock in the same close frame
    tr.cut(666, B, ST(0.45, 1.75, -0.9), ST(0, 1.5, 20.7), 'I10 the guest', ('actor', 'her'))
    tr.cut(690, A, HR(-0.35, 1.45, 1.5), HR(0, 1.35, 0), 'I10b her (line 5)', ('her',))
    tr.cut(750, B, HR(0.8, 1.2, 0.95), HR(0.2, 1.02, 0.12), 'I11 hand on the sword', ('her',))
    tr.cut(790, A, HR(0.5, 1.45, 1.7), HR(0, 1.6, 0), 'I12a standing up', ('her',))
    # the silhouette against the moon where no line plays (820-838), then her turn to the actor and the smile in one close shot
    # from the actor's side (lines 6 and 7; the video's I13 framing)
    tr.cut(820, B, ST(0, 0.25, 16.0), HR(0, 1.5, 0), 'I12 against the moon', ('her', 'moon'))
    tr.cut(838, A, ST(0.25, 1.75, 19.3), HR(0, 1.7, 0), 'I13 the turn, smile', ('her',))
    tr.cut(960, B, WP(878, 204.5, 2), WP(858, 203, 14), 'I14 the field', ())
    tr.cut(980, A, HR(0.7, 2.0, 1.5), HR(0, 1.95, 0), 'I14b her (line 8)', ('her',))
    # lines 9 and 10: a close shot before her that walks back with her (an HR eye moved onto itself is placed in her frame
    # every tick): the walk with the hand on the brim, the stop, the hat tipped back
    tr.cut(1040, B, HR(-0.45, 1.65, 1.75), HR(0, 1.65, 0), 'I15 walk, hat tipped', ('her',))
    tr.track(e('walk'), e('stop'), every=24)                         # the lens walks back before her (0.075 b/t, four segments)
    # round V (T1-STAGE-4: from under her path she was a 40-px speck in the dome): the leap from the side, 4.6 b off the
    # axis at her landing's depth: she crosses the frame a third of its height tall; the lens follows her (chase)
    tr.cut(1230, A, ST(-4.6, 1.3, 9.2), HR(0, 1.0, 0), 'I16 leap', ('her',))
    tr.chase(e('leap'), e('land') + 1)
    tr.cut(1260, B, ST(1.6, 0.5, 4.2), HR(0, 0.9, 0), 'I17 landing', ('her',))
    # (HF-B, HB-07) under the brim: the lens a little over her eye line, so her low, forward-tipped brim (intro_end 0-40, head
    # about 25-44 degrees down) lies between it and her eyes (every eye pixel: the face's rows 4-5). It opens 2.0 b out on the
    # crouched figure and pushes in once she has risen (1298-1312) to 1.25 b: her mouth shows under the brim edge from 1302,
    # her eyes only when the brim lifts (1330-1346); the lens stays >= 0.5 b from the brim (her_tracks.json; test_seq F3)
    tr.cut(1290, A, HR(0.15, 1.95, 1.9), HR(0, 1.55, 0), 'I18 under the brim', ('her',))
    tr.move(1298, 1312, eye=HR(0.15, 1.85, 1.4), ease='io')
    tr.cut(1350, B, HR(0.4, 1.4, 1.6), HR(0, 1.3, 0), 'I19 draw, stance', ('her',))
    tr.move(1350, 1400, eye=HR(0.6, 1.3, 3.2))
    tr.cut(1406, A, ST(0.6, 1.8, 3.0), ST(0, 1.5, 6.5), 'I20 back to the player', ('her', 'actor'))
    tr.move(1406, 1421, eye=ST(0.3, 2.9, 0.0))                       # the arc over the actor's head ...
    tr.move(1421, 1436, eye=ST(0, 2.6, -3.4))                        # ... to the F5 camera's place
    TRACKS['intro'] = tr
    STAGED['intro'] = [(0, 'ST', SEAT_F, 'seated'), (1148, 'ST', WALK_F, 'the walk ends'), (1258, 'ST', END_F, 'the landing'),
                       (1440, 'ST', END_F, 'control')]
    # ---- I1-I2: the rift closing behind the actor, the ambient, the wind (2 s), the actor's steps (its clip's footfalls)
    rift = K.p('arrive_rift')
    s.st(0, ST(0, 0, -api.CS0_WALK_BACK - 1.5), rift)
    # (HF-B, HB-03) the opening mask: the arrival blindness is the player's own effect and does not reach a stand's view; a
    # black over ticks 0-1 (fading 2-7) hides the avatar's teleport, the actor's spawn and the game-mode switch, as the
    # other locked sequences' white / gold do, and the first frame shown is the I1 stand's third tick at its eye
    s.at(0, K.ovl(*CS0_MASK))
    s.at(0, K.p('ambient_p1'), (f'execute at {PL} run {snd("cs0_wind")}' if snd('cs0_wind') else None))   # at the listener (HR-46)
    stop_wind = 'stopsound @a[tag=player] * minecraft:item.elytra.flying' if snd('cs0_wind') else None
    s.at(I2_T, stop_wind)
    for t, f in actor_steps('cs0', 0, api.SEQ_LEN['intro'], [(t, -api.CS0_WALK_BACK + 0.075 * (t - 20)) for t in range(20, 100, 12)]):
        s.st(t, ST(0, 0, round(f, 2)), snd('grass_step'))     # the actor's footfalls (lane H3's manifest; the design's 12 t without it)
    # ---- lines 1-10 at api.LINE_AT (their clip events l1..l10)
    for i in range(1, 11):
        assert api.LINE_AT[i][0] == 'intro' and api.LINE_AT[i][1] == e(f'l{i}'), i
        say(s, api.LINE_AT[i][1], i)
    # ---- I3-I4: one big petal falls through the moon shot (150-170, 1.5 b before the lens), then settles on her right hand
    # (176 -> 190, follows the anchor), rolls off 206-216
    p1 = PETAL[0]
    s.at(150, petal_summon(p1, before_cam(A, 0.4, 0.9, 1.5)), snd('cs0_petals'))
    for t in range(151, 170):
        u = (t - 150) / 20
        s.at(t, petal_move(p1, before_cam(A, 0.4 - 0.6 * u, 0.9 - 1.8 * u, 1.5)))
    s.at(170, petal_kill(p1))
    if K.prop('petal_big', look='whole'):
        on_hand = lambda h, dx=0.0: f'at {ANCHOR} positioned ~{num(dx)} ~{num(h)} ~'   # noqa: E731
        s.at(176, api.rig('anchor/hand_r'), petal_summon(p1, on_hand(0.8), B))
        for t in range(177, 207):
            h = max(0.06, 0.8 - 0.74 * (t - 176) / 14)
            s.at(t, api.rig('anchor/hand_r'), petal_move(p1, on_hand(h), B))
        for t in range(207, 216):
            u = (t - 206) / 10
            s.at(t, api.rig('anchor/hand_r'), petal_move(p1, on_hand(0.06 - 0.5 * u * u, 0.35 * u), B))
        s.at(216, petal_kill(p1))
    # ---- I6-I10: the bottle (rock bare 326, pour 356, back 424), the cup to the moon (the halo brighter 474-530, the chime
    # 486), the drink 612, the cup set down 700 (rock set)
    s.at(e('take_bottle'), rock('bare')).at(e('pour', 4), snd('cs0_pour'))
    s.at(e('bottle_down', 10), rock('bottle'), snd('cs0_cup'))
    s.at(e('raise', 4), halo(True)).at(e('raise', 16), snd('cs0_moon')).at(530, halo(False))
    s.at(e('drink', 12), snd('cs0_sip'))
    s.at(e('cup_down', 12), rock('set'))
    # ---- I11: both hands on the sheathed sword: the chain's sound 758, the white glint at the scabbard's mouth 770
    s.at(e('grip', 2), snd('scab_raise')).fx(e('glint', 6), 'scabbard_mouth', K.p('glint', c=api.C_WHITE))
    # ---- I12: she stands up on the rock (the clip), turns to the actor 840-880 (4.5 deg / t, then exactly)
    turn = mv.turn('turn_pl', f'entity {PLB} feet', 4.5, 'the avatar')
    for t in range(e('turn'), e('turn', 40)):
        s.at(t, turn)
    s.at(e('turn', 40), FACE_ACTOR)
    # ---- I14: the field (the petals drift, the leaves' sound)
    s.st(e('l8', -10), WP(868, 203, 8), K.p('petals_drift')).at(e('l8', 10), snd('cs0_petals'))
    # ---- I15: off the rock 1040-1052 (rock and props gone 1052), the walk f 20.73 -> 13.5 (1052-1148, 0.075 b/t)
    walk = mv.add('walk', [cand(floor_pt(WALK_F), glide(e('stop') - e('walk')))],
                  f'I15 the walk to f {WALK_F} over {e("stop") - e("walk")} t (0.075 b/t)')
    s.at(e('walk'), rock_kill(), api.rig('look/props/none'), FACE_ACTOR, walk)
    for t in range(e('walk'), e('stop'), 12):
        s.at(t, snd('grass_step'))
    # ---- I16-I17: the leap f 13.5 -> 6.5 (1234-1258, apex 4.5 b), the afterimages, the landing (dust ring)
    lp = mv.add('leap', [cand(floor_pt(END_F), leap(e('land') - e('leap'), 45))], f'I16 the leap to f {END_F} (apex 4.5 b)')
    s.at(e('leap'), lp, snd('leap'))
    for t in (e('leap', 2), e('leap', 10)):
        s.me(t, K.p('afterimage', len=20), y=0)
    s.me(e('land'), K.p('dust_ring', r=12), y=.1).at(e('land'), snd('land_far'))
    # ---- I18-I20 on the intro_end clip: line 11, the draw (the title, the glint at the blade tip, the white-lilac crescent),
    # music 1
    assert api.LINE_AT[11] == ('intro_end', ev('intro_end', 'l11'), api.LINE_AT[11][2])
    s.at(api.SKIP_T, api.play('intro_end'), FACE_ACTOR)
    say(s, x('l11'), 11)
    s.at(x('draw', -4), snd('draw_spin'))
    s.at(x('draw'), L.title(*api.TITLE), snd('draw'))
    s.fx(x('draw'), 'blade_tip', K.p('glint', c=api.C_WHITE)).me(x('draw'), K.p('qi_arc', r=18, yaw=0, pitch=0, roll=0, c=api.C_LILAC))
    s.at(x('music'), api.music(1))
    mv.write(W)
    head = ('CS0 intro (hr_design §3.1): 20 shots, lines 1-11; seated with the cup and the bottle, the walk, the leap; intro_end: '
            'line 11, the draw, the stance.')
    stage0 = [f'kill @e[type=minecraft:marker,tag={STAGE_T}]', f'kill @e[type=minecraft:marker,tag={STAGE2_T}]',
              f'summon minecraft:marker {api.xyz(P0, 3)} {{Tags:{tags(STAGE_T)}}}',
              f'execute as {STAGE} at @s facing {api.xyz((api.SEAT_POS[0], P0[1], api.SEAT_POS[2]), 3)} run tp @s ~ ~ ~ ~ 0',
              '# the one avatar teleport: the player (and with them the avatar and the fall marker) to the stage origin, under the',
              '# arrival blindness',
              f'execute as {PL} at {STAGE} run tp @s ~ ~ ~ ~ 0', f'execute as {PL} run function rlk:view/sync',
              f'execute at {STAGE} run tp @e[tag=rlk_safe,limit=1] ~ ~ ~']
    write(W, 'intro', s, head, api.SEQ_LEN['intro'], track=tr, skip=True,
          start_head=stage0 + [*stands(tr), L.cam_resend(CS0_RESEND), *actor_spawn('cs0'), api.play('intro')],
          cancel=[stop_wind, KILL_PROPS] + halo(False))
    # ---- the skip (the core calls it after api.SKIP_HOLD t of sneak, then sets #sq to SKIP_T - 1: the next tick is I18)
    b18 = tr.shot_at(api.SKIP_T)
    assert b18.t == api.SKIP_T and b18.name.startswith('I18'), b18.name
    W.w('seq/intro/skip', [
        '# The intro skip (@s = the body; hr_design §3.1, v_brief VC 8): the black falls; under it the intro is cleared (the line,',
        '# the wind, the rock and the props, a move in progress, the petal), she stands at f 6.5 facing the actor (the',
        '# landing\'s place) and her model with her (RIG_NOW: the rig\'s own follow runs in the tick\'s stale position, so without',
        '# it she stayed on the rock until the fight began), both cameras are made anew on I18; seq/intro/skipgo then sets #sq to',
        '# 1289 and the next tick plays intro_end from its tick 0. The actor shows its tick 1290 by itself (#cavT cine follows',
        '# #sq). Line 11 is typed on the camera text, under the black until that has faded.',
        *[c for c in (K.hud('clear'), L.cam_line(None), K.ovl('black', 0, 20, 6), stop_wind) if c], *halo(False), HUD_HOLD, KILL_PROPS,
        STOP, rock_kill(), api.rig('look/props/none'),
        f'execute {floor_pt(END_F)} run {TP}', FACE_ACTOR, RIG_NOW,
        *skip_cams(tr, b18)])
    mv.write(W)


# =============================================================================================================================
# CS1 — the 60 % cutscene (hr_design §3.2; clip cs1 720) and its skip (-> #sq 566)
HER_F = 9.0                                                          # her mark: 9 b ahead of the actor
S13_T = 654                                                          # (HF-B) the wide of 홍련일섬 after line 16 (618 + 36)
S11_T = 608                                                          # the cut to S11: two ticks before she sinks into the iai
#                                                                      stance (609: in S10's close frame her face would dip under line 15)
S11_EYE = HR(-0.5, 1.2, 2.05)                                        # the S11 lens: 2.15 b from her head
S11_PETAL = HR(-0.1, 1.0, 0.62)                                      # the S11 petal: 1.5 b before the lens, under her face
K1 = ST(*api.CONTACT['K1'][2])                                       # the blade lock


def her_mark(mv):
    """m/mark: her at ST(0, 0, 9.0), instantly (mv/ok as the design asks; a stage whose 9-b point is outside the safe disc:
    the nearest mark that passes, last the arena-floor check), facing the actor."""
    return mv.add('mark', [cand(floor_pt(d), TP, ok) for d, ok in ((HER_F, OK), (8.0, OK), (7.0, OK), (HER_F, OKW), (7.0, OKW),
                                                                   (5.0, OKW))],
                  'Her mark 9.0 b before the actor on the stage axis (candidates in order; none passes: she stays)')


def build_cs1(W):
    s, mv = Seq('cs1'), Moves('cs1')
    e = lambda k, d=0: ev('cs1', k, d)                                # noqa: E731
    tr = C.Track('cs1', {'ST': STAGE, 'HR': BODY}, LOCK['cs1'][1], lift=LIFT, over=OVER, her=her_of('cs1'), inside=CAMIN)
    tr.cut(0, A, ST(-9.0, 2.2, 4.5), ST(0, 1.2, 4.5), 'S1 apart', ('her', 'actor'))
    tr.cut(6, B, ST(-2.6, 1.3, 0.8), K1, 'S2 clash', ('her', 'actor'))
    tr.move(10, 22, eye=ST(-1.3, 1.4, 0.8))
    tr.cut(34, A, ST(-13.0, 3.0, 4.0), ST(0, 1.0, 4.0), 'S3 pushed apart', ('her', 'actor'))
    tr.cut(84, B, ST(0.55, 1.75, -1.3), ST(0, 1.4, 9.0), 'S4 over the shoulder', ('her', 'actor?'))
    # (HF-B, HB-06) line 13 (110-161) on a close shot of her: the over-the-shoulder wide keeps the beat before it
    tr.cut(110, A, HR(0.45, 1.65, 1.7), HR(0, 1.6, 0), 'S4b her (line 13)', ('her',))
    tr.cut(180, B, ST(0, 5.0, 4.5), ST(0, 0, 4.55), 'S5 the grass', ())   # straight down, screen-up = the stage's forward
    tr.cut(220, A, HR(0.5, 1.6, -1.6), ST(0, 1.2, 0), 'S6 hat swing', ('her', 'actor'))
    tr.cut(276, B, HR(0.2, 1.45, 1.9), HR(0, 1.45, 0), 'S7 the bottle', ('her',))
    # S8: on the actor's left (the design's ST(0.5, 1.5, 1.8) is where the point of its blade comes up in the half guard
    # 350-370: 0.15 b from the lens by lane H3's manifest)
    tr.cut(340, A, ST(-0.7, 1.5, 2.1), ST(0, 1.45, 0), 'S8 the actor', ('actor',))
    tr.cut(380, B, HR(-0.3, 1.5, 1.5), HR(0, 1.5, 0), 'S9 offer, drink', ('her',))
    tr.cut(500, A, HR(0.1, 1.38, 0.95), HR(0, 1.6, 0), 'S10 under the brim', ('her',))
    # (HF-B, HB-06) line 16 (618-653): S11 is a close shot of her in the iai stance with the petal held in the foreground
    # (the video's ECU of the petal had her out of focus behind it); it holds through the draw and the slash to the line's end
    # (round V: the petal 1.5 b before the lens, at her waist: petal-sized and under her face)
    tr.cut(S11_T, B, S11_EYE, HR(0, 1.3, 0), 'S11 the petal, her iai', ('her',))
    # (the design's eye r 0.4 hides her behind the actor: 1.2 b to the right shows both, the actor near, her beyond)
    tr.cut(S13_T, A, ST(1.2, 2.1, -4.2), ST(0.2, 1.2, 4.0), 'S13 홍련일섬', ('her', 'actor?'))
    TRACKS['cs1'] = tr
    STAGED['cs1'] = [(0, 'ST', HER_F, 'S1 apart'), (10, 'ST', 1.5, 'the lock'), (50, 'ST', HER_F, 'landed'),
                     (720, 'ST', HER_F, 'the end')]
    mark = her_mark(mv)
    # ---- S1: the white mask (hides the game-mode switch, the actor's spawn and her placement)
    s.at(0, K.ovl('white', 0, 2, 2))
    # ---- S2: the lunge f 9.0 -> 1.5 (6-10), the cut stopped at K1 at 10: the gold flash, arcs 14-22, sparks every 3 t 12-30
    lunge = mv.add('lunge', [cand(floor_pt(d), glide(e('lock') - e('lunge'))) for d in (1.5, 2.2)], 'S2 the lunge to f 1.5')
    s.at(e('lunge'), lunge, snd('lunge'))
    for t in range(e('lunge'), e('lock'), 2):
        s.me(t, K.p('afterimage', len=20), y=0)
    s.at(e('lock'), gold(0, 1, 2)).st(e('lock'), K1, K.p('clash_gold')).at(e('lock'), snd('blade_lock'))
    for t in range(e('lock', 4), e('lock', 13), 2):
        s.st(t, K1, K.p('clash_arc'))
    for t in range(e('lock', 2), e('push', 1), 3):
        s.st(t, K1, K.p('clash_spark'))
    s.at(e('lock', 4), snd('arc_crackle')).at(e('lock', 8), snd('arc_crackle'))
    # ---- S3: shoved off 30-34, the leap back f 1.5 -> 9.0 (34-50, apex 1.2 b), lands low
    back = mv.add('back', [cand(floor_pt(d), leap(e('land') - e('leap'), 12), ok) for d, ok in ((HER_F, OK), (8.0, OK), (7.0, OK),
                                                                                             (HER_F, OKW), (7.0, OKW), (5.0, OKW))],
                  'S3 the leap back to her mark (apex 1.2 b)')
    s.at(e('push', 2), snd('thrown')).at(e('leap'), back).at(e('land'), snd('land_grass'), FACE_ACTOR)
    # ---- S4: line 13; S5: the grass (petals on the wind, a few dark leaves); she sheathes and takes the bottle off screen
    for i in (13, 14, 15, 16):
        assert api.LINE_AT[i][:2] == ('cs1', e(f'l{i}')), i
        say(s, e(f'l{i}'), i)
    s.st(180, ST(0, 0.8, 4.5), K.p('petals_wind')).st(200, ST(0, 0.8, 4.5), K.p('petals_wind'))
    s.st(186, ST(0, 4.0, 4.5), K.p('leaves_dark', n=8))
    # ---- S6: the hat swept off and back on (240 / 260); S9: she drinks from the bottle (464, 478); S10: the props gone 500
    s.at(e('hat_off'), snd('hat_swing')).at(e('hat_on', 2), snd('hat_swing'))
    s.at(e('drink', 6), snd('cs0_sip')).at(e('drink', 20), snd('cs0_sip'))     # (HI) the kit's sip, was a raw stand-in
    s.at(e('props_off'), api.rig('look/props/none'))
    # ---- S10: a petal drifts past BEHIND her head from frame-left (590-606, 2 b behind her: about 3 b from the lens). Round
    # V (T1-STAGE-1): 0.6 b before her face it was a 690-px blob over her face for the whole of line 15
    p1, p2 = PETAL[1], PETAL[2]
    face = lambda r, u: at_pt(HR(r, u, -2.0))                         # noqa: E731
    s.at(590, petal_summon(p1, face(1.5, 2.0)), snd('petal_drift'))
    for t in range(591, 606):
        u = (t - 590) / 16
        s.at(t, petal_move(p1, face(1.5 - 3.0 * u, 2.0 - 0.3 * u)))
    s.at(606, petal_kill(p1))
    # ---- S11: the second petal held before her, low in the close frame (610-649): a faint glint 620, its glowing line 624
    # (look cut); it turns to the live lens every tick
    pp = S11_PETAL
    s.at(610, petal_summon(p2, at_pt(pp)))
    s.at(620, f'execute {at_pt(pp)} run {K.p("glint", c=api.C_WHITE)}' if K.p('glint', c=api.C_WHITE) else None)
    s.at(624, petal_look(p2, 'cut'), snd('petal_cut'))
    # ---- S12: the draw at 642: negative 3 t, pink-white 3 + 4 t
    s.at(e('draw'), K.ovl('negative', 0, 3, 0), snd('negative')).at(e('draw', 3), K.ovl('pinkwhite', 0, 3, 4))
    # ---- S13 홍련일섬: the halves blow off (649-664), the red line across the view through the actor's chest (650), the petal
    # burst at her, the red tint, the slash; the arena turns crimson and the rig's P2 accents at 660; the dark leaves in two
    # halves on consecutive ticks (one burst of 40 is too many commands for a tick); music 2 at 676
    s.at(649, petal_look(p2, 'split'))
    for t in range(650, 664):
        u = (t - 649) / 15
        s.at(t, petal_move(p2, at_pt(HR(pp[1] - 0.9 * u, pp[2] - 1.0 * u * u, pp[3] + 0.5 * u))))
    s.at(664, petal_kill(p2))
    s.st(e('slash'), ST(0, 1.3, 0), K.p('scarlet_line', len=600, yaw=90, roll=13))
    s.at(e('slash'), K.ovl('red_tint', 0, 4, 20), snd('iai_slash'))      # (HI) the kit's 홍련일섬 recipe, was a raw stand-in
    s.me(e('slash'), K.p('petal_burst', r=20))
    s.me(e('slash', 6), K.p('leaves_dark', n=20), y=6).me(e('slash', 7), K.p('leaves_dark', n=-20), y=6)
    s.at(e('recolour'), api.arena_look('crimson'), api.rig('look/phase/p2'))
    s.at(e('music'), api.music(2))
    mv.stage(api.STAGE_FMAX['cs1'])
    head = ('CS1 (hr_design §3.2): the clash, pushed apart, the hat and the bottle, the petal, 홍련일섬, the crimson field; '
            'locked 0-720, skippable 40-560 -> 566.')
    write(W, 'cs1', s, head, api.SEQ_LEN['cs1'], track=tr, skip=True,
          start_head=[mv.ref('stage'), 'scoreboard players set #mbNoLeash mb 1', STOP, mark, FACE_ACTOR, RIG_NOW, *stands(tr),
                      *actor_spawn('cs1'), api.play('cs1')],
          cancel=[KILL_PROPS])
    # ---- the skip (the core counts the hold, calls this, then sets #sq to 565: the next tick is 566, inside S10)
    to = api.SKIP['cs1']['to']
    s10 = tr.shot_at(to)
    assert s10.name.startswith('S10') and not s10.moves, s10.name
    seek = [f'scoreboard players set @s {RIG_T} {to - 1}'] if api.rig_real() else []
    W.w('seq/cs1/skip', [
        '# The CS1 skip (@s = the body; hr_design §3.2): the black falls; under it the line and the petals go, she stands on her',
        f'# mark facing the actor with the sword sheathed, the hat on and the bottle gone (the state of tick {to}), her clip is',
        f'# moved to tick {to - 1} (the rig shows {to} at the next rig/tick: the clip keys every part there), her model put at the',
        f'# mark now (RIG_NOW), both cameras made anew on S10; seq/cs1/skipgo then sets #sq to {to - 1}. Line 15, line 16 and the',
        '# slash follow.',
        *[c for c in (K.hud('clear'), L.cam_line(None), K.ovl('black', 0, 20, 6)) if c], HUD_HOLD, KILL_PROPS, STOP, mark, FACE_ACTOR,
        RIG_NOW,
        api.rig('look/sword/sheathed'), api.rig('look/hat/worn'), api.rig('look/scabbard/hip'), api.rig('look/props/none'),
        api.rig('look/face/calm'), *seek,
        *skip_cams(tr, s10)])
    mv.write(W)


# =============================================================================================================================
# The lead-ins (hr_design §3.3): in the fight, not locked; she faces the player every tick
def build_lead60(W):
    s = Seq('lead60')
    e = lambda k, d=0: ev('lead60', k, d)                             # noqa: E731
    assert (e('rise'), e('stand'), e('brim')) == (0, 20, 40)
    # 0: the gauge back to 5 / 5 (the core arms it at this tick; the refill's effect and sound are the sequence's)
    s.at(0, snd('shield_refill')).me(0, K.p('shield_refill'))
    for t in range(1, api.SEQ_LEN['lead60'] + 1):
        s.at(t, api.rig('face/track'))
    head = 'lead60 (hr_design §3.3; after CS1): the gauge full, she straightens, the hand to the brim; G1 at its end. Not locked.'
    write(W, 'lead60', s, head, api.SEQ_LEN['lead60'], start_head=[api.play('lead60'), K.hud('warn', on=0)])


BACK_STEP, BACK_TO = 0.12, 10.0                                      # lead5: she backs off 0.12 b/t to 10 b


def warn_lines():
    """The warning banner while the gauntlet's fail is lethal (the core's #warn hr)."""
    w = K.hud('warn', on=1)
    return [f'execute if score #warn {OBJ} matches 1 run {w}'] if w else []


def build_lead5(W):
    s, mv = Seq('lead5'), Moves('lead5')
    e = lambda k, d=0: ev('lead5', k, d)                              # noqa: E731
    assert (e('stagger'), e('back'), e('refill'), e('glow'), e('brim')) == (0, 8, 60, 84, 100)
    step = mv.add('back', [DIST, f'execute if score #mbDist mb matches {round(BACK_TO * 10)}.. run return 0',
                           cand(f'at @s facing entity {PLB} feet rotated ~180 0 positioned ^ ^ ^{num(BACK_STEP)} positioned ~ {CY} ~',
                                TP, OK)],
                  f'One step of the retreat: {BACK_STEP} b away from the player while nearer than {BACK_TO} b (mv/ok)')
    for t in range(1, api.SEQ_LEN['lead5'] + 1):
        s.at(t, api.rig('face/track'))
    for t in range(e('back'), e('refill')):
        s.at(t, step)
    s.at(e('refill'), sig('refill'), snd('shield_refill'), *warn_lines()).me(e('refill'), K.p('shield_refill'))
    s.at(e('glow'), api.rig('look/blade/lilac')).at(e('glow', 14), api.rig('look/blade/off'))
    mv.write(W)
    head = ('lead5 (hr_design §3.3; the 5 % floor): the stagger, she backs off to 10 b, the gauge refilled (+ the banner), the '
            'glow, the hand to the brim; G2 at its end. Not locked.')
    write(W, 'lead5', s, head, api.SEQ_LEN['lead5'], start_head=[api.play('lead5'), K.hud('warn', on=0)],
          cancel=[])


def build_lead_re(W):
    s, mv = Seq('lead_re'), Moves('lead_re')
    e = lambda k, d=0: ev('lead_re', k, d)                            # noqa: E731
    assert (e('refill'), e('brim')) == (10, 44)
    place = mv.add('place', [DIST, 'execute if score #mbDist mb matches 70..90 run return 0']
                   + [cand(near(d), glide(8), OK) for d in (8.0, 7.0, 6.0, 9.0, 10.0)],
                   'Her place 8 b from the player on her line to them (already 7-9 b away: she stays; mv/ok)')
    s.at(0, place)
    for t in range(1, api.SEQ_LEN['lead_re'] + 1):
        s.at(t, api.rig('face/track'))
    s.at(e('refill'), sig('refill'), snd('shield_refill'), *warn_lines()).me(e('refill'), K.p('shield_refill'))
    for g in api.SEQ_ARGS['lead_re']['g']:
        W.w(f'seq/lead_re/g/{g}', [f'# lead_re {{g:"{g}"}}: the gauntlet it leads into.', sset('#sq_g', {'a8': 8, 'a13': 13}[g])])
    mv.write(W)
    head = ('lead_re {g:"a8"|"a13"} (hr_design §3.3; a restart after a pause / the revive): she stands 8 b away, the refill '
            '(+ the banner), the hand to the brim; the gauntlet g at its end. Not locked.')
    # the gauntlet arg is dispatched through storage to static references (check_mboss_pack resolves a $(...) function
    # reference only as a numeric family)
    write(W, 'lead_re', s, head, api.SEQ_LEN['lead_re'], macro=True,
          start_head=[sset('#sq_g', 0), f'$data modify storage rlk:{OBJ} seq.g set value "$(g)"']
          + [f'execute if data storage rlk:{OBJ} seq{{g:"{g}"}} run function {SEQ}/lead_re/g/{g}' for g in api.SEQ_ARGS['lead_re']['g']]
          + [api.play('lead_re'), K.hud('warn', on=0)])


# =============================================================================================================================
# The repel counter repel {at:60|5} (hr_design §3.4; clip repel 140): locked, the bars stay on
KR = ST(*api.CONTACT['KR'][2])


def build_repel(W):
    s, mv = Seq('repel'), Moves('repel')
    e = lambda k, d=0: ev('repel', k, d)                              # noqa: E731
    assert [e(k) for k in api.COUNTER_EV] == [49, 101, 129]
    at60 = f'if score #sq_at {OBJ} matches 60'
    at5 = f'if score #sq_at {OBJ} matches 5'
    tr = C.Track('repel', {'ST': STAGE, 'HR': BODY}, LOCK['repel'][1], lift=LIFT, over=OVER, her=her_of('repel'), inside=CAMIN)
    tr.cut(0, A, ST(-1.2, 0.9, 0.65), KR, 'R0 deflect / R1 blade lock', ('her', 'actor'))
    tr.move(4, 26 - 1, eye=ST(-1.0, 1.0, 0.65))
    # R2 / R3: further round to the actor's right than the design's ST(1.9, 1.5, -0.4): from there the actor, stepping in to
    # f 0.5, stands before her (shot sheet); here the seized wrist and the hilt on her hat are between the two heads
    tr.cut(26, B, ST(2.2, 1.5, 0.1), ST(0, 1.4, 0.8), 'R2 grab / R3 hat strike', ('her', 'actor'))
    tr.cut(52, A, ST(-2.2, 1.2, 2.4), ST(0, 1.2, 0.8), 'R4 two cuts', ('her', 'actor'))
    # R5: three-quarter from the actor's right (the design's head-on ST(0, 1.6, 3.6) has the actor's head before hers: she
    # stands behind it; from here her head and the hooked arm over the right shoulder are beside the actor's)
    tr.cut(68, B, ST(2.1, 1.6, 2.7), ST(0, 1.3, 1.5), 'R5 back to back', ('her', 'actor'))
    # R6: the design's frame again (HF-B, HB-01: the throw goes low over the actor's right shoulder; the step back and the
    # higher look of H2 were for the old 2.2-b arc)
    tr.cut(78, A, ST(-2.8, 0.7, 1.8), ST(0, 1.2, 2.0), 'R6 the throw', ('her', 'actor'))
    tr.cut(102, B, ST(1.6, 1.2, 4.6), ST(0, 0.6, 2.6), 'R7 over her', ('her', 'actor'))
    tr.cut(128, A, ST(-2.4, 0.8, 2.6), ST(0, 0.5, 2.8), 'R8 the kick', ('her',))
    tr.cut(132, B, ST(-5.0, 2.4, -2.0), ST(0, 1.0, 4.0), 'R9 apart (60 % only)', ('her', 'actor'))
    TRACKS['repel'] = tr
    STAGED['repel'] = [(6, 'ST', 1.3, 'the lock'), (36, 'ST', 1.1, 'the grab'), (68, 'ST', 1.2, 'back to back'),
                       (101, 'ST', 3.0, 'on her back'), (135, 'ST', 8.0, 'kicked away (60 %)'), (140, 'ST', HER_F, 'the hand-back (60 %)')]
    # ---- R0: she drops onto the raised blade: 1 b above ST(0, 0, 1.0) at tick 0, down to f 1.3 by 6; the gold wash, the gold
    # star and the light column at KR, the deflect
    drop = mv.add('drop', [cand(floor_pt(1.0), 'tp @s ~ ~1 ~')], 'R0 her place at tick 0: 1 b above ST(0, 0, 1.0), the dive\'s end')
    land = mv.add('land', [cand(floor_pt(d), glide(6)) for d in (1.3, 1.8)], 'R0 down onto the blade: f 1.3 by tick 6')
    s.at(0, gold(0, 4, 3), snd('deflect')).st(0, KR, K.p('clash_gold')).st(0, KR, K.p('light_column'))
    # ---- R1: the blade lock (sparks every 3 t, the blade ticks 8 / 16); R2: her sword wrist seized 36, f 1.1 (30-36)
    for t in range(4, 26, 3):
        s.st(t, KR, K.p('clash_spark'))
    s.at(8, snd('blade_tick')).at(16, snd('blade_tick'))
    s.at(30, mv.add('in', [cand(floor_pt(1.1), glide(6))], 'R2 she is pulled to f 1.1')).at(e('grab'), snd('grabbed'))
    # ---- R3: the hilt on her hat crown at 49: the gold star, hp1
    s.fx(e('strike'), 'hat_crown', K.p('clash_gold')).at(e('strike'), sig('hp1'), snd('hat_clash'))
    # ---- R4: the actor's two cuts (56 rising, 62 level; white: the player's cuts are never lilac), she staggers to f 1.2
    cut_at = ST(0, 1.2, 1.0)
    s.st(e('cut1'), cut_at, K.p('qi_arc', r=22, yaw=0, pitch=0, roll=40, c=api.C_WHITE)).st(e('cut1'), cut_at, raw('entity.player.attack.sweep', 0.7, 1.2))
    s.st(e('cut2'), cut_at, K.p('qi_arc', r=22, yaw=0, pitch=0, roll=0, c=api.C_WHITE)).st(e('cut2'), cut_at, raw('entity.player.attack.sweep', 0.7, 1.4))
    s.at(e('cut1'), mv.add('stagger', [cand(floor_pt(1.2), glide(8))], 'R4 she staggers to f 1.2'))
    # ---- R5: back to back (the step 68); R6: thrown over the actor's shoulder 78 -> on her back at f 3.0 at 101, the dust ring,
    # hp2. (HF-B, HB-01) a low arc (THROW_H): her clip carries her pelvis over the actor's right shoulder, the actor's hands on
    # her sword forearm to 96; the old 2.2-b apex sailed her 2 b over a bent actor
    s.st(68, ST(0, 0, 1.8), snd('step_light'))
    toss = mv.add('toss', [cand(floor_pt(d), leap(e('land') - e('throw'), THROW_H)) for d in (3.0, 2.4)],
                  f'R6 the throw: over the actor\'s shoulder to f 3.0 (apex {THROW_H / 10} b)')
    s.at(e('throw'), toss, snd('thrown'))
    s.me(e('land'), K.p('dust_ring', r=15), y=.1).at(e('land'), sig('hp2'), snd('land_back'))
    # ---- R7: lying (the petal burst at 5 % only); R8: the kick at 129 (kept cards: at 5 % it kills her in this tick and
    # death_start's kit clear would take the flash with it), hp3; she slides to f 8.0 by 135 (60 %)
    burst = K.p('petal_burst', r=10)
    s.at(110, gate(at5, [(f'execute positioned ~ ~0.3 ~ run {burst}' if burst else None), snd('petal_break')]))
    s.at(e('kick'), K.fixed('keep_on')).fx(e('kick'), 'chest', K.p('kick_flash')).at(e('kick'), K.fixed('keep_off'))
    slide = mv.add('slide', [cand(floor_pt(d), glide(6)) for d in (8.0, 7.0, 6.0)], 'R8 kicked away: she slides to f 8.0 by 135 (60 %)')
    s.at(e('kick'), snd('kick'), gate(at60, slide), sig('hp3'))
    # the lethal kick (5 %): the core kills her on hp3 in this tick (death_start -> core/stop_all -> this cancel -> the
    # ending's start): the actor is kept for the ending (lane H3: repel 129 = ending 0, no new spawn)
    if api.actor_ready():
        s.at(e('kick'), f'execute {at5} unless score {CX_FP} {OBJ} matches 1 run {sset(KEEP_FP, 1)}')
    # ---- R9 (60 % only): she rolls to her feet and stands at f 9.0 (135-140), the actor lands 139
    up = mv.add('up', [cand(floor_pt(d), glide(5), ok) for d, ok in ((HER_F, OK), (HER_F, OKW), (8.0, OKW))],
                'R9 to her feet at f 9.0 (135-140)')
    s.at(135, up).st(139, ST(0, 0, 0), snd('land_grass')).at(e('end'), FACE_ACTOR)     # (HI) the kit's landing, was raw
    mv.stage(api.STAGE_FMAX['repel'])
    mv.write(W)
    head = ('repel {at:60|5} (hr_design §3.4): the deflect, the blade lock, the grab, the hilt on her hat, two cuts, back to back, '
            'the throw, the kick; HP steps at 49 / 101 / 129; locked 0-140, the bars on.')
    write(W, 'repel', s, head, api.SEQ_LEN['repel'], macro=True, track=tr, keep=True,
          start_head=[f'$scoreboard players set #sq_at {OBJ} $(at)', sset(KEEP_FP, 0), mv.ref('stage'), 'scoreboard players set #mbNoLeash mb 1', STOP,
                      drop, FACE_ACTOR, RIG_NOW, land, *stands(tr), *actor_spawn('repel'), api.play('repel')],
          cancel=[KILL_PROPS])


# =============================================================================================================================
# The ending (hr_design §3.5; clip ending 1372 = H); the event coda follows under the same lock (the core starts seq/event
# at #sqdone)
SEAM_CUT = ('white', 0, 2, 1)      # the opening cut (ovl g, in, hold, out): fully white over ticks 0-1, out at 2
LAND_F = 9.0                       # her landing mark: 9 b from the stage origin (toward the moon, else along the stage)
END_NEAR = 4.5                     # E16: she walks in to 4.5 b
KE2, KE5 = ST(*api.CONTACT['KE2'][2]), ST(*api.CONTACT['KE5'][2])
E2_BACK = (ST(4.5, 1.8, 2.2), ST(0, 1.3, 2.7))     # (HF-B, HB-04) E2's eye / look after the pull-back with the shove (80-90)
E16_D = 1.75                                       # (HF-B) E16: the lens before her face, b
KA = [ST(*api.CONTACT[k][2]) for k in ('KA1', 'KA2', 'KA3', 'KA4')]


def build_ending(W):
    s, mv = Seq('ending'), Moves('ending')
    e = lambda k, d=0: ev('ending', k, d)                             # noqa: E731
    tr = C.Track('ending', {'ST': STAGE, 'ST2': STAGE2, 'HR': BODY}, LOCK['ending'][1], lift=LIFT, over=OVER, her=her_of('ending'), inside=CAMIN)
    tr.cut(0, A, ST(-3.2, 1.3, 2.6), ST(0, 1.1, 3.0), 'E1 she rises', ('her', 'actor'))
    tr.cut(50, B, ST(1.3, 1.5, 2.2), KE2, 'E2 clash', ('her', 'actor'))
    # (HF-B, HB-04) the shove (80-90: she to f 6.0, the actor to -0.6) left the close frame empty from 84: B pulls back and
    # pans with it, both stay in the picture to the cut
    tr.move(80, 90, eye=E2_BACK[0], look=E2_BACK[1], ease='io')
    tr.cut(94, A, ST(1.2, 0.35, 1.2), ST(0, 1.0, -0.4), 'E3 the actor (skid)', ('actor',))
    tr.cut(118, B, ST(-1.8, 0.5, 3.6), ST(0, 1.1, 1.0), 'E3 the actor (dash-cut)', ('actor',))
    tr.cut(150, A, ST(-14.0, 2.2, 5.5), ST(0, 1.0, 5.5), 'E4 the run', ('her', 'actor'))
    tr.cut(190, B, ST(1.4, 1.5, 3.3), KE5, 'E5 gold flash', ('her', 'actor'))
    tr.cut(204, A, ST(-3.5, 3.0, 2.8), ST(0, 2.0, 2.9), 'E6 aerial duel (from below)', ('her', 'actor'))
    tr.move(204, 216, look=ST(0, 6.3, 2.8))                         # the tilt up with the spring
    tr.cut(240, B, ST(2.6, 6.8, 5.6), ST(0, 6.4, 2.6), 'E6 aerial duel (level)', ('her', 'actor'))
    tr.cut(276, A, ST(-1.6, 6.2, 0.2), ST(0, 6.5, 2.8), 'E6 aerial duel (behind the actor)', ('her', 'actor'))
    tr.cut(314, B, ST(-16.0, 3.0, 2.0), HR(0, 1.74, 0), 'E7 apart', ('her',))
    tr.chase(314, 336)                                              # her arc back to the landing mark (314-334)
    tr.cut(338, A, WP(880, 206, 30), MOON, 'E8 the field', ('moon',))
    tr.cut(378, B, ST2(0.8, 1.2, 4.6), HR(0, 1.3, 0), 'E9 sheathe', ('her',))
    # (HF-B, HB-06: lines 17-22 on shots close on her) line 17 (420-477): the sheathe from 1.3 b, her face over the hands at
    # the hip, the red moon behind her head
    tr.cut(420, A, HR(0.45, 1.35, 1.35), HR(0.05, 1.42, 0), 'E9b her, sheathing (line 17)', ('her',))
    tr.cut(470, B, HR(0.2, 1.5, 1.3), HR(0, 1.6, 0), 'E10 her face', ('her',))
    tr.cut(556, A, ST2(0.4, 1.5, 1.7), ST2(0, 1.45, 0), 'E11 the actor', ('actor',))
    tr.cut(616, B, HR(0.45, 1.5, 1.95), HR(0, 1.4, 0), 'E12 turning away', ('her',))
    # line 20 (716-833): close behind her left shoulder (her back to the lens 700-760), so her look back over that shoulder
    # (760-800) turns her face to the lens
    tr.cut(700, A, HR(-0.95, 1.6, -0.85), HR(0, 1.55, 0.15), 'E12 her back, the look back', ('her',))
    tr.cut(846, B, ST2(-0.4, 1.5, 1.6), ST2(0, 1.45, 0), 'E13 the actor', ('actor',))
    tr.cut(882, A, ST2(-2.2, 1.6, -2.6), ST2(1.2, 1.2, 9.0), 'E14 the two', ('her', 'actor?'))
    # line 21 (910-1037): her face from before her (between her and the moon, the actor small beyond her), the lens drifting
    # round to her right as she looks up at the moon (990-1060); the moon over her shoulder where the line has ended
    tr.cut(910, B, HR(0.45, 1.6, 1.7), HR(0, 1.62, 0), 'E14b her (line 21)', ('her',))
    tr.move(960, 1037, eye=HR(1.0, 1.45, 1.25), ease='io')
    # E15: over her right shoulder to the moon. In her own frame (she has faced the moon since 700, wherever ST2 points); the
    # design's ST2(0.5, 1.6, 8.0) sat 1 b behind her head: the brim hid the moon (shot sheet)
    tr.cut(1038, A, HR(1.3, 1.5, -2.2), MOON, 'E15 the moon', ('her', 'moon'))
    # line 22 (1082-1209): 1.7 b from where her face comes round in the pivot (1072-1094); the lens walks back with her
    # (1094-1154, f 9.0 -> 4.5), the gesture (1160-1196) 1.7 b away
    tr.cut(1072, B, ST2(0.4, 1.6, 9.0 - E16_D), HR(0, 1.6, 0), 'E16 the greeting', ('her',))
    tr.move(1094, 1153, eye=ST2(0.4, 1.6, END_NEAR - E16_D))
    tr.cut(1212, A, HR(0.15, 1.5, 1.15), HR(0, 1.6, 0), 'E17 the hat tip', ('her',))
    TRACKS['ending'] = tr
    STAGED['ending'] = [(0, 'ST', 4.2, 'lying'), (22, 'ST', 4.6, 'up'), (54, 'ST', 2.9, 'the lunge'), (86, 'ST', 6.0, 'shoved back'),
                        (136, 'ST', 11.0, 'out of reach'), (188, 'ST', 4.0, 'the run'), (334, 'ST2', LAND_F, 'landed'),
                        (1154, 'ST2', END_NEAR, 'the greeting')]
    # ---- E1: the hard cut (a white flash at tick 0: under it the game-mode switch, the actor, her place on her back at f 4.2);
    # she kips up 6-22 to f 4.6, raises the sword (the violet glow 30-48)
    lie = mv.add('lie', [cand(floor_pt(d), TP) for d in (4.2, 3.4, 2.6)], 'E1 her place at tick 0: on her back at f 4.2')
    s.at(0, K.ovl(*SEAM_CUT))
    s.at(e('up'), mv.add('up', [cand(floor_pt(4.6), glide(16))], 'E1 up to f 4.6'))
    s.at(e('raise', 2), api.rig('look/blade/violet'), snd('blade_charge')).at(48, api.rig('look/blade/off'))
    # ---- E2: both lunge (50-54, she to f 2.9), the brim grazed 52, the lock at KE2 56-80 (sparks every 3 t), the burst at 70,
    # shoved back to f 6.0 (80-86)
    s.at(e('lunge'), mv.add('lunge', [cand(floor_pt(d), glide(4)) for d in (2.9, 3.4)], 'E2 the lunge to f 2.9'))
    s.fx(e('graze'), 'hat_crown', K.p('clash_spark'))
    s.at(e('lock'), snd('blade_lock'))       # (HI) the kit's blade lock (as CS1's K1), was a raw stand-in
    for t in range(e('lock'), e('shove'), 3):
        s.st(t, KE2, K.p('clash_spark'))
    s.at(e('burst'), gold(0, 1, 2), snd('bolt_crackle')).st(e('burst'), KE2, K.p('clash_gold'))
    for t in (e('burst'), e('burst', 2), e('burst', 4)):
        s.st(t, KE2, K.p('clash_arc'))
    s.at(e('shove'), mv.add('shove', [cand(floor_pt(d), glide(6)) for d in (6.0, 5.0)], 'E2 shoved back to f 6.0'))
    # ---- E3: the actor skids (steps 96 / 100), dash-cuts into the air (120-124: the white crescent and the afterimage at it);
    # she springs back out of reach to f 11 (116-136)
    s.st(96, ST(0, 0, -1.0), snd('grass_step')).st(100, ST(0, 0, -1.4), snd('grass_step'))
    s.at(e('back'), mv.add('away', [cand(floor_pt(d), leap(20, 12)) for d in (11.0, 10.0, 9.0, 8.0)], 'E3 she springs back to f 11'))
    s.st(120, ST(0, 1.2, 0.5), raw('entity.player.attack.sweep', 0.7, 1.3))
    s.st(121, ST(0, 1.2, 0.8), K.p('qi_arc', r=26, yaw=0, pitch=0, roll=0, c=api.C_WHITE)).st(121, ST(0, 0, 0.2), K.p('afterimage', len=20))
    # ---- E4: both run in (150-188; she f 11 -> 4.0 at 0.18 b/t), steps every 4 t; E5: cut meets cut at KE5 at 190 (gold)
    s.at(e('run'), mv.add('run', [cand(floor_pt(d), glide(38)) for d in (4.0, 4.6)], 'E4 the run to f 4.0'))
    for t in range(e('run'), 188, 4):
        s.at(t, snd('grass_step'))
    s.at(e('clash'), gold(0, 6, 6), snd('clash_big')).st(e('clash'), KE5, K.p('clash_gold'))
    # ---- E6: the aerial duel: both spring up 204-216 (she to ST(0, 6.0, 3.6)), the cuts at 228 / 262 / 286, the lock 298-304
    air = lambda r, u, f, t: cand(at_pt(ST(r, u, f)), glide(t))       # noqa: E731
    s.at(e('rise'), mv.add('rise', [air(0, 6.0, 3.6, 12)], 'E6 up to ST(0, 6.0, 3.6)'))
    s.at(222, mv.add('a1', [air(0, 6.0, 3.2, 6)], 'E6 the passing cut: in to f 3.2'))
    s.at(250, mv.add('a2', [air(0, 6.4, 3.4, 12)], 'E6 the overhead cut: up to u 6.4'))
    s.at(276, mv.add('a3', [air(0, 6.0, 3.3, 10)], 'E6 the big one'))
    for i, k in enumerate(('a1', 'a2', 'a3', 'a4')):
        s.st(e(k), KA[i], K.p('clash_gold'))
        if k != 'a4':
            s.st(e(k), KA[i], snd('air_slash'))
    s.st(e('a2'), KA[1], snd('air_clash'))
    s.at(e('a3'), gold(0, 3, 6)).st(e('a3'), KA[2], snd('air_white'))
    # ---- E7: pushed off 304, she flies back in an arc to her landing mark (314-334): 9 b from the stage origin toward the
    # moon when that passes mv/ok, else along the stage. ST2 = the same origin facing that mark (made at 314)
    mp = api.MOON_POS
    mk2 = mv.add('stage2', [
        f'kill @e[type=minecraft:marker,tag={STAGE2_T}]',
        f'execute at {STAGE} run summon minecraft:marker ~ ~ ~ {{Tags:{tags(STAGE2_T)}}}',
        f'execute as {STAGE2} at @s rotated as {STAGE} run tp @s ~ ~ ~ ~ 0',
        f'execute as {STAGE2} at @s facing {api.xyz((mp[0], CY, mp[2]), 3)} positioned ^ ^ ^{num(LAND_F)} if {OK} at @s facing '
        f'{api.xyz((mp[0], CY, mp[2]), 3)} run tp @s ~ ~ ~ ~ 0',
        f'execute store result storage rlk:{OBJ} seq.face.yaw float 0.01 run data get entity {STAGE2} Rotation[0] 100'],
        'E7 ST2: the stage origin facing her landing mark (toward the moon when that point passes mv/ok, else as ST)')
    fly = mv.add('fly', [cand(floor_pt(d, frame='ST2'), leap(20, 40)) for d in (LAND_F, 8.0, 7.0)],
                 'E7 the arc to her landing mark, 9 b from the stage origin (apex 4 b over the path)')
    s.at(e('fly'), mk2, fly).st(316, ST(0, 3.0, 3.0), K.p('petals_wind'))
    s.st(330, ST(0, 0, 0), snd('land_far')).at(e('land'), snd('land_far'))
    # ---- E8: she rises and turns to the actor (338-350); the actor is turned to ST2 (char/cine/face, 12 t)
    face2 = [f'function rlk:char/cine/face with storage rlk:{OBJ} seq.face'] if api.actor_ready() else []
    s.at(338, *face2)
    tpl = mv.turn('turn_pl', f'entity {PLB} feet', 15, 'the avatar')
    for t in range(338, 350):
        s.at(t, tpl)
    s.at(350, FACE_ACTOR2)
    # ---- E9: the scabbard, the sheathe (click 452), line 17 + music 3 at 420, a big petal crosses the frame 430-438
    for i in range(17, 24):
        assert api.LINE_AT[i][:2] == ('ending', e(f'l{i}')), i
        say(s, e(f'l{i}'), i)
    assert e('music') == e('l17')
    s.at(e('music'), api.music(3)).at(e('sheathed'), snd('sheathe_click'))
    # (round V, T1-STAGE-1: line 17 is up: the petal crosses BEHIND her, 3.2 b before the lens of the close shot E9b)
    p3, c9 = PETAL[3], tr.shot_at(430).cam
    s.at(430, petal_summon(p3, before_cam(c9, 1.5, 0.55, 3.2)))
    for t in range(431, 446):
        u = (t - 430) / 16
        s.at(t, petal_move(p3, before_cam(c9, 1.5 - 3.0 * u, 0.55 - 0.3 * u, 3.2)))
    s.at(446, petal_kill(p3))
    # ---- E12: she turns away toward the moon (650-700, <= 4 deg / t; the feet step)
    tm = mv.turn('turn_moon', api.xyz(mp, 3), 4, 'the moon (api.MOON_POS)')
    for t in range(e('turn'), e('turn', 50)):
        s.at(t, tm)
    s.at(e('turn', 8), snd('grass_step')).at(e('turn', 28), snd('grass_step'))
    # ---- E15: the moon gaze (the halo brighter 980-1060, the heart petals 1020); E16: the pivot back (1072-1094, <= 9 deg / t),
    # the walk-in f 9.0 -> 4.5 (1094-1154, 0.075 b/t); E17: the hat tip (the heart petals 1300)
    s.at(980, halo(True)).at(1060, halo(False)).me(1020, K.p('petals_heart'))
    tp9 = mv.turn('turn_back', f'entity {PLB} feet', 9, 'the avatar')
    for t in range(e('pivot'), e('pivot', 22)):
        s.at(t, tp9)
    s.at(e('walk'), FACE_ACTOR2, mv.add('walk', [cand(floor_pt(d, frame='ST2'), glide(e('stop') - e('walk'))) for d in (END_NEAR, 5.5)],
                                        f'E16 the walk-in to {END_NEAR} b (0.075 b/t)'))
    for t in range(e('walk'), e('stop'), 12):
        s.at(t, snd('grass_step'))
    s.me(e('pull', 10), K.p('petals_heart'))
    mv.stage(api.STAGE_FMAX['ending'])
    mv.write(W)
    head = ('The ending (hr_design §3.5): she rises, the clash, the aerial duel, the landing, the sheathe, lines 17-23, the hat '
            'tip; H at its end; locked from tick 0 into the coda.')
    write(W, 'ending', s, head, api.SEQ_LEN['ending'], track=tr, fin=False,
          start_head=[mv.ref('stage'), STOP, lie, FACE_ACTOR, RIG_NOW, *stands(tr), *actor_spawn('ending', carry=True), api.play('ending')],
          cancel=[KILL_PROPS] + halo(False))


# =============================================================================================================================
# The event coda (PLAN §7.3.2, unchanged; 120 t from H, both branches on #hrEv): the thrown sword / the moonlight orb, the
# leave, the grant and the title at E56 (api.ev_apply / ev_title), the black at E110. New (hr_design §3.5): it runs under the
# ending's lock: camera B static at ST2(0.55, 1.75, -1.3) looking at her, the actor's clip `coda`; release at E118.
SWORD_T, ORB_T = 'rlk_hr_ev_sword', 'rlk_hr_ev_orb'
SWORD = f'@e[type=minecraft:item_display,tag={SWORD_T},limit=1]'
ORB = f'@e[type=minecraft:marker,tag={ORB_T},limit=1]'
FLY = (api.EV_T['toss'], api.EV_T['beam'])          # E30 -> E44: the sword's flight (14 t)
ORB_FLY = (api.EV_T['toss'], api.EV_T['arrive'])    # E30 -> E42: the orb's float (12 t)
SWORD_R = round(api.ITEM_SWORD_LEN / 2 / api.ITEM_SWORD_SCALE, 3)   # item_sword: max radius from the model centre, b at display scale 1
TH0, TH1 = 40.0, -180.0                              # the end-over-end turn: tip forward-up at the toss -> tip down (scabbard down)
S0 = S1 = api.ITEM_SWORD_SCALE                       # display scale: the rig's own at the hand; she is player-size, no shrink in flight
# E30 the toss: the item's centre from her right hand (^left ^up ^forward), measured by the rig builder at the toss (S2d)
TOSS_OFF = tuple((api.rig_manifest().get('item_sword') or {}).get('toss_offset') or (0, 0.13, 0.11))
CODA_CUT = 4                                         # the coda's camera goes live at E4 (prepared from E1: cam.PRE)
CODA_BLACK = ('black', 6, 16, 0)                     # (HF-B, HB-05) the coda's black at E110: opaque E116, the hand-back E118


def _q(axis, deg):
    s, c = math.sin(math.radians(deg) / 2), math.cos(math.radians(deg) / 2)
    return [s if axis == 'x' else 0.0, s if axis == 'y' else 0.0, s if axis == 'z' else 0.0, c]


def _qmul(a, b):
    x1, y1, z1, w1 = a
    x2, y2, z2, w2 = b
    return [w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2, w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2]


def sword_rot(th):
    """left_rotation of the thrown sword: the model's diagonal (+X,+Y; after the display's own Ry180: (-X,+Y)) turned onto +Y
    (z -45 deg), then tilted th about the display's X (0 tip up, 90 tip forward along the facing, -180 tip down)."""
    return _qmul(_q('x', th), _q('z', -45.0))


def tfm(q, s):
    """A display transformation compound: left_rotation q, uniform scale s, no translation."""
    f = lambda v: (f'{v:.5f}'.rstrip('0').rstrip('.') or '0') + 'f'   # noqa: E731
    return f'{{translation:[0f,0f,0f],left_rotation:[{",".join(f(v) for v in q)}],scale:[{f(s)},{f(s)},{f(s)}],right_rotation:[0f,0f,0f,1f]}}'


def tf(q, s):
    """The data-merge compound: the transformation interpolated over 1 t."""
    return f'{{start_interpolation:0,interpolation_duration:1,transformation:{tfm(q, s)}}}'


def homing(ent, k, n, apex_mb, ymin_mb, target):
    """Place `ent` at P0 + (T - P0) * k / n + (0, apex) (milliblocks, P0 stored at the launch in #sq_x0 / y0 / z0), T = the point
    `target` (an execute chain) this tick, its centre clamped to >= ymin; a helper marker carries the point (tp keeps the yaw)."""
    out = [f'execute {target} run summon minecraft:marker ~ ~ ~ {{Tags:{tags(HELP_T)}}}']
    for i, a in enumerate('xyz'):
        out.append(f'execute store result score #sq_{a} {OBJ} run data get entity {HELP} Pos[{i}] 1000')
    out += [f'scoreboard players set #sq_k {OBJ} {k}', f'scoreboard players set #sq_n {OBJ} {n}']
    for a in 'xyz':
        out += [f'scoreboard players operation #sq_{a} {OBJ} -= #sq_{a}0 {OBJ}', f'scoreboard players operation #sq_{a} {OBJ} *= #sq_k {OBJ}',
                f'scoreboard players operation #sq_{a} {OBJ} /= #sq_n {OBJ}', f'scoreboard players operation #sq_{a} {OBJ} += #sq_{a}0 {OBJ}']
    if apex_mb > 0:
        out.append(f'scoreboard players add #sq_y {OBJ} {apex_mb}')
    out.append(f'execute if score #sq_y {OBJ} matches ..{ymin_mb - 1} run scoreboard players set #sq_y {OBJ} {ymin_mb}')
    for i, a in enumerate('xyz'):
        out.append(f'execute store result entity {HELP} Pos[{i}] double 0.001 run scoreboard players get #sq_{a} {OBJ}')
    out += [f'execute at {HELP} run tp {ent} ~ ~ ~', f'kill @e[type=minecraft:marker,tag={HELP_T}]']
    return out


def store_p0(ent):
    return [f'execute store result score #sq_{a}0 {OBJ} run data get entity {ent} Pos[{i}] 1000' for i, a in enumerate('xyz')]


def build_event(W):
    s, mv = Seq('event'), Moves('event')
    E = api.EV_T
    item, buff = f'if score {api.EV_FP[0]} {OBJ} matches {api.EV_BRANCH["item"]}', f'if score {api.EV_FP[0]} {OBJ} matches {api.EV_BRANCH["buff"]}'
    # ---- the camera: the stand the ending did not end on (X) goes live at E4 (the other, Y, holds the ending's last frame
    # until then). (HF-B, HB-06) Line 24 / 25 (E4-E51) on shots close on her: her face from before her (E4-E29: the glint
    # along the scabbard), then over her right shoulder, the gift flying from her hand to the actor (E30-E51); from E52 (the
    # line cleared) the design's static shot over the actor's right shoulder (the grant, the title, the black)
    tr = C.Track('event', {'ST': STAGE, 'ST2': STAGE2, 'HR': BODY}, LOCK['event'][1], lift=LIFT, over=OVER, her=her_of('event'), inside=CAMIN)
    y_cam = tracks_built('ending').shots[-1].cam
    x_cam = B if y_cam == A else A
    coda_eye, coda_look = ST2(0.55, 1.75, -1.3), HR(0, 1.3, 0)
    first = tr.cut(CODA_CUT, x_cam, HR(-0.45, 1.6, 1.6), HR(0, 1.55, 0), 'coda: her (line 24 / 25)', ('her',))
    tr.cut(api.EV_T['toss'], y_cam, HR(0.6, 1.75, -1.2), HR(0, 1.2, 4.0), 'coda: over her shoulder, the gift', ('her', 'actor'))
    tr.cut(api.EV_T['line_clear'], x_cam, coda_eye, coda_look, 'coda', ('her',))
    TRACKS['event'] = tr
    # the stage when the coda starts by itself (a test, a core that cancelled the ending): made here, ST2 = ST, and camera
    # A is put on the coda's shot too (nothing to hold over)
    alone = mv.add('alone', [mv.stage(api.STAGE_FMAX['ending']),
                             f'execute at {STAGE} run summon minecraft:marker ~ ~ ~ {{Tags:{tags(STAGE2_T)}}}',
                             f'execute as {STAGE2} at @s rotated as {STAGE} run tp @s ~ ~ ~ ~ 0',
                             sset(CX_FP, 0), sset(HELD_FP, 0), L.cam('kill'),
                             *tr.spawn(HELP, HELP_SUMMON, first={A: first, B: first}),
                             f'scoreboard players set {L.CAM_ID[0]} {L.CAM_ID[1]} {x_cam}'],
                   'The coda without the ending before it: its own stage (ST2 = ST) and stands, its first shot\'s stand live at once')
    # E0: she faces the avatar; the branch's clip (ev_give / ev_toast) from the ending's last pose; the lift / chime
    s.at(0, FACE_PLB, gate(item, [api.play('ev_give'), snd('ev_lift')]),
         gate(f'unless score {api.EV_FP[0]} {OBJ} matches {api.EV_BRANCH["item"]}', api.play('ev_toast')), gate(buff, snd('ev_chime')))
    # E4 the line (24 item / 25 buff; api.EVENT['lines']), cleared at E52 (before the title)
    if api.EVENT['lines']:
        say(s, E['line'], 24, item)
        say(s, E['line'], 25, buff)
        s.at(E['line_clear'], K.hud('clear'), L.cam_line(None))
    # item: E12 the glint along the scabbard; E30 the toss: the display at the hand (scale api.ITEM_SWORD_SCALE, the rig's
    # scabbard hidden by the clip), its yaw toward the target, the end-over-end turn and the arc (apex 1.2 b) to 0.9 b before the
    # avatar's chest along its facing (re-aimed every tick), never below the floor; E44 upright (scabbard down), the moonbeam,
    # bobbing; E50-E55 sinking into the hand (S1 -> 0.15); E56 gone
    glint = K.p('ev_glint')
    if glint:
        s.at(E['present'], gate(item, [api.rig('anchor/hand_r'), f'execute at {ANCHOR} run {glint}']))
    s.at(E['present'], gate(item, snd('ev_chime')))
    target = f'at {PLB} rotated as {PLB} rotated ~ 0 positioned ^ ^1.1 ^0.9'
    q0 = sword_rot(TH0)
    item_nbt = (f'{{Tags:{tags(EV_T, SWORD_T)},item:{{id:"{api.ITEM_VANILLA}",count:1,components:{{"minecraft:item_model":"{api.ITEM_MODEL}"}}}},'
                f'item_display:"none",billboard:"fixed",teleport_duration:1,interpolation_duration:1,view_range:2f,'
                f'brightness:{{block:13,sky:15}},transformation:{tfm(q0, S0)}}}')
    t0, t1 = FLY
    s.at(t0, gate(item, [f'kill @e[type=minecraft:item_display,tag={SWORD_T}]', api.rig('anchor/hand_r'),
                         f'execute at {ANCHOR} rotated as @s rotated ~ 0 positioned {" ".join("^" + (num(v) if abs(v) > 1e-9 else "") for v in TOSS_OFF)} '
                         f'run summon minecraft:item_display ~ ~ ~ {item_nbt}',
                         f'execute as {SWORD} at @s facing entity {PLB} feet run tp @s ~ ~ ~ ~ 0', *store_p0(SWORD), snd('ev_toss')]))
    n = t1 - t0
    for k in range(1, n + 1):
        u = k / n
        sc = S0 + (S1 - S0) * u
        lines = homing(SWORD, k, n, round(1200 * 4 * u * (1 - u)), round((CY + SWORD_R * sc + .06) * 1000), target)
        lines.append(f'data merge entity {SWORD} {tf(sword_rot(TH0 + (TH1 - TH0) * u), sc)}')
        trl = K.p('ev_trail')
        if trl and k < n:
            lines.append(f'execute at {SWORD} run {trl}')
        s.at(t0 + k, gate(item, lines))
    beam = K.p('ev_beam', h=80, t=6)
    s.at(t1, gate(item, [(f'execute at {SWORD} run {beam}' if beam else None), snd('ev_beam')]))
    hold = E['grant'] - 6                                  # E50: the sink starts
    for t in range(t1 + 1, hold):                         # bobbing over the arrival point (+-0.05 b)
        f = lambda tt: .05 * math.sin((tt - t1) / (hold - t1) * 2 * math.pi)   # noqa: E731
        s.at(t, gate(item, [f'execute as {SWORD} at @s run tp @s ~ ~{num(f(t) - f(t - 1))} ~']))
    s.at(hold, gate(item, store_p0(SWORD)))
    n2 = E['grant'] - hold
    for k in range(1, n2 + 1):                            # E50-E55 sinking into the hand (scale S1 -> 0.15)
        sc = S1 + (.15 - S1) * k / n2
        s.at(hold + k - 1, gate(item, homing(SWORD, k, n2, 0, round((CY + SWORD_R * sc + .04) * 1000), f'at {PLB} rotated as {PLB} rotated ~ 0 positioned ^ ^1.0 ^0.35')
                                 + [f'data merge entity {SWORD} {tf(sword_rot(TH1), sc)}']))
    # buff: E14-E29 the moonlight cup in her palm; E30 the orb leaves the palm and floats 12 t to the avatar's chest (E42: gone,
    # the moonbeam and the wind onto it)
    palm = K.p('ev_palm')
    if palm:
        for t in range(E['present'] + 2, E['toss']):
            s.at(t, gate(buff, [api.rig('anchor/hand_l'), f'execute at {ANCHOR} positioned ~ ~0.1 ~ run {palm}']))
    o0, o1 = ORB_FLY
    s.at(o0, gate(buff, [f'kill @e[type=minecraft:marker,tag={ORB_T}]', api.rig('anchor/hand_l'),
                         f'execute at {ANCHOR} positioned ~ ~0.1 ~ run summon minecraft:marker ~ ~ ~ {{Tags:{tags(EV_T, ORB_T)}}}',
                         *store_p0(ORB), snd('ev_toss')]))
    for k in range(1, o1 - o0 + 1):                     # E31-E42: the last step lands on the avatar's chest
        u = k / (o1 - o0)
        lines = homing(ORB, k, o1 - o0, round(300 * 4 * u * (1 - u)), (CY + 1) * 1000, f'at {PLB} positioned ~ ~1.1 ~')
        if palm:
            lines.append(f'execute at {ORB} run {palm}')
        s.at(o0 + k, gate(buff, lines))
    bb, wind = K.p('ev_beam', h=80, t=10), K.p('ev_wind', r=15)
    s.at(o1, gate(buff, [f'kill @e[type=minecraft:marker,tag={ORB_T}]', (f'execute at {PLB} run {bb}' if bb else None),
                         (f'execute at {PLB} run {wind}' if wind else None), snd('ev_beam')]))
    # both: E34 the leave (clip ev_leave, the petals and wind at her chest), E40 hidden; E56 the grant + the title, the take
    # effect, the petals round the avatar every 4 t to E108; E110 the black (the original's fade) held to the return
    s.at(E['leave'], api.play('ev_leave'), snd('ev_leave')).me(E['leave'], K.p('ev_leave'))
    s.at(E['hide'], api.rig('state/hidden'))
    s.at(E['grant'], f'kill @e[type=minecraft:item_display,tag={SWORD_T}]', api.ev_apply(), api.ev_title(),
         gate(item, [(f'execute at {PLB} positioned ~ ~1.1 ~ run {K.p("ev_take", c=1)}' if K.p('ev_take', c=1) else None), snd('ev_take_i')]),
         gate(buff, [(f'execute at {PLB} positioned ~ ~1.1 ~ run {K.p("ev_take", c=2)}' if K.p('ev_take', c=2) else None), snd('ev_take_b')]))
    pet = K.p('ev_petals', n=2)
    if pet:
        for t in range(E['grant'], E['black'] - 1, 4):
            s.at(t, f'execute at {PLB} positioned ~ ~0.8 ~ run {pet}')
    # (HF-B, HB-05) the black is fully opaque before the hand-back at E118 (LOCK['event']): in 6 from E110 = opaque from E116,
    # held to E132 as before; it starts as the item / buff title's own time ends (E56 + 54)
    s.at(E['black'], K.ovl(*CODA_BLACK))
    mv.write(W)
    head = ('The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, '
            'the grant at E56, the black at E110; under the ending\'s lock until E118.')
    write(W, 'event', s, head, api.SEQ_LEN['event'], track=tr, chain=True,
          start_head=[f'execute unless entity {STAGE2} run {alone}', STOP, *actor_spawn('coda', carry=True, chained=True)],
          cancel=[f'kill @e[tag={EV_T}]'])


# ---- services -----------------------------------------------------------------------------------------------------------------
def _events(name):
    """The clip events of a sequence on its own clock (intro: intro_end's shifted by api.SKIP_T, prefixed end_; event: api.EV_T)."""
    if name == 'event':
        return dict(api.EV_T)
    out = dict(api.CLIPS[api.SEQ_CLIPS[name][0]][2])
    if name == 'intro':
        out.update({f'end_{k}': api.SKIP_T + v for k, v in api.CLIPS['intro_end'][2].items()})
    return out


_LIB = []


def _with_lib(build):
    """The shared seq/lib/** is written with the first service of a build."""
    def run(W):
        if W not in _LIB:
            _LIB.append(W)
            lib(W)
        build(W)
    return run


def tracks_built(name):
    """The track of a sequence built earlier in this build (api.SEQS order), or built now without files."""
    if name not in TRACKS:
        _BUILD[name](_NullWriter())
    return TRACKS[name]


class _NullWriter:
    """A writer that writes nothing (tracks(): the tables without the files)."""

    def w(self, rel, body):
        return None


def tracks():
    """{sequence: cam.Track} of the locked sequences (and STAGED), built without writing a file (tests, the shot sheets)."""
    if len(TRACKS) < len(LOCK):
        W = _NullWriter()
        for n in api.SEQS:
            _BUILD[n](W)
    return TRACKS


_BUILD = {'intro': build_intro, 'cs1': build_cs1, 'lead60': build_lead60, 'repel': build_repel, 'lead5': build_lead5,
          'lead_re': build_lead_re, 'ending': build_ending, 'event': build_event}
SERVICES = [api.Service(n, api.SEQ_CLIPS[n], _with_lib(_BUILD[n]), _events(n), dict(api.SEQ_ARGS.get(n, {}))) for n in api.SEQS]
assert [s.name for s in SERVICES] == list(api.SEQS)
