# The judge (the final dive's contact; S4 at api.JUDGE_T): the pip windows close and the under bar goes; #gres hr 1 =
# deflect (the shield empty: the gold starburst + light column at the player, the deflect sound, g_deflect), 2 = fail
# (the gauntlet's own branch follows).
kill @e[type=minecraft:marker,tag=rlk_hr_pip]
scoreboard players set #shb hr 0
execute if score #pips hr matches 1.. run return run scoreboard players set #gres hr 2
scoreboard players set #gres hr 1
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.3 ~ run function rlk:boss/scarlet/fx/p/clash_gold
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/scarlet/fx/p/light_column
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/scarlet/fx/snd/deflect
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/scarlet/rig/play/g_deflect
