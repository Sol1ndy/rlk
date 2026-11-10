# The far rule, P2.
scoreboard players set #ai_sum hr 0
scoreboard players set #ai_wnb hr 40
execute if score #cd_nb hr > #clk hr run scoreboard players set #ai_wnb hr 0
execute if score #last hr matches 17 run scoreboard players set #ai_wnb hr 0
scoreboard players operation #ai_sum hr += #ai_wnb hr
scoreboard players set #ai_wq hr 30
execute if score #cd_q hr > #clk hr run scoreboard players set #ai_wq hr 0
execute if score #last hr matches 18 run scoreboard players set #ai_wq hr 0
scoreboard players operation #ai_sum hr += #ai_wq hr
scoreboard players set #ai_whcut hr 30
execute if score #cd_hcut hr > #clk hr run scoreboard players set #ai_whcut hr 0
execute if score #last hr matches 13 run scoreboard players set #ai_whcut hr 0
scoreboard players operation #ai_sum hr += #ai_whcut hr
execute if score #ai_sum hr matches ..0 run return run function rlk:boss/scarlet/ai/far_none
execute store result score #ai_r hr run random value 0..999
scoreboard players operation #ai_r hr *= #ai_sum hr
scoreboard players operation #ai_r hr /= #c1000 hr
execute if score #ai_r hr < #ai_wnb hr run return run function rlk:boss/scarlet/core/start/nb
scoreboard players operation #ai_r hr -= #ai_wnb hr
execute if score #ai_r hr < #ai_wq hr run return run function rlk:boss/scarlet/core/start/q
scoreboard players operation #ai_r hr -= #ai_wq hr
execute if score #ai_r hr < #ai_whcut hr run return run function rlk:boss/scarlet/core/start/hcut
scoreboard players operation #ai_r hr -= #ai_whcut hr
function rlk:boss/scarlet/ai/far_none
