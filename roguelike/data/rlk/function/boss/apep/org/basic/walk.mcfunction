# Walking to the Heart at 0.12 b/t (bell, bobbing): melee to the wait ring r 4.5 (then a socket), ranged to r 12.6 (lies down).
execute if entity @s[tag=!rlk_mb_ap_rng] positioned 440 201 8 if entity @s[distance=..4.7] at @s run return run function rlk:boss/apep/org/basic/arrive
execute if entity @s[tag=rlk_mb_ap_rng] positioned 440 201 8 if entity @s[distance=..12.6] at @s run return run function rlk:boss/apep/org/basic/lie_go
execute facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet run function rlk:mboss/mv/step_flat {spd:0.12}
function rlk:boss/apep/om/face
