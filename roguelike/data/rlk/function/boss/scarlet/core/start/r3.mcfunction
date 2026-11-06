# Start R3 자영 활강 (@s = body; the AI, the triggers, tests): the clock, the no-repeat memory, the
# cooldown of the fight phase.
function rlk:boss/scarlet/core/stop_move
scoreboard players set #pat hr 13
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
scoreboard players set #hits hr 0
scoreboard players operation #last2 hr = #last hr
scoreboard players set #last hr 13
execute if score #ph hr matches 7 run scoreboard players operation #cd_r3 hr = #clk hr
execute if score #ph hr matches 7 run scoreboard players add #cd_r3 hr 200
function rlk:boss/scarlet/p/r3/start
