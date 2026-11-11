# Start A9 황광 원참 (@s = body; the AI, the triggers, tests): the clock, the no-repeat memory, the
# cooldown of the fight phase.
function rlk:boss/scarlet/core/stop_move
scoreboard players set #pat hr 6
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
scoreboard players set #ppf hr 0
scoreboard players set #ultq hr 0
scoreboard players set #hits hr 0
scoreboard players operation #last2 hr = #last hr
scoreboard players set #last hr 6
execute if score #ph hr matches 1 run scoreboard players operation #cd_a9 hr = #clk hr
execute if score #ph hr matches 1 run scoreboard players add #cd_a9 hr 220
execute if score #ph hr matches 7 run scoreboard players operation #cd_a9 hr = #clk hr
execute if score #ph hr matches 7 run scoreboard players add #cd_a9 hr 140
function rlk:boss/scarlet/p/a9/start
