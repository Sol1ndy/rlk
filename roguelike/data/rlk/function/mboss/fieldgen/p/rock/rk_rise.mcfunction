# [c_rocks] @s = a slab, at it, 2 t after its burst: it tears out and rises (12 t), tumbling a little.
execute positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/slab_rise
function rlk:mboss/fieldgen/fx/snd/slab_lift
data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{translation:[0f,0f,0f],left_rotation:[0.08f,0.2f,0f,0.976f],right_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f]}}
execute if score @s mbS matches 1 run tp @s ~ ~4 ~
execute if score @s mbS matches 2 run tp @s ~ ~5 ~
execute if score @s mbS matches 3 run tp @s ~ ~6 ~
execute if score @s mbS matches 4 run tp @s ~ ~4.5 ~
execute if score @s mbS matches 5 run tp @s ~ ~5.5 ~
execute if score @s mbS matches 6 run tp @s ~ ~4 ~
execute if score @s mbS matches 7 run tp @s ~ ~5 ~
execute if score @s mbS matches 8 run tp @s ~ ~6 ~
