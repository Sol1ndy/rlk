# The player stayed behind her (20 of 30 t): B2 70 % or K 30 % (no repeat, K rules; cooldowns ignored). Fails when neither may run.
execute store result score #t tk run random value 1..100
scoreboard players set #ai_wb tk 1
execute if score #last tk matches 3 run scoreboard players set #ai_wb tk 0
execute if score #ai_wb tk matches 1 run return run function rlk:boss/tachy/ai/go_b2
return fail
