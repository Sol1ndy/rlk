# Start ULT 공간 참 (@s = body; the AI, the triggers, tests): the clock, the no-repeat memory, the
# cooldown of the fight phase.
function rlk:boss/scarlet/core/stop_move
scoreboard players set #pat hr 12
scoreboard players set #pt hr 0
scoreboard players set #done hr 0
scoreboard players set #ppf hr 0
scoreboard players set #ultq hr 0
scoreboard players set #hits hr 0
scoreboard players operation #last2 hr = #last hr
scoreboard players set #last hr 12
function rlk:boss/scarlet/p/ult/start
