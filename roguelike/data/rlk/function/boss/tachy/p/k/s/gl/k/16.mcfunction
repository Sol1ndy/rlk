# K stage gl tick 16
scoreboard players operation #hzSzR mb = #k_dl tk
scoreboard players set #t3 tk 5
scoreboard players operation #hzSzR mb *= #t3 tk
scoreboard players set #t3 tk 4
scoreboard players operation #hzSzR mb /= #t3 tk
execute as @e[type=minecraft:marker,tag=rlk_tk_dl,tag=rlk_tk_p_k] run function rlk:boss/tachy/core/dash/grow
execute if score #k_dl tk matches 0..4 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:20,el:1}
execute if score #k_dl tk matches 0..4 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:20,el:3}
execute if score #k_dl tk matches 5..8 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:40,el:1}
execute if score #k_dl tk matches 5..8 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:40,el:3}
execute if score #k_dl tk matches 9..12 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:60,el:1}
execute if score #k_dl tk matches 9..12 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:60,el:3}
execute at @s run function rlk:boss/tachy/fx/snd/thrust
function rlk:boss/tachy/el/edge
