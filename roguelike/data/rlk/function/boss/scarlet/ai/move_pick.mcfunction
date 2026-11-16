# The recovery move (@s = body, #ai_d2 sampled): farther than 6 b walk in (P1) / glide in (P2), else strafe
# left / right at random; its clip (ai/play_move). Each tick ai/step moves her (mv/ok-checked).
execute if score #ai_d2 hr matches 360001.. if score #ph hr matches 7 run scoreboard players set #ai_mv hr 5
execute if score #ai_d2 hr matches 360001.. unless score #ph hr matches 7 run scoreboard players set #ai_mv hr 1
execute if score #ai_d2 hr matches 360001.. run return run function rlk:boss/scarlet/ai/play_move
execute store result score #ai_mv hr run random value 2..3
function rlk:boss/scarlet/ai/play_move
