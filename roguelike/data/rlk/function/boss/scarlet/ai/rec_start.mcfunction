# Recovery start (@s = body, after a pattern / a transition): idle P1 16-24 t, P2 12-18 t (api.RECOVER) facing the
# player - the punish window: farther than 6 b she walks in (P1 0.12 b/t) / glides in (P2 0.18 b/t), else strafes.
scoreboard players set #ai_fl hr 0
execute if score #ph hr matches 1 store result score #rec hr run random value 16..24
execute if score #ph hr matches 7 store result score #rec hr run random value 12..18
execute unless score #ph hr matches 1 unless score #ph hr matches 7 run scoreboard players set #rec hr 12
function rlk:boss/scarlet/ai/sample
execute if score #ai_nx hr matches 3 run return run function rlk:boss/scarlet/ai/approach
execute if score #ai_d2 hr matches 360001.. if score #ph hr matches 7 run scoreboard players set #ai_mv hr 5
execute if score #ai_d2 hr matches 360001.. unless score #ph hr matches 7 run scoreboard players set #ai_mv hr 1
execute if score #ai_d2 hr matches 360001.. run return run function rlk:boss/scarlet/ai/play_move
execute store result score #ai_mv hr run random value 2..3
function rlk:boss/scarlet/ai/play_move
