"""S2-S: the intro E (service 26, clip intro 150 t) and the death D (service 24, clip death 120 t + the scale-out to
140) (plan.md 5 E, D; s2.md 11). WORKING STUB by S1-MOD (ownership passes to S2-S at I1): AZ:seq/intro/** and
AZ:seq/death/** on the framework clocks (#mbT from intro_tick / death_tick; the clip tick = #mbT - 1, the core plays
the clip in its spawn / death_start), with the per-fight seal props (6 steles r 8 around the spawn, the prism UUID
0x80, theme.md 4.2 POINTS), the beats, the typed lines, the music start at the roar, the blast push ring; stand-in
kit calls. The core (core.py) owns the intro end (the fight starts at the clip end + 1) and the death clean-up."""
from . import api as A
from .api import L

PATTERNS = []
NS = A.NS
BODY = A.BODY
ARENA_M = A.ARENA_M
INTRO = A.CLIPS['intro']['events']
DEATH = A.CLIPS['death']['events']
DEATH_LEN = A.clip_len('death')
SCALE_OUT = (DEATH_LEN, A.BOSS['death'])            # 120 -> 140
LINE_INTRO = '인간 주제에, 선을 넘지 마라!'
LINE_DEATH0 = '난… 사라지지 않아!'
LINE_DEATH80 = '모…락스…!'
SEAL_TAG = 'rlk_mb_az_seal'
PRISM_UUID = '[I;1380731725,1096434688,-2147483648,128]'
SHATTER = (0, 3)                                    # the two steles that shatter at crack1 / crack2


def _pos(p):
    return ' '.join(L.num(float(v), 3) for v in p[:3])


def emit(g):
    st = A.THEME['seal_steles']
    tags = f'"rlk_mb_aux","{SEAL_TAG}"'
    setup = ['# The intro dressing (WORKING STUB, S1-MOD): 6 seal steles r 8 around the spawn (facing the centre) and the',
             '# gold glyph prism (UUID 0x80) at the centre; the floor glyph circle decal. Per-fight entities (rlk_mb_aux).',
             f'kill @e[tag={SEAL_TAG}]']
    for k, (x, y, z, yaw) in enumerate(st):
        setup.append(f'execute in minecraft:overworld positioned {_pos((x, y, z))} run summon minecraft:item_display '
                     f'~ ~1.6 ~ {{Tags:[{tags},"{SEAL_TAG}_s{k}"],Rotation:[{L.num(float(yaw))}f,0f],billboard:"fixed",'
                     'brightness:{block:13,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],'
                     'right_rotation:[0f,0f,0f,1f],scale:[1.4f,3.2f,0.5f]},item:{id:"minecraft:chiseled_tuff_bricks",count:1}}')
    setup += [f'execute as @e[type=minecraft:item_display,tag={SEAL_TAG}] run {A.K.prop("seal_stele")}',
              f'execute in minecraft:overworld positioned {_pos(A.THEME["seal_prism"])} run summon minecraft:item_display ~ ~4.2 ~ {{UUID:{PRISM_UUID},Tags:[{tags},"{SEAL_TAG}_prism"],'
              'billboard:"fixed",brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],'
              'right_rotation:[0f,0f,0f,1f],scale:[11f,9f,13f]},item:{id:"minecraft:yellow_stained_glass",count:1}}',
              f'execute as @e[type=minecraft:item_display,tag={SEAL_TAG}_prism] run {A.K.prop("seal_prism")}',
              f'execute in minecraft:overworld positioned {_pos(A.THEME["seal_prism"])} run {A.K.tele_disc(9.0, 140, 5, hold=3)}']
    g.sw('intro/setup', setup)
    c = lambda t: t + 1                                                  # noqa: E731  #mbT of clip tick t
    at = lambda t, cmd: f'execute if score #mbT mb matches {c(t)} run {cmd}'   # noqa: E731
    tick = ['# Intro beats on #mbT (clip tick = #mbT - 1; untargetable until the core ends the intro at the clip end).',
            at(0, A.K.snd('intro_drone')), at(INTRO['eyes'], A.K.snd('intro_thump')),
            at(INTRO['rise'], A.K.snd('intro_thump')),
            at(INTRO['crack1'], f'function {NS}seq/intro/shatter_{SHATTER[0]}'),
            at(INTRO['crack2'], f'function {NS}seq/intro/shatter_{SHATTER[1]}'),
            at(INTRO['seal'], f'function {NS}seq/intro/seal'),
            at(INTRO['land'], A.K.snd('intro_thump')),
            at(INTRO['roar'], f'function {NS}seq/intro/roar'),
            at(INTRO['blast'], f'function {NS}seq/intro/blast')]
    g.sw('intro/tick', tick)
    for k in SHATTER:
        g.sw(f'intro/shatter_{k}', [f'# Seal stele {k} shatters into chunks.',
                                    f'execute at @e[type=minecraft:item_display,tag={SEAL_TAG}_s{k}] run {A.K.fx("stele_shatter")}',
                                    f'execute at @e[type=minecraft:item_display,tag={SEAL_TAG}_s{k}] run {A.K.snd("stele_break")}',
                                    f'kill @e[type=minecraft:item_display,tag={SEAL_TAG}_s{k}]'])
    g.sw('intro/seal', ['# The seal shatters: the prism breaks with a white flash.',
                        f'execute at @e[type=minecraft:item_display,tag={SEAL_TAG}_prism] run {A.K.fx("prism_shatter")}',
                        A.K.snd('seal_shatter'), A.K.hud('flash_white'),
                        f'kill @e[type=minecraft:item_display,tag={SEAL_TAG}_prism]'])
    g.sw('intro/roar', ['# The roar: radial gold leaves, the line, the phase-1 music.',
                        A.K.fx('gold_leaves'), A.K.snd('intro_roar'), g.line(LINE_INTRO), g.music(1)])
    g.sw('intro/blast', ['# The blast: a push-only ring r 8 (no damage); the remaining steles crumble.',
                         A.fw('push/ring', '{r:80,to:85,kb:4}'),
                         f'execute as @e[type=minecraft:item_display,tag={SEAL_TAG}] at @s run {A.K.fx("stele_shatter")}',
                         f'kill @e[type=minecraft:item_display,tag={SEAL_TAG}]'])
    # death
    g.sw('death/start', ['# The death (WORKING STUB, S1-MOD), clip tick 0: the first line, the music stops with a sting.',
                         g.line(LINE_DEATH0), A.fw('music/stop'), g.sound('block.beacon.deactivate', 1.0, 0.6),
                         A.K.snd('death_sting')])
    d = lambda t, cmd: f'execute if score #mbT mb matches {t + 1} run {cmd}'   # noqa: E731
    g.sw('death/tick', ['# Death beats on #mbT (clip tick = #mbT - 1); the scale-out 120 -> 140.',
                        d(DEATH['chin'], g.sound('entity.iron_golem.death', 1.0, 0.5)),
                        d(DEATH['tail'], g.sound('entity.ravager.death', 1.0, 0.6)),
                        d(DEATH['last'], g.line(LINE_DEATH80)),
                        d(DEATH['head'], A.K.snd('death_fall')),
                        d(DEATH['still'], f'function {NS}seq/death/seal'),
                        d(SCALE_OUT[0], f'function {NS}seq/death/out')])
    g.sw('death/seal', ['# The seal re-forms and the rig petrifies.', f'function {A.rig_fn("look/petrify")}',
                        A.K.fx('seal_reform'), A.K.fx('petrify_pulse'), A.K.snd('death_seal'),
                        g.sound('block.amethyst_block.resonate', 1.0, 0.6)])
    g.sw('death/out', [f'# The rig scales out over {SCALE_OUT[1] - SCALE_OUT[0]} t.',
                       'execute as @e[type=minecraft:item_display,tag=rlk_mb_azhdaha_part] run data merge entity @s '
                       f'{{start_interpolation:0,interpolation_duration:{SCALE_OUT[1] - SCALE_OUT[0]},'
                       'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
                       'scale:[0f,0f,0f]}}'])
