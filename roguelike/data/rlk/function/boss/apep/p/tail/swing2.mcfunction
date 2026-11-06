# @s = body (t39): swing 2's 8 swept wedges (plan 7.11 rule 3; api.wedges of the manifest's tail track x
# the yaw schedule, in the start frame rlk_mb_ap_p5f): hz/sector r 11.4 about each tick's tail root, the
# angle swept that tick, ticks 52-59, one volley group, KB 4, height 0-3, 140 %. None row (no
# lane decal): the S-raise / cock cue / tip flash / recoil are the tell.
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^-0.017 ^0 ^2.903 rotated ~-98.79 0 run function rlk:mboss/hz/sector {r:114,a:5,tell:13,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^1.259 ^0 ^2.621 rotated ~-109.02 0 run function rlk:mboss/hz/sector {r:114,a:6,tell:14,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^2.361 ^0 ^1.702 rotated ~-111.13 0 run function rlk:mboss/hz/sector {r:114,a:4,tell:15,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^2.888 ^0 ^0.377 rotated ~-111.28 0 run function rlk:mboss/hz/sector {r:114,a:16,tell:16,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^2.777 ^0 ^-0.879 rotated ~-129.65 0 run function rlk:mboss/hz/sector {r:114,a:23,tell:17,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^2.146 ^0 ^-1.97 rotated ~-154.65 0 run function rlk:mboss/hz/sector {r:114,a:23,tell:18,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^1.112 ^0 ^-2.692 rotated ~-179.65 0 run function rlk:mboss/hz/sector {r:114,a:23,tell:19,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^-0.13 ^0 ^-2.91 rotated ~155.35 0 run function rlk:mboss/hz/sector {r:114,a:23,tell:20,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
