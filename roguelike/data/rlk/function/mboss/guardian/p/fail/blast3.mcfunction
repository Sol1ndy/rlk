# Blast of a kind-3 spear (spark): X of crossed light beams, field, debris, the impact ring again.
function rlk:mboss/guardian/p/fail/ring3
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13x","rlk_mb_gd_p13xnew"],block_state:{id:"minecraft:magenta_stained_glass"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-1.717f,0.099f,-0.21f],left_rotation:[0f,0f,-0.242f,0.97f],scale:[0.42f,10f,0.42f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13x","rlk_mb_gd_p13xnew"],block_state:{id:"minecraft:magenta_stained_glass"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[1.346f,-0.099f,-0.21f],left_rotation:[0f,0f,0.242f,0.97f],scale:[0.42f,10f,0.42f],right_rotation:[0f,0f,0f,1f]}}
tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] ~ ~ ~ ~ 0
tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] remove rlk_mb_gd_p13xnew
particle minecraft:explosion ~ ~0.8 ~ 1 0.4 1 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:brown_terracotta"} ~ ~0.5 ~ 1.92 0.4 1.92 0.3 20 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.138 ^3.902 ^2.934 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.277 ^3.547 ^2.846 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.388 ^3.193 ^3.042 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.499 ^2.838 ^3.239 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.317 ^2.483 ^3.382 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.135 ^2.128 ^3.524 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.204 ^1.774 ^3.514 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.274 ^1.419 ^3.503 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.138 ^1.064 ^3.486 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.002 ^0.709 ^3.47 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.001 ^0.355 ^3.313 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~23.706 0 positioned ^-0.001 ^0 ^3.157 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^0.171 ^3.527 ^3.437 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^0.343 ^3.206 ^3.462 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^0.492 ^2.886 ^3.431 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^0.641 ^2.565 ^3.399 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^0.862 ^2.244 ^3.61 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^1.083 ^1.924 ^3.821 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^0.89 ^1.603 ^3.797 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^0.696 ^1.283 ^3.773 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^0.786 ^0.962 ^3.753 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^0.876 ^0.641 ^3.734 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^0.569 ^0.321 ^3.621 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~127.343 0 positioned ^0.263 ^0 ^3.509 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.217 ^3.935 ^3.091 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.435 ^3.577 ^3.038 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.414 ^3.219 ^3.018 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.393 ^2.862 ^2.997 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.514 ^2.504 ^3.2 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.635 ^2.146 ^3.402 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.599 ^1.789 ^3.531 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.563 ^1.431 ^3.659 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.576 ^1.073 ^3.634 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.589 ^0.715 ^3.609 run particle minecraft:dust{color:[0.99f,0.89f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.383 ^0.358 ^3.446 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute rotated ~224.884 0 positioned ^-0.177 ^0 ^3.284 run particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.1} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
particle minecraft:electric_spark ~ ~0.8 ~ 2.88 0.8 2.88 0.4 40 force @a[tag=player]
particle minecraft:end_rod ~ ~1 ~ 1.92 0.8 1.92 0.1 12 force @a[tag=player]
particle minecraft:dust{color:[0.89f,0.52f,0.99f],scale:1.8} ~ ~1 ~ 2.88 1 2.88 0 30 force @a[tag=player]
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.9 0.8 0.3
playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.3 1.6 0.1
playsound minecraft:block.copper_bulb.turn_on hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
