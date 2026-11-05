# The far rule, P2.
scoreboard players set #ai_sum hr 0
scoreboard players set #ai_wr1 hr 40
execute if score #cd_r1 hr > #clk hr run scoreboard players set #ai_wr1 hr 0
execute if score #last hr matches 11 run scoreboard players set #ai_wr1 hr 0
scoreboard players operation #ai_sum hr += #ai_wr1 hr
scoreboard players set #ai_wa4 hr 30
execute if score #cd_a4 hr > #clk hr run scoreboard players set #ai_wa4 hr 0
execute if score #last hr matches 4 run scoreboard players set #ai_wa4 hr 0
scoreboard players operation #ai_sum hr += #ai_wa4 hr
scoreboard players set #ai_wr2 hr 30
execute if score #cd_r2 hr > #clk hr run scoreboard players set #ai_wr2 hr 0
execute if score #last hr matches 12 run scoreboard players set #ai_wr2 hr 0
scoreboard players operation #ai_sum hr += #ai_wr2 hr
execute if score #ai_sum hr matches ..0 run return run function rlk:boss/scarlet/ai/far_none
execute store result score #ai_r hr run random value 0..999
scoreboard players operation #ai_r hr *= #ai_sum hr
scoreboard players operation #ai_r hr /= #c1000 hr
execute if score #ai_r hr < #ai_wr1 hr run return run function rlk:boss/scarlet/core/start/r1
scoreboard players operation #ai_r hr -= #ai_wr1 hr
execute if score #ai_r hr < #ai_wa4 hr run return run function rlk:boss/scarlet/core/start/a4
scoreboard players operation #ai_r hr -= #ai_wa4 hr
execute if score #ai_r hr < #ai_wr2 hr run return run function rlk:boss/scarlet/core/start/r2
scoreboard players operation #ai_r hr -= #ai_wr2 hr
function rlk:boss/scarlet/ai/far_none
