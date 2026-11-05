# Start A6 후방 섬보 (@s = body; the AI, the triggers, tests): the clock, the no-repeat memory, the
# cooldown of the fight phase.
function rlk:boss/scarlet/core/stop_move
scoreboard players set #pat hr 5
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
scoreboard players set #hits hr 0
scoreboard players operation #last2 hr = #last hr
scoreboard players set #last hr 5
execute if score #ph hr matches 1 run scoreboard players operation #cd_a6 hr = #clk hr
execute if score #ph hr matches 1 run scoreboard players add #cd_a6 hr 400
execute if score #ph hr matches 7 run scoreboard players operation #cd_a6 hr = #clk hr
execute if score #ph hr matches 7 run scoreboard players add #cd_a6 hr 400
execute if score #ph hr matches 1 run scoreboard players operation #a6cd hr = #clk hr
execute if score #ph hr matches 1 run scoreboard players add #a6cd hr 400
execute if score #ph hr matches 7 run scoreboard players operation #a6cd hr = #clk hr
execute if score #ph hr matches 7 run scoreboard players add #a6cd hr 400
tag @s add rlk_mb_inv
function rlk:boss/scarlet/p/a6/start
