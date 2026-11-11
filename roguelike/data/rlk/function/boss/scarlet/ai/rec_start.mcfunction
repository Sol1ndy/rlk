# Recovery start (@s = body, after a pattern / a transition): idle P1 12-20 t, P2 14-20 t (api.RECOVER) facing
# the player - the punish window: farther than 6 b she walks in (P1 0.12 b/t) / glides in (P2 0.18 b/t), else strafes.
scoreboard players set #ai_fl hr 0
scoreboard players set #ai_nn hr 0
scoreboard players set #ai_bs hr 0
execute if score #ph hr matches 1 store result score #rec hr run random value 12..20
execute if score #ph hr matches 7 store result score #rec hr run random value 14..20
execute unless score #ph hr matches 1 unless score #ph hr matches 7 run scoreboard players set #rec hr 14
function rlk:boss/scarlet/ai/sample
execute if score #ai_nx hr matches 8 run return run function rlk:boss/scarlet/ai/approach
execute if function rlk:boss/scarlet/ai/tail_keep run return 0
function rlk:boss/scarlet/ai/move_pick
