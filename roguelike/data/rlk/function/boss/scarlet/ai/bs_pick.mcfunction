# F1 (HR-13): the decision after the backstep: the mid pick of the fight phase (cooldowns, no repeat, MID_MAX).
scoreboard players set #ai_bs hr 0
execute if score #ph hr matches 1 run return run function rlk:boss/scarlet/ai/pick/p1_mid
execute if score #ph hr matches 7 run return run function rlk:boss/scarlet/ai/pick/p2_mid
function rlk:boss/scarlet/ai/none
