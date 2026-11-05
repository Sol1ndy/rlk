# The counter: A2 now (when it may run).
scoreboard players set #ai_wa2 hr 1
execute if score #ph hr matches 1 if score #cd_a2 hr > #clk hr run scoreboard players set #ai_wa2 hr 0
execute if score #ph hr matches 1 if score #last hr matches 2 run scoreboard players set #ai_wa2 hr 0
execute if score #ph hr matches 7 if score #cd_a2 hr > #clk hr run scoreboard players set #ai_wa2 hr 0
execute if score #ph hr matches 7 if score #last hr matches 2 run scoreboard players set #ai_wa2 hr 0
execute unless score #ai_wa2 hr matches 1 run return fail
function rlk:boss/scarlet/core/start/a2
return 1
