# Spear 2 (T0+56): the hazard (disc r 2.8, 220 %, the star's element), the red
# concave 4-point star decal on the player (front arm toward the arena centre) and the giant red spear
# growing out of the column, point down, its tip 3.8 b above the target.
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzLinger mb 2
execute if score #gp13K1 mb matches 1 run scoreboard players set #hzEl mb 1
execute if score #gp13K1 mb matches 1 run scoreboard players set #hzCol mb 1
execute if score #gp13K1 mb matches 2 run scoreboard players set #hzEl mb 2
execute if score #gp13K1 mb matches 2 run scoreboard players set #hzCol mb 2
execute if score #gp13K1 mb matches 3 run scoreboard players set #hzEl mb 3
execute if score #gp13K1 mb matches 3 run scoreboard players set #hzCol mb 3
execute if score #gp13K1 mb matches 4 run scoreboard players set #hzEl mb 4
execute if score #gp13K1 mb matches 4 run scoreboard players set #hzCol mb 4
execute if score #gp13K1 mb matches 5 run scoreboard players set #hzCol mb 5
execute if score #gp13K1 mb matches 6 run scoreboard players set #hzCol mb 2
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:mboss/hz/disc {r:28,tell:24,dmg:220}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_gd_p13
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13d1","rlk_mb_gd_p13d1fr","rlk_mb_gd_p13dnew"],block_state:{Name:"minecraft:pink_stained_glass"},brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-1.55f,0.002f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.192f,0.02f,6.859f],right_rotation:[0f,0.383f,0f,0.924f]}}
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13d1","rlk_mb_gd_p13d1ff","rlk_mb_gd_p13dnew"],block_state:{Name:"minecraft:red_stained_glass"},brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[-1.3f,0.026f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.838f,0.02f,6.364f],right_rotation:[0f,0.383f,0f,0.924f]}}
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13d1","rlk_mb_gd_p13d1sr","rlk_mb_gd_p13dnew"],block_state:{Name:"minecraft:pink_stained_glass"},brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,0.002f,1.55f],left_rotation:[0f,0.707f,0f,0.707f],scale:[2.192f,0.02f,4.313f],right_rotation:[0f,0.383f,0f,0.924f]}}
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13d1","rlk_mb_gd_p13d1sf","rlk_mb_gd_p13dnew"],block_state:{Name:"minecraft:red_stained_glass"},brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,0.026f,1.3f],left_rotation:[0f,0.707f,0f,0.707f],scale:[1.838f,0.02f,3.818f],right_rotation:[0f,0.383f,0f,0.924f]}}
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p13dnew] ~ ~ ~ ~ 0
tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13dnew] remove rlk_mb_gd_p13dnew
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] positioned ~ ~11.9 ~ run function rlk:mboss/guardian/rig/prop/spear
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] run data merge entity @s {transformation:{translation:[0f,0f,0f],left_rotation:[1f,0f,0f,0f],scale:[0.6f,0.6f,0.6f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/guardian/prop_spear_red"}}}
tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p13s1
tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p13
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run particle minecraft:dust{color:[0.8f,0.16f,0.28f],scale:1.6} ~ ~0.15 ~ 1 0.02 1 0 16 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run particle minecraft:block{block_state:"minecraft:red_concrete"} ~ ~9 ~ 0.3 1.5 0.3 0 12 force @a[tag=player]
