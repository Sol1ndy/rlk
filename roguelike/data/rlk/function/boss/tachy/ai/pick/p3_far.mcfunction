# Weighted pick, phase 3, far (api.WEIGHTS; zeroed when cooling down / repeating / K rules).
scoreboard players set #ai_sum tk 0
scoreboard players set #ai_w_a1 tk 25
execute if score #cd_a1 tk > #clk tk run scoreboard players set #ai_w_a1 tk 0
execute if score #last tk matches 1 run scoreboard players set #ai_w_a1 tk 0
scoreboard players operation #ai_sum tk += #ai_w_a1 tk
execute if score #ai_sum tk matches ..0 run return run function rlk:boss/tachy/ai/none
execute store result score #ai_r tk run random value 0..999
scoreboard players operation #ai_r tk *= #ai_sum tk
scoreboard players operation #ai_r tk /= #c1000 tk
execute if score #ai_r tk < #ai_w_a1 tk run return run function rlk:boss/tachy/core/start/a1
scoreboard players operation #ai_r tk -= #ai_w_a1 tk
function rlk:boss/tachy/ai/none
