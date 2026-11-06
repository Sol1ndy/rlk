# The player stayed behind her (20 of 30 t, P2): Q3 80 % (its cooldown
# and the no-repeat rule kept). Fails when not taken.
execute store result score #t kn run random value 1..100
execute if score #t kn matches 81.. run return fail
scoreboard players set #ai_wq3 kn 1
execute if score #cd_Q3 kn > #clk kn run scoreboard players set #ai_wq3 kn 0
execute if score #last kn matches 13 run scoreboard players set #ai_wq3 kn 0
execute if score #ai_wq3 kn matches 1 run return run function rlk:boss/arlecchino/ai/go_q3_p2
return fail
