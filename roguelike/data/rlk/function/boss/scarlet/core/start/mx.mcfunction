# Start MX 자광 십자참 (@s = body; the AI, the triggers, tests): the clock, the no-repeat memory, the
# cooldown of the fight phase.
function rlk:boss/scarlet/core/stop_move
scoreboard players set #pat hr 16
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
scoreboard players set #ppf hr 0
scoreboard players set #ultq hr 0
scoreboard players set #hits hr 0
scoreboard players operation #last2 hr = #last hr
scoreboard players set #last hr 16
execute if score #ph hr matches 7 run scoreboard players operation #cd_mx hr = #clk hr
execute if score #ph hr matches 7 run scoreboard players add #cd_mx hr 150
function rlk:boss/scarlet/p/mx/start
