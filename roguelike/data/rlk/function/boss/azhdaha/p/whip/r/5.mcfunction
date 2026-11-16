# whip r #azPT 5
scoreboard players set #hzKB mb 4
scoreboard players set #hzKBDir mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzGrp mb = #aq7G mb
scoreboard players set #hzEl mb 5
scoreboard players set #pjEl mb 5
execute positioned ^-3.765 ^0 ^-2.872 rotated ~173.03 0 run function rlk:mboss/hz/sector {r:120,a:24,tell:20,dmg:129}
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
execute positioned ^-3.765 ^0 ^-2.872 run function rlk:mboss/hz/disc {r:20,tell:20,dmg:129}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p7
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p7h
