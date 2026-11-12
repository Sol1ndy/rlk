# @s = the cut hazard just made: its strike tick (objective hr), the cut + pattern tags of the running pattern (#pat),
# rlk_hr_cnt for a counting cut (the gauntlets).
scoreboard players operation @s hr = #g_s hr
tag @s add rlk_hr_cut
tag @s add rlk_hr_p
execute if score #g_n hr matches 1 run tag @s add rlk_hr_cnt
execute if score #pat hr matches 16 run tag @s add rlk_hr_p_mx
execute if score #pat hr matches 17 run tag @s add rlk_hr_p_nb
execute if score #pat hr matches 18 run tag @s add rlk_hr_p_q
execute if score #pat hr matches 21 run tag @s add rlk_hr_p_a8
execute if score #pat hr matches 27 run tag @s add rlk_hr_p_a13
