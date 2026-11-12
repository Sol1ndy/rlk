# @s = slab 4, its burst just struck: it tears out and rises 4.5 b over 12 t with a slow tumble.
data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{translation:[0f,0f,0f],left_rotation:[0.0514f,0.6739f,-0.0471f,0.7355f],right_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f]}}
tag @s add rlk_mb_fg_p12r
execute positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/slab_rise
function rlk:mboss/fieldgen/fx/snd/slab_lift
tp @s ~ ~4.5 ~
