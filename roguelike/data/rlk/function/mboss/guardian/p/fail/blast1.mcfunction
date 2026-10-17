# Blast of a kind-1 spear (fire): X of crossed light beams, field, debris.
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13x","rlk_mb_gd_p13xnew"],block_state:{id:"minecraft:orange_stained_glass"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-1.462f,0.099f,-0.21f],left_rotation:[0f,0f,-0.242f,0.97f],scale:[0.42f,10f,0.42f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13x","rlk_mb_gd_p13xnew"],block_state:{id:"minecraft:orange_stained_glass"},brightness:{sky:15,block:15},view_range:1.6f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[1.091f,-0.099f,-0.21f],left_rotation:[0f,0f,0.242f,0.97f],scale:[0.42f,10f,0.42f],right_rotation:[0f,0f,0f,1f]}}
tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] ~ ~ ~ ~ 0
tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] remove rlk_mb_gd_p13xnew
particle minecraft:explosion ~ ~0.8 ~ 1 0.4 1 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:brown_terracotta"} ~ ~0.5 ~ 1.6 0.4 1.6 0.3 20 force @a[tag=player]
particle minecraft:flame ~ ~0.8 ~ 2.4 1 2.4 0.05 40 force @a[tag=player]
particle minecraft:lava ~ ~0.4 ~ 2 0.3 2 0 10 force @a[tag=player]
particle minecraft:large_smoke ~ ~1 ~ 1.6 0.8 1.6 0.02 10 force @a[tag=player]
particle minecraft:dust{color:[1f,0.54f,0.3f],scale:1.8} ~ ~1 ~ 2.4 1 2.4 0 30 force @a[tag=player]
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 1 0.8 0.3
playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.3
