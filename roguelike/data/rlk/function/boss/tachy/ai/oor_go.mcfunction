# A melee chain of this phase with the gap closer (cooldowns and the no-repeat rule kept). Fails when none may run.
scoreboard players set #ai_o1c1 tk 1
execute if score #cd_c1 tk > #clk tk run scoreboard players set #ai_o1c1 tk 0
execute if score #last tk matches 5 run scoreboard players set #ai_o1c1 tk 0
execute if score #ai_fp tk matches 1 if score #ai_o1c1 tk matches 1 run return run function rlk:boss/tachy/ai/go_c1
scoreboard players set #ai_o1b2 tk 1
execute if score #cd_b2 tk > #clk tk run scoreboard players set #ai_o1b2 tk 0
execute if score #last tk matches 3 run scoreboard players set #ai_o1b2 tk 0
execute if score #ai_fp tk matches 1 if score #ai_o1b2 tk matches 1 run return run function rlk:boss/tachy/ai/go_b2
scoreboard players set #ai_o2c2 tk 1
execute if score #cd_c2 tk > #clk tk run scoreboard players set #ai_o2c2 tk 0
execute if score #last tk matches 6 run scoreboard players set #ai_o2c2 tk 0
execute if score #ai_fp tk matches 2 if score #ai_o2c2 tk matches 1 run return run function rlk:boss/tachy/ai/go_c2
scoreboard players set #ai_o2b1 tk 1
execute if score #cd_b1 tk > #clk tk run scoreboard players set #ai_o2b1 tk 0
execute if score #last tk matches 2 run scoreboard players set #ai_o2b1 tk 0
execute if score #ai_fp tk matches 2 if score #ai_o2b1 tk matches 1 run return run function rlk:boss/tachy/ai/go_b1
scoreboard players set #ai_o2b2 tk 1
execute if score #cd_b2 tk > #clk tk run scoreboard players set #ai_o2b2 tk 0
execute if score #last tk matches 3 run scoreboard players set #ai_o2b2 tk 0
execute if score #ai_fp tk matches 2 if score #ai_o2b2 tk matches 1 run return run function rlk:boss/tachy/ai/go_b2
scoreboard players set #ai_o3c3 tk 1
execute if score #cd_c3 tk > #clk tk run scoreboard players set #ai_o3c3 tk 0
execute if score #last tk matches 7 run scoreboard players set #ai_o3c3 tk 0
execute if score #ai_fp tk matches 3 if score #ai_o3c3 tk matches 1 run return run function rlk:boss/tachy/ai/go_c3
scoreboard players set #ai_o3b2 tk 1
execute if score #cd_b2 tk > #clk tk run scoreboard players set #ai_o3b2 tk 0
execute if score #last tk matches 3 run scoreboard players set #ai_o3b2 tk 0
execute if score #ai_fp tk matches 3 if score #ai_o3b2 tk matches 1 run return run function rlk:boss/tachy/ai/go_b2
scoreboard players set #ai_o3c2 tk 1
execute if score #cd_c2 tk > #clk tk run scoreboard players set #ai_o3c2 tk 0
execute if score #last tk matches 6 run scoreboard players set #ai_o3c2 tk 0
execute if score #ai_fp tk matches 3 if score #ai_o3c2 tk matches 1 run return run function rlk:boss/tachy/ai/go_c2
return fail
