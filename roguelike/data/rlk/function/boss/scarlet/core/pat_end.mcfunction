# The pattern set #done (@s = body): the lock marker gone, on the floor, then the recovery (after A6: the decision
# at once, 16 t after the blink, with the far rule; PLAN §4.3).
scoreboard players set #done hr 0
scoreboard players operation #dec hr = #pat hr
scoreboard players set #pat hr 0
scoreboard players set #pt hr 0
kill @e[type=minecraft:marker,tag=rlk_hr_lock]
function rlk:boss/scarlet/core/ground
execute if score #dec hr matches 5 run scoreboard players set #ai_ff hr 1
execute if score #dec hr matches 5 run return run function rlk:boss/scarlet/ai/decide
function rlk:boss/scarlet/ai/rec_start
