# RINGS pattern tick 54
execute if score #ph hr matches 7 at @s rotated as @s rotated ~ 0 positioned ~ ~1.1 ~ run function rlk:boss/scarlet/fx/p/qi_ring {r:26,c:1}
execute if score #ph hr matches 7 at @s run function rlk:boss/scarlet/fx/snd/g_ring
execute if score #ph hr matches 1 run scoreboard players set #done hr 1
