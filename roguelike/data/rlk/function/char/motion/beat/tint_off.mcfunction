# @s = player. The red-pink glow goes (the landing, or the beat ended early).
execute unless score @s pbTint matches 1 run return 0
scoreboard players set @s pbTint 0
execute as @e[tag=rlk_pm,tag=!rlk_pm_weapon] run function rlk:char/motion/beat/untint
execute as @e[tag=rlk_pl,tag=!rlk_pl_weapon] run function rlk:char/motion/beat/untint
