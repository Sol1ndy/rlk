# @s = body (t41): crack strips 3-4 (keep rows: the outline-only tele/crack_o, same tick / size / tell as each strip)
# from the root toward the lock: len 8.4 w 3.0, height 0-2.5, tells
# (34, 41), 100 % each, one volley group (<= 1 hit of the two).
function rlk:mboss/grp_new
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2s2,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s2,limit=1] run function rlk:boss/apep/fx/tele/crack_o {len:84,w:30,back:0,tell:34,nd:0,hold:3}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 25
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2s2,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s2,limit=1] run function rlk:mboss/hz/line {len:84,w:30,tell:34,dmg:100}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p2
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2s3,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s3,limit=1] run function rlk:boss/apep/fx/tele/crack_o {len:84,w:30,back:0,tell:41,nd:0,hold:3}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 25
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2s3,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s3,limit=1] run function rlk:mboss/hz/line {len:84,w:30,tell:41,dmg:100}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p2
