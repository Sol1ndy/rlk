# Nothing may run now (every candidate cooling down): the recovery goes on a little longer (8 t); F1 (HR-13): a
# second empty pick in a row (no pattern between) -> the backstep, then the mid pick.
execute if score #ai_nn hr matches 1.. run return run function rlk:boss/scarlet/ai/backstep
scoreboard players set #ai_nn hr 1
scoreboard players set #rec hr 8
