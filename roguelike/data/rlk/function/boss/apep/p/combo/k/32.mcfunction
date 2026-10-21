# combo #apPT 32
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p6b]
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^4.8 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p6","rlk_mb_ap_p6b"]}
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^4.8 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p6b,limit=1] ~ ~ ~ ~ 0
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p6b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p6b,limit=1] run function rlk:mboss/hz/disc {r:66,tell:14,dmg:120}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p6
