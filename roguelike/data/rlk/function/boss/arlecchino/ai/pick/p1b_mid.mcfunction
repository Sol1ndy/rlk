# Weighted pick, p1b, mid (api.WEIGHTS; zeroed when cooling down / repeating / A out of reach).
scoreboard players set #ai_sum kn 0
scoreboard players set #ai_wA kn 10
execute if score #cd_A kn > #clk kn run scoreboard players set #ai_wA kn 0
execute if score #last kn matches 1 run scoreboard players set #ai_wA kn 0
execute if score #ai_d2 kn matches 490001.. run scoreboard players set #ai_wA kn 0
scoreboard players operation #ai_sum kn += #ai_wA kn
scoreboard players set #ai_wB kn 30
execute if score #cd_B kn > #clk kn run scoreboard players set #ai_wB kn 0
execute if score #last kn matches 2 run scoreboard players set #ai_wB kn 0
scoreboard players operation #ai_sum kn += #ai_wB kn
scoreboard players set #ai_wC kn 25
execute if score #cd_C kn > #clk kn run scoreboard players set #ai_wC kn 0
execute if score #last kn matches 3 run scoreboard players set #ai_wC kn 0
scoreboard players operation #ai_sum kn += #ai_wC kn
scoreboard players set #ai_wD kn 20
execute if score #cd_D kn > #clk kn run scoreboard players set #ai_wD kn 0
execute if score #last kn matches 4 run scoreboard players set #ai_wD kn 0
scoreboard players operation #ai_sum kn += #ai_wD kn
scoreboard players set #ai_wE kn 20
execute if score #cd_E kn > #clk kn run scoreboard players set #ai_wE kn 0
execute if score #last kn matches 5 run scoreboard players set #ai_wE kn 0
scoreboard players operation #ai_sum kn += #ai_wE kn
scoreboard players set #ai_wG kn 20
execute if score #cd_G kn > #clk kn run scoreboard players set #ai_wG kn 0
execute if score #last kn matches 6 run scoreboard players set #ai_wG kn 0
scoreboard players operation #ai_sum kn += #ai_wG kn
scoreboard players set #ai_wH kn 15
execute if score #cd_H kn > #clk kn run scoreboard players set #ai_wH kn 0
execute if score #last kn matches 7 run scoreboard players set #ai_wH kn 0
scoreboard players operation #ai_sum kn += #ai_wH kn
execute if score #ai_sum kn matches ..0 run return run function rlk:boss/arlecchino/ai/none
execute store result score #ai_r kn run random value 0..999
scoreboard players operation #ai_r kn *= #ai_sum kn
scoreboard players operation #ai_r kn /= #c1000 kn
execute if score #ai_r kn < #ai_wA kn run return run function rlk:boss/arlecchino/ai/go_a_p1b
scoreboard players operation #ai_r kn -= #ai_wA kn
execute if score #ai_r kn < #ai_wB kn run return run function rlk:boss/arlecchino/ai/go_b_p1b
scoreboard players operation #ai_r kn -= #ai_wB kn
execute if score #ai_r kn < #ai_wC kn run return run function rlk:boss/arlecchino/ai/go_c_p1b
scoreboard players operation #ai_r kn -= #ai_wC kn
execute if score #ai_r kn < #ai_wD kn run return run function rlk:boss/arlecchino/ai/go_d_p1b
scoreboard players operation #ai_r kn -= #ai_wD kn
execute if score #ai_r kn < #ai_wE kn run return run function rlk:boss/arlecchino/ai/go_e_p1b
scoreboard players operation #ai_r kn -= #ai_wE kn
execute if score #ai_r kn < #ai_wG kn run return run function rlk:boss/arlecchino/ai/go_g_p1b
scoreboard players operation #ai_r kn -= #ai_wG kn
execute if score #ai_r kn < #ai_wH kn run return run function rlk:boss/arlecchino/ai/go_h_p1b
scoreboard players operation #ai_r kn -= #ai_wH kn
function rlk:boss/arlecchino/ai/none
