# The player stayed farther than 14 b for 40 t: the gap closer - D (P1) / Q2 (P2) 60 %,
# else C / Q4 (cooldowns ignored, no immediate repeat). Fails when neither may run.
execute store result score #t kn run random value 1..100
scoreboard players set #ai_fD kn 1
execute if score #last kn matches 4 run scoreboard players set #ai_fD kn 0
scoreboard players set #ai_fC kn 1
execute if score #last kn matches 3 run scoreboard players set #ai_fC kn 0
execute if score #ph kn matches 1 if score #t kn matches ..60 if score #ai_fD kn matches 1 run return run function rlk:boss/arlecchino/ai/go_d_p1a
execute if score #ph kn matches 1 if score #ai_fC kn matches 1 run return run function rlk:boss/arlecchino/ai/go_c_p1a
execute if score #ph kn matches 1 if score #ai_fD kn matches 1 run return run function rlk:boss/arlecchino/ai/go_d_p1a
execute if score #ph kn matches 1 if score #ai_fC kn matches 1 run return run function rlk:boss/arlecchino/ai/go_c_p1a
scoreboard players set #ai_fD kn 1
execute if score #last kn matches 4 run scoreboard players set #ai_fD kn 0
scoreboard players set #ai_fC kn 1
execute if score #last kn matches 3 run scoreboard players set #ai_fC kn 0
execute if score #ph kn matches 3 if score #t kn matches ..60 if score #ai_fD kn matches 1 run return run function rlk:boss/arlecchino/ai/go_d_p1b
execute if score #ph kn matches 3 if score #ai_fC kn matches 1 run return run function rlk:boss/arlecchino/ai/go_c_p1b
execute if score #ph kn matches 3 if score #ai_fD kn matches 1 run return run function rlk:boss/arlecchino/ai/go_d_p1b
execute if score #ph kn matches 3 if score #ai_fC kn matches 1 run return run function rlk:boss/arlecchino/ai/go_c_p1b
scoreboard players set #ai_fQ2 kn 1
execute if score #last kn matches 12 run scoreboard players set #ai_fQ2 kn 0
scoreboard players set #ai_fQ4 kn 1
execute if score #last kn matches 14 run scoreboard players set #ai_fQ4 kn 0
execute if score #ph kn matches 5 if score #t kn matches ..60 if score #ai_fQ2 kn matches 1 run return run function rlk:boss/arlecchino/ai/go_q2_p2
execute if score #ph kn matches 5 if score #ai_fQ4 kn matches 1 run return run function rlk:boss/arlecchino/ai/go_q4_p2
execute if score #ph kn matches 5 if score #ai_fQ2 kn matches 1 run return run function rlk:boss/arlecchino/ai/go_q2_p2
execute if score #ph kn matches 5 if score #ai_fQ4 kn matches 1 run return run function rlk:boss/arlecchino/ai/go_q4_p2
return fail
