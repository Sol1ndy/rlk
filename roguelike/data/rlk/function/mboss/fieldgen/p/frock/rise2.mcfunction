# @s = slab 3, its burst just struck: it tears out and rises 6 b over 12 t with a slow tumble.
data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{translation:[0f,0f,0f],left_rotation:[-0.0604f,0.4988f,0.0349f,0.8639f],right_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f]}}
tag @s add rlk_mb_fg_p12r
execute positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/slab_rise
function rlk:mboss/fieldgen/fx/snd/slab_lift
tp @s ~ ~6 ~
