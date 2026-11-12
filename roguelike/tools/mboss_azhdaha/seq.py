"""S2-S: the intro E (service 26, clip intro 150 t) and the death D (service 24, clip death 120 t + the scale-out to
140) (plan.md 5 E, D, 4.13; s2.md 11). Built on S1-MOD's working stub: AZ:seq/intro/** and AZ:seq/death/** on the
framework clocks (#mbT from intro_tick / death_tick; the clip tick = #mbT - 1, the core plays the clip in its spawn /
death_start), with the per-fight seal props (6 steles r 8 around the spawn, the prism UUID 0x80; theme.md 4.2 POINTS),
the beats of the footage ([v1] I: sealed, eyes, two steles shatter, the seal shatters, the close-up roar), the typed
lines, the music start at the roar, the blast push ring; the death's falls, the seal re-forming, the petrify and the
scale-out. The core (core.py) owns the intro end (the fight starts at the clip end + 1), the death clean-up (hazards,
fields, emitters, orbs, shards, the brand, the HUD; the music stops in the framework before death_start) and the phase
flow around these (pair roll in prep, phases / floors / music in svc/*, the brand in brand.py).

The intro glyph circle is decor (Change note 1 table: 'E intro glyph circle | decor (no hazard)'); nothing here hurts.
"""
from . import api as A
from . import h_ps as H
from .api import L

PATTERNS = []
K = A.K
NS = A.NS
BODY = A.BODY
INTRO = A.CLIPS['intro']['events']
DEATH = A.CLIPS['death']['events']
DEATH_LEN = A.clip_len('death')
SCALE_OUT = (DEATH_LEN, A.BOSS['death'])            # 120 -> 140
LINE_INTRO = '인간 주제에, 선을 넘지 마라!'
LINE_DEATH0 = '난… 사라지지 않아!'
LINE_DEATH80 = '모…락스…!'
SEAL_TAG = 'rlk_mb_az_seal'
PRISM_UUID = '[I;1380731725,1096434688,-2147483648,128]'   # 524c4b4d-415a-4400-8000-000000000080 (Rig decision change 3)
# the two steles that shatter at crack1 / crack2: the player arrives at the south edge looking north, so [v1] I's "left
# foreground stele" (first) is the south-west one (bearing 210, index 3) and the "right" one the south-east (150, index 2)
SHATTER = (3, 2)
DRONE = (0, 40, 80)                                 # snd/intro_drone loops every 40 t while sealed
THUMPS = (10, 50, 90)                               # the sealed body's heartbeat thumps (besides eyes / rise / land)
GLYPH_TELL, GLYPH_HOLD = 20, INTRO['seal'] - 20     # the floor glyph circle draws in 20 t, stays until the seal shatters
assert set(INTRO) >= {'eyes', 'rise', 'crack1', 'crack2', 'seal', 'land', 'roar', 'blast'}
assert set(DEATH) >= {'chin', 'tail', 'last', 'head', 'still'}


def _pos(p):
    return ' '.join(L.num(float(v), 3) for v in p[:3])


def _pt(p):
    x, _y, z = A.REST[p]
    return x, z


def _prism(tag_extra):
    """The gold glyph prism (UUID 0x80) standing on the floor point here (the kit model stands on the prop)."""
    tags = f'"rlk_room","rlk_mb_aux","{SEAL_TAG}","{SEAL_TAG}_prism"{tag_extra}'
    return [f'kill @e[type=minecraft:item_display,tag={SEAL_TAG}_prism]',
            f'summon minecraft:item_display ~ ~ ~ {{UUID:{PRISM_UUID},Tags:[{tags}],billboard:"fixed",'
            'brightness:{block:15,sky:15},item:{id:"minecraft:yellow_stained_glass",count:1}}',
            f'execute as @e[type=minecraft:item_display,tag={SEAL_TAG}_prism] run {K.prop("seal_prism")}']


def intro(g):
    st = A.THEME['seal_steles']
    tags = f'"rlk_room","rlk_mb_aux","{SEAL_TAG}"'
    setup = ['# The intro dressing (plan 5 E, [v1] I): 6 seal steles r 8 around the spawn (facing the centre), the gold glyph',
             '# prism (UUID 0x80) standing at the centre, the floor glyph circle (decor). Per-fight entities (rlk_mb_aux).',
             f'kill @e[tag={SEAL_TAG}]']
    for k, (x, y, z, yaw) in enumerate(st):
        setup.append(f'execute in minecraft:overworld positioned {_pos((x, y, z))} run summon minecraft:item_display '
                     f'~ ~1.6 ~ {{Tags:[{tags},"{SEAL_TAG}_s{k}"],Rotation:[{L.num(float(yaw))}f,0f],billboard:"fixed",'
                     'brightness:{block:13,sky:15},item:{id:"minecraft:chiseled_tuff_bricks",count:1}}')
    setup += [f'execute as @e[type=minecraft:item_display,tag={SEAL_TAG}] run {K.prop("seal_stele")}']
    setup += [f'execute in minecraft:overworld positioned {_pos(A.THEME["seal_prism"])} run {ln}' for ln in _prism('')]
    setup += [f'execute in minecraft:overworld positioned {_pos(A.THEME["seal_prism"])} run '
              f'{K.tele_glyph_circle(9.0, GLYPH_TELL, hold=GLYPH_HOLD)}']
    g.sw('intro/setup', setup)
    c = lambda t: t + 1                                                  # noqa: E731  #mbT of clip tick t
    at = lambda t, cmd: f'execute if score #mbT mb matches {c(t)} run {cmd}'   # noqa: E731
    fl, fr = _pt('paw_fl'), _pt('paw_fr')
    tick = ['# Intro beats on #mbT (clip tick = #mbT - 1; untargetable until the core ends the intro at the clip end).']
    tick += [at(t, K.snd('intro_drone')) for t in DRONE]
    tick += [at(t, K.snd('intro_thump')) for t in THUMPS]
    tick += [at(INTRO['eyes'], f'function {NS}seq/intro/eyes'),
             at(INTRO['rise'], K.snd('intro_thump')),
             at(INTRO['crack1'], f'function {NS}seq/intro/shatter_{SHATTER[0]}'),
             at(INTRO['crack2'], f'function {NS}seq/intro/shatter_{SHATTER[1]}'),
             at(INTRO['seal'], f'function {NS}seq/intro/seal'),
             at(INTRO['land'], f'function {NS}seq/intro/land'),
             at(INTRO['roar'], f'function {NS}seq/intro/roar'),
             at(INTRO['blast'], f'function {NS}seq/intro/blast')]
    g.sw('intro/tick', tick)
    g.sw('intro/eyes', ['# The eyes light (the rig\'s red eyes; [v1] I +25): a low growl and the gold parts lit inside the seal.',
                        g.glow(True), g.sound('entity.ravager.ambient', 0.8, 0.5), K.snd('intro_thump')])
    for k in SHATTER:
        g.sw(f'intro/shatter_{k}', [f'# Seal stele {k} shatters into chunks.',
                                    f'execute at @e[type=minecraft:item_display,tag={SEAL_TAG}_s{k}] positioned ~ ~-1.6 ~ run {K.fx("stele_shatter")}',
                                    f'execute at @e[type=minecraft:item_display,tag={SEAL_TAG}_s{k}] run {K.snd("stele_break")}',
                                    f'kill @e[type=minecraft:item_display,tag={SEAL_TAG}_s{k}]'])
    g.sw('intro/seal', ['# The seal shatters: the prism breaks with a white flash; the glyph circle goes with it.',
                        f'execute at @e[type=minecraft:item_display,tag={SEAL_TAG}_prism] run {K.fx("prism_shatter")}',
                        K.snd('seal_shatter'), K.hud('flash_white'), g.glow(False),
                        f'kill @e[type=minecraft:item_display,tag={SEAL_TAG}_prism]'])
    g.sw('intro/land', ['# The fores land after the rear-up.', K.snd('intro_thump'),
                        *H.at_local(*fl, g.fxe('footfall', 5)), *H.at_local(*fr, g.fxe('footfall', 5)),
                        *H.at_local(0, fl[1], K.fx('dust'))])
    g.sw('intro/roar', ['# The roar: radial gold leaves, a shock dome, the line, the phase-1 music.',
                        *H.at_local(0, 2.0, K.fx('gold_leaves')), K.fx('shock_dome', r=12.0), K.snd('intro_roar'),
                        g.line(LINE_INTRO), g.music(1)])
    g.sw('intro/blast', ['# The blast: a push-only ring r 8 (no damage) with its dome; the remaining steles crumble.',
                         A.fw('push/ring', '{r:80,to:85,kb:4}'), K.fx('shock_dome', r=8.0), K.snd('roar_ring'),
                         f'execute as @e[type=minecraft:item_display,tag={SEAL_TAG}] at @s positioned ~ ~-1.6 ~ run {K.fx("stele_shatter")}',
                         f'execute at @e[type=minecraft:item_display,tag={SEAL_TAG},limit=1] run {K.snd("stele_break")}',
                         f'kill @e[type=minecraft:item_display,tag={SEAL_TAG}]'])


def death(g):
    d = lambda t, cmd: f'execute if score #mbT mb matches {t + 1} run {cmd}'   # noqa: E731
    g.sw('death/start', ['# The death (plan 5 D), clip tick 0: the first line, the sting (the framework stopped the music).',
                         g.line(LINE_DEATH0), K.snd('death_sting'), g.sound('entity.ravager.hurt', 0.8, 0.5)])
    g.sw('death/tick', ['# Death beats on #mbT (clip tick = #mbT - 1); the seal and the petrify at "still"; the scale-out',
                        f'# {SCALE_OUT[0]} -> {SCALE_OUT[1]}.',
                        d(DEATH['chin'], f'function {NS}seq/death/chin'),
                        d(DEATH['tail'], f'function {NS}seq/death/tail'),
                        d(DEATH['last'], g.line(LINE_DEATH80)),
                        d(DEATH['head'], f'function {NS}seq/death/head'),
                        d(DEATH['still'], f'function {NS}seq/death/seal'),
                        d(DEATH['still'] + 4, K.fx('petrify_pulse')),
                        d(SCALE_OUT[0], f'function {NS}seq/death/out')])
    nose = _pt('nose')
    g.sw('death/chin', ['# The chin hits the floor.', K.snd('death_fall'), *H.at_local(nose[0], nose[1], K.fx('dust'))])
    g.sw('death/tail', ['# The tail falls flat.', g.sound('block.deepslate.break', 1.0, 0.5), g.sound('entity.ravager.step', 1.0, 0.5),
                        *H.at_local(0, -9.0, K.fx('dust'))])
    g.sw('death/head', ['# The head falls for the last time.', K.snd('death_fall'), *H.at_local(nose[0], nose[1], K.fx('dust'))])
    g.sw('death/seal', ['# The seal re-forms around the body (the gold glyph prism again, UUID 0x80) and the rig petrifies.',
                        f'function {A.rig_fn("look/petrify")}', K.fx('seal_reform'), K.snd('death_seal'),
                        g.sound('block.amethyst_block.resonate', 1.0, 0.6),
                        *[f'execute at @s positioned ~ {L.num(float(A.CY), 2)} ~ run {ln}' for ln in _prism('')]])
    g.sw('death/out', [f'# The rig scales out over {SCALE_OUT[1] - SCALE_OUT[0]} t inside the seal; gold motes.',
                       'execute as @e[type=minecraft:item_display,tag=rlk_mb_azhdaha_part] run data merge entity @s '
                       f'{{start_interpolation:0,interpolation_duration:{SCALE_OUT[1] - SCALE_OUT[0]},'
                       'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
                       'scale:[0f,0f,0f]}}',
                       K.fx('gold_motes'), K.fx('petrify_pulse')])


def emit(g):
    intro(g)
    death(g)
