# Weighted pick, P2, far (api.WEIGHTS; zeroed while cooling down / repeating / beyond MID_MAX).
scoreboard players set #ai_sum hr 0
scoreboard players set #ai_wa4 hr 20
execute if score #cd_a4 hr > #clk hr run scoreboard players set #ai_wa4 hr 0
execute if score #last hr matches 4 run scoreboard players set #ai_wa4 hr 0
scoreboard players operation #ai_sum hr += #ai_wa4 hr
scoreboard players set #ai_wa10 hr 10
execute if score #cd_a10 hr > #clk hr run scoreboard players set #ai_wa10 hr 0
execute if score #last hr matches 7 run scoreboard players set #ai_wa10 hr 0
scoreboard players operation #ai_sum hr += #ai_wa10 hr
scoreboard players set #ai_whcut hr 12
execute if score #cd_hcut hr > #clk hr run scoreboard players set #ai_whcut hr 0
execute if score #last hr matches 13 run scoreboard players set #ai_whcut hr 0
scoreboard players operation #ai_sum hr += #ai_whcut hr
scoreboard players set #ai_wmx hr 10
execute if score #cd_mx hr > #clk hr run scoreboard players set #ai_wmx hr 0
execute if score #last hr matches 16 run scoreboard players set #ai_wmx hr 0
scoreboard players operation #ai_sum hr += #ai_wmx hr
scoreboard players set #ai_wnb hr 35
execute if score #cd_nb hr > #clk hr run scoreboard players set #ai_wnb hr 0
execute if score #last hr matches 17 run scoreboard players set #ai_wnb hr 0
scoreboard players operation #ai_sum hr += #ai_wnb hr
scoreboard players set #ai_wq hr 20
execute if score #cd_q hr > #clk hr run scoreboard players set #ai_wq hr 0
execute if score #last hr matches 18 run scoreboard players set #ai_wq hr 0
scoreboard players operation #ai_sum hr += #ai_wq hr
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
execute if score #ai_r hr < #ai_wmx hr run return run function rlk:boss/scarlet/core/start/mx
scoreboard players operation #ai_r hr -= #ai_wmx hr
execute if score #ai_r hr < #ai_wnb hr run return run function rlk:boss/scarlet/core/start/nb
scoreboard players operation #ai_r hr -= #ai_wnb hr
execute if score #ai_r hr < #ai_wq hr run return run function rlk:boss/scarlet/core/start/q
scoreboard players operation #ai_r hr -= #ai_wq hr
function rlk:boss/scarlet/ai/none
