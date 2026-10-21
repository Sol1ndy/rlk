# @s = body (t98): hit 4, the leaping slam: the lunge goal 2.5 b ahead (inside r 16); the disc
# r 6.6 7.2 b ahead of it (the rig's slam anchor after the lunge), tell 22 (none row: the
# tallest rear from t93), 140 %.
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p6d]
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^2.5 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p6","rlk_mb_ap_p6d"]}
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^2.5 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p6d,limit=1] ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p6d,limit=1] run function rlk:boss/apep/u/clamp_glide
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p6e]
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p6d,limit=1] rotated as @s rotated ~ 0 positioned ^ ^ ^7.2 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p6","rlk_mb_ap_p6e"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p6d,limit=1] rotated as @s rotated ~ 0 positioned ^ ^ ^7.2 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p6e,limit=1] ~ ~ ~ ~ 0
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p6e,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p6e,limit=1] run function rlk:mboss/hz/disc {r:66,tell:22,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p6
