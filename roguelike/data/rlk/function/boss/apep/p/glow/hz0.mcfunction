# @s = body (t111): slam 1 at t141 (none row: the coil / re-rear / leap is the tell; tell 30): the disc r
# 5.4 at the slam point, height 0-4, 110 %; the thorn-wheel carpet: a ring front
# 3.0 -> 14.4 b in 14 t (0.814 b/t), band 1.0 b,
# jumpable (#hzY1 7), 30 %, in a new volley group with homing wheel 1 (#apq3G).
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 40
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p3c,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p3c,limit=1] run function rlk:mboss/hz/disc {r:54,tell:30,dmg:110}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p3
function rlk:mboss/grp_new
scoreboard players operation #apq3G mb = #mbGrp mb
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 15
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 7
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p3c,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p3c,limit=1] run function rlk:mboss/hz/ring {r0:20,r:30,tell:30,dmg:30}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p3
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p3c0
