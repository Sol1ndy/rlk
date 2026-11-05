# A fight phase starts (P1 after the intro, P2 after the down / the A8 fail; @s any): the phase clock (A6
# grace 200 t), every cooldown ready now, the dwell counters cleared; F1 (HR-04): a counter /
# skill trigger left from the floor time of the last phase is dropped (core/fp ignores them while a step is reserved).
scoreboard players set #ai_pht hr 0
scoreboard players set #far hr 0
scoreboard players set #rear hr 0
scoreboard players set #ai_ff hr 0
scoreboard players set #ai_nx hr 0
scoreboard players set #ctr hr 0
scoreboard players set #a6q hr 0
scoreboard players set #ai_nn hr 0
scoreboard players set #ai_bs hr 0
scoreboard players operation #a6cd hr = #clk hr
scoreboard players operation #ai_rcd hr = #clk hr
scoreboard players remove #ai_rcd hr 200
scoreboard players operation #ai_tmc hr = #clk hr
scoreboard players remove #ai_tmc hr 100
scoreboard players operation #cd_a1 hr = #clk hr
scoreboard players operation #cd_a10 hr = #clk hr
scoreboard players operation #cd_a2 hr = #clk hr
scoreboard players operation #cd_a3 hr = #clk hr
scoreboard players operation #cd_a4 hr = #clk hr
scoreboard players operation #cd_a6 hr = #clk hr
scoreboard players operation #cd_a9 hr = #clk hr
scoreboard players operation #cd_r1 hr = #clk hr
scoreboard players operation #cd_r2 hr = #clk hr
scoreboard players operation #cd_r3 hr = #clk hr
