"""Sequences of 홍련 (Scarlet): CS0 intro (+ the skip), CS1, SQ1, the counter cinematic repel {at}, the lead-ins lead_down /
lead_stand {g}, CS4 ending and the event coda (S:hr/PLAN.md §3.0-§3.8, §7.3.2). OWNER: S2b (S:hr/contract.md §1, §3.5, §3.7).

Contract (api.Service): SERVICES = one api.Service per api.SEQS name; build(W) writes only under seq/<name>/ (W =
api.Writer('S2b', api.OWN['S2b'])): the entry points seq/<name>/{start,tick,cancel} (+ seq/intro/skip, + the macro helpers
seq/lead_stand/g/<g>) and their internal files seq/<name>/k/<t> (the lines of tick t) and seq/<name>/b/<a>_<b> (a dispatch
bucket), seq/ending/land and seq/ending/turn_moon. The core (S3) sets #sq hr 0 and calls start (@s = the body, at it), then
adds 1 to #sq and calls tick every tick; rig/tick runs after the module logic, so the clip shows tick e when #sq = e and every
beat below sits on its clip event (api.ev, plus a fixed offset where the plan's tick is not a contract event). A sequence sets
#sqdone hr 1 at its length (api.SEQ_LEN). cancel has no executor, is idempotent and removes only what the sequence made.

Division of work (contract §3.5): the core owns invulnerability, cine, the bars, the shield (arm / refill), floors, the phase
switch, the HP steps, the kill, the death finish and the intro's skip input; a sequence signals it through #sq_sig hr =
api.SIG in the beat's tick (repel hp1 / hp2 / hp3 at api.COUNTER_EV, the lead-ins' refill) and never calls core functions.
A sequence owns its clips (api.play), rig looks / anchors / facing (api.rig), the kit's effects, props, sounds, lines,
overlays and the warning banner (api.K, '' while the kit manifest is missing: lines are dropped, never emitted empty), the
look requests (api.arena_look), the music line of its music event (api.music), the title (mboss_lib.title at intro_end draw),
push rings (mboss_lib.push_ring, no damage) and the body moves (mboss/mv/glide | leap at points checked with mboss/mv/ok;
face/* through the rig). The event coda grants and titles only through api.ev_apply() / api.ev_title() at E56.

Staging frame: each sequence keeps the player's position and yaw at its tick 0 in the marker rlk_hr_stage ("the player's
right / front" below). World entities a sequence makes: rlk_hr_stage, the kit prop cards (petals: rlk_hr_sqp), the event's
thrown sword (item_display of api.ITEM_MODEL) / moonlight orb (marker), all tagged rlk_room rlk_mb_aux; the event's also
rlk_hr_ev. Summoned, then rotated (summon ignores the execute rotation); every point a body move or a prop takes is on the
arena floor (y api.CY) or clamped above it.
"""
import math

from . import api

L, K = api.L, api.K
OBJ, NS = api.OBJ, api.NS
CY = api.CY
SEQ = f'{NS}seq'
BODY = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'            # the framework body (mboss/body)
PLB = '@e[tag=rlk_body,limit=1]'                                     # the player's body (avatar in shoulder view, else the player)
PL = '@a[tag=player,limit=1]'
STAGE_T = api.TAGS['stage']
STAGE = f'@e[type=minecraft:marker,tag={STAGE_T},limit=1]'
ANCHOR = f'@e[type=minecraft:marker,tag={api.TAGS["anchor"]},limit=1]'
EV_T = api.TAGS['ev']
PROP_T = 'rlk_hr_sqp'                                                # S2b's kit prop cards (the petals)
HELP_T = 'rlk_hr_sqh'                                                # a one-tick helper marker (killed in the same function)
HELP = f'@e[type=minecraft:marker,tag={HELP_T},limit=1]'
OK = 'function rlk:mboss/mv/ok'
DIST = 'function rlk:mboss/mv/dist'                                  # -> #mbDist mb (tenths, horizontal, @s -> the player)
FLOOR = f'positioned ~ {CY} ~'


def num(v):
    return L.num(v, 3)


def tags(*extra):
    return '[' + ','.join(f'"{t}"' for t in ('rlk_room', 'rlk_mb_aux') + extra) + ']'


def sq(t):
    return f'execute if score #sq {OBJ} matches {t}'


def ev(clip, e, d=0):
    """The played tick of a clip event (+ an offset for a plan tick that is not a contract event)."""
    return api.ev(clip, e) + d


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
        """A kit line at her (chest height), rotated as her."""
        if cmd:
            self.at(t, f'execute positioned ~ ~{num(y)} ~ rotated as @s rotated ~ 0 run {cmd}')
        return self


# F2 (HR-29): the cutscenes the footage plays without the HUD (CS0, CS1, CS4 + the event coda; cutscenes.md §12) hold the
# player's actionbar HUD on every tick (hudHold 2 as the skip prompt does; player/hud/tick rests while it is >= 1). CS2 / CS3,
# SQ1 and the lead-ins keep it (the footage shows it there). F2 round 1 (VF2-1-02): the hold only stops new sends, and the
# game keeps the last actionbar on screen ~60 t, so each of these sequences also blanks it once at its start (as the skip
# prompt's end and the other kits' banner ends do); CS0's skip prompt at 20 then replaces the blank.
HUD_OFF = ('intro', 'cs1', 'ending', 'event')
HUD_HOLD = 'scoreboard players set @a[tag=player] hudHold 2'
HUD_BLANK = 'title @a[tag=player] actionbar ""'


def write(W, name, s, head, length, start_head=(), cancel=(), macro=False):
    """seq/<name>/{start,tick,cancel} + k/<t> + b/<a>_<b>. start = its head lines, #sqdone 0, then the tick-0 lines."""
    base = f'{SEQ}/{name}'
    hold = [HUD_HOLD] if name in HUD_OFF else []
    blank = [HUD_BLANK] if name in HUD_OFF else []
    W.w(f'seq/{name}/start', [f'# {head}', f'# Start (@s = the body, at it; #sq {OBJ} = 0){" — macro" if macro else ""}.',
                              *[c for c in start_head if c], f'scoreboard players set #sqdone {OBJ} 0', *hold, *blank,
                              *s.t.get(0, [])])
    ticks = sorted(t for t in s.t if t > 0)
    assert all(t <= length for t in ticks), (name, max(ticks), length)
    for t in ticks:
        W.w(f'seq/{name}/k/{t}', [f'# {name} at #sq {t} (@s = the body).', *s.t[t]])
    leaf = lambda ts: [f'{sq(t)} run return run function {base}/k/{t}' for t in ts]
    tick = [f'# {head}', f'# Tick (@s = the body; #sq {OBJ} 1.. = the clip tick shown this game tick); #sqdone at {length}.',
            f'{sq(f"{length}..")} run scoreboard players set #sqdone {OBJ} 1', *hold]
    if len(ticks) <= 12:
        tick += leaf(ticks)
    else:
        n = 10
        for i in range(0, len(ticks), n):
            g = ticks[i:i + n]
            W.w(f'seq/{name}/b/{g[0]}_{g[-1]}', [f'# {name}: the ticks {g[0]}..{g[-1]}.'] + leaf(g))
            tick.append(f'{sq(f"..{g[-1]}")} run return run function {base}/b/{g[0]}_{g[-1]}')
    W.w(f'seq/{name}/tick', tick)
    W.w(f'seq/{name}/cancel', [f'# {head}', '# Cancel (no executor; idempotent): what this sequence made.',
                               f'kill @e[type=minecraft:marker,tag={STAGE_T}]', f'kill @e[type=minecraft:marker,tag={HELP_T}]',
                               *[c for c in cancel if c]])


# ---- common pieces ----------------------------------------------------------------------------------------------------------
def stage(toward_her=False):
    """The staging marker at the player's feet with the player's yaw (summoned, then rotated). toward_her: the yaw toward her
    (the sequences that turn the player to her at tick 0: the player's yaw after that one-shot facing)."""
    rot = 'facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet' if toward_her else f'rotated as {PLB}'
    return [f'kill @e[type=minecraft:marker,tag={STAGE_T}]',
            f'execute at {PLB} run summon minecraft:marker ~ ~ ~ {{Tags:{tags(STAGE_T)}}}',
            f'execute as {STAGE} at @s {rot} run tp @s ~ ~ ~ ~ 0']


def gate(cond, cmds):
    """cmds behind an execute condition (an 'execute ...' line gets the condition inserted)."""
    out = []
    for c in cmds if isinstance(cmds, (list, tuple)) else [cmds]:
        if c:
            out.append(f'execute {cond} {c[8:]}' if c.startswith('execute ') else f'execute {cond} run {c}')
    return out


def face_player_fight():
    """One-shot facing of the player toward her while fighting: pulled to their own feet at once (#pullFace 1)."""
    return f'execute positioned as {PLB} run function rlk:mboss/pull/start {{t:0}}'


def face_player_dying():
    """One-shot facing while dying (the pull refuses then). F2 (HR-02): `rotate` (no teleport: the player stays on the F5 seat
    that rides the avatar, nothing dismounts and the avatar does not move) for the player toward her eyes (from their own eyes:
    anchored eyes) and for the avatar (rlk_av, the F5 / shoulder-view body) toward her feet; first person has no avatar (the
    second line selects nothing)."""
    return [f'execute as {PL} anchored eyes run rotate @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] eyes',
            'rotate @e[tag=rlk_av,limit=1] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet']


def rock(look):
    """The kit's seat_rock (S3's decor prop at api.deco()['seat_rock']) re-looked. I1b verification round 2 (m1): the point is
    written exactly (api.xyz), as S3 summons the rock there."""
    p = api.deco()['seat_rock']
    c = K.prop('seat_rock', look=look)
    return (f'execute positioned {api.xyz(p, 3)} as @e[type=minecraft:item_display,tag={api.TAGS["deco"]},'
            f'distance=..1,limit=1] run {c}') if c else None


def rock_kill():
    p = api.deco()['seat_rock']
    return f'execute positioned {api.xyz(p, 3)} run kill @e[type=minecraft:item_display,tag={api.TAGS["deco"]},distance=..1]'


def halo(bright):
    """I1b (requests s1k-3 / s2b-4): S3's decor moon halo in the bright look of the arena's current look (moon -> p1b, crimson ->
    p2b; the arena framework's record rlk:mboss look_hr_field) or back to its own (p1 / p2); in dark it stays off."""
    out = []
    for look, base in (('moon', 'p1'), ('crimson', 'p2')):
        c = K.prop('moon_halo', look=base + ('b' if bright else ''))
        if c:
            out.append(f'execute if data storage rlk:mboss {{look_{api.AID}:"{look}"}} as @e[type=minecraft:item_display,'
                       f'tag={api.TAGS["deco_moon_halo"]}] run {c}')
    return out


def line(i):
    return K.hud('line', id=i)


FIRST_PERSON = 'if entity @a[tag=rlk_body]'        # the view system off: the player is its own body (no avatar)
AVATAR = 'unless entity @a[tag=rlk_body]'


def line_at_player(cmd, aim):
    """F2 (HR-45): the 홍련일섬 line through the player's chest point (F5: the avatar's chest, the camera behind it), and in
    first person at the eye 1.2 b toward her instead (the chest point lies on the camera's own line there: 0 px)."""
    if not cmd:
        return []
    return [f'execute {AVATAR} at {PLB} positioned ~ ~1.3 ~ {aim} run {cmd}',
            f'execute {FIRST_PERSON} at {PLB} positioned ~ ~1.62 ~ {aim} positioned ^ ^ ^1.2 run {cmd}']


def snd(name):
    return K.snd(name)


def sig(name):
    return f'scoreboard players set {api.SEQ_SIGNAL} {OBJ} {api.SIG[name]}'


def warn_on(cond=True):
    return K.hud('warn', on=1) if cond else None


# ---- the body-move helpers each sequence writes as its own files -----------------------------------------------------------
class Moves:
    """Helper functions seq/<name>/m/<key> (@s = the body): candidate destinations tried in order (return at the first)."""

    def __init__(self, name):
        self.name, self.files = name, {}

    def add(self, key, lines, head):
        self.files[key] = [f'# {head} (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).'] + lines
        return f'function {SEQ}/{self.name}/m/{key}'

    def write(self, W):
        for k, v in self.files.items():
            W.w(f'seq/{self.name}/m/{k}', v)


def cand(pos, mv):
    """One candidate line: at pos (an execute positioning chain ending on the floor) if mv/ok then the move."""
    return f'execute {pos} if {OK} run return run {mv}'


def glide(t):
    return f'function rlk:mboss/mv/glide {{t:{t}}}'


def leap(t, h):
    return f'function rlk:mboss/mv/leap {{t:{t},h:{h}}}'


def near(d, side=0):
    """d b from the player on her line to the player (side b to the player's left), on the floor."""
    return f'at {PLB} facing entity @s feet rotated ~ 0 positioned ^{num(side)} ^ ^{num(d)} {FLOOR}'


def stage_pt(x, z, y=None):
    """A point in the staging frame (x + = the player's left, z + = the player's front), on the floor (or at y above it)."""
    return f'at {STAGE} positioned ^{num(x)} ^ ^{num(z)} positioned ~ {num(CY + (y or 0))} ~'


# =============================================================================================================================
# CS0 — intro (PLAN §3.1; clip intro 554 + intro_end 86 = 640) and its skip
# S2d (11-05): she rises off the kit's seat stone (1.2 x 0.24 x 0.64 b: 0.135 b in front of her seat to 0.505 b behind it,
# requests/s2d.md s2d-2) forward over her feet, SEAT_RISE b toward the moon over the 12-t rise, then steps SEAT_ASIDE b to her
# right while she straightens (226-246), so the stone stays clear of her feet through the turn to the player and the walk. The
# rig's feet step with that one linear 20-t glide (tools/scarlet_retarget.mjs ASIDE: four 0.55-b side steps; test_rig checks
# that ASIDE matches SEAT_ASIDE and the tick)
SEAT_RISE, SEAT_ASIDE = 0.4, 1.1
def build_intro(W):
    s, mv = Seq('intro'), Moves('intro')
    e = lambda k, d=0: ev('intro', k, d)
    x = lambda k, d=0: api.SKIP_T + ev('intro_end', k, d)                # intro_end events on the intro clock
    # E0 (start): the rift closing behind the player, the ambient, the wind; lines 1-10 at api.LINE_AT
    # F2 (HR-46): the wind at the player (played at her seat, 26.7 b away, its minVolume 0 sent it to no one)
    s.at(0, (f'execute at {STAGE} rotated as {STAGE} positioned ^ ^ ^-1.5 run {K.p("arrive_rift")}' if K.p('arrive_rift') else None),
         K.p('ambient_p1'), (f'execute at {PL} run {snd("cs0_wind")}' if snd('cs0_wind') else None))
    for i in range(1, 11):
        assert api.LINE_AT[i][0] == 'intro'
        s.at(api.LINE_AT[i][1], line(i))
    stop_wind = 'stopsound @a[tag=player] * minecraft:item.elytra.flying' if snd('cs0_wind') else None
    # E1 the bottle from the rock (24, rock bare), the pour sound 32, the wind stops 40, the bottle back (52, rock bottle)
    s.at(e('pour', -6), rock('bare')).at(e('pour', 2), snd('cs0_pour')).at(e('l1', 20), stop_wind).at(e('pour', 22), rock('bottle'))
    # E2 the sip; E3 the cup to the moon (chime 118; I1b: the halo about 20 % brighter 112-146, requests s1k-3 / s2b-4)
    s.at(e('sip'), snd('cs0_sip')).at(e('raise', 8), snd('cs0_moon'))
    s.at(e('raise', 2), halo(True)).at(e('l4'), halo(False))
    # E5 the cup set down (rock set), rising (cloth 230), the turn to the player 248-268 (the body turned <= 12 deg / t)
    s.at(e('cup_down'), snd('cs0_cup'), rock('set')).at(e('stand', 16), snd('cloth'))
    rise = mv.add('rise', [cand(f'at @s rotated as @s rotated ~ 0 positioned ^ ^ ^{num(SEAT_RISE)} {FLOOR}', glide(12))],
                  f'The rise off the seat stone: {SEAT_RISE} b forward over her feet over 12 t')
    aside = mv.add('aside', [cand(f'at @s rotated as @s rotated ~ 0 positioned ^{num(-SEAT_ASIDE)} ^ ^ {FLOOR}', glide(20)),
                             cand(f'at @s rotated as @s rotated ~ 0 positioned ^{num(SEAT_ASIDE)} ^ ^ {FLOOR}', glide(20))],
                   f'Beside the seat stone: {SEAT_ASIDE} b to her right (else her left) over 20 t, before the turn')
    s.at(e('stand'), rise).at(e('stand', 12), aside)
    for t in range(e('turn'), e('turn', 21)):
        s.at(t, api.rig('face/track'))
    # E6-E7 / E9 the walks: 8-t glide legs of 1.2 b (0.15 b/t) toward the player while more than 7 b away, so she stops at
    # <= 7 b (PLAN §3.1, as the skip's near7; I1b, lead decision 1: was >= 8.2 b, which stopped her at 7-8.1 b); a footfall
    # sound every 8 t (the clip's 16-t cycle steps every 8 t)
    leg = mv.add('leg', [f'execute if score #mbDist mb matches ..70 run return 0',
                         cand(f'at @s facing entity {PLB} feet rotated ~ 0 positioned ^ ^ ^1.2 {FLOOR}', glide(8))],
                 'One walk leg: 1.2 b toward the player over 8 t while she is more than 7 b away')
    for t0, t1 in ((e('scab_hand', 12), e('l8')), (e('l9'), e('l9', 48))):
        for t in range(t0, t1, 8):
            s.at(t, api.rig('face/track'), DIST, leg, snd('grass_step'))
    # E8 the open hand from the moon across the field (petals 402, the leaves' sound 410); E10 the scabbard raised 510
    s.me(e('gesture'), K.p('petals_drift')).at(e('gesture', 8), snd('cs0_petals')).at(e('scab_up'), snd('scab_raise'))
    # E11-E12 on the intro_end clip: line 11 at its tick 0; the spin faces her to the player; the draw 610 (title, glint at the
    # blade tip, the white crescent); the tuck 630 (rock and props gone, music 1); the push ring 636 (no damage)
    s.at(x('l11'), api.play('intro_end'), line(11), api.rig('face/track'))
    s.at(x('spin'), api.rig('face/player')).at(x('draw', -4), snd('draw_spin'))
    s.at(x('draw'), L.title(*api.TITLE), snd('draw'))
    s.fx(x('draw'), 'blade_tip', K.p('glint', c=api.C_WHITE)).me(x('draw'), K.p('qi_arc', r=17, yaw=0, pitch=0, roll=0, c=api.C_LILAC))
    s.at(x('draw', 2), snd('draw_ring'))
    s.at(x('tuck'), snd('cloth'), rock_kill(), api.rig('look/props/none')).at(x('music'), api.music(1))
    s.at(x('push'), L.push_ring(4.0, 4))
    head = 'CS0 intro (PLAN §3.1): seated with the cup and bottle, lines 1-10, the walk, the scabbard raised; intro_end: line 11, the draw, the stance.'
    write(W, 'intro', s, head, api.SEQ_LEN['intro'], start_head=stage() + [api.play('intro')], cancel=[stop_wind] + halo(False))
    # the skip (the core calls it after api.SKIP_HOLD t of sneak, then sets #sq to SKIP_T - 1: the next tick plays intro_end)
    near7 = mv.add('near7', [f'execute if score #mbDist mb matches ..70 run return 0']
                   + [cand(near(d), 'tp @s ~ ~ ~') for d in (6.5, 5.0, 3.5)],
                   'The skip: her on her line to the player at <= 7 b (a mv/ok point; already nearer: she stays)')
    W.w('seq/intro/skip', [
        '# The intro skip (@s = the body; PLAN §3.1): the black falls; under it the intro is cleared (line, the wind, the rock and the',
        '# props, a walk leg in progress), she stands <= 7 b from the player facing them; the core then sets #sq to 553 and the next',
        '# tick plays intro_end from its tick 0 (E10\'s end pose) with line 11 typed on the black.',
        *[c for c in (K.hud('clear'), K.ovl('black', 0, 20, 6), stop_wind) if c], *halo(False), HUD_HOLD,
        'function rlk:mboss/mv/stop', rock_kill(), api.rig('look/props/none'), DIST, near7, api.rig('face/player')])
    mv.write(W)


# =============================================================================================================================
# CS1 — the 60 % cutscene (PLAN §3.2; clip cs1 213)
PETAL1, PETAL2, PETAL3 = 'rlk_hr_sqp_1', 'rlk_hr_sqp_2', 'rlk_hr_sqp_3'


def petal_summon(tag, pos, look='whole'):
    """A kit petal card (fx/prop/petal_big) at pos: summoned (teleport_duration 1), then rotated to face the player, then looked."""
    c = K.prop('petal_big', look=look)
    if not c:
        return []
    sel = f'@e[type=minecraft:item_display,tag={tag},limit=1]'
    return [f'kill @e[type=minecraft:item_display,tag={tag}]',
            f'execute {pos} run summon minecraft:item_display ~ ~ ~ {{Tags:{tags(PROP_T, tag)},teleport_duration:1,view_range:2f}}',
            f'execute as {sel} at @s facing entity {PLB} eyes run tp @s ~ ~ ~ ~ ~', f'execute as {sel} run {c}']


def petal_move(tag, pos):
    if not K.prop('petal_big', look='whole'):
        return None
    return f'execute as @e[type=minecraft:item_display,tag={tag},limit=1] {pos} facing entity {PLB} eyes run tp @s ~ ~ ~ ~ ~'


def petal_look(tag, look):
    c = K.prop('petal_big', look=look)
    return f'execute as @e[type=minecraft:item_display,tag={tag},limit=1] run {c}' if c else None


def build_cs1(W):
    s, mv = Seq('cs1'), Moves('cs1')
    e = lambda k, d=0: ev('cs1', k, d)
    # C0 the lunge: to 1.8 b before the player (<= 20 b away), else 20 b toward the player; 8 t; the lilac streak
    lunge = mv.add('lunge', [DIST, f'execute if score #mbDist mb matches ..218 run return run function {SEQ}/cs1/m/lunge_near',
                             cand(f'at @s facing entity {PLB} feet rotated ~ 0 positioned ^ ^ ^20 {FLOOR}', glide(8))],
                   'C0 the lunge (far: 20 b toward the player)')
    mv.add('lunge_near', [cand(near(d), glide(8)) for d in (1.8, 2.6, 3.4)], 'C0 the lunge: 1.8 b before the player')
    s.at(e('lunge'), lunge)
    for t in range(e('lunge'), e('lunge', 8), 2):
        s.me(t, K.p('afterimage', len=20), y=0)
    s.at(e('lunge', 2), snd('lunge'))
    # C1 the blade lock: the gold clash, the orange arcs 14-22, line 13
    s.fx(e('lock'), 'blade_mid', K.p('clash_gold')).at(e('lock'), snd('blade_lock')).at(e('l13'), line(13))
    for t in range(e('lock', 4), e('lock', 13), 2):
        s.fx(t, 'blade_mid', K.p('clash_arc'))
    s.at(e('lock', 4), snd('arc_crackle')).at(e('lock', 8), snd('arc_crackle'))
    # C2 the push-off (a push ring r 2.5, no damage), the leap back 6 b, the hat swing, the landing
    back = mv.add('back', [cand(f'at @s facing entity {PLB} feet rotated ~180 0 positioned ^ ^ ^{num(d)} {FLOOR}', leap(16, 15))
                           for d in (6, 4.5, 3)], 'C2 the leap back 6 b away from the player (apex 1.5 b)')
    s.at(e('push'), L.push_ring(2.5, 3)).at(e('leap'), back).at(e('hat_back'), snd('hat_swing')).at(e('land'), snd('land_grass'))
    # C3 the wide hold: leaves across the sky, line 14, the white glint
    s.me(e('land', 8), K.p('leaves_dark', n=8), y=6).at(e('l14'), line(14))
    s.fx(e('glint'), 'blade_tip', K.p('glint', c=api.C_WHITE)).at(e('glint'), snd('glint_ring'))
    # C4 the black (line 15 typed on it); C5 the petal before her face (her right -> her left 114-126, sinking past her mouth
    # 126-134), the second petal before the player's eyes (1.6 b, eye height, the stage frame; drifts in 128-150, holds), the
    # cut line 154; line 16 from 144
    s.at(e('black'), K.ovl('black', 0, 10, 3), snd('black_drop')).at(e('l15'), line(15)).at(e('l16'), line(16))
    p0 = e('petal')
    s.at(p0, petal_summon(PETAL1, f'at {BODY} rotated as {BODY} rotated ~ 0 positioned ^-0.7 ^1.74 ^1.0'), snd('petal_drift'))
    for i in range(1, 21):
        t = p0 + i
        if i <= 12:
            u = i / 12
            px, py = -0.7 + 1.4 * u, 1.74 - 0.125 * u
        else:
            u = (i - 12) / 8
            px, py = 0.7 + 0.1 * u, 1.615 - 0.5 * u
        s.at(t, petal_move(PETAL1, f'at {BODY} rotated as {BODY} rotated ~ 0 positioned ^{num(px)} ^{num(py)} ^{num(1.0 - .1 * (i > 12))}'))
    s.at(p0 + 21, f'kill @e[type=minecraft:item_display,tag={PETAL1}]')
    p2 = e('petal2')
    s.at(p2, petal_summon(PETAL2, stage_pt(0.9, 1.6, 1.62)))
    for t in range(p2 + 1, e('cut') - 3):
        u = min(1.0, (t - p2) / (e('l16', 6) - p2))
        s.at(t, petal_move(PETAL2, stage_pt(0.9 * (1 - math.sin(u * math.pi / 2)), 1.6, 1.62 - .04 * u)))
    s.at(e('cut'), petal_look(PETAL2, 'cut'), snd('petal_cut'))
    # C6 the negative, C7 the pink-white; C8 홍련일섬: the red line through the player's chest (perpendicular to her -> the player,
    # rising 13 deg to the player's right), the petal burst and sparks at her, the red tint, the slash sounds; the petal card splits
    # and its halves fall; the arena turns crimson (173), the rig's P2 accents, the dark leaves, music 2, the swirl
    s.at(e('neg'), K.ovl('negative', 0, 4, 0), snd('negative')).at(e('pink'), K.ovl('pinkwhite', 0, 4, 10))
    sl = K.p('scarlet_line', len=600, yaw=90, roll=13)
    s.at(e('slash'), line_at_player(sl, 'facing entity @s feet rotated ~ 0'),
         K.ovl('red_tint', 0, 4, 20), snd('iai_slash'), petal_look(PETAL2, 'split'))
    s.me(e('slash'), K.p('petal_burst', r=20)).me(e('slash'), K.p('clash_spark'))
    for t in range(e('slash', 1), e('slash', 21)):
        u = (t - e('slash')) / 20
        s.at(t, petal_move(PETAL2, stage_pt(0, 1.6, 1.58 - 1.3 * u * u)))
    s.at(e('slash', 21), f'kill @e[type=minecraft:item_display,tag={PETAL2}]')
    # the dark leaves: the 40 of the kit in two halves on consecutive ticks (the first 20, then the last 20: one burst of 40
    # cost 3.2 k commands in one tick, above the 3000 per fight tick; I1b verification round 1)
    s.me(e('slash', 2), K.p('leaves_dark', n=20), y=6).me(e('slash', 3), K.p('leaves_dark', n=-20), y=6)
    s.at(e('recolour'), api.arena_look('crimson'), api.rig('look/phase/p2'))
    s.at(e('music'), api.music(2)).me(e('swirl'), K.p('leaves_swirl'))
    mv.write(W)
    head = 'CS1 (PLAN §3.2): the lunge, the blade lock, apart, the iai under the brim, the petals, 홍련일섬, the crimson field.'
    write(W, 'cs1', s, head, api.SEQ_LEN['cs1'], start_head=[api.rig('face/player'), face_player_fight()] + stage(True) + [api.play('cs1')],
          cancel=[f'kill @e[type=minecraft:item_display,tag={PROP_T}]'])


# =============================================================================================================================
# SQ1 — the P2 opener (PLAN §3.3; clip sq1 60): the re-hat, the stand-off, the darkness at T0 - 17 (the dark look requested at
# its 'dark' event; the warning banner only if A8's fail is lethal), the hand to the brim (in the clip)
def build_sq1(W):
    s = Seq('sq1')
    e = lambda k, d=0: ev('sq1', k, d)
    s.me(0, K.p('leaves_swirl')).at(e('hat_on'), snd('hat_on'))
    s.at(e('dark'), api.arena_look('dark'), warn_on(api.ULT60_LETHAL)).at(e('dark', 1), snd('dark_fall')).at(e('dark', 2), snd('dark_hum'))
    s.at(e('brim', 2), snd('brim_ring'))
    head = 'SQ1 (PLAN §3.3): re-hat, stand-off, the darkness (T0 - 17), the hand to the brim; A8 at its end.'
    write(W, 'sq1', s, head, api.SEQ_LEN['sq1'], start_head=stage() + [api.play('sq1'), K.hud('warn', on=0)])


# =============================================================================================================================
# CS2 / CS3 — the counter cinematic repel {at:60|5} (PLAN §3.4; clip repel 104)
def build_repel(W):
    s, mv = Seq('repel'), Moves('repel')
    e = lambda k, d=0: ev('repel', k, d)
    # R0 the lock (sparks every 3 t); R1 grabbed; R2 the clash on the hat on her back (hp1); R3 swung round the player on a half
    # circle via the player's right (2-t legs, the stage frame, radius 1.5 -> 0.8, a 1 b arc) to 0.8 b behind the player
    for t in (0, 3, 6):
        s.fx(t, 'blade_mid', K.p('clash_spark'))
    s.at(e('lock'), snd('repel_lock')).at(e('lock', 4), snd('blade_tick')).at(e('grab', 8), snd('grabbed'))
    s.fx(e('flash'), 'hat_crown', K.p('clash_gold')).at(e('flash'), sig('hp1'), snd('hat_clash')).at(e('throw', 2), snd('tip_over'))
    for i in range(1, 9):
        th, r = math.radians(180 * i / 8), 1.5 + (0.8 - 1.5) * i / 8
        h = math.sin(math.pi * i / 8)
        k = mv.add(f'r{i}', [cand(stage_pt(-r * math.sin(th), r * math.cos(th), h), glide(2))], f'R3 the half circle, leg {i} of 8')
        s.at(e('throw', 2 * (i - 1)), k)
    s.at(e('b2b'), snd('step_light'))
    # R5 thrown over the player's shoulder to 3.5 b before them (apex 2.5 b); R6 the landing (hp2); R7 lying (the petal burst at
    # 5 % only); R8 the kick (hp3: at 5 % the core's lethal hit)
    toss = mv.add('toss', [cand(stage_pt(0, d), leap(15, 25)) for d in (3.5, 2.5, 1.5)], 'R5 the throw to 3.5 b before the player')
    s.at(e('toss'), toss, snd('thrown'))
    s.me(e('land'), K.p('dust_ring', r=12), y=.1).at(e('land'), sig('hp2'), snd('land_back'))
    burst = K.p('petal_burst', r=10)
    s.at(e('petals'), gate(f'if score #sq_at {OBJ} matches 5', [(f'execute positioned ~ ~0.3 ~ run {burst}' if burst else None), snd('petal_break')]))
    # F2 (HR-17): kept cards (the kick at 5 % kills her in this tick: death_start's fx/clear would take the flash with it)
    s.at(e('kick'), K.fixed('keep_on')).fx(e('kick'), 'head', K.p('kick_flash')).at(e('kick'), K.fixed('keep_off'))
    s.at(e('kick'), sig('hp3'), snd('kick'))
    mv.write(W)
    head = 'CS2 / CS3 repel {at:60|5} (PLAN §3.4): lock, grab, the clash on the hat, the half circle, back to back, the throw, the kick.'
    write(W, 'repel', s, head, api.SEQ_LEN['repel'], macro=True,
          start_head=[f'$scoreboard players set #sq_at {OBJ} $(at)', api.rig('face/player'), face_player_fight()] + stage(True)
          + [api.play('repel')])


# =============================================================================================================================
# the 5 % lead-ins (PLAN §3.5): lead_down (82 t, from the down window) and lead_stand {g:"a8"|"a13"} (70 t, standing / restarts)
def side_move(mv, key, t):
    """2 b sideways to her right over t ticks (else to her left; else she stays)."""
    return mv.add(key, [cand(f'at @s rotated as @s rotated ~{a} 0 positioned ^ ^ ^2 {FLOOR}', glide(t)) for a in (90, -90)],
                  f'2 b sideways (her right first) over {t} t')


def build_lead_down(W):
    s, mv = Seq('lead_down'), Moves('lead_down')
    e = lambda k, d=0: ev('lead_down', k, d)
    s.at(e('walk'), side_move(mv, 'side', e('hat_on') - e('walk')))
    s.at(e('refill'), sig('refill'), snd('shield_refill')).me(e('refill'), K.p('shield_refill'))
    s.at(e('hat_on'), snd('hat_on')).at(e('glow'), api.rig('look/blade/lilac')).at(e('glow', 7), api.rig('look/blade/off'))
    s.at(e('dark'), api.arena_look('dark'), warn_on(api.ULT5_LETHAL)).at(e('brim'), snd('dark_fall')).at(e('brim', 1), snd('dark_hum'))
    mv.write(W)
    head = 'lead_down (PLAN §3.5): the kip-up, the hat, the side steps, the shield refill, the hat on, the glow, the darkness + the brim (A13 at its end).'
    write(W, 'lead_down', s, head, api.SEQ_LEN['lead_down'], start_head=stage() + [api.play('lead_down'), K.hud('warn', on=0)])


def build_lead_stand(W):
    s, mv = Seq('lead_stand'), Moves('lead_stand')
    e = lambda k, d=0: ev('lead_stand', k, d)
    s.at(e('walk'), side_move(mv, 'side', e('hat_over') - e('walk')))
    s.at(e('refill'), sig('refill'), snd('shield_refill')).me(e('refill'), K.p('shield_refill'))
    s.at(e('hat_on'), snd('hat_on')).at(e('glow'), api.rig('look/blade/lilac')).at(e('glow', 7), api.rig('look/blade/off'))
    lethal = {'a8': api.ULT60_LETHAL, 'a13': api.ULT5_LETHAL}
    gid = {'a8': 8, 'a13': 13}
    w = K.hud('warn', on=1)
    s.at(e('dark'), api.arena_look('dark'),
         *[f'execute if score #sq_g {OBJ} matches {gid[g]} run {w}' for g in api.SEQ_ARGS['lead_stand']['g'] if lethal[g] and w])
    s.at(e('brim'), snd('dark_fall')).at(e('brim', 1), snd('dark_hum'))
    for g in api.SEQ_ARGS['lead_stand']['g']:
        W.w(f'seq/lead_stand/g/{g}', [f'# lead_stand {{g:"{g}"}}: the gauntlet it leads into.', f'scoreboard players set #sq_g {OBJ} {gid[g]}'])
    mv.write(W)
    head = 'lead_stand {g:"a8"|"a13"} (PLAN §3.5): the stagger, the hat, the side steps, the refill, the darkness + the brim (the gauntlet g at its end).'
    # I1: the gauntlet arg is dispatched through storage to static references (check_mboss_pack resolves a $(...) function
    # reference only as a numeric family <ref><n>; a string-valued g/$(g) was its one problem on the merged tree)
    write(W, 'lead_stand', s, head, api.SEQ_LEN['lead_stand'], macro=True,
          start_head=[f'scoreboard players set #sq_g {OBJ} 0', f'$data modify storage rlk:{OBJ} seq.g set value "$(g)"']
          + [f'execute if data storage rlk:{OBJ} seq{{g:"{g}"}} run function {SEQ}/lead_stand/g/{g}'
             for g in api.SEQ_ARGS['lead_stand']['g']]
          + stage() + [api.play('lead_stand'), K.hud('warn', on=0)])


# =============================================================================================================================
# CS4 — the ending (PLAN §3.7 std; clip ending 1042 = H); the event coda follows (the core starts seq/event at #sqdone)
def build_ending(W):
    s, mv = Seq('ending'), Moves('ending')
    e = lambda k, d=0: ev('ending', k, d)
    # the start: lying where CS3 left her; the one-shot facing (rotate, no teleport: F2 HR-02; the pull refuses while dying)
    # E1b the glint at the hat's edge, the lilac band across the player at chest height
    s.fx(e('glint'), 'hat_crown', K.p('glint', c=api.C_LILAC)).at(e('glint'), snd('band_glint'))
    # F2 (HR-32): the band sweeps her distance to the player + 1 b (storage seq.band.sw, tenths), so it passes over them
    band = K.pw('qi_band', f'rlk:{OBJ} seq.band')
    if band:
        s.at(e('band'), DIST, f'scoreboard players operation #sq_bd {OBJ} = #mbDist mb', f'scoreboard players add #sq_bd {OBJ} 10',
             f'data modify storage rlk:{OBJ} seq.band set value {{len:120,yaw:0,pitch:0,roll:0,sw:25}}',
             f'execute store result storage rlk:{OBJ} seq.band.sw int 1 run scoreboard players get #sq_bd {OBJ}',
             f'execute positioned ~ ~1.1 ~ facing entity {PLB} feet rotated ~ 0 run {band}')
    s.at(e('band'), snd('band_sweep'))
    # E2 up, the hat caught and on; to 3 b before the player; the violet glow on the raised blade; the gold flash between them
    s.at(e('hat_on', -4), mv.add('e2', [cand(near(d), glide(8)) for d in (3.0, 3.6)], 'E2 to 3 b before the player'))
    s.at(e('raise'), api.rig('look/blade/violet'), snd('blade_charge'))
    mid = K.p('clash_gold')
    s.at(e('clash1'), api.rig('look/blade/off'), snd('clash'),
         (f'execute at {PLB} positioned ~ ~1.3 ~ facing entity @s feet positioned ^ ^ ^1.5 run {mid}' if mid else None),
         mv.add('lock', [cand(near(d), glide(4)) for d in (1.2, 1.8)], 'E3 to 1.2 b (the blade lock)'))
    for t in range(e('lock'), e('back'), 4):
        s.fx(t, 'blade_mid', K.p('clash_spark'))
    s.at(e('lock', 2), snd('blade_tick')).at(e('lock', 10), snd('blade_tick'))
    # E6 slides back 3 b; E7 the lunge (the big clash 96, the bolts round her, three strikes stopping at the player in sparks)
    s.at(e('back'), snd('step_light'), mv.add('back', [cand(near(d), glide(12)) for d in (4.2, 3.4)], 'E6 back 3 b'))
    s.at(e('lunge'), mv.add('lunge', [cand(near(d), glide(4)) for d in (1.5, 2.2)], 'E7 the lunge to 1.5 b'))
    s.fx(e('clash2'), 'blade_mid', K.p('clash_gold')).at(e('clash2'), snd('clash_big'))
    for t in (e('clash2', 2), e('clash2', 6), e('clash2', 10)):
        s.me(t, K.p('deco_bolt'), y=0)
    s.at(e('clash2', 4), snd('bolt_crackle'))
    for k in ('x1', 'x2', 'x3'):
        s.fx(e(k), 'blade_tip', K.p('clash_spark')).at(e(k), snd('blade_tick'))
    # E8 the pass: 8 b past the player (1 b to the side), the passing strike 143, the turn back 150-160; E9 back in (strike 174,
    # the lock, the second flash 188)
    s.at(e('pass'), snd('lunge'), mv.add('pass', [cand(f'at {PLB} facing entity @s feet rotated ~180 0 positioned ^-1 ^ ^{num(d)} {FLOOR}', glide(6))
                                                  for d in (6.5, 5.0, 3.5)], 'E8 the dash past the player (8 b)'))
    for t in range(e('pass'), e('pass', 6), 2):
        s.me(t, K.p('afterimage', len=20), y=0)
    s.fx(e('strike'), 'blade_mid', K.p('clash_spark'))
    for t in range(e('pass', 10), e('pass', 21)):
        s.at(t, api.rig('face/track'))
    s.at(e('return'), mv.add('ret', [cand(near(d), glide(4)) for d in (1.2, 1.8)], 'E9 back in to 1.2 b'))
    for k in ('clash3', 'flash2'):
        s.fx(e(k), 'blade_mid', K.p('clash_gold')).at(e(k), snd('clash_big'))
    # E10-S3 the aerial exchange: up 5 b and back to 4 b (8 t), the hang; three strikes (white-hot cores), the lock, the white
    s.at(e('leap'), mv.add('up', [cand(f'at {PLB} facing entity @s feet rotated ~ 0 positioned ^ ^ ^{num(d)} positioned ~ {CY + 5} ~', glide(8))
                                  for d in (4.0, 3.0)], 'E10 the leap up and back (4 b off, 5 b up)'))
    for k in ('a1', 'a2', 'a3'):
        s.fx(e(k), 'blade_tip', K.p('clash_gold')).at(e(k), snd('air_slash'))
    s.at(e('a2'), snd('air_clash')).at(e('white'), K.ovl('white', 0, 3, 8), snd('air_white'))
    # S4 the long arc down to 10 b from the player toward the moon (the nearest free bearing to it), the petal streaks, the landing
    mp = api.MOON_POS
    land = mv.add('land', [cand(f'at {PLB} facing {api.xyz(mp, 3)} rotated ~{a} 0 positioned ^ ^ ^10 {FLOOR}', leap(20, 40))
                           for a in (0, 30, -30, 60, -60, 90, -90, 120, -120, 150, -150, 180)],
                   'S4 the landing 10 b from the player toward the moon (the nearest free bearing)')
    s.at(e('fly'), land).me(e('fly', 2), K.p('petals_wind'), y=.8).at(e('land'), snd('land_far'))
    # S5 the turn to the player 268-272, the walk-in to 4.5 b (272-296), the scabbard swing (296), the petal across the player's
    # view (306-314), line 17 + music 3 (300), the sheathe click (320)
    for t in range(e('rise2'), e('walk')):
        s.at(t, api.rig('face/track'))
    s.at(e('walk'), DIST, mv.add('walk', [f'execute if score #mbDist mb matches ..50 run return 0']
                                 + [cand(near(d), glide(24)) for d in (4.5, 5.5)], 'S5 the walk-in to 4.5 b'))
    for t in range(e('walk'), e('swing'), 6):
        s.at(t, snd('grass_step'))
    s.at(e('swing'), snd('scab_swing')).at(e('l17'), line(17)).at(e('music'), api.music(3))
    p3 = e('swing', 10)
    s.at(p3, petal_summon(PETAL3, stage_pt(1.0, 1.4, 1.5)))
    for i in range(1, 9):
        s.at(p3 + i, petal_move(PETAL3, stage_pt(1.0 - 2.0 * i / 8, 1.4, 1.5 - .25 * i / 8)))
    s.at(p3 + 9, f'kill @e[type=minecraft:item_display,tag={PETAL3}]')
    s.at(e('seated'), snd('sheathe_click'))
    # S6-S8 lines 18-20; the head lowered; the turn toward the moon 506-526 (<= 12 deg / t; the feet step)
    for k in ('l18', 'l19', 'l20', 'l21', 'l22', 'l23'):
        s.at(e(k), line(int(k[1:])))
    W.w('seq/ending/turn_moon', [
        f'# The body turns at most 12 degrees toward the moon (api.MOON_POS) this tick, yaw only (@s = the body).',
        f'execute store result score #sq_y0 {OBJ} run data get entity @s Rotation[0] 100',
        f'execute at @s run summon minecraft:marker ~ ~ ~ {{Tags:{tags(HELP_T)}}}',
        f'execute at @s facing {api.xyz(mp, 3)} run tp {HELP} ~ ~ ~ ~ 0',
        f'execute store result score #sq_y1 {OBJ} run data get entity {HELP} Rotation[0] 100',
        f'kill @e[type=minecraft:marker,tag={HELP_T}]',
        f'scoreboard players operation #sq_y1 {OBJ} -= #sq_y0 {OBJ}', f'scoreboard players add #sq_y1 {OBJ} 90000',
        f'scoreboard players operation #sq_y1 {OBJ} %= #c36000 mb', f'scoreboard players remove #sq_y1 {OBJ} 18000',
        f'execute if score #sq_y1 {OBJ} matches 1201.. run scoreboard players set #sq_y1 {OBJ} 1200',
        f'execute if score #sq_y1 {OBJ} matches ..-1201 run scoreboard players set #sq_y1 {OBJ} -1200',
        f'scoreboard players operation #sq_y0 {OBJ} += #sq_y1 {OBJ}',
        f'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #sq_y0 {OBJ}'])
    for t in range(e('turn'), e('turn', 21)):
        s.at(t, f'function {SEQ}/ending/turn_moon')
    s.at(e('turn', 4), snd('grass_step')).at(e('turn', 12), snd('grass_step'))
    # S10-C1 the moon gaze (the warm motes, the gaze chime, the heart petals); C2 the pivot back to the player 794-815 (the cloth),
    # the greeting; C3 the hat-tip (the cloth at the pull, the heart petals)
    s.me(e('l21'), K.p('motes_warm'), y=.4).at(e('gaze', 10), snd('moon_gaze')).me(e('gaze', 50), K.p('petals_heart'))
    s.at(e('gaze'), halo(True)).at(e('gaze', 90), halo(False))     # I1b: the halo about 20 % brighter over the gaze 690-780
    for t in range(e('pivot'), e('pivot', 22)):
        s.at(t, api.rig('face/track'))
    s.at(e('pivot', 11), snd('pivot_cloth')).at(e('pull', 4), snd('cloth')).me(e('pull', 20), K.p('petals_heart'))
    mv.write(W)
    head = 'CS4 ending (PLAN §3.7 std): the ground slash, the duel, the aerial exchange, the landing, the walk-in and sheathe, lines 17-23, the hat-tip; H at its end.'
    write(W, 'ending', s, head, api.SEQ_LEN['ending'],
          start_head=[api.rig('face/player')] + face_player_dying() + stage(True) + [api.play('ending')],
          cancel=[f'kill @e[type=minecraft:item_display,tag={PROP_T}]'] + halo(False))


# =============================================================================================================================
# the event coda (PLAN §7.3.2; 120 t from H, both branches on #hrEv): the thrown sword / the moonlight orb, the leave, the grant
# and the title at E56 (api.ev_apply / api.ev_title), the black at E110
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
    f = lambda v: (f'{v:.5f}'.rstrip('0').rstrip('.') or '0') + 'f'
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
    s = Seq('event')
    E = api.EV_T
    item, buff = f'if score {api.EV_FP[0]} {OBJ} matches {api.EV_BRANCH["item"]}', f'if score {api.EV_FP[0]} {OBJ} matches {api.EV_BRANCH["buff"]}'

    # E0: she faces the player; the branch's clip (ev_give / ev_toast) from CS4's last pose; the lift / chime
    s.at(0, api.rig('face/player'), gate(item, [api.play('ev_give'), snd('ev_lift')]),
         gate(f'unless score {api.EV_FP[0]} {OBJ} matches {api.EV_BRANCH["item"]}', api.play('ev_toast')), gate(buff, snd('ev_chime')))
    # E4 the line (24 item / 25 buff; api.EVENT['lines']), cleared at E52 (before the title)
    if api.EVENT['lines']:
        s.at(E['line'], gate(item, line(24)), gate(buff, line(25)))
        s.at(E['line_clear'], K.hud('clear'))
    # item: E12 the glint along the scabbard; E30 the toss: the display at the hand (scale api.ITEM_SWORD_SCALE, the rig's
    # scabbard hidden by the clip), its yaw toward the target, the end-over-end turn and the arc (apex 1.2 b) to 0.9 b before the
    # player's chest along their facing (re-aimed every tick), never below the floor; E44 upright (scabbard down), the moonbeam,
    # bobbing; E50-E55 sinking into the player's hand (S1 -> 0.15); E56 gone
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
        tr = K.p('ev_trail')
        if tr and k < n:
            lines.append(f'execute at {SWORD} run {tr}')
        s.at(t0 + k, gate(item, lines))
    beam = K.p('ev_beam', h=80, t=6)
    s.at(t1, gate(item, [(f'execute at {SWORD} run {beam}' if beam else None), snd('ev_beam')]))
    hold = E['grant'] - 6                                  # E50: the sink starts
    for t in range(t1 + 1, hold):                         # bobbing over the arrival point (+-0.05 b)
        f = lambda tt: .05 * math.sin((tt - t1) / (hold - t1) * 2 * math.pi)
        s.at(t, gate(item, [f'execute as {SWORD} at @s run tp @s ~ ~{num(f(t) - f(t - 1))} ~']))
    s.at(hold, gate(item, store_p0(SWORD)))
    n2 = E['grant'] - hold
    for k in range(1, n2 + 1):                            # E50-E55 sinking into the player's hand (scale S1 -> 0.15)
        sc = S1 + (.15 - S1) * k / n2
        s.at(hold + k - 1, gate(item, homing(SWORD, k, n2, 0, round((CY + SWORD_R * sc + .04) * 1000), f'at {PLB} rotated as {PLB} rotated ~ 0 positioned ^ ^1.0 ^0.35')
                                 + [f'data merge entity {SWORD} {tf(sword_rot(TH1), sc)}']))
    # buff: E14-E29 the moonlight cup in her palm; E30 the orb leaves the palm and floats 12 t to the player's chest (E42: gone, the
    # moonbeam and the wind onto the player)
    palm = K.p('ev_palm')
    if palm:
        for t in range(E['present'] + 2, E['toss']):
            s.at(t, gate(buff, [api.rig('anchor/hand_l'), f'execute at {ANCHOR} positioned ~ ~0.1 ~ run {palm}']))
    o0, o1 = ORB_FLY
    s.at(o0, gate(buff, [f'kill @e[type=minecraft:marker,tag={ORB_T}]', api.rig('anchor/hand_l'),
                         f'execute at {ANCHOR} positioned ~ ~0.1 ~ run summon minecraft:marker ~ ~ ~ {{Tags:{tags(EV_T, ORB_T)}}}',
                         *store_p0(ORB), snd('ev_toss')]))
    for k in range(1, o1 - o0 + 1):                     # E31-E42: the last step lands on the player's chest
        u = k / (o1 - o0)
        lines = homing(ORB, k, o1 - o0, round(300 * 4 * u * (1 - u)), (CY + 1) * 1000, f'at {PLB} positioned ~ ~1.1 ~')
        if palm:
            lines.append(f'execute at {ORB} run {palm}')
        s.at(o0 + k, gate(buff, lines))
    bb, wind = K.p('ev_beam', h=80, t=10), K.p('ev_wind', r=15)
    s.at(o1, gate(buff, [f'kill @e[type=minecraft:marker,tag={ORB_T}]', (f'execute at {PLB} run {bb}' if bb else None),
                         (f'execute at {PLB} run {wind}' if wind else None), snd('ev_beam')]))
    # both: E34 the leave (clip ev_leave, the petals and wind at her chest), E40 hidden; E56 the grant + the title, the take
    # effect, the petals round the player every 4 t to E108; E110 the black (the original's fade) held to the return
    s.at(E['leave'], api.play('ev_leave'), snd('ev_leave')).me(E['leave'], K.p('ev_leave'))
    s.at(E['hide'], api.rig('state/hidden'))
    s.at(E['grant'], f'kill @e[type=minecraft:item_display,tag={SWORD_T}]', api.ev_apply(), api.ev_title(),
         gate(item, [(f'execute at {PLB} positioned ~ ~1.1 ~ run {K.p("ev_take", c=1)}' if K.p('ev_take', c=1) else None), snd('ev_take_i')]),
         gate(buff, [(f'execute at {PLB} positioned ~ ~1.1 ~ run {K.p("ev_take", c=2)}' if K.p('ev_take', c=2) else None), snd('ev_take_b')]))
    pet = K.p('ev_petals', n=2)
    if pet:
        for t in range(E['grant'], E['black'] - 1, 4):
            s.at(t, f'execute at {PLB} positioned ~ ~0.8 ~ run {pet}')
    s.at(E['black'], K.ovl('black', 10, 12, 0))
    head = 'The event coda (PLAN §7.3.2): item 「검을 건네다」 (the thrown sword) / buff 「월하대작」 (the moonlight orb), the leave, the grant at E56, the black at E110.'
    write(W, 'event', s, head, api.SEQ_LEN['event'], start_head=stage(),
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


_BUILD = {'intro': build_intro, 'cs1': build_cs1, 'sq1': build_sq1, 'repel': build_repel, 'lead_down': build_lead_down,
          'lead_stand': build_lead_stand, 'ending': build_ending, 'event': build_event}
SERVICES = [api.Service(n, api.SEQ_CLIPS[n], _BUILD[n], _events(n), dict(api.SEQ_ARGS.get(n, {}))) for n in api.SEQS]
assert [s.name for s in SERVICES] == list(api.SEQS)
