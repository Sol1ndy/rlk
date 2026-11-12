# C3 pattern tick 99
scoreboard players operation #hzSzR mb = #c3_dl tk
scoreboard players set #t3 tk 10
scoreboard players operation #hzSzR mb *= #t3 tk
scoreboard players set #t3 tk 4
scoreboard players operation #hzSzR mb /= #t3 tk
execute as @e[type=minecraft:marker,tag=rlk_tk_dl,tag=rlk_tk_p_c3] run function rlk:boss/tachy/core/dash/grow
