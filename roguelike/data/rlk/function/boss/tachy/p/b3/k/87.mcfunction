# B3 pattern tick 87
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzEl mb 1
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:38,a:45,tell:1,dmg:42}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/tachy/core/hz_tag/b3
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzEl mb 1
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:17,tell:1,dmg:42}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/tachy/core/hz_tag/b3
