# A fight phase starts (P1 after the intro, P2 after T1, P3 after T2; @s any): weights column, forced-swap limit,
# the phase clock (L first use), the cooldowns reset to ready.
execute if score #ph tk matches 1 run scoreboard players set #ai_fp tk 1
execute if score #ph tk matches 4 run scoreboard players set #ai_fp tk 2
execute if score #ph tk matches 7 run scoreboard players set #ai_fp tk 3
execute if score #ai_fp tk matches 1 run scoreboard players set #ai_swl tk 600
execute if score #ai_fp tk matches 2 run scoreboard players set #ai_swl tk 600
execute if score #ai_fp tk matches 3 run scoreboard players set #ai_swl tk 400
scoreboard players set #ai_pht tk 0
scoreboard players operation #cd_a1 tk = #clk tk
scoreboard players operation #cd_b1 tk = #clk tk
scoreboard players operation #cd_b2 tk = #clk tk
scoreboard players operation #cd_b3 tk = #clk tk
scoreboard players operation #cd_c1 tk = #clk tk
scoreboard players operation #cd_c2 tk = #clk tk
scoreboard players operation #cd_c3 tk = #clk tk
