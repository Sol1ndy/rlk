# The judge (the final dive's contact; S4 at api.JUDGE_T): the pip windows close and the under bar goes; #gres hr 1 =
# deflect (the shield empty: the gold starburst + light column at the player, the deflect sound, g_deflect), 2 = fail
# (the gauntlet's own branch follows).
kill @e[type=minecraft:marker,tag=rlk_hr_pip]
scoreboard players set #shb hr 0
execute if score #pips hr matches 1.. run return run scoreboard players set #gres hr 2
scoreboard players set #gres hr 1
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.3 ~ run particle minecraft:end_rod ~ ~ ~ 0.4 0.4 0.4 0.15 24 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.3 ~ run particle minecraft:dust{color:[1.0,0.88,0.29],scale:1.6} ~ ~ ~ 0.3 0.3 0.3 0 12 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:end_rod ~ ~ ~ 0.1 1.6 0.1 0.02 16 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.anvil.land hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.player.attack.crit hostile @a[tag=player] ~ ~ ~ 0.8 1 0.27
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/scarlet/rig/play/g_deflect
