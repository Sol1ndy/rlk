# Start A3S 쌍월참 (@s = body; the AI, the triggers, tests): the clock, the no-repeat memory, the
# cooldown of the fight phase.
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/rig/look/blade/edge
scoreboard players set #pat hr 8
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
scoreboard players set #ppf hr 0
scoreboard players set #ultq hr 0
scoreboard players set #hits hr 0
scoreboard players operation #last2 hr = #last hr
scoreboard players set #last hr 8
execute if score #ph hr matches 1 run scoreboard players operation #cd_a3s hr = #clk hr
execute if score #ph hr matches 1 run scoreboard players add #cd_a3s hr 140
execute if score #ph hr matches 7 run scoreboard players operation #cd_a3s hr = #clk hr
execute if score #ph hr matches 7 run scoreboard players add #cd_a3s hr 100
function rlk:boss/scarlet/p/a3s/start
