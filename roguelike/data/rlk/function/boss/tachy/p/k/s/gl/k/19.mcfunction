# K stage gl tick 19
scoreboard players operation #hzSzR mb = #k_dl tk
scoreboard players set #t3 tk 20
scoreboard players operation #hzSzR mb *= #t3 tk
scoreboard players set #t3 tk 4
scoreboard players operation #hzSzR mb /= #t3 tk
execute as @e[type=minecraft:marker,tag=rlk_tk_dl,tag=rlk_tk_p_k] run function rlk:boss/tachy/core/dash/grow
