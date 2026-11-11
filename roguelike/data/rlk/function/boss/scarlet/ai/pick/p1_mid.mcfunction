# Weighted pick, P1, mid (api.WEIGHTS; zeroed while cooling down / repeating / beyond MID_MAX).
scoreboard players set #ai_sum hr 0
scoreboard players set #ai_wa3 hr 10
execute if score #cd_a3 hr > #clk hr run scoreboard players set #ai_wa3 hr 0
execute if score #last hr matches 3 run scoreboard players set #ai_wa3 hr 0
execute if score #ai_d2 hr matches 640001.. run scoreboard players set #ai_wa3 hr 0
scoreboard players operation #ai_sum hr += #ai_wa3 hr
scoreboard players set #ai_wa3s hr 15
execute if score #cd_a3s hr > #clk hr run scoreboard players set #ai_wa3s hr 0
execute if score #last hr matches 8 run scoreboard players set #ai_wa3s hr 0
execute if score #ai_d2 hr matches 640001.. run scoreboard players set #ai_wa3s hr 0
scoreboard players operation #ai_sum hr += #ai_wa3s hr
scoreboard players set #ai_wtri hr 30
execute if score #cd_tri hr > #clk hr run scoreboard players set #ai_wtri hr 0
execute if score #last hr matches 10 run scoreboard players set #ai_wtri hr 0
execute if score #ai_d2 hr matches 1000001.. run scoreboard players set #ai_wtri hr 0
scoreboard players operation #ai_sum hr += #ai_wtri hr
scoreboard players set #ai_wa4 hr 20
execute if score #cd_a4 hr > #clk hr run scoreboard players set #ai_wa4 hr 0
execute if score #last hr matches 4 run scoreboard players set #ai_wa4 hr 0
scoreboard players operation #ai_sum hr += #ai_wa4 hr
scoreboard players set #ai_wa9 hr 10
execute if score #cd_a9 hr > #clk hr run scoreboard players set #ai_wa9 hr 0
execute if score #last hr matches 6 run scoreboard players set #ai_wa9 hr 0
execute if score #ai_d2 hr matches 490001.. run scoreboard players set #ai_wa9 hr 0
scoreboard players operation #ai_sum hr += #ai_wa9 hr
scoreboard players set #ai_wa10 hr 20
execute if score #cd_a10 hr > #clk hr run scoreboard players set #ai_wa10 hr 0
execute if score #last hr matches 7 run scoreboard players set #ai_wa10 hr 0
scoreboard players operation #ai_sum hr += #ai_wa10 hr
scoreboard players set #ai_whcut hr 10
execute if score #cd_hcut hr > #clk hr run scoreboard players set #ai_whcut hr 0
execute if score #last hr matches 13 run scoreboard players set #ai_whcut hr 0
execute if score #ai_d2 hr matches ..639999 run scoreboard players set #ai_whcut hr 0
scoreboard players operation #ai_sum hr += #ai_whcut hr
scoreboard players set #ai_wblue hr 15
execute if score #cd_blue hr > #clk hr run scoreboard players set #ai_wblue hr 0
execute if score #last hr matches 14 run scoreboard players set #ai_wblue hr 0
execute if score #ai_d2 hr matches 490001.. run scoreboard players set #ai_wblue hr 0
scoreboard players operation #ai_sum hr += #ai_wblue hr
scoreboard players set #ai_wkcut hr 15
execute if score #cd_kcut hr > #clk hr run scoreboard players set #ai_wkcut hr 0
execute if score #last hr matches 15 run scoreboard players set #ai_wkcut hr 0
execute if score #ai_d2 hr matches 640001.. run scoreboard players set #ai_wkcut hr 0
scoreboard players operation #ai_sum hr += #ai_wkcut hr
execute if score #ai_sum hr matches ..0 run return run function rlk:boss/scarlet/ai/none
execute store result score #ai_r hr run random value 0..999
scoreboard players operation #ai_r hr *= #ai_sum hr
scoreboard players operation #ai_r hr /= #c1000 hr
execute if score #ai_r hr < #ai_wa3 hr run return run function rlk:boss/scarlet/core/start/a3
scoreboard players operation #ai_r hr -= #ai_wa3 hr
execute if score #ai_r hr < #ai_wa3s hr run return run function rlk:boss/scarlet/core/start/a3s
scoreboard players operation #ai_r hr -= #ai_wa3s hr
execute if score #ai_r hr < #ai_wtri hr run return run function rlk:boss/scarlet/core/start/tri
scoreboard players operation #ai_r hr -= #ai_wtri hr
execute if score #ai_r hr < #ai_wa4 hr run return run function rlk:boss/scarlet/core/start/a4
scoreboard players operation #ai_r hr -= #ai_wa4 hr
execute if score #ai_r hr < #ai_wa9 hr run return run function rlk:boss/scarlet/core/start/a9
scoreboard players operation #ai_r hr -= #ai_wa9 hr
execute if score #ai_r hr < #ai_wa10 hr run return run function rlk:boss/scarlet/core/start/a10
scoreboard players operation #ai_r hr -= #ai_wa10 hr
execute if score #ai_r hr < #ai_whcut hr run return run function rlk:boss/scarlet/core/start/hcut
scoreboard players operation #ai_r hr -= #ai_whcut hr
execute if score #ai_r hr < #ai_wblue hr run return run function rlk:boss/scarlet/core/start/blue
scoreboard players operation #ai_r hr -= #ai_wblue hr
execute if score #ai_r hr < #ai_wkcut hr run return run function rlk:boss/scarlet/core/start/kcut
scoreboard players operation #ai_r hr -= #ai_wkcut hr
function rlk:boss/scarlet/ai/none
