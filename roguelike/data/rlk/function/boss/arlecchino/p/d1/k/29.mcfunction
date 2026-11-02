# D1 pattern tick 29
scoreboard players operation #hzSzR mb = #d1_dl kn
scoreboard players set #t3 kn 20
scoreboard players operation #hzSzR mb *= #t3 kn
scoreboard players set #t3 kn 4
scoreboard players operation #hzSzR mb /= #t3 kn
execute as @e[type=minecraft:marker,tag=rlk_kn_dl,tag=rlk_kn_p_d1] run function rlk:boss/arlecchino/core/dash/grow
execute at @s run particle minecraft:flame ~ ~ ~ 0.3 0.5 0.3 0.04 10 force @a[tag=player]
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:42,a:70,tell:1,dmg:45}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/arlecchino/core/hz_tag/d1
