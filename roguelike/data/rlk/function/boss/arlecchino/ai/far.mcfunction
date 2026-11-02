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
return fail
