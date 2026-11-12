# A1 pattern tick 14
function rlk:boss/tachy/rig/look/chest/off
scoreboard players operation #hzSzR mb = #a1_dl tk
scoreboard players set #t3 tk 5
scoreboard players operation #hzSzR mb *= #t3 tk
scoreboard players set #t3 tk 6
scoreboard players operation #hzSzR mb /= #t3 tk
execute as @e[type=minecraft:marker,tag=rlk_tk_dl,tag=rlk_tk_p_a1] run function rlk:boss/tachy/core/dash/grow
execute if score #a1_dl tk matches 0..8 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:40,el:1}
execute if score #a1_dl tk matches 0..8 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:40,el:3}
execute if score #a1_dl tk matches 9..16 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:80,el:1}
execute if score #a1_dl tk matches 9..16 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:80,el:3}
execute if score #a1_dl tk matches 17..24 if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:120,el:1}
execute if score #a1_dl tk matches 17..24 if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/dash_trail {len:120,el:3}
function rlk:boss/tachy/fx/snd/dash
