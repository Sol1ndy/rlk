# D2 pattern tick 28
scoreboard players operation #hzSzR mb = #d2_dl kn
scoreboard players set #t3 kn 15
scoreboard players operation #hzSzR mb *= #t3 kn
scoreboard players set #t3 kn 4
scoreboard players operation #hzSzR mb /= #t3 kn
execute as @e[type=minecraft:marker,tag=rlk_kn_dl,tag=rlk_kn_p_d2] run function rlk:boss/arlecchino/core/dash/grow
execute at @s run particle minecraft:flame ~ ~ ~ 0.3 0.5 0.3 0.04 10 force @a[tag=player]
