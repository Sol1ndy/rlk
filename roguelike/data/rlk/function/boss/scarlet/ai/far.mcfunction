# The player stayed farther than 8 b for 30 t (or right after A6): the gap
# closer of the fight phase (FAR_RULE weights; cooldowns and no-repeat kept); none may run -> glide in + A3.
execute if score #ph hr matches 1 run return run function rlk:boss/scarlet/ai/far_p1
execute if score #ph hr matches 7 run return run function rlk:boss/scarlet/ai/far_p2
function rlk:boss/scarlet/ai/far_none
