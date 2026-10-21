"""S2-S helpers (plan.md 5 T1-T3, B3, E, D; s2.md 1, 7, 11): the pure-Python schedules of the transition services and
the sequences, shared by trans.py / seq.py and the stage suite (S:az/tests_ps/pat_trans.py), so the generator and the
tests compute the same ticks. Everything comes from the rig manifest (events, RETIME knots, rest anchors) and the plan
rows; nothing here writes a file.

    SLIDE_LEAD, slide_waves()   T1: the lead (walk / turn to the centre, then the clip), the six fronts with their sizes,
                                the slamming paw, the lift that tells each wave and the service-clock strike tick
    slide_lifts()               T1: the played ticks the lift sound plays (the tell lifts, then each wave's fore lift)
    glide_ticks(d)              T1: the walk-to-centre glide length for a distance d (b)
    b3_pulses(), b3_mounds()    B3: the tail-pillar pulse ticks and the dust-mound puffs on the B3 clock
    roar_rings(el)              T2 / T3: the roar dome rings (ticks after the roar event) per element
    at_local(x, z, lines, y=0)  execute prefix: positioned at the body's local point (x = s, the boss's left; z = f)
"""
import math

from . import api as _A

__all__ = ['SLIDE_LEAD', 'LIFT_AFTER', 'GLIDE_SPD', 'GLIDE_MIN', 'GLIDE_MAX', 'slide_waves', 'slide_lifts', 'glide_ticks', 'b3_pulses',
           'b3_mounds', 'roar_rings', 'at_local', 'flat']

# ---------------------------------------------------------------------------------------------- T1 파멸의 산사태
SLIDE_LEAD = 40            # the walk / turn to the centre (s2.md 11: <= 40 t, the clip >= 20 t after the message)
GLIDE_SPD = 0.30           # b/t: the walk glide toward the centre (the walk clip is authored for 0.13; capped below)
GLIDE_MIN, GLIDE_MAX = 8, 24   # the glide ends with walk_stop (16 t) by the clip start (24 + 16 = SLIDE_LEAD)
STOP_LEN = _A.clip_len('walk_stop')
assert GLIDE_MAX + STOP_LEN <= SLIDE_LEAD, (GLIDE_MAX, STOP_LEN)

# the tell lifts of the landslide clip (azhdaha_clips.mjs: right fore 20-40, right hind 36-56 authored -> played by its
# RETIME); waves 2-5: the next fore leaves the floor right after the previous slam (the clip's foot plan holds the slam
# 2 authored ticks, then lifts toward the next slam: Change note 1 'it starts at the previous wave; gaps 20-21 t')
_TELL_LIFTS_AUTH = (20, 36)
LIFT_AFTER = 3             # the lift sound this many ticks after the previous slam (clear of its boom)
# the slamming paw per wave (plan 5 T1, the clip note): both fores, then right / left alternately; wave 6 the body slam
_PAW = {1: ('paw_fl', 'paw_fr'), 2: ('paw_fr',), 3: ('paw_fl',), 4: ('paw_fr',), 5: ('paw_fl',), 6: ('chest',)}


def slide_waves():
    """The six landslide fronts (plan 5 T1, binding): k, clip tick E (manifest event w<k>), strike on the service clock
    (SLIDE_LEAD + E), r0 / r1 / spd / band, the DMG key, the slamming points (rest anchors), and the readable tell
    (Change note 1, *none* row): tell_t = the clip tick the motion tell starts (w1: the clip start with the head-low
    growl and the slow right fore / hind lift; w2-w5: the fore lift from the previous wave; w6: the rear-up), tell_src."""
    ev = _A.CLIPS['landslide']['events']
    out = []
    for k in range(1, 7):
        e = ev[f'w{k}']
        if k == 1:
            tell_t, src = ev['tell'], 'landslide tell 0: head low + growl, right fore lift 15-30, right hind 27-42, crouch 45-54'
        elif k < 6:
            tell_t, src = ev[f'w{k - 1}'], f'landslide fore lift from the previous slam (w{k - 1} at {ev[f"w{k - 1}"]})'
        else:
            tell_t, src = ev['rear'], 'landslide rear 159: the rear-up hang (20 t)'
        big = k == 6
        out.append(dict(k=k, ev=e, strike=SLIDE_LEAD + e, r0=4.0, r1=30.0 if big else 18.0, spd=4.0 if big else 3.0,
                        band=4.5 if big else 3.5, dmg='t1_wave6' if big else 't1_wave', paws=_PAW[k],
                        tell_t=tell_t, tell_src=src))
    return out


def slide_lifts():
    """Played clip ticks of the lift sounds: the two tell lifts, then the fore lift before waves 2-5."""
    ev = _A.CLIPS['landslide']['events']
    return [_A.rt('landslide', t) for t in _TELL_LIFTS_AUTH] + [ev[f'w{k - 1}'] + LIFT_AFTER for k in (2, 3, 4, 5)]


def glide_ticks(d):
    """Glide length (ticks) of the walk to the centre for a start distance d (b): GLIDE_SPD, clamped GLIDE_MIN..MAX."""
    return max(GLIDE_MIN, min(GLIDE_MAX, int(math.ceil(d / GLIDE_SPD))))


# ---------------------------------------------------------------------------------------------- B3
def b3_pulses():
    """The tail_pillar pulses (clip events pulse 0 / pulse2 40 of the 80-t loop that starts at B3_PILLAR) inside the
    tail window: a small element puff (footfall preset) at the pillar foot."""
    ev = _A.CLIPS['tail_pillar']['events']
    n = _A.clip_len('tail_pillar')
    out, t0 = [], _A.B3_PILLAR
    while t0 < _A.B3_TAILSINK:
        out += [t0 + v for v in sorted(ev.values()) if t0 + v < _A.B3_TAILSINK]
        t0 += n
    return out


def b3_mounds():
    """The dust mound at the centre over B3_MOUND (Change note 1: the tell of the surfacing; 35 t to the burst): one
    plume every 8 t from B3_MOUND[0] through B3_MOUND[1]."""
    a, b = _A.B3_MOUND
    return list(range(a, b + 1, 8))


# ---------------------------------------------------------------------------------------------- T2 / T3 roars
def roar_rings(el):
    """Roar dome rings after the roar_rear 'roar' event (plan 5 T2 / T3 sound rows; the footage: [v6] A Electro ~7 rings
    every 6-7 t, [v7] C Cryo two domes ~34 t apart, the leg roars one ring + one late ring)."""
    if el == 3:
        return [0, 7, 14, 21, 28]
    if el == 4:
        return [0, 34]
    return [0, 8]


# ---------------------------------------------------------------------------------------------- execute helpers
def flat(x):
    for v in x:
        if isinstance(v, (list, tuple)):
            yield from flat(v)
        else:
            yield v


def at_local(x, z, lines, y=0.0):
    """Every line run positioned at the body's local point (x = s, the boss's left; z = f forward; y up), rotated as the
    body, pitch 0 (the executor is the body)."""
    n = _A.L.num
    pre = (f'execute at @s rotated as @s rotated ~ 0 positioned ^{n(float(x), 3)} ^{n(float(y), 3)} ^{n(float(z), 3)} run ')
    return [pre + ln for ln in flat([lines])]
