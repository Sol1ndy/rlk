# Blast of a kind-4 spear (ice): X of crossed light beams, field, debris.
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13x","rlk_mb_gd_p13xnew"],block_state:{id:"minecraft:white_stained_glass"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-1.717f,0.099f,-0.21f],left_rotation:[0f,0f,-0.242f,0.97f],scale:[0.42f,10f,0.42f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13x","rlk_mb_gd_p13xnew"],block_state:{id:"minecraft:white_stained_glass"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[1.346f,-0.099f,-0.21f],left_rotation:[0f,0f,0.242f,0.97f],scale:[0.42f,10f,0.42f],right_rotation:[0f,0f,0f,1f]}}
tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] ~ ~ ~ ~ 0
tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] remove rlk_mb_gd_p13xnew
particle minecraft:explosion ~ ~0.8 ~ 1 0.4 1 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:brown_terracotta"} ~ ~0.5 ~ 1.92 0.4 1.92 0.3 20 force @a[tag=player]
execute rotated ~86.123 0 positioned ^ ^0.9 ^1.501 run particle minecraft:dust{color:[0.94f,1f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~310.836 0 positioned ^ ^0.9 ^1.083 run particle minecraft:dust{color:[0.94f,1f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~309.953 0 positioned ^ ^0.9 ^2.318 run particle minecraft:dust{color:[0.94f,1f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~229.637 0 positioned ^ ^0.9 ^2.434 run particle minecraft:dust{color:[0.94f,1f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~137.503 0 positioned ^ ^0.9 ^3.242 run particle minecraft:dust{color:[0.94f,1f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~71.183 0 positioned ^ ^0.9 ^3.236 run particle minecraft:dust{color:[0.94f,1f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~345.284 0 positioned ^ ^0.9 ^1.53 run particle minecraft:dust{color:[0.94f,1f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~344.496 0 positioned ^ ^0.9 ^1.49 run particle minecraft:dust{color:[0.94f,1f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~120.478 0 positioned ^ ^0.9 ^2.145 run particle minecraft:dust{color:[0.94f,1f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~153.71 0 positioned ^ ^0.9 ^2.473 run particle minecraft:dust{color:[0.94f,1f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
particle minecraft:splash ~ ~0.4 ~ 2.88 0.4 2.88 0 60 force @a[tag=player]
particle minecraft:falling_water ~ ~1.5 ~ 2.88 1.2 2.88 0 20 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:packed_ice"} ~ ~0.6 ~ 2.4 0.6 2.4 0.25 30 force @a[tag=player]
particle minecraft:dust{color:[0.64f,1f,0.99f],scale:1.8} ~ ~1 ~ 2.4 0.8 2.4 0 30 force @a[tag=player]
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.9 0.8 0.3
playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
playsound minecraft:entity.player.splash.high_speed hostile @a[tag=player] ~ ~ ~ 0.9 1 0.3
playsound minecraft:block.powder_snow.break hostile @a[tag=player] ~ ~ ~ 1 1 0.33
particle minecraft:snowflake ~ ~1 ~ 2.88 1 2.88 0.04 30 force @a[tag=player]
