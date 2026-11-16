# Weighted pick, p2, near (api.WEIGHTS; zeroed when cooling down / repeating / A out of reach).
scoreboard players set #ai_sum kn 0
scoreboard players set #ai_wQ1 kn 25
execute if score #cd_Q1 kn > #clk kn run scoreboard players set #ai_wQ1 kn 0
execute if score #last kn matches 11 run scoreboard players set #ai_wQ1 kn 0
scoreboard players operation #ai_sum kn += #ai_wQ1 kn
scoreboard players set #ai_wQ2 kn 10
execute if score #cd_Q2 kn > #clk kn run scoreboard players set #ai_wQ2 kn 0
execute if score #last kn matches 12 run scoreboard players set #ai_wQ2 kn 0
scoreboard players operation #ai_sum kn += #ai_wQ2 kn
scoreboard players set #ai_wQ4 kn 15
execute if score #cd_Q4 kn > #clk kn run scoreboard players set #ai_wQ4 kn 0
execute if score #last kn matches 14 run scoreboard players set #ai_wQ4 kn 0
scoreboard players operation #ai_sum kn += #ai_wQ4 kn
scoreboard players set #ai_wQ6 kn 15
execute if score #cd_Q6 kn > #clk kn run scoreboard players set #ai_wQ6 kn 0
execute if score #last kn matches 16 run scoreboard players set #ai_wQ6 kn 0
execute if score #ai_pht kn matches ..399 run scoreboard players set #ai_wQ6 kn 0
scoreboard players operation #ai_sum kn += #ai_wQ6 kn
execute if score #ai_sum kn matches ..0 run return run function rlk:boss/arlecchino/ai/none
execute store result score #ai_r kn run random value 0..999
scoreboard players operation #ai_r kn *= #ai_sum kn
scoreboard players operation #ai_r kn /= #c1000 kn
execute if score #ai_r kn < #ai_wQ1 kn run return run function rlk:boss/arlecchino/ai/go_q1_p2
scoreboard players operation #ai_r kn -= #ai_wQ1 kn
execute if score #ai_r kn < #ai_wQ2 kn run return run function rlk:boss/arlecchino/ai/go_q2_p2
scoreboard players operation #ai_r kn -= #ai_wQ2 kn
execute if score #ai_r kn < #ai_wQ4 kn run return run function rlk:boss/arlecchino/ai/go_q4_p2
scoreboard players operation #ai_r kn -= #ai_wQ4 kn
execute if score #ai_r kn < #ai_wQ6 kn run return run function rlk:boss/arlecchino/ai/go_q6_p2
scoreboard players operation #ai_r kn -= #ai_wQ6 kn
function rlk:boss/arlecchino/ai/none
