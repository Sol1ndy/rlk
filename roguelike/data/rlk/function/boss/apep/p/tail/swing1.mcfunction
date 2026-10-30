# @s = body (t14): swing 1's 8 swept wedges (plan 7.11 rule 3; api.wedges of the manifest's tail track x
# the yaw schedule, in the start frame rlk_mb_ap_p5f): hz/sector r 11.4 about each tick's tail root, the
# angle swept that tick, ticks 28-35, one volley group, KB 4, height 0-3, 130 %. None row (no
# lane decal): the S-raise / cock cue / tip flash / recoil are the tell.
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^0.977 ^0 ^-2.733 rotated ~-52.42 0 run function rlk:mboss/hz/sector {r:114,a:9,tell:14,dmg:130}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^2.08 ^0 ^-2.033 rotated ~-35.52 0 run function rlk:mboss/hz/sector {r:114,a:9,tell:15,dmg:130}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^2.8 ^0 ^-0.792 rotated ~-25.92 0 run function rlk:mboss/hz/sector {r:114,a:2,tell:16,dmg:130}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^2.843 ^0 ^0.633 rotated ~-22.7 0 run function rlk:mboss/hz/sector {r:114,a:12,tell:17,dmg:130}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^2.309 ^0 ^1.776 rotated ~-5.64 0 run function rlk:mboss/hz/sector {r:114,a:20,tell:18,dmg:130}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^1.342 ^0 ^2.585 rotated ~19.36 0 run function rlk:mboss/hz/sector {r:114,a:20,tell:19,dmg:130}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^0.124 ^0 ^2.91 rotated ~44.36 0 run function rlk:mboss/hz/sector {r:114,a:20,tell:20,dmg:130}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 30
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] positioned ^-1.117 ^0 ^2.69 rotated ~69.36 0 run function rlk:mboss/hz/sector {r:114,a:20,tell:21,dmg:130}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p5
