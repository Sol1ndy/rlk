# D1 pattern tick 26
scoreboard players operation #hzSzR mb = #d1_dl kn
scoreboard players set #t3 kn 5
scoreboard players operation #hzSzR mb *= #t3 kn
scoreboard players set #t3 kn 4
scoreboard players operation #hzSzR mb /= #t3 kn
execute as @e[type=minecraft:marker,tag=rlk_kn_dl,tag=rlk_kn_p_d1] run function rlk:boss/arlecchino/core/dash/grow
execute if score #d1_dl kn matches 0..9 at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run function rlk:boss/arlecchino/fx/p/dash_trail {len:46,c:1}
execute if score #d1_dl kn matches 10..18 at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run function rlk:boss/arlecchino/fx/p/dash_trail {len:93,c:1}
execute if score #d1_dl kn matches 19..28 at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run function rlk:boss/arlecchino/fx/p/dash_trail {len:140,c:1}
execute at @s run function rlk:boss/arlecchino/fx/snd/dash
