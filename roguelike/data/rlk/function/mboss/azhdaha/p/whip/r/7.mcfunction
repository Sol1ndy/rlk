# whip r #azPT 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzKBDir mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzGrp mb = #aq7G mb
scoreboard players set #hzEl mb 5
scoreboard players set #pjEl mb 5
execute positioned ^-4.704 ^0 ^-0.543 rotated ~137.94 0 run function rlk:mboss/hz/sector {r:120,a:26,tell:20,dmg:150}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p7
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p7h
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzGrp mb = #aq7G mb
scoreboard players set #hzEl mb 5
scoreboard players set #pjEl mb 5
execute positioned ^-4.704 ^0 ^-0.543 run function rlk:mboss/hz/disc {r:20,tell:20,dmg:150}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p7
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p7h
