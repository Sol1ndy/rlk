# Start R2 월륜 일섬 (@s = body; the AI, the triggers, tests): the clock, the no-repeat memory, the
# cooldown of the fight phase.
function rlk:boss/scarlet/core/stop_move
scoreboard players set #pat hr 12
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
scoreboard players set #hits hr 0
scoreboard players operation #last2 hr = #last hr
scoreboard players set #last hr 12
execute if score #ph hr matches 7 run scoreboard players operation #cd_r2 hr = #clk hr
execute if score #ph hr matches 7 run scoreboard players add #cd_r2 hr 260
function rlk:boss/scarlet/p/r2/start
