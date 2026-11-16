# Weighted pick, P1, far (api.WEIGHTS; zeroed while cooling down / repeating / beyond MID_MAX).
scoreboard players set #ai_sum hr 0
scoreboard players set #ai_wa4 hr 50
execute if score #cd_a4 hr > #clk hr run scoreboard players set #ai_wa4 hr 0
execute if score #last hr matches 4 run scoreboard players set #ai_wa4 hr 0
scoreboard players operation #ai_sum hr += #ai_wa4 hr
scoreboard players set #ai_wa10 hr 12
execute if score #cd_a10 hr > #clk hr run scoreboard players set #ai_wa10 hr 0
execute if score #last hr matches 7 run scoreboard players set #ai_wa10 hr 0
scoreboard players operation #ai_sum hr += #ai_wa10 hr
scoreboard players set #ai_whcut hr 14
execute if score #cd_hcut hr > #clk hr run scoreboard players set #ai_whcut hr 0
execute if score #last hr matches 13 run scoreboard players set #ai_whcut hr 0
scoreboard players operation #ai_sum hr += #ai_whcut hr
execute if score #ai_sum hr matches ..0 run return run function rlk:boss/scarlet/ai/none
execute store result score #ai_r hr run random value 0..999
scoreboard players operation #ai_r hr *= #ai_sum hr
scoreboard players operation #ai_r hr /= #c1000 hr
execute if score #ai_r hr < #ai_wa4 hr run return run function rlk:boss/scarlet/core/start/a4
scoreboard players operation #ai_r hr -= #ai_wa4 hr
execute if score #ai_r hr < #ai_wa10 hr run return run function rlk:boss/scarlet/core/start/a10
scoreboard players operation #ai_r hr -= #ai_wa10 hr
execute if score #ai_r hr < #ai_whcut hr run return run function rlk:boss/scarlet/core/start/hcut
scoreboard players operation #ai_r hr -= #ai_whcut hr
function rlk:boss/scarlet/ai/none
