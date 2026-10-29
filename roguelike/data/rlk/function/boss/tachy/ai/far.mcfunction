# The player stayed farther than 14.0 b for 40 t: A1 or W1 (50 %, no repeat; cooldowns ignored).
execute store result score #t tk run random value 1..100
scoreboard players set #ai_wa1 tk 1
execute if score #last tk matches 1 run scoreboard players set #ai_wa1 tk 0
execute if score #ai_wa1 tk matches 1 run return run function rlk:boss/tachy/ai/go_a1
return fail
