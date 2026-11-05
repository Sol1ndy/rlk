# The counter: A1 now (when it may run).
scoreboard players set #ai_wa1 hr 1
execute if score #ph hr matches 1 if score #cd_a1 hr > #clk hr run scoreboard players set #ai_wa1 hr 0
execute if score #ph hr matches 1 if score #last hr matches 1 run scoreboard players set #ai_wa1 hr 0
execute if score #ph hr matches 7 if score #cd_a1 hr > #clk hr run scoreboard players set #ai_wa1 hr 0
execute if score #ph hr matches 7 if score #last hr matches 1 run scoreboard players set #ai_wa1 hr 0
execute unless score #ai_wa1 hr matches 1 run return fail
function rlk:boss/scarlet/core/start/a1
return 1
