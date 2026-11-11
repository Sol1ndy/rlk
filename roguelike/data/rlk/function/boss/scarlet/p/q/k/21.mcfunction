# Q pattern tick 21
execute if score #hpp hr matches 1.. run scoreboard players set #q_hit hr 1
execute unless score #q_hit hr matches 1 run function rlk:boss/scarlet/rig/play/g_reform
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/rig/play/q_air
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/thrown
