# One idle tick (@s = body, #pat 0): face the player, walk / glide / strafe (mv/ok-checked), the flinch (6 t, no step;
# F1 HR-25: its last tick plays the move clip again), then the decision when the recovery ran out.
execute if score #rec hr matches 1.. run scoreboard players remove #rec hr 1
function rlk:mboss/mv/turn {max:10}
execute if score #ai_fl hr matches 1 run function rlk:boss/scarlet/ai/play_move
execute if score #ai_fl hr matches 1.. run scoreboard players remove #ai_fl hr 1
execute if score #ai_fl hr matches 1.. run return 0
function rlk:boss/scarlet/ai/step
execute if score #rec hr matches ..0 run function rlk:boss/scarlet/ai/decide
