# A1 pattern tick 19
scoreboard players operation #hzSzR mb = #a1_dl tk
scoreboard players set #t3 tk 30
scoreboard players operation #hzSzR mb *= #t3 tk
scoreboard players set #t3 tk 6
scoreboard players operation #hzSzR mb /= #t3 tk
execute as @e[type=minecraft:marker,tag=rlk_tk_dl,tag=rlk_tk_p_a1] run function rlk:boss/tachy/core/dash/grow
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players operation #hzEl mb = #el tk
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:34,a:60,tell:1,dmg:100}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/tachy/core/hz_tag/a1
