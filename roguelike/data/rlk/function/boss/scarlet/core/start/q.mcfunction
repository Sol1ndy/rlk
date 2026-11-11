# Start Q 자영 포박 · 천공 낙월 (@s = body; the AI, the triggers, tests): the clock, the no-repeat memory, the
# cooldown of the fight phase.
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/rig/look/blade/edge
scoreboard players set #pat hr 18
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
scoreboard players set #ppf hr 0
scoreboard players set #ultq hr 0
scoreboard players set #hits hr 0
scoreboard players operation #last2 hr = #last hr
scoreboard players set #last hr 18
execute if score #ph hr matches 7 run scoreboard players operation #cd_q hr = #clk hr
execute if score #ph hr matches 7 run scoreboard players add #cd_q hr 300
function rlk:boss/scarlet/p/q/start
