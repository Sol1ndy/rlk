"""Sequences of 타키 (Tachy): intro, death, T1 날개 전개, T2 심연 (S:tk/PLAN.md §3). OWNER: S2 (rig + sequences).

Contract (api.Service): SERVICES lists one api.Service per api.SEQS name; build(W) writes only seq/<name>/{start,tick,cancel}
(W = api.Writer('S2seq', api.OWN['S2seq'])). The core (S3) sets #sq tk 0 and calls start (@s = the body, at it), then adds 1
to #sq and calls tick every tick; rig/tick runs after the module logic, so the clip shows tick e when #sq = e and every
event below is the clip's event tick (api.ev). A sequence sets #sqdone tk 1 at its clip's end. cancel is called with no
executor (cleanup, death, reload) and only removes what the sequence made (the intro cables).

Division of work with the core (S:tk/requests/s3.md): the core plays music 1 at intro 176 and music 2 at T2 `swap`, the
push rings (intro 178, T1 `flare`), the invulnerability and the looks after T1 / T2; the sequences own the clip, the title
at the intro ignite (mboss_lib.title), T2's blindness and the arena look job `abyss` at `dark`, every sound and effect of
PLAN §3 (kit recipes through api.K, empty until the kit exists) and the rig's intro props (the cables).
Looks inside the sequences are keyed in the clips themselves (tools/tachy_clips.mjs: visor, edge, chest, wing form).
"""
from . import api

L = api.L
OBJ = api.OBJ
AT = 'at @s'
FLOOR = 'at @s'                                  # the body stands on the arena floor at the centre for the whole intro


def _at(t, cmd, ctx=AT):
    """One line on the sequence clock: cmd at #sq = t (cmd may already be an execute ... run ...)."""
    if not cmd:
        return None
    if cmd.startswith('execute '):
        return f'execute if score #sq {OBJ} matches {t} {cmd[8:]}'
    return f'execute if score #sq {OBJ} matches {t} {ctx} run {cmd}' if ctx else f'execute if score #sq {OBJ} matches {t} run {cmd}'


def _snd(name):
    return api.K.snd(name)


def _end(clip):
    n = api.CLIPS[clip][0]
    return f'execute if score #sq {OBJ} matches {n}.. run scoreboard players set #sqdone {OBJ} 1'


def _write(W, name, clip, head, start_extra, events, cancel_extra=()):
    ev = sorted(events, key=lambda e: e[0])
    W.w(f'seq/{name}/start', [f'# {head} @s = the body, at it; #sq {OBJ} = 0. Plays the rig clip {clip} ({api.CLIPS[clip][0]} t).',
                              f'scoreboard players set #sqdone {OBJ} 0', api.play(clip), *[c for c in start_extra if c]])
    tick = [f'# {head} @s = the body; #sq {OBJ} 1.. = the clip tick shown this game tick.']
    for t, cmd, *ctx in ev:
        line = _at(t, cmd, ctx[0] if ctx else AT)
        if line:
            tick.append(line)
    tick.append(_end(clip))
    W.w(f'seq/{name}/tick', tick)
    W.w(f'seq/{name}/cancel', [f'# {head} Cancel (no executor; idempotent).', *[c for c in cancel_extra if c]] or ['# nothing lingers'])


def build_intro(W):
    e = lambda k: api.ev('intro', k)
    ev = [
        (e('hang'), _snd('hang_amb')), (e('hang'), api.K.p('ambient_dust')),
        (10, _snd('chain_step')), (22, _snd('chain_step')),
        (e('snap1'), _snd('cable_snap')), (e('snap2'), _snd('cable_snap')), (e('snap3'), _snd('cable_snap')),
        (e('land'), _snd('body_land')), (e('land'), api.K.p('dust_ring', r=30)),
        (e('pulse1'), _snd('heartbeat')), (e('pulse2'), _snd('heartbeat')),
        (e('push') + 2, _snd('servo')), (74, _snd('armor')),
        (96, _snd('bulb')),
        (e('flare'), _snd('cape_gust')), (e('flare'), api.K.p('ambient_dust')),
        (e('hair'), _snd('hair')),
        (e('visor'), _snd('visor_close')),
        (e('skull'), _snd('skull_ignite')),
        (e('draw'), _snd('sword_draw')),
        (e('ignite'), L.title(api.NAME, api.SUB, api.COLOR), None), (e('ignite'), _snd('blade_ignite')), (e('ignite'), api.K.p('ignite_blade')),
        (e('stance'), _snd('stance')), (e('stance'), api.K.p('ember_burst')),
        (e('stance'), api.rig('prop/clear')),
    ]
    _write(W, 'intro', 'intro', 'Intro (PLAN §3: hang in the cables, drop, lie, push up, rise, cape, hair, visor, skull, draw, ignite, stance).',
           [api.rig('prop/cables')], ev, [api.rig('prop/clear')])


def build_t1(W):
    e = lambda k: api.ev('t1_wings', k)
    ev = [(e('kneel'), _snd('stagger')), (e('split'), _snd('t1_split')), (e('split'), api.K.p('ember_burst')),
          (e('spread'), _snd('cape_gust')), (e('flare'), _snd('t1_flare')), (e('flare'), api.K.p('wing_flare')),
          (e('stand'), _snd('step'))]
    _write(W, 't1', 't1_wings', 'T1 날개 전개 (PLAN §3: kneel, the cape splits into the wings, spread, gold flare, stand).', [], ev)


def build_t2(W):
    e = lambda k: api.ev('t2_abyss', k)
    ev = [(e('stagger'), _snd('stagger')), (e('flare'), _snd('t2_flare')), (e('flare'), api.K.p('core_flare', c=2)),
          (e('tendrils'), api.K.p('core_burst')), (e('dark'), _snd('t2_dark')),
          (e('dark'), 'effect give @a[tag=player] minecraft:blindness 1 0 true', None),
          (e('dark'), api.arena_look('abyss'), None), (e('rise'), api.K.p('wing_flare'))]
    _write(W, 't2', 't2_abyss', 'T2 심연 (PLAN §3: stagger, red visor, tendrils, darkness + the abyss arena, rise).', [], ev)


def build_death(W):
    e = lambda k: api.ev('death', k)
    ev = [(e('knee'), _snd('death_knee')), (e('sword_plant'), _snd('chop')), (e('collapse'), api.K.p('dust_ring', r=20)),
          (e('ash'), _snd('death_ash')), (e('ash'), api.K.p('ember_burst'))]
    _write(W, 'death', 'death', 'Death (PLAN §3: knees buckle, sword planted, visor fades, wings sag, collapse, ash).', [], ev)


SERVICES = [
    api.Service('intro', 'intro', build_intro, dict(api.CLIPS['intro'][2])),
    api.Service('death', 'death', build_death, dict(api.CLIPS['death'][2])),
    api.Service('t1', 't1_wings', build_t1, dict(api.CLIPS['t1_wings'][2])),
    api.Service('t2', 't2_abyss', build_t2, dict(api.CLIPS['t2_abyss'][2])),
]
assert [s.name for s in SERVICES] == list(api.SEQS)
