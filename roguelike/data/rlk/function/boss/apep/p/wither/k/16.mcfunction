# wither #apPT 16
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p4d]
execute at @s positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p4","rlk_mb_ap_p4d"]}
execute at @s positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p4d,limit=1] ~ ~ ~ ~ 0
execute at @s positioned ~ 201 ~ run function rlk:boss/apep/fx/tele/disc {r:90,tell:24,el:23,nd:0,hold:24}
scoreboard players set #hzAct mb 24
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzKBDir mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @s positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:90,tell:24,dmg:85}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p4
execute at @s run function rlk:boss/apep/fx/snd/p4_hum
