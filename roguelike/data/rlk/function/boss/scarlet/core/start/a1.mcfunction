# Start A1 회전 반월참 (@s = body; the AI, the triggers, tests): the clock, the no-repeat memory, the
# cooldown of the fight phase.
function rlk:boss/scarlet/core/stop_move
scoreboard players set #pat hr 1
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
scoreboard players set #hits hr 0
scoreboard players operation #last2 hr = #last hr
scoreboard players set #last hr 1
execute if score #ph hr matches 1 run scoreboard players operation #cd_a1 hr = #clk hr
execute if score #ph hr matches 1 run scoreboard players add #cd_a1 hr 100
execute if score #ph hr matches 7 run scoreboard players operation #cd_a1 hr = #clk hr
execute if score #ph hr matches 7 run scoreboard players add #cd_a1 hr 85
function rlk:boss/scarlet/p/a1/start
