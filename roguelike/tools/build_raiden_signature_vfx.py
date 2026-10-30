"""Signature display effect of Narukami that the rework still uses: the armour-break burst (exhausted_start).

The release's other signature effects (the 만겁 calamity cut and protected dome, the judgment warning ring and charge,
the transformation charge, the blink rifts, the ascend pillar and sky bolts) were replaced by the kit cues and the rig
props in the rework (rd/plan.md §B.2 15, §C.6) and are removed here (S3): this generator now owns and rebuilds
models/items `raiden/fx_signature/` and `boss/raiden/vfx/` from scratch, so their former outputs disappear.

Runtime: vfx/armor_break (as the boss) summons one painted-card display tagged rlk_rd_sfx; vfx/world ticks it, it
grows and settles for 15 ticks, then dies. vfx/init also creates the kit objectives (hazard/setup).
"""
from pathlib import Path
import argparse
import shutil

from raiden_obj_cards import Model, save, ensure_textures, fx_names, polar

DP = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--resourcepack', required=True)
RP = Path(parser.parse_args().resourcepack)
OUT = DP / 'data/rlk/function/boss/raiden/vfx'
SCALE = 16
FX = fx_names()
ensure_textures(RP, FX)

for kind in ('models/item', 'items'):
    shutil.rmtree(RP / 'assets/rlk' / kind / 'raiden/fx_signature', ignore_errors=True)
shutil.rmtree(OUT, ignore_errors=True)


def write(name, lines):
    p = OUT / (name + '.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


# Armour shards: 18 glints and shard cards spiralling round the body (painted fxg sprites).
m = Model(SCALE, FX)
for i in range(18):
    a = (i * 22.5) % 360
    r = 1.0 + (i % 3) * .3
    y = .6 + (i % 5) * .55
    m.crossed(polar(r, a, y), .55 if i % 2 else .8, 'glint', planes=2)
    m.vcard(polar(r * 1.08, a, y + .25), a, .45, .9, 'obj_shard')
save(RP, 'fx_signature', 'armor_break', m)

write('init', [f'scoreboard objectives add {n} dummy' for n in ['rdSfxAge', 'rdSfxLife', 'rdSfxKind']] +
      ['# Hazard / FX kit v2 objectives (build_raiden_hazards.py).', 'function rlk:boss/raiden/hazard/setup'])
write('armor_break', [
    'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_sfx","rlk_rd_sfx_new"],'
    'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_signature/armor_break"}},'
    'item_display:"none",brightness:{sky:15,block:15},view_range:4f,shadow_radius:0f,'
    'width:0f,height:0f,interpolation_duration:1,start_interpolation:0,'
    'transformation:{translation:[0f,0f,0f],scale:[16f,16f,16f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]}}',
    'scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxAge -1',
    'scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxLife 15',
    'scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxKind 7',
    'tag @e[tag=rlk_rd_sfx_new] remove rlk_rd_sfx_new',
])
write('world', ['execute as @e[tag=rlk_rd_sfx] at @s run function rlk:boss/raiden/vfx/tick'])


def grow(age, scale, translation, duration):
    v = lambda xs: '[' + ','.join(f'{x:g}f' for x in xs) + ']'
    return (f'execute if score @s rdSfxAge matches {age} run data merge entity @s {{interpolation_duration:{duration},'
            f'start_interpolation:0,transformation:{{scale:{v(scale)},translation:{v(translation)}}}}}')


write('tick', [
    'scoreboard players add @s rdSfxAge 1',
    'execute if score @s rdSfxAge >= @s rdSfxLife run return run kill @s',
    grow(1, (22, 19, 22), (0, .15, 0), 2),
    grow(5, (27, 20, 27), (0, -.4, 0), 4),
    grow(10, (30, 3, 30), (0, 0, 0), 4),      # settles flat on the floor (the release sank it 3 b below, R3)
])
print('Generated the signature armour-break burst (the other release signature effects are retired).')
