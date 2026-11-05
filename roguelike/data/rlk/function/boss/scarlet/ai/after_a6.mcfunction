# The decision 16 t after A6: the far rule when the player is farther than 8 b (no dwell
# needed), else the normal pick (fails).
scoreboard players set #ai_ff hr 0
execute unless score #ai_d2 hr matches 640001.. run return fail
function rlk:boss/scarlet/ai/far
return 1
