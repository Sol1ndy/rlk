# D2 pattern tick 26
scoreboard players operation #hzSzR mb = #d2_dl kn
scoreboard players set #t3 kn 5
scoreboard players operation #hzSzR mb *= #t3 kn
scoreboard players set #t3 kn 4
scoreboard players operation #hzSzR mb /= #t3 kn
execute as @e[type=minecraft:marker,tag=rlk_kn_dl,tag=rlk_kn_p_d2] run function rlk:boss/arlecchino/core/dash/grow
execute at @s run particle minecraft:flame ~ ~ ~ 0.4 0.5 0.4 0.06 16 force @a[tag=player]
execute at @s run playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @s run playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.5 1.6 0.17
