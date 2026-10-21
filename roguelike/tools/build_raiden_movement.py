"""Raiden blinks (footage A-19, plan rd/plan.md A.2: she never walks; she closes distance only by a blink), with the
release's scatter art restored (rd-sync, user request: "샤샷 하고 흐트러지는 모션").

A blink is 10 t, immune (combat/apply while rdBlink is 1..): she breaks up where she stands into a translucent
silhouette of horizontal fragments, lightning seams and speed streaks that fly back and fade (6 frames), the hidden body
relocates 3 t later, and the same silhouette reforms from scattered fragments at the destination (6 frames) while the
rig fades back in. Sounds as in the release: a trident whoosh on the scatter, a soft wing flap on the reform.
The rig is hidden with rig/state/hidden (every part scaled to 0 where it stands; nothing is ever moved below the
floor); the next clip shows it again (blink_in / t_blink_in when no pattern clip took over first).

    movement/blink_start   @s = boss: blink to the rlk_rd_blink_dest marker if one exists, else in front of the player
                           (core blink_relocate). A blink already running is not restarted.
    movement/blink_to      @s = boss, the execution position is the destination (pulled in to radius 20).
    movement/blink_tick    core tick while rdBlink 1..: 1..9 is the blink (relocation at 4, the rig fades in from 6,
                           over at 10); 20..29 is a plain immune hold that patterns set themselves (몽상의 일심 sets 24).
    movement/depart|arrive the scatter / reform art at @s with @s's yaw (Shogun or Tenma silhouette by rdPhase); never
                           move her. 찰나의 포영, 몽상의 일심 and the transformation use them for their own relocations.
    movement/world         world tick: the art frames (rdMvAge), killed after frame 5.
    movement/cleanup       pause / exhausted / death: no destination marker, no blink, no art.

Pack: assets/rlk/{models,items}/raiden/fx_movement/{shogun,tenma}_0..5 (frame 0 whole, frame 5 scattered), built from
the shared RGBA swatches rlk:raiden/fx/* (build_raiden_materials.py); no new texture.
"""
from pathlib import Path
import argparse
import json
import math
import shutil

SCALE = 8
COLORS = {name: 'rlk:raiden/fx/' + name for name in
          ('void', 'violet', 'lavender', 'white', 'cyan', 'shadow', 'violet_dense', 'glow', 'afterglow', 'pearl', 'blue')}
# The release's silhouette (head, torso, arms, legs) fitted to the new rig: the Shogun's head top is 2.07 b (release
# 2.4 b), so the body boxes scale by 0.86; the Tenma core figure is the same body floating 1.0 b up (rest pose of the
# rig, rd/plan.md C.2) with her giant arm and glaive on her right, the fan of thin arms on her left, the disc halo and
# the gauntlet hands. Points below are the rig's rest pose (raiden_clips restPose('t')), ghost frame: +X her left,
# +Z forward (the rig frame's -Z).
BODY = [((0, 2.09, 0), (.61, .61, .58)), ((0, 1.38, 0), (.62, .84, .34)), ((-.49, 1.25, .025), (.25, .83, .25)),
        ((.49, 1.25, .025), (.25, .83, .25)), ((-.16, .45, 0), (.27, .86, .30)), ((.16, .45, 0), (.27, .86, .30))]
FIT = 0.86
TENMA_LIFT = 1.0
G = lambda p: (p[0], p[1], -p[2])                  # rig rest point -> ghost frame
TENMA_LIMBS = [  # (polyline in rig rest coordinates, thickness b)
    ([(-1.25, 3.55, .6), (-3.0, 2.59, .67), (-1.52, 2.23, -.63)], .34),          # giant arm: shoulder ball, elbow, fist
    ([(-3.18, 1.87, -.86), (3.27, 1.8, -1.7)], .12),                              # the glaive across the front
    ([(.42, 2.62, .36), (1.01, 3.74, .65), (1.15, 4.85, .52)], .16),              # thin arms, fanned up on her left
    ([(.48, 2.44, .4), (1.59, 3.05, .67), (2.44, 3.67, .28)], .16),
    ([(.46, 2.26, .36), (1.74, 2.19, .57), (2.65, 2.52, -.01)], .16),
]
DISC = ((0, 2.95, -.40), .85)                 # disc halo behind her head (centre, radius)
GAUNTLETS = [(.95, .7, 1.25), (-.95, .7, 1.25)]


def box(center, extent, color):
    return {'from': [round(8 + (center[i] - extent[i] / 2) * 16 / SCALE, 5) for i in range(3)],
            'to': [round(8 + (center[i] + extent[i] / 2) * 16 / SCALE, 5) for i in range(3)],
            'shade': False,
            'faces': {face: {'texture': '#' + color, 'uv': [0, 0, 16, 16]}
                      for face in ('north', 'south', 'east', 'west', 'up', 'down')}}


def stroke(mesh, points, width, color, core=False):
    for a, b in zip(points, points[1:]):
        steps = max(1, math.ceil(math.dist(a, b) / .14))
        for j in range(steps):
            p = [a[i] + (b[i] - a[i]) * (j + .5) / steps for i in range(3)]
            extent = [abs(b[i] - a[i]) / steps + width for i in range(3)]
            mesh.append(box(p, extent, color))
            if core:
                thin = [abs(b[i] - a[i]) / steps + width * .27 for i in range(3)]
                thin[2] = extent[2] + .01
                mesh.append(box(p, thin, 'white'))


def scatter(seed, sign, amount):
    """The release's fragment drift: sideways by sign, a little up or down, and back (away from her facing)."""
    return [sign * (.35 + seed / 23 * .9) * amount, ((seed % 7) - 3) * .07 * amount, -(.36 + seed / 23 * 1.30) * amount]


def ghost(frame, tenma=False):
    amount = frame / 5
    lift = TENMA_LIFT if tenma else 0
    parts = [((c[0] * FIT, c[1] * FIT + lift, c[2] * FIT), tuple(x * FIT for x in size)) for c, size in BODY]
    mesh = []
    for part, (center, size) in enumerate(parts):
        slices = max(3, math.ceil(size[1] / .11))
        for layer in range(slices):
            seed = (part * 17 + layer * 7) % 23
            sign = -1 if (part + layer) % 2 else 1
            band = size[1] / slices
            base = [center[0], center[1] - size[1] / 2 + (layer + .5) * band, center[2]]
            shift = scatter(seed, sign, amount)
            pos = [base[i] + shift[i] for i in range(3)]
            ext = [size[0] * (1 - .72 * amount), band * .77 * (1 - .3 * amount), size[2] * (1 - .56 * amount)]
            color = ('void', 'violet_dense', 'blue', 'shadow')[(part + layer) % 4]
            if frame >= 4:
                color = 'afterglow' if layer % 2 else 'violet'
            mesh.append(box(pos, ext, color))
            if layer % 2 == 0:
                seam = [pos[0], pos[1] + ext[1] * .35, pos[2] + ext[2] / 2 + .008]
                mesh.append(box(seam, [ext[0] * .76, .018, .028], 'pearl' if frame < 4 else 'lavender'))
            if amount > 0 and layer % 3 == 0:
                # translucent strips make the fragments visibly move away
                tail = [pos[0] - sign * .12 * amount, pos[1] - .025, pos[2] - .28 - amount * .4]
                mesh.append(box(tail, [ext[0] * .34, .026, .38 + amount * .7], 'glow' if frame >= 4 else 'violet'))
    if tenma:
        # the puppet's limbs break into the same fragments, piece by piece along each limb
        for li, (pts, thick) in enumerate(TENMA_LIMBS):
            pts = [G(p) for p in pts]
            for a, b in zip(pts, pts[1:]):
                n = max(2, math.ceil(math.dist(a, b) / .24))
                for j in range(n):
                    seed = (li * 13 + j * 5) % 23
                    sign = -1 if (li + j) % 2 else 1
                    c = [a[i] + (b[i] - a[i]) * (j + .5) / n for i in range(3)]
                    shift = scatter(seed, sign, amount * .8)
                    pos = [c[i] + shift[i] for i in range(3)]
                    ext = [(abs(b[i] - a[i]) / n * .82 + thick) * (1 - .6 * amount) for i in range(3)]
                    color = ('violet_dense', 'void', 'shadow', 'blue')[(li + j) % 4] if frame < 4 else ('afterglow', 'violet')[j % 2]
                    mesh.append(box(pos, ext, color))
                    if j % 3 == 1 and amount > 0:
                        mesh.append(box([pos[0], pos[1], pos[2] - .3 - amount * .5], [ext[0] * .3, .024, .4 + amount * .6],
                                        'glow' if frame >= 4 else 'violet'))
        (cx, cy, cz), r = DISC
        for k in range(12):
            a = math.radians(30 * k)
            seed = (k * 7) % 23
            shift = scatter(seed, 1 if k % 2 else -1, amount * .7)
            pos = [cx + r * math.cos(a) + shift[0], cy + r * math.sin(a) + shift[1], cz + shift[2]]
            mesh.append(box(pos, [.3 * (1 - .5 * amount), .3 * (1 - .5 * amount), .06], 'void' if frame < 4 else 'afterglow'))
        for k, g in enumerate(GAUNTLETS):
            shift = scatter(9 + 5 * k, 1 if k else -1, amount)
            mesh.append(box([g[i] + shift[i] for i in range(3)], [.7 * (1 - .5 * amount), .32, .5 * (1 - .5 * amount)],
                            'shadow' if frame < 4 else 'afterglow'))
    # the charged head / weapon silhouette is broken into jagged seams, never a ball
    for sign in (-1, 1):
        y = 1.40 * FIT + lift
        points = [(sign * .30 * FIT, y + .49 * FIT, -.02),
                  (sign * (.48 + .16 * amount) * FIT, y + .30 * FIT, -.22 - .3 * amount),
                  (sign * (.34 + .28 * amount) * FIT, y - .02 * FIT, -.39 - .6 * amount),
                  (sign * (.62 + .38 * amount) * FIT, y - .36 * FIT, -.65 - .9 * amount)]
        stroke(mesh, points, .033 if frame < 4 else .022, 'violet_dense' if frame < 4 else 'afterglow', core=frame < 4)
    if frame > 0:
        for i in range(7):
            x = (i - 3) * .22 * FIT
            y = (.23 + (i % 4) * .56) * FIT + lift
            z = -.43 - amount * .75
            mesh.append(box((x, y, z), (.028, .025, .45 + amount * (.55 + i % 3 * .17)),
                            'pearl' if i % 3 == 0 and frame < 4 else 'lavender'))
    return mesh


PROFILES = (('shogun', False), ('tenma', True))
FRAMES = 6
DEPART_SOUND = 'playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~1 ~ 0.6 1.45 0.15'
ARRIVE_SOUND = 'playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~1 ~ 0.22 1.75 0.1'


def build(datapack, resourcepack):
    out = Path(datapack) / 'data/rlk/function/boss/raiden/movement'
    if out.exists():
        shutil.rmtree(out)

    def fn(name, lines):
        p = out / (name + '.mcfunction')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    if resourcepack:
        rp = Path(resourcepack)
        for sub in ('models/item', 'items'):
            d = rp / f'assets/rlk/{sub}/raiden/fx_movement'
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True, exist_ok=True)
        for profile, tenma in PROFILES:
            for frame in range(FRAMES):
                name = f'{profile}_{frame}'
                p = rp / f'assets/rlk/models/item/raiden/fx_movement/{name}.json'
                p.write_text(json.dumps({'ambientocclusion': False, 'textures': {**COLORS, 'particle': COLORS['violet']},
                                         'elements': ghost(frame, tenma)}, separators=(',', ':')) + '\n', encoding='utf-8')
                p = rp / f'assets/rlk/items/raiden/fx_movement/{name}.json'
                p.write_text(json.dumps({'model': {'type': 'minecraft:model', 'model': f'rlk:item/raiden/fx_movement/{name}'}},
                                        separators=(',', ':')) + '\n', encoding='utf-8')

    fn('init', [f'scoreboard objectives add {name} dummy' for name in ('rdBlink', 'rdWalk', 'rdWalkDir', 'rdMvAge', 'rdMvKind')])
    fn('cleanup', ['kill @e[tag=rlk_rd_move_fx]',
                   'kill @e[tag=rlk_rd_blink_dest]',
                   'scoreboard players set @e[tag=rlk_raiden] rdBlink 0',
                   'scoreboard players set @e[tag=rlk_raiden] rdWalk 0'])
    fn('blink_start', [
        '# @s boss where it stands. Immune while rdBlink 1.. (combat/apply); she scatters now (the rig hides where it',
        '# stands), relocates at rdBlink 4 and reforms there.',
        'execute if score @s rdBlink matches 1.. run return 0',
        'scoreboard players set @s rdWalk 0',
        'scoreboard players set @s rdBlink 1',
        'function rlk:boss/raiden/rig/state/hidden',
        'execute at @s run function rlk:boss/raiden/movement/depart',
    ])
    fn('blink_to', [
        '# @s boss; the execution position is the destination, pulled in to radius 20 about the arena centre.',
        'kill @e[tag=rlk_rd_blink_dest]',
        'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_blink_dest"]}',
        'execute as @e[tag=rlk_rd_blink_dest] at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] '
        'facing entity @s feet rotated ~ 0 positioned ^ ^ ^20 run tp @s ~ ~ ~',
        '# A blink that has not relocated yet simply takes the new destination.',
        'execute if score @s rdBlink matches 1..3 run return 0',
        'scoreboard players set @s rdBlink 0',
        'execute at @s run function rlk:boss/raiden/movement/blink_start',
    ])
    fn('blink_tick', [
        '# Core tick, as the boss, while rdBlink 1.. . The release timing: relocation + reform art at 4, the rig fades',
        '# back in from 6 (unless a pattern clip already showed it), over at 10 (10 t immune).',
        'execute unless score @s rdBlink matches 1.. run return 0',
        'execute if score @s rdBlink matches 4 run function rlk:boss/raiden/movement/blink_land',
        'execute if score @s rdBlink matches 6 if score @s rdRigS matches 2 unless score @s rdRigT matches -1 run function rlk:boss/raiden/movement/show',
        'scoreboard players add @s rdBlink 1',
        'execute if score @s rdBlink matches 10..19 run scoreboard players set @s rdBlink 0',
        'execute if score @s rdBlink matches 30.. run scoreboard players set @s rdBlink 0',
    ])
    fn('blink_land', [
        '# Hidden (scattered since rdBlink 1): relocate (core blink_relocate), then the silhouette reforms there.',
        'function rlk:boss/raiden/blink_relocate',
        'execute at @s run function rlk:boss/raiden/movement/arrive',
    ])
    fn('show', [
        '# The reform art is two frames from whole: the rig fades in on it (the blink_in clips: visible from their tick 3).',
        'execute if score @s rdPhase matches 2 run return run function rlk:boss/raiden/rig/play/t_blink_in',
        'function rlk:boss/raiden/rig/play/blink_in',
    ])
    for kind, sound in (('depart', DEPART_SOUND), ('arrive', ARRIVE_SOUND)):
        fn(kind, [
            '# Pure art helper: as the boss (or a clone husk) at @s, its yaw; never moves her or changes rdBlink.',
            f'execute if score @s rdPhase matches 2 run function rlk:boss/raiden/movement/art {{kind:{1 if kind == "depart" else 2},'
            f'model:"tenma_{0 if kind == "depart" else FRAMES - 1}"}}',
            f'execute unless score @s rdPhase matches 2 run function rlk:boss/raiden/movement/art {{kind:{1 if kind == "depart" else 2},'
            f'model:"shogun_{0 if kind == "depart" else FRAMES - 1}"}}',
            sound])
    fn('art', [
        '# The silhouette display (scale 8; right_rotation cancels the item renderer\'s turn, so +Z is her facing).',
        '$summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_move_fx","rlk_rd_mvnew"],'
        'billboard:"fixed",item_display:"none",teleport_duration:0,brightness:{block:15,sky:15},shadow_radius:0f,view_range:3f,'
        'width:10f,height:8f,transformation:{translation:[0f,0f,0f],scale:[8f,8f,8f],left_rotation:[0f,0f,0f,1f],'
        'right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":'
        '"rlk:raiden/fx_movement/$(model)"}}}',
        'execute rotated as @s run tp @e[tag=rlk_rd_mvnew] ~ ~ ~ ~ 0',
        'scoreboard players set @e[tag=rlk_rd_mvnew] rdMvAge -1',
        '$scoreboard players set @e[tag=rlk_rd_mvnew] rdMvKind $(kind)',
        'execute if score @s rdPhase matches 2 run tag @e[tag=rlk_rd_mvnew] add rlk_rd_mv_t',
        'tag @e[tag=rlk_rd_mvnew] remove rlk_rd_mvnew',
    ])
    fn('world', ['execute as @e[tag=rlk_rd_move_fx] run function rlk:boss/raiden/movement/fx_tick'])
    lines = ['# One frame per tick: the scatter plays 0 -> 5, the reform 5 -> 0; gone after the sixth.',
             'scoreboard players add @s rdMvAge 1',
             f'execute if score @s rdMvAge matches {FRAMES}.. run return run kill @s']
    for profile, tag in (('shogun', 'tag=!rlk_rd_mv_t'), ('tenma', 'tag=rlk_rd_mv_t')):
        for age in range(1, FRAMES):
            for kind in (1, 2):
                frame = age if kind == 1 else FRAMES - 1 - age
                lines.append(f'execute if entity @s[{tag}] if score @s rdMvKind matches {kind} if score @s rdMvAge matches {age} '
                             f'run return run data modify entity @s item.components."minecraft:item_model" set value '
                             f'"rlk:raiden/fx_movement/{profile}_{frame}"')
    fn('fx_tick', lines)
    print(f'Built the blink: {2 * FRAMES} scatter / reform silhouette models, the release timing (10 t, relocation at 4).')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datapack', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--resourcepack', type=Path, help='unpacked resource pack (the silhouette models)')
    args = parser.parse_args()
    build(args.datapack, args.resourcepack)
