# Weighted pick, phase 3, near (api.WEIGHTS; zeroed when cooling down / repeating / K rules).
scoreboard players set #ai_sum tk 0
scoreboard players set #ai_w_b1 tk 15
execute if score #cd_b1 tk > #clk tk run scoreboard players set #ai_w_b1 tk 0
execute if score #last tk matches 2 run scoreboard players set #ai_w_b1 tk 0
scoreboard players operation #ai_sum tk += #ai_w_b1 tk
scoreboard players set #ai_w_b2 tk 10
execute if score #cd_b2 tk > #clk tk run scoreboard players set #ai_w_b2 tk 0
execute if score #last tk matches 3 run scoreboard players set #ai_w_b2 tk 0
scoreboard players operation #ai_sum tk += #ai_w_b2 tk
scoreboard players set #ai_w_b3 tk 20
execute if score #cd_b3 tk > #clk tk run scoreboard players set #ai_w_b3 tk 0
execute if score #last tk matches 4 run scoreboard players set #ai_w_b3 tk 0
scoreboard players operation #ai_sum tk += #ai_w_b3 tk
scoreboard players set #ai_w_c2 tk 15
execute if score #cd_c2 tk > #clk tk run scoreboard players set #ai_w_c2 tk 0
execute if score #last tk matches 6 run scoreboard players set #ai_w_c2 tk 0
scoreboard players operation #ai_sum tk += #ai_w_c2 tk
scoreboard players set #ai_w_c3 tk 25
execute if score #cd_c3 tk > #clk tk run scoreboard players set #ai_w_c3 tk 0
execute if score #last tk matches 7 run scoreboard players set #ai_w_c3 tk 0
scoreboard players operation #ai_sum tk += #ai_w_c3 tk
scoreboard players set #ai_w_k tk 15
execute if score #cd_k tk > #clk tk run scoreboard players set #ai_w_k tk 0
execute if score #last tk matches 8 run scoreboard players set #ai_w_k tk 0
execute if score #kgap tk matches ..1 run scoreboard players set #ai_w_k tk 0
execute if score #last tk matches 5..7 run scoreboard players set #ai_w_k tk 0
scoreboard players operation #ai_sum tk += #ai_w_k tk
execute if score #ai_sum tk matches ..0 run return run function rlk:boss/tachy/ai/none
execute store result score #ai_r tk run random value 0..999
scoreboard players operation #ai_r tk *= #ai_sum tk
scoreboard players operation #ai_r tk /= #c1000 tk
execute if score #ai_r tk < #ai_w_b1 tk run return run function rlk:boss/tachy/core/start/b1
scoreboard players operation #ai_r tk -= #ai_w_b1 tk
execute if score #ai_r tk < #ai_w_b2 tk run return run function rlk:boss/tachy/core/start/b2
scoreboard players operation #ai_r tk -= #ai_w_b2 tk
execute if score #ai_r tk < #ai_w_b3 tk run return run function rlk:boss/tachy/core/start/b3
scoreboard players operation #ai_r tk -= #ai_w_b3 tk
execute if score #ai_r tk < #ai_w_c2 tk run return run function rlk:boss/tachy/core/start/c2
scoreboard players operation #ai_r tk -= #ai_w_c2 tk
execute if score #ai_r tk < #ai_w_c3 tk run return run function rlk:boss/tachy/core/start/c3
scoreboard players operation #ai_r tk -= #ai_w_c3 tk
execute if score #ai_r tk < #ai_w_k tk run return run function rlk:boss/tachy/core/start/k
scoreboard players operation #ai_r tk -= #ai_w_k tk
function rlk:boss/tachy/ai/none
