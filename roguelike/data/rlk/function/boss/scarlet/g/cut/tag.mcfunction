# @s = the cut hazard just made: its strike tick (objective hr), the cut + pattern tags of the running pattern (#pat),
# rlk_hr_cnt for a counting cut (the gauntlets).
scoreboard players operation @s hr = #g_s hr
tag @s add rlk_hr_cut
tag @s add rlk_hr_p
execute if score #g_n hr matches 1 run tag @s add rlk_hr_cnt
execute if score #pat hr matches 11 run tag @s add rlk_hr_p_r1
execute if score #pat hr matches 12 run tag @s add rlk_hr_p_r2
execute if score #pat hr matches 13 run tag @s add rlk_hr_p_r3
execute if score #pat hr matches 21 run tag @s add rlk_hr_p_a8
execute if score #pat hr matches 27 run tag @s add rlk_hr_p_a13
