# G1 pattern tick 33
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzBack mb 140
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~0 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:140,w:30,tell:1,dmg:45}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/arlecchino/core/hz_tag/g1
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzBack mb 140
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~90 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:140,w:30,tell:1,dmg:45}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/arlecchino/core/hz_tag/g1
