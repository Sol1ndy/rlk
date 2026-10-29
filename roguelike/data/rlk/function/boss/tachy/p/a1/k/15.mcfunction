# A1 pattern tick 15
scoreboard players operation #hzSzR mb = #a1_dl tk
scoreboard players set #t3 tk 10
scoreboard players operation #hzSzR mb *= #t3 tk
scoreboard players set #t3 tk 6
scoreboard players operation #hzSzR mb /= #t3 tk
execute as @e[type=minecraft:marker,tag=rlk_tk_dl,tag=rlk_tk_p_a1] run function rlk:boss/tachy/core/dash/grow
