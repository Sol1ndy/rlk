# The far fallback's approach ended: A3S (its cooldown and the no-repeat rule kept; else the normal pick).
scoreboard players set #ai_nx hr 0
scoreboard players set #ai_wa3s hr 1
execute if score #cd_a3s hr > #clk hr run scoreboard players set #ai_wa3s hr 0
execute if score #last hr matches 8 run scoreboard players set #ai_wa3s hr 0
execute if score #ai_wa3s hr matches 1 run return run function rlk:boss/scarlet/core/start/a3s
function rlk:boss/scarlet/ai/decide
