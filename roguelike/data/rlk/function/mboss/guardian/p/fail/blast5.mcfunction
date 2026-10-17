# Blast of a kind-5 spear (gold): X of crossed light beams, field, debris.
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13x","rlk_mb_gd_p13xnew"],block_state:{id:"minecraft:yellow_stained_glass"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-1.717f,0.099f,-0.21f],left_rotation:[0f,0f,-0.242f,0.97f],scale:[0.42f,10f,0.42f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13x","rlk_mb_gd_p13xnew"],block_state:{id:"minecraft:yellow_stained_glass"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[1.346f,-0.099f,-0.21f],left_rotation:[0f,0f,0.242f,0.97f],scale:[0.42f,10f,0.42f],right_rotation:[0f,0f,0f,1f]}}
tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] ~ ~ ~ ~ 0
tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] remove rlk_mb_gd_p13xnew
particle minecraft:explosion ~ ~0.8 ~ 1 0.4 1 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:brown_terracotta"} ~ ~0.5 ~ 1.92 0.4 1.92 0.3 20 force @a[tag=player]
execute rotated ~230.813 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^7.071",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:1.3048,s1:2.6096,move:"0f,0f,0f",life:16,fade:6}
execute rotated ~6.465 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^5.067",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:1.1337,s1:2.2674,move:"0f,0f,0f",life:19,fade:6}
execute rotated ~327.873 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^4.898",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:1.4907,s1:2.9814,move:"0f,0f,0f",life:21,fade:6}
execute rotated ~319.204 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^6.533",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:1.3418,s1:2.6835,move:"0f,0f,0f",life:19,fade:6}
execute rotated ~85.765 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^3.941",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:1.1472,s1:2.2945,move:"0f,0f,0f",life:18,fade:6}
execute rotated ~147.623 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^5.718",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:0.7808,s1:1.5616,move:"0f,0f,0f",life:19,fade:6}
execute rotated ~50.296 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^2.32",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:1.3055,s1:2.6109,move:"0f,0f,0f",life:20,fade:6}
execute rotated ~171.732 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^3.111",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:1.358,s1:2.7159,move:"0f,0f,0f",life:21,fade:6}
execute rotated ~291.323 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^2.044",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:0.9048,s1:1.8097,move:"0f,0f,0f",life:18,fade:6}
execute rotated ~338.371 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^4.049",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:1.3788,s1:2.7576,move:"0f,0f,0f",life:20,fade:6}
execute rotated ~10.002 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^4.705",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:0.8353,s1:1.6706,move:"0f,0f,0f",life:16,fade:6}
execute rotated ~77.753 0 run function rlk:fx/nv/card {kind:"shard",pos:"^ ^0.02 ^5.962",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:1.0584,s1:2.1168,move:"0f,0f,0f",life:16,fade:6}
particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.4 ~ 3.6 0.3 3.6 0.2 40 force @a[tag=player]
particle minecraft:dust{color:[1f,0.99f,0.68f],scale:1.6} ~ ~1.5 ~ 3.6 1.2 3.6 0 30 force @a[tag=player]
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
playsound minecraft:block.pointed_dripstone.land hostile @a[tag=player] ~ ~ ~ 1 1 0.33
playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.3 1.6 0.1
playsound minecraft:block.basalt.break hostile @a[tag=player] ~ ~ ~ 0.9 0.8 0.3
