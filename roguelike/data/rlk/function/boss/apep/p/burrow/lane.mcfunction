# @s = body (t52): the yaw is locked; the sweep lane from the anchor along the facing, len 10.8 w
# 3.6, height 0-3, tell 12 (none row: the loom + the lock are the tell), 140 %; the glide goal
# 7.0 b along it (inside r 16).
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p1l]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p1","rlk_mb_ap_p1l"]}
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p1l,limit=1] ~ ~ ~ ~ 0
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p1l,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p1l,limit=1] run function rlk:mboss/hz/line {len:108,w:36,tell:12,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p1
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p1e]
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p1l,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p1l,limit=1] positioned ^ ^ ^7 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p1","rlk_mb_ap_p1e"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p1l,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p1l,limit=1] positioned ^ ^ ^7 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p1e,limit=1] ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p1e,limit=1] run function rlk:boss/apep/u/clamp_glide
