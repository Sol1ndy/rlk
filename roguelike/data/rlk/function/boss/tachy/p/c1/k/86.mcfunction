# C1 pattern tick 86
scoreboard players operation #hzSzR mb = #c1_dl tk
scoreboard players set #t3 tk 5
scoreboard players operation #hzSzR mb *= #t3 tk
scoreboard players set #t3 tk 4
scoreboard players operation #hzSzR mb /= #t3 tk
execute as @e[type=minecraft:marker,tag=rlk_tk_dl,tag=rlk_tk_p_c1] run function rlk:boss/tachy/core/dash/grow
execute if score #c1_dl tk matches 0..5 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:26,el:1}
execute if score #c1_dl tk matches 0..5 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:26,el:3}
execute if score #c1_dl tk matches 6..10 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:53,el:1}
execute if score #c1_dl tk matches 6..10 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:53,el:3}
execute if score #c1_dl tk matches 11..16 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:80,el:1}
execute if score #c1_dl tk matches 11..16 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/thrust_trail {len:80,el:3}
function rlk:boss/tachy/fx/snd/thrust
function rlk:boss/tachy/el/edge
