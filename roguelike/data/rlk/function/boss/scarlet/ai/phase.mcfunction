# A fight phase starts (P1 after the intro, P2 after the down / the A8 fail; @s any): the phase clock (A6
# grace 200 t), every cooldown ready now, the dwell counters cleared.
scoreboard players set #ai_pht hr 0
scoreboard players set #far hr 0
scoreboard players set #rear hr 0
scoreboard players set #ai_ff hr 0
scoreboard players set #ai_nx hr 0
scoreboard players operation #a6cd hr = #clk hr
scoreboard players operation #ai_rcd hr = #clk hr
scoreboard players remove #ai_rcd hr 200
scoreboard players operation #cd_a1 hr = #clk hr
scoreboard players operation #cd_a10 hr = #clk hr
scoreboard players operation #cd_a2 hr = #clk hr
scoreboard players operation #cd_a3 hr = #clk hr
scoreboard players operation #cd_a4 hr = #clk hr
scoreboard players operation #cd_a6 hr = #clk hr
scoreboard players operation #cd_a9 hr = #clk hr
