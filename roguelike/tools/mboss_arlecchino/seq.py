"""Sequences of 아를레키노 (Arlecchino): the battle-entry intro, the phase-2 transition t_p2, death (S:ar/PLAN.md §3).
OWNER: S2 (rig + sequences).

Contract (api.Service): SERVICES lists one api.Service per api.SEQS name; build(W) writes only seq/<name>/{start,tick,cancel}
(W = api.Writer('S2seq', api.OWN['S2seq'])). The core (S3) sets #sq kn 0 and calls start (@s = the body, at it), then adds 1
to #sq and calls tick every tick; rig/tick runs after the module logic, so the clip shows tick e when #sq = e and every
event below is the clip's event tick (api.ev). A sequence sets #sqdone kn 1 at its clip's end. cancel is called with no
executor (cleanup, death, reload) and only removes what the sequence made.

Division of work with the core (contract §3.4, PLAN §3): the core owns the invulnerability (rlk_mb_inv), cine, music (phase 1
at intro 136, phase 2 after t_p2), the phase switch, repool and the death finish; the sequences own the rig clip, every sound,
effect and dialog line of PLAN §3 (kit recipes through api.K, empty until the kit exists, wrapped with api.lines), the
titles (mboss_lib.title at intro 'title' and t_p2 'title'), the intro push ring (mboss_lib.push_ring, no damage), t_p2's
blindness and the arena look job `crimson` at 'dark' (api.arena_look), and the three white flame-wisps of the intro (markers
tagged rlk_room rlk_mb_aux rlk_kn_prop rlk_kn_wisp rlk_kn_wisp_<i>, dressed by the kit prop `wisp`): they circle her during
the tea (0-34), flee to the rim posts api.WISP_POSTS (35-55) and stay there for the fight; t_p2 turns two of them red at
'dark' (kit wisp_turn c 2), death turns them white again at 'wisps'. The framework's rlk_mb_aux cleanup removes them with the
fight; seq/intro/cancel removes them too. Looks inside the sequences are keyed in the clips themselves
(tools/arlecchino_clips.mjs: the tea props, the form swap at t_p2 'swap'); t_p2 sets the crimson scythe glow at its start
and the normal glow at its end.
"""
import math

from . import api

L = api.L
OBJ = api.OBJ
AT = 'at @s'
ANCHOR = '@e[type=marker,tag=rlk_kn_anchor,limit=1]'
WISP = 'rlk_kn_wisp'
WISP_TAGS = ['rlk_room', 'rlk_mb_aux', 'rlk_kn_prop', WISP]
MOON = 'rlk_kn_moon'


def _at(t, cmd, ctx=AT):
    """One line on the sequence clock: cmd at #sq = t (cmd may already be an execute ... run ...)."""
    if not cmd:
        return None
    if cmd.startswith('execute '):
        return f'execute if score #sq {OBJ} matches {t} {cmd[8:]}'
    return f'execute if score #sq {OBJ} matches {t} {ctx} run {cmd}' if ctx else f'execute if score #sq {OBJ} matches {t} run {cmd}'


def _snd(name):
    return api.K.snd(name)


def _fx_at(t, anchor, line):
    """A kit line at a rig anchor of the current clip tick: rig/anchor/<name> moves the marker, the effect runs at it."""
    if not line:
        return []
    return [(t, api.rig(f'anchor/{anchor}')), (t, f'execute at {ANCHOR} rotated as @s run {line}', None)]


def _end(clip):
    n = api.CLIPS[clip][0]
    return f'execute if score #sq {OBJ} matches {n}.. run scoreboard players set #sqdone {OBJ} 1'


def _write(W, name, clip, head, start_extra, events, cancel_extra=()):
    ev = sorted(events, key=lambda e: int(str(e[0]).split('..')[0]))
    W.w(f'seq/{name}/start', [f'# {head} @s = the body, at it; #sq {OBJ} = 0. Plays the rig clip {clip} ({api.CLIPS[clip][0]} t).',
                              f'scoreboard players set #sqdone {OBJ} 0', api.play(clip), *[c for c in start_extra if c]])
    tick = [f'# {head} @s = the body; #sq {OBJ} 1.. = the clip tick shown this game tick.']
    for t, cmd, *ctx in ev:
        assert all(0 <= int(x) <= api.CLIPS[clip][0] for x in str(t).split('..')), (name, t)
        line = _at(t, cmd, ctx[0] if ctx else AT)
        if line:
            tick.append(line)
    tick.append(_end(clip))
    W.w(f'seq/{name}/tick', tick)
    W.w(f'seq/{name}/cancel', [f'# {head} Cancel (no executor; idempotent).', *[c for c in cancel_extra if c]] or ['# nothing lingers'])


def _num(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


# ---- the wisps (PLAN §3.1 E0-E1): offsets from the body, which stands at the arena centre for the intro -------------------------
WISP_R, WISP_SPIN = 1.3, 7.0                     # circle radius (b), degrees per tick (counter-clockwise from above)


def _wisp_circle(i, t):
    a = math.radians(120 * i + WISP_SPIN * t)
    return (WISP_R * math.cos(a), .6 + .3 * math.sin(.3 * t + 2.1 * i), WISP_R * math.sin(a))


def _wisp_post(i):
    """The wisp's resting point, from her at the arena centre: over its rim post (the theme's POINTS['wisps'], S1 R5:
    the post is solid y 201-203; she stands at the marker, summoned at the block centre CX + 0.5, CZ + 0.5). Without the
    theme: api.WISP_POSTS at 0.7 b (S5 review AR-04: the old 0.7 b point sat inside the post)."""
    theme = L.theme_module(api.ARENA_SPEC['theme'])
    pts = getattr(theme, 'POINTS', {}).get('wisps') if theme else None
    if pts:
        x, y, z = pts[i][:3]
        return (x - (api.CX + .5), y - api.CY, z - (api.CZ + .5))
    bearing, r = api.WISP_POSTS[i]
    b = math.radians(bearing)
    return (r * math.sin(b), .7, -r * math.cos(b))              # compass bearing: 0 north (-z), 90 east (+x)


def _wisp_tp(i, p):
    return f'tp @e[type=marker,tag={WISP}_{i},limit=1] ~{_num(p[0])} ~{_num(p[1])} ~{_num(p[2])}'


def build_intro(W):
    e = lambda k: api.ev('intro', k)
    flee0, flee1 = e('flee'), e('flee') + 20
    ev = [(4, _snd('wisp_chime')), (20, _snd('wisp_chime')), (e('sip'), _snd('tea_sip')),
          (e('embers'), _snd('cup_embers')), (e('flee'), _snd('wisps_flee')),
          (e('reach'), _snd('ember_reach')), (e('vortex'), _snd('scythe_vortex')), (e('form'), _snd('scythe_form')),
          (e('blade'), _snd('blade_ignite')), (e('title'), _snd('intro_title')),
          (e('title'), L.title(*api.TITLE_P1, api.TITLE_COLOR[1])), (e('title'), api.K.hud('line', id=api.LINE_OF['intro'][0])),
          (e('twirl'), _snd('twirl')), (e('ring'), _snd('twirl_ring')), (e('ring'), api.K.p('spin_ring', r=25, c=api.C_PYRO)),
          (e('flip'), _snd('flip')), (e('set'), _snd('stance')), (e('beat'), _snd('heartbeat')),
          (e('push'), L.push_ring(4.0, 6))]
    # effects at the rig's anchor points of the clip tick
    ev += _fx_at(e('embers'), 'hand_r', api.K.p('embers_puff')) + _fx_at(e('embers'), 'hand_l', api.K.p('embers_puff'))
    for t in (e('reach'), e('reach') + 4):
        ev += _fx_at(t, 'palm_r', api.K.p('embers_puff'))
    ev += _fx_at(e('vortex'), 'palm_r', api.K.p('scythe_form'))
    ev += _fx_at(e('blade'), 'blade_r', api.K.p('embers_puff'))
    ev += _fx_at(e('twirl'), 'hand_r', api.K.p('twirl_ring'))
    ev += _fx_at(e('flip'), 'blade_r', api.K.p('slash_arc', r=20, yaw=0, pitch=0, roll=90, c=api.C_BOL))
    ev += _fx_at(e('stance'), 'blade_r', api.K.p('embers_puff')) + _fx_at(e('set'), 'blade_r', api.K.p('embers_puff'))
    # the wisps: circle her while she drinks, flee to the rim posts (ease-out) and stay
    for t in range(1, flee0 + 1):
        for i in range(3):
            ev.append((t, _wisp_tp(i, _wisp_circle(i, t))))
    for t in range(flee0 + 1, flee1):
        u = (t - flee0) / (flee1 - flee0)
        k = 1 - (1 - u) ** 2
        for i in range(3):
            a, b = _wisp_circle(i, flee0), _wisp_post(i)
            hop = .8 * math.sin(math.pi * u)
            ev.append((t, _wisp_tp(i, tuple(a[j] + (b[j] - a[j]) * k + (hop if j == 1 else 0) for j in range(3)))))
    # at the posts from flee + 20 to the end (a range, so a reload that starts the intro and steps #sq to its end in one tick
    # still finds the wisps at their posts: start, #sq kn 150, tick)
    for i in range(3):
        ev.append((f'{flee1}..{api.CLIPS["intro"][0]}', _wisp_tp(i, _wisp_post(i))))
    start = [f'kill @e[type=marker,tag={WISP}]']
    for i in range(3):
        x, y, z = _wisp_circle(i, 0)
        start.append(f'summon minecraft:marker ~{_num(x)} ~{_num(y)} ~{_num(z)} {{Tags:{str(WISP_TAGS + [f"{WISP}_{i}"]).replace(chr(39), chr(34)).replace(" ", "")}}}')
        prop = api.K.prop('wisp', c=api.C_PYRO)
        if prop:
            start.append(f'execute as @e[type=marker,tag={WISP}_{i},limit=1] at @s run {prop}')
    start.append(api.rig('look/props/tea'))
    _write(W, 'intro', 'intro', 'Intro (PLAN §3.1: tea, cup to embers, wisps flee, reach, crimson vortex, the scythe forms, hold + title, '
           'the 360 twirl, flip, stance, push ring).', start, ev, [f'kill @e[type=marker,tag={WISP}]'])


def build_t_p2(W):
    e = lambda k: api.ev('t_p2', k)
    ev = [(e('kneel'), _snd('t_stagger')), (e('pillar'), _snd('t_pillar')), (e('pillar'), api.K.p('pillar', r=12)),
          (e('dark'), _snd('t_dark')), (e('dark'), 'effect give @a[tag=player] minecraft:blindness 1 0 true', None),
          (e('dark'), api.arena_look('crimson'), None),
          (e('swap'), _snd('t_swap')), (e('swap'), api.K.p('pillar', r=16)),
          # the form swap is hidden (ref/p2_T_transition.jpg v4 19.5-20.5: a crimson-white burst with blade shards hides
          # her): a flame cocoon closes 8 t before the swap and peels away from the bottom up after it
          (e('swap') - 8, _snd('scythe_vortex')), (e('swap') - 8, f'execute at @s rotated as @s rotated ~ 0 run {api.K.p("shroud")}' if api.K.p('shroud') else None, None),
          (e('scythes'), _snd('t_scythes')), (e('title'), _snd('t_title')),
          (e('title'), L.title(*api.TITLE_P2, api.TITLE_COLOR[2])), (e('title'), api.K.hud('line', id=api.LINE_OF['t_p2'][0])),
          (e('launch'), _snd('t_launch')), (e('launch'), api.K.p('leap_flare')),
          (e('launch'), f'kill @e[type=marker,tag={MOON}]', None), (e('end') - 10, api.rig('look/glow/normal'))]
    ev += _fx_at(e('kneel'), 'chest', api.K.p('embers_puff'))
    ev += _fx_at(e('swap'), 'chest', api.K.p('shroud_burst'))
    for i in (1, 2):                                               # two of the three wisps turn red (wiki)
        turn = api.K.p('wisp_turn', c=api.C_BOL)
        if turn:
            ev.append((e('dark') + 6 * i, f'execute as @e[type=marker,tag={WISP}_{i},limit=1] at @s run {turn}', None))
    # the red moon halo above her while she rises (kit prop moon_halo on a marker)
    moon = api.K.prop('moon_halo')
    ev.append((e('rise'), f'summon minecraft:marker ~ ~7 ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_kn_prop","{MOON}"]}}'))
    if moon:
        ev.append((e('rise'), f'execute as @e[type=marker,tag={MOON},limit=1] at @s run {moon}', None))
    for k in ('legs1', 'legs2', 'legs3'):
        ev += [(e(k), _snd('t_legs'))] + _fx_at(e(k), 'spine', api.K.p('legs_burst'))
    ev += _fx_at(e('scythes'), 'hand_r', api.K.p('scythe_form')) + _fx_at(e('scythes'), 'hand_l', api.K.p('scythe_form'))
    _write(W, 't_p2', 't_p2', 'Transition T (PLAN §3.2: stagger, kneel, the crimson pillar, blackout + the crimson arena, rise, the form '
           'swap, six blade legs, twin scythes, title, launch).', [api.rig('look/glow/crimson')], ev, [f'kill @e[type=marker,tag={MOON}]'])


def build_death(W):
    e = lambda k: api.ev('death', k)
    ev = [(e('lower'), _snd('death_lower')), (e('flames'), _snd('death_flames')), (e('flames'), api.K.p('death_flames')),
          (e('gone'), _snd('death_gone')), (e('gone'), api.K.p('final_burst', r=20))]
    ev += _fx_at(e('fade'), 'blade_r', api.K.p('embers_puff')) + _fx_at(e('fade'), 'blade_l', api.K.p('embers_puff'))
    ev += _fx_at(e('gone'), 'chest', api.K.p('embers_puff'))
    ev.append((e('end'), api.rig('state/hidden')))                  # the body ends hidden (the core finishes the fight)
    turn = api.K.p('wisp_turn', c=api.C_PYRO)
    if turn:
        ev.append((e('wisps'), f'execute as @e[type=marker,tag={WISP}] at @s run {turn}', None))
    _write(W, 'death', 'death', 'Death (PLAN §3.3: no last words; she lowers both scythes, they dissolve into embers, she straightens, '
           'crimson flames climb her, she vanishes in a flame burst; the wisps turn white again; the rig ends hidden).', [], ev)


SERVICES = [
    api.Service('intro', 'intro', build_intro, dict(api.CLIPS['intro'][2])),
    api.Service('t_p2', 't_p2', build_t_p2, dict(api.CLIPS['t_p2'][2])),
    api.Service('death', 'death', build_death, dict(api.CLIPS['death'][2])),
]
assert [s.name for s in SERVICES] == list(api.SEQS)
