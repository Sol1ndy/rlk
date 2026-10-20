# @s = body (t64): the four burst hazards r 2.5 (one group, 90 %), quiet: no decal
# (Change note 1: the planted spikes' veins glow from here, boss outward).
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p4a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p4a,limit=1] run function rlk:mboss/hz/disc {r:25,tell:12,dmg:90}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p4x
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p4b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p4b,limit=1] run function rlk:mboss/hz/disc {r:25,tell:15,dmg:90}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p4x
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p4c,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p4c,limit=1] run function rlk:mboss/hz/disc {r:25,tell:18,dmg:90}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p4x
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p4d,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p4d,limit=1] run function rlk:mboss/hz/disc {r:25,tell:21,dmg:90}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p4x
