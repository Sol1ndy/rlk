# Blast of a kind-6 spear (water): X of crossed light beams, field, debris.
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13x","rlk_mb_gd_p13xnew"],block_state:{id:"minecraft:light_blue_stained_glass"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-1.462f,0.099f,-0.21f],left_rotation:[0f,0f,-0.242f,0.97f],scale:[0.42f,10f,0.42f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13x","rlk_mb_gd_p13xnew"],block_state:{id:"minecraft:light_blue_stained_glass"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[1.091f,-0.099f,-0.21f],left_rotation:[0f,0f,0.242f,0.97f],scale:[0.42f,10f,0.42f],right_rotation:[0f,0f,0f,1f]}}
tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] ~ ~ ~ ~ 0
tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] remove rlk_mb_gd_p13xnew
particle minecraft:explosion ~ ~0.8 ~ 1 0.4 1 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:brown_terracotta"} ~ ~0.5 ~ 1.6 0.4 1.6 0.3 20 force @a[tag=player]
execute rotated ~45.229 0 positioned ^ ^0.9 ^3.885 run particle minecraft:dust{color:[0.82f,0.93f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~74.132 0 positioned ^ ^0.9 ^2.14 run particle minecraft:dust{color:[0.82f,0.93f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~284.227 0 positioned ^ ^0.9 ^0.991 run particle minecraft:dust{color:[0.82f,0.93f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~326.161 0 positioned ^ ^0.9 ^2.082 run particle minecraft:dust{color:[0.82f,0.93f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~326.162 0 positioned ^ ^0.9 ^3.121 run particle minecraft:dust{color:[0.82f,0.93f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~140.535 0 positioned ^ ^0.9 ^3.995 run particle minecraft:dust{color:[0.82f,0.93f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~59.383 0 positioned ^ ^0.9 ^1.462 run particle minecraft:dust{color:[0.82f,0.93f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~65.523 0 positioned ^ ^0.9 ^1.004 run particle minecraft:dust{color:[0.82f,0.93f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~89.218 0 positioned ^ ^0.9 ^1.931 run particle minecraft:dust{color:[0.82f,0.93f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
execute rotated ~86.585 0 positioned ^ ^0.9 ^2.598 run particle minecraft:dust{color:[0.82f,0.93f,1f],scale:1.5} ~ ~ ~ 0.05 0.8 0.05 0 6 force @a[tag=player]
particle minecraft:splash ~ ~0.4 ~ 2.4 0.4 2.4 0 60 force @a[tag=player]
particle minecraft:falling_water ~ ~1.5 ~ 2.4 1.2 2.4 0 20 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:blue_ice"} ~ ~0.6 ~ 2 0.6 2 0.25 30 force @a[tag=player]
particle minecraft:dust{color:[0.24f,0.43f,0.8f],scale:1.8} ~ ~1 ~ 2 0.8 2 0 30 force @a[tag=player]
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.9 0.8 0.3
playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
playsound minecraft:entity.player.splash.high_speed hostile @a[tag=player] ~ ~ ~ 0.9 1 0.3
playsound minecraft:block.powder_snow.break hostile @a[tag=player] ~ ~ ~ 1 1 0.33
